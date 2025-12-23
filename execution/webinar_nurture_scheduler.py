"""
Webinar Nurture Scheduler
==========================
Scheduled script (run via cron) to send timed nurture emails.
Checks all registrants and sends emails based on days until webinar.

Usage:
    python webinar_nurture_scheduler.py

Cron setup (run every hour):
    5 * * * * cd /path/to/planwell-site && python execution/webinar_nurture_scheduler.py >> /tmp/webinar_nurture.log 2>&1
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

from google_sheets_client import SheetsClient
from webinar_emails import (
    send_webinar_7day,
    send_webinar_3day,
    send_webinar_1day,
    send_webinar_dayof
)

# Webinar data with Zoom links (loaded from JSON or hardcoded)
WEBINAR_ZOOM_LINKS = {
    'dec-30-2025': '',  # Add Zoom link when available
    'jan-16-2026': '',
    'feb-06-2026': '',
    'feb-27-2026': '',
    'mar-20-2026': '',
    'apr-10-2026': '',
}


def load_zoom_links() -> dict:
    """Load Zoom links from JSON file if available."""
    zoom_file = Path(__file__).parent / '.webinar_zoom_links.json'
    if zoom_file.exists():
        with open(zoom_file, 'r') as f:
            return json.load(f)
    return WEBINAR_ZOOM_LINKS


def get_webinar_date_formatted(iso_date: str) -> str:
    """Convert ISO date to human-readable format."""
    try:
        dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
        return dt.strftime('%A, %B %d')
    except:
        return iso_date


def get_timezone_from_date(iso_date: str) -> str:
    """Extract timezone from ISO date."""
    try:
        dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
        offset = dt.utcoffset()
        if offset:
            hours = offset.total_seconds() / 3600
            if hours == -5:
                return 'EST'
            elif hours == -4:
                return 'EDT'
        return 'EST'
    except:
        return 'EST'


def parse_webinar_date(iso_date: str) -> datetime:
    """Parse ISO date string to datetime."""
    try:
        return datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
    except:
        return None


def days_until_webinar(webinar_date: datetime) -> int:
    """Calculate days until the webinar."""
    if not webinar_date:
        return -999
    now = datetime.now(webinar_date.tzinfo) if webinar_date.tzinfo else datetime.now()
    delta = webinar_date.date() - now.date()
    return delta.days


def is_morning() -> bool:
    """Check if it's morning (before noon) for day-of emails."""
    return datetime.now().hour < 12


def run_scheduler():
    """Main scheduler function - check all registrants and send due emails."""
    print(f"\n{'='*60}")
    print(f"Webinar Nurture Scheduler - {datetime.now().isoformat()}")
    print(f"{'='*60}")
    
    zoom_links = load_zoom_links()
    
    try:
        sheets = SheetsClient()
        registrants = sheets.get_all_registrants()
        print(f"Found {len(registrants)} registrants to check")
        
        emails_sent = 0
        
        for reg in registrants:
            email = reg.get('email')
            first_name = reg.get('first_name') or 'there'
            webinar_id = reg.get('webinar_id')
            webinar_date_str = reg.get('webinar_date')
            row_num = reg.get('row_number')
            
            if not email or not webinar_date_str:
                continue
            
            webinar_date = parse_webinar_date(webinar_date_str)
            if not webinar_date:
                print(f"  Skipping {email}: Invalid webinar date")
                continue
            
            days = days_until_webinar(webinar_date)
            formatted_date = get_webinar_date_formatted(webinar_date_str)
            timezone = get_timezone_from_date(webinar_date_str)
            zoom_link = zoom_links.get(webinar_id, 'https://planwellfp.com/webinar')
            
            print(f"\n  Checking {first_name} ({email}): {days} days until webinar")
            
            # Skip if webinar already passed
            if days < 0:
                print(f"    Webinar already passed, skipping")
                continue
            
            # 7-day reminder (between 6-8 days out to have some buffer)
            if 6 <= days <= 8 and not reg.get('email_7day_sent'):
                print(f"    Sending 7-day reminder...")
                if send_webinar_7day(email, first_name, formatted_date):
                    sheets.update_email_sent(row_num, 'Email_7Day_Sent')
                    emails_sent += 1
                    print(f"    ✓ Sent 7-day reminder")
            
            # 3-day reminder (between 2-4 days out)
            elif 2 <= days <= 4 and not reg.get('email_3day_sent'):
                print(f"    Sending 3-day reminder...")
                if send_webinar_3day(email, first_name, formatted_date, timezone):
                    sheets.update_email_sent(row_num, 'Email_3Day_Sent')
                    emails_sent += 1
                    print(f"    ✓ Sent 3-day reminder")
            
            # 1-day reminder (1 day before)
            elif days == 1 and not reg.get('email_1day_sent'):
                print(f"    Sending 1-day reminder with Zoom link...")
                if send_webinar_1day(email, first_name, formatted_date, zoom_link, timezone):
                    sheets.update_email_sent(row_num, 'Email_1Day_Sent')
                    emails_sent += 1
                    print(f"    ✓ Sent 1-day reminder")
            
            # Day-of reminder (morning only)
            elif days == 0 and is_morning() and not reg.get('email_dayof_sent'):
                print(f"    Sending day-of reminder...")
                if send_webinar_dayof(email, first_name, zoom_link, timezone):
                    sheets.update_email_sent(row_num, 'Email_DayOf_Sent')
                    emails_sent += 1
                    print(f"    ✓ Sent day-of reminder")
        
        print(f"\n{'='*60}")
        print(f"Scheduler complete. Sent {emails_sent} emails.")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"Scheduler error: {e}")
        raise


if __name__ == '__main__':
    run_scheduler()
