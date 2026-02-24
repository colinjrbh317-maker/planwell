"""
PlanWell Webhook Server
========================
Production Flask server handling:
- /api/webinar  - Webinar registration (Zoom S2S OAuth)
- /api/newsletter - Newsletter subscription (Mailchimp)
- /api/contact  - Contact form (email notification)

Deploy: Railway
"""

import os
import time
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# CORS: allow requests from the PlanWell website
ALLOWED_ORIGINS = [
    'https://planwellfp.com',
    'https://www.planwellfp.com',
    'https://planwell.vercel.app',
]
if os.environ.get('FLASK_ENV') == 'development':
    ALLOWED_ORIGINS.append('http://localhost:4321')

CORS(app, origins=ALLOWED_ORIGINS)


# ─── Zoom Client ──────────────────────────────────────────────

ZOOM_ACCOUNT_ID = os.environ.get('ZOOM_ACCOUNT_ID', '')
ZOOM_CLIENT_ID = os.environ.get('ZOOM_CLIENT_ID', '')
ZOOM_CLIENT_SECRET = os.environ.get('ZOOM_CLIENT_SECRET', '')

_zoom_token_cache = {'token': None, 'expires_at': 0}


def _get_zoom_token():
    if _zoom_token_cache['token'] and time.time() < _zoom_token_cache['expires_at'] - 60:
        return _zoom_token_cache['token']

    resp = requests.post(
        'https://zoom.us/oauth/token',
        params={'grant_type': 'account_credentials', 'account_id': ZOOM_ACCOUNT_ID},
        auth=(ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET),
        timeout=10,
    )
    if resp.status_code != 200:
        raise Exception(f'Zoom OAuth failed: {resp.status_code} - {resp.text}')

    data = resp.json()
    _zoom_token_cache['token'] = data['access_token']
    _zoom_token_cache['expires_at'] = time.time() + data.get('expires_in', 3600)
    return _zoom_token_cache['token']


def _zoom_headers():
    return {'Authorization': f'Bearer {_get_zoom_token()}', 'Content-Type': 'application/json'}


def find_webinar_by_date(target_date):
    """Find a Zoom webinar matching a date string like '2026-02-27'."""
    resp = requests.get(
        'https://api.zoom.us/v2/users/me/webinars',
        headers=_zoom_headers(),
        params={'page_size': 50},
        timeout=10,
    )
    if resp.status_code != 200:
        return None
    for w in resp.json().get('webinars', []):
        if w['start_time'][:10] == target_date:
            return w['id']
    return None


def zoom_register(webinar_id, first_name, last_name, email, phone=''):
    """Register a participant for a Zoom webinar."""
    clean_id = str(webinar_id).replace(' ', '')
    payload = {'first_name': first_name, 'last_name': last_name, 'email': email}
    if phone:
        payload['phone'] = phone

    resp = requests.post(
        f'https://api.zoom.us/v2/webinars/{clean_id}/registrants',
        json=payload,
        headers=_zoom_headers(),
        timeout=10,
    )
    if resp.status_code in (200, 201):
        data = resp.json()
        return {'success': True, 'join_url': data.get('join_url', ''), 'registrant_id': data.get('registrant_id', '')}
    return {'success': False, 'error': resp.text, 'status_code': resp.status_code}


# ─── Mailchimp Client ─────────────────────────────────────────

MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY', '')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID', '')
MAILCHIMP_DC = MAILCHIMP_API_KEY.split('-')[-1] if '-' in MAILCHIMP_API_KEY else 'us21'
MAILCHIMP_BASE = f'https://{MAILCHIMP_DC}.api.mailchimp.com/3.0'


def _mc_headers():
    return {'Authorization': f'Bearer {MAILCHIMP_API_KEY}', 'Content-Type': 'application/json'}


def mailchimp_subscribe(email, first_name='', tags=None):
    """Add subscriber to Mailchimp audience."""
    payload = {'email_address': email, 'status': 'subscribed', 'merge_fields': {}}
    if first_name:
        payload['merge_fields']['FNAME'] = first_name
    if tags:
        payload['tags'] = tags

    resp = requests.post(
        f'{MAILCHIMP_BASE}/lists/{MAILCHIMP_LIST_ID}/members',
        json=payload,
        headers=_mc_headers(),
        timeout=10,
    )
    if resp.status_code == 200:
        return {'success': True, 'status': 'subscribed'}
    elif resp.status_code == 400 and 'already a list member' in resp.text.lower():
        return {'success': True, 'status': 'already_subscribed', 'duplicate': True}
    return {'success': False, 'error': resp.text}


# ─── Routes ───────────────────────────────────────────────────

@app.route('/api/webinar', methods=['POST'])
def handle_webinar():
    """Webinar registration -> Zoom."""
    data = request.json
    if not data or not data.get('email'):
        return jsonify({'success': False, 'error': 'Email is required'}), 400

    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    if not first_name and data.get('name'):
        parts = data['name'].split(None, 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''

    try:
        zoom_result = {'success': False, 'join_url': ''}
        webinar_date_str = data.get('webinar_date', '')
        if webinar_date_str:
            target_date = webinar_date_str[:10]
            webinar_id = find_webinar_by_date(target_date)
            if webinar_id:
                zoom_result = zoom_register(
                    webinar_id=webinar_id,
                    first_name=first_name or 'Attendee',
                    last_name=last_name or '',
                    email=data['email'],
                    phone=data.get('phone', ''),
                )
                print(f"Zoom registration: {data['email']} -> {'success' if zoom_result['success'] else 'failed'}")
            else:
                print(f"No Zoom webinar found for {target_date}")

        return jsonify({
            'success': True,
            'message': 'Registration received',
            'zoom_registered': zoom_result.get('success', False),
            'zoom_join_url': zoom_result.get('join_url', ''),
        })
    except Exception as e:
        print(f"Webinar registration error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/newsletter', methods=['POST'])
def handle_newsletter():
    """Newsletter subscription -> Mailchimp."""
    data = request.json
    if not data or not data.get('email'):
        return jsonify({'success': False, 'error': 'Email is required'}), 400

    name = data.get('name', '')
    email = data['email'].strip().lower()
    source = data.get('source', 'homepage_popup')

    try:
        result = mailchimp_subscribe(
            email=email,
            first_name=name.split()[0] if name else '',
            tags=['free-guide', source],
        )
        print(f"Newsletter: {email} -> Mailchimp {result.get('status', 'unknown')}")
        return jsonify({
            'success': result.get('success', False),
            'message': 'Subscribed successfully' if result.get('success') else 'Subscription failed',
            'duplicate': result.get('duplicate', False),
        })
    except Exception as e:
        print(f"Newsletter error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/contact', methods=['POST'])
def handle_contact():
    """Contact form - stores submission and could send notification email."""
    data = request.json
    if not data or not data.get('email'):
        return jsonify({'success': False, 'error': 'Email is required'}), 400

    # Log the contact form submission
    print(f"Contact form: {data.get('first_name', '')} {data.get('last_name', '')} <{data['email']}>")
    print(f"  Message: {data.get('message', 'N/A')[:100]}")

    # For now, just acknowledge receipt. Can add email notification later.
    return jsonify({'success': True, 'message': 'Contact form received'})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'planwell-webhooks'})


@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'service': 'PlanWell Webhook Server',
        'endpoints': [
            {'path': '/api/webinar', 'method': 'POST'},
            {'path': '/api/newsletter', 'method': 'POST'},
            {'path': '/api/contact', 'method': 'POST'},
            {'path': '/health', 'method': 'GET'},
        ],
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"PlanWell Webhook Server running on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
