"""
TSP Post-Webinar Email Templates
==================================
HTML email templates for the TSP workshop post-webinar nurture sequence.
Covers both attendees (5 emails) and no-shows (2 emails) with separate tracks.

Key differences from FERS workshop emails:
- 1-hour workshop (not 3), hosted by David Fei, CFP®, ChFEBC℠, AIF®
- NO recording references (business decision)
- TSP-specific content: fund allocation, Roth conversion, withdrawal strategies, tax traps
- Book-a-call CTA goes to /book-call
- Cross-sells the full 3-hour FERS workshop

Usage:
    from tsp_post_webinar_emails import send_tsp_post_day1_takeaways, send_tsp_noshow_day1_missed, ...
"""

from email_sender import send_email


# ---------------------------------------------------------------------------
# Shared HTML helpers
# ---------------------------------------------------------------------------

def _html_wrap(preheader: str, header_title: str, body_html: str) -> str:
    """Wrap content in a mobile-first, Outlook-safe email shell. All CSS inline."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<title>{header_title}</title>
</head>
<body style="margin:0;padding:0;background-color:#f5f5f5;font-family:Arial,Helvetica,sans-serif;">
<!-- Preheader -->
<div style="display:none;max-height:0;overflow:hidden;color:#f5f5f5;">{preheader}&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</div>
<!-- Wrapper -->
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#f5f5f5;">
  <tr>
    <td align="center" style="padding:20px 10px;">
      <!-- Email container -->
      <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;width:100%;background-color:#ffffff;">
        <!-- Header -->
        <tr>
          <td style="background-color:#1e3a5f;padding:28px 30px;text-align:center;">
            <p style="margin:0 0 4px 0;font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#c9a55c;letter-spacing:1px;text-transform:uppercase;">PlanWell Financial Planning</p>
            <h1 style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:22px;font-weight:bold;color:#ffffff;line-height:1.3;">{header_title}</h1>
          </td>
        </tr>
        <!-- Body -->
        <tr>
          <td style="padding:30px 30px 20px 30px;background-color:#ffffff;">
            <div style="font-family:Arial,Helvetica,sans-serif;font-size:16px;line-height:1.6;color:#333333;">
              {body_html}
            </div>
          </td>
        </tr>
        <!-- Footer -->
        <tr>
          <td style="background-color:#f5f5f5;padding:20px 30px;text-align:center;">
            <p style="margin:0 0 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#666666;">PlanWell Financial Planning &bull; <a href="https://planwellfp.com" style="color:#1e3a5f;text-decoration:none;">planwellfp.com</a></p>
            <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#999999;">David Fei, CFP&reg;, ChFEBC&#8480;, AIF&reg;</p>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>"""


def _gold_btn(url: str, label: str) -> str:
    """Inline gold CTA button, 44px min touch target."""
    return f"""<table cellpadding="0" cellspacing="0" border="0" style="margin:10px auto;">
  <tr>
    <td style="background-color:#c9a55c;border-radius:6px;">
      <a href="{url}" style="display:inline-block;padding:14px 28px;font-family:Arial,Helvetica,sans-serif;font-size:16px;font-weight:bold;color:#1e3a5f;text-decoration:none;min-height:44px;line-height:1.4;">{label}</a>
    </td>
  </tr>
</table>"""


def _outline_btn(url: str, label: str) -> str:
    """Inline outline CTA button (secondary action), 44px min touch target."""
    return f"""<table cellpadding="0" cellspacing="0" border="0" style="margin:10px auto;">
  <tr>
    <td style="border:2px solid #c9a55c;border-radius:6px;">
      <a href="{url}" style="display:inline-block;padding:12px 26px;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#1e3a5f;text-decoration:none;min-height:44px;line-height:1.4;">{label}</a>
    </td>
  </tr>
</table>"""


def _callout(content_html: str) -> str:
    """Gold left-border callout box."""
    return f"""<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:20px 0;">
  <tr>
    <td style="border-left:4px solid #c9a55c;background-color:#f5f5f5;padding:16px 20px;">
      {content_html}
    </td>
  </tr>
</table>"""


# ---------------------------------------------------------------------------
# ATTENDEE TRACK
# ---------------------------------------------------------------------------

def send_tsp_post_day1_takeaways(to_email: str, first_name: str,
                                  next_webinar_date: str = '', registration_url: str = '') -> bool:
    """
    Day +1 post-webinar (attendee): TSP takeaways + dual CTA (book call / FERS workshop cross-sell).
    """
    subject = f"{first_name}, here's what we covered in the TSP workshop"

    next_webinar_section_plain = ""
    next_webinar_section_html = ""
    if next_webinar_date and registration_url:
        next_webinar_section_plain = f"\n\nReady for the full picture? The 3-hour FERS Retirement Workshop goes deep on your pension, Social Security timing, healthcare bridge, and how TSP fits into the whole plan.\n\nRegister for the FERS Workshop ({next_webinar_date}): {registration_url}"
        next_webinar_section_html = f"""<p style="margin:24px 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">Ready for the full picture? The <strong>3-hour FERS Retirement Workshop</strong> goes deep on your pension, Social Security timing, healthcare bridge, and how TSP fits into the whole plan.</p>
<p style="margin:0 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#666666;text-align:center;">Next workshop: <strong>{next_webinar_date}</strong></p>
{_outline_btn(registration_url, f"Register for the FERS Workshop")}"""

    plain_body = f"""Hi {first_name},

Thanks for joining the TSP Investment Strategies workshop with David Fei. Here are the three things that matter most coming out of today's session:

1. The G Fund is not a safe harbor — it's a slow drain. At current yields, the G Fund barely keeps pace with inflation. If you're 10+ years from retirement and sitting 70–80% in G, you're likely losing purchasing power every single year.

2. Roth TSP has a window — and it closes. The years between your MRA and when you start drawing Social Security are often the lowest-tax years of your federal career. That's the window for Roth conversions. Miss it and you're paying taxes on every dollar you pull out later.

3. Withdrawal order is where the real money is. It's not just how much you have — it's which account you draw from first. The difference between pulling from TSP before vs. after Social Security can be $40,000–$80,000 in lifetime taxes for a typical fed.

If you want to look at your specific situation — your numbers, your timeline — David does a free 45-minute TSP review:

Book your free TSP review: https://planwellfp.com/book-call{next_webinar_section_plain}

— David Fei, CFP®
PlanWell Financial Planning
planwellfp.com
"""

    body_html = f"""<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">Hi {first_name},</p>
<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">Thanks for joining the <strong>TSP Investment Strategies</strong> workshop with David. Here are the three things that matter most from today's session.</p>

{_callout('''<p style="margin:0 0 14px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#1e3a5f;">1. The G Fund is not a safe harbor — it&#8217;s a slow drain.</p>
<p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;">At current yields, the G Fund barely keeps pace with inflation. If you&#8217;re 10+ years from retirement and sitting 70–80% in G, you&#8217;re likely losing purchasing power every single year.</p>''')}

{_callout('''<p style="margin:0 0 14px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#1e3a5f;">2. Roth TSP has a window — and it closes.</p>
<p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;">The years between your MRA and when you start drawing Social Security are often the lowest-tax years of your federal career. That&#8217;s the window for Roth conversions. Miss it and you&#8217;re paying taxes on every dollar you pull out later.</p>''')}

{_callout('''<p style="margin:0 0 14px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#1e3a5f;">3. Withdrawal order is where the real money is.</p>
<p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;">It&#8217;s not just how much you have — it&#8217;s which account you draw from first. The difference between pulling from TSP before vs. after Social Security can be $40,000–$80,000 in lifetime taxes for a typical fed.</p>''')}

<p style="margin:20px 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">If you want to look at your specific situation — your numbers, your timeline — David does a <strong>free 45-minute TSP review</strong>:</p>

<p style="text-align:center;margin:20px 0;">
{_gold_btn("https://planwellfp.com/book-call", "Book Your Free TSP Review")}
</p>

{next_webinar_section_html}

<p style="margin:28px 0 4px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;">— David Fei, CFP&reg;<br>PlanWell Financial Planning</p>"""

    html_body = _html_wrap(
        preheader="Three things to remember from today's TSP workshop.",
        header_title="Your TSP Workshop Takeaways",
        body_html=body_html
    )

    return send_email(to_email, subject, plain_body, html_body)


def send_tsp_post_day3_takeaways(to_email: str, first_name: str,
                                  takeaway_1: str = '', takeaway_2: str = '', takeaway_3: str = '') -> bool:
    """
    Day +3 post-webinar (attendee): Educational — "The allocation mistake most feds make after 50."
    """
    subject = "The allocation mistake most feds make after 50"

    if not takeaway_1:
        takeaway_1 = "After 50, most feds gradually shift into the G Fund. It feels responsible. But the G Fund's real return after inflation is close to zero — sometimes negative. A GS-13 who moved to 80% G at age 52 and stayed there until 62 likely gave up $60,000–$100,000 in growth compared to a 60/40 allocation."
    if not takeaway_2:
        takeaway_2 = "The L Funds auto-rebalance toward bonds as your target date gets closer. If your L Fund is targeting 2030 but you're still 8 years from retirement, you're probably more conservative than you need to be. The built-in glide path isn't wrong — it just might not match your actual situation."
    if not takeaway_3:
        takeaway_3 = "You don't need to go aggressive. Even holding 30–40% in the C Fund or a mix of C and S through your 50s gives your money a meaningful chance to grow. The goal isn't maximum return — it's not leaving money on the table out of caution you don't actually need yet."

    plain_body = f"""Hi {first_name},

One thing we see constantly in client reviews: feds who shifted heavily into the G Fund after 50 and never moved back.

Here's why that matters — and what to think about instead:

1. {takeaway_1}

2. {takeaway_2}

3. {takeaway_3}

The right allocation depends on your specific retirement date, pension amount, other income sources, and how you'd actually sleep at night during a market dip. There's no universal answer.

If you want David to look at your current allocation and tell you what he actually thinks, the TSP review call is free:

https://planwellfp.com/book-call

— David Fei, CFP®
PlanWell Financial Planning
"""

    body_html = f"""<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">Hi {first_name},</p>
<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">One thing we see constantly in client reviews: feds who shifted heavily into the G Fund after 50 and never moved back.</p>
<p style="margin:0 0 20px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">Here's why that matters — and what to think about instead:</p>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 16px 0;">
  <tr>
    <td style="padding:16px 20px;background-color:#f5f5f5;border-left:4px solid #c9a55c;">
      <p style="margin:0 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:bold;color:#c9a55c;text-transform:uppercase;letter-spacing:0.5px;">The G Fund problem</p>
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;">{takeaway_1}</p>
    </td>
  </tr>
</table>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 16px 0;">
  <tr>
    <td style="padding:16px 20px;background-color:#f5f5f5;border-left:4px solid #c9a55c;">
      <p style="margin:0 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:bold;color:#c9a55c;text-transform:uppercase;letter-spacing:0.5px;">The L Fund trap</p>
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;">{takeaway_2}</p>
    </td>
  </tr>
</table>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 24px 0;">
  <tr>
    <td style="padding:16px 20px;background-color:#f5f5f5;border-left:4px solid #c9a55c;">
      <p style="margin:0 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;font-weight:bold;color:#c9a55c;text-transform:uppercase;letter-spacing:0.5px;">What "balanced" actually looks like</p>
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;">{takeaway_3}</p>
    </td>
  </tr>
</table>

<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">The right allocation depends on your retirement date, pension amount, other income sources, and how you'd actually handle a market dip. No universal answer here.</p>
<p style="margin:0 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">If you want David to look at your current allocation and tell you what he actually thinks, the TSP review is free:</p>

<p style="text-align:center;margin:20px 0;">
{_gold_btn("https://planwellfp.com/book-call", "Book Your Free TSP Review")}
</p>

<p style="margin:28px 0 4px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;">— David Fei, CFP&reg;<br>PlanWell Financial Planning</p>"""

    html_body = _html_wrap(
        preheader="Why G Fund heavy after 50 often costs more than it saves.",
        header_title="The Allocation Mistake Most Feds Make After 50",
        body_html=body_html
    )

    return send_email(to_email, subject, plain_body, html_body)


def send_tsp_post_day7_benefits_report(to_email: str, first_name: str,
                                        booking_url: str = '/book-call') -> bool:
    """
    Day +7 post-webinar (attendee): Free TSP review call offer.
    """
    if not booking_url.startswith('http'):
        booking_url = f"https://planwellfp.com{booking_url}"

    subject = f"{first_name}, want a second set of eyes on your TSP?"

    plain_body = f"""Hi {first_name},

It's been a week since the TSP workshop. Quick question: have you actually looked at your current fund allocation recently?

Most feds we talk to haven't changed their TSP allocation in years. Some haven't touched it since they enrolled. That's not necessarily wrong — but it's worth knowing whether what you set up in year 3 still makes sense in year 18.

In a free TSP review call with David, you'll cover:

- Your current allocation and whether it matches your timeline
- Whether traditional or Roth contributions make more sense for your bracket
- What your withdrawal sequence should look like — TSP first, pension first, or Social Security first
- What your TSP balance could realistically look like at retirement, under different contribution and return assumptions

It's 45 minutes. No pitch, no pressure. David will tell you what he actually thinks.

{booking_url}

— David Fei, CFP®
PlanWell Financial Planning
"""

    body_html = f"""<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">Hi {first_name},</p>
<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">It's been a week since the TSP workshop. Quick question: have you actually looked at your current fund allocation recently?</p>
<p style="margin:0 0 20px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">Most feds we talk to haven't changed their TSP allocation in years. Some haven't touched it since they enrolled. That's not necessarily wrong — but it's worth knowing whether what you set up in year 3 still makes sense in year 18.</p>

<p style="margin:0 0 12px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;font-weight:bold;color:#1e3a5f;">In a free TSP review call with David, you'll cover:</p>

<table cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr>
    <td style="padding:10px 0;border-bottom:1px solid #eeeeee;">
      <table cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td width="24" valign="top" style="padding-top:2px;"><span style="color:#c9a55c;font-size:18px;font-weight:bold;">&#x2713;</span></td>
          <td style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;padding-left:10px;">Your current allocation and whether it matches your retirement timeline</td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td style="padding:10px 0;border-bottom:1px solid #eeeeee;">
      <table cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td width="24" valign="top" style="padding-top:2px;"><span style="color:#c9a55c;font-size:18px;font-weight:bold;">&#x2713;</span></td>
          <td style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;padding-left:10px;">Whether traditional or Roth contributions make more sense for your tax bracket</td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td style="padding:10px 0;border-bottom:1px solid #eeeeee;">
      <table cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td width="24" valign="top" style="padding-top:2px;"><span style="color:#c9a55c;font-size:18px;font-weight:bold;">&#x2713;</span></td>
          <td style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;padding-left:10px;">What your withdrawal sequence should look like — TSP first, pension first, or Social Security first</td>
        </tr>
      </table>
    </td>
  </tr>
  <tr>
    <td style="padding:10px 0;">
      <table cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr>
          <td width="24" valign="top" style="padding-top:2px;"><span style="color:#c9a55c;font-size:18px;font-weight:bold;">&#x2713;</span></td>
          <td style="font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;padding-left:10px;">What your TSP balance could realistically look like at retirement under different scenarios</td>
        </tr>
      </table>
    </td>
  </tr>
</table>

<p style="margin:20px 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">It's 45 minutes. No pitch, no pressure. David will tell you what he actually thinks.</p>

<p style="text-align:center;margin:20px 0;">
{_gold_btn(booking_url, "Book Your Free TSP Review")}
</p>

<p style="margin:28px 0 4px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;">— David Fei, CFP&reg;<br>PlanWell Financial Planning</p>"""

    html_body = _html_wrap(
        preheader="45 minutes. No pitch. Just an honest look at your numbers.",
        header_title="Want a Second Set of Eyes on Your TSP?",
        body_html=body_html
    )

    return send_email(to_email, subject, plain_body, html_body)


def send_tsp_post_day10_case_study(to_email: str, first_name: str,
                                    case_study_url: str = '/case-studies') -> bool:
    """
    Day +10 post-webinar (attendee): Success story (GS-14, was 80% G Fund, optimized allocation).
    """
    if not case_study_url.startswith('http'):
        case_study_url = f"https://planwellfp.com{case_study_url}"

    subject = "She had $420K in TSP — 80% in G Fund. Here's what changed."

    plain_body = f"""Hi {first_name},

I want to share a situation we see fairly often.

A GS-14 in her mid-50s came to us about 18 months before her planned retirement. She had $420,000 in TSP, had been contributing for 22 years, and had moved 80% into the G Fund back in 2018 "to protect what she'd built."

The problem: she had 18 months until retirement — not 18 months until she needed the money. She'd likely draw from TSP for 25–30 years. She was treating a 30-year time horizon like it was a 18-month one.

Here's what her review turned up:

1. ALLOCATION: Moving to 50% C Fund / 30% G Fund / 20% F Fund added meaningful expected return without excessive volatility given her timeline and pension income floor.

2. ROTH CONVERSION: She was in the 22% bracket. Her pension plus Social Security would push her to 24% in retirement. We modeled converting $35,000/year from traditional TSP to Roth over three years — locking in 22% now vs. paying 24% later.

3. WITHDRAWAL SEQUENCING: Her plan was to start TSP withdrawals immediately at retirement. We ran the numbers on delaying TSP until 70 while living off her pension + bridge benefit. The difference in lifetime tax burden: roughly $68,000.

None of these are exotic moves. They're just decisions that are hard to see clearly when you're inside your own situation.

She retired on schedule. And she started retirement in a materially different position than she would have been without the review.

If you'd like to see more:
{case_study_url}

Or if you'd just like to book a call:
https://planwellfp.com/book-call

— David Fei, CFP®
PlanWell Financial Planning
"""

    body_html = f"""<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">Hi {first_name},</p>
<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">I want to share a situation we see fairly often.</p>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 20px 0;">
  <tr>
    <td style="background-color:#1e3a5f;padding:20px 24px;border-radius:4px;">
      <p style="margin:0 0 10px 0;font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#c9a55c;text-transform:uppercase;letter-spacing:1px;font-weight:bold;">Client Situation</p>
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#ffffff;line-height:1.5;">GS-14, mid-50s &bull; $420K in TSP &bull; 80% G Fund &bull; 18 months from retirement</p>
    </td>
  </tr>
</table>

<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">She'd moved 80% into G Fund in 2018 to "protect what she'd built." Reasonable instinct — but here's the problem: she had 18 months until retirement, not 18 months until she needed the money. She'd likely draw from TSP for <strong>25–30 years</strong>. She was treating a 30-year time horizon like an 18-month one.</p>

<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;font-weight:bold;color:#1e3a5f;">Here's what her review turned up:</p>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 12px 0;">
  <tr>
    <td style="padding:14px 20px;background-color:#f5f5f5;border-left:4px solid #c9a55c;">
      <p style="margin:0 0 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:bold;color:#c9a55c;text-transform:uppercase;letter-spacing:0.5px;">1. Allocation</p>
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;">Moving to 50% C Fund / 30% G Fund / 20% F Fund added meaningful expected return without excessive volatility — given her pension income floor and 30-year draw horizon.</p>
    </td>
  </tr>
</table>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 12px 0;">
  <tr>
    <td style="padding:14px 20px;background-color:#f5f5f5;border-left:4px solid #c9a55c;">
      <p style="margin:0 0 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:bold;color:#c9a55c;text-transform:uppercase;letter-spacing:0.5px;">2. Roth Conversion</p>
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;">She was in the 22% bracket now. Pension + Social Security would push her to 24% in retirement. Converting $35,000/year over three years locked in 22% instead of paying 24% later.</p>
    </td>
  </tr>
</table>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 20px 0;">
  <tr>
    <td style="padding:14px 20px;background-color:#f5f5f5;border-left:4px solid #c9a55c;">
      <p style="margin:0 0 6px 0;font-family:Arial,Helvetica,sans-serif;font-size:13px;font-weight:bold;color:#c9a55c;text-transform:uppercase;letter-spacing:0.5px;">3. Withdrawal Sequencing</p>
      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;">She planned to start TSP withdrawals immediately at retirement. Delaying TSP until 70 while living off pension + bridge benefit reduced her lifetime tax burden by roughly <strong>$68,000</strong>.</p>
    </td>
  </tr>
</table>

<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">None of these are exotic moves. They're just decisions that are hard to see clearly when you're inside your own situation.</p>
<p style="margin:0 0 20px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">She retired on schedule — in a materially different position than she would have been without the review.</p>

<p style="text-align:center;margin:20px 0;">
{_gold_btn("https://planwellfp.com/book-call", "Book Your Free TSP Review")}
{_outline_btn(case_study_url, "Read More Client Stories")}
</p>

<p style="margin:28px 0 4px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;">— David Fei, CFP&reg;<br>PlanWell Financial Planning</p>"""

    html_body = _html_wrap(
        preheader="GS-14, $420K in TSP, 80% G Fund. Here's what the review found.",
        header_title="A Real TSP Review: What Changed",
        body_html=body_html
    )

    return send_email(to_email, subject, plain_body, html_body)


def send_tsp_post_day14_soft_close(to_email: str, first_name: str,
                                    booking_url: str = '/book-call') -> bool:
    """
    Day +14 post-webinar (attendee): Soft close, mentions full FERS workshop, signed by David Fei.
    """
    if not booking_url.startswith('http'):
        booking_url = f"https://planwellfp.com{booking_url}"

    subject = "Last note from me on your TSP"

    plain_body = f"""Hi {first_name},

I've sent a few emails over the past two weeks, so I'll keep this one short.

TSP is just one piece of your retirement picture. If you've been thinking about the bigger question — when can I actually retire, what will my pension look like, how do I coordinate Social Security, what do I do with healthcare before Medicare — that's what the 3-hour FERS Retirement Workshop covers.

Most feds find it changes how they think about their retirement date. Not because the news is always good — but because they finally have the actual numbers in front of them.

If you want to work through your specific situation one-on-one, the TSP review call is still open:

{booking_url}

No expiration on that offer. Whenever you're ready.

— David Fei, CFP®, ChFEBC℠, AIF®
PlanWell Financial Planning
planwellfp.com
"""

    body_html = f"""<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">Hi {first_name},</p>
<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">I've sent a few emails over the past two weeks, so I'll keep this one short.</p>
<p style="margin:0 0 20px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">TSP is one piece of your retirement picture. If you've been thinking about the bigger questions — <em>when can I actually retire, what will my pension look like, how do I coordinate Social Security, what do I do with healthcare before Medicare</em> — that's what the <strong>3-hour FERS Retirement Workshop</strong> covers.</p>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 20px 0;">
  <tr>
    <td style="background-color:#f5f5f5;padding:20px 24px;border-left:4px solid #1e3a5f;">
      <p style="margin:0 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;">Most feds find it changes how they think about their retirement date. Not because the news is always good — but because they finally have the actual numbers in front of them.</p>
    </td>
  </tr>
</table>

<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">If you want to work through your specific situation one-on-one, the TSP review call is still open:</p>

<p style="text-align:center;margin:20px 0;">
{_gold_btn(booking_url, "Book Your Free TSP Review")}
</p>

<p style="margin:16px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#666666;text-align:center;">No expiration on that offer. Whenever you're ready.</p>

<p style="margin:28px 0 4px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;">— David Fei, CFP&reg;, ChFEBC&#8480;, AIF&reg;<br>PlanWell Financial Planning</p>"""

    html_body = _html_wrap(
        preheader="One last note — and a mention of the bigger picture.",
        header_title="Last Note on Your TSP",
        body_html=body_html
    )

    return send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# NO-SHOW TRACK
# ---------------------------------------------------------------------------

def send_tsp_noshow_day1_missed(to_email: str, first_name: str,
                                 next_webinar_date: str = '', registration_url: str = '') -> bool:
    """
    Day +1 no-show: What you missed + dual CTA (book call / next webinar).
    """
    subject = f"{first_name}, you missed the TSP workshop — here's what we covered"

    next_webinar_plain = ""
    next_webinar_html = ""
    if next_webinar_date and registration_url:
        next_webinar_plain = f"\n\nOr if you'd rather catch the full thing live, we run the TSP Investment Strategies workshop regularly:\n\nNext session ({next_webinar_date}): {registration_url}"
        next_webinar_html = f"""<p style="margin:24px 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">Or if you'd rather catch the full workshop live, we run it regularly:</p>
<p style="margin:0 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#666666;text-align:center;">Next session: <strong>{next_webinar_date}</strong></p>
{_outline_btn(registration_url, "Register for the Next Workshop")}"""

    plain_body = f"""Hi {first_name},

You registered for the TSP Investment Strategies workshop but couldn't make it — no problem.

Here's a quick rundown of what we covered in the hour:

1. Why the G Fund often doesn't do what people think it does — and what that means if you're 10+ years from retirement and sitting 70–80% in G.

2. Roth TSP: when it makes sense, when it doesn't, and why the years right before retirement are often your best window.

3. Withdrawal sequencing: how the order you draw from TSP, your pension, and Social Security affects your lifetime tax bill by tens of thousands of dollars.

If any of those hit close to home, David offers a free 45-minute TSP review:

https://planwellfp.com/book-call{next_webinar_plain}

— David Fei, CFP®
PlanWell Financial Planning
"""

    body_html = f"""<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">Hi {first_name},</p>
<p style="margin:0 0 20px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">You registered for the <strong>TSP Investment Strategies</strong> workshop but couldn't make it — no problem. Here's a quick rundown of what we covered in the hour.</p>

{_callout('''<p style="margin:0 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#1e3a5f;">1. The G Fund problem</p>
<p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;">Why the G Fund often doesn&#8217;t do what people expect — and what that means if you&#8217;re 10+ years from retirement and sitting 70–80% in G.</p>''')}

{_callout('''<p style="margin:0 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#1e3a5f;">2. Roth TSP timing</p>
<p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;">When Roth contributions make sense, when they don&#8217;t, and why the years right before retirement are often your best conversion window.</p>''')}

{_callout('''<p style="margin:0 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;font-weight:bold;color:#1e3a5f;">3. Withdrawal sequencing</p>
<p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#444444;">How the order you draw from TSP, your pension, and Social Security affects your lifetime tax bill — often by tens of thousands of dollars.</p>''')}

<p style="margin:20px 0 8px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">If any of these hit close to home, David offers a <strong>free 45-minute TSP review</strong>:</p>

<p style="text-align:center;margin:20px 0;">
{_gold_btn("https://planwellfp.com/book-call", "Book Your Free TSP Review")}
</p>

{next_webinar_html}

<p style="margin:28px 0 4px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;">— David Fei, CFP&reg;<br>PlanWell Financial Planning</p>"""

    html_body = _html_wrap(
        preheader="Here's a quick rundown of what we covered in the TSP workshop.",
        header_title="What We Covered in the TSP Workshop",
        body_html=body_html
    )

    return send_email(to_email, subject, plain_body, html_body)


def send_tsp_noshow_day5_next_webinar(to_email: str, first_name: str,
                                       next_webinar_date: str, registration_url: str) -> bool:
    """
    Day +5 no-show: Next workshop invitation.
    """
    subject = f"The next TSP workshop is {next_webinar_date}"

    plain_body = f"""Hi {first_name},

A quick heads up: we're running the TSP Investment Strategies workshop again on {next_webinar_date}.

It's one hour with David Fei, CFP®. We cover:

- Fund allocation by decade — what to hold at 45 vs. 55 vs. 62
- Roth TSP vs. traditional: how to think about it based on your specific tax situation
- Withdrawal strategy: the sequencing decisions that most feds get wrong

If your TSP is a "set it and forget it" situation, this is worth an hour. Most feds leave with at least one change they want to make.

Register here: {registration_url}

— David Fei, CFP®
PlanWell Financial Planning
planwellfp.com
"""

    body_html = f"""<p style="margin:0 0 16px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">Hi {first_name},</p>
<p style="margin:0 0 20px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">A quick heads up: we're running the <strong>TSP Investment Strategies workshop</strong> again on <strong>{next_webinar_date}</strong>.</p>

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 20px 0;">
  <tr>
    <td style="background-color:#1e3a5f;padding:20px 24px;border-radius:4px;">
      <p style="margin:0 0 12px 0;font-family:Arial,Helvetica,sans-serif;font-size:13px;color:#c9a55c;text-transform:uppercase;letter-spacing:1px;font-weight:bold;">What We Cover</p>
      <table cellpadding="0" cellspacing="0" border="0" width="100%">
        <tr><td style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#ffffff;">&#x25B8;&nbsp;&nbsp;Fund allocation by decade — what to hold at 45 vs. 55 vs. 62</td></tr>
        <tr><td style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#ffffff;">&#x25B8;&nbsp;&nbsp;Roth TSP vs. traditional, based on your actual tax situation</td></tr>
        <tr><td style="padding:6px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#ffffff;">&#x25B8;&nbsp;&nbsp;Withdrawal sequencing — the decisions most feds get wrong</td></tr>
      </table>
    </td>
  </tr>
</table>

<p style="margin:0 0 20px 0;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:#333333;">If your TSP is a "set it and forget it" situation, this is worth an hour. Most feds leave with at least one concrete change they want to make.</p>

<p style="text-align:center;margin:20px 0;">
{_gold_btn(registration_url, f"Register for {next_webinar_date}")}
</p>

<p style="margin:16px 0 0 0;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#666666;text-align:center;">Or skip the workshop and go straight to a one-on-one review: <a href="https://planwellfp.com/book-call" style="color:#1e3a5f;">planwellfp.com/book-call</a></p>

<p style="margin:28px 0 4px 0;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:#333333;">— David Fei, CFP&reg;<br>PlanWell Financial Planning</p>"""

    html_body = _html_wrap(
        preheader=f"One hour. Fund allocation, Roth timing, and withdrawal strategy.",
        header_title=f"TSP Workshop: {next_webinar_date}",
        body_html=body_html
    )

    return send_email(to_email, subject, plain_body, html_body)


# ---------------------------------------------------------------------------
# Test block
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    TEST_EMAIL = "test@example.com"
    TEST_NAME = "Alex"
    TEST_DATE = "April 10, 2026"
    TEST_REG_URL = "https://planwellfp.com/webinar"

    print("Testing TSP post-webinar email functions...")

    tests = [
        ("Day +1 Attendee Takeaways",
         send_tsp_post_day1_takeaways(TEST_EMAIL, TEST_NAME, TEST_DATE, TEST_REG_URL)),
        ("Day +3 Attendee Takeaways",
         send_tsp_post_day3_takeaways(TEST_EMAIL, TEST_NAME)),
        ("Day +7 Benefits Report",
         send_tsp_post_day7_benefits_report(TEST_EMAIL, TEST_NAME)),
        ("Day +10 Case Study",
         send_tsp_post_day10_case_study(TEST_EMAIL, TEST_NAME)),
        ("Day +14 Soft Close",
         send_tsp_post_day14_soft_close(TEST_EMAIL, TEST_NAME)),
        ("No-Show Day +1",
         send_tsp_noshow_day1_missed(TEST_EMAIL, TEST_NAME, TEST_DATE, TEST_REG_URL)),
        ("No-Show Day +5",
         send_tsp_noshow_day5_next_webinar(TEST_EMAIL, TEST_NAME, TEST_DATE, TEST_REG_URL)),
    ]

    for name, result in tests:
        status = "PASS" if result else "FAIL"
        print(f"  [{status}] {name}")

    print("Done.")
