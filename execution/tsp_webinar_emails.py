"""
TSP Webinar Email Templates
============================
Pre-formatted HTML email templates for the TSP Investment Strategies
webinar nurture sequence.

Duration: 1 hour (12:00 PM - 1:00 PM ET)
Host: David Fei, CFP®, ChFEBC℠, AIF®
Topics: Fund allocation, Roth vs Traditional, withdrawal strategies,
        L-Fund analysis, tax optimization

Usage:
    from tsp_webinar_emails import send_tsp_confirmation, send_tsp_7day, ...
"""

from email_sender import send_email


# ---------------------------------------------------------------------------
# Shared HTML building blocks (inline CSS, table layout, no style blocks)
# ---------------------------------------------------------------------------

_PREHEADER = '<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;color:#f5f5f5;line-height:1px;">{text}&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;</div>'

_FOOTER = """
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;">
  <tr>
    <td align="center" style="padding:20px 30px;font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#888888;line-height:1.5;">
      PlanWell Financial Planning &bull; <a href="https://planwellfp.com" style="color:#888888;text-decoration:underline;">planwellfp.com</a><br>
      David Fei, CFP&reg;, ChFEBC&#8480;, AIF&reg;<br>
      <span style="font-size:11px;">You registered for the TSP Investment Strategies Workshop. Questions? Reply to this email.</span>
    </td>
  </tr>
</table>
"""

def _wrap_email(preheader_text: str, header_html: str, body_html: str) -> str:
    """Wrap content in a mobile-first, Outlook-safe table shell."""
    preheader = _PREHEADER.format(text=preheader_text)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>TSP Investment Strategies Workshop</title>
</head>
<body style="margin:0;padding:0;background-color:#f5f5f5;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;">
{preheader}
<!--[if mso]><table width="600" align="center" cellpadding="0" cellspacing="0" border="0"><tr><td><![endif]-->
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;">
  <tr>
    <td align="center" style="padding:20px 10px;">
      <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#ffffff;">
        {header_html}
        {body_html}
      </table>
    </td>
  </tr>
</table>
{_FOOTER}
<!--[if mso]></td></tr></table><![endif]-->
</body>
</html>"""


def _navy_header(headline: str, subline: str = '') -> str:
    sub = f'<p style="margin:8px 0 0;font-size:15px;color:#c9a55c;font-family:Arial,Helvetica,sans-serif;">{subline}</p>' if subline else ''
    return f"""
<tr>
  <td style="background-color:#1e3a5f;padding:32px 30px;text-align:center;">
    <h1 style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:26px;font-weight:bold;color:#ffffff;line-height:1.2;">{headline}</h1>
    {sub}
  </td>
</tr>"""


def _gold_button(url: str, label: str) -> str:
    return f"""
<table cellpadding="0" cellspacing="0" border="0" style="margin:24px auto;">
  <tr>
    <td align="center" style="background-color:#c9a55c;border-radius:4px;">
      <a href="{url}" style="display:inline-block;min-height:44px;padding:14px 32px;font-family:Arial,Helvetica,sans-serif;font-size:16px;font-weight:bold;color:#1e3a5f;text-decoration:none;line-height:1.2;">{label}</a>
    </td>
  </tr>
</table>"""


def _detail_row(label: str, value: str) -> str:
    return f"""
<tr>
  <td style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#555555;width:110px;vertical-align:top;"><strong style="color:#1e3a5f;">{label}</strong></td>
  <td style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;vertical-align:top;">{value}</td>
</tr>"""


# ---------------------------------------------------------------------------
# 1. Confirmation
# ---------------------------------------------------------------------------

def send_tsp_confirmation(to_email: str, first_name: str, webinar_date: str,
                           timezone: str = 'ET', calendar_link: str = '') -> bool:
    """
    Send confirmation email immediately after TSP workshop registration.
    """
    subject = f"You're registered — TSP Workshop on {webinar_date}"

    plain_body = f"""Hi {first_name},

You're registered for the TSP Investment Strategies Workshop.

Date: {webinar_date}
Time: 12:00 PM – 1:00 PM {timezone}
Format: Online via Zoom (free)
Host: David Fei, CFP®, ChFEBC℠, AIF®

What you'll walk away with:

- A clear picture of what's inside the C, S, I, F, and G Funds — not just the names
- A framework for deciding between Traditional and Roth TSP contributions based on your marginal rate now vs. retirement
- How to read your allocation and spot whether it actually matches your timeline
- The real story on L-Funds — when they work and when they leave money on the table
- Which TSP withdrawal method minimizes your tax bill in retirement

One thing to do before the workshop: log into tsp.gov and check your current fund allocation. You'll get a lot more out of the session if you know your own numbers going in.

Your Zoom link will arrive the day before.

Questions? Just reply here.

— David Fei & the PlanWell Team
planwellfp.com
"""

    cal_btn = _gold_button(calendar_link, 'Add to Calendar') if calendar_link else ''

    header = _navy_header("You're Registered", "TSP Investment Strategies Workshop")
    body = f"""
<tr>
  <td style="padding:32px 30px 24px;background-color:#ffffff;">
    <p style="margin:0 0 16px;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;line-height:1.5;">Hi {first_name},</p>
    <p style="margin:0 0 20px;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;line-height:1.5;">You're confirmed for the <strong>TSP Investment Strategies Workshop</strong> with David Fei, CFP&reg;. Block off your lunch hour &mdash; this is one hour of focused, no-fluff TSP strategy.</p>

    <!-- Event details box -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;border-left:4px solid #c9a55c;margin-bottom:24px;">
      <tr><td style="padding:20px 20px 12px;">
        <table cellpadding="0" cellspacing="0" border="0" width="100%">
          {_detail_row('Date:', webinar_date)}
          {_detail_row('Time:', f'12:00 PM &ndash; 1:00 PM {timezone}')}
          {_detail_row('Format:', 'Online via Zoom &mdash; free')}
          {_detail_row('Host:', 'David Fei, CFP&reg;, ChFEBC&#8480;, AIF&reg;')}
        </table>
      </td></tr>
    </table>

    {cal_btn}

    <p style="margin:0 0 12px;font-family:Arial,Helvetica,sans-serif;font-size:16px;font-weight:bold;color:#1e3a5f;">What you'll walk away with:</p>
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:24px;">
      <tr><td style="padding:6px 0 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;border-bottom:1px solid #eeeeee;">A clear picture of what's inside the C, S, I, F, and G Funds &mdash; not just the names</td></tr>
      <tr><td style="padding:6px 0 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;border-bottom:1px solid #eeeeee;">A framework for deciding between Traditional and Roth TSP based on your marginal rate now vs. retirement</td></tr>
      <tr><td style="padding:6px 0 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;border-bottom:1px solid #eeeeee;">How to read your allocation and spot whether it actually matches your timeline</td></tr>
      <tr><td style="padding:6px 0 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;border-bottom:1px solid #eeeeee;">The real story on L-Funds &mdash; when they work and when they leave money on the table</td></tr>
      <tr><td style="padding:6px 0 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;">Which TSP withdrawal method minimizes your tax bill in retirement</td></tr>
    </table>

    <!-- Prep tip -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;border-radius:4px;margin-bottom:24px;">
      <tr><td style="padding:16px 20px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;">
        <strong style="color:#1e3a5f;">Before the workshop:</strong> Log into <strong>tsp.gov</strong> and check your current fund allocation. You'll get a lot more out of the session if you know your own numbers going in.
      </td></tr>
    </table>

    <p style="margin:0 0 8px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#555555;">Your Zoom link arrives the day before. Questions? Reply here.</p>
    <p style="margin:24px 0 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;">See you then,<br><strong>David Fei &amp; the PlanWell Team</strong></p>
  </td>
</tr>"""

    html_body = _wrap_email(
        f"You're registered for the TSP Workshop on {webinar_date}. Zoom link arrives the day before.",
        header, body
    )

    return send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# 2. 7-Day Reminder
# ---------------------------------------------------------------------------

def send_tsp_7day(to_email: str, first_name: str, webinar_date: str) -> bool:
    """
    Send 7-day reminder — TSP insight teaser, prep action.
    """
    subject = f"TSP Workshop in 1 week — one thing to do before {webinar_date}"

    plain_body = f"""Hi {first_name},

Your TSP Investment Strategies Workshop is one week from now — {webinar_date} at 12:00 PM ET.

Here's something worth thinking about before we meet:

Most federal employees who are in an L-Fund don't know how the fund actually invests — or whether the target date matches when they actually plan to retire. David will break down the L-Fund mechanics and show you how to check whether yours is set correctly for your situation.

What else David will cover in the hour:

- C Fund vs. S Fund vs. I Fund — the actual indexes they track and how their long-term returns differ
- The tax math behind Traditional vs. Roth TSP — when Roth makes sense and when it doesn't
- Allocation adjustments as you approach retirement (the "G Fund trap" and how to avoid it)
- TSP withdrawal options: monthly payments, annuities, or lump sum — what changes with each

One action before the workshop: Log into tsp.gov and write down your current allocation percentages. Even just knowing whether you're 100% in one fund or spread across several gives David something to work with during Q&A.

See you on {webinar_date},
David Fei & the PlanWell Team
planwellfp.com
"""

    header = _navy_header("One Week Away", f"TSP Workshop &mdash; {webinar_date}")
    body = f"""
<tr>
  <td style="padding:32px 30px 24px;background-color:#ffffff;">
    <p style="margin:0 0 16px;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;line-height:1.5;">Hi {first_name},</p>
    <p style="margin:0 0 24px;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;line-height:1.5;">Your TSP workshop is <strong>one week away</strong> &mdash; {webinar_date} at 12:00 PM ET. Here's a preview of what we'll cover.</p>

    <!-- Insight callout -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#1e3a5f;border-radius:4px;margin-bottom:24px;">
      <tr><td style="padding:20px 24px;">
        <p style="margin:0 0 8px;font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:bold;color:#c9a55c;text-transform:uppercase;letter-spacing:1px;">Worth knowing before you arrive</p>
        <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#ffffff;line-height:1.6;">Most federal employees in an L-Fund don't know how it actually invests &mdash; or whether the target date matches when they plan to retire. David will walk through the mechanics and show you how to check yours.</p>
      </td></tr>
    </table>

    <p style="margin:0 0 12px;font-family:Arial,Helvetica,sans-serif;font-size:16px;font-weight:bold;color:#1e3a5f;">The full hour agenda:</p>
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:24px;">
      <tr>
        <td style="padding:10px 0;border-bottom:1px solid #eeeeee;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;" valign="top">
          <strong style="color:#c9a55c;display:inline-block;width:24px;">C/S/I</strong> The actual indexes these funds track and how their long-term returns differ
        </td>
      </tr>
      <tr>
        <td style="padding:10px 0;border-bottom:1px solid #eeeeee;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;" valign="top">
          <strong style="color:#c9a55c;display:inline-block;width:24px;">F/G</strong> Why the G Fund feels safe but can cost you over a 20-year retirement
        </td>
      </tr>
      <tr>
        <td style="padding:10px 0;border-bottom:1px solid #eeeeee;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;" valign="top">
          <strong style="color:#c9a55c;display:inline-block;width:24px;">Tax</strong> The math behind Traditional vs. Roth TSP &mdash; when each makes sense
        </td>
      </tr>
      <tr>
        <td style="padding:10px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;" valign="top">
          <strong style="color:#c9a55c;display:inline-block;width:36px;">Withdraw</strong> Monthly payments, annuity, or lump sum &mdash; what changes with each option
        </td>
      </tr>
    </table>

    <!-- Prep action -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;border-radius:4px;margin-bottom:24px;">
      <tr><td style="padding:16px 20px;">
        <p style="margin:0 0 6px;font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:bold;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.5px;">One action this week</p>
        <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;">Log into <strong>tsp.gov</strong> and write down your current allocation percentages. Knowing your numbers makes the Q&amp;A session much more useful.</p>
      </td></tr>
    </table>

    <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;">See you on {webinar_date},<br><strong>David Fei &amp; the PlanWell Team</strong></p>
  </td>
</tr>"""

    html_body = _wrap_email(
        f"One week until your TSP Workshop. One action to do before you arrive.",
        header, body
    )

    return send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# 3. 3-Day Reminder
# ---------------------------------------------------------------------------

def send_tsp_3day(to_email: str, first_name: str, webinar_date: str,
                   timezone: str = 'ET') -> bool:
    """
    Send 3-day reminder — prep checklist and Q&A preview.
    """
    subject = f"3 days until your TSP Workshop — quick prep checklist"

    plain_body = f"""Hi {first_name},

The TSP Investment Strategies Workshop is in 3 days — {webinar_date} at 12:00 PM {timezone}.

Two-minute prep checklist:

[ ] Log into tsp.gov — check your current C/S/I/F/G allocation percentages
[ ] Note whether you're in an L-Fund or a custom mix
[ ] Check your Traditional vs Roth TSP balance split
[ ] Write down one specific TSP question you want answered

Questions David hears all the time (that he'll answer directly):

"Should I move everything into the G Fund before retirement?"
The short answer: it depends on your timeline and whether you have other income sources. David will walk through the math.

"Is it too late to switch to Roth TSP contributions?"
Probably not — and the answer depends on where your marginal rate is headed, not your age.

"How do I pick the right C/S/I mix?"
There's a straightforward framework. David will share it.

Your Zoom link arrives tomorrow.

See you Thursday,
David Fei & the PlanWell Team
planwellfp.com
"""

    header = _navy_header("3 Days Out", f"TSP Workshop &mdash; {webinar_date} at 12:00 PM {timezone}")
    body = f"""
<tr>
  <td style="padding:32px 30px 24px;background-color:#ffffff;">
    <p style="margin:0 0 16px;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;line-height:1.5;">Hi {first_name},</p>
    <p style="margin:0 0 24px;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;line-height:1.5;">Three days out. Here's a quick checklist to get the most out of the hour.</p>

    <!-- Checklist -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;border-radius:4px;margin-bottom:24px;">
      <tr><td style="padding:20px 24px;">
        <p style="margin:0 0 14px;font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:bold;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.5px;">Two-minute prep checklist</p>
        <table width="100%" cellpadding="0" cellspacing="0" border="0">
          <tr><td style="padding:7px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.4;border-bottom:1px solid #e0e0e0;">&#9744;&nbsp;&nbsp;Log into <strong>tsp.gov</strong> — write down your C/S/I/F/G allocation percentages</td></tr>
          <tr><td style="padding:7px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.4;border-bottom:1px solid #e0e0e0;">&#9744;&nbsp;&nbsp;Note whether you're in an L-Fund or a custom mix</td></tr>
          <tr><td style="padding:7px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.4;border-bottom:1px solid #e0e0e0;">&#9744;&nbsp;&nbsp;Check your Traditional vs. Roth TSP balance split</td></tr>
          <tr><td style="padding:7px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.4;">&#9744;&nbsp;&nbsp;Write down one specific TSP question you want answered</td></tr>
        </table>
      </td></tr>
    </table>

    <p style="margin:0 0 16px;font-family:Arial,Helvetica,sans-serif;font-size:16px;font-weight:bold;color:#1e3a5f;">Questions David gets all the time (he'll answer them directly):</p>

    <!-- Q&A items -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:24px;">
      <tr>
        <td style="padding:14px 0;border-bottom:1px solid #eeeeee;">
          <p style="margin:0 0 6px;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#333333;line-height:1.4;">"Should I move everything into the G Fund before retirement?"</p>
          <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#666666;line-height:1.5;">Depends on your timeline and whether you have other income. David will walk through the math.</p>
        </td>
      </tr>
      <tr>
        <td style="padding:14px 0;border-bottom:1px solid #eeeeee;">
          <p style="margin:0 0 6px;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#333333;line-height:1.4;">"Is it too late to switch to Roth TSP contributions?"</p>
          <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#666666;line-height:1.5;">Probably not &mdash; and the answer depends on where your marginal rate is headed, not your age.</p>
        </td>
      </tr>
      <tr>
        <td style="padding:14px 0;">
          <p style="margin:0 0 6px;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#333333;line-height:1.4;">"How do I pick the right C/S/I mix?"</p>
          <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#666666;line-height:1.5;">There's a straightforward framework. David will share it.</p>
        </td>
      </tr>
    </table>

    <!-- Zoom link notice -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#1e3a5f;border-radius:4px;margin-bottom:24px;">
      <tr><td style="padding:16px 20px;text-align:center;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#ffffff;line-height:1.5;">
        Your Zoom link arrives tomorrow.
      </td></tr>
    </table>

    <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;">See you soon,<br><strong>David Fei &amp; the PlanWell Team</strong></p>
  </td>
</tr>"""

    html_body = _wrap_email(
        f"TSP Workshop in 3 days. Quick checklist inside — takes 2 minutes.",
        header, body
    )

    return send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# 4. 1-Day Reminder
# ---------------------------------------------------------------------------

def send_tsp_1day(to_email: str, first_name: str, webinar_date: str,
                   zoom_link: str, timezone: str = 'ET') -> bool:
    """
    Send 1-day reminder with Zoom link.
    """
    subject = "Tomorrow: TSP Workshop — Zoom link inside"

    plain_body = f"""Hi {first_name},

The TSP Investment Strategies Workshop is tomorrow at 12:00 PM {timezone}.

Join via Zoom: {zoom_link}

A few things that'll make the hour more useful:

- Have tsp.gov open (or your account number handy) — David sometimes pulls up fund data live
- Know your current allocation going in — even just "80% C, 20% G" is enough
- Come with a question. The Q&A is where most people get the most value.

What David covers tomorrow:

- C, S, I, F, and G Fund breakdown — the actual holdings, not just the letters
- Traditional vs. Roth TSP: the breakeven calculation David uses with his own clients
- L-Fund mechanics and how to tell if yours is actually right for your retirement date
- TSP withdrawal strategies and which ones minimize your tax exposure in retirement

Grab lunch and join us. It's one hour.

See you tomorrow,
David Fei & the PlanWell Team
planwellfp.com
"""

    header = _navy_header("Tomorrow at Noon", "TSP Investment Strategies Workshop")
    body = f"""
<tr>
  <td style="padding:32px 30px 24px;background-color:#ffffff;">
    <p style="margin:0 0 16px;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;line-height:1.5;">Hi {first_name},</p>
    <p style="margin:0 0 24px;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;line-height:1.5;">The TSP workshop is <strong>tomorrow at 12:00 PM {timezone}</strong>. Here's your Zoom link.</p>

    <!-- Big Zoom button -->
    {_gold_button(zoom_link, 'Join the Workshop')}

    <p style="margin:-16px 0 24px;text-align:center;font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#888888;">Or copy: {zoom_link}</p>

    <!-- Details box -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;border-left:4px solid #c9a55c;margin-bottom:24px;">
      <tr><td style="padding:16px 20px;">
        <table cellpadding="0" cellspacing="0" border="0" width="100%">
          {_detail_row('Date:', webinar_date)}
          {_detail_row('Time:', f'12:00 PM &ndash; 1:00 PM {timezone}')}
          {_detail_row('Host:', 'David Fei, CFP&reg;, ChFEBC&#8480;, AIF&reg;')}
        </table>
      </td></tr>
    </table>

    <p style="margin:0 0 12px;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#1e3a5f;">Make it a useful hour:</p>
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:24px;">
      <tr><td style="padding:8px 0;border-bottom:1px solid #eeeeee;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;">Have <strong>tsp.gov</strong> open or your account number handy</td></tr>
      <tr><td style="padding:8px 0;border-bottom:1px solid #eeeeee;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;">Know your current allocation going in (even "80% C, 20% G" is enough)</td></tr>
      <tr><td style="padding:8px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.5;">Come with a question &mdash; the Q&amp;A is where most people get the most value</td></tr>
    </table>

    <!-- Agenda teaser -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;border-radius:4px;margin-bottom:24px;">
      <tr><td style="padding:20px 24px;">
        <p style="margin:0 0 12px;font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:bold;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.5px;">Tomorrow's agenda</p>
        <p style="margin:0 0 6px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.6;">&#8594;&nbsp; C, S, I, F, and G Funds &mdash; what you're actually invested in</p>
        <p style="margin:0 0 6px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.6;">&#8594;&nbsp; Traditional vs. Roth TSP: the breakeven calculation David uses with clients</p>
        <p style="margin:0 0 6px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.6;">&#8594;&nbsp; L-Fund mechanics and how to check if yours fits your retirement date</p>
        <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.6;">&#8594;&nbsp; TSP withdrawal strategies that minimize your tax exposure</p>
      </td></tr>
    </table>

    <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;">Grab lunch and join us. It's one hour.<br><br><strong>David Fei &amp; the PlanWell Team</strong></p>
  </td>
</tr>"""

    html_body = _wrap_email(
        "Your Zoom link is inside. TSP Workshop tomorrow at noon — grab lunch and join us.",
        header, body
    )

    return send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# 5. Day-Of
# ---------------------------------------------------------------------------

def send_tsp_dayof(to_email: str, first_name: str, zoom_link: str,
                    timezone: str = 'ET') -> bool:
    """
    Send day-of reminder (morning of webinar).
    """
    subject = "Today at noon — TSP Workshop starts in a few hours"

    plain_body = f"""Hi {first_name},

The TSP Investment Strategies Workshop starts today at 12:00 PM {timezone}.

Join here: {zoom_link}

One hour. Bring your lunch. David will cover TSP fund allocation, Roth conversion strategy, and withdrawal planning — the stuff that actually moves the needle on your federal retirement.

If you have a TSP question you've been sitting on, bring it. David takes questions throughout.

See you at noon,
David Fei & the PlanWell Team
planwellfp.com
"""

    header = _navy_header("Today at Noon", "TSP Investment Strategies Workshop &mdash; 12:00 PM " + timezone)
    body = f"""
<tr>
  <td style="padding:32px 30px 24px;background-color:#ffffff;text-align:center;">
    <p style="margin:0 0 8px;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;line-height:1.5;text-align:left;">Hi {first_name},</p>
    <p style="margin:0 0 24px;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;line-height:1.5;text-align:left;">It's today. The TSP workshop starts at <strong>12:00 PM {timezone}</strong>. Grab your lunch and click below.</p>

    {_gold_button(zoom_link, 'Join the Workshop Now')}

    <p style="margin:-12px 0 28px;font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#888888;">{zoom_link}</p>

    <!-- What's happening today -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;border-radius:4px;margin-bottom:24px;text-align:left;">
      <tr><td style="padding:20px 24px;">
        <p style="margin:0 0 12px;font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:bold;color:#1e3a5f;text-transform:uppercase;letter-spacing:0.5px;">In today's session</p>
        <p style="margin:0 0 8px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.6;">&#8594;&nbsp; TSP fund breakdown: what C, S, I, F, and G actually hold</p>
        <p style="margin:0 0 8px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.6;">&#8594;&nbsp; Traditional vs. Roth TSP &mdash; the decision most feds get wrong</p>
        <p style="margin:0 0 8px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.6;">&#8594;&nbsp; L-Fund analysis and allocation strategy by retirement timeline</p>
        <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;line-height:1.6;">&#8594;&nbsp; TSP withdrawal options and tax strategy</p>
      </td></tr>
    </table>

    <p style="margin:0 0 24px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#555555;text-align:left;">Questions are welcome throughout. If you've got a TSP question you've been sitting on, today's the day to ask it.</p>

    <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;text-align:left;">See you at noon,<br><strong>David Fei &amp; the PlanWell Team</strong></p>
  </td>
</tr>"""

    html_body = _wrap_email(
        "TSP Workshop starts at noon today. One click to join — bring your lunch.",
        header, body
    )

    return send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# Main — smoke test
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    print("Testing TSP webinar email templates...")

    send_tsp_confirmation(
        to_email="test@example.com",
        first_name="John",
        webinar_date="Wednesday, April 15",
        timezone="ET",
        calendar_link="https://planwellfp.com/calendar"
    )
    print("✓ TSP Confirmation template ready")

    send_tsp_7day(
        to_email="test@example.com",
        first_name="John",
        webinar_date="Wednesday, April 15"
    )
    print("✓ TSP 7-day template ready")

    send_tsp_3day(
        to_email="test@example.com",
        first_name="John",
        webinar_date="Wednesday, April 15",
        timezone="ET"
    )
    print("✓ TSP 3-day template ready")

    send_tsp_1day(
        to_email="test@example.com",
        first_name="John",
        webinar_date="Wednesday, April 15",
        zoom_link="https://zoom.us/j/123456789",
        timezone="ET"
    )
    print("✓ TSP 1-day template ready")

    send_tsp_dayof(
        to_email="test@example.com",
        first_name="John",
        zoom_link="https://zoom.us/j/123456789",
        timezone="ET"
    )
    print("✓ TSP Day-of template ready")
