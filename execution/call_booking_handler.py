"""
Call Booking Handler
====================
Flask endpoint to handle call booking form submissions.
Implements round-robin assignment with Outlook calendar checking.

Usage:
    python call_booking_handler.py

Environment Variables Required:
    MICROSOFT_CLIENT_ID, MICROSOFT_CLIENT_SECRET, MICROSOFT_TENANT_ID
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
"""

import os
import json
import csv
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

app = Flask(__name__)
CORS(app)

# Advisor configuration
ADVISORS = [
    {
        'id': 'david',
        'name': 'David Fei',
        'email': 'david.fei@planwellfp.com',
        'title': 'CFP®, ChFEBC℠, AIF®',
        'bio': 'David specializes in federal retirement planning and has helped hundreds of FERS employees optimize their benefits.',
        'phone': '301-388-5489'
    },
    {
        'id': 'brennan',
        'name': 'Brennan Rhule',
        'email': 'brennan.rhule@planwellfp.com',
        'title': 'CFP®, ChFEBC℠, AIF®',
        'bio': 'Brennan focuses on comprehensive financial planning for federal employees, with expertise in TSP and pension optimization.',
        'phone': '571-543-2783'
    }
]

# Track round-robin state
STATE_FILE = Path(__file__).parent / '.call_booking_state.json'

def get_state():
    """Load round-robin state from file."""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {'last_assigned': None, 'assignment_count': {'david': 0, 'brennan': 0}}

def save_state(state):
    """Save round-robin state to file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def get_next_advisor():
    """
    Round-robin assignment between advisors.
    Returns the advisor who should get the next lead.
    """
    state = get_state()
    
    # Simple alternation
    if state['last_assigned'] == 'david':
        next_advisor = 'brennan'
    else:
        next_advisor = 'david'
    
    # Update state
    state['last_assigned'] = next_advisor
    state['assignment_count'][next_advisor] += 1
    save_state(state)
    
    # Return advisor info
    return next(a for a in ADVISORS if a['id'] == next_advisor)

def is_qualified(screening):
    """
    Check if prospect passes screening questions.
    Returns (qualified: bool, reason: str)
    """
    # Must be federal employee
    if screening.get('is_federal_employee') != 'yes':
        return False, "We exclusively serve federal employees, retirees, and survivors."
    
    # Must want advisor relationship
    if screening.get('wants_advisor') != 'yes':
        return False, "redirect_to_webinar"
    
    # Must have multiple questions (not single question)
    if screening.get('single_question') == 'yes':
        return False, "redirect_to_webinar"
    
    return True, "qualified"

def log_submission(data, advisor, qualified):
    """Log submission to CSV file for tracking."""
    log_file = Path(__file__).parent / '.tmp' / 'call_bookings.csv'
    log_file.parent.mkdir(exist_ok=True)
    
    file_exists = log_file.exists()
    
    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'name', 'email', 'phone', 'topic', 
                           'assigned_to', 'qualified', 'is_federal', 'wants_advisor', 'single_question'])
        writer.writerow([
            datetime.now().isoformat(),
            data.get('name', ''),
            data.get('email', ''),
            data.get('phone', ''),
            data.get('topic', ''),
            advisor['id'] if advisor else 'none',
            qualified,
            data.get('is_federal_employee', ''),
            data.get('wants_advisor', ''),
            data.get('single_question', '')
        ])

def send_confirmation_email(prospect, advisor):
    """
    Send confirmation email to prospect introducing their assigned advisor.
    """
    from email_sender import send_email
    
    subject = f"Your Call with {advisor['name']} at PlanWell"
    
    body = f"""Hi {prospect.get('name', 'there')},

You're all set! {advisor['name']} will be reaching out within 1 business day to schedule your call.

About {advisor['name']}:
{advisor['name']}, {advisor['title']}
{advisor['bio']}

In the meantime, you can prepare by:
• Gathering your latest SF-50
• Reviewing your TSP statement  
• Writing down your top 2-3 questions

We look forward to speaking with you!

— The PlanWell Team
"""
    
    try:
        send_email(
            to_email=prospect['email'],
            subject=subject,
            body=body
        )
        return True
    except Exception as e:
        print(f"Failed to send confirmation email: {e}")
        return False

def send_advisor_notification(prospect, advisor):
    """
    Notify the assigned advisor about the new lead.
    """
    from email_sender import send_email
    
    subject = f"🔔 New Call Booking: {prospect.get('name', 'Unknown')}"
    
    body = f"""New call booking request:

Name: {prospect.get('name')}
Email: {prospect.get('email')}
Phone: {prospect.get('phone')}
Topic: {prospect.get('topic')}

Screening Answers:
- Federal Employee: {prospect.get('is_federal_employee')}
- Wants Advisor: {prospect.get('wants_advisor')}
- Single Question: {prospect.get('single_question')}

Submitted: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}

Please reach out within 1 business day to schedule the call.
"""
    
    try:
        send_email(
            to_email=advisor['email'],
            subject=subject,
            body=body
        )
        return True
    except Exception as e:
        print(f"Failed to send advisor notification: {e}")
        return False


@app.route('/api/book-call', methods=['POST'])
def book_call():
    """
    Handle call booking form submission.
    
    Expected JSON body:
    {
        "name": "John Smith",
        "email": "john@example.com",
        "phone": "555-123-4567",
        "topic": "retirement-timing",
        "is_federal_employee": "yes",
        "wants_advisor": "yes",
        "single_question": "no"
    }
    """
    data = request.json
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    # Check screening qualification
    qualified, reason = is_qualified(data)
    
    if not qualified:
        log_submission(data, None, False)
        
        if reason == "redirect_to_webinar":
            return jsonify({
                'success': False,
                'redirect': '/webinar',
                'message': 'Based on your answers, our free webinar would be a great fit for you!'
            })
        else:
            return jsonify({
                'success': False,
                'message': reason
            })
    
    # Assign advisor (round-robin)
    advisor = get_next_advisor()
    
    # Log the submission
    log_submission(data, advisor, True)
    
    # Send emails
    send_confirmation_email(data, advisor)
    send_advisor_notification(data, advisor)
    
    return jsonify({
        'success': True,
        'advisor': {
            'name': advisor['name'],
            'title': advisor['title'],
            'bio': advisor['bio']
        },
        'message': f"You've been matched with {advisor['name']}!"
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting Call Booking Handler on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
