export interface GuideSection {
  heading: string;
  html: string;
}

export interface GuideDecisionPoint {
  scenario: string;
  recommendation: string;
}

export interface DecisionGuide {
  slug: string;
  title: string;
  metaTitle: string;
  metaDescription: string;
  heroEyebrow: string;
  heroHeading: string;
  heroLead: string;
  tldr: string;
  sections: GuideSection[];
  decisionMatrix?: GuideDecisionPoint[];
  relatedCalculator?: { label: string; href: string };
  relatedGuideSlugs?: string[];
  faq: { q: string; a: string }[];
}

export const decisionGuides: DecisionGuide[] = [
  {
    slug: 'mra-10-vs-mra-30',
    title: 'FERS MRA+10 vs MRA+30: Which Retirement Path Fits You?',
    metaTitle: 'FERS MRA+10 vs MRA+30 Retirement | PlanWell',
    metaDescription: 'MRA+10 lets you retire with 10 years of service at your Minimum Retirement Age , but the penalty is steep. Here is the full comparison with real dollar scenarios.',
    heroEyebrow: 'Decision Guide',
    heroHeading: 'FERS MRA+10 vs MRA+30: Which Retirement Path Fits You?',
    heroLead: 'You have hit your Minimum Retirement Age and you have options. The MRA+10 path lets you retire now , at a permanent cost. The MRA+30 path means waiting, but the math is dramatically different. Here is how to choose.',
    tldr: 'MRA+10 slashes your annuity by 5% per year you are under 62. For most feds with 25-29 years of service, postponing retirement until the penalty disappears is worth the wait , but not always.',
    sections: [
      {
        heading: 'What MRA Actually Means',
        html: `<p>Your Minimum Retirement Age depends on your birth year. If you were born between 1953 and 1964, your MRA is 56. Born in 1970 or later, it is 57. This is the earliest age you can retire under FERS with any immediate annuity.</p>
<p>There are three main retirement paths available at or after MRA. The most commonly confused are MRA+10 (retire at MRA with at least 10 years of creditable service) and the more common "voluntary" retirement with 30 years at MRA, or 20 years at age 60, or 5 years at age 62. The MRA+30 label is shorthand for reaching MRA with 30+ years.</p>
<p>The difference in lifetime income between these two paths can exceed $200,000 for a mid-career fed , and that gap is often permanent.</p>`,
      },
      {
        heading: 'The MRA+10 Penalty: How Bad Is It?',
        html: `<p>If you retire under MRA+10, your FERS annuity is reduced by 5% for every year you are under age 62 at retirement. That reduction is permanent , it does not go away when you turn 62.</p>
<p>Say you retire at 57 with 15 years of service. You are 5 years under 62, so your annuity is cut by 25%. If your unreduced annuity would be $24,000 per year (roughly $2,000/month), you instead receive $18,000 per year , forever.</p>
<p>There is one workaround: the postponed retirement option. Under MRA+10, you can separate from service now, suspend your annuity, and elect to start it later , at a reduced age-based penalty. If you postpone to age 62, you receive the full amount with no reduction. Postpone to 60? You are 2 years under, so the cut is only 10%. This is a powerful tool most feds do not know about.</p>
<p>FEHB and FEGLI do NOT continue during a postponed retirement period. You must find your own coverage in the gap years, which can cost $600-$1,200 per month for a federal employee family used to FEHB premiums.</p>`,
      },
      {
        heading: 'MRA+30: The Clean Exit',
        html: `<p>If you reach MRA with 30 or more years of creditable service, you get an immediate, unreduced annuity. There is no age penalty. Your FERS Supplement also kicks in immediately and runs until you turn 62, adding roughly $800-$1,500 per month for most feds depending on your Social Security earnings history.</p>
<p>Consider two feds with identical salaries and a high-3 of $90,000. Fed A retires at MRA+10 at age 57 with 15 years of service. Annual annuity before penalty: 15 years x 1.0% x $90,000 = $13,500. After the 25% penalty: $10,125 per year. Fed B waits until 57 with 30 years. Annual annuity: 30 x 1.0% x $90,000 = $27,000, with no penalty and the full Supplement on top.</p>
<p>The difference is $16,875 per year , before the Supplement. Over a 25-year retirement, that gap exceeds $420,000 in nominal dollars. The math almost always favors the longer career.</p>`,
      },
      {
        heading: 'When MRA+10 Actually Makes Sense',
        html: `<p>There are real situations where MRA+10 is the right call. If you have a health condition that meaningfully shortens your expected retirement horizon, taking a reduced annuity now beats a larger annuity you may not live long enough to collect. A CFP or ChFEBC can help you run break-even age calculations for your specific situation.</p>
<p>Career changers who entered federal service later in life and hit their MRA with 10-15 years might find that private-sector income more than offsets the annuity reduction during a postponed period. But be careful: this only works if you actually have high private-sector earning power and solid health coverage.</p>
<p>If you are fleeing an agency reorganization, a toxic workplace, or a position being eliminated, MRA+10 with postponed retirement can let you separate cleanly and still land the unreduced annuity at 62. The key is carrying private health coverage for the gap years and maintaining the discipline not to start the annuity early.</p>`,
      },
      {
        heading: 'Special Provisions: Different Rules Apply',
        html: `<p>If you are a law enforcement officer, firefighter, or air traffic controller, MRA+10 is not your relevant path. Special provision employees can retire at 50 with 20 years of covered service, or at any age with 25 years, with no age reduction. Their accrual rate is 1.7% for the first 20 years of covered service , significantly richer than the standard 1.0%.</p>
<p>A federal law enforcement officer with 25 years of covered service and a high-3 of $100,000 retires with (20 x 1.7% x $100,000) + (5 x 1.0% x $100,000) = $39,000/year , before any Supplement. The standard-provision comparison does not apply to you if you are in this group.</p>`,
      },
      {
        heading: 'Important Disclaimers',
        html: `<p><em>This content is educational and general in nature. It is not tax, legal, or investment advice for your specific situation. Rules for FERS, TSP, Social Security, Medicare, and tax treatment change and can depend on factors unique to you. Consult a qualified tax professional, attorney, or CFP professional before acting on any of the strategies discussed here. PlanWell Financial Planning, LLC is not affiliated with or endorsed by OPM, the U.S. Office of Personnel Management, or any federal agency.</em></p>`
      }
    ],
    decisionMatrix: [
      {
        scenario: 'You are 57, have 10-19 years of service, and good health',
        recommendation: 'Strongly consider postponed retirement: separate now, defer the annuity start to 62, and avoid the permanent reduction. Line up private health coverage for the gap.',
      },
      {
        scenario: 'You are 57, have 30+ years of service',
        recommendation: 'MRA+30 immediate retirement: take the unreduced annuity plus the FERS Supplement now. No reason to use MRA+10.',
      },
      {
        scenario: 'You are 57, have 25-29 years of service, and plan to keep working',
        recommendation: 'Work the additional years to reach 30 if possible. The annuity jump from year 25 to 30 is roughly $4,500-$6,000 per year in additional lifetime income for a $90k high-3.',
      },
      {
        scenario: 'You are 57, have 10-15 years of service, and have a serious health condition',
        recommendation: 'MRA+10 with immediate annuity may beat waiting. Run a break-even analysis: if your life expectancy is under 75, the present value of the earlier, reduced annuity often wins.',
      },
      {
        scenario: 'You are 55, have 20 years of service, and your agency is offering VERA',
        recommendation: 'VERA changes the math. With VERA, you can retire at 55 as if you met the age requirement. Compare the annuity at 55+20 vs waiting to 57+22 , the Supplement access and earlier start often tip the scale.',
      },
    ],
    relatedCalculator: { label: 'Estimate your FERS annuity', href: '/fers-retirement-calculator' },
    relatedGuideSlugs: ['vera-vsip-explained', 'when-should-federal-employees-retire', 'deferred-vs-postponed-retirement'],
    faq: [
      {
        q: 'Can I avoid the MRA+10 penalty entirely?',
        a: 'Yes, through postponed retirement. If you separate under MRA+10 but do not start your annuity until age 62, the reduction disappears. Between 60 and 62 the penalty is 10% (2 years x 5%). You give up FEHB and FEGLI during the postponement period.',
      },
      {
        q: 'Does the FERS Supplement apply to MRA+10 retirees?',
        a: 'Only if you retire with an immediate, unreduced annuity. MRA+10 retirees who take the immediate reduced annuity receive no Supplement. Postponed retirement retirees who delay to 62 also receive no Supplement (it ends at 62 anyway for everyone).',
      },
      {
        q: 'If I take MRA+10 now, can I later change my mind and repay the annuity?',
        a: 'No. Once you elect an immediate annuity under MRA+10, the reduction is permanent. You cannot retroactively switch to postponed retirement. This decision requires getting the math right before you separate.',
      },
      {
        q: 'How do I calculate my MRA?',
        a: 'If you were born before 1948, your MRA is 55. It scales up by two months per birth year from 1948 through 1952, landing at 56 for those born 1953-1964. It scales up again from 1965 to 1969, reaching 57 for everyone born 1970 or later.',
      },
      {
        q: 'What counts as creditable service for MRA+10?',
        a: 'Most civilian federal service, active-duty military service for which you have made a deposit, and certain Peace Corps and VISTA service. Unused sick leave counts toward the annuity computation but not toward the 10-year minimum for MRA+10 eligibility.',
      },
      {
        q: 'Can part-time service count toward MRA+10?',
        a: 'Part-time FERS service counts toward the 10-year minimum, but your annuity is prorated for the part-time periods. A year at 50% time counts as one year of service for eligibility but as half a year for annuity computation.',
      },
    ],
  },

  {
    slug: 'csrs-vs-fers',
    title: 'CSRS vs FERS: What\'s the Real Difference?',
    metaTitle: 'CSRS vs FERS Comparison | PlanWell Federal Retirement',
    metaDescription: 'CSRS and FERS are not interchangeable. The annuity formulas, Social Security coverage, and TSP matching are completely different. Here is the real comparison with dollar amounts.',
    heroEyebrow: 'Decision Guide',
    heroHeading: 'CSRS vs FERS: What\'s the Real Difference?',
    heroLead: 'Most feds hired after 1987 are under FERS, but CSRS employees are still retiring today , and the two systems have almost nothing in common. If you are CSRS or thinking about what you gave up by being FERS, this guide runs the real numbers.',
    tldr: 'CSRS pays a much richer annuity formula (up to 80% of high-3) but you pay more into it and get no Social Security or TSP matching. FERS pays less from the pension but adds Social Security, TSP matching, and the FERS Supplement.',
    sections: [
      {
        heading: 'Who Is Still Under CSRS?',
        html: `<p>CSRS was closed to new employees after December 31, 1983. Anyone hired (or rehired without a break in service) after that date is under FERS. If you started federal service before 1984 and have been continuously covered, you are likely still CSRS or CSRS Offset.</p>
<p>CSRS Offset is a hybrid: you are covered by CSRS but also paid Social Security taxes on earnings from 1984 onward. When you retire, your CSRS annuity is offset (reduced) by the Social Security benefit you earned from federal service. Many feds in this category do not realize they are offset until they see their first Social Security statement.</p>
<p>As of April 2026, roughly 50,000 CSRS employees remain in the workforce, concentrated in longer-tenured positions at agencies like State, VA, and DoD. If you are one of them, your retirement planning is materially different from FERS.</p>`,
      },
      {
        heading: 'The Annuity Formula: Where CSRS Wins',
        html: `<p>CSRS uses a tiered formula: 1.5% per year for the first 5 years, 1.75% per year for years 6-10, and 2.0% per year for every year after 10. The maximum benefit is 80% of your high-3, reached at around 41.5 years of service.</p>
<p>A CSRS employee with 35 years of service and a high-3 of $95,000 receives: (5 x 1.5%) + (5 x 1.75%) + (25 x 2.0%) = 7.5% + 8.75% + 50% = 66.25% of $95,000 = $62,937 per year, or $5,245 per month.</p>
<p>The equivalent FERS calculation for 35 years at the standard 1.0% rate: 35 x 1.0% x $95,000 = $33,250 per year. If you qualify for the 1.1% rate (age 62+ with 20+ years), it would be $36,575. CSRS pays nearly double the pension for the same career length.</p>
<p>CSRS annuities receive full COLA every year, tied to CPI. FERS annuities are capped at CPI-1% when inflation is above 3%, and capped at 2% when CPI is between 2% and 3%. Over a 25-year retirement with average 3% inflation, CSRS retirees come out meaningfully ahead on COLA alone.</p>`,
      },
      {
        heading: 'Where FERS Closes the Gap',
        html: `<p>FERS was designed with the "three-legged stool" in mind: pension + Social Security + TSP. CSRS employees do not pay Social Security taxes on federal earnings and generally do not qualify for Social Security from their federal career. If they have enough outside employment to qualify, they may receive Social Security from those non-federal earnings. Before January 2025, the Windfall Elimination Provision (WEP) reduced those benefits by up to $587/month, and the Government Pension Offset (GPO) could reduce spousal benefits. The Social Security Fairness Act, signed January 5, 2025 (Public Law 118-273), repealed both WEP and GPO for all benefits payable after December 2023. CSRS retirees' Social Security from outside employment is no longer reduced by WEP.</p>
<p>TSP matching is the biggest FERS advantage in accumulation. Under FERS, OPM automatically contributes 1% of your salary to TSP even if you contribute nothing. If you contribute at least 5%, you get a total of 5% from the government (1% automatic + 4% match). On a $90,000 salary, that is $4,500 per year in free money. CSRS employees receive no matching contributions.</p>
<p>The FERS Supplement bridges the gap between early retirement and Social Security eligibility. A FERS employee who retires at 57 with 30 years can receive $1,200/month from the Supplement until age 62 , that is $72,000 in additional income the CSRS employee does not receive (because they are not covered by Social Security).</p>`,
      },
      {
        heading: 'Employee Contributions: What You Pay',
        html: `<p>CSRS employees contribute 7% of base pay toward their annuity. CSRS Offset employees pay 0.8% (the rest flows to Social Security). FERS employees hired before 2013 pay 0.8%; those hired in 2013 pay 3.1%; those hired in 2014 and later pay 4.4%. The contribution rate does not affect your annuity amount.</p>
<p>A CSRS employee earning $90,000 contributes $6,300 per year to the retirement fund. A newer FERS employee at the same salary contributes $3,960 (4.4%). The FERS employee keeps $2,340 more per year to invest in TSP , and gets matching on top of it. The net cash position during the career is better under FERS for employees who use the TSP.</p>`,
      },
      {
        heading: 'Which System Produces More Lifetime Income?',
        html: `<p>For high-career, long-tenure employees, CSRS usually wins on total lifetime income from the pension alone , especially when COLA compounding is factored in. A CSRS retiree with 40 years of service and a $100,000 high-3 retires with roughly $80,000 per year growing with full CPI. A FERS employee with the same high-3 and career gets about $44,000 in pension but adds Social Security ($18,000-$28,000 per year) and whatever TSP accumulation they have built.</p>
<p>When Social Security and TSP are included, FERS employees with disciplined TSP saving often match or exceed CSRS total income. The key variable is TSP balance: a FERS employee who contributed 15% for 30 years and captured all matching has a TSP balance of $600,000-$900,000 at retirement, generating $24,000-$36,000 per year in sustainable withdrawals. That stacks on top of the FERS pension.</p>
<p>Our team at PlanWell runs this analysis side by side for clients who want the full picture. The answer depends on your salary history, expected Social Security benefit, TSP balance, and life expectancy.</p>`,
      },
      {
        heading: 'Important Disclaimers',
        html: `<p><em>This content is educational and general in nature. It is not tax, legal, or investment advice for your specific situation. Rules for FERS, TSP, Social Security, Medicare, and tax treatment change and can depend on factors unique to you. Consult a qualified tax professional, attorney, or CFP professional before acting on any of the strategies discussed here. PlanWell Financial Planning, LLC is not affiliated with or endorsed by OPM, the U.S. Office of Personnel Management, or any federal agency.</em></p>`
      }
    ],
    decisionMatrix: [
      {
        scenario: 'You are CSRS with 35+ years and approaching retirement',
        recommendation: 'Your annuity will be rich , focus on survivor benefit election, FEHB continuation, and managing any remaining CSRS considerations for outside Social Security earnings. Note: WEP and GPO were repealed by the Social Security Fairness Act (January 5, 2025) and no longer reduce CSRS retirees\' Social Security benefits from non-federal employment.',
      },
      {
        scenario: 'You are CSRS with under 5 years and considering leaving',
        recommendation: 'You can withdraw your contributions (with interest) or leave them and receive a deferred annuity at 62. A withdrawal forfeits all future benefits. Model both options before separating.',
      },
      {
        scenario: 'You are FERS and envious of CSRS annuity levels',
        recommendation: 'Close the gap with aggressive TSP saving. Contributing 15%+ and capturing all matching can produce $700,000-$1,000,000 in TSP by retirement. Combined with Social Security, your total retirement income can match or exceed a CSRS peer.',
      },
    ],
    relatedCalculator: { label: 'Estimate your FERS annuity', href: '/fers-retirement-calculator' },
    relatedGuideSlugs: ['when-should-federal-employees-retire', 'survivor-benefit-election-guide'],
    faq: [
      {
        q: 'Can I switch from CSRS to FERS?',
        a: 'OPM has periodically offered CSRS employees the option to transfer to FERS, but those windows have long closed. You cannot voluntarily transfer today. You are locked into whichever system covers you.',
      },
      {
        q: 'What happens to my CSRS if I leave before retirement eligibility?',
        a: 'You can request a refund of your contributions (plus interest), which forfeits all future annuity rights. Alternatively, you can leave the contributions in the fund and collect a deferred annuity at age 62 with at least 5 years of creditable service.',
      },
      {
        q: 'Does CSRS cover survivors the same way FERS does?',
        a: 'CSRS survivor annuity elections work similarly: you can elect a full survivor annuity (55% of your annuity to a spouse) or a partial amount, at a cost to your own annuity. The survivor benefit formula differs slightly but the concept is the same.',
      },
      {
        q: 'What was the Windfall Elimination Provision and does it still apply?',
        a: 'WEP historically reduced Social Security benefits for people who received a pension from non-covered employment (like CSRS), by up to $587/month. However, the Social Security Fairness Act (Public Law 118-273), signed January 5, 2025, repealed WEP and the related Government Pension Offset (GPO) for all benefits payable after December 2023. CSRS retirees who also have Social Security from outside employment now receive those benefits without the WEP reduction. FERS employees were never affected by WEP because they paid Social Security taxes throughout their federal career.',
      },
      {
        q: 'Is the CSRS annuity really COLA-protected every year?',
        a: 'Yes. CSRS COLAs match CPI-W without any cap. In high-inflation years like 2022 (when COLA was 5.9%) and 2023 (8.7%), CSRS retirees received the full amount. FERS retirees received CPI minus 1 percentage point in those years.',
      },
    ],
  },

  {
    slug: 'deferred-vs-postponed-retirement',
    title: 'Deferred vs Postponed Retirement Under FERS',
    metaTitle: 'FERS Deferred vs Postponed Retirement | PlanWell',
    metaDescription: 'Deferred and postponed retirement are not the same under FERS. One preserves FEHB; the other does not. One removes the age penalty; the other is for those who left federal service entirely.',
    heroEyebrow: 'Decision Guide',
    heroHeading: 'Deferred vs Postponed Retirement Under FERS',
    heroLead: 'If you leave federal service before meeting your retirement requirements, you have two options for your pension: deferred or postponed. They sound similar but the rules, benefits, and costs are completely different.',
    tldr: 'Postponed retirement is for MRA+10 employees who separate and delay their annuity start to reduce or eliminate the age penalty. Deferred retirement is for anyone who leaves before meeting MRA+10 requirements and waits until the minimum age to collect. Postponed preserves the option to restart FEHB; deferred does not.',
    sections: [
      {
        heading: 'Who Qualifies for Each Path',
        html: `<p>Postponed retirement requires that you separate at or after your MRA with at least 10 years of creditable service (the MRA+10 standard). You choose to delay starting your annuity beyond your separation date to reduce or eliminate the 5%-per-year age penalty.</p>
<p>Deferred retirement applies when you separate from service before reaching MRA+10 eligibility. You must have at least 5 years of creditable civilian service. The annuity starts at age 62 regardless of when you separated, and it is not reduced by any age penalty.</p>
<p>The practical difference: an employee who leaves at age 50 with 20 years of service cannot use postponed retirement (not yet MRA). They use deferred retirement, collect at 62, and forgo 12 years of annuity income they would have received under a normal retirement scenario. No FERS Supplement. No FEHB continuation.</p>`,
      },
      {
        heading: 'FEHB Coverage: The Critical Difference',
        html: `<p>This is the issue that catches feds off guard. Under postponed retirement, you can reenroll in FEHB when your annuity starts. The gap period (between separation and annuity start) requires you to cover yourself with other insurance , COBRA for up to 18 months or a marketplace plan. But when the annuity begins, FEHB returns.</p>
<p>Under deferred retirement, FEHB does not come back. Period. If you separated at 50 and your annuity starts at 62, you have 12 years to find your own health coverage (COBRA for 18 months, then marketplace or a spouse's plan). At 62, you cannot reenroll in FEHB through OPM. You would need Medicare at 65 without any FEHB to supplement it.</p>
<p>For a fed used to paying $200-$400/month in FEHB premiums with robust coverage, the lifetime healthcare cost of deferred retirement is staggering. Marketplace plans for a 55-year-old can run $800-$1,500/month before subsidies. This is often the deciding factor in whether to leave early.</p>`,
      },
      {
        heading: 'FEGLI: Similarly Important',
        html: `<p>Under both deferred and postponed retirement, FEGLI does not continue during the separation period. You lose your federal life insurance coverage when you separate, regardless of which path you take. If you restart an annuity under postponed retirement, you can reenroll in FEGLI at that point , but you will pay older-age premiums. Under deferred retirement, FEGLI does not resume at age 62.</p>
<p>Many feds who plan an early exit underestimate the value of their FEGLI Basic benefit. At retirement under a normal annuity, Basic FEGLI reduces to 25% of face value with no cost , a meaningful benefit for survivors. That path is not available to deferred retirees.</p>`,
      },
      {
        heading: 'The Annuity Calculation Under Each Path',
        html: `<p>Both paths use the same underlying formula: years of creditable service x 1.0% x high-3 average salary. But your high-3 is locked at the date you separate , it does not grow with inflation while you wait for your annuity to start.</p>
<p>Someone who separates at age 50 with a high-3 of $80,000 and 20 years of service has an annual annuity of $16,000. That amount does not adjust for inflation between separation and age 62. In 12 years at 3% average inflation, $16,000 has the purchasing power of about $11,200 in today's dollars.</p>
<p>Under postponed retirement (MRA+10), the same calculation applies, but if you delay starting until age 62 you eliminate the 5%-per-year age penalty. If you had separated at 57 with 12 years, your unreduced annuity would be $10,800. Starting it at 62 instead of 57 saves you the 25% penalty, netting you $10,800 instead of $8,100 per year.</p>`,
      },
      {
        heading: 'Which Path Should You Take?',
        html: `<p>If you have reached MRA with at least 10 years, postponed retirement is almost always preferable to deferred. You preserve the FEHB reenrollment option, and you can time your annuity start to minimize or eliminate the age reduction.</p>
<p>Deferred retirement is sometimes unavoidable , if you separate before MRA, you have no other option for keeping your FERS benefit alive other than a contribution refund (which terminates all rights). In that case, think carefully about the healthcare gap and whether your post-federal income stream bridges it.</p>
<p>For feds considering leaving in their late 40s or early 50s for private-sector opportunities, the deferred retirement path is often modeled as a bonus payment at age 62 rather than a retirement income strategy. That framing is more accurate: $16,000 per year at 62 is a supplement to a private-sector career, not a retirement foundation.</p>`,
      },
      {
        heading: 'Important Disclaimers',
        html: `<p><em>This content is educational and general in nature. It is not tax, legal, or investment advice for your specific situation. Rules for FERS, TSP, Social Security, Medicare, and tax treatment change and can depend on factors unique to you. Consult a qualified tax professional, attorney, or CFP professional before acting on any of the strategies discussed here. PlanWell Financial Planning, LLC is not affiliated with or endorsed by OPM, the U.S. Office of Personnel Management, or any federal agency.</em></p>`
      }
    ],
    decisionMatrix: [
      {
        scenario: 'You are 57 at MRA with 12 years of service, separating for a private job',
        recommendation: 'Use postponed retirement. Delay your annuity to 62 and eliminate the full 25% penalty. Line up marketplace health coverage for 5 years.',
      },
      {
        scenario: 'You are 50 with 20 years of service, considering leaving',
        recommendation: 'You cannot use postponed retirement. Deferred retirement locks in your current high-3 and annuity without inflation adjustment. Model whether the private-sector income and 401k matching outweighs the FEHB loss and frozen annuity.',
      },
      {
        scenario: 'You are 55 with 8 years of service, separating involuntarily',
        recommendation: 'You have 5+ years so you qualify for deferred retirement at 62. The annuity will be small (roughly 8% of high-3) but real. Leave your contributions in the fund; do not take a refund.',
      },
      {
        scenario: 'You are 58 at MRA with 22 years, your spouse has employer health coverage',
        recommendation: 'Postponed retirement becomes much more attractive when health coverage is solved through a spouse. Delay to 60 (10% penalty) or 62 (no penalty) depending on your income needs.',
      },
    ],
    relatedCalculator: { label: 'Estimate your FERS annuity', href: '/fers-retirement-calculator' },
    relatedGuideSlugs: ['mra-10-vs-mra-30', 'when-should-federal-employees-retire', 'fehb-to-medicare-transition'],
    faq: [
      {
        q: 'Can I change my mind after electing postponed retirement and start the annuity early?',
        a: 'Yes. Under postponed retirement you can start your annuity at any time after separation, but the age reduction applies to how old you are when you start. Starting at 59 with an MRA of 57 means a 15% reduction (3 years x 5%). You are not locked in to waiting until 62.',
      },
      {
        q: 'Does deferred retirement include the FERS Supplement?',
        a: 'No. The FERS Supplement is only available to employees who retire with an immediate annuity (including postponed retirement once the annuity starts before 62 in some cases). Deferred retirees who start collecting at 62 get the pension only.',
      },
      {
        q: 'What happens to my TSP if I take deferred or postponed retirement?',
        a: 'TSP is separate from your pension. You can leave your TSP invested and withdraw from it independently of your annuity start date. TSP does not require you to start withdrawals until age 73 (IRS Required Minimum Distribution rules apply).',
      },
      {
        q: 'If I take a refund of my FERS contributions, can I redeposit them later?',
        a: 'Yes, if you return to federal service. You can redeposit the refunded amount with interest to restore the creditable service. If you never return, the refund permanently forfeits those years for annuity purposes.',
      },
      {
        q: 'How long does OPM take to process a deferred retirement at age 62?',
        a: 'OPM typically takes 60-90 days to process deferred retirement applications. Submit your application at least 3-4 months before your 62nd birthday to avoid a gap in income. OPM pays retroactively once processing completes, but the cash flow delay can be disruptive.',
      },
    ],
  },

  {
    slug: 'divorce-and-fers',
    title: 'Divorce and Your FERS Pension: What You Need to Know',
    metaTitle: 'Divorce and FERS Pension Division | PlanWell Federal Retirement',
    metaDescription: 'Divorce can split your FERS annuity, TSP balance, and survivor benefits. Understanding how court orders interact with OPM rules is the difference between a clean settlement and years of complications.',
    heroEyebrow: 'Decision Guide',
    heroHeading: 'Divorce and Your FERS Pension: What You Need to Know',
    heroLead: 'Your FERS annuity and TSP are marital assets in most states. A divorce settlement that does not account for the OPM court order rules can leave both parties worse off than necessary. Here is how the system actually works.',
    tldr: 'FERS benefits split through court orders that OPM must honor. The pension requires a "court order acceptable for processing" (COAP). TSP splits through a retirement benefits court order (RBCO). Get both wrong and the intended division does not happen.',
    sections: [
      {
        heading: 'What Is Actually Divisible at Divorce',
        html: `<p><strong>Important:</strong> FERS pension division involves specialized federal rules that most family law attorneys are unfamiliar with. Work with a family law attorney experienced in federal retirement benefits before finalizing any divorce settlement or court order.</p>
<p>Three FERS-related assets are typically subject to division at divorce: the FERS annuity itself, the TSP balance, and the survivor benefit election. Each has separate rules and separate court order requirements. Lumping them into one vague "you get half my retirement" clause in a settlement agreement is a recipe for litigation years later.</p>
<p>Your FERS annuity can be divided through a court order that OPM accepts and implements. Your TSP balance (including contributions made during the marriage and their earnings) can be divided through a retirement benefits court order that TSP honors. The survivor benefit , the right to receive a portion of your annuity after you die , can be assigned to a former spouse through a court order or negotiated separately during divorce.</p>
<p>Each of these is independent. You can give your former spouse a share of the TSP without touching the pension. You can assign survivor benefits without splitting the annuity. Or you can structure the settlement to trade one for another , many couples negotiate TSP for pension or vice versa, depending on ages and expected timelines.</p>`,
      },
      {
        heading: 'The Court Order Acceptable for Processing (COAP)',
        html: `<p>OPM will not honor just any divorce decree that mentions the pension. It requires a specific document , a court order acceptable for processing , that meets OPM's requirements. If the COAP does not meet those requirements, OPM will reject it and the former spouse receives nothing from the annuity, regardless of what the divorce agreement says.</p>
<p>A COAP can award a former spouse a fixed dollar amount per month, a percentage of the annuity, or a formula based on service during the marriage. The order cannot give the former spouse more than the employee's own share. And it must be submitted to OPM before the employee retires, or at retirement at the latest.</p>
<p>OPM has a model COAP language available on its website. Divorcing feds should ensure their attorney uses language OPM will accept, not generic marital property order language. The consequences of a rejected COAP are severe: the former spouse has no claim against OPM even if they have a valid court order against you.</p>`,
      },
      {
        heading: 'Splitting the TSP Through an RBCO',
        html: `<p>TSP requires a retirement benefits court order to divide the account. The RBCO must specify whether the award is a fixed dollar amount or a percentage, and whether earnings since the cutoff date are included. TSP processes RBCOs and, if accepted, establishes a separate TSP account for the former spouse , who then manages that account independently.</p>
<p>Importantly, TSP does not allow loans against the awarded share, and the former spouse cannot keep the funds in TSP long-term unless they meet eligibility requirements. Most former spouses roll the RBCO award into an IRA. The transfer is not a taxable event when done correctly.</p>
<p>A TSP balance of $450,000 divided 50/50 through an RBCO means each party leaves with $225,000 plus or minus any earnings since the valuation date specified in the order. If the order does not specify a valuation date clearly, disputes arise about which balance applies.</p>`,
      },
      {
        heading: 'Former Spouse Survivor Benefits: Protecting the Spouse After Retirement',
        html: `<p>If you divorce after retirement, your surviving spouse election generally defaults to the person you were married to at retirement. A former spouse can be awarded survivor benefits through a court order, but this requires timely filing with OPM. Miss the deadline and the former spouse loses that protection permanently.</p>
<p>Former spouse survivor benefit elections interact with any current spouse coverage. You cannot provide full survivor benefits to both a former spouse and a current spouse , the total cannot exceed the maximum election. Divorce settlements often fail to address this adequately, creating conflicts that surface decades later when the employee dies.</p>
<p>The cost of a survivor benefit is a permanent reduction to your annuity: a full survivor annuity for a spouse costs 10% of your annuity. If you are ordered to provide that to a former spouse, your take-home annuity drops by 10% for the rest of your life , even if your former spouse predeceases you (there is no recovery).</p>`,
      },
      {
        heading: 'FEHB Coverage for Former Spouses',
        html: `<p>A former spouse can continue FEHB coverage if the divorce decree awards it and the former spouse enrolls within 60 days of the divorce. The former spouse pays both the employee and the government share of premiums , which is significantly more expensive than the standard employee share. For 2025, a Self Plus One premium averages roughly $300-$500 per month for the employee share; the former spouse pays the full $700-$1,200 range.</p>
<p>This coverage continues until the former spouse remarries before age 55, becomes covered under another FEHB enrollment, or the coverage is terminated for non-payment. It does not continue if the employee dies while still employed , that triggers different rules around survivor benefits.</p>
<p>Former spouse FEHB is often overlooked in settlement negotiations. For a former spouse who is 55-62 and cannot get affordable marketplace coverage, this provision can be worth $50,000-$100,000 in healthcare cost savings before Medicare eligibility.</p>`,
      },
      {
        heading: 'Important Disclaimers',
        html: `<p><em>This content is educational and general in nature. It is not tax, legal, or investment advice for your specific situation. Rules for FERS, TSP, Social Security, Medicare, and tax treatment change and can depend on factors unique to you. Consult a qualified tax professional, attorney, or CFP professional before acting on any of the strategies discussed here. PlanWell Financial Planning, LLC is not affiliated with or endorsed by OPM, the U.S. Office of Personnel Management, or any federal agency.</em></p>`
      }
    ],
    decisionMatrix: [
      {
        scenario: 'You are the federal employee and your spouse wants 50% of your pension',
        recommendation: 'Insist on a COAP with OPM-accepted language. Do not agree to pension division in the settlement agreement without a parallel COAP already drafted and reviewed. The settlement agreement alone does not bind OPM.',
      },
      {
        scenario: 'You are the former spouse and you were awarded a share of the TSP',
        recommendation: 'File the RBCO with TSP immediately after divorce. There is no filing deadline per se, but the employee can spend down the TSP while you wait. TSP cannot restore funds disbursed before your RBCO is received.',
      },
      {
        scenario: 'You are divorcing after retirement and your pension is already paying',
        recommendation: 'Survivor benefits and any pension division must be handled through post-retirement court orders. OPM must receive the COAP. Former spouse survivor benefits require timely filing; the election is irrevocable once it ages out.',
      },
      {
        scenario: 'You have a young child and divorce involves custody considerations',
        recommendation: 'Child support can be withheld from a FERS annuity through a standard income withholding order. OPM will honor these orders. This is separate from the pension division question and does not require a COAP.',
      },
    ],
    relatedGuideSlugs: ['survivor-benefit-election-guide', 'when-should-federal-employees-retire'],
    faq: [
      {
        q: 'What if my divorce settlement mentions the pension but no COAP was ever filed?',
        a: 'If no COAP was filed with OPM, your former spouse has no claim against OPM , only against you personally. They would need to go back to the divorce court to enforce the settlement and compel you to comply. If you have already retired, this can be very difficult to remedy.',
      },
      {
        q: 'Can a former spouse receive both a share of the annuity and survivor benefits?',
        a: 'Yes. A COAP can award a share of the annuity while you are alive, and separately, a court order can award former spouse survivor benefits. These are two different benefits paid from two different pools, so both are possible simultaneously.',
      },
      {
        q: 'Does remarriage affect the former spouse survivor benefit?',
        a: 'If a former spouse remarries before age 55, any former spouse survivor annuity terminates immediately. If they remarry at 55 or older, the survivor benefit continues. This rule creates a strong financial disincentive to remarry before 55 for former spouses receiving this benefit.',
      },
      {
        q: 'What happens if I die before retiring and I have a COAP in place?',
        a: 'If you die before retirement and a COAP awards your former spouse survivor benefits, OPM will pay them a basic employee death benefit and a survivor annuity. The specifics depend on the language in the COAP , vague orders often produce unintended results.',
      },
      {
        q: 'Can my TSP beneficiary designation override a divorce agreement?',
        a: 'No. A valid RBCO awarding TSP funds to a former spouse supersedes a beneficiary designation for the covered portion. However, if the RBCO was never filed with TSP and you die with a new beneficiary named, the new beneficiary may receive the full balance. Filing the RBCO promptly protects the former spouse.',
      },
    ],
  },

  {
    slug: 'fers-disability-retirement',
    title: 'FERS Disability Retirement: A Step-by-Step Guide',
    metaTitle: 'FERS Disability Retirement Guide | PlanWell Federal Retirement',
    metaDescription: 'FERS disability retirement requires proving you cannot perform your current position , not that you are totally disabled. Here is the application process, the benefit formula, and the traps to avoid.',
    heroEyebrow: 'Decision Guide',
    heroHeading: 'FERS Disability Retirement: A Step-by-Step Guide',
    heroLead: 'FERS disability retirement is not the same as Social Security Disability Insurance. The eligibility standard, the benefit amount, and the process are all different. If a medical condition is ending your federal career, you need to understand this path before you decide anything.',
    tldr: 'To qualify, you must have 18 months of creditable service and a medical condition that prevents you from performing your current position , not total and permanent disability. The benefit is the greater of 40% of your high-3 or your earned annuity, for the first year.',
    sections: [
      {
        heading: 'Eligibility: What You Must Prove',
        html: `<p>FERS disability retirement requires three things: at least 18 months of creditable civilian service, a medical condition that is expected to last at least one year, and a showing that the condition prevents you from performing the essential functions of your current position. You do not need to be unable to work at all , just unable to do your specific job.</p>
<p>The agency must also demonstrate it cannot reasonably accommodate your condition. If your agency offers you a reassignment to a vacant position at the same grade and pay that you are medically able to perform, OPM may deny your disability application on the grounds that accommodation exists.</p>
<p>Medical documentation is the core of the application. OPM looks for treating physician statements, diagnostic records, and functional capacity evaluations. "I feel pain" is not enough. OPM needs clinical evidence that your condition functionally prevents job performance , specific limitations tied to specific essential functions of your position description.</p>`,
      },
      {
        heading: 'The Benefit Formula',
        html: `<p>FERS disability retirement pays a percentage of your high-3 based on your age and years of service at the time of disability. For the first 12 months of disability retirement, you receive the higher of: (a) 60% of your high-3, or (b) your earned annuity (years x 1.0% x high-3). Starting in the second year, the benefit drops to the higher of: (a) 40% of your high-3, or (b) your earned annuity.</p>
<p>For a fed with a high-3 of $85,000 and only 10 years of service: earned annuity = $8,500/year. 40% of high-3 = $34,000/year. The guaranteed minimum of $34,000 applies , a significant protection for employees who become disabled early in their careers.</p>
<p>At age 62, OPM recalculates your benefit as if you had continued working until 62. Your actual service plus the disability period counts as if it were creditable. This recomputation often produces a higher benefit than the 40% floor, and it becomes your permanent annuity going forward.</p>`,
      },
      {
        heading: 'Social Security Disability and the Offset',
        html: `<p>If you receive both FERS disability retirement and Social Security Disability Insurance, FERS reduces your benefit. In the first year, the SSDI offset reduces your 60% FERS benefit by 100% of any SSDI amount. In subsequent years, the 40% FERS benefit is reduced by 60% of SSDI. This can substantially reduce your net income if you receive both benefits.</p>
<p>Example: You receive $34,000/year from FERS disability retirement. You also receive $18,000/year from SSDI. The FERS offset: 60% of $18,000 = $10,800. Your FERS payment drops to $34,000 - $10,800 = $23,200. Combined, you receive $41,200 , better than either alone, but less than you might expect when adding the two numbers.</p>
<p>Filing for SSDI simultaneously with FERS disability is often recommended because approval of one can support the other. But coordinate your applications carefully , OPM and SSA have different processing timelines and different approval standards.</p>`,
      },
      {
        heading: 'The Application Process',
        html: `<p>The FERS disability retirement application is a multi-form package. You file SF-3107 (Application for Immediate Retirement) and SF-3112 (Documentation in Support of Disability Retirement) through your agency HR. Your agency completes its portion and forwards the package to OPM within 30 days.</p>
<p>OPM processing for disability cases typically takes 6-18 months. During that period, you remain on agency rolls if you have sick leave or annual leave to burn. Once leave is exhausted, you enter leave-without-pay status. FEHB continues during LWOP for up to one year, then you must self-pay premiums. OPM pays benefits retroactively to your separation date once approved.</p>
<p>If OPM denies your application, you can appeal to the Merit Systems Protection Board within 30 days. Many feds who are denied at the OPM level succeed on MSPB appeal when their medical evidence is stronger and better organized. Consider working with a federal employment attorney or ChFEBC for complex cases.</p>`,
      },
      {
        heading: 'What Happens to TSP and FEHB',
        html: `<p>TSP remains yours regardless of disability retirement , you can leave it invested, take withdrawals, or roll it over to an IRA. If you are under 59.5 at disability retirement, TSP withdrawals are exempt from the 10% early withdrawal penalty. You still owe ordinary income tax on withdrawals from the traditional (pre-tax) balance.</p>
<p>FEHB continues into disability retirement just as it does with regular retirement , you pay the employee share of premiums, and coverage continues for life as long as your annuity is active. FEGLI also continues, though the coverage reduces over time as it does for all retirees who elect the free Basic option.</p>`,
      },
      {
        heading: 'Important Disclaimers',
        html: `<p><em>This content is educational and general in nature. It is not tax, legal, or investment advice for your specific situation. Rules for FERS, TSP, Social Security, Medicare, and tax treatment change and can depend on factors unique to you. Consult a qualified tax professional, attorney, or CFP professional before acting on any of the strategies discussed here. PlanWell Financial Planning, LLC is not affiliated with or endorsed by OPM, the U.S. Office of Personnel Management, or any federal agency.</em></p>`
      }
    ],
    decisionMatrix: [
      {
        scenario: 'You have 5 years of service and a serious medical condition',
        recommendation: 'You do not meet the 18-month minimum (you exceed it). Apply. Your guaranteed minimum of 40% of high-3 is likely higher than your earned annuity at 5 years.',
      },
      {
        scenario: 'You have 30 years of service and a serious medical condition',
        recommendation: 'Compare your disability benefit to your earned voluntary retirement annuity. With 30 years and a good high-3, your earned annuity may exceed the 40% floor , making the disability benefit similar to or less than early voluntary retirement.',
      },
      {
        scenario: 'You have 20 years of service and your condition qualifies for SSDI',
        recommendation: 'Apply for both FERS disability and SSDI simultaneously. Understand the offset formula before projecting your combined income. The offset reduces FERS, but the combined amount typically exceeds FERS alone.',
      },
    ],
    relatedCalculator: { label: 'Estimate your FERS annuity', href: '/fers-retirement-calculator' },
    relatedGuideSlugs: ['when-should-federal-employees-retire', 'fehb-to-medicare-transition'],
    faq: [
      {
        q: 'Can I work after receiving FERS disability retirement?',
        a: 'You can work, but OPM monitors your earnings. If your income from employment exceeds 80% of the current salary for your former position, your disability annuity may be terminated. OPM conducts periodic reviews and can require medical documentation to confirm your condition persists.',
      },
      {
        q: 'Does FERS disability retirement count for TSP matching purposes?',
        a: 'No. Once you separate and enter disability retirement, you are no longer an active employee and cannot contribute to TSP or receive matching contributions. Your TSP balance is frozen for investment growth only.',
      },
      {
        q: 'Is FERS disability retirement income taxable?',
        a: 'Yes, it is ordinary income for federal tax purposes. However, the portion attributable to your own after-tax contributions (which is typically a small amount) may be excluded. State tax treatment varies , some states exempt federal retirement income entirely.',
      },
      {
        q: 'What if I recover from my condition after being approved for disability retirement?',
        a: 'OPM conducts medical re-examinations, usually in the first few years. If you are found recovered, your disability retirement can be terminated. You would then need to find employment; you cannot simply return to your former federal position automatically.',
      },
      {
        q: 'How does the age-62 recomputation work?',
        a: 'At age 62, OPM recalculates your annuity using your actual years of creditable service PLUS the years you were on disability retirement (as if you had worked those years). It then applies the standard FERS formula: total years x 1.0% x high-3 (using the high-3 at the time of your original disability retirement, adjusted for COLA). This often increases your benefit significantly.',
      },
    ],
  },

  {
    slug: 'vera-vsip-explained',
    title: 'VERA and VSIP: Should You Take the Early Out?',
    metaTitle: 'VERA and VSIP Federal Early Retirement | PlanWell',
    metaDescription: 'VERA lets agencies offer early retirement to employees who do not yet meet normal requirements. VSIP adds a cash incentive. Here is how to decide if the offer is actually good.',
    heroEyebrow: 'Decision Guide',
    heroHeading: 'VERA and VSIP: Should You Take the Early Out?',
    heroLead: 'When your agency announces a VERA or VSIP window, the pressure to decide is intense and the timeline is short. This guide gives you the framework to evaluate the offer without panic.',
    tldr: 'VERA waives the normal age requirement for early retirement; VSIP adds a cash incentive up to $25,000 at most agencies (the DoD cap is $40,000 under the 2017 VSIP Adjustment Act; all other agencies remain at $25,000). Together they can be a genuinely good deal , or a trap if you need a few more years of service for a meaningfully higher annuity.',
    sections: [
      {
        heading: 'What VERA Is and Who Qualifies',
        html: `<p>A Voluntary Early Retirement Authority allows an agency to temporarily lower the age and service requirements for retirement. Under normal FERS rules, you need to be at least MRA with 30 years, or 60 with 20 years, or 62 with 5 years. Under an approved VERA, the agency can offer retirement to employees who are at least 50 with 20 years of service, or any age with 25 years of service.</p>
<p>VERA must be approved by OPM. Not every agency gets approval, and not every employee within an approved agency is eligible. VERA windows are targeted , they apply to specific organizational units, positions, or geographic locations. Your HR office will notify eligible employees directly.</p>
<p>Importantly, VERA is voluntary. The agency cannot force you out. If you receive a VERA offer and decline it, you retain your position (assuming no RIF follows). VSIP works differently , it is an incentive for voluntary separation, and rejecting VSIP may sometimes limit future VSIP eligibility at the same agency.</p>`,
      },
      {
        heading: 'The VSIP Cash Incentive',
        html: `<p>VSIP pays a lump sum , by law, the lesser of $25,000 or the amount of severance pay you would receive if involuntarily separated (the DoD cap is $40,000 under the 2017 VSIP Adjustment Act; all other agencies remain at $25,000). For most employees with 20+ years, the maximum applies. The payment is taxable as ordinary income in the year received.</p>
<p>At a 22% federal tax bracket, a $25,000 VSIP nets roughly $19,500 after federal tax. Add state income taxes and the net amount in a high-tax state could be $17,000-$18,000. That is still real money , but it is a one-time payment, not a lifetime annuity increment. Do not overweight it.</p>
<p>VSIP is not always tied to VERA. An agency can offer VSIP to employees who resign voluntarily (not just retire). In that case, the cash payment accompanies a resignation rather than a retirement. For FERS employees who plan to resign anyway, a VSIP window can be a windfall if timed correctly.</p>`,
      },
      {
        heading: 'The Annuity Math Under VERA',
        html: `<p>Your VERA annuity uses the same FERS formula as any other retirement: years of creditable service x 1.0% x high-3. There is no special penalty for VERA retirement , you are simply treated as if you met the age and service requirements. The annuity starts immediately.</p>
<p>The catch is the FERS Supplement. VERA retirees who are under MRA at retirement do not receive the Supplement immediately. The Supplement starts when they reach MRA. This can create a 2-5 year income gap depending on your age at VERA retirement.</p>
<p>Compare two feds with a high-3 of $88,000. Fed A retires under VERA at 50 with 20 years: annuity = $17,600/year ($1,467/month). Fed B waits until MRA (57) with 27 years: annuity = $23,760/year ($1,980/month), plus the Supplement of roughly $1,000/month immediately. The 7-year wait produces $513/month more in pension and $1,000/month more in Supplement , a $1,513/month improvement. At that rate, Fed B recovers the 7 years of additional working income within 15 years of retirement.</p>`,
      },
      {
        heading: 'What VERA Does NOT Include',
        html: `<p>VERA retirement does not waive the 5-year rule for FEHB continuity. You must have been enrolled in FEHB for the 5 years immediately preceding retirement (or since your first opportunity to enroll) to carry FEHB into retirement. If you have not met this requirement, you lose FEHB coverage at retirement , a significant liability.</p>
<p>FEGLI continues into VERA retirement under the same rules as any retirement. However, if you retire at 50, you are paying full premiums for Option A and B/C coverages for many more years before age-based free reductions kick in. Budget for this.</p>
<p>Unused sick leave adds to your annuity computation under VERA just as it does under regular retirement. If you have 2,000 hours of sick leave, that adds roughly 11.5 months to your creditable service , worth about $840/year for a fed with an $88,000 high-3. It is not huge, but it is real.</p>`,
      },
      {
        heading: 'How to Evaluate the Offer',
        html: `<p>Run the annuity math first. What is your pension at VERA versus what it would be if you worked 3, 5, or 7 more years? The incremental annuity from each additional year is 1.0% of your high-3 , on an $88,000 salary, that is $880/year, or $73/month per additional year. Three additional years adds $2,640/year, or $220/month, for life.</p>
<p>Then model the healthcare gap. If you retire at 50 and rely on a spouse's employer coverage, the VERA deal looks much better than if you need to buy marketplace coverage for 15 years until Medicare. A family marketplace plan at age 50-62 can cost $10,000-$18,000 per year , that number can dwarf any VSIP payment over a 7-10 year period.</p>
<p>Finally, assess your post-federal opportunity. VERA plus a second career in the private sector with a 401k match and a higher salary can produce total retirement income that beats staying in federal service. The analysis is highly individual. Our team helps feds run these scenarios before the window closes.</p>`,
      },
      {
        heading: 'Important Disclaimers',
        html: `<p><em>This content is educational and general in nature. It is not tax, legal, or investment advice for your specific situation. Rules for FERS, TSP, Social Security, Medicare, and tax treatment change and can depend on factors unique to you. Consult a qualified tax professional, attorney, or CFP professional before acting on any of the strategies discussed here. PlanWell Financial Planning, LLC is not affiliated with or endorsed by OPM, the U.S. Office of Personnel Management, or any federal agency.</em></p>`
      }
    ],
    decisionMatrix: [
      {
        scenario: 'You are 55 with 28 years, your agency offers VERA+VSIP',
        recommendation: 'You are 2 years short of the MRA+30 threshold. The annuity difference is $1,760/year (2 more years x 1% x $88k). VSIP of $25,000 takes roughly 14 years to consume at $1,760/year , meaning staying wins only if you live well into your 80s. VERA looks attractive here.',
      },
      {
        scenario: 'You are 52 with 20 years, your agency offers VERA+VSIP',
        recommendation: 'Your annuity at VERA would be $17,600/year. Waiting 5 more years to 57+25 yields $22,000/year , a $4,400/year improvement plus the Supplement starting at MRA. The annuity gap is large enough that staying likely wins unless your post-federal opportunity is strong.',
      },
      {
        scenario: 'You are 58 with 33 years, your agency offers VERA+VSIP',
        recommendation: 'You already meet the 30-year requirement at MRA. You would retire under normal rules anyway. Take the VSIP as a bonus , it supplements your already-earned full annuity.',
      },
      {
        scenario: 'You have a pension from a prior private-sector job and federal VERA eligibility',
        recommendation: 'Model total retirement income from all sources. Prior pension + FERS VERA annuity + potential Social Security + TSP may sum to a comfortable number even with the lower VERA annuity. This is more common than it seems.',
      },
    ],
    relatedCalculator: { label: 'Estimate your FERS annuity', href: '/fers-retirement-calculator' },
    relatedGuideSlugs: ['mra-10-vs-mra-30', 'when-should-federal-employees-retire', 'fehb-to-medicare-transition'],
    faq: [
      {
        q: 'Is my VERA annuity reduced the same way MRA+10 is reduced?',
        a: 'No. VERA retirement produces an immediate, unreduced annuity as long as you meet the VERA eligibility requirements (50 with 20 years, or any age with 25 years). There is no 5%-per-year age penalty under VERA.',
      },
      {
        q: 'Can I be offered VERA if I am a special-provision employee (LEO, firefighter)?',
        a: 'Special provision employees already have more favorable retirement rules (retire at 50 with 20 years of covered service). A VERA window may not provide additional benefit if you already qualify for regular retirement. Check with your HR office about which rules apply to your position.',
      },
      {
        q: 'Does accepting VSIP prevent me from being rehired?',
        a: 'Yes. If you accept VSIP and later return to a federal position, you must repay the VSIP amount before you can be rehired , or the repayment is waived only in limited circumstances. This is a real constraint if you plan to return to government work.',
      },
      {
        q: 'How long is a VERA window typically open?',
        a: 'VERA windows are short , often 30-60 days from notification to decision. This is not an accident. Agencies want rapid workforce reduction. If you receive a VERA offer, begin your financial modeling immediately, not the week before the deadline.',
      },
      {
        q: 'What if I receive VERA but my position is not actually being eliminated?',
        a: 'VERA is voluntary regardless of whether your position is being cut. If you want to stay and your position survives the reorganization, you can simply decline VERA. The agency cannot compel you to accept it.',
      },
    ],
  },

  {
    slug: 'when-should-federal-employees-retire',
    title: 'When Should a Federal Employee Retire? A Decision Framework',
    metaTitle: 'When Should Federal Employees Retire? | PlanWell',
    metaDescription: 'The right retirement date for a federal employee is not simply the earliest date you are eligible. Here is the framework our CFP and ChFEBC advisors use to find the optimal date.',
    heroEyebrow: 'Decision Guide',
    heroHeading: 'When Should a Federal Employee Retire? A Decision Framework',
    heroLead: 'Retiring at the earliest eligible date can cost you tens of thousands of dollars over your retirement. So can waiting too long. This guide gives you the variables, the math, and a framework for finding your optimal date.',
    tldr: 'The best retirement date is usually the one that maximizes your annuity without unnecessary delay , often tied to a leave year boundary, a high-3 increment, or a special-provision milestone. Run the numbers before you pick a date.',
    sections: [
      {
        heading: 'The Five Variables That Determine Your Optimal Date',
        html: `<p>Five factors interact to determine when you should retire: (1) your eligibility date, (2) your high-3 calculation window, (3) the leave year boundary, (4) the FERS Supplement start date, and (5) your TSP and Social Security timing strategy. Getting all five right can add $20,000-$50,000 in cumulative first-decade income.</p>
<p>Most feds focus only on the first factor , when they are technically eligible. The other four are equally important and often require modeling with actual numbers. A retirement date that is two months later than you planned might capture an additional high-3 pay period, an extra sick leave increment, and a more favorable leave payout , easily worth $3,000-$8,000.</p>`,
      },
      {
        heading: 'The High-3 and Pay Raise Timing',
        html: `<p>Your high-3 is the average of your highest three consecutive years of basic pay. "Consecutive years" means 36 consecutive calendar months , not necessarily three calendar years. If a federal pay raise takes effect in January, retiring in February of that year means the raise is in your high-3 window.</p>
<p>For a fed earning $95,000 who receives a 4.1% pay raise in January, retiring in February means their high-3 includes one month of the higher salary. Retiring in December of the prior year means it does not. The difference in high-3: roughly $300-$400 per year in annuity. Not enormous, but it compounds over a 25-year retirement to $7,500-$10,000.</p>
<p>The more impactful scenario is a within-grade increase (WGI) or a promotion within your high-3 window. Moving from GS-13 Step 7 to Step 8 ($2,000-$3,000 salary increase) during your high-3 period adds the salary difference to your average. A promotion from GS-13 to GS-14 within the window can add $5,000+ to your high-3 , translating to $50-$75/month in annuity, for life.</p>`,
      },
      {
        heading: 'Leave Year and Lump-Sum Leave Payout',
        html: `<p>At retirement, you receive a lump-sum payout for your accrued annual leave, at your final hourly rate. Most full-time feds accrue 8 hours per pay period (26 pay periods per year = 208 hours, or about 26 days) when they have 15+ years of service. The maximum carryover is 240 hours (30 days).</p>
<p>If you retire on the last day of a leave year (typically the first Saturday in January), you have maximized your leave balance , you can carry up to 240 hours and have accrued additional leave throughout the year. If you retire mid-year, you may be paid out on a balance that has not yet reached its maximum.</p>
<p>On a $95,000 salary, each hour is worth $45.67. A full 240-hour payout is $10,961 before tax. Retiring a few weeks early (mid-December vs. early January) might reduce that payout by $2,000-$3,000. It is worth checking the leave year calendar before confirming your date.</p>`,
      },
      {
        heading: 'When the FERS Supplement Kicks In',
        html: `<p>The FERS Supplement starts the day your annuity begins , if you retire with an immediate, unreduced annuity at or after MRA. The Supplement averages $800-$1,500/month depending on your Social Security earnings history, and it runs until age 62. That is $9,600-$18,000 per year in additional income that terminates at a fixed date.</p>
<p>The Supplement is subject to an earnings test: if your earned income exceeds $23,400 (2025 threshold), the Supplement is reduced by $1 for every $2 of excess earnings. This means working part-time after retirement can silently eliminate the Supplement. Feds who plan to consult or work after retirement should model whether part-time income makes sense net of the Supplement reduction.</p>
<p>If you are considering delaying retirement by even one month, factor in the Supplement: one extra month of Supplement income (at $1,200/month average) is $1,200 you leave on the table by working an extra month instead of retiring. At some point, the Supplement income exceeds the annuity increment from the additional work month.</p>`,
      },
      {
        heading: 'Sick Leave Conversion and the Last Few Months',
        html: `<p>Unused sick leave is converted to additional creditable service at retirement. OPM uses 2,087 hours per year as the conversion factor. Every 174 hours of sick leave equals approximately one additional month of creditable service, which adds about 1/12 of 1% of your high-3 to your annuity.</p>
<p>If you have 1,000 hours of sick leave and a $95,000 high-3, those hours add roughly 5.7 months of service, or 0.48% of $95,000 = $456/year to your annuity. Over 25 years, that is $11,400. Some feds with 2,000+ hours of accumulated sick leave (possible after a long career with minimal illness) gain nearly a full year of additional creditable service, adding $950/year to their annuity.</p>
<p>Do not burn sick leave in the months before retirement unless you are genuinely ill. Many feds make this mistake, thinking unused sick leave is "lost" , it is not. It converts to annuity income. The exception: if you have a chronic condition that consumes sick leave, there is no harm in using it for legitimate health needs.</p>`,
      },
      {
        heading: 'Special Provision Employees: Mandatory Separation Ages',
        html: `<p>If you are a law enforcement officer, firefighter, or air traffic controller, you face mandatory separation at age 57 (LEO/FF) or 56 (ATC). You do not choose your last possible date , OPM requires you to leave. Your planning should work backward from that mandatory date.</p>
<p>Special provision employees who reach their mandatory separation age but want to stay must apply for a waiver. Waivers are granted only under specific circumstances and agency need. Assuming you will receive a waiver is a planning error. Build your retirement date around the mandatory limit.</p>`,
      },
      {
        heading: 'Important Disclaimers',
        html: `<p><em>This content is educational and general in nature. It is not tax, legal, or investment advice for your specific situation. Rules for FERS, TSP, Social Security, Medicare, and tax treatment change and can depend on factors unique to you. Consult a qualified tax professional, attorney, or CFP professional before acting on any of the strategies discussed here. PlanWell Financial Planning, LLC is not affiliated with or endorsed by OPM, the U.S. Office of Personnel Management, or any federal agency.</em></p>`
      }
    ],
    decisionMatrix: [
      {
        scenario: 'You are 3 months from MRA+30, considering retiring now vs. waiting',
        recommendation: 'Wait the 3 months. You gain 3 more months of high-3 average salary and 3 more months of service. At $90,000/year high-3, that is $2,250/year more in annuity. You also capture any sick leave accrued in those months.',
      },
      {
        scenario: 'You are eligible now but a promotion is 6 months away',
        recommendation: 'Model the high-3 impact of the promotion. If the pay jump is $8,000/year, working 6 more months captures 6 months of higher salary in your high-3 window. The annuity bump depends on how the promotion date falls within your 36-month high-3 window.',
      },
      {
        scenario: 'You are eligible now, the leave year ends in 3 weeks',
        recommendation: 'Consider staying 3 extra weeks. A full leave year carryover of 240 hours at $45/hour is $10,800 in lump-sum payout. That is often worth a brief delay if your plans allow.',
      },
      {
        scenario: 'You qualify for special provisions (LEO/FF) and are 54 with 25 years',
        recommendation: 'You can retire now under special provisions with an unreduced annuity. Model the difference between retiring at 54 vs. your mandatory separation age of 57. Three extra years at 1.7% per year for a $100k high-3 adds $5,100/year. Whether the extra income is worth 3 more working years is personal.',
      },
    ],
    relatedCalculator: { label: 'Estimate your FERS annuity', href: '/fers-retirement-calculator' },
    relatedGuideSlugs: ['mra-10-vs-mra-30', 'vera-vsip-explained', 'fers-supplement-earnings-test'],
    faq: [
      {
        q: 'What is the best day of the month to retire?',
        a: 'Generally, the last day of the month. Your annuity starts the first day of the following month. If you retire January 31, your annuity starts February 1 and you get a full month of pay for January. Retiring January 3 means you get 3 days of salary and your annuity starts February 1 , you lose most of January\'s pay.',
      },
      {
        q: 'Does it matter if I retire at the beginning or end of a pay period?',
        a: 'Yes. Federal employees are paid bi-weekly. Retiring mid-pay-period means your final paycheck covers only the days worked in that period. Retiring on the last day of a pay period gives you the full paycheck and the cleanest transition.',
      },
      {
        q: 'How long does OPM take to process retirement and start paying my annuity?',
        a: 'OPM\'s processing time for immediate retirements is typically 3-6 months for full processing. During that period, you receive an interim annuity payment , about 85% of your estimated final amount. Once OPM finalizes your case, you receive a lump sum retroactive true-up and your full monthly payment begins.',
      },
      {
        q: 'Can I retire and then return to federal service?',
        a: 'Yes, as a reemployed annuitant. Your salary and annuity may both continue, but this depends on the agency\'s authority to hire annuitants and whether your annuity is reduced by your salary (most positions do not require salary offset but it is agency-dependent).',
      },
      {
        q: 'What is the impact of working past 62 under FERS?',
        a: 'If you retire at 62 or later with 20+ years of service, your annuity formula becomes 1.1% per year instead of 1.0%. Working to 62 triggers this higher rate automatically , a 10% permanent annuity increase compared to retiring at the same service level before 62.',
      },
    ],
  },

  {
    slug: 'fers-supplement-earnings-test',
    title: 'The FERS Supplement Earnings Test: Rules, Math, and Traps',
    metaTitle: 'FERS Supplement Earnings Test Explained | PlanWell',
    metaDescription: 'The FERS Supplement earnings test can silently eliminate hundreds of dollars per month from your retirement income if you work after retirement. Here is how the math works and what traps to avoid.',
    heroEyebrow: 'Decision Guide',
    heroHeading: 'The FERS Supplement Earnings Test: Rules, Math, and Traps',
    heroLead: 'The FERS Supplement can add $800-$1,500 per month to your early retirement income. But if you take on part-time work or consulting after you retire, an earnings test can silently cut that benefit in half , or eliminate it entirely. Here is what you need to know.',
    tldr: 'If your earnings from work exceed $23,400 (2025), OPM reduces your Supplement by $1 for every $2 of excess earnings. At $35,400 in earnings, your Supplement is cut by $6,000 , over half of a typical Supplement amount. Many feds who plan to work part-time after retirement do not realize this until their first OPM review.',
    sections: [
      {
        heading: 'What the FERS Supplement Actually Is',
        html: `<p>The FERS Supplement is a monthly payment that bridges the income gap between early retirement and Social Security eligibility at age 62. OPM calculates it by estimating the Social Security benefit you would receive at age 62 based on your federal earnings only, then multiplying by a fraction representing your FERS service divided by 40.</p>
<p>If your estimated Social Security benefit at 62 (from federal service) would be $1,800/month and you have 30 years of FERS service: Supplement = $1,800 x (30/40) = $1,350/month. The Supplement is not your actual Social Security benefit , it is a proxy for the portion attributable to your federal career, paid by OPM until SSA takes over at 62.</p>
<p>The Supplement is only available to employees who retire under an immediate, unreduced annuity (MRA+30, age 60+20, or age 62+5). Special provision employees (LEO, FF, ATC) who retire with their special provision annuity qualify at retirement. VERA retirees qualify when they reach MRA, not at the VERA retirement date. Disability retirees do not receive the Supplement.</p>`,
      },
      {
        heading: 'How the Earnings Test Works',
        html: `<p>The earnings test mirrors the Social Security earnings test for pre-62 beneficiaries. For 2025, the exempt amount is $23,400. If your earned income exceeds this threshold, OPM reduces your Supplement by $1 for every $2 of income above the threshold.</p>
<p>If you earn $35,400 in 2025, you exceed the threshold by $12,000. The Supplement reduction is $12,000 / 2 = $6,000 for the year , meaning OPM will reduce your monthly Supplement payments by $500/month for the following year. If your Supplement is $1,100/month, it drops to $600/month.</p>
<p>If you earn $47,400 in 2025, you exceed the threshold by $24,000. The reduction is $12,000 for the year, or $1,000/month. If your Supplement is $1,100/month, it is eliminated entirely (you cannot receive a negative Supplement , it simply zeroes out).</p>`,
      },
      {
        heading: 'What Counts as Earnings',
        html: `<p>Earnings for the test include wages, salaries, commissions, self-employment income, and business income from a trade or business. They do NOT include investment income (dividends, interest, capital gains), rental income (unless you are a real estate professional), pension income, annuity income, Social Security benefits, or TSP withdrawals.</p>
<p>Self-employment income after expenses counts. If you do consulting and gross $60,000 but have $20,000 in legitimate business expenses, your net self-employment income for earnings test purposes is $40,000. The deduction for half of self-employment tax also reduces the counted amount.</p>
<p>Many retiring feds plan to do light consulting , 10-15 hours per week at $75-$150 per hour. At $100/hour for 15 hours per week over 48 weeks, that is $72,000 in gross consulting income. Net of expenses, the earnings test hit could be $20,000+ in Supplement reductions per year , largely wiping out the Supplement while you are earning consulting income.</p>`,
      },
      {
        heading: 'The OPM Reporting Process',
        html: `<p>OPM uses a self-reporting system for the earnings test. In April of each year, OPM mails a survey to annuitants receiving the Supplement who are under age 62. You must report the prior year\'s earnings on this form. If you do not respond, OPM can suspend your Supplement payments.</p>
<p>OPM also cross-checks IRS data. If your reported earnings do not match what the IRS shows, OPM can demand repayment of excess Supplement payments. Overpayments are typically recovered by reducing future payments , not a demand for immediate cash , but the recovery period can last months or years.</p>
<p>The survey is straightforward. The trap is not the form itself but the feds who receive Supplement payments without realizing the earnings test applies , they work, earn above the threshold, and then discover two years later that OPM wants back $8,000 in overpaid Supplement. This is entirely avoidable with upfront planning.</p>`,
      },
      {
        heading: 'Planning Strategies to Protect Your Supplement',
        html: `<p>If you plan to work after retirement, keep earned income below $23,400 per year to preserve the full Supplement. For feds who need more income than that, the question becomes: is the post-retirement work worth the Supplement reduction net of taxes?</p>
<p>If your Supplement is $1,200/month ($14,400/year) and your part-time consulting income is $30,000/year (a $6,600 excess), the Supplement reduction is $3,300/year. You keep $10,800 of your $30,000 consulting income after the Supplement loss. At that point, your effective wage from consulting is about $10,800 on $30,000 of gross , plus you still owe income tax on the $30,000. Some feds find this math unattractive and choose to keep work income deliberately below the threshold.</p>
<p>Investment income does not trigger the earnings test. A retiring fed who builds a dividend portfolio or has rental properties (as a passive investor) can receive substantial investment income without affecting the Supplement. This is why TSP withdrawals and investment distributions become attractive income sources during the Supplement years , they are test-exempt.</p>`,
      },
      {
        heading: 'Important Disclaimers',
        html: `<p><em>This content is educational and general in nature. It is not tax, legal, or investment advice for your specific situation. Rules for FERS, TSP, Social Security, Medicare, and tax treatment change and can depend on factors unique to you. Consult a qualified tax professional, attorney, or CFP professional before acting on any of the strategies discussed here. PlanWell Financial Planning, LLC is not affiliated with or endorsed by OPM, the U.S. Office of Personnel Management, or any federal agency.</em></p>`
      }
    ],
    decisionMatrix: [
      {
        scenario: 'You plan to retire at MRA+30 and do no post-retirement work',
        recommendation: 'No earnings test concern. Receive the full Supplement monthly without any reporting risk. Focus on TSP withdrawal timing and Social Security claiming strategy for the years approaching 62.',
      },
      {
        scenario: 'You plan to retire and do light consulting ($30,000-$40,000 per year)',
        recommendation: 'Model the Supplement reduction against the consulting income. At $36,000 in earnings, the Supplement is cut by $6,300/year. Whether the consulting income nets more than the Supplement loss depends on your tax bracket and consulting expenses.',
      },
      {
        scenario: 'You plan to retire and work full-time for a private employer ($70,000+)',
        recommendation: 'Assume the Supplement is effectively zero once earnings exceed $46,000+ (for a $1,200/month Supplement). Your retirement income planning should not rely on the Supplement in this scenario , model only the FERS pension, TSP withdrawals, and Social Security at 62.',
      },
      {
        scenario: 'You plan to retire and generate income only from TSP withdrawals and investments',
        recommendation: 'Investment income is exempt from the earnings test. You can withdraw aggressively from TSP, collect dividends, or realize capital gains without affecting the Supplement at all.',
      },
    ],
    relatedCalculator: { label: 'Estimate your FERS Supplement', href: '/fers-supplement-calculator' },
    relatedGuideSlugs: ['when-should-federal-employees-retire', 'mra-10-vs-mra-30', 'fehb-to-medicare-transition'],
    faq: [
      {
        q: 'Does the FERS Supplement increase with COLA each year?',
        a: 'No. The FERS Supplement does not receive annual COLA adjustments. It is fixed at the amount OPM calculated at your retirement and does not increase with inflation. This is one reason the Supplement becomes less valuable in real terms the longer you receive it.',
      },
      {
        q: 'What happens to my Supplement if I return to federal employment?',
        a: 'If you return to a federal position (as a reemployed annuitant), your Supplement payments are suspended during reemployment. They do not resume after you leave the reemployment , at 62 everything terminates anyway. Short-term reemployment typically does not make financial sense if you are receiving the Supplement.',
      },
      {
        q: 'Can I delay starting my annuity (and Supplement) to get a higher first payment?',
        a: 'No. The Supplement starts when your annuity starts, and both are fixed at that time. There is no mechanism to delay the Supplement separately from the annuity to get a higher amount later.',
      },
      {
        q: 'If I take the earnings test hit one year, does my Supplement ever go back to full?',
        a: 'Yes. OPM recalculates your Supplement each year based on the prior year\'s reported earnings. If you earn $50,000 in 2025 and reduce your earnings to $20,000 in 2026 (below the threshold), your Supplement is restored to the full amount in 2027.',
      },
      {
        q: 'What if I underreport my earnings to OPM?',
        a: 'OPM cross-references IRS records. Underreporting is likely to be caught, and OPM will recover the overpayment from future annuity payments. Intentional underreporting can be treated as fraud, with more serious consequences. Always report accurately.',
      },
    ],
  },

  {
    slug: 'fehb-to-medicare-transition',
    title: 'FEHB to Medicare: Your Transition Playbook',
    metaTitle: 'FEHB and Medicare Transition for Federal Retirees | PlanWell',
    metaDescription: 'Federal retirees face a choice at 65: keep FEHB alone, add Medicare Part B, or combine both. The right answer depends on your health, your FEHB plan, and the math. Here is how to decide.',
    heroEyebrow: 'Decision Guide',
    heroHeading: 'FEHB to Medicare: Your Transition Playbook',
    heroLead: 'When you turn 65, Medicare becomes available , and the interplay with FEHB is one of the most consequential financial decisions of your retirement. Get it wrong and you either overpay for coverage you do not need or leave yourself exposed in ways you will not discover until you have a claim.',
    tldr: 'Most federal retirees who kept FEHB into retirement should enroll in Medicare Part A (it is free and has no downside). Part B is the real decision: it costs $185/month or more in 2025 and offers real value only if your FEHB plan does not already cover what Part B covers at lower total cost.',
    sections: [
      {
        heading: 'Medicare Parts A and B: What Each Covers',
        html: `<p>Medicare Part A covers hospital inpatient care, skilled nursing facility care (up to 100 days), some home health services, and hospice care. For most federal retirees, Part A is premium-free because you paid Medicare taxes throughout your career (or at least 40 quarters worth).</p>
<p>Medicare Part B covers outpatient services: physician visits, lab work, imaging, durable medical equipment, preventive care, and outpatient surgery. Part B has a monthly premium , $185/month for most retirees in 2025, rising to $628/month at the highest income tier ($500,000+ for married couples). There is also a 20% coinsurance after the annual deductible ($257 in 2025).</p>
<p>Medicare Part D covers prescription drugs. Most federal retirees who keep FEHB do not need a separate Part D plan , FEHB drug coverage is typically equivalent or superior, and OPM has stated that FEHB drug coverage is creditable for Medicare Part D purposes. Enrolling in a separate Part D plan while keeping FEHB is redundant and wasteful for most people.</p>`,
      },
      {
        heading: 'The Case for Keeping FEHB Without Medicare Part B',
        html: `<p>FEHB plans, especially Blue Cross Blue Shield's Standard option (one of the most popular among retirees), already provide comprehensive coverage for outpatient services, physician visits, and lab work. Many FEHB plans have relatively low out-of-pocket maximums , $6,000-$8,000 per year for Self Plus One in many plans.</p>
<p>If you are healthy and have low expected healthcare utilization, FEHB alone may cost less in total (premium + out-of-pocket) than FEHB + Part B. Adding Part B at $185/month ($2,220/year) for a couple means $4,440/year in additional premiums alone , before you see any claim. You would need to generate significant Part B claims to break even on that cost.</p>
<p>The strongest argument against Part B: FEHB is your primary insurer when you do not have Part B. Claims that Medicare Part B would cover (like outpatient physician visits) go to FEHB instead. If your FEHB plan covers those claims well, you may not miss Part B at all. Consult a specific FEHB plan summary of benefits before drawing conclusions , plan quality varies significantly.</p>`,
      },
      {
        heading: 'The Case for Adding Medicare Part B',
        html: `<p>When you add Medicare Part B and keep FEHB, the two programs coordinate to cover nearly all your healthcare costs. Medicare Part B pays first (as primary) for outpatient services, covering 80% after the deductible. FEHB then covers much or all of the remaining 20%. Your total out-of-pocket for physician and outpatient services drops to near zero in many cases.</p>
<p>For retirees with chronic conditions, cancer history, or high healthcare utilization, this coordination can save more than the Part B premium cost. A retiree managing diabetes with frequent specialist visits, lab work, and ongoing medications might see $5,000-$8,000/year in FEHB claims that become near-zero with Part B coordination , easily justifying the $2,220/year in Part B premiums.</p>
<p>Part B also reduces the FEHB plan\'s liability, which is one reason OPM has historically offered premium incentives for retirees who enroll. As of January 2025, FEHB plans coordinate benefits with Medicare Part B in ways that can eliminate almost all out-of-pocket costs for Medicare-covered services. The new Medicare Advantage for FEHB options introduced in recent years also shift the calculation for some retirees.</p>`,
      },
      {
        heading: 'Income-Related Monthly Adjustment Amount (IRMAA)',
        html: `<p>If your Modified Adjusted Gross Income (MAGI) was above $106,000 (single) or $212,000 (married filing jointly) two years prior, you pay a higher Part B premium , the Income-Related Monthly Adjustment Amount. IRMAA tiers for 2025 range from $185/month to $628/month per person.</p>
<p>A married couple with $250,000 MAGI pays $296/month each for Part B , $7,104/year combined. That premium level changes the break-even analysis significantly. At that cost, Part B needs to produce substantial out-of-pocket savings to pay off.</p>
<p>IRMAA is based on income two years prior. If you retired in 2024 and had high employment income that year, your 2026 Part B premium will reflect that. You can appeal IRMAA if your income has since dropped due to a qualifying life event (retirement is one). File a Life Changing Event appeal with SSA using Form SSA-44.</p>`,
      },
      {
        heading: 'Enrollment Timing: Do Not Miss the Windows',
        html: `<p>You are automatically enrolled in Medicare Part A when you turn 65 if you are already receiving Social Security. If you have not claimed Social Security, you must actively enroll in Part A , the Initial Enrollment Period runs from 3 months before your 65th birthday through 3 months after it.</p>
<p>Part B also has an Initial Enrollment Period. If you delay Part B and miss it without a qualifying Special Enrollment Period, you will pay a late enrollment penalty: 10% per year of delay, permanently added to your premium. A 2-year delay means a 20% premium surcharge for the rest of your life.</p>
<p>Federal retirees who remain employed past 65 with employer coverage have a Special Enrollment Period when they separate. But FEHB in retirement is not "employer coverage" in the Medicare sense , OPM has clarified that FEHB in retirement does NOT qualify as employer coverage for purposes of the Part B Special Enrollment Period. Delaying Part B enrollment past 65 while relying only on FEHB (in retirement) will trigger the late penalty.</p>`,
      },
      {
        heading: 'Important Disclaimers',
        html: `<p><em>This content is educational and general in nature. It is not tax, legal, or investment advice for your specific situation. Rules for FERS, TSP, Social Security, Medicare, and tax treatment change and can depend on factors unique to you. Consult a qualified tax professional, attorney, or CFP professional before acting on any of the strategies discussed here. PlanWell Financial Planning, LLC is not affiliated with or endorsed by OPM, the U.S. Office of Personnel Management, or any federal agency.</em></p>`
      }
    ],
    decisionMatrix: [
      {
        scenario: 'You are 64, retiring next year, and in good health with low healthcare use',
        recommendation: 'Enroll in Part A immediately (free, no downside). Analyze your specific FEHB plan\'s outpatient coverage before enrolling in Part B. If your FEHB plan covers physician/outpatient well, consider delaying Part B decision 1-2 years and reassessing based on actual utilization.',
      },
      {
        scenario: 'You are 65, have a chronic condition, and use healthcare regularly',
        recommendation: 'Enroll in both Part A and Part B. The coordination of benefits will likely produce net savings that exceed the Part B premium at any meaningful level of utilization.',
      },
      {
        scenario: 'You are 65 with MAGI of $280,000 from investments and pension combined',
        recommendation: 'Calculate your IRMAA tier , you likely pay $296/month per person for Part B. At that cost, model carefully whether Part B coordination savings justify the premium. For a healthy couple with low utilization at this income level, the math may favor FEHB alone.',
      },
      {
        scenario: 'You are 67 and never enrolled in Part B because you thought FEHB was enough',
        recommendation: 'If you missed the Initial Enrollment Period without a valid Special Enrollment Period, you now face the late penalty. Enroll at the next General Enrollment Period (January through March, coverage begins July). Calculate the lifetime penalty cost and whether FEHB alone remains cheaper.',
      },
    ],
    relatedGuideSlugs: ['when-should-federal-employees-retire', 'fers-supplement-earnings-test'],
    faq: [
      {
        q: 'Can I drop FEHB once I have Medicare Parts A and B?',
        a: 'Yes, you can drop FEHB voluntarily. But this is a permanent decision , if you drop FEHB in retirement, you cannot re-enroll later. For most federal retirees, keeping at least a lower-cost FEHB plan alongside Medicare provides better coverage coordination than Medicare alone.',
      },
      {
        q: 'Does FEHB cover dental and vision in retirement?',
        a: 'Standard FEHB plans provide limited dental and vision. The Federal Dental and Vision Insurance Program (FEDVIP) is a separate election available to federal retirees. Medicare does not cover routine dental or vision. This is an area where FEHB + FEDVIP combination remains valuable even when Medicare is your primary for medical.',
      },
      {
        q: 'What happens to FEHB if my annuity is not large enough to cover the premiums?',
        a: 'OPM deducts FEHB premiums directly from your annuity. If your annuity is smaller than the premium, you can arrange direct billing. If your annuity is extremely small, you may need to self-pay directly to OPM. The key is that a very small annuity does not disqualify you from FEHB , it just changes how you pay.',
      },
      {
        q: 'If I get Medicare Advantage through an FEHB plan, do I still need to pay Part B?',
        a: 'Some FEHB plans now offer Medicare Advantage options that waive or rebate the Part B premium. These plans are available only to retirees enrolled in both Medicare Part A and Part B. The math can be compelling if the plan\'s coverage equals your current FEHB plan and the premium rebate is substantial.',
      },
      {
        q: 'My spouse is covered under my FEHB self-plus-one plan and is not yet 65. What happens when I turn 65?',
        a: 'Your FEHB self-plus-one plan continues covering your spouse regardless of your Medicare status. Medicare coordinates with FEHB for your claims; FEHB alone covers your spouse\'s claims. There is no need to change your FEHB enrollment when you turn 65.',
      },
    ],
  },

  {
    slug: 'survivor-benefit-election-guide',
    title: 'FERS Survivor Benefit Election: Full, Partial, or None?',
    metaTitle: 'FERS Survivor Benefit Election Guide | PlanWell',
    metaDescription: 'The survivor benefit election at FERS retirement is permanent. Choosing wrong costs either your spouse thousands per year or you thousands per year for the rest of your life. Here is the analysis.',
    heroEyebrow: 'Decision Guide',
    heroHeading: 'FERS Survivor Benefit Election: Full, Partial, or None?',
    heroLead: 'When you retire under FERS, you must elect whether to provide a survivor annuity for your spouse. The cost is permanent and nonrefundable. The protection it provides can be the difference between financial security and financial crisis for a surviving spouse.',
    tldr: 'A full survivor annuity pays 50% of your unreduced annuity to your spouse if you die first, and costs you 10% of your annuity for life. The cost is real; so is the risk of leaving it uncovered. Run the math on both sides before you sign.',
    sections: [
      {
        heading: 'What You Are Choosing Between',
        html: `<p>At FERS retirement, you can elect: (a) a full survivor annuity of 50% of your unreduced base annuity, at a cost of 10% of your annuity; (b) a partial survivor annuity of any lesser amount, at a prorated cost; or (c) no survivor annuity, at no cost to your annuity.</p>
<p>Your spouse must consent in writing to any election less than the full survivor annuity. OPM requires a notarized spouse signature on form SF-2801 if you elect partial or no survivor annuity. If your spouse does not consent or cannot be located, OPM defaults to the full election.</p>
<p>The election is permanent at the moment your annuity begins. You cannot change from "none" to "full" later, even if your spouse becomes seriously ill. The only exception: if you divorce and remarry, you can elect a survivor annuity for a new spouse , but only within 2 years of the remarriage and subject to an actuarial reduction.</p>`,
      },
      {
        heading: 'The Full Survivor Annuity: Running the Numbers',
        html: `<p>Suppose your FERS annuity is $42,000/year ($3,500/month). The cost of a full survivor annuity is 10% of your annuity: $4,200/year ($350/month). Your take-home annuity drops to $37,800/year ($3,150/month). Your spouse, if they survive you, receives 50% of the unreduced $42,000 = $21,000/year ($1,750/month), indexed for COLA.</p>
<p>Is $4,200/year a fair price for a $21,000/year benefit to your spouse? That depends entirely on who dies first and when. If you die 5 years into retirement, your spouse receives $21,000/year for potentially 20+ more years , a total benefit of $420,000+. The cost to you was $4,200/year x 5 years = $21,000. An extraordinary return.</p>
<p>If you live to 90 and your spouse predeceases you at 80, you paid $4,200/year for 25 years ($105,000) and your spouse never collected a dollar. The cost was entirely lost. This is the survivor benefit equivalent of life insurance , pure risk transfer.</p>`,
      },
      {
        heading: 'No Survivor Annuity: When It Makes Sense',
        html: `<p>Electing no survivor annuity keeps the full $42,000/year annuity in your pocket. Over 20 years, that is $84,000 you retain instead of paying for coverage. If you invest those savings at a modest 5% real return, you build a portfolio of roughly $140,000 over 20 years , available to your spouse as a liquid asset.</p>
<p>The "self-insure" approach works best when: your spouse has substantial independent income or assets that would not rely on your annuity; your spouse is in poor health and unlikely to outlive you; or you have a large TSP balance and other assets that provide the same income replacement function.</p>
<p>A spouse with their own pension (CSRS, state/local, or a private defined-benefit plan) and Social Security income may have sufficient independent income that the survivor benefit is redundant. The question is always: if you die tomorrow, can your spouse maintain their standard of living without your annuity?</p>`,
      },
      {
        heading: 'FEHB and Survivor Benefits: The Connection',
        html: `<p>If you elect no survivor annuity and you die first, your spouse loses FEHB coverage. FEHB in retirement is contingent on the retired employee having an active annuity. When that annuity terminates (at the retiree\'s death), so does the spouse\'s FEHB unless a survivor annuity is in place.</p>
<p>This is the most underappreciated consequence of electing no survivor annuity. A spouse who is 65 and on Medicare can lose their FEHB supplement. A spouse who is 58 and relies on FEHB for primary coverage now needs to find insurance in the individual market , potentially at a significant premium , for the remainder of their pre-Medicare years.</p>
<p>If your spouse is significantly younger than you, the FEHB consequence alone may justify the full survivor annuity election. A 63-year-old retiree with a 58-year-old spouse who dies early without survivor benefits leaves that spouse to buy marketplace insurance for 7 years at potentially $15,000-$20,000/year before Medicare. That is $105,000-$140,000 in unplanned health insurance costs.</p>`,
      },
      {
        heading: 'The Partial Survivor Annuity Option',
        html: `<p>The partial option allows you to elect any specific dollar amount as the survivor annuity base , the minimum is $1 (yes, literally one dollar, which produces a nominal survivor benefit and costs almost nothing but preserves FEHB). The cost scales proportionally: if you elect a survivor base of $21,000 (half your $42,000 annuity), the cost is 5% of your annuity.</p>
<p>Some feds elect a minimal partial survivor benefit solely to keep FEHB available to their spouse after death. If your primary concern is healthcare continuity rather than income replacement, a $1 survivor base election preserves FEHB for your spouse at essentially zero annuity cost. Confirm this interpretation with OPM or your HR office, as the rule requires the annuity to be "payable" for FEHB to continue.</p>
<p>A partial election of $10,000/year would cost you roughly 2.4% of your annuity ($1,008/year) and provide your spouse $10,000/year income plus FEHB continuation. This middle path is often overlooked in the binary framing of "full or none."</p>`,
      },
      {
        heading: 'Important Disclaimers',
        html: `<p><em>This content is educational and general in nature. It is not tax, legal, or investment advice for your specific situation. Rules for FERS, TSP, Social Security, Medicare, and tax treatment change and can depend on factors unique to you. Consult a qualified tax professional, attorney, or CFP professional before acting on any of the strategies discussed here. PlanWell Financial Planning, LLC is not affiliated with or endorsed by OPM, the U.S. Office of Personnel Management, or any federal agency.</em></p>`
      }
    ],
    decisionMatrix: [
      {
        scenario: 'You are 57 with a spouse 5 years younger, both in good health',
        recommendation: 'Elect the full survivor annuity. Statistical life expectancy means your spouse is likely to outlive you by several years. The FEHB protection and $21,000/year income floor for a surviving spouse at 52+ years old is well worth the $350/month cost.',
      },
      {
        scenario: 'You are 62, your spouse is 70 and in poor health',
        recommendation: 'Consider a partial or no election. If actuarial odds favor you outliving your spouse, paying 10% of your annuity for coverage your spouse may never collect is a poor expected-value bet. Consult a CFP before signing; this is the scenario where the no-election case is strongest.',
      },
      {
        scenario: 'Your spouse has their own federal pension of $40,000/year and Medicare',
        recommendation: 'Evaluate whether your spouse\'s independent income covers their expenses without your annuity. If yes, consider a partial election just large enough to keep FEHB , at minimal cost to you.',
      },
      {
        scenario: 'You are single at retirement but may remarry',
        recommendation: 'No election needed at retirement. If you remarry within 2 years, you can elect a survivor annuity for the new spouse. If you remarry and want survivor coverage, act within the 2-year window.',
      },
      {
        scenario: 'Your spouse has a serious health condition and is unlikely to outlive you',
        recommendation: 'The expected-value math shifts toward partial or no election. But FEHB continuity still matters , if your spouse\'s condition requires ongoing care that depends on FEHB, a minimal partial election preserves that coverage at low cost.',
      },
    ],
    relatedCalculator: { label: 'Estimate your FERS annuity', href: '/fers-retirement-calculator' },
    relatedGuideSlugs: ['divorce-and-fers', 'when-should-federal-employees-retire', 'fehb-to-medicare-transition'],
    faq: [
      {
        q: 'What if my spouse dies before me after I elected the full survivor annuity?',
        a: 'Your annuity increases back to the full unreduced amount the month after your spouse\'s death. However, you do not receive a refund of the premiums you paid during the years the election was in effect. The cost was for coverage during the period when the risk of your spouse surviving you existed.',
      },
      {
        q: 'Can I change my survivor benefit election after retirement?',
        a: 'Generally no. The election is irrevocable once your annuity begins. The only post-retirement changes allowed are: (1) adding a survivor annuity for a new spouse within 2 years of remarriage, and (2) removing a survivor annuity if the qualifying spouse dies or you divorce.',
      },
      {
        q: 'Does the survivor annuity receive COLA the same as the employee annuity?',
        a: 'Yes. The survivor annuity receives the same COLA as FERS retiree annuities , CPI minus 1 percentage point when CPI is above 3%, and the full CPI when it is between 2% and 3%, and no COLA when CPI is below 2%.',
      },
      {
        q: 'Is a domestic partner eligible for a FERS survivor annuity?',
        a: 'No. FERS survivor annuities are only available to legally married spouses and, in some cases, former spouses under a court order. Domestic partners do not qualify regardless of the length or nature of the relationship. TSP beneficiary designations can accommodate domestic partners as account inheritors.',
      },
      {
        q: 'If I elect no survivor annuity, can I use a life insurance policy to replace the income for my spouse?',
        a: 'Yes, and many feds do this analysis. Term or permanent life insurance can be purchased to provide a lump sum that your spouse invests for income. The break-even question is whether the life insurance premium (plus investment return) produces more income for your spouse than the survivor annuity would. FEGLI Option B provides some coverage, but it is expensive in later years.',
      },
    ],
  },
];

export function getGuide(slug: string): DecisionGuide | undefined {
  return decisionGuides.find((g) => g.slug === slug);
}

export function getAllGuides(): DecisionGuide[] {
  return decisionGuides;
}
