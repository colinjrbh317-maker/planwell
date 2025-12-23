"""
Google Sheets Client
====================
Wrapper for Google Sheets API operations.
Used for reading/writing webinar registrations and tracking email sends.

Usage:
    from google_sheets_client import SheetsClient
    client = SheetsClient()
    rows = client.get_all_registrants()
    client.update_email_sent(row_index, 'Email_Confirmation_Sent')
"""

import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Column mappings (0-indexed) - Updated: Retirement Timeline removed
COLUMNS = {
    'First Name': 0,
    'Last Name': 1,
    'Email': 2,
    'Agency': 3,
    'Submitted At': 4,
    'Source': 5,
    'Webinar_ID': 6,
    'Webinar_Date': 7,
    'Email_Confirmation_Sent': 8,
    'Email_7Day_Sent': 9,
    'Email_3Day_Sent': 10,
    'Email_1Day_Sent': 11,
    'Email_DayOf_Sent': 12,
}

def get_column_letter(index: int) -> str:
    """Convert 0-indexed column to letter (A, B, C, ...)"""
    return chr(ord('A') + index)


class SheetsClient:
    """Google Sheets client for webinar registrations."""
    
    def __init__(self, sheet_id: str = None):
        self.sheet_id = sheet_id or os.environ.get('GOOGLE_SHEET_ID')
        if not self.sheet_id:
            raise ValueError("GOOGLE_SHEET_ID not set in environment")
        
        self.creds = self._get_credentials()
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.sheet = self.service.spreadsheets()
    
    def _get_credentials(self) -> Credentials:
        """Get or refresh Google OAuth credentials."""
        creds = None
        token_path = Path(__file__).parent.parent / 'n8n-workflows' / 'token.json'
        creds_path = Path(__file__).parent.parent / 'n8n-workflows' / 'credentials.json'
        
        # Try parent directory as fallback
        if not creds_path.exists():
            creds_path = Path(__file__).parent.parent.parent / 'credentials.json'
            token_path = Path(__file__).parent.parent.parent / 'token.json'
        
        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not creds_path.exists():
                    raise FileNotFoundError(f"credentials.json not found at {creds_path}")
                flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        return creds
    
    def ensure_headers(self):
        """Ensure the sheet has all required headers."""
        headers = list(COLUMNS.keys())
        
        # Get current headers
        result = self.sheet.values().get(
            spreadsheetId=self.sheet_id,
            range='Sheet1!1:1'
        ).execute()
        
        current_headers = result.get('values', [[]])[0]
        
        # Add missing headers
        if len(current_headers) < len(headers):
            self.sheet.values().update(
                spreadsheetId=self.sheet_id,
                range='Sheet1!A1',
                valueInputOption='RAW',
                body={'values': [headers]}
            ).execute()
            print(f"Updated headers to include all {len(headers)} columns")
    
    def add_registrant(self, data: Dict[str, Any]) -> int:
        """
        Add a new registrant to the sheet.
        Returns the row number of the new entry.
        """
        # Prepare row data
        row = [''] * len(COLUMNS)
        row[COLUMNS['First Name']] = data.get('name', '').split()[0] if data.get('name') else ''
        row[COLUMNS['Last Name']] = ' '.join(data.get('name', '').split()[1:]) if data.get('name') else ''
        row[COLUMNS['Email']] = data.get('email', '')
        row[COLUMNS['Agency']] = data.get('agency', '')

        row[COLUMNS['Submitted At']] = datetime.now().isoformat()
        row[COLUMNS['Source']] = data.get('source', 'webinar_registration')
        row[COLUMNS['Webinar_ID']] = data.get('webinar_id', '')
        row[COLUMNS['Webinar_Date']] = data.get('webinar_date', '')
        
        # Append row
        result = self.sheet.values().append(
            spreadsheetId=self.sheet_id,
            range='Sheet1!A:M',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [row]}
        ).execute()
        
        # Parse the updated range to get row number
        updated_range = result.get('updates', {}).get('updatedRange', '')
        # Format: Sheet1!A2:N2
        if updated_range:
            row_num = int(updated_range.split('!')[1].split(':')[0][1:])
            return row_num
        return -1
    
    def get_all_registrants(self) -> List[Dict[str, Any]]:
        """Get all registrants with their data."""
        result = self.sheet.values().get(
            spreadsheetId=self.sheet_id,
            range='Sheet1!A:M'
        ).execute()
        
        rows = result.get('values', [])
        if len(rows) <= 1:
            return []  # Only header or empty
        
        registrants = []
        for i, row in enumerate(rows[1:], start=2):  # Skip header, 1-indexed
            # Pad row to ensure we have all columns
            row = row + [''] * (len(COLUMNS) - len(row))
            
            registrants.append({
                'row_number': i,
                'first_name': row[COLUMNS['First Name']],
                'last_name': row[COLUMNS['Last Name']],
                'email': row[COLUMNS['Email']],
                'agency': row[COLUMNS['Agency']],
                'webinar_id': row[COLUMNS['Webinar_ID']],
                'webinar_date': row[COLUMNS['Webinar_Date']],
                'email_confirmation_sent': row[COLUMNS['Email_Confirmation_Sent']],
                'email_7day_sent': row[COLUMNS['Email_7Day_Sent']],
                'email_3day_sent': row[COLUMNS['Email_3Day_Sent']],
                'email_1day_sent': row[COLUMNS['Email_1Day_Sent']],
                'email_dayof_sent': row[COLUMNS['Email_DayOf_Sent']],
            })
        
        return registrants
    
    def update_email_sent(self, row_number: int, column_name: str) -> bool:
        """Update a specific email sent timestamp."""
        if column_name not in COLUMNS:
            raise ValueError(f"Unknown column: {column_name}")
        
        col_letter = get_column_letter(COLUMNS[column_name])
        cell_range = f'Sheet1!{col_letter}{row_number}'
        
        self.sheet.values().update(
            spreadsheetId=self.sheet_id,
            range=cell_range,
            valueInputOption='RAW',
            body={'values': [[datetime.now().isoformat()]]}
        ).execute()
        
        return True


if __name__ == '__main__':
    # Test the client
    print("Testing Google Sheets client...")
    try:
        client = SheetsClient()
        client.ensure_headers()
        registrants = client.get_all_registrants()
        print(f"Found {len(registrants)} registrants")
        for r in registrants[:3]:
            print(f"  - {r['first_name']} {r['last_name']} ({r['email']})")
    except Exception as e:
        print(f"Error: {e}")
