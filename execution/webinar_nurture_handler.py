"""
Webinar Nurture Handler
========================
Flask webhook endpoint to handle webinar registration submissions.
Adds to Google Sheet and sends confirmation email immediately.

Usage:
    python webinar_nurture_handler.py

Expects POST to /api/webinar with JSON:
{
    "name": "John Smith",
    "email": "john@example.com",
    "agency": "DoD",
    "webinar_id": "dec-30-2025",
    "webinar_date": "2025-12-30T11:00:00-05:00"
}
"""

import os
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

# Import our modules
from google_sheets_client import SheetsClient
from webinar_emails import send_webinar_confirmation

app = Flask(__name__)
CORS(app)


def format_webinar_date(iso_date: str) -> str:
    """Convert ISO date to human-readable format."""
    try:
        dt = datetime.fromisoformat(iso_date.replace('Z', '+00:00'))
        return dt.strftime('%A, %B %d')  # e.g., "Monday, December 30"
    except:
        return iso_date


def get_timezone_from_date(iso_date: str) -> str:
    """Extract timezone abbreviation from ISO date."""
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


@app.route('/api/webinar', methods=['POST'])
def handle_webinar_registration():
    """
    Handle webinar registration form submission.
    
    1. Add to Google Sheet
    2. Send confirmation email
    3. Return success response
    """
    data = request.json
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    # Validate required fields
    email = data.get('email')
    if not email:
        return jsonify({'success': False, 'error': 'Email is required'}), 400
    
    try:
        # Initialize sheets client
        sheets = SheetsClient()
        sheets.ensure_headers()
        
        # Add registrant to sheet
        row_num = sheets.add_registrant({
            'name': data.get('name', ''),
            'email': email,
            'agency': data.get('agency', ''),
            'timeline': data.get('timeline', ''),
            'source': 'webinar_registration',
            'webinar_id': data.get('webinar_id', ''),
            'webinar_date': data.get('webinar_date', ''),
        })
        
        print(f"Added registrant to row {row_num}")
        
        # Format date for email
        webinar_date = format_webinar_date(data.get('webinar_date', ''))
        timezone = get_timezone_from_date(data.get('webinar_date', ''))
        first_name = data.get('name', '').split()[0] if data.get('name') else 'there'
        
        # Send confirmation email
        email_sent = send_webinar_confirmation(
            to_email=email,
            first_name=first_name,
            webinar_date=webinar_date,
            timezone=timezone
        )
        
        # Update email sent timestamp
        if email_sent and row_num > 0:
            sheets.update_email_sent(row_num, 'Email_Confirmation_Sent')
            print(f"Updated confirmation timestamp for row {row_num}")
        
        return jsonify({
            'success': True,
            'message': 'Registration received',
            'email_sent': email_sent
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
