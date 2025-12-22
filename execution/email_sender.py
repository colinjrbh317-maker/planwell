"""
Email Sender
=============
SMTP email sending utility for call booking confirmations and notifications.

Usage:
    from email_sender import send_email
    send_email(to_email, subject, body)
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent / '.env')

def send_email(to_email: str, subject: str, body: str, html_body: str = None) -> bool:
    """
    Send an email via SMTP.
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        body: Plain text email body
        html_body: Optional HTML version of the body
        
    Returns:
        True if email was sent successfully, False otherwise
    """
    smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', 587))
    smtp_user = os.environ.get('SMTP_USER')
    smtp_password = os.environ.get('SMTP_PASSWORD')
    from_email = os.environ.get('FROM_EMAIL', smtp_user)
    from_name = os.environ.get('FROM_NAME', 'PlanWell Financial Planning')
    
    if not smtp_user or not smtp_password:
        print("Warning: SMTP credentials not configured. Email not sent.")
        print(f"Would have sent to: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body: {body[:200]}...")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{from_name} <{from_email}>"
        msg['To'] = to_email
        
        # Attach plain text version
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach HTML version if provided
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))
        
        # Connect and send
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        print(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_confirmation_html(to_email: str, prospect_name: str, advisor: dict) -> bool:
    """
    Send a nicely formatted HTML confirmation email.
    
    Args:
        to_email: Prospect's email
        prospect_name: Prospect's name
        advisor: Dict with advisor info (name, title, bio, email)
    """
    subject = f"Your Call with {advisor['name']} at PlanWell"
    
    plain_body = f"""Hi {prospect_name},

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
    
    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #1e3a5f; color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 30px; background: #f9f9f9; }}
        .advisor-card {{ background: white; border-radius: 8px; padding: 20px; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .advisor-name {{ color: #1e3a5f; font-size: 1.3em; margin-bottom: 5px; }}
        .advisor-title {{ color: #c9a55c; font-size: 0.9em; margin-bottom: 10px; }}
        .checklist {{ background: white; border-radius: 8px; padding: 20px; margin: 20px 0; }}
        .checklist li {{ margin: 10px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>You're All Set!</h1>
        </div>
        <div class="content">
            <p>Hi {prospect_name},</p>
            <p><strong>{advisor['name']}</strong> will be reaching out within 1 business day to schedule your call.</p>
            
            <div class="advisor-card">
                <div class="advisor-name">{advisor['name']}</div>
                <div class="advisor-title">{advisor['title']}</div>
                <p>{advisor['bio']}</p>
            </div>
            
            <div class="checklist">
                <p><strong>In the meantime, you can prepare by:</strong></p>
                <ul>
                    <li>Gathering your latest SF-50</li>
                    <li>Reviewing your TSP statement</li>
                    <li>Writing down your top 2-3 questions</li>
                </ul>
            </div>
            
            <p>We look forward to speaking with you!</p>
        </div>
        <div class="footer">
            <p>— The PlanWell Team</p>
            <p>PlanWell Financial Planning | planwellfp.com</p>
        </div>
    </div>
</body>
</html>
"""
    
    return send_email(to_email, subject, plain_body, html_body)


if __name__ == '__main__':
    # Test email sending
    print("Testing email sender...")
    test_result = send_email(
        to_email="test@example.com",
        subject="Test Email from PlanWell",
        body="This is a test email."
    )
    print(f"Test result: {'Success' if test_result else 'Failed (check SMTP config)'}")
