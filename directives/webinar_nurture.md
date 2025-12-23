# Webinar Nurture Email Workflow

## Purpose
Automatically send timed nurture emails to webinar registrants based on their signup date relative to the webinar.

## Inputs
- Registration webhook: POST with name, email, agency, webinar_id, webinar_date
- Google Sheet: Registrant tracking with email send timestamps

## Tools/Scripts
- `execution/webinar_nurture_handler.py` - Flask webhook for registrations  
- `execution/webinar_nurture_scheduler.py` - Cron job for timed emails
- `execution/email_sender.py` - SMTP email sending
- `execution/google_sheets_client.py` - Google Sheets read/write

## Email Sequence
| Trigger | Purpose |
|---------|---------|
| Immediately | Confirmation + calendar invite |
| 7 days before | Build excitement, preview topics |
| 3 days before | What to prepare |
| 1 day before | Zoom link, logistics |
| Morning of | "Join now" |

## Flow

### Registration (webinar_nurture_handler.py)
1. Receive POST from webinar.astro form
2. Add row to Google Sheet with webinar info
3. Send confirmation email immediately
4. Update Email_Confirmation_Sent timestamp
5. Return success response

### Scheduled (webinar_nurture_scheduler.py)
1. Run via cron every hour
2. Read all registrants from Sheet
3. For each: calculate days until webinar
4. Send emails where timing matches and not already sent
5. Update sent timestamps

## Environment Variables
```
GOOGLE_SHEET_ID=1hfZaFYNwdAW6GC78HkQpCBf6yWqH-AqUZwVtTGgA4bo
SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
FROM_EMAIL, FROM_NAME
```

## Google Sheet Columns
First Name, Last Name, Email, Agency, Retirement Timeline, Submitted At, Source,
Webinar_ID, Webinar_Date, Email_Confirmation_Sent, Email_7Day_Sent, 
Email_3Day_Sent, Email_1Day_Sent, Email_DayOf_Sent

## Edge Cases
- Registration close to webinar: Skip already-passed emails
- Missing email: Log error, don't crash
- SMTP failure: Log to .tmp/, retry on next run

## Cron Setup
```bash
# Run every hour at :05
5 * * * * cd /path/to/planwell-site && python execution/webinar_nurture_scheduler.py
```

## Updates Log
- 2025-12-22: Initial creation
