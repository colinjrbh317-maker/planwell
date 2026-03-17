"""
Mailchimp API Client
====================
Handles subscriber management for the PlanWell Federal Newsletter.

API Docs: https://mailchimp.com/developer/marketing/api/
Auth: HTTP Basic Auth (anystring:api_key)
Data Center: extracted from API key suffix (e.g., us21)
"""

import os
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / '.env')

MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY', '')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID', '')

# Extract data center from API key (e.g., "xxx-us21" → "us21")
MAILCHIMP_DC = MAILCHIMP_API_KEY.split('-')[-1] if '-' in MAILCHIMP_API_KEY else 'us21'
BASE_URL = f'https://{MAILCHIMP_DC}.api.mailchimp.com/3.0'


def _headers():
    return {
        'Authorization': f'Bearer {MAILCHIMP_API_KEY}',
        'Content-Type': 'application/json',
    }


def add_subscriber(email, first_name='', tags=None):
    """
    Add a subscriber to the PlanWell Federal Newsletter audience.

    Args:
        email: Subscriber email address
        first_name: Optional first name
        tags: Optional list of tags (e.g., ['free-guide', 'homepage-popup'])

    Returns:
        dict with success status and Mailchimp response
    """
    url = f'{BASE_URL}/lists/{MAILCHIMP_LIST_ID}/members'

    payload = {
        'email_address': email,
        'status': 'subscribed',
        'merge_fields': {},
    }

    if first_name:
        payload['merge_fields']['FNAME'] = first_name

    if tags:
        payload['tags'] = tags

    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=10)

        if resp.status_code == 200:
            return {'success': True, 'status': 'subscribed', 'id': resp.json().get('id')}
        elif resp.status_code == 400 and 'already a list member' in resp.text.lower():
            return {'success': True, 'status': 'already_subscribed', 'duplicate': True}
        else:
            print(f'Mailchimp error: {resp.status_code} - {resp.text}')
            return {'success': False, 'error': resp.text, 'status_code': resp.status_code}

    except Exception as e:
        print(f'Mailchimp request failed: {e}')
        return {'success': False, 'error': str(e)}


def list_audiences():
    """List all Mailchimp audiences (for debugging/setup)."""
    url = f'{BASE_URL}/lists'
    resp = requests.get(url, headers=_headers(), timeout=10)
    if resp.status_code == 200:
        lists = resp.json().get('lists', [])
        return [{'id': l['id'], 'name': l['name'], 'member_count': l['stats']['member_count']} for l in lists]
    return []


def get_audience_stats(list_id=None):
    """
    Get detailed audience stats: member count, growth, open/click rates.

    Returns:
        dict with subscriber stats and engagement metrics.
    """
    lid = list_id or MAILCHIMP_LIST_ID
    url = f'{BASE_URL}/lists/{lid}'
    resp = requests.get(url, headers=_headers(), timeout=10)
    if resp.status_code != 200:
        return {'error': resp.text}

    data = resp.json()
    stats = data.get('stats', {})
    return {
        'list_name': data.get('name', ''),
        'member_count': stats.get('member_count', 0),
        'unsubscribe_count': stats.get('unsubscribe_count', 0),
        'cleaned_count': stats.get('cleaned_count', 0),
        'open_rate': round(stats.get('open_rate', 0), 1),
        'click_rate': round(stats.get('click_rate', 0), 1),
        'last_sub_date': stats.get('last_sub_date', ''),
        'last_unsub_date': stats.get('last_unsub_date', ''),
    }


def get_recent_campaigns(count=5):
    """
    Get recent campaign performance.

    Args:
        count: Number of recent campaigns to return.

    Returns:
        List of dicts with campaign stats.
    """
    url = f'{BASE_URL}/campaigns'
    params = {
        'count': count,
        'sort_field': 'send_time',
        'sort_dir': 'DESC',
        'status': 'sent',
    }
    resp = requests.get(url, headers=_headers(), params=params, timeout=10)
    if resp.status_code != 200:
        return []

    campaigns = []
    for c in resp.json().get('campaigns', []):
        report = c.get('report_summary', {})
        campaigns.append({
            'id': c.get('id'),
            'title': c.get('settings', {}).get('subject_line', 'Untitled'),
            'send_time': c.get('send_time', ''),
            'emails_sent': c.get('emails_sent', 0),
            'open_rate': round(report.get('open_rate', 0) * 100, 1),
            'click_rate': round(report.get('click_rate', 0) * 100, 1),
            'unique_opens': report.get('unique_opens', 0),
            'unique_clicks': report.get('subscriber_clicks', 0),
            'unsubscribes': report.get('unsubscribed', 0),
        })
    return campaigns


def get_growth_history(list_id=None, count=12):
    """
    Get monthly subscriber growth history.

    Args:
        list_id: Mailchimp list ID (defaults to env var).
        count: Number of months to return.

    Returns:
        List of dicts with monthly growth data.
    """
    lid = list_id or MAILCHIMP_LIST_ID
    url = f'{BASE_URL}/lists/{lid}/growth-history'
    params = {'count': count, 'sort_field': 'month', 'sort_dir': 'DESC'}
    resp = requests.get(url, headers=_headers(), params=params, timeout=10)
    if resp.status_code != 200:
        return []

    history = []
    for h in resp.json().get('history', []):
        history.append({
            'month': h.get('month', ''),
            'existing': h.get('existing', 0),
            'imports': h.get('imports', 0),
            'optins': h.get('optins', 0),
        })
    return history


def get_subscriber_activity_since(since_date, list_id=None):
    """
    Get subscriber count changes since a given date.

    Args:
        since_date: ISO date string (YYYY-MM-DD) to count from.
        list_id: Mailchimp list ID.

    Returns:
        dict with new subscribers and unsubscribes since date.
    """
    lid = list_id or MAILCHIMP_LIST_ID
    url = f'{BASE_URL}/lists/{lid}/members'

    # Count subscribed since date
    params = {
        'since_timestamp_opt': f'{since_date}T00:00:00+00:00',
        'status': 'subscribed',
        'count': 0,  # We only need total_items
    }
    resp = requests.get(url, headers=_headers(), params=params, timeout=10)
    new_subs = resp.json().get('total_items', 0) if resp.status_code == 200 else 0

    # Count unsubscribed since date
    params['status'] = 'unsubscribed'
    resp = requests.get(url, headers=_headers(), params=params, timeout=10)
    unsubs = resp.json().get('total_items', 0) if resp.status_code == 200 else 0

    return {
        'new_subscribers': new_subs,
        'unsubscribes': unsubs,
        'net_growth': new_subs - unsubs,
        'since': since_date,
    }


if __name__ == '__main__':
    """Test: show audience stats and recent campaigns."""
    import sys

    if '--stats' in sys.argv:
        print("Audience Stats:")
        print("-" * 40)
        stats = get_audience_stats()
        for k, v in stats.items():
            print(f"  {k}: {v}")

        print()
        print("Growth (this week):")
        print("-" * 40)
        from datetime import datetime, timedelta
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        activity = get_subscriber_activity_since(week_ago)
        for k, v in activity.items():
            print(f"  {k}: {v}")

        print()
        print("Recent Campaigns:")
        print("-" * 40)
        campaigns = get_recent_campaigns()
        for c in campaigns:
            print(f"  {c['title']}")
            print(f"    Sent: {c['send_time']} | Opens: {c['open_rate']}% | Clicks: {c['click_rate']}%")
    else:
        audiences = list_audiences()
        if audiences:
            print('Mailchimp audiences:')
            for a in audiences:
                print(f"  {a['name']} (ID: {a['id']}, members: {a['member_count']})")
        else:
            print('No audiences found or API key invalid.')
        print()
        print("Tip: Use --stats for detailed stats and campaign data.")
