"""
Webinar Registration Handler
==============================
Flask webhook endpoint to handle webinar registration submissions.
Registers in Zoom; Zoom handles its own confirmation email.

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
    "webinar_date": "2025-12-30T11:00:00-05:00"
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

app = Flask(__name__)
CORS(app)


@app.route('/api/webinar', methods=['POST'])
def handle_webinar_registration():
    """
    Handle webinar registration form submission.

    1. Register in Zoom (auto-discovers webinar by date)
    2. Return success response
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

    try:
        # Register in Zoom
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

        return jsonify({
            'success': True,
            'message': 'Registration received',
            'zoom_registered': zoom_result.get('success', False),
            'zoom_join_url': zoom_result.get('join_url', ''),
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
