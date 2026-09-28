"""
Webinar calendar links
======================
Builds the "Add to Calendar" options for the registration confirmation email.

Why this exists: the confirmation email used to carry only a Google Calendar
"render?action=TEMPLATE" link. For Outlook and Apple users (most PlanWell
registrants are on government or corporate Outlook) that link opens a Google
web page and never produces an invitation file. The fix is a real .ics file.

Mailchimp campaigns (our send path) cannot carry attachments, so the .ics is
served by the webhook server at /api/webinar/calendar.ics. The link carries
the start time, type and the registrant's personal join URL, and is signed
with an HMAC so the endpoint cannot be used to mint arbitrary calendar files
with somebody else's links in them.
"""

import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone
from urllib.parse import quote, urlencode


def _nth_sunday(year, month, n):
    d = datetime(year, month, 1)
    d += timedelta(days=(6 - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def to_new_york(dt_utc):
    """UTC -> America/New_York wall time (naive), using current US DST rules.

    Done by hand rather than with zoneinfo because the slim Docker image the
    webhook runs on is not guaranteed to ship tzdata, and a silent fallback to
    UTC would put the event at the wrong hour in every calendar.
    """
    dt_utc = dt_utc.astimezone(timezone.utc).replace(tzinfo=None)
    y = dt_utc.year
    dst_start_utc = _nth_sunday(y, 3, 2) + timedelta(hours=7)   # 2:00 EST
    dst_end_utc = _nth_sunday(y, 11, 1) + timedelta(hours=6)    # 2:00 EDT
    offset = -4 if dst_start_utc <= dt_utc < dst_end_utc else -5
    return dt_utc + timedelta(hours=offset)


WEBINAR_TYPES = {
    'fers': {
        'title': 'FERS Retirement Workshop (PlanWell)',
        'duration_min': 180,
        'summary': ('Free 3-hour FERS workshop with David Fei, CFP and Brennan Rhule, CFP. '
                    'Covers pension, TSP, FEHB, FEGLI and survivor benefits.'),
        'filename': 'PlanWell-FERS-Workshop.ics',
    },
    'tsp': {
        'title': 'TSP Investment Strategies Workshop (PlanWell)',
        'duration_min': 60,
        'summary': ('Free 1-hour TSP workshop with David Fei, CFP. Covers fund allocation, '
                    'Roth TSP and withdrawal strategies.'),
        'filename': 'PlanWell-TSP-Workshop.ics',
    },
}

DEFAULT_PUBLIC_BASE = 'https://pleasant-vision-production.up.railway.app'


def public_base_url():
    base = os.environ.get('WEBHOOK_PUBLIC_URL', '').strip()
    if not base:
        domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '').strip()
        base = f'https://{domain}' if domain else DEFAULT_PUBLIC_BASE
    return base.rstrip('/')


def _signing_key():
    explicit = os.environ.get('CALENDAR_LINK_SECRET', '').strip()
    if explicit:
        return explicit.encode()
    # Derive from a secret the service already has, so no new env var is
    # required to deploy. Rotating the Zoom secret invalidates old links,
    # which only matters for emails already sent (the Google/Outlook web
    # links in them keep working).
    seed = os.environ.get('ZOOM_CLIENT_SECRET', '').strip() or 'planwell-calendar'
    return hashlib.sha256(('planwell-ics:' + seed).encode()).digest()


def _canonical(webinar_type, start, join_url, passcode):
    return '\n'.join([webinar_type or '', start or '', join_url or '', passcode or ''])


def sign(webinar_type, start, join_url, passcode=''):
    msg = _canonical(webinar_type, start, join_url, passcode).encode()
    return hmac.new(_signing_key(), msg, hashlib.sha256).hexdigest()[:32]


def verify(webinar_type, start, join_url, passcode, sig):
    if not sig:
        return False
    return hmac.compare_digest(sign(webinar_type, start, join_url, passcode), sig)


def parse_start(value):
    """Accept ISO 8601 (with Z or offset) or compact UTC (20261016T150000Z)."""
    value = (value or '').strip()
    if not value:
        raise ValueError('empty start')
    if len(value) == 16 and value.endswith('Z') and 'T' in value and '-' not in value:
        return datetime.strptime(value, '%Y%m%dT%H%M%SZ').replace(tzinfo=timezone.utc)
    dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        raise ValueError('start must carry a timezone')
    return dt.astimezone(timezone.utc)


def compact_utc(dt):
    return dt.astimezone(timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def _details(webinar_type, join_url, passcode):
    info = WEBINAR_TYPES.get(webinar_type, WEBINAR_TYPES['fers'])
    lines = [info['summary'], '']
    if join_url:
        lines += ['Join the workshop (this link is personal to you):', join_url]
        if passcode:
            lines += ['Passcode, if Zoom asks for one: ' + passcode]
        lines += ['', 'No Zoom account needed. On a computer you can choose '
                      '"Join from your browser".']
    else:
        lines += ['Your personal Zoom join link is in your confirmation email.']
    lines += ['', 'Questions? Email info@planwellfp.com']
    return '\n'.join(lines)


def ics_link(webinar_type, start_utc, join_url, passcode=''):
    start = compact_utc(start_utc)
    params = {'t': webinar_type, 's': start, 'j': join_url or ''}
    if passcode:
        params['p'] = passcode
    params['sig'] = sign(webinar_type, start, join_url or '', passcode or '')
    return public_base_url() + '/api/webinar/calendar.ics?' + urlencode(params)


def google_link(webinar_type, start_utc, join_url, passcode=''):
    info = WEBINAR_TYPES.get(webinar_type, WEBINAR_TYPES['fers'])
    end = start_utc + timedelta(minutes=info['duration_min'])
    return (
        'https://calendar.google.com/calendar/render?action=TEMPLATE'
        '&text=' + quote(info['title']) +
        '&dates=' + compact_utc(start_utc) + '/' + compact_utc(end) +
        '&ctz=America/New_York'
        '&details=' + quote(_details(webinar_type, join_url, passcode)) +
        '&location=' + quote(join_url or 'Online via Zoom')
    )


def outlook_web_link(webinar_type, start_utc, join_url, passcode=''):
    """Outlook on the web (works for both Microsoft 365 work and outlook.com accounts)."""
    info = WEBINAR_TYPES.get(webinar_type, WEBINAR_TYPES['fers'])
    end = start_utc + timedelta(minutes=info['duration_min'])
    iso = lambda d: d.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    params = {
        'path': '/calendar/action/compose',
        'rru': 'addevent',
        'subject': info['title'],
        'startdt': iso(start_utc),
        'enddt': iso(end),
        'body': _details(webinar_type, join_url, passcode),
        'location': join_url or 'Online via Zoom',
    }
    return 'https://outlook.office.com/calendar/0/deeplink/compose?' + urlencode(params, quote_via=quote)


# ---------------------------------------------------------------------------
# .ics generation (RFC 5545)
# ---------------------------------------------------------------------------

def _escape(text):
    return (text.replace('\\', '\\\\').replace(';', '\\;')
            .replace(',', '\\,').replace('\r\n', '\\n').replace('\n', '\\n'))


def _fold(line):
    """Fold to 75 octets per line without splitting a UTF-8 character."""
    out = []
    current = ''
    limit = 75
    for ch in line:
        if len((current + ch).encode('utf-8')) > limit:
            out.append(current)
            current = ' ' + ch
            limit = 75
        else:
            current += ch
    out.append(current)
    return '\r\n'.join(out)


_VTIMEZONE_NY = [
    'BEGIN:VTIMEZONE',
    'TZID:America/New_York',
    'BEGIN:DAYLIGHT',
    'TZOFFSETFROM:-0500',
    'TZOFFSETTO:-0400',
    'TZNAME:EDT',
    'DTSTART:19700308T020000',
    'RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU',
    'END:DAYLIGHT',
    'BEGIN:STANDARD',
    'TZOFFSETFROM:-0400',
    'TZOFFSETTO:-0500',
    'TZNAME:EST',
    'DTSTART:19701101T020000',
    'RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU',
    'END:STANDARD',
    'END:VTIMEZONE',
]


def build_ics(webinar_type, start_utc, join_url, passcode='', now=None):
    info = WEBINAR_TYPES.get(webinar_type, WEBINAR_TYPES['fers'])
    start_utc = start_utc.astimezone(timezone.utc)
    end_utc = start_utc + timedelta(minutes=info['duration_min'])
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)

    fmt = lambda d: to_new_york(d).strftime('%Y%m%dT%H%M%S')
    dtstart = 'DTSTART;TZID=America/New_York:' + fmt(start_utc)
    dtend = 'DTEND;TZID=America/New_York:' + fmt(end_utc)

    # Stable per registrant and session, so re-opening the file updates the
    # same event instead of creating a duplicate.
    uid_seed = f'{webinar_type}|{compact_utc(start_utc)}|{join_url or ""}'
    uid = hashlib.sha256(uid_seed.encode()).hexdigest()[:24] + '@planwellfp.com'

    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//PlanWell Financial Planning//Webinar//EN',
        'CALSCALE:GREGORIAN',
        'METHOD:PUBLISH',
        *_VTIMEZONE_NY,
        'BEGIN:VEVENT',
        'UID:' + uid,
        'DTSTAMP:' + compact_utc(now),
        dtstart,
        dtend,
        'SUMMARY:' + _escape(info['title']),
        'DESCRIPTION:' + _escape(_details(webinar_type, join_url, passcode)),
        'LOCATION:' + _escape(join_url or 'Online via Zoom'),
    ]
    if join_url:
        lines.append('URL:' + join_url)
    lines += [
        'STATUS:CONFIRMED',
        'TRANSP:OPAQUE',
        'BEGIN:VALARM',
        'ACTION:DISPLAY',
        'DESCRIPTION:' + _escape(info['title'] + ' starts in 30 minutes'),
        'TRIGGER:-PT30M',
        'END:VALARM',
        'END:VEVENT',
        'END:VCALENDAR',
    ]
    return '\r\n'.join(_fold(l) for l in lines) + '\r\n'


def calendar_links(webinar_type, start_utc, join_url, passcode=''):
    return {
        'ics': ics_link(webinar_type, start_utc, join_url, passcode),
        'google': google_link(webinar_type, start_utc, join_url, passcode),
        'outlook_web': outlook_web_link(webinar_type, start_utc, join_url, passcode),
    }
