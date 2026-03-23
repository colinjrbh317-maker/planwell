"""
Webinar Registration Handler
==============================
Flask webhook endpoint to handle webinar registration submissions.
Registers in Zoom, adds/updates subscriber in Mailchimp, and sends
SMTP confirmation email.

Usage:
    python webinar_nurture_handler.py

Expects POST to /api/webinar with JSON:
{
    "firstName": "John",
    "lastName": "Smith",
    "email": "john@example.com",
    "phone": "555-0100",       (optional)
    "agency": "DoD",
    "webinar_id": "dec-30-2025",
    "webinar_date": "2025-12-30T11:00:00-05:00",
    "webinar_type": "fers"     (optional, defaults to "fers"; also "tsp")
}
"""

import os
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

# Import our modules
from zoom_client import add_registrant as zoom_add_registrant, find_webinar_by_date
from mailchimp_client import add_subscriber_or_update

app = Flask(__name__)
CORS(app)


@app.route('/api/webinar', methods=['POST'])
def handle_webinar_registration():
    """
    Handle webinar registration form submission.

    1. Register in Zoom (auto-discovers webinar by date)
    2. Add/update subscriber in Mailchimp with merge fields and tags
    3. Send SMTP confirmation email (FERS or TSP template)
    4. Return success response
    """
    data = request.json

    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    # Validate required fields
    email = data.get('email')
    if not email:
        return jsonify({'success': False, 'error': 'Email is required'}), 400

    # Support both old (name) and new (firstName/lastName) field formats
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    if not first_name and data.get('name'):
        parts = data['name'].split(None, 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''

    phone = data.get('phone', '')
    full_name = f"{first_name} {last_name}".strip()
    webinar_type = data.get('webinar_type', 'fers')

    try:
        # --- Step 1: Register in Zoom ---
        zoom_result = {'success': False, 'join_url': ''}
        webinar_date_str = data.get('webinar_date', '')
        if webinar_date_str:
            # Extract date portion for matching (e.g., "2026-02-27")
            target_date = webinar_date_str[:10]
            zoom_webinar_id = find_webinar_by_date(target_date)

            if zoom_webinar_id:
                zoom_result = zoom_add_registrant(
                    webinar_id=zoom_webinar_id,
                    first_name=first_name or 'Attendee',
                    last_name=last_name or '',
                    email=email,
                    phone=phone,
                )
                if zoom_result.get('success'):
                    print(f"Zoom registration successful: {email} → webinar {zoom_webinar_id}")
                else:
                    print(f"Zoom registration warning (non-blocking): {zoom_result.get('error', 'unknown')}")
            else:
                print(f"No Zoom webinar found for date {target_date} — skipping Zoom registration")

        # --- Step 2: Add/update subscriber in Mailchimp ---
        mailchimp_result = {'success': False}
        try:
            mailchimp_result = add_subscriber_or_update(
                email=email,
                first_name=first_name,
                last_name=last_name,
                merge_fields={
                    'ZOOMURL': zoom_result.get('join_url', ''),
                    'WBNRDATE': webinar_date_str,
                    'WBNRTYPE': webinar_type,
                },
                tags=[
                    f'{webinar_type}-registered-{data.get("webinar_id", "")}',
                    f'webinar-type-{webinar_type}',
                ]
            )
            if mailchimp_result.get('success'):
                print(f"Mailchimp upsert successful: {email} ({mailchimp_result.get('status')})")
            else:
                print(f"Mailchimp upsert warning (non-blocking): {mailchimp_result.get('error', 'unknown')}")
        except Exception as mc_err:
            print(f"Mailchimp error (non-blocking): {mc_err}")

        # --- Step 3: Send SMTP confirmation email ---
        confirmation_sent = False
        try:
            if webinar_type == 'tsp':
                from tsp_webinar_emails import send_tsp_confirmation
                confirmation_sent = send_tsp_confirmation(email, first_name, webinar_date_str, 'ET')
            else:
                from webinar_emails import send_webinar_confirmation
                confirmation_sent = send_webinar_confirmation(email, first_name, webinar_date_str, 'ET')

            if confirmation_sent:
                print(f"Confirmation email sent: {email} (type={webinar_type})")
            else:
                print(f"Confirmation email failed (non-blocking): {email}")
        except Exception as email_err:
            print(f"Confirmation email error (non-blocking): {email_err}")

        return jsonify({
            'success': True,
            'message': 'Registration received',
            'zoom_registered': zoom_result.get('success', False),
            'zoom_join_url': zoom_result.get('join_url', ''),
            'mailchimp_registered': mailchimp_result.get('success', False),
            'confirmation_sent': confirmation_sent,
        })

    except Exception as e:
        print(f"Error handling registration: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'service': 'webinar-nurture'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting Webinar Nurture Handler on port {port}")
    print(f"Webhook URL: http://localhost:{port}/api/webinar")
    app.run(host='0.0.0.0', port=port, debug=True)
