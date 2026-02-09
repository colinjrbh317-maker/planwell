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


if __name__ == '__main__':
    """Test: list audiences to verify API key works."""
    audiences = list_audiences()
    if audiences:
        print('Mailchimp audiences:')
        for a in audiences:
            print(f"  {a['name']} (ID: {a['id']}, members: {a['member_count']})")
    else:
        print('No audiences found or API key invalid.')
