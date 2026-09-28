"""
Webinar Registration Handler
==============================
Flask webhook endpoint to handle webinar registration submissions.
Registers in Zoom, adds/updates subscriber in Mailchimp, and sends
SMTP confirmation email.

Usage:
    python webinar_nurture_handler.py

Expects POST to /api/webinar with JSON:
{
    "firstName": "John",
    "lastName": "Smith",
    "email": "john@example.com",
    "phone": "555-0100",       (optional)
    "agency": "DoD",
    "webinar_id": "dec-30-2025",
    "webinar_date": "2025-12-30T11:00:00-05:00",
    "webinar_type": "fers"     (optional, defaults to "fers"; also "tsp")
}
"""

import os
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

# Import our modules
from zoom_client import add_registrant as zoom_add_registrant, find_webinar_by_date
from zoom_client import get_webinar as get_zoom_webinar
from mailchimp_client import add_subscriber_or_update

app = Flask(__name__)
CORS(app)


# Seconds between re-sends while Mailchimp reports "recipients not ready".
# Cumulative ~16 minutes.
CONFIRMATION_RETRY_DELAYS = (15, 30, 60, 120, 240, 480)


def _send_confirmation(email, first_name, formatted_date, webinar_type,
                       join_url, passcode, cal_links, retry_delays=CONFIRMATION_RETRY_DELAYS):
    try:
        if webinar_type == 'tsp':
            from tsp_webinar_emails import send_tsp_confirmation
            ok = send_tsp_confirmation(email, first_name, formatted_date, 'ET',
                                       calendar_link=cal_links.get('google', ''))
        else:
            from webinar_emails import send_webinar_confirmation
            ok = send_webinar_confirmation(
                email, first_name, formatted_date, 'ET',
                calendar_link=cal_links.get('google', ''),
                zoom_link=join_url,
                ics_link=cal_links.get('ics', ''),
                outlook_link=cal_links.get('outlook_web', ''),
                passcode=passcode,
                retry_delays=retry_delays,
            )
        if ok:
            print(f"Confirmation email sent: {email} (type={webinar_type})")
        else:
            print(f"Confirmation email failed (non-blocking): {email}")
        return ok
    except Exception as email_err:
        print(f"Confirmation email error (non-blocking): {email_err}")
        return False


def _send_confirmation_async(**kwargs):
    import threading
    t = threading.Thread(target=_send_confirmation, kwargs=kwargs, daemon=True)
    t.start()
    return t


@app.route('/api/webinar', methods=['POST'])
def handle_webinar_registration():
    """
    Handle webinar registration form submission.

    1. Register in Zoom (auto-discovers webinar by date)
    2. Add/update subscriber in Mailchimp with merge fields and tags
    3. Send SMTP confirmation email (FERS or TSP template)
    4. Return success response
    """
    data = request.json

    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400

    # Validate required fields
    email = data.get('email')
    if not email:
        return jsonify({'success': False, 'error': 'Email is required'}), 400

    # Support both old (name) and new (firstName/lastName) field formats
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    if not first_name and data.get('name'):
        parts = data['name'].split(None, 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ''

    phone = data.get('phone', '')
    full_name = f"{first_name} {last_name}".strip()
    webinar_type = data.get('webinar_type', 'fers')

    try:
        # --- Step 1: Register in Zoom ---
        zoom_result = {'success': False, 'join_url': ''}
        zoom_webinar = {}
        webinar_date_str = data.get('webinar_date', '')

        # Format date for human-readable display in emails
        # "2026-04-10T15:00:00.000Z" → "Thursday, April 10"
        formatted_date = webinar_date_str
        google_cal_url = ''
        try:
            from datetime import datetime, timedelta
            from urllib.parse import quote
            dt = datetime.fromisoformat(webinar_date_str.replace('Z', '+00:00'))
            formatted_date = dt.strftime('%A, %B %d').replace(' 0', ' ')

            # Build Google Calendar URL
            if webinar_type == 'tsp':
                cal_title = 'TSP Investment Strategies Workshop — PlanWell'
                cal_duration = timedelta(hours=1)
                cal_desc = 'Free 1-hour TSP workshop with David Fei, CFP. Covers fund allocation, Roth TSP, withdrawal strategies. Join via Zoom.'
            else:
                cal_title = 'FERS Retirement Workshop — PlanWell'
                cal_duration = timedelta(hours=3)
                cal_desc = 'Free 3-hour FERS workshop with Brennan Rhule and David Fei. Covers pension, TSP, FEHB, FEGLI, survivor benefits. Join via Zoom.'

            start_str = dt.strftime('%Y%m%dT%H%M%SZ')
            end_str = (dt + cal_duration).strftime('%Y%m%dT%H%M%SZ')
            google_cal_url = (
                f'https://calendar.google.com/calendar/render?action=TEMPLATE'
                f'&text={quote(cal_title)}'
                f'&dates={start_str}/{end_str}'
                f'&details={quote(cal_desc)}'
                f'&location={quote("Online via Zoom")}'
            )
        except Exception:
            formatted_date = webinar_date_str[:10] if webinar_date_str else 'TBD'
        if webinar_date_str:
            # Extract date portion for matching (e.g., "2026-02-27")
            target_date = webinar_date_str[:10]
            zoom_webinar_id = find_webinar_by_date(target_date)

            if zoom_webinar_id:
                zoom_result = zoom_add_registrant(
                    webinar_id=zoom_webinar_id,
                    first_name=first_name or 'Attendee',
                    # Zoom rejects an empty last_name (400 "The parameter is
                    # required: last_name"), which silently cost single-name
                    # registrants their Zoom seat and join link.
                    last_name=last_name or '-',
                    email=email,
                    phone=phone,
                )
                if zoom_result.get('success'):
                    print(f"Zoom registration successful: {email} → webinar {zoom_webinar_id}")
                    zoom_webinar = get_zoom_webinar(zoom_webinar_id)
                else:
                    print(f"Zoom registration warning (non-blocking): {zoom_result.get('error', 'unknown')}")
            else:
                print(f"No Zoom webinar found for date {target_date} — skipping Zoom registration")

        join_url = zoom_result.get('join_url', '') or ''

        # Put the personal join link in the calendar event too, so the invite
        # works on its own without waiting for a later email.
        if join_url and google_cal_url:
            from urllib.parse import quote
            google_cal_url = google_cal_url.replace(
                f'&location={quote("Online via Zoom")}',
                f'&location={quote(join_url)}',
            ).replace(
                f'&details={quote(cal_desc)}',
                f'&details={quote(cal_desc + " Your personal join link: " + join_url)}',
            )

        # Calendar options that work outside Google: a signed .ics served by
        # this server (Outlook desktop, Apple) plus Outlook on the web. Zoom's
        # own start_time is preferred over the form's date when we have it.
        passcode = zoom_webinar.get('password', '') if join_url else ''
        cal_links = {'ics': '', 'google': google_cal_url, 'outlook_web': ''}
        try:
            import webinar_calendar
            start_src = zoom_webinar.get('start_time') or webinar_date_str
            if start_src:
                start_utc = webinar_calendar.parse_start(start_src)
                cal_links = webinar_calendar.calendar_links(webinar_type, start_utc, join_url, passcode)
        except Exception as cal_err:
            print(f"Calendar link build failed (non-blocking): {cal_err}")

        # --- Step 2: Add/update subscriber in Mailchimp ---
        mailchimp_result = {'success': False}
        try:
            mailchimp_result = add_subscriber_or_update(
                email=email,
                first_name=first_name,
                last_name=last_name,
                merge_fields={
                    'ZOOMURL': join_url,
                    'WBNRDATE': webinar_date_str,
                    'WBNRTYPE': webinar_type,
                },
                tags=[
                    f'{webinar_type}-registered-{data.get("webinar_id", "")}',
                    f'webinar-type-{webinar_type}',
                ]
            )
            if mailchimp_result.get('success'):
                print(f"Mailchimp upsert successful: {email} ({mailchimp_result.get('status')})")
            else:
                print(f"Mailchimp upsert warning (non-blocking): {mailchimp_result.get('error', 'unknown')}")
        except Exception as mc_err:
            print(f"Mailchimp error (non-blocking): {mc_err}")

        # --- Step 3: Send the confirmation email (background, with retries) ---
        # A brand-new Mailchimp contact is not visible to campaign segments for
        # a short while, so the first send to a new registrant fails with
        # "recipients not ready". Retrying in a background thread keeps the
        # form response fast while the send completes a minute or two later.
        _send_confirmation_async(
            email=email,
            first_name=first_name,
            formatted_date=formatted_date,
            webinar_type=webinar_type,
            join_url=join_url,
            passcode=passcode,
            cal_links=cal_links,
        )
        confirmation_sent = 'queued'

        return jsonify({
            'success': True,
            'message': 'Registration received',
            'zoom_registered': zoom_result.get('success', False),
            'zoom_join_url': join_url,
            'join_url': join_url,
            'mailchimp_registered': mailchimp_result.get('success', False),
            'confirmation_sent': confirmation_sent,
        })

    except Exception as e:
        print(f"Error handling registration: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok', 'service': 'webinar-nurture'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting Webinar Nurture Handler on port {port}")
    print(f"Webhook URL: http://localhost:{port}/api/webinar")
    app.run(host='0.0.0.0', port=port, debug=True)
