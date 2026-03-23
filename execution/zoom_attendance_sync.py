"""
Zoom-to-Mailchimp Attendance Sync
==================================
Automates post-webinar attendance tracking:
1. Pulls participant data from Zoom Report API (who actually joined)
2. Pulls registrants from Mailchimp by tag (fers-registered-* or tsp-registered-*)
3. Cross-references to determine attended vs no-show
4. Tags members in Mailchimp (webinar-attended-{date}, webinar-noshow-{date},
   plus type-specific tags like fers-attended-{date} or tsp-attended-{date})

Usage:
    python zoom_attendance_sync.py --latest              # Auto-detect latest past webinar
    python zoom_attendance_sync.py --webinar-id 12345    # Sync specific webinar
    python zoom_attendance_sync.py --latest --dry-run    # Preview without changes

Depends on:
    - zoom_client.py (_get_access_token, _headers)
    - mailchimp_client.py (batch_tag_members, get_members_by_tag)
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
from mailchimp_client import batch_tag_members, get_members_by_tag


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


def get_latest_past_webinar():
    """
    Find the most recently completed webinar.

    Endpoint: GET /v2/users/me/webinars?type=past

    Returns:
        dict: {id, topic, start_time, date_str} or None
    """
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


def get_webinar_details(webinar_id):
    """
    Fetch details for a specific webinar (topic, start_time, etc.).

    Endpoint: GET /v2/webinars/{webinarId}

    Args:
        webinar_id: Zoom webinar ID

    Returns:
        dict: {id, topic, start_time, date_str} or None
    """
    clean_id = str(webinar_id).replace(' ', '')
    url = f'https://api.zoom.us/v2/webinars/{clean_id}'

    try:
        resp = requests.get(url, headers=zoom_headers(), timeout=10)

        if resp.status_code != 200:
            # Try past webinar endpoint as fallback
            url = f'https://api.zoom.us/v2/past_webinars/{clean_id}'
            resp = requests.get(url, headers=zoom_headers(), timeout=10)

            if resp.status_code != 200:
                print(f"Zoom webinar details error: {resp.status_code} - {resp.text}")
                return None

        data = resp.json()
        start_time = data.get('start_time', '')
        date_str = start_time[:10] if start_time else ''

        return {
            'id': data.get('id', webinar_id),
            'topic': data.get('topic', ''),
            'start_time': start_time,
            'date_str': date_str,
        }

    except Exception as e:
        print(f"Zoom webinar details request failed: {e}")
        return None


def detect_webinar_type(topic):
    """
    Detect webinar type from topic string.

    Args:
        topic: Webinar topic from Zoom API

    Returns:
        str: 'tsp' if topic contains 'TSP', otherwise 'fers'
    """
    if 'TSP' in (topic or '').upper():
        return 'tsp'
    return 'fers'


def get_mailchimp_registrants(webinar_type, webinar_date_str):
    """
    Pull registrants from Mailchimp by looking for members with
    registration tags matching the webinar date and type.

    Looks for tags like: fers-registered-2026-03-20 or tsp-registered-2026-03-20

    Args:
        webinar_type: 'fers' or 'tsp'
        webinar_date_str: Date string (YYYY-MM-DD)

    Returns:
        set of email addresses
    """
    tag_name = f'{webinar_type}-registered-{webinar_date_str}'
    print(f"Looking up Mailchimp members with tag: {tag_name}")

    members = get_members_by_tag(tag_name)
    emails = {m['email'].lower().strip() for m in members if m.get('email')}

    print(f"Found {len(emails)} registrants in Mailchimp with tag '{tag_name}'")
    return emails


def sync_attendance(webinar_id, webinar_date_str, webinar_topic='', dry_run=False):
    """
    Main sync function: cross-reference Zoom participants with Mailchimp registrants.

    Steps:
        1. Detect webinar type from topic (fers or tsp)
        2. Pull participants from Zoom Report API
        3. Pull registrants from Mailchimp (by registration tag)
        4. Cross-reference: attended = participants & registrants, no-show = registrants - participants
        5. Apply Mailchimp tags for both groups

    Args:
        webinar_id: Zoom webinar ID
        webinar_date_str: Date string for tags (e.g., '2026-03-20')
        webinar_topic: Webinar topic string (for type detection)
        dry_run: If True, print actions without executing

    Returns:
        dict: {attended, noshow, total, webinar_type, webinar_id, webinar_date, dry_run}
    """
    print(f"\n{'='*60}")
    print(f"Syncing attendance for webinar {webinar_id} ({webinar_date_str})")
    print(f"{'='*60}")

    # Step 1: Detect webinar type
    webinar_type = detect_webinar_type(webinar_topic)
    print(f"Webinar type: {webinar_type} (topic: {webinar_topic!r})")

    # Step 2: Pull participants from Zoom
    participants = get_past_webinar_participants(webinar_id)
    attended_emails = {p['email'] for p in participants if p['email']}
    print(f"\nZoom: {len(attended_emails)} unique attendee emails")

    # Step 3: Pull registrants from Mailchimp
    registrant_emails = get_mailchimp_registrants(webinar_type, webinar_date_str)

    # Step 4: Cross-reference
    attended_list = sorted(attended_emails & registrant_emails)
    noshow_list = sorted(registrant_emails - attended_emails)

    print(f"\nClassification:")
    print(f"  Attended: {len(attended_list)}")
    print(f"  No-show:  {len(noshow_list)}")

    # Step 5: Apply Mailchimp tags
    # Generic tags
    attended_tag = f'webinar-attended-{webinar_date_str}'
    noshow_tag = f'webinar-noshow-{webinar_date_str}'
    # Type-specific tags
    type_attended_tag = f'{webinar_type}-attended-{webinar_date_str}'
    type_noshow_tag = f'{webinar_type}-noshow-{webinar_date_str}'

    if not dry_run:
        print(f"\nTagging in Mailchimp...")

        if attended_list:
            print(f"  Tagging {len(attended_list)} attendees with '{attended_tag}'...")
            result = batch_tag_members(attended_list, attended_tag)
            print(f"  Result: {result['success_count']} success, {result['fail_count']} failed")

            print(f"  Tagging {len(attended_list)} attendees with '{type_attended_tag}'...")
            result = batch_tag_members(attended_list, type_attended_tag)
            print(f"  Result: {result['success_count']} success, {result['fail_count']} failed")

        if noshow_list:
            print(f"  Tagging {len(noshow_list)} no-shows with '{noshow_tag}'...")
            result = batch_tag_members(noshow_list, noshow_tag)
            print(f"  Result: {result['success_count']} success, {result['fail_count']} failed")

            print(f"  Tagging {len(noshow_list)} no-shows with '{type_noshow_tag}'...")
            result = batch_tag_members(noshow_list, type_noshow_tag)
            print(f"  Result: {result['success_count']} success, {result['fail_count']} failed")
    else:
        print(f"\n[DRY RUN] Would tag in Mailchimp:")
        print(f"  {len(attended_list)} attendees -> '{attended_tag}', '{type_attended_tag}'")
        print(f"  {len(noshow_list)} no-shows -> '{noshow_tag}', '{type_noshow_tag}'")

        if attended_list:
            print(f"\n  Attendees:")
            for email in attended_list:
                print(f"    - {email}")

        if noshow_list:
            print(f"\n  No-shows:")
            for email in noshow_list:
                print(f"    - {email}")

    # Summary
    summary = {
        'attended': len(attended_list),
        'noshow': len(noshow_list),
        'total': len(attended_list) + len(noshow_list),
        'webinar_type': webinar_type,
        'webinar_id': str(webinar_id),
        'webinar_date': webinar_date_str,
        'dry_run': dry_run,
    }

    print(f"\n{'='*60}")
    print(f"Sync complete: {summary['attended']} attended, {summary['noshow']} no-show, {summary['total']} total")
    print(f"Webinar type: {webinar_type}")
    if dry_run:
        print(f"[DRY RUN] No changes were made")
    print(f"{'='*60}\n")

    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Sync Zoom webinar attendance to Mailchimp tags'
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
            webinar_topic = webinar['topic']
        else:
            webinar_id = args.webinar_id
            webinar_date_str = args.webinar_date
            if not webinar_date_str:
                parser.error('--webinar-date is required when using --webinar-id')
            # Fetch topic from Zoom for type detection
            details = get_webinar_details(webinar_id)
            webinar_topic = details['topic'] if details else ''

        result = sync_attendance(webinar_id, webinar_date_str, webinar_topic=webinar_topic, dry_run=args.dry_run)
        sys.exit(0)

    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
