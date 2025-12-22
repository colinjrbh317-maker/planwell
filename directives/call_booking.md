# Call Booking Workflow

## Purpose
Handle call booking form submissions, check Outlook calendar availability, assign round-robin to advisors, and send confirmation emails.

## Inputs
- Form data: name, email, phone, topic, screening answers
- Webhook POST to `/api/book-call`

## Tools/Scripts
- `execution/call_booking_handler.py` - Main Flask endpoint
- `execution/outlook_calendar.py` - Microsoft Graph API for calendar checks
- `execution/email_sender.py` - SMTP email sending

## Flow
1. Receive form submission via webhook
2. Validate screening answers (must be qualified)
3. Check David's Outlook calendar availability
4. Check Brennan's Outlook calendar availability
5. Assign based on round-robin + availability
6. Send confirmation email to prospect
7. Send notification to assigned advisor
8. Log to CSV file

## Environment Variables Required
```
MICROSOFT_CLIENT_ID=
MICROSOFT_CLIENT_SECRET=
MICROSOFT_TENANT_ID=
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=
```

## Edge Cases
- Both advisors unavailable: Still assign based on round-robin, note in email
- Invalid email: Return error, don't send
- Disqualified screening: Don't process, return redirect URL

## Updates Log
- 2025-12-22: Initial creation
