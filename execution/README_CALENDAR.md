# Call Booking System - Setup Guide

## Overview
The call booking system uses a **simple local calendar** to track advisor availability and bookings.

## Required Credentials (Already Configured)

Your `.env` file has been configured with:

### SMTP Email (Smarsh Gateway)
```env
SMTP_HOST=agmail.smarshmail.com
SMTP_PORT=587
SMTP_USER=david.fei@planwellfp.com
SMTP_PASSWORD=Captaind@vegoinglong2
```

### Calendar System
- **Type:** Local JSON storage
- **Location:** `execution/calendar_bookings.json`
- **No API keys required** - simple file-based system

## How It Works

### 1. **Call Booking Form** (`/book-call`)
- User completes screening questions
- System checks qualification criteria
- Round-robin assigns to David or Brennan
- Emails sent automatically

### 2. **Calendar Management**
- Bookings stored in `calendar_bookings.json`
- System checks conflicts before booking
- Can find next available time slot
- Supports business hours restrictions

### 3. **Email Notifications**
- **To Client:** Confirmation with assigned advisor info
- **To Advisor:** New lead notification with details
- All emails sent via Smarsh (compliance-archived)

## Starting the Server

```bash
cd /Users/colinryan/PLAN\ WELL/planwell-site
python3 execution/call_booking_handler.py
```

Server runs on `http://localhost:5001`

## API Endpoints

### POST `/api/book-call`
Handle call booking submissions

**Request:**
```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "phone": "555-1234",
  "topic": "retirement-timing",
  "is_federal_employee": "yes",
  "wants_advisor": "yes",
  "single_question": "no"
}
```

**Response (Success):**
```json
{
  "success": true,
  "advisor": {
    "name": "David Fei",
    "title": "CFP®, ChFEBC℠, AIF®",
    "bio": "..."
  }
}
```

**Response (Redirect to Webinar):**
```json
{
  "success": false,
  "redirect": "/webinar",
  "message": "Our free webinar would be a great fit!"
}
```

## Calendar Python API

```python
from greminders_calendar import get_calendar

# Get calendar instance
calendar = get_calendar()

# Check availability
available = calendar.check_availability(
    email="david.fei@planwellfp.com",
    start_time=datetime(2026, 1, 15, 10, 0),
    duration_minutes=60
)

# Create booking
booking = calendar.create_booking(
    email="david.fei@planwellfp.com",
    start_time=datetime(2026, 1, 15, 10, 0),
    duration_minutes=60,
    client_name="John Smith",
    client_email="john@example.com",
    client_phone="555-1234",
    notes="Wants to discuss TSP allocation"
)

# Find next available slot
next_slot = calendar.find_next_available_slot(
    email="brennan.rhule@planwellfp.com",
    preferred_date=datetime.now(),
    duration_minutes=60
)
```

## Future Enhancements

If you want to integrate with actual GReminders/Google Calendar later:
1. Get GReminders OAuth credentials
2. Update `greminders_calendar.py` to use their API
3. Maintain same function signatures for backward compatibility

For now, the local calendar system is simpler and works perfectly for tracking bookings!
