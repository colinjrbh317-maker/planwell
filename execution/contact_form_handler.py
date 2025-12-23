"""
Contact Form Handler
====================
Flask webhook endpoint to handle contact form submissions.
Replaces the n8n contact form workflow.

Usage:
    python contact_form_handler.py

Expects POST to /api/contact with JSON:
{
    "first_name": "John",
    "last_name": "Smith",
    "email": "john@example.com",
    "phone": "555-123-4567",
    "message": "I have a question about..."
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

from google_sheets_client import SheetsClient

app = Flask(__name__)
CORS(app)

# Contact form uses a different sheet - configure the ID here or in .env
CONTACT_SHEET_ID = os.environ.get('CONTACT_SHEET_ID', os.environ.get('GOOGLE_SHEET_ID'))


class ContactSheetsClient(SheetsClient):
    """Extended client for contact form submissions."""
    
    def __init__(self):
        # Use contact sheet ID if different from webinar sheet
        super().__init__(sheet_id=CONTACT_SHEET_ID)
    
    def add_contact_submission(self, data: dict) -> int:
        """Add a contact form submission to the sheet."""
        row = [
            data.get('first_name', ''),
            data.get('last_name', ''),
            data.get('email', ''),
            data.get('phone', ''),
            data.get('message', ''),
            datetime.now().isoformat(),
            'contact_form'
        ]
        
        result = self.sheet.values().append(
            spreadsheetId=self.sheet_id,
            range='Sheet1!A:G',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [row]}
        ).execute()
        
        updated_range = result.get('updates', {}).get('updatedRange', '')
        if updated_range:
            return int(updated_range.split('!')[1].split(':')[0][1:])
        return -1


@app.route('/api/contact', methods=['POST'])
def handle_contact_form():
    """
    Handle contact form submission.
    Adds to Google Sheet (no notification emails - advisors check sheet directly).
    """
    data = request.json
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    email = data.get('email')
    if not email:
        return jsonify({'success': False, 'error': 'Email is required'}), 400
    
    try:
        sheets = ContactSheetsClient()
        row_num = sheets.add_contact_submission(data)
        
        print(f"Contact form submission added to row {row_num}")
        print(f"  Name: {data.get('first_name')} {data.get('last_name')}")
        print(f"  Email: {email}")
        
        return jsonify({
            'success': True,
            'message': 'Contact form received'
        })
        
    except Exception as e:
        print(f"Error handling contact form: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'service': 'contact-form'})


if __name__ == '__main__':
    port = int(os.environ.get('CONTACT_PORT', 5002))
    print(f"Starting Contact Form Handler on port {port}")
    print(f"Webhook URL: http://localhost:{port}/api/contact")
    app.run(host='0.0.0.0', port=port, debug=True)
