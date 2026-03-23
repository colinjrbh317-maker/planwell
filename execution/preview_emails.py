#!/usr/bin/env python3
"""
Email Template Preview Generator
=================================
Generates a single HTML file that renders all 24 PlanWell email templates
so they can be previewed in a browser.

Usage:
    python preview_emails.py
    # Opens .tmp/email-template-preview.html
"""

import sys
import os
import html

# Add the execution directory to path so imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# --- Monkey-patch send_email to capture instead of send ---
import email_sender

captured_emails = []

def capture_email(to_email, subject, body, html_body=None):
    captured_emails.append({
        'to_email': to_email,
        'subject': subject,
        'body': body,
        'html_body': html_body
    })
    return True

email_sender.send_email = capture_email

# --- Now import all email modules (they use the patched send_email) ---
from webinar_emails import (
    send_webinar_confirmation, send_webinar_7day, send_webinar_3day,
    send_webinar_1day, send_webinar_dayof
)
from post_webinar_emails import (
    send_post_day1_takeaways, send_post_day3_takeaways,
    send_post_day7_benefits_report, send_post_day10_case_study,
    send_post_day14_soft_close, send_noshow_day1_missed,
    send_noshow_day5_next_webinar
)
from tsp_webinar_emails import (
    send_tsp_confirmation, send_tsp_7day, send_tsp_3day,
    send_tsp_1day, send_tsp_dayof
)
from tsp_post_webinar_emails import (
    send_tsp_post_day1_takeaways, send_tsp_post_day3_takeaways,
    send_tsp_post_day7_benefits_report, send_tsp_post_day10_case_study,
    send_tsp_post_day14_soft_close, send_tsp_noshow_day1_missed,
    send_tsp_noshow_day5_next_webinar
)

# --- Sample data ---
EMAIL = 'preview@example.com'
NAME = 'Sarah'
WEBINAR_DATE = 'Friday, April 10'
TIMEZONE = 'ET'
ZOOM_LINK = 'https://us06web.zoom.us/j/81503639493'
BOOKING_URL = 'https://planwellfp.com/book-call'
NEXT_WEBINAR_DATE = 'Thursday, May 1'
REG_URL = 'https://planwellfp.com/webinar'

# --- Define all emails in order, grouped by section ---
sections = [
    {
        'title': 'FERS Pre-Webinar',
        'color': '#1e3a5f',
        'emails': [
            ('Confirmation (Day 0)', lambda: send_webinar_confirmation(EMAIL, NAME, WEBINAR_DATE, TIMEZONE)),
            ('7-Day Reminder', lambda: send_webinar_7day(EMAIL, NAME, WEBINAR_DATE)),
            ('3-Day Reminder', lambda: send_webinar_3day(EMAIL, NAME, WEBINAR_DATE, TIMEZONE)),
            ('1-Day Reminder + Zoom Link', lambda: send_webinar_1day(EMAIL, NAME, WEBINAR_DATE, ZOOM_LINK, TIMEZONE)),
            ('Day-Of Reminder', lambda: send_webinar_dayof(EMAIL, NAME, ZOOM_LINK, TIMEZONE)),
        ]
    },
    {
        'title': 'FERS Post-Webinar (Attendee)',
        'color': '#2d6a4f',
        'emails': [
            ('Day +1: Key Takeaways', lambda: send_post_day1_takeaways(EMAIL, NAME, NEXT_WEBINAR_DATE, REG_URL)),
            ('Day +3: Top 3 Insights', lambda: send_post_day3_takeaways(EMAIL, NAME,
                'Your FERS pension is based on your High-3 salary and years of service — small moves in your final years can add tens of thousands.',
                'The FERS supplement bridges the gap between retirement and Social Security eligibility at 62.',
                'You can keep FEHB in retirement if you have been enrolled for 5+ continuous years before retiring.')),
            ('Day +7: Federal Benefits Report', lambda: send_post_day7_benefits_report(EMAIL, NAME, BOOKING_URL)),
            ('Day +10: Case Study', lambda: send_post_day10_case_study(EMAIL, NAME)),
            ('Day +14: Soft Close', lambda: send_post_day14_soft_close(EMAIL, NAME, BOOKING_URL)),
        ]
    },
    {
        'title': 'FERS Post-Webinar (No-Show)',
        'color': '#9b2226',
        'emails': [
            ('Day +1: What You Missed', lambda: send_noshow_day1_missed(EMAIL, NAME, NEXT_WEBINAR_DATE, REG_URL)),
            ('Day +5: Next Webinar Invite', lambda: send_noshow_day5_next_webinar(EMAIL, NAME, NEXT_WEBINAR_DATE, REG_URL)),
        ]
    },
    {
        'title': 'TSP Pre-Webinar',
        'color': '#7b2d8e',
        'emails': [
            ('Confirmation (Day 0)', lambda: send_tsp_confirmation(EMAIL, NAME, WEBINAR_DATE, TIMEZONE)),
            ('7-Day Reminder', lambda: send_tsp_7day(EMAIL, NAME, WEBINAR_DATE)),
            ('3-Day Reminder', lambda: send_tsp_3day(EMAIL, NAME, WEBINAR_DATE, TIMEZONE)),
            ('1-Day Reminder + Zoom Link', lambda: send_tsp_1day(EMAIL, NAME, WEBINAR_DATE, ZOOM_LINK, TIMEZONE)),
            ('Day-Of Reminder', lambda: send_tsp_dayof(EMAIL, NAME, ZOOM_LINK, TIMEZONE)),
        ]
    },
    {
        'title': 'TSP Post-Webinar (Attendee)',
        'color': '#b45309',
        'emails': [
            ('Day +1: Key Takeaways', lambda: send_tsp_post_day1_takeaways(EMAIL, NAME, NEXT_WEBINAR_DATE, REG_URL)),
            ('Day +3: Allocation Deep-Dive', lambda: send_tsp_post_day3_takeaways(EMAIL, NAME)),
            ('Day +7: TSP Review Offer', lambda: send_tsp_post_day7_benefits_report(EMAIL, NAME, BOOKING_URL)),
            ('Day +10: Case Study ($47K)', lambda: send_tsp_post_day10_case_study(EMAIL, NAME)),
            ('Day +14: Soft Close', lambda: send_tsp_post_day14_soft_close(EMAIL, NAME, BOOKING_URL)),
        ]
    },
    {
        'title': 'TSP Post-Webinar (No-Show)',
        'color': '#dc2626',
        'emails': [
            ('Day +1: What You Missed', lambda: send_tsp_noshow_day1_missed(EMAIL, NAME, NEXT_WEBINAR_DATE, REG_URL)),
            ('Day +5: Next Workshop Invite', lambda: send_tsp_noshow_day5_next_webinar(EMAIL, NAME, NEXT_WEBINAR_DATE, REG_URL)),
        ]
    },
]

# --- Call all email functions to capture the HTML ---
all_emails = []  # list of (section_title, section_color, timing_label, subject, html_body)

for section in sections:
    for timing_label, fn in section['emails']:
        idx_before = len(captured_emails)
        fn()
        if len(captured_emails) > idx_before:
            email = captured_emails[-1]
            all_emails.append((
                section['title'],
                section['color'],
                timing_label,
                email['subject'],
                email['html_body'] or email['body']
            ))

print(f"Captured {len(all_emails)} email templates.")

# --- Build the master HTML preview ---

def make_id(section_title, timing_label):
    return f"{section_title}-{timing_label}".lower().replace(' ', '-').replace('+', 'plus').replace('(', '').replace(')', '').replace(':', '').replace(',', '').replace('$', '').replace('#', '')

toc_html = ""
emails_html = ""
current_section = ""
email_counter = 0

for section_title, section_color, timing_label, subject, html_body in all_emails:
    email_counter += 1
    anchor_id = make_id(section_title, timing_label)

    if section_title != current_section:
        current_section = section_title
        section_id = make_id(section_title, "section")
        toc_html += f"""
        <div class="toc-section">
            <h3 style="color: {section_color}; margin: 18px 0 8px 0; font-size: 15px; text-transform: uppercase; letter-spacing: 1px;">{html.escape(section_title)}</h3>
        </div>"""
        emails_html += f"""
        <div class="section-divider" id="{section_id}">
            <h2 style="color: {section_color};">{html.escape(section_title)}</h2>
        </div>"""

    toc_html += f"""
            <a href="#{anchor_id}" class="toc-link">{email_counter}. {html.escape(timing_label)}</a>"""

    # Use srcdoc for iframe rendering of the email HTML
    escaped_html = html.escape(html_body) if html_body else ""

    emails_html += f"""
        <div class="email-card" id="{anchor_id}">
            <div class="email-header" style="border-left: 4px solid {section_color};">
                <div class="email-number" style="background: {section_color};">{email_counter}</div>
                <div class="email-meta">
                    <div class="email-timing">{html.escape(timing_label)}</div>
                    <div class="email-subject">Subject: {html.escape(subject)}</div>
                </div>
                <a href="#top" class="back-to-top">Back to top</a>
            </div>
            <div class="email-body">
                <iframe srcdoc="{escaped_html}" class="email-iframe" scrolling="no" onload="this.style.height = this.contentDocument.body.scrollHeight + 20 + 'px';"></iframe>
            </div>
        </div>"""

master_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PlanWell Email Templates Preview - All 24 Emails</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f0f2f5;
            color: #333;
            line-height: 1.5;
        }}
        .page-header {{
            background: linear-gradient(135deg, #1e3a5f 0%, #152a45 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }}
        .page-header h1 {{
            font-size: 28px;
            margin-bottom: 8px;
        }}
        .page-header p {{
            opacity: 0.8;
            font-size: 16px;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 32px;
            font-weight: bold;
            color: #c9a55c;
        }}
        .stat-label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            opacity: 0.7;
        }}
        .layout {{
            display: flex;
            max-width: 1200px;
            margin: 0 auto;
            gap: 0;
        }}
        .sidebar {{
            width: 280px;
            background: white;
            padding: 20px;
            position: sticky;
            top: 0;
            height: 100vh;
            overflow-y: auto;
            border-right: 1px solid #e0e0e0;
            flex-shrink: 0;
        }}
        .sidebar h2 {{
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #888;
            margin-bottom: 12px;
        }}
        .toc-link {{
            display: block;
            padding: 6px 12px;
            color: #555;
            text-decoration: none;
            font-size: 13px;
            border-radius: 4px;
            transition: all 0.15s;
        }}
        .toc-link:hover {{
            background: #f0f2f5;
            color: #1e3a5f;
        }}
        .main-content {{
            flex: 1;
            padding: 30px;
            max-width: 900px;
        }}
        .section-divider {{
            margin: 40px 0 20px 0;
            padding: 15px 20px;
            background: white;
            border-radius: 8px;
        }}
        .section-divider h2 {{
            font-size: 20px;
            margin: 0;
        }}
        .email-card {{
            background: white;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            overflow: hidden;
        }}
        .email-header {{
            display: flex;
            align-items: center;
            padding: 16px 20px;
            background: #fafafa;
            border-bottom: 1px solid #eee;
            gap: 14px;
        }}
        .email-number {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
            flex-shrink: 0;
        }}
        .email-meta {{
            flex: 1;
        }}
        .email-timing {{
            font-weight: 600;
            font-size: 14px;
            color: #333;
        }}
        .email-subject {{
            font-size: 13px;
            color: #666;
            margin-top: 2px;
        }}
        .back-to-top {{
            font-size: 12px;
            color: #999;
            text-decoration: none;
            flex-shrink: 0;
        }}
        .back-to-top:hover {{
            color: #1e3a5f;
        }}
        .email-body {{
            background: #e8e8e8;
            padding: 20px;
            display: flex;
            justify-content: center;
        }}
        .email-iframe {{
            width: 650px;
            border: none;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        @media (max-width: 1000px) {{
            .sidebar {{ display: none; }}
            .main-content {{ padding: 15px; }}
            .email-iframe {{ width: 100%; }}
        }}
    </style>
</head>
<body>
    <div class="page-header" id="top">
        <h1>PlanWell Email Templates</h1>
        <p>Complete preview of all nurture sequence emails</p>
        <div class="stats">
            <div class="stat">
                <div class="stat-number">{len(all_emails)}</div>
                <div class="stat-label">Templates</div>
            </div>
            <div class="stat">
                <div class="stat-number">6</div>
                <div class="stat-label">Sequences</div>
            </div>
            <div class="stat">
                <div class="stat-number">2</div>
                <div class="stat-label">Workshops</div>
            </div>
        </div>
    </div>
    <div class="layout">
        <div class="sidebar">
            <h2>Table of Contents</h2>
            {toc_html}
        </div>
        <div class="main-content">
            {emails_html}
        </div>
    </div>
    <script>
        // Auto-resize iframes after load
        document.querySelectorAll('.email-iframe').forEach(iframe => {{
            iframe.addEventListener('load', function() {{
                try {{
                    this.style.height = this.contentDocument.body.scrollHeight + 20 + 'px';
                }} catch(e) {{}}
            }});
        }});
    </script>
</body>
</html>"""

# --- Write output ---
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '.tmp', 'email-template-preview.html')
output_path = os.path.abspath(output_path)

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(master_html)

print(f"Preview saved to: {output_path}")
print(f"Open in browser: file://{output_path}")
