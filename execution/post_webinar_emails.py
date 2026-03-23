"""
Post-Webinar Email Templates
==============================
HTML email templates for the post-webinar nurture sequence.
Covers both attendees and no-shows with separate tracks.

Usage:
    from post_webinar_emails import send_post_day1_takeaways, send_noshow_day1_missed, ...
"""

from email_sender import send_email


def send_post_day1_takeaways(to_email: str, first_name: str,
                              next_webinar_date: str = '', registration_url: str = 'https://planwellfp.com/webinar') -> bool:
    """
    Day 1 post-webinar: Key insights recap + dual CTA (book call / refer a colleague).
    No recording shared — business decision to maintain exclusivity.
    """
    subject = f"{first_name}, here's what we covered yesterday"

    next_webinar_plain = f"\nRegister for the next workshop ({next_webinar_date}): {registration_url}" if next_webinar_date else ""

    next_webinar_btn = f"""
            <tr>
              <td align="center" style="padding-top: 12px;">
                <a href="{registration_url}" style="display: inline-block; background-color: #ffffff; color: #1e3a5f; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 15px; font-family: Arial, Helvetica, sans-serif; border: 2px solid #c9a55c; min-height: 44px; line-height: 1.2;">Register for the Next Workshop ({next_webinar_date})</a>
              </td>
            </tr>""" if next_webinar_date else ""

    plain_body = f"""Hi {first_name},

Thanks for spending three hours with us yesterday. Here are the three things we most want you to walk away knowing:

1. Your High-3 matters more than your current salary. If you have flexibility in your last three years, even a modest pay bump compounds into a permanent pension increase for the rest of your life.

2. TSP, pension, and Social Security don't exist in a vacuum. The order you draw from each account directly affects your federal tax rate in retirement — and most federal employees get this wrong.

3. FEHB is one of the best benefits in the federal system, but only if you protect it. You must be enrolled for 5 consecutive years before retirement to carry it into retirement. Miss that window and you lose it permanently.

If any of that raised specific questions about your own numbers, that's exactly what the free 30-minute call is for.

Book a call: https://planwellfp.com/book-call{next_webinar_plain}

— Brennan & David
PlanWell Financial Planning | planwellfp.com
"""

    html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Key Insights from Yesterday's Workshop</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: Arial, Helvetica, sans-serif;">
  <!-- Preheader -->
  <div style="display: none; max-height: 0; overflow: hidden; font-size: 1px; color: #f5f5f5;">Your High-3, TSP timing, and the FEHB rule most people miss &#8203;&nbsp;&#8203;&nbsp;</div>

  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f5;">
    <tr>
      <td align="center" style="padding: 24px 16px;">

        <!-- Card -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; overflow: hidden;">

          <!-- Header -->
          <tr>
            <td style="background-color: #1e3a5f; padding: 32px 32px 28px; text-align: center;">
              <p style="margin: 0 0 6px; font-size: 13px; color: #c9a55c; letter-spacing: 1px; text-transform: uppercase; font-family: Arial, Helvetica, sans-serif;">FERS Retirement Workshop</p>
              <h1 style="margin: 0; font-size: 24px; color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-weight: bold; line-height: 1.3;">Three things to take away from yesterday</h1>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding: 32px;">

              <p style="margin: 0 0 20px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Hi {first_name},</p>

              <p style="margin: 0 0 24px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Thanks for spending three hours with us yesterday. Here are the three things we most want you to walk away knowing:</p>

              <!-- Takeaway 1 -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 16px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 16px 20px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0 0 4px; font-size: 12px; color: #c9a55c; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; font-family: Arial, Helvetica, sans-serif;">Your High-3</p>
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">If you have flexibility in your last three years, even a modest pay bump compounds into a permanent pension increase for the rest of your life.</p>
                  </td>
                </tr>
              </table>

              <!-- Takeaway 2 -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 16px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 16px 20px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0 0 4px; font-size: 12px; color: #c9a55c; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; font-family: Arial, Helvetica, sans-serif;">TSP + Pension + Social Security</p>
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">The order you draw from each account directly affects your federal tax rate in retirement — and most federal employees get this wrong.</p>
                  </td>
                </tr>
              </table>

              <!-- Takeaway 3 -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 28px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 16px 20px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0 0 4px; font-size: 12px; color: #c9a55c; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; font-family: Arial, Helvetica, sans-serif;">FEHB in Retirement</p>
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">You must be enrolled for 5 consecutive years before retirement to carry it into retirement. Miss that window and you lose it permanently.</p>
                  </td>
                </tr>
              </table>

              <p style="margin: 0 0 28px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">If any of that raised specific questions about your own numbers, that's exactly what the free 30-minute call is for.</p>

              <!-- CTA -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="center" style="padding-bottom: 12px;">
                    <a href="https://planwellfp.com/book-call" style="display: inline-block; background-color: #c9a55c; color: #1e3a5f; padding: 16px 32px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; font-family: Arial, Helvetica, sans-serif; min-height: 44px; line-height: 1.2;">Book a Free 30-Min Call</a>
                  </td>
                </tr>
                {next_webinar_btn}
              </table>

              <p style="margin: 28px 0 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">— Brennan &amp; David<br><span style="color: #666666; font-size: 14px;">Brennan Rhule, CFP&#174;, ChFEBC&#8480;, AIF&#174; &amp; David Fei, CFP&#174;, ChFEBC&#8480;, AIF&#174;</span></p>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #f5f5f5; padding: 20px 32px; text-align: center; border-top: 1px solid #e0e0e0;">
              <p style="margin: 0; font-size: 13px; color: #888888; font-family: Arial, Helvetica, sans-serif;">PlanWell Financial Planning &nbsp;|&nbsp; <a href="https://planwellfp.com" style="color: #888888; text-decoration: underline;">planwellfp.com</a></p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    return send_email(to_email, subject, plain_body, html_body)


def send_post_day3_takeaways(to_email: str, first_name: str,
                              takeaway_1: str = '', takeaway_2: str = '', takeaway_3: str = '') -> bool:
    """
    Day 3 post-webinar: Educational deep-dive on ONE topic from the workshop.
    Defaults to the FERS supplement — a high-value, often misunderstood topic.
    """
    subject = "The FERS supplement: what it is and who qualifies"

    # Use passed takeaways if provided, otherwise use default FERS supplement deep-dive
    if takeaway_1 and takeaway_2 and takeaway_3:
        insight_1 = takeaway_1
        insight_2 = takeaway_2
        insight_3 = takeaway_3
        topic_headline = "Three things worth revisiting"
        topic_intro = f"Here are three specifics from the workshop worth sitting with:"
        use_custom = True
    else:
        use_custom = False

    plain_body = f"""Hi {first_name},

Today I want to zero in on something we covered in the workshop that tends to generate the most follow-up questions: the FERS Special Retirement Supplement.

Here's the short version:

If you retire before age 62 under an immediate, unreduced retirement (MRA+30, MRA+10 doesn't qualify), you're entitled to a monthly supplement that approximates what Social Security would pay you at 62 based only on your federal service years.

The formula: (years of FERS service ÷ 40) × your estimated Social Security benefit at 62.

Example: 30 years of service, $1,800 estimated SS benefit at 62 → supplement = $1,350/month.

It stops automatically at 62, regardless of whether you've started Social Security. It's also subject to an earnings test — if you earn more than the annual exempt amount (currently around $22,320), your supplement gets reduced $1 for every $2 over that threshold.

This matters if you're planning to work part-time in retirement. A $30,000 side income could reduce your supplement by nearly $4,000/year.

The supplement is automatic — you don't apply for it separately. But confirming your eligibility and running your numbers before you retire is worth doing.

If you want to see exactly what your supplement would be, we can calculate it on your free call.

Book a call: https://planwellfp.com/book-call

— Brennan & David
PlanWell Financial Planning | planwellfp.com
""" if not use_custom else f"""Hi {first_name},

Three specifics from last week's workshop worth sitting with:

{insight_1}

{insight_2}

{insight_3}

Any of these apply directly to your situation? Book a free 30-minute call and we'll run the numbers.

Book a call: https://planwellfp.com/book-call

— Brennan & David
PlanWell Financial Planning | planwellfp.com
"""

    if use_custom:
        insight_rows = f"""
              <!-- Takeaway 1 -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 16px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 16px 20px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">{insight_1}</p>
                  </td>
                </tr>
              </table>
              <!-- Takeaway 2 -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 16px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 16px 20px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">{insight_2}</p>
                  </td>
                </tr>
              </table>
              <!-- Takeaway 3 -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 28px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 16px 20px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">{insight_3}</p>
                  </td>
                </tr>
              </table>
              <p style="margin: 0 0 28px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Any of these apply to your situation? We can run the actual numbers on a free call.</p>"""
        body_headline = "Three things worth revisiting"
        body_intro = f"""<p style="margin: 0 0 24px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Hi {first_name},</p>
              <p style="margin: 0 0 24px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Three specifics from last week's workshop worth sitting with:</p>"""
    else:
        insight_rows = """
              <p style="margin: 0 0 20px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Here's the short version:</p>

              <!-- Rule box -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
                <tr>
                  <td style="padding: 20px 24px; background-color: #1e3a5f; border-radius: 6px;">
                    <p style="margin: 0 0 8px; font-size: 15px; color: #c9a55c; font-weight: bold; font-family: Arial, Helvetica, sans-serif;">Who qualifies</p>
                    <p style="margin: 0; font-size: 15px; color: #ffffff; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">You must retire under an immediate, <em>unreduced</em> retirement — meaning MRA+30, age 60+20, or age 62+5. MRA+10 does not qualify.</p>
                  </td>
                </tr>
              </table>

              <!-- Formula box -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 16px 20px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0 0 6px; font-size: 12px; color: #c9a55c; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; font-family: Arial, Helvetica, sans-serif;">The Formula</p>
                    <p style="margin: 0 0 10px; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">(Years of FERS service &#247; 40) &#215; Your estimated Social Security benefit at 62</p>
                    <p style="margin: 0; font-size: 14px; color: #555555; font-style: italic; font-family: Arial, Helvetica, sans-serif;">Example: 30 years of service, $1,800 estimated SS benefit at 62 &rarr; supplement = $1,350/month.</p>
                  </td>
                </tr>
              </table>

              <!-- Earnings test warning -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
                <tr>
                  <td width="4" style="background-color: #1e3a5f; border-radius: 2px;"></td>
                  <td style="padding: 16px 20px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0 0 6px; font-size: 12px; color: #1e3a5f; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; font-family: Arial, Helvetica, sans-serif;">Watch out: the earnings test</p>
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">The supplement stops at 62 — automatically. And if you earn more than ~$22,320/year from work, your supplement is reduced $1 for every $2 over that. A $30,000 part-time income could cost you nearly $4,000/year in lost supplement.</p>
                  </td>
                </tr>
              </table>

              <p style="margin: 0 0 28px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">The supplement is automatic — you don't apply separately. But confirming your eligibility and calculating your exact number before you retire is worth doing. We can do that on a free call.</p>"""
        body_headline = "The FERS supplement, explained"
        body_intro = f"""<p style="margin: 0 0 20px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Hi {first_name},</p>
              <p style="margin: 0 0 24px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Today I want to zero in on something from the workshop that tends to generate the most follow-up questions: the <strong>FERS Special Retirement Supplement</strong>.</p>"""

    html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The FERS supplement: what it is and who qualifies</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: Arial, Helvetica, sans-serif;">
  <!-- Preheader -->
  <div style="display: none; max-height: 0; overflow: hidden; font-size: 1px; color: #f5f5f5;">The formula, the earnings test, and who actually qualifies &#8203;&nbsp;&#8203;&nbsp;</div>

  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f5;">
    <tr>
      <td align="center" style="padding: 24px 16px;">

        <!-- Card -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; overflow: hidden;">

          <!-- Header -->
          <tr>
            <td style="background-color: #1e3a5f; padding: 32px 32px 28px; text-align: center;">
              <p style="margin: 0 0 6px; font-size: 13px; color: #c9a55c; letter-spacing: 1px; text-transform: uppercase; font-family: Arial, Helvetica, sans-serif;">Workshop Follow-Up</p>
              <h1 style="margin: 0; font-size: 24px; color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-weight: bold; line-height: 1.3;">{body_headline}</h1>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding: 32px;">
              {body_intro}
              {insight_rows}

              <!-- CTA -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="center">
                    <a href="https://planwellfp.com/book-call" style="display: inline-block; background-color: #c9a55c; color: #1e3a5f; padding: 16px 32px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; font-family: Arial, Helvetica, sans-serif; min-height: 44px; line-height: 1.2;">Calculate My Supplement on a Free Call</a>
                  </td>
                </tr>
              </table>

              <p style="margin: 28px 0 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">— Brennan &amp; David<br><span style="color: #666666; font-size: 14px;">Brennan Rhule, CFP&#174;, ChFEBC&#8480;, AIF&#174; &amp; David Fei, CFP&#174;, ChFEBC&#8480;, AIF&#174;</span></p>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #f5f5f5; padding: 20px 32px; text-align: center; border-top: 1px solid #e0e0e0;">
              <p style="margin: 0; font-size: 13px; color: #888888; font-family: Arial, Helvetica, sans-serif;">PlanWell Financial Planning &nbsp;|&nbsp; <a href="https://planwellfp.com" style="color: #888888; text-decoration: underline;">planwellfp.com</a></p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    return send_email(to_email, subject, plain_body, html_body)


def send_post_day7_benefits_report(to_email: str, first_name: str,
                                    booking_url: str = 'https://planwellfp.com/book-call') -> bool:
    """
    Day 7 post-webinar: Offer personalized Federal Benefits Report.
    Transition from education to personalization — "let's look at YOUR numbers."
    """
    subject = f"{first_name}, let's look at your actual numbers"

    plain_body = f"""Hi {first_name},

One week out from the workshop, here's what we hear most: "I learned a lot — but I still don't know what my retirement actually looks like."

That's the gap the Federal Benefits Report fills. It's a personalized analysis we build using your actual data:

- Your projected FERS pension at multiple retirement ages
- TSP projection based on your current balance and contribution rate
- FEHB cost comparison between your current plan and retirement options
- Social Security coordination strategy (when to claim, in what order)
- Your optimal retirement date, based on your specific numbers

It's not a sales presentation. It's a 30-minute working session where we run your numbers together.

It's free. And at the end, you'll know what your retirement actually looks like — not a federal employee's retirement in the abstract.

Book your call: {booking_url}

— Brennan & David
PlanWell Financial Planning | planwellfp.com
"""

    html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Federal Benefits Report</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: Arial, Helvetica, sans-serif;">
  <!-- Preheader -->
  <div style="display: none; max-height: 0; overflow: hidden; font-size: 1px; color: #f5f5f5;">What your retirement actually looks like — with your numbers, not a generic example &#8203;&nbsp;&#8203;&nbsp;</div>

  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f5;">
    <tr>
      <td align="center" style="padding: 24px 16px;">

        <!-- Card -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; overflow: hidden;">

          <!-- Header -->
          <tr>
            <td style="background-color: #1e3a5f; padding: 32px 32px 28px; text-align: center;">
              <p style="margin: 0 0 6px; font-size: 13px; color: #c9a55c; letter-spacing: 1px; text-transform: uppercase; font-family: Arial, Helvetica, sans-serif;">Week One Follow-Up</p>
              <h1 style="margin: 0; font-size: 24px; color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-weight: bold; line-height: 1.3;">Let's look at your actual numbers</h1>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding: 32px;">

              <p style="margin: 0 0 20px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Hi {first_name},</p>

              <!-- Quote -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 24px;">
                <tr>
                  <td style="padding: 20px 24px; background-color: #f5f5f5; border-left: 4px solid #c9a55c; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0; font-size: 16px; color: #555555; line-height: 1.6; font-style: italic; font-family: Arial, Helvetica, sans-serif;">"I learned a lot — but I still don't know what my retirement actually looks like."</p>
                    <p style="margin: 8px 0 0; font-size: 13px; color: #888888; font-family: Arial, Helvetica, sans-serif;">What most attendees tell us one week out</p>
                  </td>
                </tr>
              </table>

              <p style="margin: 0 0 20px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">That's the gap the <strong>Federal Benefits Report</strong> fills. It's a personalized analysis built from your actual data:</p>

              <!-- Report items -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 24px;">
                <tr>
                  <td style="padding: 20px 24px; background-color: #f5f5f5; border-radius: 6px;">
                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                      <tr>
                        <td style="padding: 6px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;">&#10003;&nbsp; Your projected FERS pension at multiple retirement ages</td>
                      </tr>
                      <tr>
                        <td style="padding: 6px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;">&#10003;&nbsp; TSP projection based on your current balance and contribution rate</td>
                      </tr>
                      <tr>
                        <td style="padding: 6px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;">&#10003;&nbsp; FEHB cost comparison between your current plan and retirement options</td>
                      </tr>
                      <tr>
                        <td style="padding: 6px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;">&#10003;&nbsp; Social Security coordination strategy — when to claim, in what order</td>
                      </tr>
                      <tr>
                        <td style="padding: 6px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;">&#10003;&nbsp; Your optimal retirement date, based on your specific numbers</td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

              <p style="margin: 0 0 28px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">It's not a sales presentation. It's a 30-minute working session where we run your numbers together. Free. And at the end, you'll know what your retirement actually looks like.</p>

              <!-- CTA -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 8px;">
                <tr>
                  <td align="center">
                    <a href="{booking_url}" style="display: inline-block; background-color: #c9a55c; color: #1e3a5f; padding: 16px 32px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; font-family: Arial, Helvetica, sans-serif; min-height: 44px; line-height: 1.2;">Book My Free Benefits Review</a>
                  </td>
                </tr>
              </table>

              <p style="margin: 28px 0 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">— Brennan &amp; David<br><span style="color: #666666; font-size: 14px;">Brennan Rhule, CFP&#174;, ChFEBC&#8480;, AIF&#174; &amp; David Fei, CFP&#174;, ChFEBC&#8480;, AIF&#174;</span></p>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #f5f5f5; padding: 20px 32px; text-align: center; border-top: 1px solid #e0e0e0;">
              <p style="margin: 0; font-size: 13px; color: #888888; font-family: Arial, Helvetica, sans-serif;">PlanWell Financial Planning &nbsp;|&nbsp; <a href="https://planwellfp.com" style="color: #888888; text-decoration: underline;">planwellfp.com</a></p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    return send_email(to_email, subject, plain_body, html_body)


def send_post_day10_case_study(to_email: str, first_name: str,
                                case_study_url: str = 'https://planwellfp.com/case-studies') -> bool:
    """
    Day 10 post-webinar: Anonymized client success story to build trust.
    Social proof through a specific, credible scenario.
    """
    subject = "A GS-14 with 24 years discovered he could retire 18 months earlier"

    plain_body = f"""Hi {first_name},

This came up on a client call last month that I think is worth sharing.

A GS-14 program manager at DoD — 24 years in, planning to retire at 62. He'd been budgeting his whole career around that number and had built a solid TSP balance. He came to us for a second opinion before the final stretch.

When we ran his Federal Benefits Report, three things stood out:

1. His MRA was 56. With 30 years at that point, he qualified for an immediate unreduced pension — not at 62, at 56+6.

2. He'd been contributing to traditional TSP exclusively. A Roth TSP conversion strategy over the next three years before retirement would have saved him an estimated $47,000 in federal taxes over the first decade of withdrawals.

3. His FEGLI coverage was costing him $340/month. In retirement, that cost was going to rise significantly with age. A term life policy through a private insurer would give him the same coverage for about $90/month.

He's now on track to retire 18 months earlier than planned, with a more tax-efficient withdrawal strategy and lower insurance costs.

None of this required unusual circumstances — just running the actual numbers and knowing where to look.

Read more client examples: {case_study_url}

If you'd like us to look at your situation the same way, the free 30-minute call is how we start.

Book a call: https://planwellfp.com/book-call

— Brennan & David
PlanWell Financial Planning | planwellfp.com
"""

    html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>A GS-14 with 24 years discovered he could retire 18 months earlier</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: Arial, Helvetica, sans-serif;">
  <!-- Preheader -->
  <div style="display: none; max-height: 0; overflow: hidden; font-size: 1px; color: #f5f5f5;">He'd been planning for age 62. The numbers said 56+6. &#8203;&nbsp;&#8203;&nbsp;</div>

  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f5;">
    <tr>
      <td align="center" style="padding: 24px 16px;">

        <!-- Card -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; overflow: hidden;">

          <!-- Header -->
          <tr>
            <td style="background-color: #1e3a5f; padding: 32px 32px 28px; text-align: center;">
              <p style="margin: 0 0 6px; font-size: 13px; color: #c9a55c; letter-spacing: 1px; text-transform: uppercase; font-family: Arial, Helvetica, sans-serif;">Client Story</p>
              <h1 style="margin: 0; font-size: 24px; color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-weight: bold; line-height: 1.3;">A GS-14 at DoD who thought he was retiring at 62</h1>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding: 32px;">

              <p style="margin: 0 0 20px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Hi {first_name},</p>

              <p style="margin: 0 0 24px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">This came up on a client call last month that I think is worth sharing.</p>

              <!-- Scenario -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 24px;">
                <tr>
                  <td style="padding: 20px 24px; background-color: #f5f5f5; border-radius: 6px;">
                    <p style="margin: 0 0 4px; font-size: 13px; color: #888888; text-transform: uppercase; letter-spacing: 1px; font-family: Arial, Helvetica, sans-serif;">The situation</p>
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">GS-14 program manager, DoD. 24 years of service. Planning to retire at 62. Strong TSP balance. Came to us for a second opinion before the final stretch.</p>
                  </td>
                </tr>
              </table>

              <p style="margin: 0 0 16px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">When we ran his Federal Benefits Report, three things stood out:</p>

              <!-- Finding 1 -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 12px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 14px 18px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0 0 4px; font-size: 13px; color: #c9a55c; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; font-family: Arial, Helvetica, sans-serif;">Early retirement eligibility</p>
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">His MRA was 56. With 30 years at that point, he qualified for an immediate unreduced pension at 56+6 — not 62.</p>
                  </td>
                </tr>
              </table>

              <!-- Finding 2 -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 12px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 14px 18px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0 0 4px; font-size: 13px; color: #c9a55c; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; font-family: Arial, Helvetica, sans-serif;">TSP tax strategy</p>
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">He was 100% traditional TSP. A Roth conversion strategy over three years before retirement would save an estimated $47,000 in federal taxes over the first decade of withdrawals.</p>
                  </td>
                </tr>
              </table>

              <!-- Finding 3 -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 24px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 14px 18px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0 0 4px; font-size: 13px; color: #c9a55c; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; font-family: Arial, Helvetica, sans-serif;">FEGLI cost</p>
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">His FEGLI was $340/month — and rising with age. A private term policy gave him identical coverage for ~$90/month.</p>
                  </td>
                </tr>
              </table>

              <p style="margin: 0 0 12px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;"><strong>He's now on track to retire 18 months earlier than planned</strong> — with a more tax-efficient strategy and lower insurance costs.</p>

              <p style="margin: 0 0 28px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">None of this required unusual circumstances. Just running the actual numbers and knowing where to look.</p>

              <!-- CTA -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 16px;">
                <tr>
                  <td align="center">
                    <a href="https://planwellfp.com/book-call" style="display: inline-block; background-color: #c9a55c; color: #1e3a5f; padding: 16px 32px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; font-family: Arial, Helvetica, sans-serif; min-height: 44px; line-height: 1.2;">Run My Numbers — Free Call</a>
                  </td>
                </tr>
                <tr>
                  <td align="center" style="padding-top: 12px;">
                    <a href="{case_study_url}" style="font-size: 14px; color: #c9a55c; text-decoration: underline; font-family: Arial, Helvetica, sans-serif;">Read more client examples</a>
                  </td>
                </tr>
              </table>

              <p style="margin: 28px 0 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">— Brennan &amp; David<br><span style="color: #666666; font-size: 14px;">Brennan Rhule, CFP&#174;, ChFEBC&#8480;, AIF&#174; &amp; David Fei, CFP&#174;, ChFEBC&#8480;, AIF&#174;</span></p>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #f5f5f5; padding: 20px 32px; text-align: center; border-top: 1px solid #e0e0e0;">
              <p style="margin: 0; font-size: 13px; color: #888888; font-family: Arial, Helvetica, sans-serif;">PlanWell Financial Planning &nbsp;|&nbsp; <a href="https://planwellfp.com" style="color: #888888; text-decoration: underline;">planwellfp.com</a></p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    return send_email(to_email, subject, plain_body, html_body)


def send_post_day14_soft_close(to_email: str, first_name: str,
                                booking_url: str = 'https://planwellfp.com/book-call') -> bool:
    """
    Day 14 post-webinar: Soft close. Signed personally by David Fei.
    Human, no pressure — "most people learn but don't act."
    """
    subject = f"{first_name}, a quick note from David"

    plain_body = f"""Hi {first_name},

It's been two weeks since the workshop. I wanted to reach out personally.

Most people who attend learn something useful and then get back to work — and the information stays theoretical. That's not a criticism. It's just what happens when retirement feels like it's still a few years away.

But the federal employees who end up in the best position aren't the ones who had the most complex strategies. They're the ones who looked at their actual numbers early enough to do something about it.

If you've been meaning to get to it, this is your nudge. The free 30-minute call is just a working session — no pitch, no pressure. We'll look at your specific situation and tell you exactly where you stand.

If now isn't the right time, no problem. We'll be here when it is.

Book a call: {booking_url}

— David Fei, CFP®, ChFEBC℠, AIF®
PlanWell Financial Planning | planwellfp.com
"""

    html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>A quick note from David</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: Arial, Helvetica, sans-serif;">
  <!-- Preheader -->
  <div style="display: none; max-height: 0; overflow: hidden; font-size: 1px; color: #f5f5f5;">The ones who end up in the best position are the ones who looked early enough to do something about it &#8203;&nbsp;&#8203;&nbsp;</div>

  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f5;">
    <tr>
      <td align="center" style="padding: 24px 16px;">

        <!-- Card -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; overflow: hidden;">

          <!-- Header -->
          <tr>
            <td style="background-color: #1e3a5f; padding: 32px 32px 28px; text-align: center;">
              <p style="margin: 0 0 6px; font-size: 13px; color: #c9a55c; letter-spacing: 1px; text-transform: uppercase; font-family: Arial, Helvetica, sans-serif;">Two Weeks Later</p>
              <h1 style="margin: 0; font-size: 24px; color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-weight: bold; line-height: 1.3;">A quick note from David</h1>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding: 32px;">

              <p style="margin: 0 0 20px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Hi {first_name},</p>

              <p style="margin: 0 0 20px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">It's been two weeks since the workshop. I wanted to reach out personally.</p>

              <p style="margin: 0 0 20px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Most people who attend learn something useful and then get back to work — and the information stays theoretical. That's not a criticism. It's just what happens when retirement feels like it's still a few years away.</p>

              <!-- Highlight -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
                <tr>
                  <td style="padding: 20px 24px; background-color: #f5f5f5; border-left: 4px solid #1e3a5f; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">The federal employees who end up in the best position aren't the ones who had the most complex strategies. They're the ones who looked at their actual numbers early enough to do something about it.</p>
                  </td>
                </tr>
              </table>

              <p style="margin: 0 0 28px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">If you've been meaning to get to it, this is your nudge. The free 30-minute call is just a working session — no pitch, no pressure. We look at your specific situation and tell you exactly where you stand. If now isn't the right time, that's fine too. We'll be here when it is.</p>

              <!-- CTA -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 8px;">
                <tr>
                  <td align="center">
                    <a href="{booking_url}" style="display: inline-block; background-color: #c9a55c; color: #1e3a5f; padding: 16px 32px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; font-family: Arial, Helvetica, sans-serif; min-height: 44px; line-height: 1.2;">Book a Free 30-Min Call</a>
                  </td>
                </tr>
              </table>

              <p style="margin: 28px 0 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">— David Fei, CFP&#174;, ChFEBC&#8480;, AIF&#174;<br><span style="color: #666666; font-size: 14px;">PlanWell Financial Planning</span></p>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #f5f5f5; padding: 20px 32px; text-align: center; border-top: 1px solid #e0e0e0;">
              <p style="margin: 0; font-size: 13px; color: #888888; font-family: Arial, Helvetica, sans-serif;">PlanWell Financial Planning &nbsp;|&nbsp; <a href="https://planwellfp.com" style="color: #888888; text-decoration: underline;">planwellfp.com</a></p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    return send_email(to_email, subject, plain_body, html_body)


def send_noshow_day1_missed(to_email: str, first_name: str,
                            next_webinar_date: str = '', registration_url: str = 'https://planwellfp.com/webinar') -> bool:
    """
    Day 1 no-show: Empathetic summary of what was covered. Dual CTA (book call / register next).
    No recording shared — business decision to maintain exclusivity.
    """
    subject = "You registered for the FERS Workshop — here's what was covered"

    next_webinar_plain = f"\nRegister for the next workshop ({next_webinar_date}): {registration_url}" if next_webinar_date else ""

    next_webinar_btn = f"""
            <tr>
              <td align="center" style="padding-top: 12px;">
                <a href="{registration_url}" style="display: inline-block; background-color: #ffffff; color: #1e3a5f; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 15px; font-family: Arial, Helvetica, sans-serif; border: 2px solid #c9a55c; min-height: 44px; line-height: 1.2;">Register for the Next Workshop ({next_webinar_date})</a>
              </td>
            </tr>""" if next_webinar_date else ""

    plain_body = f"""Hi {first_name},

You registered for yesterday's FERS Retirement Workshop but weren't able to make it. No worries — life happens.

Here's a brief summary of what Brennan and David covered over the three hours:

FERS pension formula and optimization
The workshop walked through exactly how your pension is calculated (1% × High-3 × years of service, or 1.1% if you're 62+ with 20+ years). More importantly, it covered the levers you can actually pull in your final years — and which ones make the biggest difference.

TSP withdrawal strategies
Most federal employees don't realize that withdrawing TSP in the wrong order can push them into a higher federal tax bracket. The workshop covered sequencing: which accounts to draw from first, when to convert to Roth, and how Social Security timing fits in.

FEHB and FEGLI decisions
The workshop covered the 5-year enrollment rule for carrying FEHB into retirement, how FEHB coordinates with Medicare, and whether FEGLI is worth keeping at age-adjusted rates (spoiler: often it isn't).

Survivor benefits
The default survivor benefit election is not always the right choice — and once you retire, changing it is extremely limited. The workshop explained the tradeoffs.

If you'd like to talk through how any of this applies to your specific situation, the free 30-minute call is available.

Book a call: https://planwellfp.com/book-call{next_webinar_plain}

— Brennan & David
PlanWell Financial Planning | planwellfp.com
"""

    html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>What was covered at the FERS Workshop</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: Arial, Helvetica, sans-serif;">
  <!-- Preheader -->
  <div style="display: none; max-height: 0; overflow: hidden; font-size: 1px; color: #f5f5f5;">Pension formula, TSP sequencing, FEHB rules, and survivor benefit tradeoffs &#8203;&nbsp;&#8203;&nbsp;</div>

  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f5;">
    <tr>
      <td align="center" style="padding: 24px 16px;">

        <!-- Card -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; overflow: hidden;">

          <!-- Header -->
          <tr>
            <td style="background-color: #1e3a5f; padding: 32px 32px 28px; text-align: center;">
              <p style="margin: 0 0 6px; font-size: 13px; color: #c9a55c; letter-spacing: 1px; text-transform: uppercase; font-family: Arial, Helvetica, sans-serif;">FERS Retirement Workshop</p>
              <h1 style="margin: 0; font-size: 24px; color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-weight: bold; line-height: 1.3;">Here's what was covered yesterday</h1>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding: 32px;">

              <p style="margin: 0 0 20px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Hi {first_name},</p>

              <p style="margin: 0 0 24px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">You registered for yesterday's FERS Retirement Workshop but weren't able to make it. No worries — here's what Brennan and David covered over the three hours.</p>

              <!-- Topic 1 -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 16px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 16px 20px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0 0 6px; font-size: 14px; color: #1e3a5f; font-weight: bold; font-family: Arial, Helvetica, sans-serif;">FERS Pension Formula and Optimization</p>
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">How your pension is calculated (1% × High-3 × years, or 1.1% at 62+/20+), and the levers you can pull in your final years to increase your lifetime payout.</p>
                  </td>
                </tr>
              </table>

              <!-- Topic 2 -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 16px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 16px 20px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0 0 6px; font-size: 14px; color: #1e3a5f; font-weight: bold; font-family: Arial, Helvetica, sans-serif;">TSP Withdrawal Strategies</p>
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Withdrawing TSP in the wrong order can push you into a higher federal tax bracket. The workshop covered sequencing, Roth conversion timing, and how Social Security fits in.</p>
                  </td>
                </tr>
              </table>

              <!-- Topic 3 -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 16px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 16px 20px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0 0 6px; font-size: 14px; color: #1e3a5f; font-weight: bold; font-family: Arial, Helvetica, sans-serif;">FEHB and FEGLI in Retirement</p>
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">The 5-year enrollment rule for carrying FEHB into retirement, how it coordinates with Medicare, and whether FEGLI is worth keeping at age-adjusted rates.</p>
                  </td>
                </tr>
              </table>

              <!-- Topic 4 -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 28px;">
                <tr>
                  <td width="4" style="background-color: #c9a55c; border-radius: 2px;"></td>
                  <td style="padding: 16px 20px; background-color: #f5f5f5; border-radius: 0 6px 6px 0;">
                    <p style="margin: 0 0 6px; font-size: 14px; color: #1e3a5f; font-weight: bold; font-family: Arial, Helvetica, sans-serif;">Survivor Benefits</p>
                    <p style="margin: 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">The default survivor benefit election isn't always right — and once you retire, changing it is extremely limited. The workshop covered the tradeoffs.</p>
                  </td>
                </tr>
              </table>

              <p style="margin: 0 0 28px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">If you'd like to talk through how any of this applies to your specific situation, the free 30-minute call is available.</p>

              <!-- CTA -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td align="center">
                    <a href="https://planwellfp.com/book-call" style="display: inline-block; background-color: #c9a55c; color: #1e3a5f; padding: 16px 32px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; font-family: Arial, Helvetica, sans-serif; min-height: 44px; line-height: 1.2;">Book a Free 30-Min Call</a>
                  </td>
                </tr>
                {next_webinar_btn}
              </table>

              <p style="margin: 28px 0 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">— Brennan &amp; David<br><span style="color: #666666; font-size: 14px;">Brennan Rhule, CFP&#174;, ChFEBC&#8480;, AIF&#174; &amp; David Fei, CFP&#174;, ChFEBC&#8480;, AIF&#174;</span></p>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #f5f5f5; padding: 20px 32px; text-align: center; border-top: 1px solid #e0e0e0;">
              <p style="margin: 0; font-size: 13px; color: #888888; font-family: Arial, Helvetica, sans-serif;">PlanWell Financial Planning &nbsp;|&nbsp; <a href="https://planwellfp.com" style="color: #888888; text-decoration: underline;">planwellfp.com</a></p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    return send_email(to_email, subject, plain_body, html_body)


def send_noshow_day5_next_webinar(to_email: str, first_name: str,
                                   next_webinar_date: str, registration_url: str) -> bool:
    """
    Day 5 no-show: Invite to the next workshop. Focus on what's ahead, not what was missed.
    """
    subject = f"Next FERS Workshop: {next_webinar_date}"

    plain_body = f"""Hi {first_name},

Last week's workshop didn't work out timing-wise — we get it. Schedules are unpredictable.

The next FERS Retirement Workshop is scheduled for {next_webinar_date}. Same three-hour format, same topics: pension formula, TSP withdrawal strategies, FEHB in retirement, FEGLI analysis, survivor benefits, and Social Security coordination.

Workshop details:
- Date: {next_webinar_date}
- Time: 11:00 AM – 2:00 PM EST
- Format: Online via Zoom
- Cost: Free

Spots are capped to keep the Q&A session useful — so if you're planning to attend, register sooner rather than later.

Register here: {registration_url}

If your schedule won't allow the next workshop either and you'd rather talk through your situation directly, the free 30-minute call is also available:
https://planwellfp.com/book-call

— Brennan & David
PlanWell Financial Planning | planwellfp.com
"""

    html_body = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Next FERS Workshop: {next_webinar_date}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5; font-family: Arial, Helvetica, sans-serif;">
  <!-- Preheader -->
  <div style="display: none; max-height: 0; overflow: hidden; font-size: 1px; color: #f5f5f5;">Pension, TSP, FEHB, survivor benefits — same format, new date &#8203;&nbsp;&#8203;&nbsp;</div>

  <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f5f5f5;">
    <tr>
      <td align="center" style="padding: 24px 16px;">

        <!-- Card -->
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; overflow: hidden;">

          <!-- Header -->
          <tr>
            <td style="background-color: #1e3a5f; padding: 32px 32px 28px; text-align: center;">
              <p style="margin: 0 0 6px; font-size: 13px; color: #c9a55c; letter-spacing: 1px; text-transform: uppercase; font-family: Arial, Helvetica, sans-serif;">FERS Retirement Workshop</p>
              <h1 style="margin: 0; font-size: 26px; color: #ffffff; font-family: Arial, Helvetica, sans-serif; font-weight: bold; line-height: 1.3;">{next_webinar_date}</h1>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding: 32px;">

              <p style="margin: 0 0 20px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Hi {first_name},</p>

              <p style="margin: 0 0 24px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Last week's workshop didn't work out timing-wise — we get it. The next one is on <strong>{next_webinar_date}</strong>.</p>

              <!-- Details box -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 24px;">
                <tr>
                  <td style="padding: 20px 24px; background-color: #f5f5f5; border-left: 4px solid #c9a55c; border-radius: 0 6px 6px 0;">
                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                      <tr>
                        <td style="padding: 5px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;"><strong>Date:</strong> {next_webinar_date}</td>
                      </tr>
                      <tr>
                        <td style="padding: 5px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;"><strong>Time:</strong> 11:00 AM – 2:00 PM EST</td>
                      </tr>
                      <tr>
                        <td style="padding: 5px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;"><strong>Format:</strong> Online via Zoom</td>
                      </tr>
                      <tr>
                        <td style="padding: 5px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;"><strong>Cost:</strong> Free</td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

              <!-- Topics -->
              <p style="margin: 0 0 12px; font-size: 15px; color: #555555; font-family: Arial, Helvetica, sans-serif;">Three hours covering:</p>
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 24px;">
                <tr>
                  <td style="padding: 16px 20px; background-color: #f5f5f5; border-radius: 6px;">
                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                      <tr><td style="padding: 4px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;">&#8226;&nbsp; FERS pension formula and High-3 optimization</td></tr>
                      <tr><td style="padding: 4px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;">&#8226;&nbsp; TSP withdrawal strategies and tax sequencing</td></tr>
                      <tr><td style="padding: 4px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;">&#8226;&nbsp; FEHB in retirement and Medicare coordination</td></tr>
                      <tr><td style="padding: 4px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;">&#8226;&nbsp; FEGLI cost analysis</td></tr>
                      <tr><td style="padding: 4px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;">&#8226;&nbsp; Survivor benefit elections</td></tr>
                      <tr><td style="padding: 4px 0; font-size: 15px; color: #333333; font-family: Arial, Helvetica, sans-serif;">&#8226;&nbsp; Social Security coordination</td></tr>
                    </table>
                  </td>
                </tr>
              </table>

              <p style="margin: 0 0 28px; font-size: 16px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Spots are capped to keep the Q&amp;A session useful. Register sooner rather than later.</p>

              <!-- Primary CTA -->
              <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 20px;">
                <tr>
                  <td align="center">
                    <a href="{registration_url}" style="display: inline-block; background-color: #c9a55c; color: #1e3a5f; padding: 16px 32px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; font-family: Arial, Helvetica, sans-serif; min-height: 44px; line-height: 1.2;">Register for {next_webinar_date}</a>
                  </td>
                </tr>
              </table>

              <!-- Secondary note -->
              <p style="margin: 0 0 0; font-size: 14px; color: #888888; text-align: center; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">Can't make the workshop? <a href="https://planwellfp.com/book-call" style="color: #c9a55c; text-decoration: underline;">Book a free 30-min call instead.</a></p>

              <p style="margin: 28px 0 0; font-size: 15px; color: #333333; line-height: 1.6; font-family: Arial, Helvetica, sans-serif;">— Brennan &amp; David<br><span style="color: #666666; font-size: 14px;">Brennan Rhule, CFP&#174;, ChFEBC&#8480;, AIF&#174; &amp; David Fei, CFP&#174;, ChFEBC&#8480;, AIF&#174;</span></p>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background-color: #f5f5f5; padding: 20px 32px; text-align: center; border-top: 1px solid #e0e0e0;">
              <p style="margin: 0; font-size: 13px; color: #888888; font-family: Arial, Helvetica, sans-serif;">PlanWell Financial Planning &nbsp;|&nbsp; <a href="https://planwellfp.com" style="color: #888888; text-decoration: underline;">planwellfp.com</a></p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    return send_email(to_email, subject, plain_body, html_body)


if __name__ == '__main__':
    # Test email templates (will print to console if SMTP not configured)
    print("Testing post-webinar email templates...")

    send_post_day1_takeaways(
        to_email="test@example.com",
        first_name="John",
        next_webinar_date="Friday, April 10",
        registration_url="https://planwellfp.com/webinar"
    )
    print("  Day 1 takeaways template ready")

    send_post_day3_takeaways(
        to_email="test@example.com",
        first_name="John",
        takeaway_1="Your FERS pension is based on your High-3 salary and years of service",
        takeaway_2="The FERS supplement bridges the gap between retirement and Social Security",
        takeaway_3="You can keep FEHB in retirement if you've been enrolled for 5+ years"
    )
    print("  Day 3 takeaways template ready")

    send_post_day7_benefits_report(
        to_email="test@example.com",
        first_name="John"
    )
    print("  Day 7 benefits report template ready")

    send_post_day10_case_study(
        to_email="test@example.com",
        first_name="John"
    )
    print("  Day 10 case study template ready")

    send_post_day14_soft_close(
        to_email="test@example.com",
        first_name="John"
    )
    print("  Day 14 soft close template ready")

    send_noshow_day1_missed(
        to_email="test@example.com",
        first_name="John",
        next_webinar_date="Friday, April 10",
        registration_url="https://planwellfp.com/webinar"
    )
    print("  No-show day 1 missed template ready")

    send_noshow_day5_next_webinar(
        to_email="test@example.com",
        first_name="John",
        next_webinar_date="Friday, April 10",
        registration_url="https://planwellfp.com/webinar"
    )
    print("  No-show day 5 next webinar template ready")

    print("\nAll post-webinar templates validated.")
