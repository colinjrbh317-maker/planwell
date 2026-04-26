"""
Zoom API Client (Server-to-Server OAuth)
==========================================
Manages webinar registrations via the Zoom API.

Auth: Server-to-Server OAuth (client credentials grant)
Token endpoint: POST https://zoom.us/oauth/token
API base: https://api.zoom.us/v2

Scopes required: webinar:write:admin, webinar:read:admin
"""

import os
import time
import requests
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / '.env')

ZOOM_ACCOUNT_ID = os.environ.get('ZOOM_ACCOUNT_ID', '').strip()
ZOOM_CLIENT_ID = os.environ.get('ZOOM_CLIENT_ID', '').strip()
ZOOM_CLIENT_SECRET = os.environ.get('ZOOM_CLIENT_SECRET', '').strip()

# Token cache
_token_cache = {'token': None, 'expires_at': 0}


def _get_access_token():
    """Get OAuth access token using Server-to-Server client credentials."""
    if _token_cache['token'] and time.time() < _token_cache['expires_at'] - 60:
        return _token_cache['token']

    url = 'https://zoom.us/oauth/token'
    params = {
        'grant_type': 'account_credentials',
        'account_id': ZOOM_ACCOUNT_ID,
    }

    resp = requests.post(
        url,
        params=params,
        auth=(ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET),
        timeout=10,
    )

    if resp.status_code != 200:
        raise Exception(f'Zoom OAuth failed: {resp.status_code} - {resp.text}')

    data = resp.json()
    _token_cache['token'] = data['access_token']
    _token_cache['expires_at'] = time.time() + data.get('expires_in', 3600)

    return _token_cache['token']


def _headers():
    token = _get_access_token()
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }


def list_upcoming_webinars():
    """
    List all upcoming webinars for the account.
    Returns list of webinars with id, topic, start_time, duration.
    """
    url = 'https://api.zoom.us/v2/users/me/webinars'
    params = {'page_size': 50}

    resp = requests.get(url, headers=_headers(), params=params, timeout=10)

    if resp.status_code != 200:
        print(f'Zoom list webinars error: {resp.status_code} - {resp.text}')
        return []

    webinars = resp.json().get('webinars', [])
    return [
        {
            'id': w['id'],
            'topic': w['topic'],
            'start_time': w['start_time'],
            'duration': w.get('duration', 0),
        }
        for w in webinars
    ]


def find_webinar_by_date(target_date):
    """
    Find a webinar matching a target date string (e.g., '2026-02-27').
    Returns the webinar ID or None.
    """
    webinars = list_upcoming_webinars()
    for w in webinars:
        # Compare date portion of start_time (format: 2026-02-27T16:00:00Z)
        webinar_date = w['start_time'][:10]
        if webinar_date == target_date:
            return w['id']
    return None


def add_registrant(webinar_id, first_name, last_name, email, phone=''):
    """
    Register a participant for a Zoom webinar.
    Zoom automatically sends a confirmation email with the join link.

    Args:
        webinar_id: Zoom webinar ID (numeric, spaces stripped)
        first_name: Registrant's first name
        last_name: Registrant's last name
        email: Registrant's email
        phone: Optional phone number

    Returns:
        dict with success status, join_url, and registrant_id
    """
    # Strip spaces from webinar ID (e.g., "851 7076 2995" → "85170762995")
    clean_id = str(webinar_id).replace(' ', '')

    url = f'https://api.zoom.us/v2/webinars/{clean_id}/registrants'

    payload = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
    }

    if phone:
        payload['phone'] = phone

    try:
        resp = requests.post(url, json=payload, headers=_headers(), timeout=10)

        if resp.status_code in (200, 201):
            data = resp.json()
            return {
                'success': True,
                'join_url': data.get('join_url', ''),
                'registrant_id': data.get('registrant_id', ''),
            }
        else:
            print(f'Zoom registration error: {resp.status_code} - {resp.text}')
            return {
                'success': False,
                'error': resp.text,
                'status_code': resp.status_code,
            }

    except Exception as e:
        print(f'Zoom request failed: {e}')
        return {'success': False, 'error': str(e)}


def list_webinar_registrants(webinar_id, status='approved'):
    """
    List all registrants for a Zoom webinar. Paginates until exhausted.

    Args:
        webinar_id: Zoom webinar ID (numeric, spaces stripped)
        status: 'approved', 'pending', or 'denied' (default 'approved')

    Returns:
        list of dicts: [{first_name, last_name, email, join_url, registrant_id, status}, ...]
    """
    clean_id = str(webinar_id).replace(' ', '')
    base = f'https://api.zoom.us/v2/webinars/{clean_id}/registrants'

    registrants = []
    next_token = None
    page = 0

    while True:
        page += 1
        params = {'page_size': 300, 'status': status}
        if next_token:
            params['next_page_token'] = next_token

        resp = requests.get(base, headers=_headers(), params=params, timeout=15)

        if resp.status_code != 200:
            print(f'Zoom list registrants error: {resp.status_code} - {resp.text}')
            return registrants

        data = resp.json()
        for r in data.get('registrants', []):
            registrants.append({
                'first_name': r.get('first_name', '').strip(),
                'last_name': r.get('last_name', '').strip(),
                'email': r.get('email', '').strip().lower(),
                'join_url': r.get('join_url', ''),
                'registrant_id': r.get('id', ''),
                'status': r.get('status', status),
                'create_time': r.get('create_time', ''),
            })

        next_token = data.get('next_page_token', '')
        if not next_token:
            break

    return registrants


if __name__ == '__main__':
    """Test: list upcoming webinars to verify credentials."""
    print('Testing Zoom API connection...\n')

    webinars = list_upcoming_webinars()
    if webinars:
        print(f'Found {len(webinars)} upcoming webinar(s):')
        for w in webinars:
            print(f"  [{w['id']}] {w['topic']} - {w['start_time']}")
    else:
        print('No webinars found or credentials invalid.')
