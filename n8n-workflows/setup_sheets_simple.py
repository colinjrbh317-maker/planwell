#!/usr/bin/env python3
"""
PlanWell Google Sheets Setup Script - Simple Version

Simpler version that focuses on creating sheets with correct headers.
Run: python3 setup_sheets_simple.py
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_credentials():
    """Get or create credentials for Google Sheets API."""
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("❌ ERROR: credentials.json not found!")
                exit(1)

            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def create_sheet_simple(service, title, headers):
    """Create a Google Sheet with headers."""
    print(f"\n📋 Creating {title}...")

    # Create spreadsheet
    spreadsheet = {
        'properties': {'title': title}
    }

    result = service.spreadsheets().create(body=spreadsheet).execute()
    spreadsheet_id = result.get('spreadsheetId')
    spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"

    # Get the first sheet's ID
    sheets = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheet_id = sheets['sheets'][0]['properties']['sheetId']

    # Write headers
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Sheet1!A1',
        valueInputOption='RAW',
        body={'values': [headers]}
    ).execute()

    # Simple formatting: header row bold with background color
    color = {'red': 0.26, 'green': 0.52, 'blue': 0.96} if 'Contact' in title else {'red': 0.06, 'green': 0.62, 'blue': 0.35}

    requests = [{
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': 0,
                'endRowIndex': 1
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': color,
                    'textFormat': {
                        'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
                        'bold': True
                    },
                    'horizontalAlignment': 'CENTER'
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }
    }, {
        'updateSheetProperties': {
            'properties': {
                'sheetId': sheet_id,
                'gridProperties': {'frozenRowCount': 1}
            },
            'fields': 'gridProperties.frozenRowCount'
        }
    }]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    print(f"✅ Sheet Created!")
    print(f"   ID: {spreadsheet_id}")
    print(f"   URL: {spreadsheet_url}")

    return {
        'id': spreadsheet_id,
        'url': spreadsheet_url,
        'name': title
    }

def main():
    """Main function to create both sheets."""
    print("=" * 60)
    print("PlanWell Google Sheets Setup - Simple Version")
    print("=" * 60)

    try:
        creds = get_credentials()
        service = build('sheets', 'v4', credentials=creds)

        # Create Contact Form Sheet
        contact_headers = ['First Name', 'Last Name', 'Email', 'Phone', 'Message', 'Submitted At', 'Source']
        contact_sheet = create_sheet_simple(service, 'PlanWell Contact Form Submissions', contact_headers)

        # Create Webinar Registration Sheet
        webinar_headers = ['First Name', 'Last Name', 'Email', 'Agency', 'Retirement Timeline', 'Submitted At', 'Source']
        webinar_sheet = create_sheet_simple(service, 'PlanWell Webinar Registrations', webinar_headers)

        # Print summary
        print("\n" + "=" * 60)
        print("✨ SETUP COMPLETE!")
        print("=" * 60)

        print("\n📋 CONTACT FORM SHEET:")
        print(f"   ID: {contact_sheet['id']}")
        print(f"   URL: {contact_sheet['url']}")

        print("\n🎓 WEBINAR REGISTRATION SHEET:")
        print(f"   ID: {webinar_sheet['id']}")
        print(f"   URL: {webinar_sheet['url']}")

        # Save IDs
        config = {
            'contact_form_sheet_id': contact_sheet['id'],
            'contact_form_url': contact_sheet['url'],
            'webinar_sheet_id': webinar_sheet['id'],
            'webinar_sheet_url': webinar_sheet['url']
        }

        with open('sheet_ids.json', 'w') as f:
            json.dump(config, f, indent=2)

        print("\n" + "=" * 60)
        print("NEXT STEPS:")
        print("=" * 60)
        print("1. Copy the Sheet IDs above")
        print("2. In n8n, configure each workflow:")
        print("   - Click 'Add to Google Sheet' node")
        print("   - Paste the appropriate Sheet ID")
        print("   - Set Sheet Name to 'Sheet1'")
        print("3. Configure Gmail OAuth")
        print("4. Activate both workflows")
        print("=" * 60)
        print("\n💾 Sheet IDs saved to sheet_ids.json")

    except HttpError as err:
        print(f"\n❌ Error: {err}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == '__main__':
    main()
