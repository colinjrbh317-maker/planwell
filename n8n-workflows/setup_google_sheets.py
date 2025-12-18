#!/usr/bin/env python3
"""
PlanWell Google Sheets Setup Script

This script creates and configures the Google Sheets needed for n8n workflows.

Requirements:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

Setup:
    1. Go to https://console.cloud.google.com/
    2. Create a new project (or select existing)
    3. Enable Google Sheets API
    4. Create OAuth 2.0 credentials (Desktop app)
    5. Download credentials.json and place in same folder as this script
    6. Run: python setup_google_sheets.py
"""

import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_credentials():
    """Get or create credentials for Google Sheets API."""
    creds = None

    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("❌ ERROR: credentials.json not found!")
                print("\nPlease follow these steps:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a new project or select existing")
                print("3. Enable Google Sheets API")
                print("4. Create OAuth 2.0 credentials (Desktop app)")
                print("5. Download credentials.json")
                print("6. Place it in the same folder as this script")
                exit(1)

            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def create_contact_form_sheet(service):
    """Create the Contact Form Submissions sheet."""
    print("\n📋 Creating Contact Form Sheet...")

    # Create spreadsheet
    spreadsheet = {
        'properties': {
            'title': 'PlanWell Contact Form Submissions'
        },
        'sheets': [{
            'properties': {
                'title': 'Sheet1',
                'gridProperties': {
                    'frozenRowCount': 1
                }
            }
        }]
    }

    spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId,spreadsheetUrl').execute()
    spreadsheet_id = spreadsheet.get('spreadsheetId')
    spreadsheet_url = spreadsheet.get('spreadsheetUrl')

    # Headers
    headers = [
        'First Name',
        'Last Name',
        'Email',
        'Phone',
        'Message',
        'Submitted At',
        'Source'
    ]

    # Write headers
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Sheet1!A1:G1',
        valueInputOption='RAW',
        body={'values': [headers]}
    ).execute()

    # Format header row
    requests = [
        # Header background color (blue)
        {
            'repeatCell': {
                'range': {
                    'sheetId': 0,
                    'startRowIndex': 0,
                    'endRowIndex': 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': 7
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {
                            'red': 0.26,
                            'green': 0.52,
                            'blue': 0.96
                        },
                        'textFormat': {
                            'foregroundColor': {
                                'red': 1.0,
                                'green': 1.0,
                                'blue': 1.0
                            },
                            'bold': True
                        },
                        'horizontalAlignment': 'CENTER'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
            }
        },
        # Set column widths
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': 1
                },
                'properties': {
                    'pixelSize': 120
                },
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 1,
                    'endIndex': 2
                },
                'properties': {
                    'pixelSize': 120
                },
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': 0,
                    'dimension': 'COLUMNS',
                    'startIndex': 2,
                    'endIndex': 3
                },
                'properties': {
                    'pixelSize': 200
                },
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': 0,
                    'dimension': 'COLUMNS',
                    'startIndex': 3,
                    'endIndex': 4
                },
                'properties': {
                    'pixelSize': 120
                },
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 4,
                    'endIndex': 5
                },
                'properties': {
                    'pixelSize': 300
                },
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 5,
                    'endIndex': 7
                },
                'properties': {
                    'pixelSize': 150
                },
                'fields': 'pixelSize'
            }
        }
    ]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    print(f"✅ Contact Form Sheet Created!")
    print(f"   Sheet ID: {spreadsheet_id}")
    print(f"   URL: {spreadsheet_url}")

    return {
        'id': spreadsheet_id,
        'url': spreadsheet_url,
        'name': 'PlanWell Contact Form Submissions'
    }

def create_webinar_registration_sheet(service):
    """Create the Webinar Registration Submissions sheet."""
    print("\n🎓 Creating Webinar Registration Sheet...")

    # Create spreadsheet
    spreadsheet = {
        'properties': {
            'title': 'PlanWell Webinar Registrations'
        },
        'sheets': [{
            'properties': {
                'title': 'Sheet1',
                'gridProperties': {
                    'frozenRowCount': 1
                }
            }
        }]
    }

    spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId,spreadsheetUrl').execute()
    spreadsheet_id = spreadsheet.get('spreadsheetId')
    spreadsheet_url = spreadsheet.get('spreadsheetUrl')

    # Headers
    headers = [
        'First Name',
        'Last Name',
        'Email',
        'Agency',
        'Retirement Timeline',
        'Submitted At',
        'Source'
    ]

    # Write headers
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range='Sheet1!A1:G1',
        valueInputOption='RAW',
        body={'values': [headers]}
    ).execute()

    # Format header row
    requests = [
        # Header background color (green)
        {
            'repeatCell': {
                'range': {
                    'sheetId': 0,
                    'startRowIndex': 0,
                    'endRowIndex': 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': 7
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {
                            'red': 0.06,
                            'green': 0.62,
                            'blue': 0.35
                        },
                        'textFormat': {
                            'foregroundColor': {
                                'red': 1.0,
                                'green': 1.0,
                                'blue': 1.0
                            },
                            'bold': True
                        },
                        'horizontalAlignment': 'CENTER'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
            }
        },
        # Set column widths
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': 0,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': 2
                },
                'properties': {
                    'pixelSize': 120
                },
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': 0,
                    'dimension': 'COLUMNS',
                    'startIndex': 2,
                    'endIndex': 3
                },
                'properties': {
                    'pixelSize': 200
                },
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': 0,
                    'dimension': 'COLUMNS',
                    'startIndex': 3,
                    'endIndex': 4
                },
                'properties': {
                    'pixelSize': 200
                },
                'fields': 'pixelSize'
            }
        },
        {
            'updateDimensionProperties': {
                'range': {
                    'sheetId': 0,
                    'dimension': 'COLUMNS',
                    'startIndex': 4,
                    'endIndex': 7
                },
                'properties': {
                    'pixelSize': 150
                },
                'fields': 'pixelSize'
            }
        }
    ]

    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests}
    ).execute()

    print(f"✅ Webinar Registration Sheet Created!")
    print(f"   Sheet ID: {spreadsheet_id}")
    print(f"   URL: {spreadsheet_url}")

    return {
        'id': spreadsheet_id,
        'url': spreadsheet_url,
        'name': 'PlanWell Webinar Registrations'
    }

def main():
    """Main function to create both sheets."""
    print("=" * 60)
    print("PlanWell Google Sheets Setup")
    print("=" * 60)

    try:
        # Get credentials
        creds = get_credentials()

        # Build service
        service = build('sheets', 'v4', credentials=creds)

        # Create both sheets
        contact_sheet = create_contact_form_sheet(service)
        webinar_sheet = create_webinar_registration_sheet(service)

        # Print summary
        print("\n" + "=" * 60)
        print("✨ SETUP COMPLETE!")
        print("=" * 60)

        print("\n📋 CONTACT FORM SHEET:")
        print(f"   Name: {contact_sheet['name']}")
        print(f"   ID: {contact_sheet['id']}")
        print(f"   URL: {contact_sheet['url']}")

        print("\n🎓 WEBINAR REGISTRATION SHEET:")
        print(f"   Name: {webinar_sheet['name']}")
        print(f"   ID: {webinar_sheet['id']}")
        print(f"   URL: {webinar_sheet['url']}")

        print("\n" + "=" * 60)
        print("NEXT STEPS:")
        print("=" * 60)
        print("1. Copy the Sheet IDs above")
        print("2. In n8n, edit each workflow:")
        print("   - Click 'Add to Google Sheet' node")
        print("   - Paste the appropriate Sheet ID")
        print("   - Set Sheet Name to 'Sheet1'")
        print("3. Configure Gmail OAuth credentials")
        print("4. Activate both workflows")
        print("5. Test with the curl commands in QUICK-START.md")
        print("=" * 60)

        # Save IDs to a file for easy reference
        config = {
            'contact_form_sheet_id': contact_sheet['id'],
            'contact_form_url': contact_sheet['url'],
            'webinar_sheet_id': webinar_sheet['id'],
            'webinar_sheet_url': webinar_sheet['url']
        }

        with open('sheet_ids.json', 'w') as f:
            json.dump(config, f, indent=2)

        print("\n💾 Sheet IDs saved to sheet_ids.json")

    except HttpError as err:
        print(f"\n❌ Error: {err}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
