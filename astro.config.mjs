// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import vercel from '@astrojs/vercel';
import { createClient } from '@sanity/client';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const SITE_URL = 'https://planwellfp.com';

// Fetch all published article slugs from Sanity at build time so the
// 450+ blog posts actually appear in sitemap-0.xml.
async function getArticleUrls() {
    try {
        const client = createClient({
            projectId: 'nwzt57tx',
            dataset: 'production',
            useCdn: true,
            apiVersion: '2024-01-01',
        });
        const posts = await client.fetch(
            `*[_type == "post" && (!defined(publishedAt) || publishedAt <= now())]{ "slug": slug.current }`
        );
        return posts
            .filter((p) => p && p.slug)
            .map((p) => `${SITE_URL}/${p.slug}`);
    } catch (err) {
        console.warn('[sitemap] Sanity fetch failed; building without articles:', err?.message || err);
        return [];
    }
}

// Extract webinar IDs from local TS sources (regex is sufficient for
// simple data files and keeps the config from needing a TS loader).
function getWebinarUrls() {
    try {
        const here = dirname(fileURLToPath(import.meta.url));
        const webinars = readFileSync(resolve(here, 'src/data/webinars.ts'), 'utf8');
        const tspWebinars = readFileSync(resolve(here, 'src/data/tsp-webinars.ts'), 'utf8');
        const idRegex = /^\s*id:\s*'([^']+)'/gm;
        const urls = [];
        for (const match of webinars.matchAll(idRegex)) {
            urls.push(`${SITE_URL}/webinar/${match[1]}`);
        }
        for (const match of tspWebinars.matchAll(idRegex)) {
            urls.push(`${SITE_URL}/webinar/tsp/${match[1]}`);
        }
        return urls;
    } catch (err) {
        console.warn('[sitemap] Could not read webinar IDs:', err?.message || err);
        return [];
    }
}

const articleUrls = await getArticleUrls();
const webinarUrls = getWebinarUrls();
const customPages = [...articleUrls, ...webinarUrls];

console.log(`[sitemap] Including ${articleUrls.length} articles and ${webinarUrls.length} webinars as customPages`);

// https://astro.build/config
export default defineConfig({
    site: SITE_URL,
    adapter: vercel({
        isr: {
            expiration: 60,
        },
    }),
    integrations: [
        sitemap({
            changefreq: 'weekly',
            priority: 0.7,
            lastmod: new Date(),
            customPages,
        }),
    ],
    trailingSlash: 'never',
    redirects: {
        // Legacy WordPress URLs
        '/resources': '/blog',
        '/resources/:slug': '/:slug',

        // Blog/Resources
        '/federal-benefits-blog': '/blog',

        // Webinars
        '/federal-employee-retirement-benefits-education-workshops': '/federal-retirement-webinars',
        '/tsp-webinar-calendar': '/federal-retirement-webinars',
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

        // Calculators (URLs now match old site exactly)
        // Reverse redirects for anyone who bookmarked the temporary new URLs
        '/special-retirement-supplement-calculator': '/fers-supplement-calculator',
        '/sick-leave-conversion-calculator': '/fers-sick-leave-conversion-chart',
        '/federal-employee-retirement-planning-calculators': '/calculators',

        // Services
        '/financial-advisor-for-federal-employees': '/financial-planner-for-federal-employees',
        '/federal-employee-financial-advisor': '/financial-planner-for-federal-employees',
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
    },
});
