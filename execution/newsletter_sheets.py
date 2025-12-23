"""
Newsletter Google Sheets Integration

Creates and manages the "Plan Well Newsletter Emails" Google Sheet
for collecting newsletter subscriptions from the blog.

Usage:
    python execution/newsletter_sheets.py setup    # Create the sheet
    python execution/newsletter_sheets.py add EMAIL    # Add an email manually
"""

import os
import sys
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

SHEET_NAME = "Plan Well Newsletter Emails"

def get_credentials():
    """Get or refresh Google credentials."""
    creds = None
    token_path = os.path.join(os.path.dirname(__file__), '..', 'token.pickle')
    credentials_path = os.path.join(os.path.dirname(__file__), '..', 'credentials.json')

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                print("Error: credentials.json not found. Please download it from Google Cloud Console.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def find_sheet_by_name(drive_service, name):
    """Find a Google Sheet by name."""
    results = drive_service.files().list(
        q=f"name='{name}' and mimeType='application/vnd.google-apps.spreadsheet'",
        spaces='drive',
        fields='files(id, name)'
    ).execute()

    files = results.get('files', [])
    return files[0]['id'] if files else None

def setup_sheet():
    """Create the newsletter emails Google Sheet."""
    creds = get_credentials()
    sheets_service = build('sheets', 'v4', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    # Check if sheet already exists
    existing_id = find_sheet_by_name(drive_service, SHEET_NAME)
    if existing_id:
        print(f"Sheet already exists: https://docs.google.com/spreadsheets/d/{existing_id}")
        return existing_id

    # Create new spreadsheet
    spreadsheet = {
        'properties': {'title': SHEET_NAME},
        'sheets': [{
            'properties': {'title': 'Subscribers'},
            'data': [{
                'rowData': [{
                    'values': [
                        {'userEnteredValue': {'stringValue': 'Email'}},
                        {'userEnteredValue': {'stringValue': 'Source'}},
                        {'userEnteredValue': {'stringValue': 'Subscribed At'}},
                        {'userEnteredValue': {'stringValue': 'Status'}},
                    ]
                }]
            }]
        }]
    }

    result = sheets_service.spreadsheets().create(body=spreadsheet).execute()
    sheet_id = result['spreadsheetId']

    # Format header row
    requests = [{
        'repeatCell': {
            'range': {'sheetId': 0, 'startRowIndex': 0, 'endRowIndex': 1},
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': {'red': 0.1, 'green': 0.2, 'blue': 0.4},
                    'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'bold': True}
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
        }
    }, {
        'updateSheetProperties': {
            'properties': {'sheetId': 0, 'gridProperties': {'frozenRowCount': 1}},
            'fields': 'gridProperties.frozenRowCount'
        }
    }]

    sheets_service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={'requests': requests}
    ).execute()

    print(f"Created sheet: https://docs.google.com/spreadsheets/d/{sheet_id}")
    print(f"\nSheet ID: {sheet_id}")
    print("\nTo receive form submissions, deploy this Apps Script:")
    print_apps_script(sheet_id)

    return sheet_id

def add_email(email, source='manual'):
    """Add an email to the newsletter sheet."""
    creds = get_credentials()
    sheets_service = build('sheets', 'v4', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    sheet_id = find_sheet_by_name(drive_service, SHEET_NAME)
    if not sheet_id:
        print("Sheet not found. Run 'setup' first.")
        return False

    # Add row
    values = [[email, source, datetime.now().isoformat(), 'active']]
    sheets_service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range='Subscribers!A:D',
        valueInputOption='RAW',
        body={'values': values}
    ).execute()

    print(f"Added: {email}")
    return True

def print_apps_script(sheet_id):
    """Print the Apps Script code for receiving form submissions."""
    script = f'''
// ===========================================
// APPS SCRIPT FOR NEWSLETTER FORM SUBMISSIONS
// ===========================================
// 1. Go to: https://script.google.com
// 2. Create new project
// 3. Paste this code
// 4. Deploy > New Deployment > Web App
// 5. Execute as: Me, Who has access: Anyone
// 6. Copy the Web App URL and update the blog page

const SHEET_ID = '{sheet_id}';

function doPost(e) {{
  try {{
    const data = JSON.parse(e.postData.contents);
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName('Subscribers');

    // Check for duplicate
    const emails = sheet.getRange('A:A').getValues().flat();
    if (emails.includes(data.email)) {{
      return ContentService.createTextOutput(JSON.stringify({{
        success: false,
        message: 'Email already subscribed'
      }})).setMimeType(ContentService.MimeType.JSON);
    }}

    // Add new subscriber
    sheet.appendRow([
      data.email,
      data.source || 'blog',
      data.timestamp || new Date().toISOString(),
      'active'
    ]);

    return ContentService.createTextOutput(JSON.stringify({{
      success: true,
      message: 'Subscribed successfully'
    }})).setMimeType(ContentService.MimeType.JSON);

  }} catch (error) {{
    return ContentService.createTextOutput(JSON.stringify({{
      success: false,
      message: error.message
    }})).setMimeType(ContentService.MimeType.JSON);
  }}
}}

function doGet(e) {{
  return ContentService.createTextOutput('Newsletter API is running');
}}
'''
    print(script)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python newsletter_sheets.py setup       # Create the sheet")
        print("  python newsletter_sheets.py add EMAIL   # Add an email")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'setup':
        setup_sheet()
    elif command == 'add' and len(sys.argv) >= 3:
        add_email(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
