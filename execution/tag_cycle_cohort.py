#!/usr/bin/env python3
"""
Tag Cycle Cohort in Mailchimp
==============================

Reads a Zoom attendee report CSV from a webinar-{date}-debrief folder,
scrubs test rows + panelists + duplicates, splits into attendees vs no-shows,
and pushes two tags to Mailchimp:

  - webinar-attended-{cycle}
  - webinar-noshow-{cycle}

DOES NOT SEND EMAILS. Mailchimp UI handles the actual send once Colin
approves the drafted copy in campaigns/nurture/{cycle}/.

Usage:
    python execution/tag_cycle_cohort.py \\
        --cycle 2026-04-cycle \\
        --csv "../webinar-2026-04-10-debrief/Meeting History Apr 10 2026.csv" \\
        --dry-run

    # Live:
    python execution/tag_cycle_cohort.py \\
        --cycle 2026-04-cycle \\
        --csv "../webinar-2026-04-10-debrief/Meeting History Apr 10 2026.csv"
"""

import argparse
import csv
import re
import sys
from pathlib import Path
from collections import defaultdict

# Emails we always exclude (panelists, David's test, hot leads handled manually)
ALWAYS_EXCLUDE = {
    'david.fei@planwellfp.com',
    'brennan.rhule@planwellfp.com',
    'brennan.rhule@gmail.com',
    'thefobster@outlook.com',  # David's personal test
    'joetsilva@msn.com',       # Joseph Silva — David handled Apr 11 directly
}

# Substring patterns that mark a test/debug row
TEST_PATTERNS = [
    'test-delete-me',
    'testdebug',
    'bufftest',
    'buff.verify',
    'webhook',
    'debugtest',
    'zoomtest',
    'manualtest',
    'directtest',
    'finaltest',
    'livetest',
    'planwelltest',
    'colin+webinartest',
    'colinjrbh317+',
    '@testing.com',
    '@example.com',
]


def is_test_email(email: str) -> bool:
    email_lower = email.lower().strip()
    if not email_lower or '@' not in email_lower:
        return True
    return any(pat in email_lower for pat in TEST_PATTERNS)


def parse_attendee_report(csv_path: Path):
    """
    Parse the Zoom attendee report. The file has a quirky multi-section
    structure: summary, host, panelist, then attendee details.

    Returns: list of dicts with {email, first_name, last_name, attended, time_in_session}
    """
    rows = []
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        in_attendee_section = False
        header = None
        for row in reader:
            if not row:
                continue
            if row[0] == 'Attendee Details':
                in_attendee_section = True
                continue
            if in_attendee_section and header is None:
                header = row
                continue
            if in_attendee_section and header:
                # row fields: Attended, User Name, First Name, Last Name, Email,
                # Registration Time, Approval Status, Join Time, Leave Time,
                # Time in Session (minutes), Is Guest, Country
                if len(row) < 10:
                    continue
                attended = row[0].strip().lower() == 'yes'
                first_name = row[2].strip()
                last_name = row[3].strip()
                email = row[4].strip()
                approval = row[6].strip().lower() if len(row) > 6 else ''
                time_in_session = row[9].strip() if len(row) > 9 else '0'

                # Drop cancelled rows
                if 'cancelled' in approval:
                    continue

                try:
                    minutes = int(time_in_session) if time_in_session not in ('', '--') else 0
                except ValueError:
                    minutes = 0

                rows.append({
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'attended': attended,
                    'minutes': minutes,
                })
    return rows


def dedupe_by_email(rows):
    """Keep one row per email, picking the one with the highest minutes."""
    by_email = {}
    for r in rows:
        key = r['email'].lower().strip()
        if not key:
            continue
        if key not in by_email or r['minutes'] > by_email[key]['minutes']:
            by_email[key] = r
    return list(by_email.values())


def scrub_and_split(rows):
    """Apply all exclusions and return (attendees, noshows)."""
    clean = []
    for r in rows:
        email = r['email'].lower().strip()
        if email in ALWAYS_EXCLUDE:
            continue
        if is_test_email(email):
            continue
        clean.append(r)
    clean = dedupe_by_email(clean)
    attendees = [r for r in clean if r['attended']]
    noshows = [r for r in clean if not r['attended']]
    return attendees, noshows


def print_list(label, rows):
    print(f"\n{label} ({len(rows)}):")
    for r in sorted(rows, key=lambda x: x['email'].lower()):
        print(f"  {r['email']:<45} {r['first_name']} {r['last_name']} ({r['minutes']}m)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cycle', required=True, help='e.g. 2026-04-cycle')
    ap.add_argument('--csv', required=True, help='Path to Zoom attendee report CSV')
    ap.add_argument('--dry-run', action='store_true', help='Print lists, do NOT touch Mailchimp')
    args = ap.parse_args()

    csv_path = Path(args.csv).expanduser().resolve()
    if not csv_path.exists():
        print(f"ERROR: CSV not found: {csv_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {csv_path}")
    rows = parse_attendee_report(csv_path)
    print(f"Parsed {len(rows)} raw rows from attendee section")

    attendees, noshows = scrub_and_split(rows)
    print_list("ATTENDEES (will receive Day-1 attendee email)", attendees)
    print_list("NO-SHOWS (will receive Day-1 no-show email)", noshows)

    attended_tag = f"webinar-attended-{args.cycle}"
    noshow_tag = f"webinar-noshow-{args.cycle}"

    print(f"\nTags to apply:")
    print(f"  {attended_tag}  -> {len(attendees)} members")
    print(f"  {noshow_tag}    -> {len(noshows)} members")

    # Sanity checks
    excluded_safety_net = {'joetsilva@msn.com', 'david.fei@planwellfp.com'}
    all_emails = {r['email'].lower() for r in attendees + noshows}
    leaked = excluded_safety_net & all_emails
    if leaked:
        print(f"\n❌ SAFETY NET TRIGGERED: {leaked} leaked into output. Aborting.", file=sys.stderr)
        sys.exit(2)
    print("✅ Safety net check passed (Joseph Silva excluded, panelists excluded)")

    if args.dry_run:
        print("\n[DRY RUN] Not touching Mailchimp. Re-run without --dry-run to push tags.")
        return

    # Live mode — import Mailchimp client only when actually needed
    from mailchimp_client import batch_tag_members

    print(f"\nPushing {attended_tag}...")
    attended_result = batch_tag_members([r['email'] for r in attendees], attended_tag)
    print(f"  {attended_result}")

    print(f"\nPushing {noshow_tag}...")
    noshow_result = batch_tag_members([r['email'] for r in noshows], noshow_tag)
    print(f"  {noshow_result}")

    print("\n✅ Tags applied. Next step: Mailchimp UI → create two campaigns targeting these tags.")
    print("   See campaigns/nurture/RUNBOOK-next-cycle.md")


if __name__ == '__main__':
    main()
