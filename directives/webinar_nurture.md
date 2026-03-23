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
Email_3Day_Sent, Email_1Day_Sent, Email_DayOf_Sent,
Attended, Recording_URL, Email_PostDay1_Sent, Email_PostDay3_Sent,
Email_PostDay7_Sent, Email_PostDay10_Sent, Email_PostDay14_Sent,
Email_NoShowDay1_Sent, Email_NoShowDay5_Sent

## Post-Webinar Sequence (Attendees)
| Trigger | Purpose |
|---------|---------|
| +1 day | Key takeaways summary + dual CTA (book call / next webinar) |
| +3 days | Top 3 key takeaways deep dive (educational value) |
| +7 days | Personalized Benefits Report offer → book call |
| +10 days | Case study success story |
| +14 days | Soft close — book free 30-min call |

**Note:** No recordings are shared post-webinar. This is a deliberate business decision to maintain urgency and encourage live attendance.

## Non-Attendee Re-engagement
| Trigger | Purpose |
|---------|---------|
| +1 day | "Here's what you missed" summary + dual CTA (book call / next webinar) |
| +5 days | Next webinar pre-registration |

**Note:** No recordings are shared with no-shows. Instead, content summary drives them to book a call or register for the next live session.

## Newsletter → Webinar Funnel
| Trigger | Purpose |
|---------|---------|
| -21 days | Early access announcement to subscribers |
| -14 days | Social proof email |
| -3 days | Last chance + scarcity |

## Mailchimp Migration Plan
All sequences migrating from SMTP to Mailchimp automations.
Tag-triggered automations replace cron-based scheduler for nurture sequences.
SMTP retained for transactional-only emails.

## Tag System
- `webinar-registered-{cycle-id}`, `webinar-attended-{cycle-id}`, `webinar-noshow-{cycle-id}`
- `retirement-timeline-{range}`: `under-5yr`, `5-10yr`, `10-plus-yr`
- `source-{channel}`: `organic`, `meta-ad`, `newsletter`, `referral`

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
- 2026-03-19: Added post-webinar, re-engagement, and newsletter funnel sequences
- 2026-03-19: Added Mailchimp migration plan and tag system
- 2026-03-22: Removed all recording references from post-webinar emails (business decision: no recordings shared to maintain live attendance urgency)
