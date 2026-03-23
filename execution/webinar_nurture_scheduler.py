"""
Webinar Nurture Scheduler
==========================
Scheduled script (run via cron) to send timed nurture emails.
Queries Mailchimp tags and merge fields for all registrants,
then sends pre- and post-webinar emails based on timing windows.

Supports both FERS and TSP webinar types.

Usage:
    python webinar_nurture_scheduler.py           # Run scheduler
    python webinar_nurture_scheduler.py --dry-run  # Preview without sending

Cron setup (run every hour):
    5 * * * * cd /path/to/planwell-site && python execution/webinar_nurture_scheduler.py >> /tmp/webinar_nurture.log 2>&1
"""

import sys
import os
from datetime import datetime, date
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

from mailchimp_client import get_members_by_tag, get_member_tags, update_member_tags

# FERS email functions
from webinar_emails import (
    send_webinar_7day,
    send_webinar_3day,
    send_webinar_1day,
    send_webinar_dayof
)
from post_webinar_emails import (
    send_post_day1_takeaways,
    send_post_day3_takeaways,
    send_post_day7_benefits_report,
    send_post_day10_case_study,
    send_post_day14_soft_close,
    send_noshow_day1_missed,
    send_noshow_day5_next_webinar
)

# TSP email functions
from tsp_webinar_emails import (
    send_tsp_7day,
    send_tsp_3day,
    send_tsp_1day,
    send_tsp_dayof
)
from tsp_post_webinar_emails import (
    send_tsp_post_day1_takeaways,
    send_tsp_post_day3_takeaways,
    send_tsp_post_day7_benefits_report,
    send_tsp_post_day10_case_study,
    send_tsp_post_day14_soft_close,
    send_tsp_noshow_day1_missed,
    send_tsp_noshow_day5_next_webinar
)

# ─────────────────────────────────────────────────────────────
# ACTIVE WEBINARS — update this list as webinars are scheduled
# ─────────────────────────────────────────────────────────────
ACTIVE_WEBINARS = [
    {'id': 'mar-27-2026', 'type': 'tsp',  'date': '2026-03-27'},
    {'id': 'apr-10-2026', 'type': 'fers', 'date': '2026-04-10'},
    {'id': 'apr-17-2026', 'type': 'tsp',  'date': '2026-04-17'},
    {'id': 'may-01-2026', 'type': 'fers', 'date': '2026-05-01'},
]

# Default FERS takeaways for post-day-3 email
DEFAULT_FERS_TAKEAWAYS = {
    'takeaway_1': 'Your FERS pension is based on your High-3 salary and years of creditable service -- even small salary bumps in your final years can significantly increase your lifetime pension.',
    'takeaway_2': 'The FERS supplement bridges the income gap between your retirement date and age 62 -- but it ends the month you turn 62, so plan your Social Security timing accordingly.',
    'takeaway_3': 'You can keep FEHB in retirement if you\'ve been continuously enrolled for 5 years before retirement -- this is one of the most valuable benefits federal employees have.',
}

# Default TSP takeaways for post-day-3 email
DEFAULT_TSP_TAKEAWAYS = {
    'takeaway_1': 'Your TSP fund allocation should shift as you approach retirement -- but the G Fund isn\'t always the safe play you think it is.',
    'takeaway_2': 'Roth TSP contributions grow tax-free, but the conversion window matters -- timing is everything.',
    'takeaway_3': 'Your withdrawal strategy can save or cost you tens of thousands in taxes -- the order you pull from accounts matters enormously.',
}

# Next webinar dates for no-show re-registration
NEXT_WEBINAR_DATES = {
    'mar-27-2026': {'date': 'Friday, April 10',  'url': 'https://planwellfp.com/webinar'},
    'apr-10-2026': {'date': 'Thursday, April 17', 'url': 'https://planwellfp.com/webinar'},
    'apr-17-2026': {'date': 'Friday, May 1',      'url': 'https://planwellfp.com/webinar'},
    'may-01-2026': {'date': 'TBD',                'url': 'https://planwellfp.com/webinar'},
}


def days_until_webinar(webinar_date: date) -> int:
    """Calculate days until the webinar (negative means webinar has passed)."""
    return (webinar_date - date.today()).days


def days_since_webinar(webinar_date: date) -> int:
    """Calculate days since the webinar occurred."""
    return (date.today() - webinar_date).days


def is_morning() -> bool:
    """Check if it's morning (before noon) for day-of emails."""
    return datetime.now().hour < 12


def format_date_human(iso_date_str: str) -> str:
    """Convert 'YYYY-MM-DD' to 'Friday, April 10'."""
    try:
        dt = datetime.strptime(iso_date_str, '%Y-%m-%d')
        return dt.strftime('%A, %B %d')
    except (ValueError, TypeError):
        return iso_date_str


def has_sent_tag(member_tags: list, tag_name: str) -> bool:
    """Check if a sent-tracking tag exists on the member."""
    return tag_name in member_tags


def apply_sent_tag(email: str, tag_name: str, dry_run: bool = False) -> bool:
    """Apply a sent-tracking tag to the member."""
    if dry_run:
        print(f"      [DRY RUN] Would apply tag: {tag_name}")
        return True
    result = update_member_tags(email, tags_to_add=[tag_name])
    return result.get('success', False)


def process_pre_webinar(email, first_name, days, webinar_type, webinar_id,
                        formatted_date, zoom_url, timezone, member_tags, dry_run):
    """Send pre-webinar emails based on timing window. Returns number of emails sent."""
    tag_prefix = webinar_type  # 'fers' or 'tsp'
    sent = 0

    # 7-day reminder (6-8 days out)
    tag_7day = f'{tag_prefix}-email-7day-sent-{webinar_id}'
    if 6 <= days <= 8 and not has_sent_tag(member_tags, tag_7day):
        print(f"    Sending 7-day reminder...")
        if dry_run:
            print(f"      [DRY RUN] Would send {webinar_type.upper()} 7-day to {email}")
            apply_sent_tag(email, tag_7day, dry_run=True)
            sent += 1
        else:
            if webinar_type == 'tsp':
                ok = send_tsp_7day(email, first_name, formatted_date)
            else:
                ok = send_webinar_7day(email, first_name, formatted_date)
            if ok:
                apply_sent_tag(email, tag_7day)
                sent += 1
                print(f"    Sent 7-day reminder")

    # 3-day reminder (2-4 days out)
    tag_3day = f'{tag_prefix}-email-3day-sent-{webinar_id}'
    if 2 <= days <= 4 and not has_sent_tag(member_tags, tag_3day):
        print(f"    Sending 3-day reminder...")
        if dry_run:
            print(f"      [DRY RUN] Would send {webinar_type.upper()} 3-day to {email}")
            apply_sent_tag(email, tag_3day, dry_run=True)
            sent += 1
        else:
            if webinar_type == 'tsp':
                ok = send_tsp_3day(email, first_name, formatted_date, timezone)
            else:
                ok = send_webinar_3day(email, first_name, formatted_date, timezone)
            if ok:
                apply_sent_tag(email, tag_3day)
                sent += 1
                print(f"    Sent 3-day reminder")

    # 1-day reminder
    tag_1day = f'{tag_prefix}-email-1day-sent-{webinar_id}'
    if days == 1 and not has_sent_tag(member_tags, tag_1day):
        print(f"    Sending 1-day reminder with Zoom link...")
        if dry_run:
            print(f"      [DRY RUN] Would send {webinar_type.upper()} 1-day to {email}")
            apply_sent_tag(email, tag_1day, dry_run=True)
            sent += 1
        else:
            if webinar_type == 'tsp':
                ok = send_tsp_1day(email, first_name, formatted_date, zoom_url, timezone)
            else:
                ok = send_webinar_1day(email, first_name, formatted_date, zoom_url, timezone)
            if ok:
                apply_sent_tag(email, tag_1day)
                sent += 1
                print(f"    Sent 1-day reminder")

    # Day-of reminder (morning only)
    tag_dayof = f'{tag_prefix}-email-dayof-sent-{webinar_id}'
    if days == 0 and is_morning() and not has_sent_tag(member_tags, tag_dayof):
        print(f"    Sending day-of reminder...")
        if dry_run:
            print(f"      [DRY RUN] Would send {webinar_type.upper()} day-of to {email}")
            apply_sent_tag(email, tag_dayof, dry_run=True)
            sent += 1
        else:
            if webinar_type == 'tsp':
                ok = send_tsp_dayof(email, first_name, zoom_url, timezone)
            else:
                ok = send_webinar_dayof(email, first_name, zoom_url, timezone)
            if ok:
                apply_sent_tag(email, tag_dayof)
                sent += 1
                print(f"    Sent day-of reminder")

    return sent


def process_post_webinar_attendee(email, first_name, since, webinar_type, webinar_id,
                                  member_tags, dry_run):
    """Send post-webinar attendee emails. Returns number of emails sent."""
    tag_prefix = webinar_type
    next_info = NEXT_WEBINAR_DATES.get(webinar_id, {})
    next_date = next_info.get('date', '')
    next_url = next_info.get('url', 'https://planwellfp.com/webinar')

    takeaways = DEFAULT_TSP_TAKEAWAYS if webinar_type == 'tsp' else DEFAULT_FERS_TAKEAWAYS

    # Define the attendee email schedule: (min_days, tag_suffix, send_fn_args)
    schedule = [
        (1,  'post-day1',  lambda: _send_post_day1(webinar_type, email, first_name, next_date, next_url)),
        (3,  'post-day3',  lambda: _send_post_day3(webinar_type, email, first_name, takeaways)),
        (7,  'post-day7',  lambda: _send_post_day7(webinar_type, email, first_name)),
        (10, 'post-day10', lambda: _send_post_day10(webinar_type, email, first_name)),
        (14, 'post-day14', lambda: _send_post_day14(webinar_type, email, first_name)),
    ]

    sent = 0
    for min_days, tag_suffix, send_fn in schedule:
        tag_name = f'{tag_prefix}-{tag_suffix}-sent-{webinar_id}'
        if since >= min_days and not has_sent_tag(member_tags, tag_name):
            print(f"    Sending {tag_suffix} (attendee)...")
            if dry_run:
                print(f"      [DRY RUN] Would send {webinar_type.upper()} {tag_suffix} to {email}")
                apply_sent_tag(email, tag_name, dry_run=True)
                sent += 1
            else:
                if send_fn():
                    apply_sent_tag(email, tag_name)
                    sent += 1
                    print(f"    Sent {tag_suffix}")
            break  # Only send one post-webinar email per run
    return sent


def process_post_webinar_noshow(email, first_name, since, webinar_type, webinar_id,
                                member_tags, dry_run):
    """Send post-webinar no-show emails. Returns number of emails sent."""
    tag_prefix = webinar_type
    next_info = NEXT_WEBINAR_DATES.get(webinar_id, {})
    next_date = next_info.get('date', '')
    next_url = next_info.get('url', 'https://planwellfp.com/webinar')

    sent = 0

    # Day 1: missed email
    tag_ns1 = f'{tag_prefix}-noshow-day1-sent-{webinar_id}'
    if since >= 1 and not has_sent_tag(member_tags, tag_ns1):
        print(f"    Sending no-show day-1 missed...")
        if dry_run:
            print(f"      [DRY RUN] Would send {webinar_type.upper()} noshow-day1 to {email}")
            apply_sent_tag(email, tag_ns1, dry_run=True)
            sent += 1
        else:
            if webinar_type == 'tsp':
                ok = send_tsp_noshow_day1_missed(email, first_name, next_date, next_url)
            else:
                ok = send_noshow_day1_missed(email, first_name, next_date, next_url)
            if ok:
                apply_sent_tag(email, tag_ns1)
                sent += 1
                print(f"    Sent no-show day-1 missed")
        return sent

    # Day 5: register for next webinar
    tag_ns5 = f'{tag_prefix}-noshow-day5-sent-{webinar_id}'
    if since >= 5 and not has_sent_tag(member_tags, tag_ns5):
        if next_date and next_date != 'TBD':
            print(f"    Sending no-show day-5 next webinar...")
            if dry_run:
                print(f"      [DRY RUN] Would send {webinar_type.upper()} noshow-day5 to {email}")
                apply_sent_tag(email, tag_ns5, dry_run=True)
                sent += 1
            else:
                if webinar_type == 'tsp':
                    ok = send_tsp_noshow_day5_next_webinar(email, first_name, next_date, next_url)
                else:
                    ok = send_noshow_day5_next_webinar(email, first_name, next_date, next_url)
                if ok:
                    apply_sent_tag(email, tag_ns5)
                    sent += 1
                    print(f"    Sent no-show day-5 next webinar")

    return sent


# ─────────────────────────────────────────────
# Helper dispatch functions for post-webinar
# ─────────────────────────────────────────────

def _send_post_day1(wtype, email, first_name, next_date, next_url):
    if wtype == 'tsp':
        return send_tsp_post_day1_takeaways(email, first_name, next_date, next_url)
    return send_post_day1_takeaways(email, first_name, next_date, next_url)


def _send_post_day3(wtype, email, first_name, takeaways):
    if wtype == 'tsp':
        return send_tsp_post_day3_takeaways(
            email, first_name,
            takeaways['takeaway_1'], takeaways['takeaway_2'], takeaways['takeaway_3']
        )
    return send_post_day3_takeaways(
        email, first_name,
        takeaways['takeaway_1'], takeaways['takeaway_2'], takeaways['takeaway_3']
    )


def _send_post_day7(wtype, email, first_name):
    if wtype == 'tsp':
        return send_tsp_post_day7_benefits_report(email, first_name)
    return send_post_day7_benefits_report(email, first_name)


def _send_post_day10(wtype, email, first_name):
    if wtype == 'tsp':
        return send_tsp_post_day10_case_study(email, first_name)
    return send_post_day10_case_study(email, first_name)


def _send_post_day14(wtype, email, first_name):
    if wtype == 'tsp':
        return send_tsp_post_day14_soft_close(email, first_name)
    return send_post_day14_soft_close(email, first_name)


# ─────────────────────────────────────────────
# Main scheduler
# ─────────────────────────────────────────────

def run_scheduler(dry_run: bool = False):
    """
    Main scheduler function.
    Loops through ACTIVE_WEBINARS, queries Mailchimp for registrants,
    determines which emails to send, sends them, and applies sent-tracking tags.
    """
    mode_label = " [DRY RUN]" if dry_run else ""
    print(f"\n{'='*60}")
    print(f"Webinar Nurture Scheduler{mode_label} - {datetime.now().isoformat()}")
    print(f"{'='*60}")

    total_emails_sent = 0
    total_registrants = 0

    for webinar in ACTIVE_WEBINARS:
        webinar_id = webinar['id']
        webinar_type = webinar['type']
        webinar_date_str = webinar['date']
        webinar_date = date.fromisoformat(webinar_date_str)
        days = days_until_webinar(webinar_date)
        formatted_date = format_date_human(webinar_date_str)

        print(f"\n--- {webinar_type.upper()} Webinar: {webinar_id} ({formatted_date}) ---")
        print(f"    Days until webinar: {days}")

        # Skip webinars that are too far in the future (no emails needed yet)
        if days > 8:
            print(f"    Skipping: more than 8 days out, no emails due")
            continue

        # Skip webinars that finished their full post sequence (>30 days ago)
        if days < -30:
            print(f"    Skipping: webinar was >30 days ago, sequence complete")
            continue

        # Query Mailchimp for registrants with this webinar's tag
        registration_tag = f'{webinar_type}-registered-{webinar_id}'
        print(f"    Querying Mailchimp for tag: {registration_tag}")
        members = get_members_by_tag(registration_tag)
        print(f"    Found {len(members)} registrants")
        total_registrants += len(members)

        for member in members:
            email = member.get('email', '')
            first_name = member.get('first_name', '') or 'there'
            merge_fields = member.get('merge_fields', {})
            member_tags_from_query = member.get('tags', [])

            if not email:
                continue

            # Get zoom URL from merge fields, fall back to default
            zoom_url = merge_fields.get('ZOOMURL', '') or 'https://planwellfp.com/webinar'
            timezone = 'EST'

            # Get full tag list for sent-tracking checks
            # The tags from get_members_by_tag may not include all tags,
            # so fetch the complete list for accurate sent-tracking
            member_tags = member_tags_from_query if member_tags_from_query else get_member_tags(email)

            print(f"\n  {first_name} ({email}): {days} days until webinar")

            if days >= 0:
                # Pre-webinar sequence
                sent = process_pre_webinar(
                    email, first_name, days, webinar_type, webinar_id,
                    formatted_date, zoom_url, timezone, member_tags, dry_run
                )
                total_emails_sent += sent
            else:
                # Post-webinar sequence
                since = days_since_webinar(webinar_date)
                attended_tag = f'webinar-attended-{webinar_id}'
                noshow_tag = f'webinar-noshow-{webinar_id}'

                if attended_tag in member_tags:
                    sent = process_post_webinar_attendee(
                        email, first_name, since, webinar_type, webinar_id,
                        member_tags, dry_run
                    )
                    total_emails_sent += sent
                elif noshow_tag in member_tags:
                    sent = process_post_webinar_noshow(
                        email, first_name, since, webinar_type, webinar_id,
                        member_tags, dry_run
                    )
                    total_emails_sent += sent
                else:
                    print(f"    No attendance/noshow tag found yet, skipping post-webinar")

    print(f"\n{'='*60}")
    print(f"Scheduler complete{mode_label}. Processed {total_registrants} registrants, sent {total_emails_sent} emails.")
    print(f"{'='*60}\n")

    return total_emails_sent


if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv
    run_scheduler(dry_run=dry_run)
