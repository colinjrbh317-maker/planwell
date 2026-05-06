"""
Sync webinars.ts from Zoom
==========================
Pulls upcoming "FERS Retirement Workshop" webinars from Zoom, regenerates the
schedule block in src/data/webinars.ts, and writes the file in place.

Idempotent: if the file already matches Zoom, exits 0 with no diff.
Designed to be run by GitHub Actions (triggered nightly by N8N).

Env required:
    ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET

Exit codes:
    0  success (changed or unchanged)
    1  Zoom API failure
    2  parse failure (webinars.ts shape unexpected)
"""
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

import zoom_client as z

REPO_ROOT = Path(__file__).resolve().parent.parent
WEBINARS_TS = REPO_ROOT / 'src' / 'data' / 'webinars.ts'
TARGET_TOPIC = 'FERS Retirement Workshop'
EASTERN = ZoneInfo('America/New_York')


def fetch_workshops():
    """Return list of upcoming FERS workshops from Zoom (full details), sorted by start_time."""
    items = z.list_upcoming_webinars()
    workshops = [w for w in items if TARGET_TOPIC.lower() in (w.get('topic') or '').lower()]
    workshops.sort(key=lambda w: w.get('start_time', ''))
    headers = z._headers()
    detailed = []
    for w in workshops:
        try:
            r = requests.get(f'https://api.zoom.us/v2/webinars/{w["id"]}', headers=headers, timeout=10)
            if r.status_code == 200:
                detailed.append({**w, **r.json()})
            else:
                detailed.append(w)
        except Exception:
            detailed.append(w)
    return detailed


def webinar_to_entry(w):
    """Convert a Zoom webinar dict to the webinars.ts entry dict."""
    start_utc = datetime.fromisoformat(w['start_time'].replace('Z', '+00:00'))
    start_local = start_utc.astimezone(EASTERN)
    duration_min = int(w.get('duration', 180))
    end_local = start_local.replace(minute=0) + (start_utc - start_utc)  # placeholder, computed below
    end_local = (start_local.replace(tzinfo=EASTERN))
    end_h = start_local.hour + duration_min // 60
    end_m = duration_min % 60
    is_dst = bool(start_local.dst())
    offset = '-04:00' if is_dst else '-05:00'
    tz_label = 'EDT' if is_dst else 'EST'

    month_str = start_local.strftime('%b').lower()
    entry_id = f"{month_str}-{start_local.day:02d}-{start_local.year}"
    iso_date = start_local.strftime(f'%Y-%m-%dT%H:%M:%S{offset}')

    def fmt12(h, m):
        period = 'AM' if h < 12 else 'PM'
        h12 = h - 12 if h > 12 else (12 if h == 0 else h)
        return f'{h12}:{m:02d} {period}'

    return {
        'id': entry_id,
        'iso_date': iso_date,
        'title': TARGET_TOPIC,
        'startTime': fmt12(start_local.hour, start_local.minute),
        'endTime': fmt12(end_h % 24, end_m),
        'timezone': tz_label,
        'zoomLink': w.get('registration_url') or w.get('join_url') or '',
    }


def render_entries(entries):
    lines = []
    for e in entries:
        zoom_line = f"        zoomLink: '{e['zoomLink']}',\n" if e['zoomLink'] else ''
        lines.append(
            "    {\n"
            f"        id: '{e['id']}',\n"
            f"        date: new Date('{e['iso_date']}'),\n"
            f"        title: '{e['title']}',\n"
            f"        startTime: '{e['startTime']}',\n"
            f"        endTime: '{e['endTime']}',\n"
            f"        timezone: '{e['timezone']}',\n"
            f"{zoom_line}"
            "    },"
        )
    return '\n'.join(lines)


ARRAY_RE = re.compile(
    r'(export const webinars: Webinar\[\] = \[)(.*?)(\n\];)',
    re.DOTALL,
)


def update_file(rendered_block: str) -> bool:
    text = WEBINARS_TS.read_text()
    m = ARRAY_RE.search(text)
    if not m:
        print('ERR: could not locate webinars[] in webinars.ts', file=sys.stderr)
        sys.exit(2)

    new_text = text[: m.start(2)] + '\n' + rendered_block + '\n' + text[m.end(2):]
    if new_text == text:
        return False
    WEBINARS_TS.write_text(new_text)
    return True


def main():
    workshops = fetch_workshops()
    if not workshops:
        print('No upcoming FERS workshops found on Zoom — leaving file untouched.')
        return 0

    entries = [webinar_to_entry(w) for w in workshops]
    rendered = render_entries(entries)
    changed = update_file(rendered)
    if changed:
        print(f'Updated webinars.ts with {len(entries)} upcoming webinars:')
        for e in entries:
            print(f"  - {e['id']} ({e['iso_date']})")
    else:
        print(f'webinars.ts already up to date ({len(entries)} entries).')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f'ERR: {e}', file=sys.stderr)
        sys.exit(1)
