#!/usr/bin/env tsx
// Generate a plain-text markdown file of ALL new page copy for compliance review.
// Pulls directly from source data (not rendered HTML) so no tile/preview truncation.
// Run: npx tsx scripts/generate-compliance-md.ts

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { agencies, type Agency } from '../src/data/agencies';
import { decisionGuides, type DecisionGuide } from '../src/data/decision-guides';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, '..', 'PlanWell-Compliance-Review-SEO-Phase-1.md');
const SITE = 'https://planwellfp.com';

const NEW_LOCATIONS = [
  'philadelphia', 'ogden', 'kansas-city', 'st-louis', 'chicago', 'boston',
  'seattle', 'oklahoma-city', 'albuquerque', 'jacksonville', 'phoenix',
  'anchorage', 'sacramento', 'richmond', 'charleston',
];

// Strip HTML tags + decode common entities, normalize whitespace, keep paragraph breaks
function stripHtml(html: string): string {
  return html
    .replace(/<br\s*\/?>/gi, '\n')
    .replace(/<\/p>/gi, '\n\n')
    .replace(/<\/li>/gi, '\n')
    .replace(/<li[^>]*>/gi, '- ')
    .replace(/<\/(h[1-6]|div|section)>/gi, '\n\n')
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x27;/g, "'")
    .replace(/&nbsp;/g, ' ')
    .replace(/&#x2019;/g, '\u2019')
    .replace(/&rsquo;/g, '\u2019')
    .replace(/&lsquo;/g, '\u2018')
    .replace(/&ldquo;/g, '\u201C')
    .replace(/&rdquo;/g, '\u201D')
    .replace(/&reg;/g, '\u00AE')
    .replace(/\u00AE/g, '\u00AE')
    .replace(/[ \t]+/g, ' ')
    .replace(/\n[ \t]+/g, '\n')
    .replace(/[ \t]+\n/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

const out: string[] = [];

function line(s = '') { out.push(s); }
function divider() { line(''); line('============================================================'); line(''); }
function sub() { line(''); line('------------------------------------------------------------'); line(''); }

// ---------- Cover ----------
line('PLANWELL FINANCIAL PLANNING');
line('SEO PHASE 1 CONTENT FOR COMPLIANCE REVIEW');
line('');
line(`Date: ${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}`);
line('');
line('WHAT THIS DOCUMENT CONTAINS');
line('');
line('Full page copy for 40 new SEO pages built for planwellfp.com, grouped by category:');
line('');
line('- 15 federal agency pages (/federal-agencies/{agency}) plus the hub page');
line('- 10 decision guides (/guides/{slug}) plus the hub page');
line('- 15 new city location pages (/locations/{city})');
line('');
line('HOW TO READ THIS DOCUMENT');
line('');
line('Each URL appears as its own section with a divider line above and below. For each page you will see:');
line('');
line('- URL (not yet pushed to production)');
line('- Meta title and meta description (what appears in Google search results)');
line('- Eyebrow, heading, and lead (hero section)');
line('- Full body copy in the order it appears on the page');
line('- Lists of positions and duty locations (agency pages only)');
line('- Full FAQ questions and answers');
line('- Standing educational disclaimer (decision guides only)');
line('');
line('PAGES NOT INCLUDED');
line('');
line('The 14 existing, previously-approved city location pages (Atlanta, Colorado Springs, Dallas-Fort Worth, Denver, Fort Meade, Honolulu, Huntsville, Maryland, Norfolk, Northern Virginia, San Antonio, San Diego, Tampa, Washington DC) are not included. Their content did not change; only the underlying page template was refactored to reuse shared components. The "Typical [City] Advisors" comparison card label was softened to "Many [City] Advisors" across all 29 location pages (existing and new) as a compliance improvement.');
line('');
line('STANDING DISCLOSURES');
line('');
line('Every page wraps in a shared BaseLayout that already emits the full Osaic Wealth, FINRA, and SIPC compliance footer, plus the non-affiliation disclaimer regarding OPM and federal agencies. These appear on every live page but are not repeated below to keep the review focused on new copy.');
line('');
line('Each of the 10 decision guides now ends with a standing educational disclaimer stating that the content is not tax, legal, or investment advice and that readers should consult qualified professionals. That disclaimer is captured below in each guide section.');
line('');

// ---------- Agency hub ----------
divider();
line('SECTION: FEDERAL AGENCY PAGES');
divider();
line('URL: ' + SITE + '/federal-agencies');
line('');
line('META TITLE: FERS Retirement Planning by Federal Agency | PlanWell Financial Planning');
line('');
line('META DESCRIPTION: PlanWell helps civilian employees at every major federal agency plan their FERS retirement. Find guidance tailored to your agency: DoD, VA, DHS, USPS, IRS, and more.');
line('');
line('EYEBROW: Agency-Specific Planning');
line('');
line('HEADING: FERS Retirement Planning by Federal Agency');
line('');
line('LEAD');
line('');
line('Every agency has its quirks: how it handles military service credit, which buyout authorities apply, whether special provisions cover your job series. Pick your agency to see how PlanWell helps.');
line('');
line('BODY');
line('');
line('Agencies we work with. Listed below with a one-line description and employee count. Each tile on the live page links to its own agency-specific page.');
line('');
for (const a of agencies) {
  line(`- ${a.name} (${a.employeeCount})`);
}
line('');
line('Do not see your agency? FERS rules are the same across the civilian federal government. Attend a free workshop and bring your questions.');
line('');

// ---------- Individual agencies ----------
for (const a of agencies) {
  divider();
  line('URL: ' + SITE + '/federal-agencies/' + a.slug);
  line('');
  line('META TITLE: ' + a.metaTitle);
  line('');
  line('META DESCRIPTION: ' + a.metaDescription);
  line('');
  line('EYEBROW: ' + a.heroEyebrow);
  line('');
  line('HEADING: ' + a.heroHeading);
  line('');
  line('LEAD');
  line('');
  line(a.heroLead);
  line('');
  line('Employee count: ' + a.employeeCount);
  line('');

  sub();
  line('INTRODUCTION');
  line('');
  line(stripHtml(a.introHtml));
  line('');

  sub();
  line(`WHY FERS PLANNING MATTERS MORE FOR ${a.shortName.toUpperCase()} CIVILIANS`);
  line('');
  line(stripHtml(a.whyMattersHtml));
  line('');

  sub();
  line(`WHAT MAKES ${a.shortName.toUpperCase()} RETIREMENT PLANNING DIFFERENT`);
  line('');
  for (const c of a.uniqueConsiderations) {
    line(c.title);
    line('');
    line(c.body);
    line('');
  }

  if (a.specialProvisionsNote) {
    sub();
    line('SPECIAL PROVISIONS NOTE');
    line('');
    line(a.specialProvisionsNote);
    line('');
  }

  sub();
  line(`WHO WE WORK WITH AT ${a.shortName.toUpperCase()}`);
  line('');
  line('Common positions');
  line('');
  for (const j of a.commonJobs) line(`- ${j}`);
  line('');
  line('Primary duty locations');
  line('');
  for (const loc of a.primaryLocations) line(`- ${loc}`);
  line('');
  line('Common questions we hear');
  line('');
  line(stripHtml(a.commonQuestionsHtml));
  line('');

  sub();
  line(`${a.shortName.toUpperCase()} RETIREMENT FAQs`);
  line('');
  for (const f of a.faq) {
    line('Q: ' + f.q);
    line('');
    line('A: ' + stripHtml(f.a));
    line('');
  }
}

// ---------- Guides hub ----------
divider();
line('SECTION: DECISION GUIDES');
divider();
line('URL: ' + SITE + '/guides');
line('');
line('META TITLE: FERS Decision Guides for Federal Employees | PlanWell Financial Planning');
line('');
line('META DESCRIPTION: Practical, scenario-based guides for the biggest federal retirement decisions. Read the right one before you act.');
line('');
line('EYEBROW: Federal Retirement Decisions');
line('');
line('HEADING: Decision Guides for Federal Retirement');
line('');
line('LEAD');
line('');
line('Federal retirement has a handful of hinge decisions that swing your lifetime income by six figures. Each guide below walks through one of them with real numbers, a decision framework, and a FAQ.');
line('');
line('GUIDES LISTED ON HUB');
line('');
for (const g of decisionGuides) {
  line(`- ${g.heroHeading}`);
}
line('');

// ---------- Individual guides ----------
for (const g of decisionGuides) {
  divider();
  line('URL: ' + SITE + '/guides/' + g.slug);
  line('');
  line('META TITLE: ' + g.metaTitle);
  line('');
  line('META DESCRIPTION: ' + g.metaDescription);
  line('');
  line('EYEBROW: ' + g.heroEyebrow);
  line('');
  line('HEADING: ' + g.heroHeading);
  line('');
  line('LEAD');
  line('');
  line(g.heroLead);
  line('');

  sub();
  line('BOTTOM LINE UP FRONT');
  line('');
  line(g.tldr);
  line('');

  for (const s of g.sections) {
    sub();
    line(s.heading.toUpperCase());
    line('');
    line(stripHtml(s.html));
    line('');
  }

  if (g.decisionMatrix && g.decisionMatrix.length > 0) {
    sub();
    line('DECISION MATRIX');
    line('');
    for (const d of g.decisionMatrix) {
      line('Scenario: ' + d.scenario);
      line('Recommendation: ' + d.recommendation);
      line('');
    }
  }

  if (g.relatedCalculator) {
    sub();
    line('RELATED CALCULATOR');
    line('');
    line(`${g.relatedCalculator.label}: ${SITE}${g.relatedCalculator.href}`);
    line('');
  }

  sub();
  line('FAQ');
  line('');
  for (const f of g.faq) {
    line('Q: ' + f.q);
    line('');
    line('A: ' + stripHtml(f.a));
    line('');
  }
}

// ---------- Locations ----------
divider();
line('SECTION: NEW CITY LOCATION PAGES');
divider();

function extractLocationContent(slug: string): string {
  const file = path.join(ROOT, 'src', 'pages', 'locations', slug + '.astro');
  if (!fs.existsSync(file)) return '';
  return fs.readFileSync(file, 'utf8');
}

function extractBaseLayoutProp(src: string, prop: string): string {
  const rx = new RegExp(`${prop}=(?:"([^"]+)"|\\{[\`'"]([^\\\`'"]+)[\`'"]\\})`);
  const m = src.match(rx);
  return m ? (m[1] || m[2] || '') : '';
}

function astroBodyText(src: string): string {
  // Grab everything inside <BaseLayout>...</BaseLayout>, then strip tags
  const m = src.match(/<BaseLayout[^>]*>([\s\S]*?)<\/BaseLayout>/);
  if (!m) return '';
  let body = m[1];

  // Remove shared component invocations (WebinarCTA, FAQSchema) and capture their props
  // For FAQSchema, extract the inline questions array from the top faqs const in frontmatter
  body = body.replace(/<WebinarCTA[^>]*\/?>/g, '[[WEBINAR_CTA]]\n');
  body = body.replace(/<FAQSchema[^>]*\/?>/g, '[[FAQ_HERE]]\n');
  body = body.replace(/\{[^}]*\}/g, ''); // strip remaining JSX expressions

  // Convert block tags to newlines
  return stripHtml(body);
}

function extractFaqsFromFrontmatter(src: string): { q: string; a: string }[] {
  const fm = src.match(/^---([\s\S]*?)---/);
  if (!fm) return [];
  const frontmatter = fm[1];
  const faqsMatch = frontmatter.match(/const\s+faqs\s*=\s*\[([\s\S]*?)\];/);
  if (!faqsMatch) return [];
  const body = faqsMatch[1];
  const items: { q: string; a: string }[] = [];
  const itemRx = /\{\s*q\s*:\s*["']([\s\S]*?)["']\s*,\s*a\s*:\s*["']([\s\S]*?)["']\s*,?\s*\}/g;
  let m;
  while ((m = itemRx.exec(body))) {
    items.push({ q: m[1].replace(/\\"/g, '"').replace(/\\'/g, "'"), a: m[2].replace(/\\"/g, '"').replace(/\\'/g, "'") });
  }
  return items;
}

for (const slug of NEW_LOCATIONS) {
  const src = extractLocationContent(slug);
  if (!src) { line('MISSING: ' + slug); continue; }

  const title = extractBaseLayoutProp(src, 'title');
  const desc = extractBaseLayoutProp(src, 'description');
  const body = astroBodyText(src);
  const faqs = extractFaqsFromFrontmatter(src);

  divider();
  line('URL: ' + SITE + '/locations/' + slug);
  line('');
  line('META TITLE: ' + title);
  line('');
  line('META DESCRIPTION: ' + desc);
  line('');
  sub();
  line('PAGE BODY');
  line('');
  line(body.replace(/\[\[WEBINAR_CTA\]\]/g, '[Register for Free Workshop CTA block]').replace(/\[\[FAQ_HERE\]\]/g, ''));
  line('');

  if (faqs.length > 0) {
    sub();
    line(`${slug.toUpperCase().replace(/-/g, ' ')} FEDERAL RETIREMENT FAQs`);
    line('');
    for (const f of faqs) {
      line('Q: ' + f.q);
      line('');
      line('A: ' + f.a);
      line('');
    }
  }
}

// ---------- End ----------
divider();
line('END OF DOCUMENT');
divider();

const content = out.join('\n');
fs.writeFileSync(OUT, content);
console.log('Wrote:', OUT);
console.log('Size:', (content.length / 1024).toFixed(1) + ' KB');
console.log('Lines:', out.length);
