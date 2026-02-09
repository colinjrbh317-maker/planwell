"""
Newsletter Subscription Handler
================================
Receives newsletter subscriptions from the homepage popup,
stores them in Google Sheets, and adds to Mailchimp.

Endpoint: POST /api/newsletter
Payload: { name, email, source, timestamp }
"""

from flask import request, jsonify
from datetime import datetime
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from newsletter_sheets import get_credentials, find_sheet_by_name, SHEET_NAME
from googleapiclient.discovery import build
from mailchimp_client import add_subscriber as mailchimp_add_subscriber


def handle_newsletter_subscription():
    """
    Handle newsletter subscription from homepage popup.

    Expected payload:
    {
        "name": "John Doe",
        "email": "john@example.com",
        "source": "homepage_popup",
        "timestamp": "2024-01-15T10:30:00.000Z"
    }
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data or 'email' not in data:
            return jsonify({
                'success': False,
                'error': 'Email is required'
            }), 400

        name = data.get('name', '')
        email = data['email'].strip().lower()
        source = data.get('source', 'homepage_popup')
        timestamp = data.get('timestamp', datetime.now().isoformat())

        # Get Google Sheets credentials
        creds = get_credentials()
        sheets_service = build('sheets', 'v4', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)

        # Find the newsletter sheet
        sheet_id = find_sheet_by_name(drive_service, SHEET_NAME)
        if not sheet_id:
            return jsonify({
                'success': False,
                'error': 'Newsletter sheet not found. Please run setup first.'
            }), 500

        # Check for duplicates
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range='Subscribers!A:A'
        ).execute()

        existing_emails = [row[0].lower() for row in result.get('values', []) if row]

        if email in existing_emails:
            return jsonify({
                'success': True,
                'message': 'Already subscribed',
                'duplicate': True
            })

        # Add new subscriber
        values = [[email, name, source, timestamp, 'active']]
        sheets_service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range='Subscribers!A:E',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': values}
        ).execute()

        print(f"Newsletter subscription added to Sheets: {email} from {source}")

        # Also add to Mailchimp
        mc_result = mailchimp_add_subscriber(
            email=email,
            first_name=name.split()[0] if name else '',
            tags=['free-guide', source]
        )
        if mc_result.get('success'):
            print(f"Mailchimp: {email} - {mc_result.get('status', 'subscribed')}")
        else:
            print(f"Mailchimp warning (non-blocking): {mc_result.get('error', 'unknown')}")

        return jsonify({
            'success': True,
            'message': 'Subscribed successfully',
            'mailchimp': mc_result.get('status', 'unknown')
        })

    except Exception as e:
        print(f"Error processing newsletter subscription: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    """Test the handler locally."""
    from flask import Flask
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app)

    app.add_url_rule('/api/newsletter', 'newsletter', handle_newsletter_subscription, methods=['POST'])

    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'ok', 'service': 'newsletter-handler'}

    port = int(os.environ.get('PORT', 5002))
    print(f"\nNewsletter Handler running on http://localhost:{port}")
    print(f"POST /api/newsletter - Newsletter subscription")
    app.run(host='0.0.0.0', port=port, debug=True)
