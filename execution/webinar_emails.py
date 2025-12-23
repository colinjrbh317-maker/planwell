"""
Webinar Email Templates
=======================
Pre-formatted HTML email templates for the webinar nurture sequence.

Usage:
    from webinar_emails import send_webinar_confirmation, send_webinar_7day, ...
"""

from email_sender import send_email


def send_webinar_confirmation(to_email: str, first_name: str, webinar_date: str, 
                               timezone: str = 'EST', calendar_link: str = None) -> bool:
    """
    Send confirmation email immediately after registration.
    """
    subject = f"You're registered for the FERS Workshop on {webinar_date}"
    
    plain_body = f"""Hi {first_name},

You're all set for the FERS Retirement Workshop!

Date: {webinar_date}
Time: 11:00 AM – 2:00 PM {timezone}
Location: Online via Zoom

What we'll cover:
• Your FERS pension calculation and strategies
• TSP optimization and withdrawal options
• FEHB and Medicare coordination
• Survivor benefits decisions
• Live Q&A with our Certified Financial Planners

Your Zoom link will be sent the day before the workshop.

Questions? Just reply to this email.

See you there,
The PlanWell Team

---
PlanWell Financial Planning
planwellfp.com
"""

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #1e3a5f 0%, #152a45 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 24px; }}
        .content {{ padding: 30px; background: #ffffff; }}
        .details-box {{ background: #f8f9fa; border-left: 4px solid #c9a55c; padding: 20px; margin: 20px 0; }}
        .details-box p {{ margin: 5px 0; }}
        .topics {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .topics h3 {{ color: #1e3a5f; margin-top: 0; }}
        .topics ul {{ margin: 0; padding-left: 20px; }}
        .topics li {{ margin: 8px 0; }}
        .note {{ background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>You're Registered!</h1>
        </div>
        <div class="content">
            <p>Hi {first_name},</p>
            <p>You're all set for the <strong>FERS Retirement Workshop</strong>!</p>
            
            <div class="details-box">
                <p><strong>📅 Date:</strong> {webinar_date}</p>
                <p><strong>🕐 Time:</strong> 11:00 AM – 2:00 PM {timezone}</p>
                <p><strong>📍 Location:</strong> Online via Zoom</p>
            </div>
            
            <div class="topics">
                <h3>What we'll cover:</h3>
                <ul>
                    <li>Your FERS pension calculation and strategies</li>
                    <li>TSP optimization and withdrawal options</li>
                    <li>FEHB and Medicare coordination</li>
                    <li>Survivor benefits decisions</li>
                    <li>Live Q&A with our Certified Financial Planners</li>
                </ul>
            </div>
            
            <div class="note">
                <strong>📧 Your Zoom link will be sent the day before the workshop.</strong>
            </div>
            
            <p>Questions? Just reply to this email.</p>
            <p>See you there,<br>The PlanWell Team</p>
        </div>
        <div class="footer">
            <p>PlanWell Financial Planning | planwellfp.com</p>
        </div>
    </div>
</body>
</html>
"""
    
    return send_email(to_email, subject, plain_body, html_body)


def send_webinar_7day(to_email: str, first_name: str, webinar_date: str) -> bool:
    """
    Send 7-day reminder email - preview topics, build excitement.
    """
    subject = "One week until the FERS Workshop – Here's what to expect"
    
    plain_body = f"""Hi {first_name},

Your FERS Retirement Workshop is coming up in one week ({webinar_date}).

Here's what makes this different from other benefits briefings:

✓ Led by Certified Financial Planners (not insurance salespeople)
✓ Specific to federal employees – we speak FERS fluently
✓ 3 hours of real content, not a 30-minute sales pitch
✓ Live Q&A where you can ask your specific questions

To get the most out of it:
• Grab your most recent LES (Leave and Earnings Statement)
• Have your years of service handy
• Think about questions you want answered

Over 500 federal employees have attended our workshops. We're looking forward to having you join us.

See you on {webinar_date},
The PlanWell Team
"""

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #1e3a5f 0%, #152a45 100%); color: white; padding: 30px; text-align: center; }}
        .content {{ padding: 30px; background: #ffffff; }}
        .highlight {{ color: #c9a55c; }}
        .checklist {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .checklist h3 {{ color: #1e3a5f; margin-top: 0; }}
        .different {{ background: #e8f4f8; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .different p {{ margin: 8px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>One Week to Go!</h1>
        </div>
        <div class="content">
            <p>Hi {first_name},</p>
            <p>Your FERS Retirement Workshop is coming up in <strong>one week</strong> ({webinar_date}).</p>
            
            <div class="different">
                <h3>Here's what makes this different:</h3>
                <p>✓ Led by Certified Financial Planners (not insurance salespeople)</p>
                <p>✓ Specific to federal employees – we speak FERS fluently</p>
                <p>✓ 3 hours of real content, not a 30-minute sales pitch</p>
                <p>✓ Live Q&A where you can ask your specific questions</p>
            </div>
            
            <div class="checklist">
                <h3>To get the most out of it:</h3>
                <p>• Grab your most recent LES</p>
                <p>• Have your years of service handy</p>
                <p>• Think about questions you want answered</p>
            </div>
            
            <p>Over 500 federal employees have attended our workshops. We're looking forward to having you join us.</p>
            <p>See you on {webinar_date},<br>The PlanWell Team</p>
        </div>
        <div class="footer">
            <p>PlanWell Financial Planning | planwellfp.com</p>
        </div>
    </div>
</body>
</html>
"""
    
    return send_email(to_email, subject, plain_body, html_body)


def send_webinar_3day(to_email: str, first_name: str, webinar_date: str, 
                       timezone: str = 'EST') -> bool:
    """
    Send 3-day reminder - what to prepare.
    """
    subject = "3 days until your FERS Workshop – Quick prep"
    
    plain_body = f"""Hi {first_name},

Just 3 days until the FERS Retirement Workshop on {webinar_date} at 11:00 AM {timezone}.

Quick things to have ready:
□ Your most recent LES
□ Number of years of creditable service
□ Any specific questions about your situation

Common questions we'll answer:
• "When can I retire with full benefits?"
• "How does the FERS supplement work?"
• "Should I keep FEHB or switch to Medicare?"
• "What happens to my TSP when I retire?"

Your Zoom link will arrive tomorrow.

See you soon,
The PlanWell Team
"""

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #1e3a5f 0%, #152a45 100%); color: white; padding: 30px; text-align: center; }}
        .content {{ padding: 30px; background: #ffffff; }}
        .prep-box {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .questions {{ background: #e8f4f8; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .note {{ background: #d4edda; padding: 15px; border-radius: 8px; margin: 20px 0; text-align: center; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>3 Days to Go!</h1>
        </div>
        <div class="content">
            <p>Hi {first_name},</p>
            <p>Just <strong>3 days</strong> until the FERS Retirement Workshop on <strong>{webinar_date}</strong> at 11:00 AM {timezone}.</p>
            
            <div class="prep-box">
                <h3>Quick things to have ready:</h3>
                <p>☐ Your most recent LES</p>
                <p>☐ Number of years of creditable service</p>
                <p>☐ Any specific questions about your situation</p>
            </div>
            
            <div class="questions">
                <h3>Common questions we'll answer:</h3>
                <p>• "When can I retire with full benefits?"</p>
                <p>• "How does the FERS supplement work?"</p>
                <p>• "Should I keep FEHB or switch to Medicare?"</p>
                <p>• "What happens to my TSP when I retire?"</p>
            </div>
            
            <div class="note">
                <strong>📧 Your Zoom link will arrive tomorrow.</strong>
            </div>
            
            <p>See you soon,<br>The PlanWell Team</p>
        </div>
        <div class="footer">
            <p>PlanWell Financial Planning | planwellfp.com</p>
        </div>
    </div>
</body>
</html>
"""
    
    return send_email(to_email, subject, plain_body, html_body)


def send_webinar_1day(to_email: str, first_name: str, webinar_date: str, 
                       zoom_link: str, timezone: str = 'EST') -> bool:
    """
    Send 1-day reminder with Zoom link.
    """
    subject = f"Tomorrow: Your FERS Workshop + Zoom Link"
    
    plain_body = f"""Hi {first_name},

Your FERS Retirement Workshop is tomorrow!

📅 {webinar_date}
🕐 11:00 AM – 2:00 PM {timezone}
📍 Join via Zoom: {zoom_link}

A few tips:
• Join a few minutes early to test your audio/video
• Have questions ready – we save plenty of time for Q&A
• Feel free to turn your camera off if you prefer

We recommend blocking off the full 3 hours. Most attendees tell us they wished they'd scheduled even more time.

See you tomorrow,
The PlanWell Team
"""

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #1e3a5f 0%, #152a45 100%); color: white; padding: 30px; text-align: center; }}
        .content {{ padding: 30px; background: #ffffff; }}
        .details-box {{ background: #f8f9fa; border-left: 4px solid #c9a55c; padding: 20px; margin: 20px 0; }}
        .join-btn {{ display: inline-block; background: linear-gradient(135deg, #c9a55c 0%, #a88a44 100%); color: #152a45; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 18px; margin: 20px 0; }}
        .tips {{ background: #e8f4f8; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>See You Tomorrow!</h1>
        </div>
        <div class="content">
            <p>Hi {first_name},</p>
            <p>Your FERS Retirement Workshop is <strong>tomorrow</strong>!</p>
            
            <div class="details-box">
                <p><strong>📅</strong> {webinar_date}</p>
                <p><strong>🕐</strong> 11:00 AM – 2:00 PM {timezone}</p>
            </div>
            
            <p style="text-align: center;">
                <a href="{zoom_link}" class="join-btn">Join Workshop</a>
            </p>
            <p style="text-align: center; font-size: 14px; color: #666;">
                Or copy this link: {zoom_link}
            </p>
            
            <div class="tips">
                <h3>A few tips:</h3>
                <p>• Join a few minutes early to test your audio/video</p>
                <p>• Have questions ready – we save plenty of time for Q&A</p>
                <p>• Feel free to turn your camera off if you prefer</p>
            </div>
            
            <p>We recommend blocking off the full 3 hours. Most attendees tell us they wished they'd scheduled even more time.</p>
            <p>See you tomorrow,<br>The PlanWell Team</p>
        </div>
        <div class="footer">
            <p>PlanWell Financial Planning | planwellfp.com</p>
        </div>
    </div>
</body>
</html>
"""
    
    return send_email(to_email, subject, plain_body, html_body)


def send_webinar_dayof(to_email: str, first_name: str, zoom_link: str, 
                        timezone: str = 'EST') -> bool:
    """
    Send day-of reminder (morning of webinar).
    """
    subject = "Starting in a few hours – Join the FERS Workshop"
    
    plain_body = f"""Hi {first_name},

The FERS Retirement Workshop starts today at 11:00 AM {timezone}.

📍 Join now: {zoom_link}

See you soon,
The PlanWell Team
"""

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #c9a55c 0%, #a88a44 100%); color: #152a45; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; }}
        .content {{ padding: 30px; background: #ffffff; text-align: center; }}
        .join-btn {{ display: inline-block; background: linear-gradient(135deg, #1e3a5f 0%, #152a45 100%); color: white; padding: 20px 40px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 20px; margin: 20px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Starts in a Few Hours!</h1>
        </div>
        <div class="content">
            <p>Hi {first_name},</p>
            <p style="font-size: 18px;">The FERS Retirement Workshop starts today at <strong>11:00 AM {timezone}</strong>.</p>
            
            <p>
                <a href="{zoom_link}" class="join-btn">Join Workshop Now</a>
            </p>
            <p style="font-size: 14px; color: #666;">
                {zoom_link}
            </p>
            
            <p>See you soon,<br>The PlanWell Team</p>
        </div>
        <div class="footer">
            <p>PlanWell Financial Planning | planwellfp.com</p>
        </div>
    </div>
</body>
</html>
"""
    
    return send_email(to_email, subject, plain_body, html_body)


if __name__ == '__main__':
    # Test email templates (will print to console if SMTP not configured)
    print("Testing webinar email templates...")
    
    # Test confirmation
    send_webinar_confirmation(
        to_email="test@example.com",
        first_name="John",
        webinar_date="Monday, December 30",
        timezone="EST"
    )
    print("✓ Confirmation template ready")
    
    # Test 7-day
    send_webinar_7day(
        to_email="test@example.com",
        first_name="John",
        webinar_date="Monday, December 30"
    )
    print("✓ 7-day template ready")
    
    # Test 3-day
    send_webinar_3day(
        to_email="test@example.com",
        first_name="John",
        webinar_date="Monday, December 30"
    )
    print("✓ 3-day template ready")
    
    # Test 1-day
    send_webinar_1day(
        to_email="test@example.com",
        first_name="John",
        webinar_date="Monday, December 30",
        zoom_link="https://zoom.us/j/123456789"
    )
    print("✓ 1-day template ready")
    
    # Test day-of
    send_webinar_dayof(
        to_email="test@example.com",
        first_name="John",
        zoom_link="https://zoom.us/j/123456789"
    )
    print("✓ Day-of template ready")
