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
    Day 1 post-webinar: Key takeaways and dual CTA (book call + next webinar).
    No recording shared — business decision to maintain urgency.
    """
    subject = "Key Insights from Yesterday's FERS Workshop"

    next_webinar_plain = f"\nRegister for the next workshop ({next_webinar_date}): {registration_url}" if next_webinar_date else ""

    next_webinar_btn = f"""
                <a href="{registration_url}" style="display: inline-block; background: transparent; color: #c9a55c; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; margin: 10px 0; border: 2px solid #c9a55c;">Register for Next Workshop ({next_webinar_date})</a>""" if next_webinar_date else ""

    plain_body = f"""Hi {first_name},

Thanks for joining the FERS Retirement Workshop! Here are the three biggest takeaways from yesterday's session:

1. Your FERS pension is likely worth $1M+ over your retirement. Small moves in your final years — like maximizing your High-3 — can add tens of thousands to your lifetime benefit.

2. TSP withdrawal timing can save you thousands in taxes. The order and timing of withdrawals from your TSP, Social Security, and pension can dramatically reduce your tax burden in retirement.

3. FEHB decisions must be made before age 65. If you're planning to coordinate FEHB with Medicare, the enrollment rules have firm deadlines that catch many federal employees off guard.

Over the next couple of weeks, we'll dig deeper into each of these topics.

If any of these hit close to home and you'd like to talk through your specific numbers, book a free 30-minute call:
https://planwellfp.com/book-call{next_webinar_plain}

Best,
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
        .takeaway-box {{ background: #f8f9fa; border-left: 4px solid #c9a55c; padding: 20px; margin: 20px 0; }}
        .takeaway-box h3 {{ color: #1e3a5f; margin-top: 0; }}
        .takeaway-box ol {{ margin: 0; padding-left: 20px; }}
        .takeaway-box li {{ margin: 12px 0; }}
        .cta-box {{ text-align: center; margin: 30px 0; }}
        .book-btn {{ display: inline-block; background: linear-gradient(135deg, #c9a55c 0%, #a88a44 100%); color: #152a45; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 18px; margin: 10px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Key Insights from Your Workshop</h1>
        </div>
        <div class="content">
            <p>Hi {first_name},</p>
            <p>Thanks for joining the <strong>FERS Retirement Workshop</strong>! Here are the three biggest takeaways from yesterday's session:</p>

            <div class="takeaway-box">
                <ol>
                    <li><strong>Your FERS pension is likely worth $1M+</strong> over your retirement. Small moves in your final years — like maximizing your High-3 — can add tens of thousands to your lifetime benefit.</li>
                    <li><strong>TSP withdrawal timing can save you thousands in taxes.</strong> The order and timing of withdrawals from your TSP, Social Security, and pension can dramatically reduce your tax burden in retirement.</li>
                    <li><strong>FEHB decisions must be made before age 65.</strong> If you're planning to coordinate FEHB with Medicare, the enrollment rules have firm deadlines that catch many federal employees off guard.</li>
                </ol>
            </div>

            <p>Over the next couple of weeks, we'll dig deeper into each of these topics.</p>
            <p>If any of these hit close to home and you'd like to talk through your specific numbers:</p>

            <div class="cta-box">
                <a href="https://planwellfp.com/book-call" class="book-btn">Book a Free Call</a>
                <br>{next_webinar_btn}
            </div>

            <p>Best,<br>The PlanWell Team</p>
        </div>
        <div class="footer">
            <p>PlanWell Financial Planning | planwellfp.com</p>
        </div>
    </div>
</body>
</html>
"""

    return send_email(to_email, subject, plain_body, html_body)


def send_post_day3_takeaways(to_email: str, first_name: str,
                              takeaway_1: str, takeaway_2: str, takeaway_3: str) -> bool:
    """
    Day 3 post-webinar: Top 3 insights from the workshop.
    """
    subject = "3 key takeaways from the FERS Workshop"

    plain_body = f"""Hi {first_name},

Here are the top 3 takeaways from the FERS Retirement Workshop:

1. {takeaway_1}

2. {takeaway_2}

3. {takeaway_3}

These are the areas where we see the biggest impact for federal employees planning their retirement.

Want to see how these apply to your specific situation? We offer a free 30-minute Federal Benefits Review where we can walk through your numbers.

Book a call: https://planwellfp.com/book-call

Best,
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
        .takeaway {{ background: #f8f9fa; border-left: 4px solid #c9a55c; padding: 15px 20px; margin: 15px 0; }}
        .takeaway .number {{ color: #c9a55c; font-size: 24px; font-weight: bold; }}
        .cta-box {{ background: #e8f4f8; padding: 20px; border-radius: 8px; margin: 25px 0; text-align: center; }}
        .book-btn {{ display: inline-block; background: linear-gradient(135deg, #c9a55c 0%, #a88a44 100%); color: #152a45; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Top 3 Workshop Takeaways</h1>
        </div>
        <div class="content">
            <p>Hi {first_name},</p>
            <p>Here are the top 3 takeaways from the FERS Retirement Workshop:</p>

            <div class="takeaway">
                <span class="number">1.</span> {takeaway_1}
            </div>
            <div class="takeaway">
                <span class="number">2.</span> {takeaway_2}
            </div>
            <div class="takeaway">
                <span class="number">3.</span> {takeaway_3}
            </div>

            <p>These are the areas where we see the biggest impact for federal employees planning their retirement.</p>

            <div class="cta-box">
                <p><strong>Want to see how these apply to your situation?</strong></p>
                <p>We offer a free 30-minute Federal Benefits Review.</p>
                <a href="https://planwellfp.com/book-call" class="book-btn">Book a Free Call</a>
            </div>

            <p>Best,<br>The PlanWell Team</p>
        </div>
        <div class="footer">
            <p>PlanWell Financial Planning | planwellfp.com</p>
        </div>
    </div>
</body>
</html>
"""

    return send_email(to_email, subject, plain_body, html_body)


def send_post_day7_benefits_report(to_email: str, first_name: str,
                                    booking_url: str = 'https://planwellfp.com/book-call') -> bool:
    """
    Day 7 post-webinar: Offer personalized Federal Benefits Report.
    """
    subject = f"{first_name}, get your personalized Federal Benefits Report"

    plain_body = f"""Hi {first_name},

One week after the workshop, attendees often tell us the same thing: "I learned a lot, but I still don't know my exact numbers."

That's why we created the Federal Benefits Report -- a personalized analysis of YOUR specific retirement picture:

What you'll get:
- Your projected FERS pension (at different retirement ages)
- TSP projection with current balance and contribution rate
- FEHB cost analysis in retirement
- Social Security coordination strategy
- Optimal retirement date recommendation

It's free. It takes 30 minutes. And you'll walk away knowing your numbers.

Book your call: {booking_url}

Best,
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
        .intro {{ font-style: italic; color: #555; margin: 20px 0; padding: 15px; border-left: 3px solid #ccc; }}
        .benefits {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .benefits h3 {{ color: #1e3a5f; margin-top: 0; }}
        .benefits ul {{ margin: 0; padding-left: 20px; }}
        .benefits li {{ margin: 8px 0; }}
        .cta-box {{ background: linear-gradient(135deg, #1e3a5f 0%, #152a45 100%); padding: 25px; border-radius: 8px; margin: 25px 0; text-align: center; }}
        .cta-box p {{ color: white; margin: 5px 0; }}
        .book-btn {{ display: inline-block; background: linear-gradient(135deg, #c9a55c 0%, #a88a44 100%); color: #152a45; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 18px; margin-top: 15px; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Your Federal Benefits Report</h1>
        </div>
        <div class="content">
            <p>Hi {first_name},</p>

            <div class="intro">
                "I learned a lot, but I still don't know my exact numbers."
                <br>-- What most attendees tell us one week after the workshop
            </div>

            <p>That's why we created the <strong>Federal Benefits Report</strong> -- a personalized analysis of YOUR specific retirement picture.</p>

            <div class="benefits">
                <h3>What you'll get:</h3>
                <ul>
                    <li>Your projected FERS pension (at different retirement ages)</li>
                    <li>TSP projection with current balance and contribution rate</li>
                    <li>FEHB cost analysis in retirement</li>
                    <li>Social Security coordination strategy</li>
                    <li>Optimal retirement date recommendation</li>
                </ul>
            </div>

            <p>It's free. It takes 30 minutes. And you'll walk away knowing your numbers.</p>

            <div class="cta-box">
                <p><strong>Ready to see your numbers?</strong></p>
                <a href="{booking_url}" class="book-btn">Book Your Free Call</a>
            </div>

            <p>Best,<br>The PlanWell Team</p>
        </div>
        <div class="footer">
            <p>PlanWell Financial Planning | planwellfp.com</p>
        </div>
    </div>
</body>
</html>
"""

    return send_email(to_email, subject, plain_body, html_body)


def send_post_day10_case_study(to_email: str, first_name: str,
                                case_study_url: str = 'https://planwellfp.com/case-studies') -> bool:
    """
    Day 10 post-webinar: Client success story to build trust.
    """
    subject = "How Sarah retired 2 years earlier than she thought possible"

    plain_body = f"""Hi {first_name},

I wanted to share a story that might resonate with you.

Sarah, a GS-13 with 28 years of service, came to us thinking she couldn't retire until 62. She was worried about:
- Whether her pension would be enough
- The gap between retirement and Social Security
- Keeping FEHB coverage

After running her Federal Benefits Report, we found:
- She was eligible for an immediate unreduced pension at 56+10 months
- Her FERS supplement would bridge the Social Security gap
- She could keep FEHB in retirement (she didn't know this was guaranteed)

She retired 2 years earlier than planned -- with more confidence about her finances than she'd ever had.

Read more stories: {case_study_url}

Every federal employee's situation is different. That's why we start with your numbers.

Book a free call to get your Federal Benefits Report:
https://planwellfp.com/book-call

Best,
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
        .story-box {{ background: #f8f9fa; border-left: 4px solid #c9a55c; padding: 20px; margin: 20px 0; }}
        .story-box h3 {{ color: #1e3a5f; margin-top: 0; }}
        .results {{ background: #d4edda; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .results h3 {{ color: #155724; margin-top: 0; }}
        .results p {{ margin: 5px 0; }}
        .cta-box {{ background: #e8f4f8; padding: 20px; border-radius: 8px; margin: 25px 0; text-align: center; }}
        .book-btn {{ display: inline-block; background: linear-gradient(135deg, #c9a55c 0%, #a88a44 100%); color: #152a45; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>A Story Worth Sharing</h1>
        </div>
        <div class="content">
            <p>Hi {first_name},</p>
            <p>I wanted to share a story that might resonate with you.</p>

            <div class="story-box">
                <h3>Sarah's Situation</h3>
                <p><strong>Sarah, a GS-13 with 28 years of service</strong>, came to us thinking she couldn't retire until 62. She was worried about:</p>
                <p>- Whether her pension would be enough</p>
                <p>- The gap between retirement and Social Security</p>
                <p>- Keeping FEHB coverage</p>
            </div>

            <div class="results">
                <h3>What We Found</h3>
                <p>- She was eligible for an immediate unreduced pension at 56+10 months</p>
                <p>- Her FERS supplement would bridge the Social Security gap</p>
                <p>- She could keep FEHB in retirement (she didn't know this was guaranteed)</p>
            </div>

            <p><strong>She retired 2 years earlier than planned</strong> -- with more confidence about her finances than she'd ever had.</p>

            <p style="text-align: center;"><a href="{case_study_url}" style="color: #c9a55c;">Read more client stories</a></p>

            <div class="cta-box">
                <p>Every situation is different. Let's look at <strong>your</strong> numbers.</p>
                <a href="https://planwellfp.com/book-call" class="book-btn">Book a Free Call</a>
            </div>

            <p>Best,<br>The PlanWell Team</p>
        </div>
        <div class="footer">
            <p>PlanWell Financial Planning | planwellfp.com</p>
        </div>
    </div>
</body>
</html>
"""

    return send_email(to_email, subject, plain_body, html_body)


def send_post_day14_soft_close(to_email: str, first_name: str,
                                booking_url: str = 'https://planwellfp.com/book-call') -> bool:
    """
    Day 14 post-webinar: Soft close - book a free 30-minute call.
    """
    subject = f"{first_name}, one last thing from the workshop"

    plain_body = f"""Hi {first_name},

It's been two weeks since the FERS Retirement Workshop, and I wanted to check in.

If you're like most attendees, you probably:
- Learned a lot but haven't taken action yet
- Still have questions about your specific numbers
- Want to make sure you're not leaving money on the table

That's completely normal. Retirement planning is complex, and generic information only gets you so far.

Here's what I'd suggest: book a free 30-minute Federal Benefits Review. No sales pitch -- just your numbers, your options, and honest answers to your questions.

We've helped over 500 federal employees get clarity on their retirement. Let us help you too.

Book your call: {booking_url}

Best,
David Perez, CFP
PlanWell Financial Planning

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
        .checklist {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .checklist p {{ margin: 8px 0; }}
        .promise {{ background: #e8f4f8; border-left: 4px solid #1e3a5f; padding: 15px 20px; margin: 20px 0; }}
        .cta-box {{ background: linear-gradient(135deg, #1e3a5f 0%, #152a45 100%); padding: 25px; border-radius: 8px; margin: 25px 0; text-align: center; }}
        .cta-box p {{ color: white; margin: 5px 0; }}
        .book-btn {{ display: inline-block; background: linear-gradient(135deg, #c9a55c 0%, #a88a44 100%); color: #152a45; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 18px; margin-top: 15px; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>One Last Thing</h1>
        </div>
        <div class="content">
            <p>Hi {first_name},</p>
            <p>It's been two weeks since the FERS Retirement Workshop, and I wanted to check in.</p>

            <div class="checklist">
                <p>If you're like most attendees, you probably:</p>
                <p>- Learned a lot but haven't taken action yet</p>
                <p>- Still have questions about your specific numbers</p>
                <p>- Want to make sure you're not leaving money on the table</p>
            </div>

            <p>That's completely normal. Retirement planning is complex, and generic information only gets you so far.</p>

            <div class="promise">
                <strong>Here's what I'd suggest:</strong> Book a free 30-minute Federal Benefits Review. No sales pitch -- just your numbers, your options, and honest answers to your questions.
            </div>

            <p>We've helped over 500 federal employees get clarity on their retirement. Let us help you too.</p>

            <div class="cta-box">
                <p><strong>30 minutes. Your numbers. No obligation.</strong></p>
                <a href="{booking_url}" class="book-btn">Book Your Free Call</a>
            </div>

            <p>Best,<br>David Perez, CFP<br>PlanWell Financial Planning</p>
        </div>
        <div class="footer">
            <p>PlanWell Financial Planning | planwellfp.com</p>
        </div>
    </div>
</body>
</html>
"""

    return send_email(to_email, subject, plain_body, html_body)


def send_noshow_day1_missed(to_email: str, first_name: str,
                            next_webinar_date: str = '', registration_url: str = 'https://planwellfp.com/webinar') -> bool:
    """
    Day 1 no-show: Summarize what they missed, dual CTA.
    No recording shared — business decision to maintain urgency.
    """
    subject = "Here's What You Missed at the FERS Workshop"

    next_webinar_plain = f"\nRegister for the next workshop ({next_webinar_date}): {registration_url}" if next_webinar_date else ""

    next_webinar_btn = f"""
                <a href="{registration_url}" style="display: inline-block; background: transparent; color: #c9a55c; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; margin: 10px 0; border: 2px solid #c9a55c;">Register for Next Workshop ({next_webinar_date})</a>""" if next_webinar_date else ""

    plain_body = f"""Hi {first_name},

We missed you at the FERS Retirement Workshop! Life happens -- no worries at all.

Here's a quick summary of what was covered so you know what you missed:

1. FERS Pension Optimization — We walked through how your High-3 salary, years of service, and retirement age interact to determine your pension. Most attendees were surprised to learn their pension could be worth over $1M in lifetime payments.

2. TSP Withdrawal Strategies — We covered the tax implications of different withdrawal orders and how timing your TSP distributions with Social Security can save thousands in taxes.

3. FEHB + Medicare Coordination — We explained the critical deadlines around age 65 that determine whether you can keep your federal health benefits alongside Medicare. Missing these deadlines can be costly.

The good news: we run these workshops regularly, and you're welcome to join the next one.

Book a free 30-minute call to discuss your situation:
https://planwellfp.com/book-call{next_webinar_plain}

Best,
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
        .topics {{ background: #e8f4f8; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .topics h3 {{ color: #1e3a5f; margin-top: 0; }}
        .topics ol {{ margin: 0; padding-left: 20px; }}
        .topics li {{ margin: 12px 0; }}
        .cta-box {{ text-align: center; margin: 30px 0; }}
        .book-btn {{ display: inline-block; background: linear-gradient(135deg, #c9a55c 0%, #a88a44 100%); color: #152a45; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 18px; margin: 10px 0; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Here's What You Missed</h1>
        </div>
        <div class="content">
            <p>Hi {first_name},</p>
            <p>We missed you at the <strong>FERS Retirement Workshop</strong>! Life happens -- no worries at all.</p>
            <p>Here's a quick summary of what was covered:</p>

            <div class="topics">
                <ol>
                    <li><strong>FERS Pension Optimization</strong> — We walked through how your High-3 salary, years of service, and retirement age interact. Most attendees were surprised to learn their pension could be worth over $1M in lifetime payments.</li>
                    <li><strong>TSP Withdrawal Strategies</strong> — We covered the tax implications of different withdrawal orders and how timing your TSP distributions with Social Security can save thousands.</li>
                    <li><strong>FEHB + Medicare Coordination</strong> — We explained the critical deadlines around age 65 for keeping federal health benefits alongside Medicare. Missing these can be costly.</li>
                </ol>
            </div>

            <p>The good news: we run these workshops regularly, and you're welcome to join the next one.</p>

            <div class="cta-box">
                <a href="https://planwellfp.com/book-call" class="book-btn">Book a Free Call</a>
                <br>{next_webinar_btn}
            </div>

            <p>Best,<br>The PlanWell Team</p>
        </div>
        <div class="footer">
            <p>PlanWell Financial Planning | planwellfp.com</p>
        </div>
    </div>
</body>
</html>
"""

    return send_email(to_email, subject, plain_body, html_body)


def send_noshow_day5_next_webinar(to_email: str, first_name: str,
                                   next_webinar_date: str, registration_url: str) -> bool:
    """
    Day 5 no-show: Invite to next upcoming webinar.
    """
    subject = f"Next FERS Workshop: {next_webinar_date}"

    plain_body = f"""Hi {first_name},

We know the last workshop didn't work out with your schedule. Good news -- the next one is coming up on {next_webinar_date}.

FERS Retirement Workshop
Date: {next_webinar_date}
Time: 11:00 AM - 2:00 PM EST
Location: Online via Zoom

What attendees are saying:
"I learned more in 3 hours than in 20 years of benefits briefings." -- Recent attendee

Register here: {registration_url}

Spots are limited to keep the Q&A interactive, so grab yours early.

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
        .testimonial {{ background: #e8f4f8; padding: 20px; border-radius: 8px; margin: 20px 0; font-style: italic; }}
        .register-btn {{ display: inline-block; background: linear-gradient(135deg, #c9a55c 0%, #a88a44 100%); color: #152a45; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 18px; margin: 10px 0; }}
        .note {{ background: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; text-align: center; }}
        .footer {{ text-align: center; padding: 20px; color: #666; font-size: 14px; background: #f8f9fa; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Next Workshop: {next_webinar_date}</h1>
        </div>
        <div class="content">
            <p>Hi {first_name},</p>
            <p>We know the last workshop didn't work out with your schedule. Good news -- the next one is coming up.</p>

            <div class="details-box">
                <p><strong>FERS Retirement Workshop</strong></p>
                <p><strong>Date:</strong> {next_webinar_date}</p>
                <p><strong>Time:</strong> 11:00 AM - 2:00 PM EST</p>
                <p><strong>Location:</strong> Online via Zoom</p>
            </div>

            <div class="testimonial">
                "I learned more in 3 hours than in 20 years of benefits briefings."
                <br><span style="font-style: normal; color: #666;">-- Recent attendee</span>
            </div>

            <p style="text-align: center;">
                <a href="{registration_url}" class="register-btn">Register for {next_webinar_date}</a>
            </p>

            <div class="note">
                <strong>Spots are limited</strong> to keep the Q&A interactive. Grab yours early.
            </div>

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
