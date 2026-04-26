"""
send_webinar_email.py
=====================
One-shot orchestrator for pre-webinar email sends.

Pulls registrants from Zoom (source of truth), upserts them into Mailchimp
with the appropriate registration tag, then sends the stage-specific email
via Mailchimp's campaign API. Idempotent: skips registrants who already
have the per-stage sent tag.

Usage:
    # Dry run (counts only, no sends, no tag writes)
    python3 send_webinar_email.py --webinar-date 2026-05-01 --stage 5day --dry-run

    # Test send to a single inbox
    python3 send_webinar_email.py --webinar-date 2026-05-01 --stage 5day --test you@example.com

    # Real production send to all Zoom registrants
    python3 send_webinar_email.py --webinar-date 2026-05-01 --stage 5day

Stages: 5day | 1day | dayof  (only 5day implemented in this revision)
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote_plus

EXEC_DIR = Path(__file__).parent
sys.path.insert(0, str(EXEC_DIR))

from zoom_client import find_webinar_by_date, list_webinar_registrants
from mailchimp_client import (
    add_subscriber_or_update,
    get_member_tags,
    update_member_tags,
)
from webinar_emails import send_webinar_5day, send_webinar_1day_mc, send_webinar_dayof_mc, send_webinar_final_mc


WEBINAR_HUMAN_DATES = {
    '2026-05-01': 'Friday, May 1',
}

# UTC start/end for each known webinar (used to build calendar links)
WEBINAR_UTC = {
    '2026-05-01': {
        'start_utc': '20260501T150000Z',
        'end_utc':   '20260501T180000Z',
        'start_iso': '2026-05-01T15:00:00Z',
        'end_iso':   '2026-05-01T18:00:00Z',
    },
}


def build_calendar_urls(webinar_date_iso):
    """Generate Google / Outlook / Apple calendar add-event URLs."""
    times = WEBINAR_UTC[webinar_date_iso]
    title = 'FERS Retirement Workshop'
    details = 'Free 3-hour FERS Retirement Workshop with David Fei, CFP and Brennan Rhule, CFP. Online via Zoom. Your join link will arrive the day before.'
    location = 'Online via Zoom'

    google = (
        'https://calendar.google.com/calendar/render?action=TEMPLATE'
        f'&text={quote_plus(title)}'
        f'&dates={times["start_utc"]}/{times["end_utc"]}'
        f'&details={quote_plus(details)}'
        f'&location={quote_plus(location)}'
    )
    outlook = (
        'https://outlook.live.com/calendar/0/deeplink/compose'
        f'?subject={quote_plus(title)}'
        f'&startdt={quote_plus(times["start_iso"])}'
        f'&enddt={quote_plus(times["end_iso"])}'
        f'&body={quote_plus(details)}'
        f'&location={quote_plus(location)}'
    )
    apple = f'https://planwellfp.com/calendar/fers-{webinar_date_iso[5:7]}-{webinar_date_iso[8:10]}-{webinar_date_iso[:4]}.ics'
    # Final apple URL convention matches the .ics we created: fers-may-01-2026.ics
    # Override for May 1:
    if webinar_date_iso == '2026-05-01':
        apple = 'https://planwellfp.com/calendar/fers-may-01-2026.ics'

    return google, outlook, apple


def webinar_id_tag(webinar_date_iso):
    """Convert 2026-05-01 -> may-01-2026."""
    months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    y, m, d = webinar_date_iso.split('-')
    return f'{months[int(m)-1]}-{d}-{y}'


def send_for_stage(stage, registrant, webinar_human_date, cal_urls, dry_run=False):
    """Dispatch to the correct send_webinar_*  function. Returns bool."""
    g, o, a = cal_urls
    if stage == '5day':
        if dry_run:
            print(f"      [DRY RUN] Would send 5day to {registrant['email']}")
            return True
        return send_webinar_5day(
            to_email=registrant['email'],
            first_name=registrant['first_name'] or 'there',
            webinar_date=webinar_human_date,
            google_cal_url=g,
            outlook_cal_url=o,
            apple_cal_url=a,
        )
    elif stage == '1day':
        zoom_link = registrant.get('join_url') or 'https://zoom.us/'
        if dry_run:
            print(f"      [DRY RUN] Would send 1day to {registrant['email']} (link {zoom_link[:40]}...)")
            return True
        return send_webinar_1day_mc(
            to_email=registrant['email'],
            first_name=registrant['first_name'] or 'there',
            webinar_date=webinar_human_date,
            zoom_link=zoom_link,
        )
    elif stage == 'dayof':
        zoom_link = registrant.get('join_url') or 'https://zoom.us/'
        if dry_run:
            print(f"      [DRY RUN] Would send dayof to {registrant['email']} (link {zoom_link[:40]}...)")
            return True
        return send_webinar_dayof_mc(
            to_email=registrant['email'],
            first_name=registrant['first_name'] or 'there',
            zoom_link=zoom_link,
        )
    elif stage == 'final':
        zoom_link = registrant.get('join_url') or 'https://zoom.us/'
        if dry_run:
            print(f"      [DRY RUN] Would send final to {registrant['email']} (link {zoom_link[:40]}...)")
            return True
        return send_webinar_final_mc(
            to_email=registrant['email'],
            first_name=registrant['first_name'] or 'there',
            zoom_link=zoom_link,
        )
    else:
        raise ValueError(f"Unknown stage: {stage}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--webinar-date', required=True, help='ISO date e.g. 2026-05-01')
    parser.add_argument('--stage', required=True, choices=['5day', '1day', 'dayof', 'final'])
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--test', metavar='EMAIL', help='Send only to this address (using Test First name)')
    args = parser.parse_args()

    webinar_date_iso = args.webinar_date
    stage = args.stage
    webinar_id_str = webinar_id_tag(webinar_date_iso)            # 'may-01-2026'
    webinar_human_date = WEBINAR_HUMAN_DATES.get(webinar_date_iso, webinar_date_iso)

    register_tag = f'fers-registered-{webinar_id_str}'
    sent_tag = f'fers-email-{stage}-sent-{webinar_id_str}'

    cal_urls = build_calendar_urls(webinar_date_iso)

    print('=' * 64)
    print(f'send_webinar_email | stage={stage} | webinar={webinar_date_iso}')
    print(f'  register_tag = {register_tag}')
    print(f'  sent_tag     = {sent_tag}')
    print(f'  dry_run      = {args.dry_run}')
    print(f'  test         = {args.test or "(none)"}')
    print('=' * 64)

    log = {
        'started_at': datetime.now(timezone.utc).isoformat(),
        'webinar_date': webinar_date_iso,
        'stage': stage,
        'dry_run': args.dry_run,
        'test_recipient': args.test,
        'results': [],
    }

    # ---- Test mode: single recipient, skip Zoom/Mailchimp tagging ----
    if args.test:
        print(f'\n[TEST MODE] Sending {stage} to {args.test} only.')
        # Subscribe test recipient if needed (uses TEST as name)
        if not args.dry_run:
            up = add_subscriber_or_update(
                email=args.test,
                first_name='Colin',
                last_name='Test',
                tags=[register_tag, 'test-recipient'],
            )
            print(f'  Mailchimp upsert: {up}')

        ok = send_for_stage(
            stage,
            {
                'email': args.test,
                'first_name': 'Colin',
                'last_name': 'Test',
                'join_url': 'https://us02web.zoom.us/w/PLACEHOLDER_TEST_LINK',
            },
            webinar_human_date,
            cal_urls,
            dry_run=args.dry_run,
        )
        log['results'].append({'email': args.test, 'sent': bool(ok), 'mode': 'test'})
        print(f'\nTest send {"succeeded" if ok else "FAILED"}')
        _write_log(log, webinar_date_iso, stage, suffix='test')
        return 0 if ok else 1

    # ---- Real run: pull from Zoom ----
    print(f'\nLooking up Zoom webinar for {webinar_date_iso}...')
    webinar_id = find_webinar_by_date(webinar_date_iso)
    if not webinar_id:
        print(f'ERROR: No Zoom webinar found for {webinar_date_iso}')
        return 2
    print(f'  Webinar ID: {webinar_id}')

    print(f'\nFetching approved registrants from Zoom...')
    registrants = list_webinar_registrants(webinar_id)
    print(f'  Found {len(registrants)} approved registrants')

    if not registrants:
        print('No registrants. Exiting.')
        _write_log(log, webinar_date_iso, stage)
        return 0

    sent_count = 0
    skipped_count = 0
    failed_count = 0

    for i, r in enumerate(registrants, 1):
        email = r['email']
        first = r['first_name'] or 'there'
        last = r['last_name'] or ''
        print(f'\n  [{i}/{len(registrants)}] {first} {last} <{email}>')

        if not email:
            print('    SKIP: no email')
            skipped_count += 1
            log['results'].append({'email': '', 'sent': False, 'reason': 'no-email'})
            continue

        # Upsert into Mailchimp + apply register tag (idempotent)
        if not args.dry_run:
            up = add_subscriber_or_update(
                email=email,
                first_name=first,
                last_name=last,
                tags=[register_tag],
            )
            if not up.get('success'):
                print(f'    Mailchimp upsert failed: {up}')
                failed_count += 1
                log['results'].append({'email': email, 'sent': False, 'reason': 'upsert-failed', 'detail': up})
                continue
        else:
            print(f'    [DRY RUN] Would upsert {email} with tag {register_tag}')

        # Skip if already sent (idempotent across re-runs)
        if not args.dry_run:
            existing_tags = get_member_tags(email)
            if sent_tag in existing_tags:
                print(f'    SKIP: already has {sent_tag}')
                skipped_count += 1
                log['results'].append({'email': email, 'sent': False, 'reason': 'already-sent'})
                continue

        ok = send_for_stage(stage, r, webinar_human_date, cal_urls, dry_run=args.dry_run)

        if ok and not args.dry_run:
            tag_res = update_member_tags(email, tags_to_add=[sent_tag])
            if not tag_res.get('success'):
                print(f'    WARN: send succeeded but sent-tag write failed: {tag_res}')
            sent_count += 1
            log['results'].append({'email': email, 'sent': True})
            time.sleep(0.4)  # gentle on Mailchimp API
        elif ok and args.dry_run:
            sent_count += 1
            log['results'].append({'email': email, 'sent': True, 'mode': 'dry-run'})
        else:
            failed_count += 1
            log['results'].append({'email': email, 'sent': False, 'reason': 'send-failed'})

    print('\n' + '=' * 64)
    print(f'DONE | sent={sent_count} | skipped={skipped_count} | failed={failed_count} | total={len(registrants)}')
    print('=' * 64)

    _write_log(log, webinar_date_iso, stage)
    return 0 if failed_count == 0 else 3


def _write_log(log, webinar_date_iso, stage, suffix=''):
    tmp_dir = EXEC_DIR.parent / '.tmp'
    tmp_dir.mkdir(exist_ok=True)
    fname = f'sends_{webinar_date_iso}_{stage}'
    if suffix:
        fname += f'_{suffix}'
    fname += '.json'
    path = tmp_dir / fname
    with open(path, 'w') as f:
        json.dump(log, f, indent=2)
    print(f'Log: {path}')


if __name__ == '__main__':
    sys.exit(main())
