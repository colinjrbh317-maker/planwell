// Article data for static generation
// Will be replaced with Sanity CMS queries later

interface Article {
  title: string;
  category: string;
  date: string;
  author: string;
  readTime: string;
  image: string;
  content: string;
}

export const articles: Record<string, Article> = {
  'fers-retirement-planning-essential-guide': {
    title: "FERS Retirement Planning: Your Essential Guide to a Secure Future",
    category: "FERS",
    date: "December 15, 2025",
    author: "David Fei, CFP®, ChFEBC℠",
    readTime: "15 min read",
    image: "/images/articles/fers-essential-guide.png",
    content: `
      <h2>Understanding Your FERS Retirement System</h2>
      <p>The Federal Employees Retirement System (FERS) is a retirement plan for federal civilian employees that became effective January 1, 1987. Understanding how FERS works is crucial for maximizing your retirement benefits.</p>
      
      <p>FERS is a three-tiered retirement system consisting of:</p>
      <ul>
        <li><strong>FERS Basic Benefit Plan:</strong> A defined benefit pension based on your years of service and high-3 average salary</li>
        <li><strong>Social Security:</strong> Federal employees under FERS are covered by Social Security</li>
        <li><strong>Thrift Savings Plan (TSP):</strong> A 401(k)-style defined contribution plan with agency matching</li>
      </ul>
      
      <h2>The FERS Basic Benefit Formula</h2>
      <p>Your FERS basic annuity is calculated using this formula:</p>
      <p><strong>High-3 Average Salary × Years of Service × Multiplier = Annual Pension</strong></p>
      
      <p>The multiplier depends on your age at retirement:</p>
      <ul>
        <li><strong>1% multiplier:</strong> If retiring before age 62</li>
        <li><strong>1.1% multiplier:</strong> If retiring at age 62 or later with 20+ years of service</li>
      </ul>
      
      <h2>Example Calculation</h2>
      <p>Let's say your high-3 salary is $95,000 and you have 30 years of service:</p>
      <ul>
        <li>Retiring at 60: $95,000 × 30 × 1% = <strong>$28,500/year</strong></li>
        <li>Retiring at 62: $95,000 × 30 × 1.1% = <strong>$31,350/year</strong></li>
      </ul>
      
      <h2>Maximizing Your FERS Benefits</h2>
      <p>There are several strategies to maximize your FERS pension:</p>
      <ol>
        <li><strong>Optimize your high-3:</strong> Time your retirement to capture your highest three consecutive years of salary</li>
        <li><strong>Use your sick leave:</strong> Unused sick leave adds to your service credit for pension calculation</li>
        <li><strong>Understand survivor benefits:</strong> Know the cost-benefit of electing survivor annuity options</li>
        <li><strong>Coordinate with Social Security:</strong> Plan the optimal time to claim Social Security benefits</li>
      </ol>
      
      <h2>Next Steps</h2>
      <p>For personalized guidance on your FERS retirement, attend our free workshop or schedule a one-on-one consultation with our certified planners.</p>
    `
  },
  'fers-supplement-explained': {
    title: "FERS Supplement Explained: Your 2025 Bridge to Social Security",
    category: "FERS",
    date: "December 10, 2025",
    author: "Brennan Rhule, CFP®, ChFEBC℠",
    readTime: "10 min read",
    image: "/images/articles/fers-supplement.png",
    content: `
      <h2>What is the FERS Special Retirement Supplement?</h2>
      <p>The FERS Special Retirement Supplement (SRS) is a benefit designed to bridge the gap between your FERS retirement and Social Security eligibility. It provides income similar to what you would receive from Social Security before you reach age 62.</p>
      
      <h2>Who Qualifies?</h2>
      <p>You may be eligible for the SRS if you:</p>
      <ul>
        <li>Retire under the MRA+30 provision (Minimum Retirement Age with 30 years of service)</li>
        <li>Retire under the age 60 with 20 years provision</li>
        <li>Are a special provision employee (law enforcement, firefighters, air traffic controllers)</li>
      </ul>
      
      <p><strong>Note:</strong> If you retire under MRA+10 with a reduced annuity, you are NOT eligible for the supplement.</p>
      
      <h2>How is the SRS Calculated?</h2>
      <p>The supplement approximates the Social Security benefit you earned during your federal service only. The formula is:</p>
      <p><strong>Estimated Social Security Benefit × (FERS Service ÷ 40) = SRS Amount</strong></p>
      
      <h2>Earnings Test Warning</h2>
      <p>The SRS is subject to an earnings test. In 2025, if you earn more than $22,320 from wages, your supplement is reduced by $1 for every $2 earned above that threshold.</p>
      
      <h2>When Does It Stop?</h2>
      <p>The FERS Supplement stops at age 62, when you become eligible for Social Security benefits. You can then choose when to claim Social Security—at 62, at full retirement age, or later.</p>
    `
  },
  'boost-your-fers-retirement-plan': {
    title: "Boost Your FERS Retirement Plan: How to Master Your Government Pension",
    category: "Strategy",
    date: "December 5, 2025",
    author: "David Fei, CFP®, ChFEBC℠",
    readTime: "12 min read",
    image: "/images/articles/boost-fers.png",
    content: `
      <h2>Maximizing Your High-3 Average Salary</h2>
      <p>Your pension is based on your highest average basic pay over any three consecutive years of service. Here's how to maximize it:</p>
      
      <h3>1. Time Your Retirement Strategically</h3>
      <p>If you expect a promotion, within-grade increase, or locality pay adjustment, consider timing your retirement to capture those higher earnings in your high-3 calculation.</p>
      
      <h3>2. Know What Counts</h3>
      <p>The following counts toward your high-3:</p>
      <ul>
        <li>Basic pay</li>
        <li>Locality pay</li>
        <li>Availability pay (for certain positions)</li>
        <li>Night differential</li>
      </ul>
      
      <p>The following does NOT count:</p>
      <ul>
        <li>Overtime pay</li>
        <li>Bonuses and awards</li>
        <li>Holiday pay premiums</li>
      </ul>
      
      <h2>The Value of Unused Sick Leave</h2>
      <p>As of 2014, 100% of your unused sick leave is converted to service credit for pension calculation purposes. 2,087 hours equals one year of service credit.</p>
      
      <p>Example: If you retire with 1,000 hours of sick leave, that adds approximately 5.7 months to your service calculation—potentially increasing your pension by thousands over your lifetime.</p>
      
      <h2>TSP Optimization</h2>
      <p>Don't forget the third leg of your FERS stool. Maximize your TSP contributions:</p>
      <ul>
        <li>Contribute at least 5% to get the full agency match</li>
        <li>Consider the 2025 contribution limit of $23,500</li>
        <li>If 50+, add the $7,500 catch-up contribution</li>
      </ul>
    `
  },
  'opm-retirement-backlog-november-2025': {
    title: "Federal Retirement Applications OPM Backlog November 2025",
    category: "Federal News",
    date: "November 2025",
    author: "PlanWell Team",
    readTime: "5 min read",
    image: "/images/articles/opm-backlog.png",
    content: `
      <h2>Current OPM Processing Times</h2>
      <p>As of November 2025, the Office of Personnel Management (OPM) continues to work through a significant backlog of federal retirement applications. Here's what you need to know:</p>
      
      <h2>Average Processing Times</h2>
      <ul>
        <li><strong>FERS applications:</strong> 60-90 days average</li>
        <li><strong>CSRS applications:</strong> 75-100 days average</li>
        <li><strong>Complex cases:</strong> May take 4-6 months</li>
      </ul>
      
      <h2>What This Means for Your Retirement</h2>
      <p>If you're planning to retire soon, factor in these processing delays. Your agency will typically begin paying you an estimated annuity (usually about 80% of your expected benefit) while your case is being processed.</p>
      
      <h2>Tips to Avoid Delays</h2>
      <ol>
        <li><strong>Submit complete documentation:</strong> Missing documents are the #1 cause of delays</li>
        <li><strong>Verify your service history:</strong> Ensure your SF-50s and service records are accurate</li>
        <li><strong>Address military service deposits early:</strong> Don't wait until retirement to make military deposits</li>
        <li><strong>Work with your HR office:</strong> They can help catch issues before submission</li>
      </ol>
    `
  },
  'service-deposits-timing-retirement': {
    title: "Federal Employee Retirement: Service Deposits and Timing Your Exit",
    category: "FERS",
    date: "November 2025",
    author: "Brennan Rhule, CFP®, ChFEBC℠",
    readTime: "8 min read",
    image: "/images/articles/service-deposits.png",
    content: `
      <h2>Understanding Service Deposits</h2>
      <p>Service deposits allow you to receive credit for periods of service that wouldn't otherwise count toward your retirement. The two main types are:</p>
      
      <h3>Military Deposit</h3>
      <p>If you have post-1956 military service, you can make a deposit to receive credit for that time. The deposit equals 3% of your military basic pay, plus interest.</p>
      
      <h3>Civilian Deposit (Redeposit)</h3>
      <p>If you previously worked in a position covered by FERS or CSRS and received a refund of your contributions, you can redeposit those funds to receive service credit.</p>
      
      <h2>Why Timing Matters</h2>
      <p>Deposits accrue interest if not paid by the time you retire. Making deposits early saves money:</p>
      <ul>
        <li>Interest is compounded annually</li>
        <li>Current interest rate: Variable Rate I Bonds rate</li>
        <li>No interest charged if paid within 3 years of returning to federal service (for redeposits)</li>
      </ul>
      
      <h2>Timing Your Retirement</h2>
      <p>Consider these timing factors:</p>
      <ol>
        <li><strong>Leave accrual:</strong> You get paid for unused annual leave as a lump sum</li>
        <li><strong>Pay periods:</strong> Retire at the end of a pay period to avoid partial pay complications</li>
        <li><strong>FEHB:</strong> Ensure you meet the 5-year requirement for continuing health benefits</li>
      </ol>
    `
  },
  'simplify-fers-pension-calculation': {
    title: "Simplify Your FERS Pension Calculation",
    category: "FERS",
    date: "October 2025",
    author: "David Fei, CFP®, ChFEBC℠",
    readTime: "7 min read",
    image: "/images/articles/pension-calculator.png",
    content: `
      <h2>The Basic FERS Calculation</h2>
      <p>While FERS calculations can seem complex, they follow a straightforward formula:</p>
      <p><strong>Annual Pension = High-3 × Years of Service × Multiplier</strong></p>
      
      <h2>Step 1: Calculate Your High-3</h2>
      <p>Your high-3 is the average of your highest 3 consecutive years of basic pay. For most employees, this is their final 3 years before retirement.</p>
      
      <h2>Step 2: Count Your Years of Service</h2>
      <p>Include:</p>
      <ul>
        <li>All creditable civilian service</li>
        <li>Military service (with deposit)</li>
        <li>Unused sick leave (for calculation only, not eligibility)</li>
      </ul>
      
      <h2>Step 3: Apply the Multiplier</h2>
      <ul>
        <li><strong>1%:</strong> Standard multiplier</li>
        <li><strong>1.1%:</strong> If retiring at age 62+ with 20+ years</li>
      </ul>
      
      <h2>Quick Example</h2>
      <p>High-3: $90,000 | Service: 28 years | Age at retirement: 60</p>
      <p>$90,000 × 28 × 1% = <strong>$25,200 per year</strong> (before survivor benefit election)</p>
    `
  }
};

export function getArticleSlugs() {
  return Object.keys(articles);
}

export function getArticle(slug: string) {
  return articles[slug];
}
