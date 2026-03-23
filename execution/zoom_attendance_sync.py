"""
Zoom-to-Mailchimp Attendance Sync
==================================
Automates post-webinar attendance tracking:
1. Pulls participant data from Zoom (who actually joined)
2. Cross-references against registrants to determine attended vs no-show
3. Updates Google Sheet 'Attended' column for each registrant
4. Tags members in Mailchimp (webinar-attended-{date} or webinar-noshow-{date})

Usage:
    python zoom_attendance_sync.py --latest              # Auto-detect latest past webinar
    python zoom_attendance_sync.py --webinar-id 12345    # Sync specific webinar
    python zoom_attendance_sync.py --latest --dry-run    # Preview without changes

Depends on:
    - zoom_client.py (_get_access_token, _headers)
    - mailchimp_client.py (batch_tag_members)
    - google_sheets_client.py (SheetsClient)
"""

import os
import sys
import argparse
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

# Import shared clients
from zoom_client import _get_access_token, _headers as zoom_headers
from mailchimp_client import batch_tag_members
from google_sheets_client import SheetsClient, COLUMNS, get_column_letter

# Attended column index - extends the existing COLUMNS schema
# Column N (index 13) in the Google Sheet
ATTENDED_COL_INDEX = 13
ATTENDED_COL_LETTER = get_column_letter(ATTENDED_COL_INDEX)


def get_past_webinar_participants(webinar_id):
    """
    Fetch all participants who actually joined a past webinar.

    Endpoint: GET /v2/past_webinars/{webinarId}/participants
    Handles pagination (Zoom returns max 300 per page).

    Args:
        webinar_id: Zoom webinar ID (numeric string)

    Returns:
        list of dicts: [{email, name, join_time, leave_time, duration}, ...]
    """
    clean_id = str(webinar_id).replace(' ', '')
    url = f'https://api.zoom.us/v2/past_webinars/{clean_id}/participants'

    all_participants = []
    next_page_token = ''

    while True:
        params = {'page_size': 300}
        if next_page_token:
            params['next_page_token'] = next_page_token

        try:
            resp = requests.get(url, headers=zoom_headers(), params=params, timeout=10)

            if resp.status_code != 200:
                print(f"Zoom participants error: {resp.status_code} - {resp.text}")
                break

            data = resp.json()
            participants = data.get('participants', [])

            for p in participants:
                all_participants.append({
                    'email': (p.get('user_email') or '').lower().strip(),
                    'name': p.get('name', ''),
                    'join_time': p.get('join_time', ''),
                    'leave_time': p.get('leave_time', ''),
                    'duration': p.get('duration', 0),
                })

            next_page_token = data.get('next_page_token', '')
            if not next_page_token:
                break

        except Exception as e:
            print(f"Zoom participants request failed: {e}")
            break

    print(f"Fetched {len(all_participants)} participants from Zoom")
    return all_participants


def get_webinar_registrants(webinar_id):
    """
    Fetch all registrants for a webinar (everyone who signed up).

    Endpoint: GET /v2/webinars/{webinarId}/registrants
    Handles pagination.

    Args:
        webinar_id: Zoom webinar ID (numeric string)

    Returns:
        list of dicts: [{email, first_name, last_name, status}, ...]
    """
    clean_id = str(webinar_id).replace(' ', '')
    url = f'https://api.zoom.us/v2/webinars/{clean_id}/registrants'

    all_registrants = []
    next_page_token = ''

    while True:
        params = {'page_size': 300, 'status': 'approved'}
        if next_page_token:
            params['next_page_token'] = next_page_token

        try:
            resp = requests.get(url, headers=zoom_headers(), params=params, timeout=10)

            if resp.status_code != 200:
                print(f"Zoom registrants error: {resp.status_code} - {resp.text}")
                break

            data = resp.json()
            registrants = data.get('registrants', [])

            for r in registrants:
                all_registrants.append({
                    'email': (r.get('email') or '').lower().strip(),
                    'first_name': r.get('first_name', ''),
                    'last_name': r.get('last_name', ''),
                    'status': r.get('status', ''),
                })

            next_page_token = data.get('next_page_token', '')
            if not next_page_token:
                break

        except Exception as e:
            print(f"Zoom registrants request failed: {e}")
            break

    print(f"Fetched {len(all_registrants)} registrants from Zoom")
    return all_registrants


def get_latest_past_webinar():
    """
    Find the most recently completed webinar.

    Endpoint: GET /v2/users/me/webinars?type=past

    Returns:
        dict: {id, topic, start_time, date_str} or None
    """
    url = 'https://api.zoom.us/v2/past_webinars'
    # The past webinars endpoint is actually /v2/users/{userId}/webinars with type=past
    url = 'https://api.zoom.us/v2/users/me/webinars'
    params = {'page_size': 10, 'type': 'past'}

    try:
        resp = requests.get(url, headers=zoom_headers(), params=params, timeout=10)

        if resp.status_code != 200:
            print(f"Zoom list past webinars error: {resp.status_code} - {resp.text}")
            return None

        webinars = resp.json().get('webinars', [])
        if not webinars:
            print("No past webinars found")
            return None

        # Sort by start_time descending (most recent first)
        webinars.sort(key=lambda w: w.get('start_time', ''), reverse=True)
        latest = webinars[0]

        # Extract date string (YYYY-MM-DD) from start_time
        start_time = latest.get('start_time', '')
        date_str = start_time[:10] if start_time else ''

        result = {
            'id': latest['id'],
            'topic': latest.get('topic', ''),
            'start_time': start_time,
            'date_str': date_str,
        }
        print(f"Latest past webinar: [{result['id']}] {result['topic']} ({date_str})")
        return result

    except Exception as e:
        print(f"Zoom past webinars request failed: {e}")
        return None


def sync_attendance(webinar_id, webinar_date_str, dry_run=False):
    """
    Main sync function: cross-reference Zoom data with Google Sheets and Mailchimp.

    Steps:
        1. Get all Zoom registrants and participants for the webinar
        2. Build attended/no-show sets by email
        3. Update Google Sheet 'Attended' column (Yes/No)
        4. Tag in Mailchimp: webinar-attended-{date} or webinar-noshow-{date}

    Args:
        webinar_id: Zoom webinar ID
        webinar_date_str: Date string for tags (e.g., '2026-03-20')
        dry_run: If True, print actions without executing

    Returns:
        dict: {attended: N, noshow: M, total: N+M, skipped: K}
    """
    print(f"\n{'='*60}")
    print(f"Syncing attendance for webinar {webinar_id} ({webinar_date_str})")
    print(f"{'='*60}")

    # Step 1: Get Zoom data
    participants = get_past_webinar_participants(webinar_id)
    registrants = get_webinar_registrants(webinar_id)

    # Build set of emails who actually attended
    attended_emails = set()
    for p in participants:
        if p['email']:
            attended_emails.add(p['email'])

    print(f"\nZoom summary: {len(registrants)} registered, {len(attended_emails)} unique attendees")

    # Step 2: Cross-reference with Google Sheet
    if not dry_run:
        try:
            sheets = SheetsClient()
        except Exception as e:
            print(f"Google Sheets connection failed: {e}")
            print("Continuing with Mailchimp-only sync...")
            sheets = None
    else:
        sheets = None

    # Get sheet registrants to match by email
    sheet_registrants = []
    if sheets:
        try:
            sheet_registrants = sheets.get_all_registrants()
            print(f"Found {len(sheet_registrants)} registrants in Google Sheet")
        except Exception as e:
            print(f"Failed to read Google Sheet: {e}")

    # Step 3: Classify and update
    attended_list = []
    noshow_list = []
    skipped = 0

    # Build registrant email set from Zoom registrants
    registrant_emails = {r['email'] for r in registrants if r['email']}

    for email in registrant_emails:
        if email in attended_emails:
            attended_list.append(email)
        else:
            noshow_list.append(email)

    print(f"\nClassification:")
    print(f"  Attended: {len(attended_list)}")
    print(f"  No-show:  {len(noshow_list)}")

    # Step 4: Update Google Sheet
    if sheet_registrants and not dry_run:
        print(f"\nUpdating Google Sheet 'Attended' column...")
        updated = 0
        for reg in sheet_registrants:
            reg_email = (reg.get('email') or '').lower().strip()
            if not reg_email:
                continue

            row_num = reg.get('row_number')
            if not row_num:
                continue

            # Check if this registrant is for this webinar date
            reg_webinar_date = (reg.get('webinar_date') or '')[:10]
            if reg_webinar_date != webinar_date_str:
                continue

            # Determine attendance
            if reg_email in attended_emails:
                value = 'Yes'
            elif reg_email in registrant_emails:
                value = 'No'
            else:
                # Not in Zoom registrants at all (maybe registered only via site)
                # Check if they attended anyway
                if reg_email in attended_emails:
                    value = 'Yes'
                else:
                    value = 'No'

            try:
                cell_range = f'Sheet1!{ATTENDED_COL_LETTER}{row_num}'
                sheets.sheet.values().update(
                    spreadsheetId=sheets.sheet_id,
                    range=cell_range,
                    valueInputOption='RAW',
                    body={'values': [[value]]}
                ).execute()
                updated += 1
            except Exception as e:
                print(f"  Failed to update row {row_num} for {reg_email}: {e}")
                skipped += 1

        print(f"  Updated {updated} rows in Google Sheet")
    elif dry_run:
        print(f"\n[DRY RUN] Would update Google Sheet for {len(attended_list) + len(noshow_list)} registrants")

    # Step 5: Tag in Mailchimp
    attended_tag = f'webinar-attended-{webinar_date_str}'
    noshow_tag = f'webinar-noshow-{webinar_date_str}'

    if not dry_run:
        print(f"\nTagging in Mailchimp...")

        if attended_list:
            print(f"  Tagging {len(attended_list)} attendees with '{attended_tag}'...")
            result = batch_tag_members(attended_list, attended_tag)
            print(f"  Result: {result['success_count']} success, {result['fail_count']} failed")

        if noshow_list:
            print(f"  Tagging {len(noshow_list)} no-shows with '{noshow_tag}'...")
            result = batch_tag_members(noshow_list, noshow_tag)
            print(f"  Result: {result['success_count']} success, {result['fail_count']} failed")
    else:
        print(f"\n[DRY RUN] Would tag in Mailchimp:")
        print(f"  {len(attended_list)} attendees -> '{attended_tag}'")
        print(f"  {len(noshow_list)} no-shows -> '{noshow_tag}'")

        if attended_list:
            print(f"\n  Attendees:")
            for email in sorted(attended_list):
                print(f"    - {email}")

        if noshow_list:
            print(f"\n  No-shows:")
            for email in sorted(noshow_list):
                print(f"    - {email}")

    # Summary
    summary = {
        'attended': len(attended_list),
        'noshow': len(noshow_list),
        'total': len(attended_list) + len(noshow_list),
        'skipped': skipped,
        'webinar_id': str(webinar_id),
        'webinar_date': webinar_date_str,
        'dry_run': dry_run,
    }

    print(f"\n{'='*60}")
    print(f"Sync complete: {summary['attended']} attended, {summary['noshow']} no-show, {summary['total']} total")
    if dry_run:
        print(f"[DRY RUN] No changes were made")
    print(f"{'='*60}\n")

    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Sync Zoom webinar attendance to Google Sheets and Mailchimp'
    )
    parser.add_argument(
        '--webinar-id',
        type=str,
        help='Zoom webinar ID to sync'
    )
    parser.add_argument(
        '--webinar-date',
        type=str,
        help='Webinar date (YYYY-MM-DD) for tagging. Auto-detected if using --latest.'
    )
    parser.add_argument(
        '--latest',
        action='store_true',
        help='Auto-detect the most recent past webinar and sync it'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would happen without making changes'
    )

    args = parser.parse_args()

    if not args.webinar_id and not args.latest:
        parser.error('Provide --webinar-id ID or --latest')

    try:
        if args.latest:
            webinar = get_latest_past_webinar()
            if not webinar:
                print("Could not find a past webinar. Exiting.")
                sys.exit(1)
            webinar_id = webinar['id']
            webinar_date_str = webinar['date_str']
        else:
            webinar_id = args.webinar_id
            webinar_date_str = args.webinar_date
            if not webinar_date_str:
                parser.error('--webinar-date is required when using --webinar-id')

        result = sync_attendance(webinar_id, webinar_date_str, dry_run=args.dry_run)
        sys.exit(0)

    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
