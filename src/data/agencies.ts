export interface AgencyBenefitHighlight {
  title: string;
  body: string;
}

export interface Agency {
  slug: string;
  name: string;
  shortName: string;
  employeeCount: string;
  metaTitle: string;
  metaDescription: string;
  heroEyebrow: string;
  heroHeading: string;
  heroLead: string;
  introHtml: string;
  whyMattersHtml: string;
  uniqueConsiderations: AgencyBenefitHighlight[];
  commonQuestionsHtml: string;
  specialProvisionsNote?: string;
  commonJobs: string[];
  primaryLocations: string[];
  relatedAgencySlugs?: string[];
  faq: { q: string; a: string }[];
}

export const agencies: Agency[] = [
  {
    slug: 'department-of-defense',
    name: 'Department of Defense',
    shortName: 'DoD',
    employeeCount: '750,000+ civilian employees',
    metaTitle: 'FERS Retirement Planning for DoD Civilian Employees',
    metaDescription:
      'Expert FERS retirement planning for Department of Defense civilian employees. Navigate TSP, FEHB, military-civilian service credit, and special provisions with a CFP-led workshop. Free.',
    heroEyebrow: 'Department of Defense',
    heroHeading: 'FERS Retirement Planning for DoD Civilian Employees',
    heroLead:
      'With 750,000+ civilian employees across every state and 80+ countries, DoD is the largest civilian employer in the federal government. The rules are the same FERS rules, but the decisions are bigger: military service credit, early-out authorities, FEHB versus Tricare, and TSP allocations that have to last 30 years in retirement.',
    introHtml: `
      <p>If you are a DoD civilian, you have spent your career around complexity. Your retirement deserves the same rigor you brought to the mission. The problem is that most financial advisors do not understand the FERS pension, do not know how prior military service rolls into civilian time, and have never heard of a CSRS Offset or a military deposit.</p>
      <p>PlanWell was built for federal employees. Both of our founders hold the Chartered Federal Employee Benefits Consultant (ChFEBC) designation in addition to the CFP. That means when we sit down with a DoD civilian, we know the acronyms, the forms, and the traps.</p>
    `,
    whyMattersHtml: `
      <p>DoD civilian retirement decisions are rarely simple. A typical DoD workshop attendee has served 25 to 35 years, often with prior active-duty time, a mid-career PCS move or two, and a TSP balance between $400,000 and $1.5 million. The wrong survivor benefit election, the wrong TSP withdrawal order, or a missed military deposit can cost six figures over a 30-year retirement.</p>
      <p>The FERS retirement system is generous, but it is not automatic. Every DoD civilian should pressure-test their plan against four questions: Am I retiring on the right date? Am I taking the survivor benefit that fits my spouse, not the default? Is my TSP allocation actually giving me the income I need? And have I coordinated FEHB, Medicare, and any Tricare eligibility correctly? Our free 3-hour workshop covers all four.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'Military service credit',
        body:
          'If you served on active duty before your DoD civilian career, that time likely counts toward your FERS pension, but only if you make a military deposit before you retire. We calculate whether the deposit pays off for your specific service dates and high-3.',
      },
      {
        title: 'VERA and VSIP offers',
        body:
          'DoD components routinely offer Voluntary Early Retirement Authority and Voluntary Separation Incentive Payments during reorganizations. The math on whether to take them is non-trivial. We break down the break-even, the FERS supplement impact, and the tax treatment of the VSIP.',
      },
      {
        title: 'Overseas and hardship service',
        body:
          'Time at an overseas post or a designated hardship duty station can affect your high-3 in unexpected ways if you receive locality-free pay. We make sure your high-3 is calculated correctly before you lock in a retirement date.',
      },
      {
        title: 'Tricare coordination for former military',
        body:
          'If you are a military retiree now working as a DoD civilian, you have a Tricare-FEHB-Medicare three-way decision to make. Most advisors cannot navigate this. We do it every week.',
      },
    ],
    commonQuestionsHtml: `
      <p>The three questions we hear most from DoD civilians in the workshop are: "Should I pay my military deposit?", "Can I take the VSIP and still get my full pension?", and "Do I keep FEHB or switch to Tricare in retirement?" The answer to each depends on your exact service history, age, and health. We help you run the numbers.</p>
    `,
    specialProvisionsNote:
      'DoD firefighters, law enforcement officers, air traffic controllers, and nuclear materials couriers qualify for FERS special provisions with a reduced MRA (50 with 20 years or any age with 25 years) and an enhanced pension multiplier. See our LEO and ATC calculator for a custom estimate.',
    commonJobs: [
      'Engineers and logistics specialists',
      'Acquisition and contracting (1102 series)',
      'Intelligence analysts',
      'IT and cybersecurity specialists',
      'Financial managers',
      'Base operations and facilities',
    ],
    primaryLocations: [
      'Pentagon (Arlington, VA)',
      'Fort Meade, MD',
      'Norfolk Naval Station',
      'San Diego Naval Base',
      'Wright-Patterson AFB, OH',
      'Hanscom AFB, MA',
      'Huntsville (Redstone Arsenal)',
    ],
    relatedAgencySlugs: ['department-of-veterans-affairs', 'department-of-homeland-security', 'nasa'],
    faq: [
      {
        q: 'Are DoD civilian employees in FERS?',
        a: 'Yes. Civilian employees hired after January 1, 1984 are in the Federal Employees Retirement System (FERS). A small number of longer-tenured employees remain in CSRS or CSRS Offset. Your retirement plan coverage is listed in your SF-50 under "Retirement Plan."',
      },
      {
        q: 'Should I make a military deposit for my active-duty service?',
        a: 'Usually yes, but not always. Post-1956 military service counts toward your FERS pension only if you buy it back by paying a military deposit (3% of base pay plus interest). The deposit typically pays for itself in 2 to 5 years of retirement, but if you are close to retirement and have a short life expectancy or no survivor, the math can tilt the other way. We run the calculation in the workshop.',
      },
      {
        q: 'Can I take VSIP and still collect my full FERS pension?',
        a: 'Yes, if you meet the regular FERS retirement requirements on your separation date (MRA with 30 years, age 60 with 20, or age 62 with 5). VSIP does not reduce your pension. DoD\'s VSIP cap is $40,000 per employee (raised in 2017), versus $25,000 at other federal agencies. VSIP is fully taxable as ordinary income in the year you receive it, which can push you into a higher bracket. Planning the tax year matters.',
      },
      {
        q: 'How does DoD service abroad affect my high-3?',
        a: 'Your high-3 is based on your three highest consecutive years of basic pay including locality pay. Overseas assignments typically pay a post allowance and cost-of-living allowance (COLA), but those do not count toward your high-3. If you took an overseas assignment in your final years, you may have accidentally lowered your high-3. We catch this regularly.',
      },
      {
        q: 'Do DoD civilians keep FEHB in retirement?',
        a: 'Yes, if you have been continuously enrolled in FEHB for the 5 years immediately before retirement (or since you were first eligible). FEHB in retirement is the single most valuable federal benefit after the pension itself. Most DoD retirees should keep it. Former military retirees with Tricare have additional coordination options we cover in the workshop.',
      },
      {
        q: 'What is the FERS supplement and do DoD civilians qualify?',
        a: 'The FERS supplement is a bridge payment designed to replace Social Security until you reach age 62. DoD civilians who retire under regular FERS at MRA with 30 years, or age 60 with 20 years, qualify. Special-provision employees (law enforcement, firefighters, ATC) qualify regardless of age. It is subject to an earnings test if you go back to work.',
      },
    ],
  },
  {
    slug: 'department-of-veterans-affairs',
    name: 'Department of Veterans Affairs',
    shortName: 'VA',
    employeeCount: '400,000+ civilian employees',
    metaTitle: 'VA Employee FERS Retirement Planning | PlanWell',
    metaDescription:
      'Free FERS retirement workshop for VA employees. Learn how Title 38 pay, hybrid retirement, and FEHB interact. Expert CFP and ChFEBC guidance. Register free.',
    heroEyebrow: 'Department of Veterans Affairs',
    heroHeading: 'FERS Retirement Planning for VA Employees',
    heroLead:
      'The VA is the largest healthcare employer in the federal government, with over 400,000 civilian employees across 1,200 facilities nationwide. Your retirement picture is often more complicated than peers at other agencies because of Title 38 pay authorities, hybrid appointment structures, and a high-3 salary that may not match your GS peers.',
    introHtml: `
      <p>VA employees come to our workshops with questions that most financial advisors cannot answer: "Does my Title 38 premium pay count toward my high-3?" "I am a hybrid Title 38 employee, which retirement rules apply to me?" "I have a physician comparability allowance. How does that affect my annuity?" PlanWell's team holds the ChFEBC designation specifically because these details matter.</p>
      <p>We work with VA clinicians, nurses, pharmacists, and administrative staff from Richmond to Palo Alto. The FERS framework is the same everywhere, but the inputs, particularly base pay, locality, and special pay, look very different for a GS-12 program analyst versus a VN-0610 nurse practitioner. We help you get the inputs right before you calculate anything.</p>
    `,
    whyMattersHtml: `
      <p>Getting your high-3 wrong at the VA costs real money. If you are a physician earning $275,000 in base pay plus a $30,000 physician comparability allowance, your high-3 is based on the base salary, not total compensation, unless your PCA was converted to base pay. That one distinction can reduce your annual annuity by $3,000 to $7,000 per year, compounding for 25 years of retirement. We see this miscalculation regularly.</p>
      <p>The VA also has a higher-than-average CSRS holdover population among long-tenured nurses and administrators hired before 1984. If you are in CSRS or CSRS Offset, your retirement math is entirely different, your Social Security interaction was historically subject to the Windfall Elimination Provision (WEP), which was repealed by the Social Security Fairness Act signed January 5, 2025; CSRS retirees with outside Social Security earnings now receive those benefits without WEP reduction. Your FEHB continuation rules also have subtle differences. Our workshop addresses both FERS and CSRS populations in separate breakout tracks.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'Title 38 and hybrid pay authorities',
        body:
          'Title 38 employees, including physicians, dentists, and many nurses, are paid under pay tables separate from the GS schedule. Your high-3 is calculated from your Title 38 base pay, but special pay components like market pay and physician comparability allowances may or may not count depending on how your HR office coded the payment. Verify your high-3 inputs before you do any retirement projections.',
      },
      {
        title: 'Hybrid appointment structures',
        body:
          'Some VA nurses and allied health professionals hold hybrid Title 38/Title 5 appointments. Your retirement system, FERS or CSRS, is determined by your appointment date and appointment authority, not your pay table. If you are unsure which retirement system applies to your hybrid appointment, pull your SF-50 and look at block 30.',
      },
      {
        title: 'FEHB and VA health benefits coordination',
        body:
          'As a VA employee, you receive care at VA facilities at no cost, which can make FEHB feel redundant during your working years. But FEHB is your retirement healthcare bridge, and you need 5 years of continuous enrollment to carry it into retirement. Dropping FEHB during your career to save premiums can permanently disqualify you from coverage after you separate.',
      },
      {
        title: 'Geographic pay variation',
        body:
          'VA facilities range from rural community-based outpatient clinics to major academic medical centers in high-cost cities. Locality pay differentials across VA locations are significant: a GS-13 in San Francisco earns roughly 40% more locality than the same grade in rural Alabama. If you moved facilities mid-career, your high-3 window needs to capture your highest-pay years, not just your final three.',
      },
    ],
    commonQuestionsHtml: `
      <p>The top questions we hear from VA employees are: "Does my market pay count in my high-3?", "Can I retire at MRA if I started as a Title 38 hybrid?", and "Should I keep FEHB even though I get free VA care?" Each answer turns on details specific to your appointment type, pay category, and enrollment history. We work through all three in the workshop.</p>
    `,
    commonJobs: [
      'Registered nurses and nurse practitioners (VN-0610)',
      'Physicians and dentists (Title 38)',
      'Medical support assistants',
      'Program analysts and administrators (GS series)',
      'Pharmacists and pharmacy technicians',
      'Social workers and mental health counselors',
    ],
    primaryLocations: [
      'Washington, DC (Central Office)',
      'Richmond, VA (Benefits Administration)',
      'Bay Pines, FL',
      'Houston, TX (Michael E. DeBakey VAMC)',
      'Los Angeles, CA (West LA VAMC)',
      'Minneapolis, MN',
      'Philadelphia, PA',
    ],
    relatedAgencySlugs: ['department-of-defense', 'department-of-health-and-human-services', 'department-of-homeland-security'],
    faq: [
      {
        q: 'Does VA physician market pay count toward my high-3?',
        a: 'Market pay for VA physicians is base pay under Title 38, so yes, it counts toward your high-3. Physician comparability allowances (PCAs), however, are treated as special pay in most cases and do not count toward your FERS annuity base. If your HR office reclassified your PCA as base pay, the answer changes. Check your earnings and leave statement under "pay plan" before assuming.',
      },
      {
        q: 'I am a hybrid Title 38/Title 5 VA nurse. Which retirement system am I in?',
        a: 'Your retirement system is determined by your appointment date, not your pay authority. If you were hired after December 31, 1983, you are in FERS (or FERS-FRAE if hired after 2013). The hybrid designation refers to which pay table governs your salary, not your retirement coverage. Confirm by looking at block 30 of your most recent SF-50.',
      },
      {
        q: 'Can I drop FEHB while working at the VA since I get free care there?',
        a: 'You can, but doing so is one of the most expensive retirement mistakes VA employees make. To carry FEHB into retirement, you must have been continuously enrolled for the five years immediately before your retirement date. A gap, even one open season, breaks that eligibility permanently. The premium savings during your career are rarely worth losing a benefit worth $15,000 to $25,000 per year in retirement.',
      },
      {
        q: 'What is my MRA as a VA FERS employee?',
        a: 'Your Minimum Retirement Age depends on your birth year. Employees born in 1970 or later have an MRA of 57. Born before 1948, the MRA is 55. The MRA scales up between those birth years. At MRA with 30 years of creditable service, you qualify for an immediate unreduced FERS annuity. At MRA with 10 to 29 years, you qualify for a reduced annuity (5% per year under age 62).',
      },
      {
        q: 'Does VA service count differently toward FERS than other federal agencies?',
        a: 'No. Creditable service for FERS purposes is the same regardless of which agency employs you. Every year of FERS-covered civilian service counts at the same 1% accrual rate (1.1% if you retire at age 62 or later with 20+ years). What differs at the VA is the base pay that feeds your high-3, which can be significantly higher than GS peers, making your annuity calculation worth more attention.',
      },
      {
        q: 'I have both VA service and prior military service. Should I buy back my military time?',
        a: 'Almost certainly yes. A military buyback deposit costs 3% of your active-duty base pay (plus interest for periods after 1985 without a deposit). For a 4-year enlistment at typical enlisted pay, the deposit might run $3,000 to $5,000 total. That buys you 4 additional years in your FERS creditable service calculation, increasing your annuity by 4% of your high-3 forever. At a $120,000 high-3, that is $4,800 per year for life.',
      },
    ],
  },
  {
    slug: 'department-of-homeland-security',
    name: 'Department of Homeland Security',
    shortName: 'DHS',
    employeeCount: '250,000+ employees across all components',
    metaTitle: 'DHS Employee FERS Retirement Planning | PlanWell',
    metaDescription:
      'Free FERS retirement workshop for DHS employees. TSA, CBP, USCIS, FEMA, Secret Service. LEO special provisions, TSP, FEHB explained. Expert CFP guidance.',
    heroEyebrow: 'Department of Homeland Security',
    heroHeading: 'FERS Retirement Planning for DHS Employees',
    heroLead:
      'DHS is a patchwork of components, each with its own mission, pay structure, and retirement considerations. Whether you are a CBP officer with special provisions at age 57, a USCIS adjudicator on a GS schedule, or a FEMA disaster-response employee with irregular high-3 years, the details of your FERS plan look different from anyone else at your table.',
    introHtml: `
      <p>DHS components have a higher concentration of law enforcement special-provision employees than almost any other civilian agency. CBP, Secret Service, ICE, and HSI employees retire under a fundamentally different formula from their non-LEO colleagues: 1.7% per year for the first 20 years, mandatory separation at 57, and a retirement age as young as 50 with 20 years. Most financial advisors have never heard of any of this.</p>
      <p>PlanWell's workshop covers both LEO special-provision math and standard FERS in the same session, with breakout scenarios so each employee works the numbers that actually apply to them. Our CFP and ChFEBC team has run this workshop with CBP officers in Laredo, FEMA analysts in DC, and TSA screeners in Atlanta. The rules are different for each group, and we know which rules apply where.</p>
    `,
    whyMattersHtml: `
      <p>For DHS law enforcement officers, retirement timing is not a choice, it is a deadline. CBP officers and Secret Service agents covered under the LEO special provision must retire by age 57 with 20 years, or at any age with 25 years. If you hit 57 without 20 years, you lose the LEO annuity enhancement and revert to regular FERS rules. Missing this window by even one pay period can cost $40,000 to $80,000 in cumulative annuity over a 25-year retirement.</p>
      <p>For non-LEO DHS employees, the challenge is different. FEMA's surge-hiring model and TSA's frontline turnover create employees with non-linear career histories, part-time periods, and service credit gaps that need to be audited before retirement. A USCIS adjudicator with 25 years of service who took an 18-month break in the late 1990s may have a creditable service calculation that looks different from what their SF-50 suggests. We catch these gaps before they become surprises.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'CBP and Secret Service mandatory retirement',
        body:
          'Law enforcement officers at CBP, Secret Service, ICE, and certain other DHS components are subject to mandatory retirement at age 57. This is not optional. If you reach 57 before completing 20 years of LEO service, the agency can separate you and you revert to standard FERS rules. The earlier you map your creditable LEO service, the more accurately you can plan your separation date.',
      },
      {
        title: 'TSA employee retirement system differences',
        body:
          'TSA screeners hired before the Aviation and Transportation Security Act reforms were covered under unique employment authorities. If you are a long-tenured TSA employee, confirm whether your early service years count as FERS creditable service at the standard rate. The agency has had several HR system migrations that occasionally affect service credit records.',
      },
      {
        title: 'FEMA disaster deployment and high-3',
        body:
          'FEMA employees who deploy to disaster operations may receive additional pay, hazard pay, or overtime that does not count toward their high-3. Your high-3 is based on basic pay including locality, not total compensation. If your highest-earning years included significant disaster deployment premiums, your retirement estimate using gross earnings will be overstated.',
      },
      {
        title: 'USCG commissioned officers vs. civilian workforce',
        body:
          'The U.S. Coast Guard is part of DHS, but commissioned officers are military personnel under the Uniformed Services Retirement System, not FERS. If you are a USCG civilian employee, you are in FERS. If you are a former USCG officer who transferred to a civilian DHS position, your military time may count toward FERS with a military deposit, and your retirement math involves both systems.',
      },
    ],
    commonQuestionsHtml: `
      <p>The questions we hear most from DHS employees are: "Do I qualify for LEO special provisions or am I under regular FERS?", "What happens to my FERS supplement if I go back to work in private security after I retire?", and "How do I calculate my high-3 when my pay varied widely during surge periods?" All three require agency-specific analysis, not generic answers.</p>
    `,
    specialProvisionsNote:
      'DHS law enforcement officers at CBP, Secret Service, ICE, HSI, and certain other components qualify for FERS special provisions: a 1.7% accrual rate for the first 20 years of LEO service, mandatory retirement at age 57, and eligibility as early as age 50 with 20 years of LEO service. Confirming your LEO coverage code on your SF-50 (retirement coverage "E" or "KE") is the first step.',
    commonJobs: [
      'CBP officers and agents (GS-1895)',
      'USCIS immigration officers and adjudicators',
      'FEMA emergency management analysts',
      'TSA transportation security officers',
      'Secret Service special agents',
      'ICE and HSI special agents',
    ],
    primaryLocations: [
      'Washington, DC (HQ)',
      'El Paso and Laredo, TX (CBP)',
      'Miami, FL (ICE/HSI)',
      'Emmitsburg, MD (FEMA training)',
      'San Diego, CA (CBP)',
      'New York, NY (multi-component)',
    ],
    relatedAgencySlugs: ['department-of-defense', 'department-of-justice', 'department-of-veterans-affairs'],
    faq: [
      {
        q: 'How do I know if I am covered under FERS LEO special provisions at DHS?',
        a: 'Your SF-50 block 30 shows your retirement plan. Coverage code "E" or "KE" indicates law enforcement officer special provisions. You can also look for whether your agency deducts the LEO-rate FERS contribution (1.3% for FERS, 0.8% for FERS-FRAE). If you are unsure, ask your HR office for your retirement coverage determination letter. Do not assume based on your job title alone.',
      },
      {
        q: 'What is the LEO retirement formula and how does it compare to regular FERS?',
        a: 'Under the LEO special provision, your annuity accrues at 1.7% per year for your first 20 years of covered service, then 1.0% per year for each year after 20. Regular FERS accrues at 1.0% per year (1.1% at age 62 with 20+ years). For a DHS LEO retiring at 52 with exactly 20 years and a $110,000 high-3, the LEO formula gives you $37,400 per year versus $22,000 under regular FERS. That gap, $15,400 annually, is why the coverage determination matters.',
      },
      {
        q: 'I am a CBP officer at age 53 with 18 years of LEO service. Can I retire now?',
        a: 'Under the LEO special provision, you need 20 years of covered LEO service to retire early. At 18 years, you are not yet eligible unless you have 25 or more total years of federal service. Your best move is to complete the 20 LEO years if possible, then you qualify for the enhanced annuity regardless of age. Leaving at 18 years forces you into a deferred FERS annuity starting at age 62, with the regular 1.0% accrual rate, which is a significant financial step down.',
      },
      {
        q: 'Does FEMA overtime count toward my high-3?',
        a: 'No. Overtime, hazard pay, and most disaster-related premium pay do not count toward your high-3 average salary. Your high-3 is based on basic pay plus locality pay only. A FEMA employee who earns $95,000 base but $130,000 total during heavy deployment years will have a high-3 based on the $95,000 base, not the $130,000 gross. Use your basic pay from your leave and earnings statement, not your W-2 gross, for any retirement estimate.',
      },
      {
        q: 'What happens to my FERS supplement if I take a private security job after retiring from DHS?',
        a: 'The FERS supplement is subject to an earnings test. If you earn more than the Social Security exempt amount ($23,400 in 2025) from wages or self-employment after retirement, your supplement is reduced by $1 for every $2 of excess earnings. Private security work that pays $60,000 per year would reduce your supplement by approximately $19,000 annually. The supplement stops completely at age 62 regardless of earnings.',
      },
      {
        q: 'Can I keep FEHB in retirement after leaving DHS?',
        a: 'Yes, if you have maintained continuous FEHB enrollment for the 5 years immediately before your retirement date and you are retiring on an immediate annuity. For LEO special-provision retirees who separate at 50 to 52, this means verifying your FEHB enrollment history carefully, since some employees let coverage lapse during periods of hardship or career transition. A single gap breaks the 5-year rule.',
      },
    ],
  },
  {
    slug: 'us-postal-service',
    name: 'U.S. Postal Service',
    shortName: 'USPS',
    employeeCount: '~530,000 career employees (640,000+ total workforce including non-career)',
    metaTitle: 'USPS Employee FERS Retirement Planning | PlanWell',
    metaDescription:
      'Free retirement workshop for USPS career employees. FERS supplement, CSRS mix, USPS health plan transition. Expert CFP and ChFEBC guidance. Register free today.',
    heroEyebrow: 'U.S. Postal Service',
    heroHeading: 'FERS Retirement Planning for USPS Career Employees',
    heroLead:
      'USPS is one of the most complex retirement environments in the federal workforce. With approximately 530,000 career employees (and 640,000+ total workforce including non-career), you have the largest CSRS holdover population of any agency, a FERS workforce that depends heavily on the FERS supplement, and beginning in 2025, a transition to the new USPS Health Benefits Program that changes the FEHB equation entirely. Getting your retirement math right at USPS requires knowing which version of the rules applies to you.',
    introHtml: `
      <p>No other agency sends us as many employees asking about CSRS versus FERS as USPS does. Long-tenured letter carriers and mail processing clerks hired in the 1970s and early 1980s are still in CSRS, with 40+ year careers and annuities that can exceed $60,000 per year. Their colleagues hired after January 1, 1984 are in FERS, dependent on three income streams that need to be coordinated carefully. Both groups deserve a retirement plan built for their actual system.</p>
      <p>PlanWell has worked with postal employees from city carriers to plant managers to postmasters. The retirement questions are agency-specific in ways that matter: USPS has its own bargaining unit agreements, a unique approach to overtime pay and the high-3 calculation, and now a whole new health benefits system to understand. Our ChFEBC-credentialed team knows which answers apply to your career.</p>
    `,
    whyMattersHtml: `
      <p>For FERS postal employees, the FERS supplement is not a small extra, it is often the largest single retirement income source in the years between separation and Social Security eligibility at 62. A city carrier retiring at 57 with 30 years and a $75,000 high-3 will receive roughly a $22,500 FERS annuity plus a FERS supplement of approximately $14,000 to $18,000 per year until 62. Misunderstanding the supplement's earnings test can eliminate a third of your retirement income if you go back to work part-time.</p>
      <p>CSRS postal employees should be aware of recent Social Security law changes. The Social Security Fairness Act (Public Law 118-273), signed January 5, 2025, repealed the Windfall Elimination Provision (WEP) and the Government Pension Offset (GPO) for all benefits payable after December 2023. If you are a CSRS employee who also has Social Security credits from outside employment, those benefits are no longer reduced by WEP. We review your complete picture in the workshop.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'USPS Health Benefits Program transition',
        body:
          'Beginning in January 2025, USPS career employees transitioned from FEHB to the new USPS Health Benefits (USPSHB) Program. Employees who retire after January 1, 2025 will carry USPSHB coverage into retirement rather than FEHB. The 5-year continuous enrollment rule still applies, but the calculation now references USPSHB enrollment history. If you transitioned from FEHB to USPSHB without a gap, your prior FEHB years count toward the 5-year requirement.',
      },
      {
        title: 'CSRS holdover population',
        body:
          'USPS has one of the largest remaining CSRS populations in the federal government. If you were hired before January 1, 1984, you are likely in CSRS, which provides a richer pension formula but no employer TSP contributions and a Social Security offset if you have covered earnings. CSRS employees should be aware that the Social Security Fairness Act (signed January 5, 2025) repealed WEP and GPO for benefits payable after December 2023, which may increase any Social Security benefits they receive from outside employment.',
      },
      {
        title: 'Overtime and high-3 at USPS',
        body:
          'USPS overtime is widespread, particularly in mail processing operations. Overtime pay does not count toward your high-3. Your high-3 is calculated from basic pay, including any USPS locality equivalent, but not premium pay, overtime, or night-shift differentials. Employees who work heavy overtime often overestimate their high-3 by 15% to 25% if they use gross earnings instead of basic pay.',
      },
      {
        title: 'Rural carriers and FERS supplement timing',
        body:
          'Rural Carrier Associates (RCAs) and rural carriers have complex service credit questions tied to their pre-career appointment type. Hours worked as a non-career employee generally do not count as FERS creditable service. Verify your SCD (service computation date) on your leave and earnings statement against your hire history to confirm what years actually count toward your annuity.',
      },
    ],
    commonQuestionsHtml: `
      <p>The questions USPS employees bring most often are: "Does my overtime count in my high-3?", "What is the FERS supplement and when does it stop?", and "I was hired in 1982, am I in CSRS or FERS?" The CSRS/FERS question alone has a nuanced answer for employees hired between 1982 and 1987 who may have switched systems or been auto-enrolled incorrectly. We check your SF-50 in the workshop and confirm.</p>
    `,
    commonJobs: [
      'City and rural letter carriers',
      'Mail processing clerks',
      'Postmasters and supervisors',
      'Maintenance mechanics and technicians',
      'Mail handlers',
      'Window clerks (retail associates)',
    ],
    primaryLocations: [
      'Washington, DC (HQ and L\'Enfant Plaza)',
      'Shoreham Building, DC',
      'Atlanta, GA (Southern Area)',
      'Memphis, TN (network distribution)',
      'Chicago, IL (bulk mail center)',
      'Los Angeles, CA (Pacific Area)',
      'Pittsburgh, PA (mail processing)',
    ],
    relatedAgencySlugs: ['department-of-veterans-affairs', 'social-security-administration', 'department-of-labor'],
    faq: [
      {
        q: 'I am a USPS letter carrier. Does my overtime pay count toward my high-3?',
        a: 'No. Overtime pay, Sunday premium pay, and night-shift differentials do not count toward your FERS high-3. Your high-3 is calculated from your basic annual rate of pay, including any applicable USPS locality pay equivalent, averaged over your three highest consecutive years. A carrier earning $75,000 basic pay but $95,000 in gross wages due to heavy overtime will have a high-3 based on the $75,000 basic rate.',
      },
      {
        q: 'What is the FERS supplement and how much will I receive?',
        a: 'The FERS supplement bridges the gap between your retirement date and age 62, when Social Security begins. It is calculated to approximate the Social Security benefit you earned during your FERS career. A rough estimate: divide your years of FERS service by 40, then multiply by your age-62 Social Security estimate. For a carrier with 30 years of service and a projected $24,000 age-62 Social Security benefit, the supplement would be approximately $18,000 per year. It ends completely at 62, so budget for that income drop.',
      },
      {
        q: 'I was hired at USPS in 1983. Am I in CSRS or FERS?',
        a: 'Employees hired between January 1, 1982 and December 31, 1986 may be in CSRS, CSRS Interim, or FERS depending on whether they elected to switch during the 1987 open enrollment window. Check block 30 of your SF-50: "1" means CSRS, "6" means FERS, "C" means CSRS Offset. If you are in CSRS, your retirement formula is entirely different from FERS, and you need a separate planning conversation.',
      },
      {
        q: 'How does the USPS Health Benefits transition affect my retirement healthcare?',
        a: 'Starting January 2025, USPS career employees enrolled in the USPS Health Benefits Program (USPSHB) rather than FEHB. The 5-year continuous enrollment requirement to carry coverage into retirement still applies. OPM has confirmed that continuous FEHB enrollment before the January 2025 transition counts toward your 5-year total. As long as you did not have a gap in coverage, your prior FEHB years and your USPSHB years combine to meet the requirement.',
      },
      {
        q: 'Can I retire from USPS and then work at another federal agency?',
        a: 'Yes, with important caveats. If you retire on an immediate FERS annuity and return to federal service, your annuity typically continues but your new salary may be offset if you are reemployed in the same position type. More importantly, if you are receiving the FERS supplement and earn more than the Social Security annual exempt amount from any wages, your supplement is reduced. Returning to federal service usually counts as wages for the earnings test.',
      },
      {
        q: 'Does USPS have early retirement incentive offers?',
        a: 'USPS has used VERA (Voluntary Early Retirement Authority) in various restructuring efforts. Under VERA, eligible employees with 20 years of service at age 50, or 25 years at any age, can separate with an immediate FERS annuity. The annuity is not reduced for age but is calculated on actual service and high-3. If USPS offers VSIP alongside VERA, the lump-sum payment is fully taxable as ordinary income in the year received. We model both scenarios in the workshop.',
      },
    ],
  },
  {
    slug: 'internal-revenue-service',
    name: 'Internal Revenue Service',
    shortName: 'IRS',
    employeeCount: '90,000+ employees (Treasury Department)',
    metaTitle: 'IRS Employee FERS Retirement Planning | PlanWell',
    metaDescription:
      'Free FERS retirement workshop for IRS employees. High-3, TSP, FEHB, and Inflation Reduction Act hiring wave explained. CFP and ChFEBC guidance. Register free.',
    heroEyebrow: 'Internal Revenue Service',
    heroHeading: 'FERS Retirement Planning for IRS Employees',
    heroLead:
      'IRS employees spend their careers helping enforce the tax code, which makes it quietly ironic that many of them have not optimized the tax treatment of their own retirement. Your TSP is one of the most powerful tax-deferral tools available, your FERS annuity is taxed as ordinary income, and coordinating withdrawals across those two streams can make a meaningful difference in what you keep after retirement.',
    introHtml: `
      <p>The IRS went through a significant hiring expansion beginning in 2022 under the Inflation Reduction Act, adding thousands of revenue agents, tax examiners, and IT specialists over a two-year period. If you are part of that wave, your career timeline is compressed and your retirement planning questions look different from a 25-year IRS veteran. You may be asking about SCD, military buybacks, and TSP contribution strategies for a career that might run 20 to 25 years rather than 35.</p>
      <p>For longer-tenured IRS employees, particularly those approaching the end of a 30+ year career in field operations, criminal investigation, or appeals, the questions shift to TSP withdrawal sequencing, FEHB plan selection, and whether to take a lump-sum refund of FERS contributions versus the full annuity. PlanWell's team has worked with IRS employees at every career stage, from Ogden clerks to Washington executives, and the planning is always more specific than generic federal retirement advice.</p>
    `,
    whyMattersHtml: `
      <p>The IRS retirement community tends to be financially literate, which creates a specific risk: overconfidence in estimates. We see IRS employees who have read every OPM publication, run their own high-3 calculations, and still miss the interaction between FERS annuity taxation and TSP Roth conversions. If you are drawing a $55,000 taxable FERS annuity plus $30,000 from a traditional TSP, converting some TSP to Roth before retirement could save you $4,000 to $8,000 annually in taxes. The math is available, but most people do not run it.</p>
      <p>IRS Criminal Investigation special agents are covered under the LEO special provision, which fundamentally changes their retirement timeline and formula. CI agents who transfer to non-LEO positions mid-career need to understand how that service credit split affects their ultimate annuity. Blended LEO and non-LEO service is calculated differently from pure LEO or pure regular FERS, and getting it wrong produces an annuity estimate that is off by years and dollars.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'IRS CI agents and LEO special provisions',
        body:
          'IRS Criminal Investigation special agents are covered under FERS LEO special provisions, with the same 1.7% first-20-years accrual and mandatory retirement at age 57 that applies to FBI and DEA agents. If you are a CI agent who transferred to a revenue agent or compliance position, the service you spent in CI counts as LEO service and the rest counts as regular FERS. The calculation is a blended formula, and it favors maximizing your LEO years.',
      },
      {
        title: 'IRA hiring wave and shorter career timelines',
        body:
          'Employees hired after 2022 under the IRA expansion are in FERS-FRAE, which requires a higher employee contribution rate (4.4% rather than 0.8%). Your take-home pay reflects this, but your benefit formula is identical to older FERS. For a new hire projecting a 20-year career to age 62, the key question is whether a full FERS annuity makes sense or whether maximizing TSP contributions for a potential private-sector transition is the better strategy.',
      },
      {
        title: 'Seasonal and intermittent employment history',
        body:
          'The IRS historically hired large seasonal workforces for filing season. If any of your early IRS career involved temporary, seasonal, or intermittent appointments, those periods may not count as FERS creditable service. Your SCD on your current pay stub should reflect only the creditable service OPM recognizes. Confirm it matches your expectation before you build a retirement date around it.',
      },
      {
        title: 'TSP tax strategy for high earners',
        body:
          'Senior IRS executives and long-tenured revenue agents often have high-3 salaries in the $150,000 to $200,000 range, large traditional TSP balances, and Social Security benefits. In retirement, combined income from these sources can push them into the 22% to 24% bracket. Pre-retirement Roth TSP contributions and strategic Roth conversions during low-income years between retirement and Social Security claiming are tools worth modeling before you separate.',
      },
    ],
    commonQuestionsHtml: `
      <p>IRS employees most frequently ask: "How is my FERS annuity taxed compared to my TSP withdrawals?", "I was hired in 2023, what does FERS-FRAE mean for my benefits?", and "I am an IRS CI agent approaching 57, what is my mandatory retirement date?" All three questions have specific numerical answers that depend on your individual career history, and we work through each in the workshop.</p>
    `,
    specialProvisionsNote:
      'IRS Criminal Investigation (CI) special agents qualify for FERS LEO special provisions, including the 1.7% accrual rate for the first 20 years of LEO service and mandatory retirement at age 57. Agents who transferred from CI to non-LEO positions carry their LEO service credit forward in a blended calculation.',
    commonJobs: [
      'Revenue agents and revenue officers',
      'Tax examiners and tax compliance officers',
      'IRS Criminal Investigation special agents',
      'Appeals officers',
      'IT specialists and cybersecurity analysts',
      'Human capital and administrative staff',
    ],
    primaryLocations: [
      'Washington, DC (National Office)',
      'Ogden, UT (service center)',
      'Kansas City, MO (service center)',
      'Atlanta, GA (Chamblee campus)',
      'Austin, TX (service center)',
      'Andover, MA (service center)',
      'Fresno, CA (service center)',
    ],
    relatedAgencySlugs: ['department-of-justice', 'department-of-the-treasury', 'social-security-administration'],
    faq: [
      {
        q: 'How is my FERS annuity taxed compared to my TSP in retirement?',
        a: 'Your FERS annuity is fully taxable as ordinary income, minus a small pro-rated exclusion for your after-tax contributions to FERS (typically less than 2% of each payment). Your traditional TSP withdrawals are also fully taxable as ordinary income. Roth TSP withdrawals are tax-free if you have held the account for 5 years and are over 59.5. The combination of annuity plus TSP RMDs is where IRS retirees often find themselves pushed into higher brackets than expected.',
      },
      {
        q: 'I was hired in 2023 under the IRA funding. What is FERS-FRAE and does it change my benefits?',
        a: 'FERS-FRAE (Further Revised Annuity Employees) applies to employees hired after December 31, 2013. You contribute 4.4% of your basic pay toward FERS rather than the 0.8% rate under older FERS. Your benefit formula is identical: 1% per year of creditable service times your high-3 (1.1% if you retire at 62 or later with 20+ years). The only difference is the cost to you. Your retirement benefit is the same as a colleague hired in 2010.',
      },
      {
        q: 'I am an IRS CI special agent turning 57 next year. Do I have to retire?',
        a: 'Yes, if you have 20 or more years of LEO-covered service. The mandatory separation rule for FERS law enforcement officers is age 57 with 20 qualifying years, unless your agency grants a limited extension. IRS CI has used such extensions in specific circumstances, but they are not guaranteed. If you have fewer than 20 years of LEO service at 57, the mandatory separation does not apply, but your annuity reverts to the standard FERS formula for any non-LEO service.',
      },
      {
        q: 'My IRS career started as a seasonal employee. Does that time count toward my FERS annuity?',
        a: 'Seasonal and intermittent appointments generally do not count as FERS creditable service unless you were in a covered position contributing to the retirement fund. Check your official SCD (service computation date) on your current leave and earnings statement. If your SCD is later than your first day of IRS employment, the gap likely reflects non-creditable time. An HR records audit can confirm exactly which periods are included.',
      },
      {
        q: 'Should I contribute to traditional TSP or Roth TSP as an IRS employee?',
        a: 'It depends on where you expect your tax rate to be in retirement. If you have a large traditional TSP balance and will also receive a taxable FERS annuity and Social Security, your retirement income may be taxed at 22% or higher. In that case, contributing to Roth TSP now and paying taxes at your current rate can be advantageous if your current rate is below your expected retirement rate. Many senior IRS employees in the $130,000 to $180,000 salary range benefit from a split contribution strategy.',
      },
      {
        q: 'Can I retire before 57 as a non-CI IRS employee?',
        a: 'Yes. Non-LEO IRS employees can retire at their Minimum Retirement Age (57 for those born in 1970 or later) with 30 or more years of service, at age 60 with 20 years, or at age 62 with as few as 5 years. An unreduced annuity at MRA requires 30 years of creditable service. With 10 to 29 years at MRA, the annuity is reduced by 5% for each year under age 62 unless you defer the annuity to age 62.',
      },
    ],
  },
  {
    slug: 'department-of-justice',
    name: 'Department of Justice',
    shortName: 'DOJ',
    employeeCount: '115,000+ employees across all components',
    metaTitle: 'DOJ Employee FERS Retirement | FBI, DEA, ATF | PlanWell',
    metaDescription:
      'Free FERS retirement workshop for DOJ employees. FBI, DEA, ATF, USMS, BOP. LEO special provisions at 57 explained by CFP and ChFEBC experts. Register free.',
    heroEyebrow: 'Department of Justice',
    heroHeading: 'FERS Retirement Planning for DOJ Employees',
    heroLead:
      'DOJ has the most concentrated population of law enforcement special-provision employees in the federal government. FBI agents, DEA investigators, ATF special agents, U.S. marshals, and Bureau of Prisons officers all face a mandatory retirement age of 57, a 1.7% pension accrual rate for the first 20 years, and a retirement decision that carries six-figure consequences if you time it wrong.',
    introHtml: `
      <p>If you work at the FBI, DEA, ATF, USMS, or BOP in a covered law enforcement position, your retirement is not like your non-LEO colleagues at DOJ. The formula is richer, the timeline is compressed, and the mandatory retirement clock is running whether you are paying attention to it or not. A DOJ LEO with 20 years of service and a $130,000 high-3 retiring at 52 receives roughly $44,200 per year under the LEO formula. Under regular FERS with the same service and salary, that number drops to $26,000. The difference, $18,200 per year, is what understanding your coverage is worth.</p>
      <p>PlanWell works with DOJ employees across all components. Our ChFEBC designation means we know the LEO special provision calculation, the survivor benefit election mechanics for law enforcement spouses, and how the FERS supplement interacts with post-retirement consulting income common among former FBI agents. The planning conversation at DOJ is almost always more urgent than employees realize until they are six months from mandatory separation.</p>
    `,
    whyMattersHtml: `
      <p>The mandatory retirement cliff at DOJ is real, and it catches people off guard. A BOP correctional officer who reaches age 57 with 23 years of LEO service will be separated involuntarily if the agency does not grant an extension. The annuity at that point is based on actual service, not a projected 25 or 30 years. Every year of LEO service you do not complete is a year of the 1.7% formula you leave on the table permanently.</p>
      <p>DOJ also has a significant population of attorneys, paralegals, and administrative staff who are not LEO-covered but share office space with agents who are. It is common for non-LEO DOJ employees to misunderstand their own retirement system because they hear LEO rules constantly. If you are a trial attorney in a U.S. Attorney's Office, you are under standard FERS, not the LEO special provision, and your retirement planning is different in every material respect.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'FBI, DEA, ATF mandatory retirement at 57',
        body:
          'Federal law enforcement officers at DOJ components, including FBI, DEA, ATF, and USMS, must retire at age 57 with 20 or more years of covered LEO service. Agencies can grant limited extensions to age 60 in exceptional circumstances, but extensions are not routine. If you will reach 57 before 20 years, you separate without the LEO premium and under standard FERS rules. Map your exact LEO service history against your birthday now.',
      },
      {
        title: 'Bureau of Prisons and correctional officer provisions',
        body:
          'BOP correctional officers are covered under the LEO special provision if their primary duty is the custody of federal prisoners. Shift supervisors and associate wardens in correctional roles are also typically covered. Administrative staff at BOP facilities are not. The distinction matters because BOP employees in admin roles sometimes assume they have LEO coverage based on their work environment rather than their official position description.',
      },
      {
        title: 'Prior military service and LEO deposit timing',
        body:
          'DOJ agents who served in the military before their law enforcement career should buy back that military service time. The deposit (3% of military base pay plus interest for post-1956 service) can add years to your creditable service calculation. For a DEA agent with 4 years of military service who pays the deposit, those years count toward both the creditable service total and the LEO-specific 20-year threshold. Time the deposit early, because OPM takes several months to process.',
      },
      {
        title: 'Survivor benefit election for law enforcement families',
        body:
          'The survivor benefit election at retirement is among the most consequential decisions a DOJ LEO makes. Electing full survivor benefit reduces your annuity by 10% but provides your spouse a lifetime income stream if you die first. The typical DOJ retiree who elects no survivor benefit to preserve full annuity income is making a bet that their spouse will not outlive them. We model the break-even in every workshop session.',
      },
    ],
    commonQuestionsHtml: `
      <p>The top questions from DOJ employees are: "Do I qualify for LEO special provisions or am I under regular FERS?", "What is my mandatory retirement date and how do I calculate it?", and "Should I elect the survivor benefit or buy life insurance instead?" All three answers are specific to your position, service history, and family situation. We work through them with real numbers in the workshop.</p>
    `,
    specialProvisionsNote:
      'DOJ law enforcement officers at the FBI, DEA, ATF, USMS, and BOP (in correctional officer positions) are covered under FERS LEO special provisions: a 1.7% annuity accrual rate for the first 20 years of covered service, plus 1.0% per year after that, with mandatory retirement at age 57 and early retirement eligibility at age 50 with 20 LEO years.',
    commonJobs: [
      'FBI special agents',
      'DEA special agents and diversion investigators',
      'ATF special agents and industry operations inspectors',
      'U.S. marshals and deputy marshals',
      'BOP correctional officers and staff',
      'DOJ trial attorneys and paralegals',
    ],
    primaryLocations: [
      'Washington, DC (Main Justice)',
      'Quantico, VA (FBI Academy)',
      'Springfield, VA (DEA HQ)',
      'Washington, DC (ATF HQ)',
      'Kansas City, MO (USMS training)',
      'Glynco, GA (BOP training)',
      'New York, NY (SDNY and EDNY)',
    ],
    relatedAgencySlugs: ['department-of-homeland-security', 'department-of-defense', 'internal-revenue-service'],
    faq: [
      {
        q: 'What is the LEO retirement formula for FBI and DEA agents?',
        a: 'For the first 20 years of covered LEO service, your annuity accrues at 1.7% per year times your high-3. For each year beyond 20, the rate drops to 1.0%. An FBI agent with exactly 25 years of LEO service and a $145,000 high-3 would receive: (20 x 1.7% x $145,000) + (5 x 1.0% x $145,000) = $49,300 + $7,250 = $56,550 per year before survivor benefit and other adjustments. The same service under regular FERS would yield $36,250. The LEO premium is $20,300 per year.',
      },
      {
        q: 'What is mandatory retirement for DOJ law enforcement and can it be extended?',
        a: 'The mandatory retirement age for covered FERS law enforcement officers is 57 with 20 or more years of LEO service. Agencies may request an extension to age 60, but it requires formal approval and is not guaranteed. Extensions are most commonly granted for ongoing investigations or specialized expertise. Do not plan your retirement timeline around an extension. Plan around your mandatory separation date and treat any extension as a bonus.',
      },
      {
        q: 'I am a BOP correctional officer. Am I covered under LEO special provisions?',
        a: 'Most BOP correctional officers are covered, but coverage is tied to your official position description and primary duty designation, not just your work location. Officers whose primary duty is the custody and control of federal inmates are covered. If you have moved into a supervisory or administrative role that no longer involves primary inmate contact, your LEO coverage may have changed. Pull your most recent SF-50 and look at block 30 for coverage code "E" or "KE."',
      },
      {
        q: 'Should I elect the survivor benefit reduction for my spouse?',
        a: 'This is the retirement decision DOJ employees most often regret getting wrong. The full survivor benefit reduces your annuity by 10% permanently but provides your spouse 50% of your unreduced annuity for life. If you die first at age 65 and your spouse lives to 85, that is 20 years of survivor income. The break-even for most couples is 10 to 12 years. The question is not just actuarial, it is also about whether your spouse could sustain their lifestyle without the survivor benefit if you died in your first year of retirement.',
      },
      {
        q: 'I have prior military service before joining the FBI. Should I buy it back?',
        a: 'Almost certainly yes, particularly because at DOJ your military time potentially counts toward the 20-year LEO service threshold. A buyback deposit of approximately $4,000 to $8,000 for 4 years of military service could add those years to both your creditable service total and your LEO service count, pushing you past the 20-year LEO retirement floor earlier. Timing matters: submit your deposit application at least 18 months before your intended retirement date to allow for OPM processing.',
      },
      {
        q: 'I am a DOJ trial attorney, not a special agent. Am I under LEO special provisions?',
        a: 'No. Attorneys, paralegals, and administrative staff at Main Justice, U.S. Attorney offices, and the Executive Office for U.S. Attorneys are under standard FERS, not LEO special provisions. Your MRA is 57 (for those born in 1970 or later) and you need 30 years for an unreduced annuity at MRA. You do not have a mandatory retirement age. Your annuity accrues at 1.0% per year (1.1% at 62 with 20+ years). The LEO rules you hear about from agent colleagues do not apply to your retirement.',
      },
    ],
  },
  {
    slug: 'department-of-state',
    name: 'Department of State',
    shortName: 'State',
    employeeCount: '75,000+ civil service and Foreign Service employees',
    metaTitle: 'State Department FERS & FSPS Retirement | PlanWell',
    metaDescription:
      'Free retirement workshop for State Department civil service and Foreign Service employees. FSPS, FERS, overseas pay, and FEHB explained. Expert CFP guidance.',
    heroEyebrow: 'Department of State',
    heroHeading: 'Retirement Planning for State Department Employees',
    heroLead:
      'The State Department has two distinct retirement systems running simultaneously: FERS for civil service employees and the Foreign Service Pension System (FSPS) for Foreign Service officers and specialists. If you are in the Foreign Service, your retirement math is fundamentally different from your civil service colleagues in the same building, and the career interruptions, post differentials, and hardship pay that define overseas service add layers of complexity that most financial advisors cannot untangle.',
    introHtml: `
      <p>Foreign Service officers accumulate service credit, high-3 calculations, and retirement eligibility under FSPS rules that track closely to FERS but diverge in important ways at the margins. The normal retirement age for FSPS is different, mandatory retirement applies to some senior Foreign Service positions, and the salary base for your high-3 can include or exclude overseas differentials depending on how your specific assignments were classified. Getting this right requires someone who has studied the Foreign Affairs Manual, not just the CFR.</p>
      <p>Civil service employees at State, including those who work overseas in civil service-designated positions, are in FERS and follow standard FERS rules. But even for civil service employees at State, the high-3 calculation can be tricky when your career includes periods of overseas locality pay, difficult-to-service differentials, and danger pay, none of which count toward your pension base. PlanWell works with both Foreign Service and civil service State employees and knows which rules apply to each.</p>
    `,
    whyMattersHtml: `
      <p>For Foreign Service employees, the risk of a miscalculated high-3 is acute. A Foreign Service officer who spent their final three years at a hardship post in Kabul earning base pay plus a 35% hardship differential and a 25% danger pay differential may assume their total earnings determine their high-3. They do not. The high-3 is based on basic salary only, and a FS-03 step 10 in Washington might have a lower actual high-3 than they projected by $30,000 to $50,000 if they counted the differentials.</p>
      <p>The mandatory separation rules in the Foreign Service add urgency that civil service employees do not face. Senior Foreign Service officers who do not receive tenure or are selected out must separate. Planning for the possibility of early separation, and ensuring TSP and FSPS benefits are optimized if that happens, requires a contingency plan that most Foreign Service employees do not have written down anywhere.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'Foreign Service Pension System vs. FERS',
        body:
          'Foreign Service officers and specialists are covered under the Foreign Service Pension System (FSPS) if hired after December 31, 1983, or the older Foreign Service Retirement and Disability System (FSRDS) if hired earlier. FSPS tracks closely to FERS in many ways but has a different normal retirement eligibility structure and its own OPM form set. If you are in FSRDS, your plan is closer to CSRS and should be analyzed separately.',
      },
      {
        title: 'Overseas pay and the high-3 calculation',
        body:
          'Post differentials, hardship pay, danger pay, and foreign area allowances do not count toward your high-3. Only your basic salary and domestic locality pay (if any) feed the pension calculation. Foreign Service employees who spent their highest-earning years in hardship posts need to calculate their true high-3 using basic pay only, which can be significantly lower than total overseas compensation.',
      },
      {
        title: 'Mandatory retirement for senior Foreign Service',
        body:
          'Senior Foreign Service officers (FE-MC and above) face mandatory retirement upon reaching the maximum time-in-class limits. This creates a hard deadline that does not exist for GS civil service employees. If you are a Senior Foreign Service officer, your retirement planning window is shorter and more defined than peers at other agencies, and TSP allocation, FEHB continuation, and survivor elections should be addressed well before the deadline arrives.',
      },
      {
        title: 'FEHB while posted overseas',
        body:
          'Maintaining FEHB enrollment is critical for Foreign Service employees because it is your primary retirement health coverage. Some Foreign Service employees drop FEHB during long overseas tours because the government-provided medical at post covers their needs. Dropping FEHB creates a gap in the 5-year continuous enrollment required to carry it into retirement. If you are posted overseas, keep your FEHB enrollment active, even if you are not using it.',
      },
    ],
    commonQuestionsHtml: `
      <p>State Department employees most often ask: "I am in the Foreign Service, am I in FERS or FSPS?", "Do my hardship and danger pay differentials count toward my retirement pension?", and "What happens to my FEHB if I am posted abroad for 4 years?" Each question has a specific answer that depends on your appointment type, assignment history, and enrollment records. We walk through all three in the workshop.</p>
    `,
    commonJobs: [
      'Foreign Service officers (political, economic, consular, management)',
      'Foreign Service specialists (security, IT, office management)',
      'Civil service program analysts and policy advisors',
      'Diplomatic security agents',
      'Consular officers',
      'Administrative and financial management staff',
    ],
    primaryLocations: [
      'Washington, DC (Foggy Bottom HQ)',
      'Rosslyn, VA (support offices)',
      'Foreign Service Institute (Arlington, VA)',
      'New York, NY (UN Mission)',
      'Overseas embassies and consulates (global)',
      'Frankfurt, Germany (regional support)',
    ],
    relatedAgencySlugs: ['department-of-defense', 'department-of-homeland-security', 'department-of-justice'],
    faq: [
      {
        q: 'Am I in FERS or the Foreign Service Pension System?',
        a: 'Your retirement system depends on your appointment type. Civil service employees at State, hired through competitive civil service procedures and holding GS or SES positions, are in FERS (or CSRS if hired before 1984). Foreign Service officers and specialists appointed under the Foreign Service Act are in FSPS if hired after December 31, 1983, or FSRDS if hired earlier. Check your SF-50 block 30: code "6" is FERS, code "8" is FSPS.',
      },
      {
        q: 'Does my danger pay or hardship differential count toward my FSPS pension?',
        a: 'No. Danger pay, post differentials, hardship differentials, and foreign area allowances are excluded from the FSPS high-3 base salary calculation. Only your basic salary and any applicable domestic locality pay count. A Foreign Service officer earning $120,000 base plus a $42,000 hardship differential has a high-3 based on the $120,000, not the $162,000 total. Use your base salary line from your LES, not your gross pay.',
      },
      {
        q: 'I have been posted overseas for 3 years and let my FEHB lapse. Can I still retire with health coverage?',
        a: 'If your FEHB lapsed for any period during those 3 years, you may have broken the 5-year continuous enrollment requirement. Whether the gap affects your eligibility depends on exactly how long the lapse was and whether it fell within the 5-year window before your retirement date. Talk to your HR benefits specialist immediately. In some cases, a retroactive correction is possible; in others, the lapse permanently eliminates your FEHB retirement eligibility.',
      },
      {
        q: 'What is the normal retirement age for FSPS Foreign Service employees?',
        a: 'Under FSPS, the normal retirement age is 50 with 20 years of Foreign Service service, or age 60 with any amount of qualifying service. Senior Foreign Service officers may face mandatory retirement under time-in-class rules before reaching those thresholds. This is more generous than standard FERS in some respects, reflecting the career demands of overseas service. TSP and Social Security coordination still applies at the same ages as FERS.',
      },
      {
        q: 'I am a civil service State Department employee working in Washington. How is my high-3 different from a Foreign Service officer?',
        a: 'As a GS civil service employee, your high-3 is calculated the same way as any other FERS employee: the average of your three highest consecutive years of basic pay plus locality. Washington, DC locality pay runs roughly 33% above base, so your total high-3 base is higher than Foreign Service colleagues posted overseas without locality. Your retirement formula, MRA, and creditable service rules are standard FERS across the board.',
      },
      {
        q: 'Can I count my overseas years toward FERS creditable service?',
        a: 'Yes, absolutely. Civil service employees posted overseas on civil service-designated positions continue to accrue FERS creditable service during those assignments. Foreign Service employees in FSPS accrue FSPS creditable service. The overseas posting does not interrupt your service or create a gap in your retirement record, as long as you remain in a covered position. The only retirement-related risk during overseas assignments is the FEHB enrollment lapse issue covered above.',
      },
    ],
  },
  {
    slug: 'nasa',
    name: 'National Aeronautics and Space Administration',
    shortName: 'NASA',
    employeeCount: '18,000+ civil service employees',
    metaTitle: 'NASA Employee FERS Retirement Planning | PlanWell',
    metaDescription:
      'Free FERS retirement workshop for NASA engineers, scientists, and technicians. High-3, TSP, military buyback, and FEHB planning. Expert CFP guidance. Register free.',
    heroEyebrow: 'NASA',
    heroHeading: 'FERS Retirement Planning for NASA Civil Service Employees',
    heroLead:
      'NASA civil servants are among the most credentialed and well-paid employees in the federal government. Aerospace engineers, physicists, and research scientists at Johnson, Marshall, Goddard, and JPL often carry high-3 salaries in the $160,000 to $220,000 range, large TSP balances from maxing contributions for 30 years, and prior military service that can add years to their creditable service if the deposit is handled correctly.',
    introHtml: `
      <p>A NASA engineer retiring after 32 years with a $185,000 high-3 and a $1.2 million TSP balance is not a typical federal employee retirement. The numbers are larger, the tax implications are more significant, and the sequence of decisions, when to claim Social Security, how to withdraw from TSP without triggering avoidable tax brackets, whether to use Roth conversions before 72, matters more than it does for employees with more modest balances. PlanWell's CFP team specializes in the complex end of federal retirement planning.</p>
      <p>Many NASA civil servants came out of the military or the defense contractor world before transitioning to civil service. That background creates opportunities, military service buybacks, prior private-sector 401(k) rollovers into TSP, and potential dual retirement income, but it also creates complexity. We help you audit your full career picture before you lock in a retirement date.</p>
    `,
    whyMattersHtml: `
      <p>For NASA employees with large TSP balances, the sequence of withdrawals is a tax strategy as much as a retirement income strategy. If you have $1.5 million in traditional TSP, your Required Minimum Distributions starting at age 73 will be approximately $54,000 per year on top of your FERS annuity and Social Security. That combined income can push you firmly into the 24% or 32% bracket. Doing Roth TSP conversions in the years between retirement and age 70, when your income drops before RMDs begin, is a meaningful lever.',
      <p>NASA also has a meaningful population of employees with prior active-duty military service. A NASA engineer with 6 years of Air Force service who pays the military deposit adds 6 years of creditable service to their FERS calculation. At a $190,000 high-3, that is an additional $11,400 per year for life, plus a higher supplement and potentially an earlier unreduced retirement date. The deposit math almost always favors paying it.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'Military service deposits for prior active duty',
        body:
          'A significant portion of NASA civil servants are veterans. If you served on active duty before joining NASA, you can buy back that service time with a military deposit (3% of base pay for service before 1957 or after 1982, plus interest). For an engineer with 5 years of prior Air Force service and a $190,000 high-3, the deposit might cost $12,000 and return $9,500 per year more in annuity. That is a 1.3-year payback, permanent.',
      },
      {
        title: 'High-3 and senior executive pay',
        body:
          'NASA has a disproportionate number of employees at GS-14, GS-15, and Senior Executive Service levels, where salaries approach the federal pay cap. The federal pay cap in 2025 is $221,900. If you have reached the cap, your high-3 calculation is straightforward, but any bonus, award, or performance pay that pushed you over the cap in individual years did not count. Verify your capped years against your official leave and earnings statements.',
      },
      {
        title: 'TSP balance management and bracket optimization',
        body:
          'NASA employees frequently accumulate TSP balances over $1 million through decades of maximum contributions. At retirement, the interaction between FERS annuity, TSP withdrawals, and Social Security can create a tax burden that surprises people. Modeling your annual income in retirement, including eventual RMDs, before you separate lets you make TSP Roth conversion decisions intelligently rather than reactively.',
      },
      {
        title: 'JPL and contractor versus civil service status',
        body:
          'The Jet Propulsion Laboratory is managed by Caltech under contract to NASA. JPL employees are not NASA civil servants; they are Caltech employees covered by private-sector benefits. If you have worked at JPL under the contract before moving to a NASA civil service position at another center, your JPL service does not count as federal creditable service and does not roll into FERS. Verify your SCD reflects only your direct civil service tenure.',
      },
    ],
    commonQuestionsHtml: `
      <p>NASA employees most often ask: "I have $1.4 million in TSP, how do I withdraw it without getting destroyed by taxes?", "I served 8 years in the Air Force before NASA, should I buy back that time?", and "How do I coordinate my FERS annuity, TSP withdrawals, and Social Security to minimize my total tax burden?" These are exactly the high-stakes planning questions that require individual modeling, not generic answers.</p>
    `,
    commonJobs: [
      'Aerospace engineers and systems engineers',
      'Physicists and research scientists',
      'Computer scientists and software engineers',
      'Program and project managers',
      'Contracts and procurement specialists',
      'Flight directors and mission controllers',
    ],
    primaryLocations: [
      'Johnson Space Center (Houston, TX)',
      'Marshall Space Flight Center (Huntsville, AL)',
      'Goddard Space Flight Center (Greenbelt, MD)',
      'Kennedy Space Center (Cape Canaveral, FL)',
      'Langley Research Center (Hampton, VA)',
      'Ames Research Center (Moffett Field, CA)',
      'NASA Headquarters (Washington, DC)',
    ],
    relatedAgencySlugs: ['department-of-defense', 'department-of-energy', 'department-of-commerce'],
    faq: [
      {
        q: 'I served 7 years in the Air Force before joining NASA. Should I pay the military buyback deposit?',
        a: 'For most NASA engineers and scientists with high salaries, the answer is yes. The deposit costs 3% of your active-duty base pay (typically $25,000 to $45,000 total for 7 years, depending on your rank and year of service, plus interest). At a $185,000 high-3, adding 7 years of creditable service increases your annual annuity by $12,950 ($185,000 x 1% x 7). The deposit pays itself back in about 2 to 3 years of retirement. Submit your DD-214 and deposit application to your NASA HR office at least 18 months before retirement.',
      },
      {
        q: 'I have $1.6 million in TSP. What are my RMD obligations and how do they affect my taxes?',
        a: 'RMDs from traditional TSP begin at age 73. At age 73, with a $1.6 million balance, your first-year RMD would be approximately $60,150 (based on a 26.5 life expectancy divisor). Added to a $70,000 FERS annuity and $36,000 in Social Security, that is roughly $166,000 of taxable income, putting you squarely in the 22% to 24% federal bracket. Roth TSP conversions between retirement at 58 and your RMD start date can materially reduce that future tax exposure.',
      },
      {
        q: 'I am at GS-15 and approaching the federal pay cap. How does that affect my high-3?',
        a: 'The Executive Level IV pay cap limits GS-15 salaries at certain locality-adjusted rates. In 2025, the cap is $221,900. If your GS-15 step and locality combination exceeds the cap, your retirement-relevant basic pay is the capped amount, not the higher theoretically applicable rate. For high-cost locality areas like DC or San Jose, this means some GS-15 step 9 and 10 employees are effectively at the same high-3 regardless of step, because both are capped.',
      },
      {
        q: 'I worked at JPL for 8 years before transferring to Johnson Space Center as a civil servant. Does my JPL time count?',
        a: 'No. JPL is managed by the California Institute of Technology under a NASA contract. JPL employees are Caltech employees in the private sector, not federal civil servants. Your 8 years at JPL do not count as FERS creditable service and cannot be bought back. Your FERS service computation date (SCD) starts from your first day as a NASA civil servant. This is a common surprise for employees who made the JPL-to-civil-service transition mid-career.',
      },
      {
        q: 'Can I retire at my MRA with 30 years at NASA and keep all my benefits?',
        a: 'Yes. At MRA (57 for employees born in 1970 or later) with 30 or more years of FERS creditable service, you qualify for an immediate unreduced FERS annuity plus the FERS supplement (until age 62) plus the right to continue FEHB. The FERS supplement is subject to an earnings test if you return to work. Your TSP is accessible without the 10% early withdrawal penalty at age 55 or later in the year you separate, under the Rule of 55.',
      },
      {
        q: 'Is my FEGLI life insurance worth keeping in retirement?',
        a: 'It depends on your age and health. FEGLI Basic coverage in retirement is heavily subsidized and costs nothing if you elect the 75% reduction option (the premium is zero, but coverage erodes to 25% of the face amount by age 65). The problem is that if you need meaningful life insurance in retirement to protect a spouse, the death benefit may be too small after reductions. Many NASA retirees with large TSP balances do not need life insurance at all because the portfolio is the legacy. We compare the FEGLI retention cost against alternatives in the workshop.',
      },
    ],
  },
  {
    slug: 'department-of-health-and-human-services',
    name: 'Department of Health and Human Services',
    shortName: 'HHS',
    employeeCount: '80,000+ employees across all operating divisions',
    metaTitle: 'HHS Employee FERS Retirement Planning | PlanWell',
    metaDescription:
      'Free FERS retirement workshop for HHS, CDC, NIH, FDA, and CMS employees. Title 38 pay, TSP, FEHB coordination explained. Expert CFP and ChFEBC guidance.',
    heroEyebrow: 'Department of Health and Human Services',
    heroHeading: 'FERS Retirement Planning for HHS Employees',
    heroLead:
      'HHS spans CDC, NIH, FDA, CMS, HRSA, SAMHSA, and more, and its workforce ranges from epidemiologists with NIH salaries north of $200,000 to benefits examiners processing Medicaid claims at $55,000. The retirement planning questions are just as varied. What is consistent is that HHS employees often underestimate their FERS annuity because they overestimate how complicated the calculation will be, and that hesitation costs them planning time they cannot get back.',
    introHtml: `
      <p>NIH is one of the best-compensated scientific agencies in the federal government, and its senior researchers often approach or exceed the GS pay cap. FDA scientists and reviewers in the DC metro area earn significant locality pay. CDC epidemiologists and public health professionals span a wide salary range depending on their grade and posting. For all of them, the high-3 calculation, TSP strategy, and FEHB continuation decision are the same structural questions, but the dollar amounts matter a lot.</p>
      <p>HHS also includes the U.S. Public Health Service Commissioned Corps, a uniformed service whose officers are not in FERS. If you are a Commissioned Corps officer, your retirement is under the PHS retirement system, not FERS, and this workshop is not the right starting point. If you are a civil service employee at an agency that also employs Commissioned Corps officers (CDC, FDA, IHS, NIH), you are in FERS and everything we cover applies to you.</p>
    `,
    whyMattersHtml: `
      <p>For CMS employees who administer Medicare and Medicaid, the irony of being unclear on their own federal health benefits in retirement is not lost on them. CMS benefits examiners and policy analysts often know more about the healthcare system than any other group of federal employees, yet many have not run their own FEHB plan comparison or modeled their Medicare Part B premium in retirement. The enrollment decisions you make at age 64 and 11 months have lasting cost implications.</p>
      <p>NIH scientists and FDA medical officers who earn six-figure salaries need to think carefully about the tax treatment of their retirement income. A researcher with a $210,000 high-3 and a $1.1 million TSP balance will have a combined FERS annuity and RMD income that exceeds $150,000 per year in many scenarios. At that income level, Roth conversions in the first few years of retirement, before RMDs begin, can reduce lifetime tax exposure by $50,000 or more. Most federal employees are not running this analysis.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'NIH scientists and the federal pay cap',
        body:
          'Many NIH Principal Investigators and branch chiefs are compensated through Title 42 appointments that allow pay above the GS scale. If you are on a Title 42 appointment at NIH, your retirement may not be under standard FERS. Some Title 42 positions carry FERS coverage; others do not. Confirm your retirement coverage code on your SF-50 before assuming your NIH service is all counting toward a FERS pension.',
      },
      {
        title: 'FDA user fee salary supplementation',
        body:
          'FDA employees in certain centers have historically had salary levels supplemented by prescription drug user fee revenues, which can create pay structures different from standard GS. If your pay has been set through user fee supplementation or special hiring authority, confirm that all pay components count toward your high-3. Your HR specialist can pull your official basic pay history from the payroll system.',
      },
      {
        title: 'FEHB and Medicare coordination planning',
        body:
          'HHS employees who spend their careers administering Medicare have unique expertise here, but expertise does not always translate into personal action. The decision of when to enroll in Medicare Part B (and whether to keep FEHB or downgrade to a lower premium plan) is one of the highest-dollar retirement decisions HHS employees make. An FEHB plan that costs $300 per month in retirement paired with Medicare Part B at $174.70 per month in 2025 may or may not be worth $5,700 per year compared to Medicare Advantage alternatives.',
      },
      {
        title: 'CDC deployments and emergency response pay',
        body:
          'CDC employees who are deployed to disease outbreak responses or public health emergencies may receive additional pay, travel, or per diem during surge periods. Per diem and travel reimbursements are not income and never affect high-3. Overtime and hazard pay do not count toward high-3. Only basic pay and locality pay feed your pension calculation. A CDC epidemiologist who worked extensive overtime during a response year may misestimate their high-3 by 20% or more if using gross W-2 income.',
      },
    ],
    commonQuestionsHtml: `
      <p>The questions HHS employees ask most often are: "I am at NIH on a Title 42 appointment, am I in FERS?", "How do I coordinate FEHB with Medicare when I retire?", and "My high-3 is over $180,000 from my NIH salary, how do I minimize taxes on my TSP distributions?" Each requires a specific answer based on your appointment type, retirement date, and income projection.</p>
    `,
    commonJobs: [
      'NIH researchers and program officers',
      'FDA medical officers and drug reviewers',
      'CMS policy analysts and benefits examiners',
      'CDC epidemiologists and public health analysts',
      'HRSA and SAMHSA program officers',
      'HHS IT specialists and administrative staff',
    ],
    primaryLocations: [
      'Bethesda, MD (NIH campus)',
      'Rockville, MD (FDA HQ)',
      'Atlanta, GA (CDC campus)',
      'Baltimore, MD (CMS HQ)',
      'Washington, DC (HHS Humphrey Building)',
      'Research Triangle Park, NC',
      'Dallas, TX and Kansas City, MO (regional offices)',
    ],
    relatedAgencySlugs: ['department-of-veterans-affairs', 'social-security-administration', 'department-of-agriculture'],
    faq: [
      {
        q: 'I am at NIH on a Title 42 appointment. Am I in FERS?',
        a: 'It depends on how your Title 42 appointment was structured. Most Title 42(b) scientific research appointments at NIH include FERS coverage, but some Title 42(f) senior biomedical research service positions do not. Check block 30 of your SF-50. If it shows retirement coverage code "6" (FERS) or "K" (FERS-FRAE), you are in FERS and accruing toward a pension. If it shows "0" (not covered), your NIH service is not building a FERS annuity.',
      },
      {
        q: 'How do FEHB and Medicare Part B work together in retirement?',
        a: 'Most federal retirees keep FEHB and also enroll in Medicare Part B at age 65. When you have both, FEHB becomes secondary to Medicare, which often dramatically reduces your out-of-pocket healthcare costs. Many FEHB plans waive cost-sharing entirely when Medicare is primary. The combined premium (FEHB plus Part B) typically runs $450 to $650 per month in 2025. The question is whether the reduced cost-sharing is worth the total premium outlay compared to Medicare Advantage alternatives, which we model for your specific plan.',
      },
      {
        q: 'My CDC salary was $145,000 during outbreak response years when I worked significant overtime. What is my high-3?',
        a: 'Your high-3 is based on basic pay only. Overtime, hazard pay, and surge-response premium pay are excluded. Pull your leave and earnings statements for your three highest-pay years and use the basic pay line, not the total pay line. For a CDC GS-14 step 10 in Atlanta, basic pay plus Atlanta locality in 2025 is approximately $155,000 to $162,000. That is your high-3 ceiling if those were your peak years, regardless of what overtime added to your W-2.',
      },
      {
        q: 'I have 28 years at HHS and I am 59. Should I retire now or wait until 62 for the 1.1% accrual rate?',
        a: 'The 1.1% rate applies if you retire at age 62 or later with 20 or more years of creditable service. At 59 with 28 years, your annuity is calculated at 1.0% per year. Waiting until 62 with 31 years at 1.1% gives you a 7.7% higher annuity base (3 more years at 1.1% vs. 1.0%). On a $160,000 high-3, that is a difference of approximately $12,300 per year for life. Whether 3 more years of working earns that premium depends on your salary, the FERS supplement, and your personal circumstances.',
      },
      {
        q: 'Does the U.S. Public Health Service Commissioned Corps count as FERS service?',
        a: 'No. PHS Commissioned Corps officers are in the uniformed PHS retirement system, not FERS. However, former Commissioned Corps officers who transitioned to civil service positions at HHS, CDC, or FDA can sometimes count their uniformed service toward FERS through a military deposit, similar to the process for Army or Navy veterans. The deposit is 3% of base pay for the uniformed service period. Confirm with your HR office whether your specific PHS service qualifies.',
      },
      {
        q: 'I worked at CMS for 20 years and am considering leaving for a private insurance company. What happens to my FERS?',
        a: 'If you leave federal service before your Minimum Retirement Age, you can either take a refund of your FERS contributions (forfeiting the pension) or leave your contributions in place for a deferred annuity starting at age 62. The deferred annuity preserves all 20 years of creditable service at the 1.0% formula. On a $130,000 high-3, that is $26,000 per year starting at 62. Do not take the refund unless you need the cash and have run the long-term math against what you are giving up.',
      },
    ],
  },
  {
    slug: 'social-security-administration',
    name: 'Social Security Administration',
    shortName: 'SSA',
    employeeCount: '60,000+ employees nationwide',
    metaTitle: 'SSA Employee FERS Retirement Planning | PlanWell',
    metaDescription:
      'Free FERS retirement workshop for SSA employees. Claims examiners, field offices, TSP, FEHB, and Social Security coordination explained. Expert CFP guidance.',
    heroEyebrow: 'Social Security Administration',
    heroHeading: 'FERS Retirement Planning for SSA Employees',
    heroLead:
      'SSA employees spend their careers explaining Social Security benefits to the public, which creates a specific paradox: most of them understand Social Security better than any financial advisor they will ever meet, but they often have not integrated their own Social Security benefit into a complete retirement income plan alongside their FERS annuity and TSP. Those three income streams, when coordinated correctly, compound into a more resilient retirement than most federal employees realize.',
    introHtml: `
      <p>SSA field office employees, disability examiners, and teleservice representatives cover a wide salary range, typically GS-7 through GS-12 in most locations, with regional and metropolitan exceptions. The high-3 for most SSA employees is moderate compared to science agencies or defense, which means the FERS annuity is meaningful but not the dominant income source in retirement. TSP and Social Security take on proportionally more weight in your retirement income plan.</p>
      <p>PlanWell works with SSA employees who know the rules for everyone else and are now trying to apply them to themselves. The irony is not lost on anyone. What makes our workshop different is that we run the actual numbers for your salary, years of service, and expected Social Security benefit and show you what retirement looks like month by month. That specificity is what moves people from understanding to action.</p>
    `,
    whyMattersHtml: `
      <p>For SSA employees, the decision of when to claim Social Security is particularly consequential, and somewhat awkward to think about, because you have spent years telling the public how the system works. The personal decision is the same as for any federal employee: claiming at 62 gives you a benefit roughly 30% smaller than claiming at 70. If you retire from SSA at 57 with 30 years and have the FERS supplement bridging to 62, your decision on when to actually claim Social Security from 62 onward is worth mapping carefully against your other income sources.</p>
      <p>SSA has faced significant budget pressure and workforce reductions over the past decade, creating an environment where early retirement incentives, VERA offers, and involuntary separations are more common than at most agencies. If SSA offers a VERA or VSIP while you have 20 or more years of service and are at least 50 years old, the decision window is short and the financial analysis is urgent. We have run this calculation for SSA employees in multiple workforce reduction cycles.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'Social Security coordination from inside SSA',
        body:
          'SSA employees have access to their own Social Security earnings records and a deeper understanding of the benefit calculation than almost any other worker in the country. The question is not whether to claim but when and how to integrate it with FERS and TSP. For a married couple where one spouse is an SSA employee, spousal benefit coordination and survivor benefit strategies deserve specific modeling before the first claim is filed.',
      },
      {
        title: 'Budget-driven workforce reductions and VERA',
        body:
          'SSA has offered Voluntary Early Retirement Authority in multiple rounds. If you are age 50 with 20 years or any age with 25 years, a VERA offer gives you an immediate FERS annuity. The annuity is not reduced for early age, but it is based on actual service and high-3 at the time of separation. VSIP payments accompanying VERA are taxable as ordinary income. The combination is worth modeling before accepting.',
      },
      {
        title: 'Field office high-3 variation by locality',
        body:
          'SSA has field offices in every state, with significant locality pay variation. An SSA claims examiner in San Francisco earns roughly 44% more in locality than one in rural Oklahoma at the same GS grade. If you transferred between offices mid-career, your high-3 years are the ones that matter, and a transfer into a high-locality office in the final 3 to 5 years of your career can meaningfully increase your annuity.',
      },
      {
        title: 'Hearings operations and administrative law judge careers',
        body:
          'Administrative law judges (ALJs) at SSA are appointed under the Administrative Procedure Act and are paid under a separate AL pay schedule. ALJ salaries in 2025 range from AL-3/A through AL-1, with AL-1 topping out around $183,000. If you are an SSA ALJ, your high-3 is likely substantially higher than field office colleagues, and your FERS annuity correspondingly larger. TSP withdrawal tax planning is more significant at those income levels.',
      },
    ],
    commonQuestionsHtml: `
      <p>SSA employees most often ask: "When should I claim my own Social Security benefit, and how does the FERS supplement affect that decision?", "What happens to my FERS if SSA offers a VERA and I take it at 51?", and "I transferred from a rural office to the DC metro, does that change my retirement estimate?" All three have answers that depend on your personal numbers, and we model them in the workshop.</p>
    `,
    commonJobs: [
      'Claims representatives and service representatives',
      'Disability examiners and analysts',
      'Teleservice representatives',
      'Administrative law judges',
      'Program analysts and policy staff',
      'IT specialists and systems analysts',
    ],
    primaryLocations: [
      'Baltimore, MD (National Headquarters)',
      'Woodlawn, MD (main campus)',
      'Birmingham, AL (region IV)',
      'Kansas City, MO (region VII)',
      'San Francisco, CA (region IX)',
      'Field offices in all 50 states',
      'Philadelphia, PA (region III)',
    ],
    relatedAgencySlugs: ['department-of-health-and-human-services', 'department-of-labor', 'us-postal-service'],
    faq: [
      {
        q: 'I work at SSA and understand Social Security well. When should I claim my own benefit?',
        a: 'You probably already know the actuarial case for delayed claiming. The question is whether your personal circumstances support waiting. If you retire from SSA at 57 with the FERS supplement bridging to 62, you have income without claiming Social Security. At 62, the supplement ends. If your other income is sufficient, waiting to claim Social Security until 67 or 70 can increase your benefit by 30% to 77% versus claiming at 62. For married couples, the higher earner delaying to 70 also maximizes the survivor benefit.',
      },
      {
        q: 'SSA is offering VERA. I am 51 with 22 years. Should I take it?',
        a: 'Under VERA, you qualify for an immediate FERS annuity based on your 22 years of service and your high-3 at separation. At 1.0% per year, a $82,000 high-3 produces $18,040 per year. The FERS supplement would add approximately $6,000 to $9,000 per year until 62. You would need to cover health insurance (FEHB continuation), which runs $6,000 to $14,000 per year depending on the plan and family size. The real question is whether $24,000 to $27,000 in combined retirement income is sufficient while you are 51 and likely employable at higher wages.',
      },
      {
        q: 'I recently transferred from a rural SSA office to Woodlawn, MD. Does my new higher pay change my retirement projection?',
        a: 'Yes, significantly. The Washington-Baltimore locality pay in 2025 adds roughly 33% to your base salary, compared to 16% in many Midwest rural areas. If your final 3 years at Woodlawn occur at a GS-12 step 10, your DC-area basic pay might be $112,000 versus $88,000 in your prior location. Those 3 years become your high-3 at the higher rate. A transfer to a high-locality office in your final career phase is one of the most impactful moves an SSA employee can make for retirement income.',
      },
      {
        q: 'I am an SSA administrative law judge. How is my retirement different from claims staff?',
        a: 'Your pay is under the AL schedule rather than the GS scale, and AL salaries can be considerably higher. Otherwise, your FERS retirement mechanics are the same: 1% per year of creditable service times your high-3 (1.1% at 62 with 20+), TSP, FEHB, and Social Security coordination. The main difference is that your annuity will be larger in absolute dollars because of the higher high-3, which makes TSP tax strategy and Medicare/FEHB coordination proportionally more important.',
      },
      {
        q: 'How does the FERS supplement interact with part-time SSA work after retirement?',
        a: 'If you return to any employment, including part-time consulting or re-employment at SSA, after retiring on an immediate FERS annuity, the supplement is subject to the Social Security earnings test. For 2025, you can earn up to $23,400 from wages without penalty. Above that, the supplement is reduced by $1 for every $2 of excess earnings. If you earn $42,000 in a post-retirement part-time role, your supplement is reduced by $10,000. Investment income does not count toward the earnings test.',
      },
      {
        q: 'Can I retire from SSA and then work for a state Social Security disability agency?',
        a: 'Yes. State disability determination services (DDS) that conduct SSA disability reviews under federal contract employ people independently of the federal government. DDS employees are state workers, not federal workers, so FERS reemployment rules do not apply. However, the FERS supplement earnings test does apply to any wages you earn, including from a DDS position. Budget accordingly if a DDS role is part of your post-retirement plan.',
      },
    ],
  },
  {
    slug: 'environmental-protection-agency',
    name: 'Environmental Protection Agency',
    shortName: 'EPA',
    employeeCount: '15,000+ employees across headquarters and regional offices',
    metaTitle: 'EPA Employee FERS Retirement Planning | PlanWell',
    metaDescription:
      'Free FERS retirement workshop for EPA employees. Scientists, attorneys, and regional staff. FERS, TSP, FEHB planning by CFP and ChFEBC experts. Register free.',
    heroEyebrow: 'Environmental Protection Agency',
    heroHeading: 'FERS Retirement Planning for EPA Employees',
    heroLead:
      'EPA has a highly educated workforce with deep institutional knowledge, and its employees tend to stay long. The average EPA tenure is among the highest across mid-size agencies, which means many employees are within 5 to 10 years of a retirement they have thought about but not yet planned in detail. The FERS pension is more generous the longer you stay, and at EPA, most employees have the time to earn it fully.',
    introHtml: `
      <p>EPA scientists, engineers, environmental protection specialists, and attorneys span a salary range from entry-level GS-7 to Senior Executive Service. What they share is a commitment to careers longer than most private-sector equivalents, which makes the FERS pension a genuinely powerful income tool. An EPA scientist who retires at 62 with 32 years and a $145,000 high-3 receives $51,040 per year in annuity, indexed for inflation. That is a floor, not a ceiling.</p>
      <p>Regional EPA offices from Boston to San Francisco carry significant locality pay differences. An EPA GS-13 step 5 in the DC region earns roughly $127,000 in total basic pay including locality, versus approximately $99,000 at the same grade in a lower-cost region. If you are considering your final career posting before retirement, locality pay has a direct and permanent effect on your annuity. PlanWell helps EPA employees model the relocation decision with retirement dollars in the picture.</p>
    `,
    whyMattersHtml: `
      <p>EPA has experienced budget variability and staffing uncertainty over multiple administrations, creating an environment where VERA and VSIP offers appear with some regularity. If you are in your 50s with 20+ years, you need to understand the VERA math in advance so you can make a decision in the 30-day window that typically accompanies such offers. Running the numbers cold during an offer period is not a planning strategy.</p>
      <p>EPA employees also tend to have more Social Security earnings from pre-federal careers than some other agencies, because EPA draws scientists and engineers from the private sector and academia. If you had a private-sector career before EPA with meaningful 401(k) contributions, those assets need to be integrated into your retirement income plan alongside FERS and TSP. The three-bucket coordination (pension, TSP, outside assets) is more common at EPA than at agencies that hire primarily from entry level.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'Regional office locality pay and retirement relocation',
        body:
          'EPA\'s 10 regional offices carry meaningfully different locality pay rates. If you are within 5 years of retirement and considering a transfer to headquarters in Washington, DC, or to a high-locality regional office (Region 1 Boston, Region 9 San Francisco), the locality increase can raise your high-3 by $15,000 to $30,000, adding $150 to $300 per month to your pension permanently. Model the transfer decision as a financial one, not just a quality-of-life one.',
      },
      {
        title: 'Pre-federal private-sector retirement assets',
        body:
          'Many EPA scientists and attorneys entered federal service mid-career after time in private industry. If you have a 401(k) or 403(b) from a prior employer sitting in a rollover IRA or an old plan, that asset needs to be part of your retirement income model. It also affects TSP contribution strategy: if you already have substantial pre-tax retirement savings, directing marginal TSP contributions to Roth may reduce your future tax burden more efficiently.',
      },
      {
        title: 'Attorney bar status and FERS leave buyout',
        body:
          'EPA attorneys with 20+ years sometimes leave for state agencies or private environmental law practice before reaching MRA. If you leave before retirement eligibility, you can defer your FERS annuity to age 62, keeping all your creditable service intact, or take a refund of contributions, forfeiting the pension. For an EPA attorney with a $155,000 high-3 and 22 years of service, the deferred annuity at 62 is worth $34,100 per year for life. Taking the contribution refund, typically $40,000 to $60,000, gives up $34,100 per year permanently.',
      },
      {
        title: 'FERS supplement and post-retirement consulting',
        body:
          'Retired EPA specialists, particularly those with hazardous waste, water quality, or air quality expertise, are often recruited as consultants by regulated industries and environmental firms. Post-retirement consulting income is subject to the FERS supplement earnings test. Consulting through an LLC or S-corp is still wages or self-employment income for the earnings test; it does not escape the reduction. Budget for the supplement loss if consulting is in your post-retirement plan.',
      },
    ],
    commonQuestionsHtml: `
      <p>EPA employees most often ask: "I have worked in the private sector before EPA, how do those assets interact with my FERS plan?", "EPA just announced a VERA, I have 22 years and I am 53, should I take it?", and "I am thinking of transferring to the DC office in my last 3 years for the locality pay bump, is it worth it?" All three require specific modeling to answer, and we work through each in the workshop.</p>
    `,
    commonJobs: [
      'Environmental scientists and chemists',
      'Environmental engineers (water, air, hazardous waste)',
      'Environmental protection specialists',
      'EPA attorneys and legal advisors',
      'Program analysts and policy officers',
      'IT specialists and data analysts',
    ],
    primaryLocations: [
      'Washington, DC (headquarters)',
      'Research Triangle Park, NC (ORISE and research offices)',
      'Cincinnati, OH (Region 5 and research)',
      'Atlanta, GA (Region 4)',
      'San Francisco, CA (Region 9)',
      'Boston, MA (Region 1)',
      'Dallas, TX (Region 6)',
    ],
    relatedAgencySlugs: ['department-of-agriculture', 'department-of-the-interior', 'department-of-energy'],
    faq: [
      {
        q: 'I transferred to EPA headquarters in DC two years ago from a regional office. How does that affect my high-3?',
        a: 'Positively. The Washington-Baltimore-Arlington locality rate in 2025 adds approximately 33% to your base pay, compared to lower rates in many regions. If your DC salary in your final 3 years is $15,000 to $25,000 higher than your regional salary would have been, your high-3 captures that increase in full. For a GS-14 step 7, the annual annuity difference from a $20,000 higher high-3 is $200 per month for life. That is $72,000 over a 30-year retirement.',
      },
      {
        q: 'EPA offered VERA. I am 53 with 24 years of service. Should I take it?',
        a: 'At 53 with 24 years, you qualify for an immediate FERS annuity under VERA. At 1.0% per year, a $130,000 high-3 gives you $31,200 per year, plus a FERS supplement of approximately $10,000 to $14,000 until 62. You would bear the full FEHB premium (no retiree subsidy exists beyond what OPM provides), typically $6,000 to $16,000 per year for a family plan. The real question is whether $45,000 in combined income is sufficient or whether staying 4 more years to MRA with 28 years is worth more. We model the break-even in the workshop.',
      },
      {
        q: 'I have a $180,000 IRA rollover from a private-sector 401(k) before EPA. How does that affect my retirement plan?',
        a: 'Your IRA is a separate retirement asset that counts alongside FERS and TSP in your income plan. For tax purposes, pre-tax IRA distributions are fully taxable as ordinary income. If you are also drawing FERS annuity and TSP, combined distributions could push you into higher brackets. You may benefit from Roth converting some of your IRA in lower-income years early in retirement. Your IRA also subjects you to RMDs at 73, so the long-term withdrawal sequencing matters.',
      },
      {
        q: 'How does the FERS annuity cost-of-living adjustment work for EPA retirees?',
        a: 'FERS retirees receive a COLA on their annuity each year based on the Consumer Price Index. The FERS COLA is capped: if CPI is 2% or less, you get the full amount; if CPI is 2% to 3%, you get 2%; if CPI exceeds 3%, you receive CPI minus 1 percentage point. CSRS retirees get the full CPI with no cap. The COLA for FERS begins the year after you turn 62, so retirees who separate before 62 do not receive COLA adjustments until age 62.',
      },
      {
        q: 'Can I consult for environmental firms after retiring from EPA?',
        a: 'Yes, with two important considerations. First, federal ethics rules restrict former employees from certain communications with EPA on matters they personally and substantially participated in. The cooling-off period is typically 1 to 2 years for senior employees, and some restrictions are permanent. Second, consulting income counts as wages for the FERS supplement earnings test. Significant consulting income will reduce your supplement dollar-for-dollar above the exempt threshold.',
      },
      {
        q: 'What is my FERS MRA and when can I retire without a penalty?',
        a: 'For employees born in 1970 or later, the Minimum Retirement Age is 57. An unreduced annuity requires MRA with 30 or more years of service, age 60 with 20 or more years, or age 62 with at least 5 years. Retiring at MRA with 10 to 29 years results in a 5% per year reduction for each year under age 62. You can avoid the reduction by postponing the annuity start date to age 62, but you forfeit the FERS supplement during any postponed period.',
      },
    ],
  },
  {
    slug: 'department-of-energy',
    name: 'Department of Energy',
    shortName: 'DOE',
    employeeCount: '15,000 federal employees and 90,000+ contractor M&O employees',
    metaTitle: 'DOE Employee FERS Retirement Planning | PlanWell',
    metaDescription:
      'Free FERS retirement workshop for DOE federal employees. National labs, nuclear security, security clearances, TSP, and high-3 planning. Expert CFP guidance.',
    heroEyebrow: 'Department of Energy',
    heroHeading: 'FERS Retirement Planning for DOE Federal Employees',
    heroLead:
      'The Department of Energy has a small federal workforce and a massive contractor workforce. If you are a federal employee at DOE, you are in FERS with the same rules as any federal civilian. But if you work at a national laboratory under a Management and Operating (M&O) contract, you are not a federal employee, your retirement is through the lab\'s private plan, and this workshop is not the right fit. Knowing which category you are in is the first question you need to answer.',
    introHtml: `
      <p>DOE federal employees oversee the nation\'s nuclear weapons complex, energy research programs, and environmental cleanup at dozens of sites. The work involves security clearances, remote duty stations, and in some cases hazardous material exposures that add complexity to a career history. If you hold a Q or L clearance and are approaching retirement, the clearance itself does not affect your FERS benefits, but the career path that comes with clearance work, frequent moves, contractor adjacency, and potential security vetting gaps, can affect your service record.</p>
      <p>PlanWell works with DOE federal employees at headquarters in Washington and at field sites including Savannah River, Hanford, and Oak Ridge. The retirement questions are familiar FERS questions, but the career histories are anything but standard. We help DOE employees audit their federal service record, identify any gaps or non-creditable periods, and build a retirement projection that reflects their actual career rather than a simplified version of it.</p>
    `,
    whyMattersHtml: `
      <p>DOE federal employees often have mid-career transitions that complicate their FERS service history. A physicist who worked 8 years at a national lab as a contractor before converting to federal service at age 38 has a FERS career starting at 38, not at the start of their career. Their SCD reflects only the federal service, and their retirement eligibility date is later than peers who entered federal service at 22. This is a common source of retirement date miscalculation.</p>
      <p>The nuclear weapons complex and environmental cleanup sites involve occupational exposures that may qualify for special FERS disability provisions or workers\' compensation considerations. If your career included meaningful radiation exposure or chemical hazard exposure, talk to your occupational health office and benefits specialist well before retirement. FERS disability retirement is a separate track from regular FERS retirement and has different eligibility criteria and benefit calculations.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'Contractor-to-federal transitions and SCD',
        body:
          'Many DOE federal employees previously worked at the same site as M&O contractor employees. Time as a contractor does not count as FERS creditable federal service. Your FERS SCD starts on your first day as a federal employee, not your first day at the site. If you spent 10 years as a contractor at Hanford before converting to DOE federal employment, your FERS creditable service is calculated from the conversion date. Verify your SCD on your pay stub against your actual hire date.',
      },
      {
        title: 'Remote and hazardous duty station considerations',
        body:
          'DOE sites including Hanford, Savannah River, and Nevada National Security Site are in areas with limited post-retirement service options and sometimes elevated COL relative to their locality pay designation. If you are planning to remain near your duty station in retirement, factor local healthcare access and FEHB network coverage in that geography into your plan selection. Some FEHB plans have thin networks in rural DOE site communities.',
      },
      {
        title: 'Security clearance and post-retirement consulting',
        body:
          'Retired DOE federal employees with active or recently lapsed clearances are in demand for defense and nuclear consulting roles. Post-retirement consulting income is earned income for the FERS supplement earnings test. Additionally, federal ethics rules restrict certain post-employment communications with your former agency. The cooling-off period for senior employees is typically 1 year for general matters and permanent for specific matters you personally participated in.',
      },
      {
        title: 'NNSA employees and national security pay authorities',
        body:
          'The National Nuclear Security Administration within DOE uses special hiring authorities and pay flexibilities to compete for nuclear security and weapons program talent. If you have been compensated under a demonstration project or alternative pay system at NNSA, confirm that all pay periods under the alternative system count toward your high-3 at the rate actually paid. Some demonstration project pay flexibilities have created payroll coding issues in the past.',
      },
    ],
    commonQuestionsHtml: `
      <p>DOE federal employees most often ask: "I worked 12 years as an M&O contractor before going federal, does that time count?", "I have a Q clearance, does that affect my FERS benefits?", and "I am at Hanford and thinking about retiring in place, what FEHB plans cover that area?" All three are specific to DOE careers, and we address each in the workshop.</p>
    `,
    commonJobs: [
      'Nuclear engineers and physicists',
      'Environmental engineers and scientists',
      'Program and project managers',
      'Contracting officers and specialists',
      'IT and cybersecurity specialists (with clearance)',
      'Policy analysts and congressional affairs staff',
    ],
    primaryLocations: [
      'Washington, DC (Forrestal Building HQ)',
      'Oak Ridge, TN (Oak Ridge Office)',
      'Richland, WA (Hanford Site)',
      'Aiken, SC (Savannah River)',
      'Las Vegas, NV (Nevada site)',
      'Los Alamos and Albuquerque, NM (NNSA)',
      'Germantown, MD (suburban DC offices)',
    ],
    relatedAgencySlugs: ['department-of-defense', 'nasa', 'environmental-protection-agency'],
    faq: [
      {
        q: 'I worked 10 years at Hanford as an M&O contractor before converting to DOE federal employment. Does my contractor time count toward FERS?',
        a: 'No. Time as an M&O contractor employee is private-sector employment, not federal service. Your FERS creditable service and SCD start from your first day as a DOE federal employee. Your retirement eligibility and annuity calculation are both based solely on your federal tenure. If you contributed to the contractor plan during those 10 years, those assets are yours (typically a 401(k) or defined benefit through the lab), but they are separate from FERS entirely.',
      },
      {
        q: 'Does my Q or L clearance affect my FERS benefits in any way?',
        a: 'No. Security clearances do not change your FERS coverage, accrual rate, eligibility, or benefit calculation. What the clearance does affect is your career options during and after federal service. Post-retirement, maintaining or monetizing a clearance through contractor consulting roles creates earned income subject to the FERS supplement earnings test. Plan for the supplement reduction if you expect to consult in the cleared community after separation.',
      },
      {
        q: 'I am at Savannah River Site in rural South Carolina. Are there FEHB plans that actually cover my area?',
        a: 'Yes, but your options are more limited than colleagues in metropolitan areas. The Aiken-Augusta area has Blue Cross Blue Shield plans and some HMO options with reasonable coverage, but not every FEHB plan has in-network providers in that area. Before retiring in place at SRS, compare your current FEHB plan\'s network for the Aiken area against alternatives during open season. Switching plans is easiest before you retire, when you have the most flexibility.',
      },
      {
        q: 'I am an NNSA employee under a demonstration project pay plan. How does that affect my high-3?',
        a: 'It should not, if your pay was coded correctly. Demonstration project pay at NNSA is typically basic pay for retirement purposes, which means it counts in your high-3. However, any performance bonuses, discretionary awards, or one-time payments under a demonstration project do not count toward basic pay. Pull your official basic pay history from HR rather than using your total W-2 gross to verify your high-3 inputs.',
      },
      {
        q: 'When can I retire from DOE without a penalty on my annuity?',
        a: 'The standard FERS retirement eligibility rules apply. Unreduced retirement requires MRA (57 for those born in 1970 or later) with 30 years, age 60 with 20 years, or age 62 with 5 years. If DOE offers VERA during a workforce reduction, you may qualify at age 50 with 20 years or any age with 25 years for an immediate unreduced annuity. Without VERA, retiring before the thresholds above results in a 5% per year penalty for each year under age 62.',
      },
      {
        q: 'What happens to my TSP if I leave DOE before retirement eligibility?',
        a: 'Your TSP account belongs to you regardless of when you separate. You can leave it in TSP (which continues to earn returns and remains accessible without penalty at age 59.5), roll it to an IRA, or in limited cases take a partial withdrawal. You cannot continue contributing after separation, and you lose access to TSP loans. If you separate before age 55 and take distributions, the 10% early withdrawal penalty applies unless you use a substantially equal periodic payment (72(t)) arrangement or other exception.',
      },
    ],
  },
  {
    slug: 'department-of-agriculture',
    name: 'Department of Agriculture',
    shortName: 'USDA',
    employeeCount: '100,000+ employees across agencies and field offices',
    metaTitle: 'USDA Employee FERS Retirement Planning | PlanWell',
    metaDescription:
      'Free FERS retirement workshop for USDA employees. FSIS inspectors, Forest Service firefighters, FSA staff. LEO provisions, TSP, FEHB guidance. Register free.',
    heroEyebrow: 'Department of Agriculture',
    heroHeading: 'FERS Retirement Planning for USDA Employees',
    heroLead:
      'USDA is one of the most geographically dispersed agencies in the federal government, with employees in almost every county in the country. Food Safety and Inspection Service inspectors work in processing plants from Iowa to Mississippi. Forest Service firefighters serve under special provisions in the mountains of Montana and California. Farm Service Agency county office staff handle loans and conservation programs from rural courthouses. The retirement planning challenges are as diverse as the workforce itself.',
    introHtml: `
      <p>USDA\'s field-heavy workforce means that many employees have spent their entire career in lower-cost-of-living areas with correspondingly lower locality pay. A county FSA office employee in Nebraska earns the "Rest of U.S." locality pay of roughly 17%, while a colleague in the DC area earns 33%. That difference compounds over a 30-year career into a high-3 that can be $15,000 to $25,000 lower, and an annuity that reflects those rural years. We help USDA employees understand exactly what their pension looks like given their actual location history.</p>
      <p>FSIS inspectors and Forest Service employees represent two of the most distinct USDA populations. Inspectors often face physical demands and irregular hours that make early retirement attractive, but they need to understand the FERS supplement and its earnings test before they walk out the door. Forest Service firefighters covered under the wildland fire special provision have a retirement formula and timeline that looks more like a law enforcement officer than a standard GS employee. PlanWell addresses both groups in the same workshop with separate breakout scenarios.</p>
    `,
    whyMattersHtml: `
      <p>For FSIS inspectors, the physical nature of the work creates a genuine retirement urgency. An inspector who started at 24, works in a poultry processing plant for 30 years, and hits MRA at 57 with exactly 30 years can retire with an unreduced annuity and the FERS supplement. But if they do not understand the supplement\'s earnings test and pick up a part-time job at $30,000 per year, they will lose most of the supplement in the first year. That is a planning gap, not an unavoidable outcome.</p>
      <p>Forest Service employees face a different kind of urgency. Those covered under the wildland fire special provision have a mandatory retirement age of 57 with 20 years, and their accrual rate is 1.7% for those first 20 years. Missing the 20-year threshold because of a career interruption, a transfer to a non-covered forestry position, or a misunderstanding about which roles qualify means losing the premium formula permanently. We see this miscalculation more often at USDA than at almost any other agency.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'Forest Service wildland firefighter special provisions',
        body:
          'Wildland firefighters at the Forest Service who meet the primary duty test are covered under FERS firefighter special provisions: a 1.7% accrual rate for the first 20 years of covered service, mandatory retirement at age 57, and early retirement eligibility at age 50 with 20 years. The primary duty test requires that at least 50% of your time is spent in the performance of firefighting duties. Moving into a supervisory or administrative role can terminate your covered status.',
      },
      {
        title: 'FSIS inspector career and high-3 considerations',
        body:
          'FSIS inspectors typically serve in meat, poultry, and egg product processing facilities across rural America. Their high-3 often reflects lower-locality pay, but hazardous duty differentials and premium pay for overnight or weekend inspection shifts do not count toward the high-3 base. Some FSIS inspectors move into supervisory or circuit supervisory roles in the final years of their career, which can increase their base pay grade and improve the high-3 window.',
      },
      {
        title: 'Rural field office locality pay and career geography',
        body:
          'USDA employees in Rural Development, Natural Resources Conservation Service, Farm Service Agency, and other field agencies are overwhelmingly stationed in counties with "Rest of U.S." or low-tier locality pay. If you are within 5 to 10 years of retirement and there is any possibility of a reassignment to a higher-locality area, the annuity impact of even a 3-year high-locality posting is worth modeling as a career decision.',
      },
      {
        title: 'Cooperative extension and partner agency service credit',
        body:
          'Some USDA employees have prior service in state cooperative extension systems before moving to federal employment. State extension service is generally not federal service and does not count as FERS creditable service. However, if you had prior federal appointments (temporary, term, or permanent) before or alongside extension work, those federal periods may count if you were in a covered retirement position. Your SCD on your current pay stub tells you what OPM recognizes.',
      },
    ],
    commonQuestionsHtml: `
      <p>USDA employees ask most often: "I am a Forest Service firefighter, do I qualify for special provisions?", "As an FSIS inspector, can I retire at 57 with 30 years and get the supplement?", and "My career has been entirely in rural offices, how does that affect my pension?" All three answers depend on your specific position history, and we work through them with your actual numbers in the workshop.</p>
    `,
    specialProvisionsNote:
      'USDA Forest Service wildland firefighters whose primary duty (at least 50% of time) involves firefighting qualify for FERS firefighter special provisions: the 1.7% accrual rate for the first 20 years of covered service, early retirement at age 50 with 20 years, and mandatory separation at age 57. Confirm your primary duty designation with your HR office before planning around the special provision.',
    commonJobs: [
      'FSIS meat and poultry inspectors',
      'Forest Service wildland firefighters and foresters',
      'FSA and RD county office specialists',
      'NRCS soil conservation specialists',
      'Research scientists and agronomists',
      'Animal and Plant Health Inspection Service officers',
    ],
    primaryLocations: [
      'Washington, DC (Whitten Building HQ)',
      'Kansas City, MO (USDA service centers)',
      'Ft. Collins, CO (Forest Service research)',
      'Missoula, MT (Forest Service aerial fire depot)',
      'Minneapolis, MN (Forest Service NHQ)',
      'Temple, TX (NRCS)',
      'County offices in all 50 states',
    ],
    relatedAgencySlugs: ['department-of-the-interior', 'environmental-protection-agency', 'department-of-health-and-human-services'],
    faq: [
      {
        q: 'I am a Forest Service wildland firefighter. How do I know if I qualify for special provisions?',
        a: 'You qualify if your official position description designates firefighting as your primary duty, meaning at least 50% of your time is spent in firefighting activities as defined by OPM. Your SF-50 retirement code should be "E" or "KE" for firefighter coverage. If you have moved into a resource management, timber, or administrative role where firefighting is secondary, you may have lost covered status even if you still occasionally fight fire. Your benefits office can confirm your current coverage designation.',
      },
      {
        q: 'I am an FSIS inspector. What is my retirement formula and when can I retire?',
        a: 'FSIS inspectors are covered under standard FERS, not special provisions (unless they hold a separate LEO designation, which is uncommon). Your annuity accrues at 1.0% per year of creditable service times your high-3 (1.1% if you retire at 62 or later with 20+ years). You can retire at MRA (57 if born in 1970 or later) with 30 years without a penalty. With 30 years of service and a $78,000 high-3, your annual annuity is $23,400 plus the FERS supplement until 62.',
      },
      {
        q: 'My entire USDA career has been in rural county offices. How does that affect my annuity?',
        a: 'Rural office employees typically receive the "Rest of U.S." locality pay (17% in 2025) rather than the higher rates for metropolitan areas. This reduces your basic pay and, consequently, your high-3. A GS-11 step 10 in rural Nebraska earns approximately $77,000 basic pay including Rest of U.S. locality, versus $92,000 for the same grade and step in the DC area. Over a 30-year career, that locality gap translates to roughly $4,500 less in annual annuity. It is not a planning error, it is a career geography reality.',
      },
      {
        q: 'I worked for a state cooperative extension service for 5 years before USDA. Does that count?',
        a: 'State extension service employment is not federal service and does not count as FERS creditable service. Your FERS SCD reflects only periods when you were in a covered federal position contributing to the retirement fund. However, if you worked as a temporary federal employee in an earlier USDA seasonal appointment alongside or before the extension work, those federal periods may count. Pull your complete SF-50 history from HR to identify all federal appointment dates.',
      },
      {
        q: 'USDA offered a VERA buyout and I am 52 with 22 years. What happens if I take it?',
        a: 'Under VERA, you qualify at 50 with 20 years for an immediate FERS annuity. At 1.0% per year, 22 years of service with a $90,000 high-3 yields $19,800 per year. The FERS supplement adds approximately $7,000 to $10,000 per year until 62. FEHB continues in retirement but you pay the full employee-share premium without a discount. The combined annuity plus supplement of roughly $27,000 to $30,000 per year is meaningful, but warrants comparison against staying another 5 years to 57 with 27 years, which would yield approximately $24,300 in annuity without the supplement.',
      },
      {
        q: 'Does premium pay for weekend FSIS inspection shifts count toward my high-3?',
        a: 'No. Sunday premium pay, night differential, overtime, and availability pay do not count toward your FERS high-3. Only basic pay and applicable locality pay feed the pension calculation. Many FSIS inspectors significantly overestimate their high-3 because their gross pay from shift work is 20% to 30% higher than basic pay. Use the basic pay line on your leave and earnings statement for any retirement projections.',
      },
    ],
  },
  {
    slug: 'department-of-commerce',
    name: 'Department of Commerce',
    shortName: 'Commerce',
    employeeCount: '50,000+ employees across bureaus',
    metaTitle: 'Commerce Department FERS Retirement Planning | PlanWell',
    metaDescription:
      'Free FERS retirement workshop for Commerce employees. NOAA, Census, NIST, Patent Office. TSP, FEHB, Commissioned Corps planning. Expert CFP guidance.',
    heroEyebrow: 'Department of Commerce',
    heroHeading: 'FERS Retirement Planning for Commerce Department Employees',
    heroLead:
      'Commerce is a more varied agency than its size suggests. NOAA meteorologists and oceanographers, Census Bureau statisticians who surge once a decade for the decennial count, NIST metrologists at the cutting edge of measurement science, and USPTO patent examiners working production quotas every day all sit under the same Commerce umbrella but have entirely different retirement planning profiles.',
    introHtml: `
      <p>USPTO patent examiners face a unique production-based compensation model that affects their earnings trajectory differently from most GS employees. Bonus pay for production exceeding quota does not count toward the high-3. Patent examiners also have among the highest rates of telework in the federal government, which has raised questions over recent years about locality pay coding when an examiner\'s official duty station differs from their home location. If you are a patent examiner, confirm your official duty station and locality designation before using your pay stub as a high-3 proxy.</p>
      <p>NOAA Commissioned Corps officers are not in FERS. They are uniformed service personnel in the NOAA Commissioned Officer Corps, with their own retirement system. NOAA civil service employees working alongside Corps officers are in FERS and follow standard FERS rules. If you are uncertain which category applies to you, your SF-50 is definitive: a retirement coverage code other than "0" means you are in a retirement system; the specific code tells you which one.</p>
    `,
    whyMattersHtml: `
      <p>Census Bureau employees face an unusual career arc. The decennial census creates temporary hiring surges that draw thousands of employees into short-term federal work. Career Census employees who have worked multiple decennial cycles alongside temporary staff need to confirm that their permanent, career-conditional, or term appointments, not the temporary survey worker periods, are the ones counting in their FERS SCD. Mixing temporary and career service in a personal calculation produces an overstated creditable service figure.</p>
      <p>NIST scientists and NOAA civil servants often have high-3 salaries in ranges comparable to NASA and EPA scientists, with complex career histories that include prior academic or private-sector work. The TSP tax optimization questions at these income levels mirror what we see at NASA: large pre-tax balances, high current incomes, and a risk of landing in the 24% to 32% bracket in retirement if TSP withdrawals are not sequenced thoughtfully.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'USPTO patent examiner production pay and high-3',
        body:
          'Patent examiners at the USPTO receive production bonuses when they exceed their examination quota. These bonuses are not basic pay and do not count toward the FERS high-3. USPTO examiners also have unique locality pay questions because many work from home in locations with different locality rates than the USPTO\'s Alexandria, VA headquarters. Your official duty station, as recorded by HR, determines your locality rate, regardless of where you physically work.',
      },
      {
        title: 'NOAA Commissioned Corps versus civil service',
        body:
          'NOAA has both civil service employees (in FERS) and Commissioned Corps officers (in the NOAA Corp retirement system). If you are a NOAA civil servant, your retirement is standard FERS. If you are a Commissioned Corps officer, your retirement is under a separate uniformed service system and this planning framework does not directly apply. If you transitioned from Commissioned Corps to civil service, your Corp service may count toward FERS through a buyback process similar to military deposits.',
      },
      {
        title: 'Census Bureau career versus decennial employees',
        body:
          'The Census Bureau\'s decennial cycles bring in large numbers of temporary employees. Career Census employees sometimes have early federal service as temporary decennial workers that does not count toward FERS. Verify your SCD reflects only permanent or term federal service in covered positions. Temporary, intermittent, or WAE (when actually employed) periods are typically excluded from creditable service.',
      },
      {
        title: 'NIST post-retirement research and intellectual property',
        body:
          'NIST scientists who retire sometimes continue working as emeritus researchers or consultants. Income from NIST consulting contracts after retirement constitutes wages for FERS supplement purposes. Additionally, if you hold patents or receive royalties from inventions developed during federal service, those royalties are typically investment income, not wages, and do not count toward the supplement earnings test.',
      },
    ],
    commonQuestionsHtml: `
      <p>Commerce employees most often ask: "I am a USPTO patent examiner working from home in a different state, what is my locality pay?", "I worked at NOAA as a Commissioned Corps officer and transferred to a civil service role, how does my Corp time count?", and "My Census career included early temporary decennial work, does that count?" Each question has a specific answer tied to your appointment type and payroll records.</p>
    `,
    commonJobs: [
      'USPTO patent examiners and trademark attorneys',
      'NOAA meteorologists and oceanographers (civil service)',
      'Census Bureau statisticians and survey researchers',
      'NIST physicists, engineers, and metrologists',
      'International Trade Administration economists',
      'National Telecommunications and Information Administration analysts',
    ],
    primaryLocations: [
      'Washington, DC (Herbert C. Hoover Building)',
      'Alexandria, VA (USPTO campus)',
      'Suitland, MD (Census Bureau)',
      'Gaithersburg, MD (NIST campus)',
      'Silver Spring, MD (NOAA HQ)',
      'Boulder, CO (NOAA and NIST research)',
      'Regional ITA offices nationwide',
    ],
    relatedAgencySlugs: ['nasa', 'environmental-protection-agency', 'department-of-the-interior'],
    faq: [
      {
        q: 'I am a USPTO patent examiner working from home in Texas. Is my locality pay based on Texas or Alexandria, VA?',
        a: 'Your locality pay is based on your official duty station as recorded in the payroll system, not your physical work location. USPTO has designated Alexandria, VA as the official duty station for most remote examiners, which carries the Washington-Baltimore-Arlington locality rate of approximately 33%. However, USPTO has also offered some employees the option to change their official duty station to their home location. Confirm your official duty station with USPTO HR to verify your actual locality rate, because the difference can be $15,000 or more annually at the GS-13 and GS-14 levels.',
      },
      {
        q: 'I transferred from NOAA Commissioned Corps to a civil service position. Does my Corp time count toward FERS?',
        a: 'Former NOAA Commissioned Corps officers who transition to civil service can buy back their Corps service time with a military deposit, similar to military veterans buying back Army or Navy service. The deposit is typically 3% of your Corps base pay plus interest. Purchased Corps time counts toward your FERS creditable service and can also count toward the 20-year service thresholds for early retirement eligibility. Submit your buyback documentation to your HR office early in your civil service career.',
      },
      {
        q: 'My Census career started with temporary decennial work in 2010. Does that period count toward my FERS pension?',
        a: 'Probably not, if that work was as a temporary or intermittent employee during the decennial census operation. Temporary appointments and non-career positions generally do not count as FERS creditable service. Your FERS SCD reflects only career-conditional, career, or term appointments in covered positions. Check the SCD on your current leave and earnings statement. If it shows a date after your 2010 start, the gap reflects non-creditable early service.',
      },
      {
        q: 'My USPTO production bonuses doubled my income some years. How does that affect my retirement calculation?',
        a: 'It does not. Production bonuses at USPTO are not basic pay and are excluded from the FERS high-3 calculation. Your high-3 is based on your basic salary (GS base pay plus locality), averaged over your three highest consecutive years. In a year where you earned $120,000 in bonuses on top of $110,000 in basic pay, your retirement-relevant income for that year is $110,000. Many patent examiners are genuinely surprised to see how much lower their FERS annuity projection is relative to their peak total compensation.',
      },
      {
        q: 'I am a NOAA civil servant. Does my retirement work the same as any other FERS employee?',
        a: 'Yes. NOAA civil service employees are in standard FERS with the same rules as any other federal civilian. Your annuity is 1.0% per year of creditable service times your high-3 (1.1% at 62 with 20+). Your MRA, FEHB continuation rules, TSP eligibility, and FERS supplement work identically to EPA or HHS colleagues. The only NOAA-specific wrinkle is distinguishing yourself from Commissioned Corps officers at the same facilities, who are in a different retirement system entirely.',
      },
      {
        q: 'Can NIST royalties from federal patents affect my FERS supplement?',
        a: 'Generally no. Royalties from government-owned patents are typically classified as investment income or intellectual property income, not wages from employment. The FERS supplement earnings test only counts wages, salary, and net self-employment income. Passive royalty income does not count. However, if you structured a post-retirement consulting arrangement with NIST or a licensee that pays you for active services (research, consulting, testing), that income would count as self-employment income and could reduce your supplement.',
      },
    ],
  },
  {
    slug: 'department-of-the-interior',
    name: 'Department of the Interior',
    shortName: 'Interior',
    employeeCount: '70,000+ employees across bureaus',
    metaTitle: 'Interior Department FERS Retirement | NPS, BLM | PlanWell',
    metaDescription:
      'Free FERS retirement workshop for Interior employees. NPS rangers, BLM, USGS, wildland firefighters. Special provisions, remote duty, TSP. Expert CFP guidance.',
    heroEyebrow: 'Department of the Interior',
    heroHeading: 'FERS Retirement Planning for Interior Department Employees',
    heroLead:
      'The Department of the Interior manages more public land than any other agency in the federal government, and its employees often work in locations so remote that a PlanWell workshop might be the first professional retirement planning conversation they have had. National Park Service rangers, Bureau of Land Management specialists, wildland firefighters, and USGS scientists share an agency but live in retirement planning worlds that are far apart.',
    introHtml: `
      <p>Interior employees at remote duty stations face practical retirement planning challenges that office-based feds rarely encounter. A BLM range management specialist in Elko, Nevada and a USGS hydrologist in Anchorage, Alaska are each earning meaningful FERS benefits, but they are doing it at the "Rest of U.S." or Alaska locality pay rates, in geographic markets where FEHB networks can be limited and post-retirement life may look very different from their working years. Planning for Interior employees requires knowing where they work now and where they plan to live in retirement.</p>
      <p>Interior also houses the Bureau of Indian Affairs, which serves tribal communities and employs many Native American federal employees. BIA employees are in FERS and follow standard rules, but the duty stations are often remote, the career paths can include both tribal and federal government roles, and the interaction between federal FERS benefits and any tribal employment history requires careful auditing. PlanWell works with BIA employees and helps them confirm what counts toward their federal pension.</p>
    `,
    whyMattersHtml: `
      <p>For NPS law enforcement rangers and wildland firefighters at Interior bureaus, the special provision retirement formula is a core career benefit. An NPS ranger who retires at 52 with 22 years of covered LEO service and a $100,000 high-3 receives $37,400 per year under the 1.7% formula. Under regular FERS, the same career produces $22,000. That $15,400 annual gap, sustained over 30 years, is $462,000 in lifetime annuity income. The stakes of getting the coverage determination right are enormous.</p>
      <p>Interior employees in remote locations also face a unique FEHB challenge. If you plan to retire and stay in a rural area near your park or BLM district, you need to verify that your chosen FEHB plan has adequate in-network coverage in that location before you commit to a plan. Some high-deductible plans and HMOs have thin or nonexistent networks in rural western states. Choosing your FEHB plan based on premium alone without checking the network in your retirement location is a mistake we help people avoid.</p>
    `,
    uniqueConsiderations: [
      {
        title: 'NPS law enforcement rangers and special provisions',
        body:
          'National Park Service law enforcement rangers whose primary duty involves law enforcement are covered under FERS LEO special provisions. This means the 1.7% accrual rate for the first 20 years, early retirement at age 50 with 20 years, and mandatory separation at age 57. NPS also employs general (non-law enforcement) rangers and interpretive rangers who are not LEO-covered and retire under standard FERS. Your position description, not your uniform or badge, determines your coverage.',
      },
      {
        title: 'Interior wildland firefighters at BLM, NPS, and FWS',
        body:
          'BLM, NPS, and Fish and Wildlife Service wildland firefighters who meet the primary duty test qualify for FERS firefighter special provisions. The primary duty test requires at least 50% of your work time to involve firefighting activities. Moving into a fire management planning, prevention, or administrative role can remove your covered status even if you respond to fires occasionally. Confirm your primary duty designation annually, because it can change without your awareness if your role evolves.',
      },
      {
        title: 'Remote duty station FEHB network gaps',
        body:
          'Interior employees stationed at remote parks, refuges, and public land offices often live in areas where FEHB plan networks are limited or absent. If you plan to retire in place near your duty station, review the provider directory for any FEHB plan you are considering against the healthcare providers actually available in your zip code. Self-plus-one and family plans with strong metropolitan networks can leave rural retirees paying out-of-network rates for routine care.',
      },
      {
        title: 'BIA employees and tribal service credit',
        body:
          'Bureau of Indian Affairs employees sometimes have prior service with tribal governments or tribal enterprises before moving to the federal BIA workforce. Tribal government service is not federal service and does not count toward FERS creditable service. However, prior federal appointments at other agencies (BLM, NPS, or any other federal employer) do count, and your SCD should reflect those. Tribal service after retirement is treated as private-sector employment for FERS supplement earnings test purposes.',
      },
    ],
    commonQuestionsHtml: `
      <p>Interior employees ask most often: "I am an NPS law enforcement ranger, do I have LEO special provisions?", "I am a BLM wildland firefighter who has moved into a fire management desk role, am I still covered under firefighter provisions?", and "I am retiring near Yellowstone, which FEHB plan actually covers the local providers?" All three have specific answers tied to your position, duty designation, and plan network research.</p>
    `,
    specialProvisionsNote:
      'Interior law enforcement rangers at NPS (in law enforcement positions), wildland firefighters at BLM, NPS, FWS, and BIA whose primary duty involves firefighting, and certain other covered positions qualify for FERS special provisions: a 1.7% accrual rate for the first 20 years of covered service, early retirement at age 50 with 20 years, and mandatory separation at age 57. Coverage is determined by primary duty, not job title or uniform.',
    commonJobs: [
      'NPS law enforcement rangers and interpretive rangers',
      'BLM range management and land use planning specialists',
      'USGS hydrologists, geologists, and scientists',
      'FWS wildlife biologists and refuge officers',
      'BIA education and social services staff',
      'Wildland firefighters across all Interior bureaus',
    ],
    primaryLocations: [
      'Washington, DC (Main Interior Building)',
      'Lakewood, CO (BLM State Offices)',
      'Reston, VA (USGS HQ)',
      'National parks in every state',
      'Anchorage, AK (Alaska Regional Office)',
      'Albuquerque, NM (BIA Southwest Region)',
      'Boise, ID (BLM and fire management)',
    ],
    relatedAgencySlugs: ['department-of-agriculture', 'environmental-protection-agency', 'department-of-commerce'],
    faq: [
      {
        q: 'I am an NPS ranger. How do I know if I am covered under LEO special provisions?',
        a: 'NPS law enforcement rangers, those whose primary duty involves enforcement of federal laws and protection of park resources with arrest authority, are covered under FERS LEO special provisions. Interpretive rangers, resource management rangers, and concession management staff are typically not covered. Your SF-50 block 30 should show retirement coverage code "E" or "KE" for LEO coverage. If you have changed roles from law enforcement to a non-LE position, your coverage may have changed. Your HR office can provide a written coverage determination.',
      },
      {
        q: 'I moved from wildland firefighting to a fire management desk role at BLM. Am I still under firefighter special provisions?',
        a: 'Possibly not. The firefighter special provision requires that at least 50% of your time be spent in the performance of firefighting duties, not fire planning, prevention, or administrative coordination. Moving to a fire management planning or fuels management desk role typically changes your primary duty away from firefighting, which can terminate your covered status. Your coverage status should be formally re-evaluated whenever your position description changes. Request a coverage determination letter from your HR benefits office.',
      },
      {
        q: 'What is my mandatory retirement age as an Interior wildland firefighter or NPS LEO ranger?',
        a: 'Under FERS special provisions for firefighters and law enforcement officers, the mandatory retirement age is 57 with 20 or more years of covered service. You can retire as early as age 50 with 20 years. If you reach 57 without 20 years of covered service, the mandatory separation does not apply, but your annuity reverts to the regular 1.0% formula for any non-covered service years. Some agencies can grant limited extensions to age 60 in specific circumstances.',
      },
      {
        q: 'I plan to retire near Grand Teton after NPS service. What FEHB plan covers that area?',
        a: 'The Teton County, Wyoming area has limited provider networks for some FEHB plans. BCBS Service Benefit Plan (the Blue plan), which is nationwide, typically has the broadest rural network and covers providers in small communities adjacent to national parks. Government Employees Health Association (GEHA) and Aetna FEHB plans also have reasonable national networks. Verify in-network providers by entering your specific zip code in the OPM FEHB plan comparison tool before open season. Do not assume any plan covers your area without checking.',
      },
      {
        q: 'My BIA career followed 8 years at a tribal college. Does my tribal time count toward FERS?',
        a: 'No. Tribal college employment and tribal government service are not federal service. Your FERS creditable service and SCD reflect only your federal BIA employment (and any other prior federal agency service). If your tribal college was receiving federal grants, that still does not make you a federal employee for retirement purposes. Your SCD on your leave and earnings statement shows the date OPM recognizes as the start of your creditable federal service.',
      },
      {
        q: 'I have 30 years at USGS and am 62. What is my annuity and how does the 1.1% rate apply?',
        a: 'At age 62 with 30 years of FERS service, you qualify for the enhanced 1.1% accrual rate. Your annuity is calculated as 30 x 1.1% x your high-3. With a $140,000 high-3, that is $46,200 per year, indexed for FERS COLA after 62. The 1.1% rate versus 1.0% adds $4,200 per year compared to retiring at 60 with the same 30 years. You also would not receive the FERS supplement at 62, since the supplement is only for those who retire before 62. Social Security eligibility begins at 62, so the supplement becomes moot for you.',
      },
    ],
  },
];

export function getAgency(slug: string): Agency | undefined {
  return agencies.find((a) => a.slug === slug);
}

export function getAllAgencies(): Agency[] {
  return agencies;
}
