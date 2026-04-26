"""
Webinar Email Templates
=======================
Pre-formatted HTML email templates for the FERS webinar nurture sequence.
Mobile-first, table-based layout with 100% inline CSS for Outlook compatibility.

Sequence:
  1. Confirmation  — immediate, on registration
  2. 7-day         — build anticipation, set expectations
  3. 3-day         — prep checklist, surface key questions
  4. 1-day         — logistics + Zoom link
  5. Day-of        — short, high-urgency, single CTA

Usage:
    from webinar_emails import send_webinar_confirmation, send_webinar_7day, ...
"""

from email_sender import send_email


# ---------------------------------------------------------------------------
# Shared HTML helpers (all CSS inline, table layout, no gradients)
# ---------------------------------------------------------------------------

def _base_html(preheader, header_bg, header_text_color,
               header_line1, header_line2, body_html):
    """
    Wraps content in a consistent, mobile-first, inline-CSS email shell.
    Table layout for Outlook compatibility. No gradients. No <style> blocks.
    """
    if header_line2:
        sub = ('<p style="margin:8px 0 0 0;font-size:15px;color:' +
               header_text_color + ';opacity:0.85;">' + header_line2 + '</p>')
    else:
        sub = ''

    return (
        '<!DOCTYPE html>\n'
        '<html lang="en">\n'
        '<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        '<meta http-equiv="X-UA-Compatible" content="IE=edge">\n'
        '<title>PlanWell FERS Workshop</title>\n'
        '</head>\n'
        '<body style="margin:0;padding:0;background-color:#f5f5f5;'
        'font-family:Arial,Helvetica,sans-serif;">\n\n'
        '<!-- Preheader -->\n'
        '<span style="display:none;font-size:1px;color:#f5f5f5;max-height:0;'
        'max-width:0;opacity:0;overflow:hidden;">' + preheader + '</span>\n\n'
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"'
        ' style="background-color:#f5f5f5;">\n'
        '  <tr><td align="center" style="padding:20px 10px;">\n\n'
        '    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"'
        ' style="max-width:600px;background-color:#ffffff;">\n\n'
        '      <!-- HEADER -->\n'
        '      <tr><td align="center" style="background-color:' + header_bg + ';padding:32px 30px;">\n'
        '        <p style="margin:0;font-size:12px;font-weight:bold;letter-spacing:2px;'
        'text-transform:uppercase;color:' + header_text_color + ';opacity:0.75;">'
        'FERS Retirement Workshop</p>\n'
        '        <h1 style="margin:8px 0 0 0;font-size:26px;font-weight:bold;color:' +
        header_text_color + ';line-height:1.3;">' + header_line1 + '</h1>\n' +
        sub + '\n'
        '      </td></tr>\n\n'
        '      <!-- BODY -->\n'
        '      <tr><td style="padding:32px 30px;color:#333333;font-size:15px;line-height:1.7;">\n' +
        body_html + '\n'
        '      </td></tr>\n\n'
        '      <!-- FOOTER -->\n'
        '      <tr><td style="background-color:#f5f5f5;padding:24px 30px;text-align:center;'
        'border-top:1px solid #e0e0e0;">\n'
        '        <p style="margin:0 0 6px 0;font-size:13px;color:#666666;font-weight:bold;">'
        'PlanWell Financial Planning</p>\n'
        '        <p style="margin:0;font-size:13px;color:#666666;">'
        '<a href="https://planwellfp.com" style="color:#1e3a5f;text-decoration:none;">'
        'planwellfp.com</a></p>\n'
        '      </td></tr>\n\n'
        '      <!-- COMPLIANCE DISCLAIMER -->\n'
        '      <tr><td style="padding:20px 30px;text-align:center;">\n'
        '        <p style="margin:0 0 10px 0;font-size:11px;color:#999999;line-height:1.5;">'
        'Securities and advisory services offered through '
        '<a href="https://www.osaic.com" style="color:#999999;text-decoration:underline;">Osaic</a> '
        'Wealth, Inc., member '
        '<a href="https://www.finra.org/" style="color:#999999;text-decoration:underline;">FINRA</a>, '
        '<a href="https://www.sipc.org/" style="color:#999999;text-decoration:underline;">SIPC</a>. '
        'Osaic Wealth is separately owned and other entities and/or marketing names, products or '
        'services referenced here are independent of Osaic Wealth.</p>\n'
        '        <p style="margin:0 0 10px 0;font-size:11px;color:#999999;line-height:1.5;">'
        'PlanWell Financial Planning, LLC is not affiliated with, endorsed by, or authorized to '
        'speak on behalf of the U.S. Government, OPM, the Federal Employee Retirement System, or '
        'any other federal agency benefits programs or retirement plans, including the Thrift '
        'Savings Plan.</p>\n'
        '        <p style="margin:0 0 10px 0;font-size:11px;color:#999999;line-height:1.5;">'
        'The content is developed from sources believed to be providing accurate information. '
        'The information in this material is not intended as tax or legal advice. Please consult '
        'legal or tax professionals for specific information regarding your individual situation.</p>\n'
        '        <p style="margin:0;font-size:11px;color:#999999;line-height:1.5;">'
        'Check the background of your financial professional on FINRA\'s '
        '<a href="https://brokercheck.finra.org/" style="color:#999999;text-decoration:underline;">'
        'BrokerCheck</a>. View Osaic '
        '<a href="https://www.osaic.com/crs" style="color:#999999;text-decoration:underline;">'
        'Form CRS</a>.</p>\n'
        '      </td></tr>\n\n'
        '    </table>\n\n'
        '  </td></tr>\n'
        '</table>\n\n'
        '</body>\n</html>'
    )


def _gold_button(url, label):
    """Solid gold CTA button, min 44px touch target."""
    return (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0"'
        ' style="margin:24px auto;">\n'
        '  <tr><td align="center" style="background-color:#c9a55c;border-radius:6px;">\n'
        '    <a href="' + url + '" style="display:inline-block;padding:0 32px;'
        'font-size:16px;font-weight:bold;color:#1e3a5f;text-decoration:none;'
        'font-family:Arial,Helvetica,sans-serif;line-height:48px;min-height:48px;">'
        + label + '</a>\n'
        '  </td></tr>\n'
        '</table>'
    )


def _section_box(bg, border_color, content):
    """Bordered left-accent box."""
    return (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"'
        ' style="margin:20px 0;">\n'
        '  <tr><td style="background-color:' + bg + ';border-left:4px solid ' +
        border_color + ';padding:18px 20px;font-size:15px;color:#333333;line-height:1.7;">\n' +
        content + '\n'
        '  </td></tr>\n'
        '</table>'
    )


def _detail_row(label, value):
    return (
        '<tr>\n'
        '  <td style="padding:5px 0;font-size:15px;color:#333333;white-space:nowrap;">'
        '<strong style="color:#1e3a5f;">' + label + '</strong></td>\n'
        '  <td style="padding:5px 0 5px 14px;font-size:15px;color:#333333;">' + value + '</td>\n'
        '</tr>'
    )


def _navy_note(text):
    """Full-width navy callout for important one-liners."""
    return (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"'
        ' style="margin:20px 0;">\n'
        '  <tr><td style="background-color:#1e3a5f;padding:16px 20px;border-radius:4px;'
        'text-align:center;">\n'
        '    <p style="margin:0;font-size:15px;color:#ffffff;"><strong>' + text + '</strong></p>\n'
        '  </td></tr>\n'
        '</table>'
    )


# ---------------------------------------------------------------------------
# 1. Confirmation Email
# ---------------------------------------------------------------------------

def send_webinar_confirmation(to_email, first_name, webinar_date,
                               timezone='ET', calendar_link=''):
    """
    Send confirmation email immediately after registration.
    Purpose: Confirm the spot, set expectations, give one action (add to calendar).
    """
    subject = "You're registered for the FERS Workshop on " + webinar_date

    plain_body = (
        "Hi " + first_name + ",\n\n"
        "You're registered. Here are your details:\n\n"
        "  Date:    " + webinar_date + "\n"
        "  Time:    11:00 AM - 2:00 PM " + timezone + "\n"
        "  Format:  Online via Zoom (link arrives the day before)\n"
        "  Cost:    Free\n\n"
        "David Fei, CFP(r) will lead the workshop, covering the FERS pension formula, "
        "TSP withdrawal strategies, and how FEHB, FEGLI, and Social Security fit together "
        "in retirement. Brennan Rhule, CFP(r) will be available throughout to answer your "
        "questions in the chat.\n\n"
        "The full 3 hours are spent on content. No sales pitch. The goal is for you to "
        "leave knowing your numbers and your options.\n\n"
        "One thing to do before the workshop: pull up your most recent LES (Leave and Earnings "
        "Statement). Having your base pay and years of creditable service in front of you makes "
        "the pension calculation section much more useful.\n\n"
        "Your Zoom link will arrive the day before the workshop.\n\n"
        "See you on " + webinar_date + ",\n"
        "David & Brennan\n"
        "PlanWell Financial Planning\n"
        "planwellfp.com\n\n"
        "---\n"
        "Questions? Reply to this email.\n"
    )

    details_rows = (
        _detail_row("Date:", webinar_date) +
        _detail_row("Time:", "11:00 AM &ndash; 2:00 PM " + timezone) +
        _detail_row("Format:", "Online via Zoom") +
        _detail_row("Zoom link:", "Arrives the day before")
    )

    cal_btn = _gold_button(calendar_link, "Add to Calendar") if calendar_link else ""

    topics_content = (
        '<p style="margin:0 0 12px 0;font-size:15px;color:#1e3a5f;font-weight:bold;">'
        'What David will cover in 3 hours:</p>\n'
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0;">\n'
        '  <tr><td style="padding:4px 8px 4px 0;vertical-align:top;font-size:15px;color:#c9a55c;">&#8226;</td>'
        '<td style="padding:4px 0;font-size:15px;color:#333333;">FERS pension formula and how to run your own numbers</td></tr>\n'
        '  <tr><td style="padding:4px 8px 4px 0;vertical-align:top;font-size:15px;color:#c9a55c;">&#8226;</td>'
        '<td style="padding:4px 0;font-size:15px;color:#333333;">TSP withdrawal strategies (Roth vs. traditional, RMDs, sequencing)</td></tr>\n'
        '  <tr><td style="padding:4px 8px 4px 0;vertical-align:top;font-size:15px;color:#c9a55c;">&#8226;</td>'
        '<td style="padding:4px 0;font-size:15px;color:#333333;">FEHB in retirement and the Medicare Part B decision</td></tr>\n'
        '  <tr><td style="padding:4px 8px 4px 0;vertical-align:top;font-size:15px;color:#c9a55c;">&#8226;</td>'
        '<td style="padding:4px 0;font-size:15px;color:#333333;">FEGLI: what to keep, what to drop, and when</td></tr>\n'
        '  <tr><td style="padding:4px 8px 4px 0;vertical-align:top;font-size:15px;color:#c9a55c;">&#8226;</td>'
        '<td style="padding:4px 0;font-size:15px;color:#333333;">Survivor benefit election and what it costs your annuity</td></tr>\n'
        '  <tr><td style="padding:4px 8px 4px 0;vertical-align:top;font-size:15px;color:#c9a55c;">&#8226;</td>'
        '<td style="padding:4px 0;font-size:15px;color:#333333;">Social Security coordination with your FERS annuity</td></tr>\n'
        '</table>'
    )

    details_box = (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"'
        ' style="margin:20px 0;background-color:#f5f5f5;border-left:4px solid #c9a55c;">\n'
        '  <tr><td style="padding:18px 20px;">\n'
        '    <table role="presentation" cellpadding="0" cellspacing="0" border="0">\n' +
        details_rows + '\n'
        '    </table>\n'
        '  </td></tr>\n'
        '</table>'
    )

    body_html = (
        '<p style="margin:0 0 16px 0;">Hi ' + first_name + ',</p>\n\n'
        '<p style="margin:0 0 16px 0;">You\'re registered. Here are your details:</p>\n\n' +
        details_box + '\n\n' +
        cal_btn + '\n\n' +
        _section_box('#f5f5f5', '#1e3a5f', topics_content) + '\n\n'
        '<p style="margin:20px 0 16px 0;"><strong>One thing to do before the workshop:</strong> '
        'pull up your most recent LES (Leave and Earnings Statement). Having your base pay and '
        'years of creditable service in front of you makes the pension calculation section much '
        'more useful.</p>\n\n'
        '<p style="margin:0 0 16px 0;">The full 3 hours are spent on content: your pension, '
        'your TSP, your benefits. David presents, and Brennan is in the chat to answer your '
        'questions throughout. You\'ll leave knowing your numbers.</p>\n\n'
        '<p style="margin:0 0 8px 0;">See you on ' + webinar_date + ',</p>\n'
        '<p style="margin:0;font-weight:bold;color:#1e3a5f;">David &amp; Brennan<br>'
        '<span style="font-weight:normal;color:#555555;">PlanWell Financial Planning</span></p>\n'
    )

    html_body = _base_html(
        preheader="You're registered for the FERS Workshop on " + webinar_date + ". Here are your details.",
        header_bg="#1e3a5f",
        header_text_color="#ffffff",
        header_line1="You're registered.",
        header_line2=webinar_date + " &nbsp;&middot;&nbsp; 11 AM &ndash; 2 PM " + timezone + " &nbsp;&middot;&nbsp; Zoom",
        body_html=body_html
    )

    return send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# Calendar button helpers (used by 5-day reminder)
# ---------------------------------------------------------------------------

def _calendar_buttons_row(google_url, outlook_url, apple_url):
    """
    Three side-by-side gold-outlined buttons for calendar add.
    Mobile-friendly: stacks naturally because each is its own table cell.
    """
    btn = (
        lambda url, label: (
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0"'
            ' style="margin:6px auto;display:inline-table;">\n'
            '  <tr><td align="center" style="background-color:#c9a55c;border-radius:6px;">\n'
            '    <a href="' + url + '" style="display:inline-block;padding:0 22px;'
            'font-size:14px;font-weight:bold;color:#1e3a5f;text-decoration:none;'
            'font-family:Arial,Helvetica,sans-serif;line-height:44px;min-height:44px;">'
            + label + '</a>\n'
            '  </td></tr>\n'
            '</table>'
        )
    )
    return (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"'
        ' style="margin:18px 0 8px 0;">\n'
        '  <tr><td align="center" style="text-align:center;">\n'
        + btn(google_url, 'Google Calendar') + '&nbsp;\n'
        + btn(outlook_url, 'Outlook') + '&nbsp;\n'
        + btn(apple_url, 'Apple Calendar') + '\n'
        '  </td></tr>\n'
        '</table>'
    )


# ---------------------------------------------------------------------------
# 1b. 5-Day Reminder (Mailchimp send path)
# ---------------------------------------------------------------------------

def send_webinar_5day(to_email, first_name, webinar_date,
                      google_cal_url, outlook_cal_url, apple_cal_url,
                      subject_override=None):
    """
    Send the 5-day pre-webinar email via Mailchimp.
    Routes through mailchimp_client.send_email (NOT SMTP).

    Subject: "Five days until the FERS workshop, {first_name}"
    CTA: three calendar buttons (Google, Outlook, Apple)
    Voice: David & Brennan, no em dashes, no "week" / "7 days" language.
    """
    # Import here to avoid forcing all templates to use Mailchimp
    from mailchimp_client import send_email as mc_send_email

    safe_first = first_name.strip() if first_name else 'there'
    subject = subject_override or ("Five days until the FERS workshop, " + safe_first)

    plain_body = (
        "Hi " + safe_first + ",\n\n"
        "The FERS Retirement Workshop is five days away. " + webinar_date + ".\n\n"
        "A few people have asked what we'll actually cover, so here's the full agenda.\n\n"
        "Friday's agenda:\n"
        "  - The FERS pension formula: 1% or 1.1% x high-3 x years of service. "
        "Why your retirement date can swing the number by thousands.\n"
        "  - TSP withdrawal strategy: which account to draw from first, how RMDs work, "
        "and why the textbook \"safe withdrawal rate\" doesn't fit a federal retirement.\n"
        "  - The FERS Supplement: who gets it, how it's calculated, and the earnings "
        "test that catches people off guard.\n"
        "  - Survivor benefit election: the one-time decision most people get wrong, "
        "and what it actually costs.\n"
        "  - FEHB vs. Medicare Part B: should you keep both, drop one, or coordinate "
        "them in retirement.\n"
        "  - FEGLI: when it makes sense to keep it and when private term insurance is cheaper.\n"
        "  - Social Security timing: how it interacts with your pension and the FERS Supplement.\n\n"
        "David Fei, CFP(r) will lead the session. Brennan Rhule, CFP(r) will be answering "
        "your questions in the chat throughout. Both work exclusively with federal employees. "
        "No insurance products. No annuity sales.\n\n"
        "Add the workshop to your calendar so you don't miss it:\n"
        "  Google:  " + google_cal_url + "\n"
        "  Outlook: " + outlook_cal_url + "\n"
        "  Apple:   " + apple_cal_url + "\n\n"
        "If you can, take five minutes this week to pull up your most recent LES and note "
        "your current base pay and total years of creditable service. It will make the pension "
        "section much more concrete for your situation.\n\n"
        "See you Friday,\n"
        "David & Brennan\n"
        "PlanWell Financial Planning\n"
        "planwellfp.com\n"
    )

    agenda_content = (
        '<p style="margin:0 0 12px 0;font-size:15px;font-weight:bold;color:#1e3a5f;">'
        "Friday's agenda:</p>\n"
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0;">\n'
        '  <tr><td style="padding:6px 8px 6px 0;vertical-align:top;font-size:15px;color:#c9a55c;">&#8226;</td>'
        '<td style="padding:6px 0;font-size:15px;color:#333333;">'
        '<strong>The FERS pension formula.</strong> 1% or 1.1% &times; high-3 &times; years of service. '
        'Why your retirement date can swing the number by thousands.</td></tr>\n'
        '  <tr><td style="padding:6px 8px 6px 0;vertical-align:top;font-size:15px;color:#c9a55c;">&#8226;</td>'
        '<td style="padding:6px 0;font-size:15px;color:#333333;">'
        '<strong>TSP withdrawal strategy.</strong> Which account to draw from first, how RMDs work, '
        'and why the textbook &ldquo;safe withdrawal rate&rdquo; does not fit a federal retirement.</td></tr>\n'
        '  <tr><td style="padding:6px 8px 6px 0;vertical-align:top;font-size:15px;color:#c9a55c;">&#8226;</td>'
        '<td style="padding:6px 0;font-size:15px;color:#333333;">'
        '<strong>The FERS Supplement.</strong> Who gets it, how it is calculated, and the earnings '
        'test that catches people off guard.</td></tr>\n'
        '  <tr><td style="padding:6px 8px 6px 0;vertical-align:top;font-size:15px;color:#c9a55c;">&#8226;</td>'
        '<td style="padding:6px 0;font-size:15px;color:#333333;">'
        '<strong>Survivor benefit election.</strong> The one-time decision most people get wrong, '
        'and what it actually costs.</td></tr>\n'
        '  <tr><td style="padding:6px 8px 6px 0;vertical-align:top;font-size:15px;color:#c9a55c;">&#8226;</td>'
        '<td style="padding:6px 0;font-size:15px;color:#333333;">'
        '<strong>FEHB vs. Medicare Part B.</strong> Should you keep both, drop one, or coordinate '
        'them in retirement.</td></tr>\n'
        '  <tr><td style="padding:6px 8px 6px 0;vertical-align:top;font-size:15px;color:#c9a55c;">&#8226;</td>'
        '<td style="padding:6px 0;font-size:15px;color:#333333;">'
        '<strong>FEGLI.</strong> When it makes sense to keep it and when private term insurance is cheaper.</td></tr>\n'
        '  <tr><td style="padding:6px 8px 6px 0;vertical-align:top;font-size:15px;color:#c9a55c;">&#8226;</td>'
        '<td style="padding:6px 0;font-size:15px;color:#333333;">'
        '<strong>Social Security timing.</strong> How it interacts with your pension and the FERS Supplement.</td></tr>\n'
        '</table>'
    )

    body_html = (
        '<p style="margin:0 0 16px 0;">Hi ' + safe_first + ',</p>\n\n'
        '<p style="margin:0 0 16px 0;">The FERS Retirement Workshop is five days away. '
        '<strong>' + webinar_date + '</strong>.</p>\n\n'
        '<p style="margin:0 0 8px 0;">First things first, lock it into your calendar so '
        'you do not miss it:</p>\n\n' +
        _calendar_buttons_row(google_cal_url, outlook_cal_url, apple_cal_url) + '\n\n'
        '<p style="margin:20px 0 16px 0;">A few people have asked what we will actually cover, '
        'so here is the full agenda for Friday.</p>\n\n' +
        _section_box('#f5f5f5', '#c9a55c', agenda_content) + '\n\n'
        '<p style="margin:20px 0 16px 0;"><strong style="color:#1e3a5f;">David Fei, CFP&#174;</strong> '
        'will lead the session. <strong style="color:#1e3a5f;">Brennan Rhule, CFP&#174;</strong> '
        'will be answering your questions in the chat throughout. Both work exclusively with federal '
        'employees. No insurance products. No annuity sales.</p>\n\n'
        '<p style="margin:20px 0 16px 0;">If you can, take five minutes this week to pull up your '
        'most recent LES and note your current base pay and total years of creditable service. '
        'It will make the pension section much more concrete for your situation.</p>\n\n'
        '<p style="margin:20px 0 8px 0;">See you Friday,</p>\n'
        '<p style="margin:0;font-weight:bold;color:#1e3a5f;">David &amp; Brennan<br>'
        '<span style="font-weight:normal;color:#555555;">PlanWell Financial Planning</span></p>\n'
    )

    html_body = _base_html(
        preheader="Five days from today. Here is exactly what we will cover Friday, plus an easy way to add it to your calendar.",
        header_bg="#1e3a5f",
        header_text_color="#ffffff",
        header_line1="Five days from today.",
        header_line2="FERS Retirement Workshop &nbsp;&middot;&nbsp; " + webinar_date,
        body_html=body_html
    )

    return mc_send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# 1c. 1-Day Reminder (Mailchimp send path)
# ---------------------------------------------------------------------------

def send_webinar_1day_mc(to_email, first_name, webinar_date, zoom_link,
                         timezone='ET', zoom_passcode='', subject_override=None):
    """
    1-day reminder routed through Mailchimp. Single focus: the Zoom link.
    Each registrant gets their own personalized join_url from Zoom.
    """
    from mailchimp_client import send_email as mc_send_email

    safe_first = first_name.strip() if first_name else 'there'
    subject = subject_override or ("Tomorrow at 11 AM, " + safe_first + ": your FERS Workshop link")

    passcode_line = "  Passcode:  " + zoom_passcode + "\n" if zoom_passcode else ""
    plain_body = (
        "Hi " + safe_first + ",\n\n"
        "The FERS Retirement Workshop is tomorrow. Here is everything you need to join.\n\n"
        "  Date:  " + webinar_date + "\n"
        "  Time:  11:00 AM - 2:00 PM " + timezone + "\n"
        "  Link:  " + zoom_link + "\n"
        + passcode_line + "\n"
        "A few practical notes:\n\n"
        "Join 5 minutes early if you can. David starts right at 11, "
        "and the opening context is worth catching.\n\n"
        "You do not need your camera on. Most attendees do not use it.\n\n"
        "Type questions in the chat. Brennan monitors it closely and works through "
        "questions throughout the session.\n\n"
        "Block the full 3 hours. The workshop runs to 2 PM and Q&A is built into "
        "the end, not cut short.\n\n"
        "See you tomorrow,\n"
        "David & Brennan\n"
        "PlanWell Financial Planning\n"
        "planwellfp.com\n\n"
        "---\n"
        "Cannot make it? Reply to this email and we will get you on a future date.\n"
    )

    details_rows = (
        _detail_row("Date:", webinar_date) +
        _detail_row("Time:", "11:00 AM &ndash; 2:00 PM " + timezone)
    )
    if zoom_passcode:
        details_rows += _detail_row("Passcode:", zoom_passcode)

    details_box = (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"'
        ' style="margin:20px 0;background-color:#f5f5f5;border-left:4px solid #c9a55c;">\n'
        '  <tr><td style="padding:18px 20px;">\n'
        '    <table role="presentation" cellpadding="0" cellspacing="0" border="0">\n' +
        details_rows + '\n'
        '    </table>\n'
        '  </td></tr>\n'
        '</table>'
    )

    notes_content = (
        '<p style="margin:0 0 10px 0;font-size:15px;font-weight:bold;color:#1e3a5f;">'
        'A few practical notes:</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;"><strong>Join 5 minutes early.</strong> '
        'David starts right at 11 and the opening context is worth catching.</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;"><strong>Camera is optional.</strong> '
        'Most attendees do not use it.</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;"><strong>Type questions in the chat.</strong> '
        'Brennan monitors it closely and works through questions throughout.</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;"><strong>Block the full 3 hours.</strong> '
        'Q&amp;A is built into the end, not cut short.</p>'
    )

    body_html = (
        '<p style="margin:0 0 16px 0;">Hi ' + safe_first + ',</p>\n\n'
        '<p style="margin:0 0 16px 0;">The FERS Retirement Workshop is tomorrow. '
        'Here is your join link, plus the practical details.</p>\n\n' +
        _gold_button(zoom_link, "Join the Workshop") + '\n\n'
        '<p style="text-align:center;margin:-16px 0 24px 0;font-size:13px;color:#888888;">'
        'Or copy this link: <a href="' + zoom_link + '" style="color:#1e3a5f;word-break:break-all;">'
        + zoom_link + '</a></p>\n\n' +
        details_box + '\n\n' +
        _section_box('#f5f5f5', '#1e3a5f', notes_content) + '\n\n'
        '<p style="margin:20px 0 8px 0;">See you tomorrow,</p>\n'
        '<p style="margin:0;font-weight:bold;color:#1e3a5f;">David &amp; Brennan<br>'
        '<span style="font-weight:normal;color:#555555;">PlanWell Financial Planning</span></p>\n\n'
        '<p style="margin:24px 0 0 0;font-size:13px;color:#888888;">Cannot make it? Reply to '
        'this email and we will get you on a future date.</p>\n'
    )

    html_body = _base_html(
        preheader="Your Zoom link for tomorrow's FERS Workshop is inside. Starts 11 AM " + timezone + ".",
        header_bg="#1e3a5f",
        header_text_color="#ffffff",
        header_line1="Tomorrow at 11 AM.",
        header_line2="Your Zoom link is below.",
        body_html=body_html
    )

    return mc_send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# 1d. Day-Of Reminder (Mailchimp send path)
# ---------------------------------------------------------------------------

def send_webinar_dayof_mc(to_email, first_name, zoom_link,
                          timezone='ET', zoom_passcode='', subject_override=None):
    """
    Day-of reminder routed through Mailchimp. One job: get them to click the link.
    """
    from mailchimp_client import send_email as mc_send_email

    safe_first = first_name.strip() if first_name else 'there'
    subject = subject_override or ("Starting at 11 AM today, " + safe_first + ": join the FERS Workshop")

    passcode_line = "\nPasscode: " + zoom_passcode + "\n" if zoom_passcode else ""
    plain_body = (
        "Hi " + safe_first + ",\n\n"
        "The FERS Retirement Workshop starts at 11:00 AM " + timezone + " today. "
        "David will start right on time.\n\n"
        "Join here: " + zoom_link + "\n" + passcode_line + "\n"
        "See you in a few hours,\n"
        "David & Brennan\n"
        "PlanWell Financial Planning\n"
        "planwellfp.com\n\n"
        "---\n"
        "Having trouble with the link? Reply to this email and we will get it resolved.\n"
    )

    passcode_html = (
        '<p style="text-align:center;margin:0 0 24px 0;font-size:14px;color:#888888;">'
        'Passcode: <strong style="color:#333333;">' + zoom_passcode + '</strong></p>\n\n'
    ) if zoom_passcode else ''

    body_html = (
        '<p style="margin:0 0 16px 0;">Hi ' + safe_first + ',</p>\n\n'
        '<p style="margin:0 0 20px 0;font-size:17px;">The FERS Retirement Workshop starts at '
        '<strong>11:00 AM ' + timezone + '</strong> today. '
        'David will start right on time.</p>\n\n' +
        _gold_button(zoom_link, "Join the Workshop Now") + '\n\n'
        '<p style="text-align:center;margin:-16px 0 8px 0;font-size:13px;color:#888888;">'
        '<a href="' + zoom_link + '" style="color:#1e3a5f;word-break:break-all;">'
        + zoom_link + '</a></p>\n' +
        passcode_html +
        '<p style="margin:20px 0 8px 0;">See you in a few hours,</p>\n'
        '<p style="margin:0;font-weight:bold;color:#1e3a5f;">David &amp; Brennan<br>'
        '<span style="font-weight:normal;color:#555555;">PlanWell Financial Planning</span></p>\n\n'
        '<p style="margin:24px 0 0 0;font-size:14px;color:#888888;">Having trouble with the link? '
        'Reply to this email and we will get it resolved.</p>\n'
    )

    html_body = _base_html(
        preheader="The FERS Workshop starts at 11 AM " + timezone + " today. Your link is inside.",
        header_bg="#c9a55c",
        header_text_color="#1e3a5f",
        header_line1="Starting at 11 AM today.",
        header_line2="FERS Retirement Workshop",
        body_html=body_html
    )

    return mc_send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# 2. 7-Day Reminder
# ---------------------------------------------------------------------------

def send_webinar_7day(to_email, first_name, webinar_date):
    """
    Send 7-day reminder.
    Purpose: Build anticipation, explain what makes this different,
    introduce Brennan and David by name.
    """
    subject = "One week out: what to expect at the FERS Workshop"

    plain_body = (
        "Hi " + first_name + ",\n\n"
        "Your FERS Retirement Workshop is one week from today (" + webinar_date + ").\n\n"
        "Here is what to expect.\n\n"
        "David Fei, CFP(r) will lead the full 3-hour session, with Brennan Rhule, CFP(r) "
        "answering questions in the chat throughout. Both work exclusively with federal "
        "employees. No insurance products. No annuity sales. The entire workshop is built "
        "around one question: what do you need to know to retire well under FERS?\n\n"
        "David will walk through the FERS pension formula (1% or 1.1% x high-3 average "
        "salary x years of creditable service) and show you how small differences in your "
        "retirement date can change the math significantly.\n\n"
        "He will also cover TSP: which accounts to draw from first, how to handle RMDs, and "
        "why the \"safe withdrawal rate\" most advisors cite does not map cleanly onto a federal "
        "retirement with a pension and FERS Supplement.\n\n"
        "The workshop also addresses the decisions many federal employees delay too long: "
        "survivor benefit election, FEGLI, FEHB vs. Medicare Part B, and Social Security timing.\n\n"
        "One thing to do this week: locate your most recent LES and note your current base pay "
        "and total years of creditable service. It will make the pension section much more "
        "concrete for your situation.\n\n"
        "See you on " + webinar_date + ",\n"
        "David & Brennan\n"
        "PlanWell Financial Planning\n"
        "planwellfp.com\n"
    )

    what_box_content = (
        '<p style="margin:0 0 10px 0;font-size:15px;font-weight:bold;">'
        'What this workshop covers:</p>\n'
        '<p style="margin:0;font-size:15px;color:#333333;">A 3-hour session led by David Fei, CFP&#174;, '
        'with Brennan Rhule, CFP&#174; answering your questions in the chat. Both work exclusively '
        'with federal employees. No insurance products. No sales pitch. The entire workshop is '
        'built around one question: what do you need to know to retire well under FERS?</p>'
    )

    prep_box_content = (
        '<p style="margin:0 0 8px 0;font-size:15px;font-weight:bold;">'
        'One thing to do this week:</p>\n'
        '<p style="margin:0;font-size:15px;color:#333333;">Locate your most recent LES and note '
        'your current base pay and total years of creditable service. It will make the pension '
        'calculation section much more concrete for your situation.</p>'
    )

    body_html = (
        '<p style="margin:0 0 16px 0;">Hi ' + first_name + ',</p>\n\n'
        '<p style="margin:0 0 16px 0;">Your FERS Retirement Workshop is one week from today: '
        '<strong>' + webinar_date + '</strong>.</p>\n\n'
        '<p style="margin:0 0 16px 0;">Here is what to expect.</p>\n\n' +
        _section_box('#f5f5f5', '#c9a55c', what_box_content) + '\n\n'
        '<p style="margin:20px 0 16px 0;"><strong>What that looks like in practice:</strong></p>\n\n'
        '<p style="margin:0 0 16px 0;"><strong style="color:#1e3a5f;">David</strong> will walk '
        'through the FERS pension formula (1% or 1.1% &times; high-3 average salary '
        '&times; years of creditable service) and show you how small differences in your '
        'retirement date can change the math significantly.</p>\n\n'
        '<p style="margin:0 0 16px 0;">He will also cover '
        'TSP: which accounts to draw from first, how to handle RMDs, and why the &ldquo;safe '
        'withdrawal rate&rdquo; most advisors cite does not map cleanly onto a federal retirement '
        'with a pension and FERS Supplement.</p>\n\n'
        '<p style="margin:0 0 16px 0;">The workshop also addresses the decisions many federal '
        'employees delay too long: survivor benefit election, FEGLI, FEHB vs. Medicare Part B, '
        'and Social Security timing. <strong style="color:#1e3a5f;">Brennan</strong> monitors '
        'the chat throughout, so type your questions as they come up.</p>\n\n' +
        _section_box('#fff8ec', '#c9a55c', prep_box_content) + '\n\n'
        '<p style="margin:20px 0 8px 0;">See you on ' + webinar_date + ',</p>\n'
        '<p style="margin:0;font-weight:bold;color:#1e3a5f;">David &amp; Brennan<br>'
        '<span style="font-weight:normal;color:#555555;">PlanWell Financial Planning</span></p>\n'
    )

    html_body = _base_html(
        preheader="One week until the FERS Workshop. Here's exactly what Brennan and David will cover.",
        header_bg="#1e3a5f",
        header_text_color="#ffffff",
        header_line1="One week to go.",
        header_line2="FERS Retirement Workshop &nbsp;&middot;&nbsp; " + webinar_date,
        body_html=body_html
    )

    return send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# 3. 3-Day Reminder
# ---------------------------------------------------------------------------

def send_webinar_3day(to_email, first_name, webinar_date, timezone='ET'):
    """
    Send 3-day reminder.
    Purpose: Prep checklist, surface the questions they likely have,
    make the workshop feel immediately useful before it starts.
    """
    subject = "3 days out: quick prep for the FERS Workshop"

    plain_body = (
        "Hi " + first_name + ",\n\n"
        "Three days until the FERS Workshop (" + webinar_date + ", 11 AM - 2 PM " + timezone + ").\n\n"
        "Before the workshop, it helps to have a few things in front of you:\n\n"
        "  [] Your most recent LES (base pay and creditable service years)\n"
        "  [] Your TSP balance and current contribution rate\n"
        "  [] The specific questions you want answered\n\n"
        "Questions we hear most often:\n\n"
        '  "When can I retire with an unreduced annuity?"\n'
        '  "What is my FERS Supplement, and when does it end?"\n'
        '  "Should I elect the full survivor benefit, partial, or none?"\n'
        '  "When does it make sense to add Medicare Part B on top of FEHB?"\n'
        '  "How do I calculate my high-3 if my pay has changed significantly?"\n'
        '  "What order should I draw from my TSP vs. other accounts?"\n\n'
        "You do not need to have all the answers before the workshop. That is the point. "
        "But knowing what you want to walk away with makes the time more useful.\n\n"
        "Your Zoom link arrives tomorrow morning.\n\n"
        "See you on " + webinar_date + ",\n"
        "David & Brennan\n"
        "PlanWell Financial Planning\n"
        "planwellfp.com\n"
    )

    prep_content = (
        '<p style="margin:0 0 10px 0;font-size:15px;font-weight:bold;color:#1e3a5f;">'
        'Quick prep checklist:</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;">&#9744; Your most recent LES '
        '(base pay and years of creditable service)</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;">&#9744; Your TSP balance and '
        'current contribution rate</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;">&#9744; The specific questions '
        'you want answered</p>'
    )

    questions_content = (
        '<p style="margin:0 0 10px 0;font-size:15px;font-weight:bold;color:#1e3a5f;">'
        'Questions we hear most often:</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;">'
        '&ldquo;When can I retire with an unreduced annuity?&rdquo;</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;">'
        '&ldquo;What is my FERS Supplement, and when does it end?&rdquo;</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;">'
        '&ldquo;Should I elect the full survivor benefit, partial, or none?&rdquo;</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;">'
        '&ldquo;When does it make sense to add Medicare Part B on top of FEHB?&rdquo;</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;">'
        '&ldquo;How do I calculate my high-3 if my pay has changed significantly?&rdquo;</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;">'
        '&ldquo;What order should I draw from my TSP vs. other accounts?&rdquo;</p>'
    )

    body_html = (
        '<p style="margin:0 0 16px 0;">Hi ' + first_name + ',</p>\n\n'
        '<p style="margin:0 0 16px 0;">Three days until the FERS Workshop: '
        '<strong>' + webinar_date + '</strong>, 11 AM &ndash; 2 PM ' + timezone + '.</p>\n\n' +
        _section_box('#f5f5f5', '#c9a55c', prep_content) + '\n\n' +
        _section_box('#f9f6f0', '#c9a55c', questions_content) + '\n\n'
        '<p style="margin:20px 0 16px 0;">You do not need all the answers before the '
        'workshop. That is the point. But knowing what you want to walk away with makes the '
        'time more useful.</p>\n\n' +
        _navy_note("Your Zoom link arrives tomorrow morning.") + '\n\n'
        '<p style="margin:20px 0 8px 0;">See you on ' + webinar_date + ',</p>\n'
        '<p style="margin:0;font-weight:bold;color:#1e3a5f;">David &amp; Brennan<br>'
        '<span style="font-weight:normal;color:#555555;">PlanWell Financial Planning</span></p>\n'
    )

    html_body = _base_html(
        preheader="3 days until the FERS Workshop. Quick prep checklist inside. Takes 5 minutes.",
        header_bg="#1e3a5f",
        header_text_color="#ffffff",
        header_line1="3 days to go.",
        header_line2=webinar_date + " &nbsp;&middot;&nbsp; 11 AM &ndash; 2 PM " + timezone,
        body_html=body_html
    )

    return send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# 4. 1-Day Reminder (with Zoom link)
# ---------------------------------------------------------------------------

def send_webinar_1day(to_email, first_name, webinar_date, zoom_link, timezone='ET', zoom_passcode=''):
    """
    Send 1-day reminder with Zoom link.
    Purpose: Remove all friction for joining. Single focus: here's the link,
    here's what you need to know to show up ready.
    """
    subject = "Tomorrow at 11 AM: your Zoom link for the FERS Workshop"

    passcode_line = "  Passcode:  " + zoom_passcode + "\n" if zoom_passcode else ""
    plain_body = (
        "Hi " + first_name + ",\n\n"
        "The workshop is tomorrow. Here is everything you need:\n\n"
        "  Date:  " + webinar_date + "\n"
        "  Time:  11:00 AM - 2:00 PM " + timezone + "\n"
        "  Link:  " + zoom_link + "\n"
        + passcode_line + "\n"
        "A few practical notes:\n\n"
        "Join 5 minutes early if you can. David starts right at 11, "
        "and the opening context is worth catching.\n\n"
        "You do not need your camera on. Most attendees do not use it.\n\n"
        "Type questions in the chat. Brennan monitors it closely and works through "
        "questions throughout the session.\n\n"
        "Block the full 3 hours. The workshop runs to 2 PM and Q&A is built into "
        "the end, not cut short.\n\n"
        "See you tomorrow,\n"
        "David & Brennan\n"
        "PlanWell Financial Planning\n"
        "planwellfp.com\n\n"
        "---\n"
        "Cannot make it? Reply to this email and we will get you on a future date.\n"
    )

    details_rows = (
        _detail_row("Date:", webinar_date) +
        _detail_row("Time:", "11:00 AM &ndash; 2:00 PM " + timezone)
    )
    if zoom_passcode:
        details_rows += _detail_row("Passcode:", zoom_passcode)

    details_box = (
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"'
        ' style="margin:20px 0;background-color:#f5f5f5;border-left:4px solid #c9a55c;">\n'
        '  <tr><td style="padding:18px 20px;">\n'
        '    <table role="presentation" cellpadding="0" cellspacing="0" border="0">\n' +
        details_rows + '\n'
        '    </table>\n'
        '  </td></tr>\n'
        '</table>'
    )

    notes_content = (
        '<p style="margin:0 0 10px 0;font-size:15px;font-weight:bold;color:#1e3a5f;">'
        'A few practical notes:</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;"><strong>Join 5 minutes early.</strong> '
        'David starts right at 11 and the opening context is worth catching.</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;"><strong>Camera is optional.</strong> '
        'Most attendees do not use it.</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;"><strong>Type questions in the chat.</strong> '
        'Brennan monitors it closely and works through questions throughout.</p>\n'
        '<p style="margin:6px 0;font-size:15px;color:#333333;"><strong>Block the full 3 hours.</strong> '
        'Q&amp;A is built into the end, not cut short.</p>'
    )

    body_html = (
        '<p style="margin:0 0 16px 0;">Hi ' + first_name + ',</p>\n\n'
        "<p style=\"margin:0 0 16px 0;\">The workshop is tomorrow. Here is everything you need:</p>\n\n" +
        details_box + '\n\n' +
        _gold_button(zoom_link, "Join the Workshop") + '\n\n'
        '<p style="text-align:center;margin:-16px 0 24px 0;font-size:13px;color:#888888;">'
        'Or copy this link: <a href="' + zoom_link + '" style="color:#1e3a5f;word-break:break-all;">'
        + zoom_link + '</a></p>\n\n' +
        _section_box('#f5f5f5', '#1e3a5f', notes_content) + '\n\n'
        '<p style="margin:20px 0 8px 0;">See you tomorrow,</p>\n'
        '<p style="margin:0;font-weight:bold;color:#1e3a5f;">David &amp; Brennan<br>'
        '<span style="font-weight:normal;color:#555555;">PlanWell Financial Planning</span></p>\n\n'
        '<p style="margin:24px 0 0 0;font-size:13px;color:#888888;">Cannot make it? Reply to '
        'this email and we will get you on a future date.</p>\n'
    )

    html_body = _base_html(
        preheader="Your Zoom link for tomorrow's FERS Workshop is inside. Starts 11 AM " + timezone + ".",
        header_bg="#1e3a5f",
        header_text_color="#ffffff",
        header_line1="Tomorrow at 11 AM.",
        header_line2="Your Zoom link is below.",
        body_html=body_html
    )

    return send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# 5. Day-Of Reminder
# ---------------------------------------------------------------------------

def send_webinar_dayof(to_email, first_name, zoom_link, timezone='ET', zoom_passcode=''):
    """
    Send morning-of reminder.
    Purpose: One job — get them to click the link. Short, direct, high urgency.
    """
    subject = "Starting at 11 AM today: join the FERS Workshop"

    passcode_line = "\nPasscode: " + zoom_passcode + "\n" if zoom_passcode else ""
    plain_body = (
        "Hi " + first_name + ",\n\n"
        "The FERS Retirement Workshop starts at 11:00 AM " + timezone + " today. "
        "David will start right on time.\n\n"
        "Join here: " + zoom_link + "\n" + passcode_line + "\n"
        "See you in a few hours,\n"
        "The PlanWell Team\n"
        "planwellfp.com\n\n"
        "---\n"
        "Having trouble with the link? Reply to this email and we will get it resolved.\n"
    )

    passcode_html = (
        '<p style="text-align:center;margin:0 0 24px 0;font-size:14px;color:#888888;">'
        'Passcode: <strong style="color:#333333;">' + zoom_passcode + '</strong></p>\n\n'
    ) if zoom_passcode else ''

    body_html = (
        '<p style="margin:0 0 16px 0;">Hi ' + first_name + ',</p>\n\n'
        '<p style="margin:0 0 20px 0;font-size:17px;">The FERS Retirement Workshop starts at '
        '<strong>11:00 AM ' + timezone + '</strong> today. '
        'David will start right on time.</p>\n\n' +
        _gold_button(zoom_link, "Join the Workshop Now") + '\n\n'
        '<p style="text-align:center;margin:-16px 0 8px 0;font-size:13px;color:#888888;">'
        '<a href="' + zoom_link + '" style="color:#1e3a5f;word-break:break-all;">'
        + zoom_link + '</a></p>\n' +
        passcode_html +
        '<p style="margin:20px 0 0 0;font-size:14px;color:#888888;">Having trouble with the link? '
        'Reply to this email and we will get it resolved.</p>\n'
    )

    html_body = _base_html(
        preheader="The FERS Workshop starts at 11 AM " + timezone + " today. Your link is inside.",
        header_bg="#c9a55c",
        header_text_color="#1e3a5f",
        header_line1="Starting at 11 AM today.",
        header_line2="FERS Retirement Workshop",
        body_html=body_html
    )

    return send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# Test block
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print("Testing FERS webinar email templates...\n")

    send_webinar_confirmation(
        to_email="test@example.com",
        first_name="Sarah",
        webinar_date="Tuesday, April 8",
        timezone="ET",
        calendar_link="https://calendar.google.com/calendar/render?action=TEMPLATE&text=FERS+Retirement+Workshop&dates=20260410T150000Z/20260410T180000Z&details=Free+3-hour+FERS+workshop+with+David+Fei+and+Brennan+Rhule&location=Online+via+Zoom"
    )
    print("Confirmation template OK")

    send_webinar_7day(
        to_email="test@example.com",
        first_name="Sarah",
        webinar_date="Tuesday, April 8"
    )
    print("7-day template OK")

    send_webinar_3day(
        to_email="test@example.com",
        first_name="Sarah",
        webinar_date="Tuesday, April 8",
        timezone="ET"
    )
    print("3-day template OK")

    send_webinar_1day(
        to_email="test@example.com",
        first_name="Sarah",
        webinar_date="Tuesday, April 8",
        zoom_link="https://zoom.us/j/123456789",
        timezone="ET"
    )
    print("1-day template OK")

    send_webinar_dayof(
        to_email="test@example.com",
        first_name="Sarah",
        zoom_link="https://zoom.us/j/123456789",
        timezone="ET"
    )
    print("Day-of template OK")

    print("\nAll 5 templates ready.")
