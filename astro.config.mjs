// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
    site: 'https://planwellfp.com',
    integrations: [
        sitemap({
            changefreq: 'weekly',
            priority: 0.7,
            lastmod: new Date(),
        }),
    ],
    image: {
        service: {
            entrypoint: 'astro/assets/services/sharp',
        },
    },
    trailingSlash: 'never',
    redirects: {
        // Legacy WordPress URLs
        '/resources': '/blog',
        '/resources/:slug': '/:slug',

        // Blog/Resources
        '/federal-benefits-blog': '/blog',
        '/blog/': '/blog',

        // Webinars
        '/federal-employee-retirement-benefits-education-workshops': '/webinars',
        '/tsp-webinar-calendar': '/webinars',
        '/thrift-savings-plan-tsp-webinar-1': '/webinar/tsp',
        '/thrift-savings-plan-tsp-webinar-2': '/webinar/tsp',
        '/thrift-savings-plan-tsp-webinar-3': '/webinar/tsp',
        '/federal-retirement-webinar-workshop': '/webinars',
        '/webinar-sign-up-1': '/webinar',
        '/webinar-sign-up-2': '/webinar',
        '/webinar-sign-up-3': '/webinar',
        '/webinar-sign-up-4': '/webinar',
        '/webinar-sign-up-5': '/webinar',
        '/webinar-sign-up-6': '/webinar',
        '/federal-benefits-fehb-open-season-2025-webinars': '/webinars',

        // Calculators
        '/fers-supplement-calculator': '/special-retirement-supplement-calculator',
        '/fers-sick-leave-conversion-chart': '/sick-leave-conversion-calculator',
        '/federal-employee-retirement-planning-calculators': '/calculators',

        // Services
        '/financial-advisor-for-federal-employees': '/services/comprehensive-planning',
        '/federal-employee-financial-advisor': '/services/comprehensive-planning',
        '/fegli-and-life-insurance': '/services/survivor-benefits',
        '/tax-strategy-for-federal-employees': '/services/tax-planning',
        '/fehb-federal-employee-health-benefits-and-medicare': '/services/fehb-medicare',
        '/fers-survivor-benefits-for-federal-employees': '/services/survivor-benefits',
        '/tsp-thrift-savings-plan-for-federal-employees-investing': '/services/tsp-management',
        '/financial-planning-for-federal-employees': '/services/comprehensive-planning',
        '/federal-employee-retirement-system-fers': '/services/fers-retirement-planning',
        '/federal-retirement-planning': '/services',
        '/investment-management': '/services/comprehensive-planning',
        '/retirement-planning': '/services',
        '/federal-long-term-care-insurance-program-fltcip': '/services/fehb-medicare',
        '/social-security-for-federal-employees': '/blog/topic/fers',

        // About pages
        '/our-team-brennan-rhule-and-david-fei': '/about',
        '/our-process': '/about/financial-blueprint',
        '/the-planwell-difference': '/about/financial-blueprint',
        '/chartered-federal-employee-benefits-consultant-chfebc': '/about/our-credentials',
        '/certified-financial-planner-for-federal-employees': '/about/our-credentials',

        // General pages
        '/planwell-for-federal-employee-benefits-education-and-retirement-planning': '/',
        '/federal-employees-info': '/services',
        '/private-sector-info': '/services',
        '/federal-employees': '/services',
        '/private-sector': '/services',

        // Legal
        '/privacy-statement-us': '/privacy',
        '/opt-out-preferences': '/privacy',

        // Lead gen / Thank you pages
        '/get-your-fers-retirement-guide-the-complete-handbook': '/book-call',
        '/thank-you-for-your-registration-1': '/book-call',
        '/federal-retirement-report-fers-retirement-estimate': '/book-call',
        '/federal-retirement-benefits-report': '/book-call',

        // Missing old articles → redirect to similar new articles
        '/2025-tax-deduction-standard-deduction-for-seniors-explained': '/blog/topic/fers',
        '/2026-gsa-mileage-reimbursement-rate-standard-mileage-rates-updated': '/2025-gsa-mileage-rates-for-reimbursement',
        '/2026-irmaa-brackets-and-medicare-part-b-and-part-d-premium-surcharges': '/2026-irmaa-brackets-anticipated-changes-to-medicare-costs',
        '/2026-retirement-plan-annual-limits-updated-for-tsp-401k-ira-and-more': '/2025-annual-limits-updated-tsp-401k-ira-and-more',
        '/average-pension-amount-for-federal-employee-retirement-system-fers': '/pension-calculator-calculate-fers-retirement-annuity-for-federal-employees',
        '/avoid-the-early-tsp-withdrawal-penalty-thrift-savings-plan-tips': '/tsp-withdrawal-rules-for-public-safety-employees-early-withdrawal-penalty',
        '/best-life-insurance-for-feds-fegli-option-b-vs-private-policy': '/comparing-federal-employee-group-life-insurance-fegli-option-b-with-term-life-insurance-which-is-right-for-you',
        '/enhanced-retirement-for-air-traffic-controller-supervisors': '/air-traffic-controller-retirement-age-and-fers-benefits',
        '/federal-employee-divorce-and-fers-dividing-federal-pension-and-tsp': '/navigating-divorce-understanding-the-impact-on-your-federal-employee-benefits-and-retirement',
        '/federal-employee-retirement-planning-choosing-a-financial-advisor': '/financial-advisor-or-financial-planner-whats-the-difference',
        '/fers-survivor-benefit-federal-retirement-annuity-options': '/fers-survivor-benefit-for-spouse-after-active-federal-employee-death',
        '/how-to-contact-opm-retirement-services-federal-retirement-guide': '/federal-ora-service-online-the-opm-online-retirement-application',
        '/pending-federal-retirement-claims-in-opm-backlog-hits-50000': '/flood-of-federal-retirement-applications-hits-opm-backlog',
        '/starting-2026-mandatory-catch-up-contributions-to-the-roth-tsp': '/tsp-and-401k-plan-tax-change-new-rule-for-catch-up-contributions',
        '/thrift-savings-plan-g-fund-current-rate-january-2026-tsp-planner': '/december-2025-g-fund-rate-today-for-thrift-savings-plan',
        '/tsp-investment-guidance-for-building-your-thrift-savings-plan-strategy': '/thrift-savings-plan-optimization-best-tsp-investing-strategies-for-2025',
    },
});
