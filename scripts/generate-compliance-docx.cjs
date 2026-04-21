#!/usr/bin/env node
/**
 * Generate compliance-review docx from built HTML.
 * One URL per section with H1/H2 structure, meta, body copy, FAQs.
 *
 * Run from project root:
 *   node scripts/generate-compliance-docx.js
 */

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, PageBreak,
  AlignmentType, PageOrientation, TableOfContents, LevelFormat,
  BorderStyle, Header, Footer, PageNumber,
} = require('docx');

const DIST = path.join(__dirname, '..', 'dist', 'client');
const OUT = path.join(__dirname, '..', '..', 'PlanWell-Compliance-Review-SEO-Phase-1.docx');

const SITE = 'https://planwellfp.com';

const AGENCIES = [
  'department-of-defense', 'department-of-veterans-affairs', 'department-of-homeland-security',
  'us-postal-service', 'internal-revenue-service', 'department-of-justice',
  'department-of-state', 'nasa', 'department-of-health-and-human-services',
  'social-security-administration', 'environmental-protection-agency',
  'department-of-energy', 'department-of-agriculture', 'department-of-commerce',
  'department-of-the-interior',
];

const GUIDES = [
  'mra-10-vs-mra-30', 'csrs-vs-fers', 'deferred-vs-postponed-retirement',
  'divorce-and-fers', 'fers-disability-retirement', 'vera-vsip-explained',
  'when-should-federal-employees-retire', 'fers-supplement-earnings-test',
  'fehb-to-medicare-transition', 'survivor-benefit-election-guide',
];

const NEW_LOCATIONS = [
  'philadelphia', 'ogden', 'kansas-city', 'st-louis', 'chicago', 'boston',
  'seattle', 'oklahoma-city', 'albuquerque', 'jacksonville', 'phoenix',
  'anchorage', 'sacramento', 'richmond', 'charleston',
];

function decodeEntities(s) {
  return s
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#x27;/g, "'")
    .replace(/&#x2019;/g, "\u2019")
    .replace(/&#x201C;/g, "\u201C")
    .replace(/&#x201D;/g, "\u201D")
    .replace(/&#xAE;/g, "\u00AE")
    .replace(/&reg;/g, "\u00AE")
    .replace(/&nbsp;/g, ' ')
    .replace(/&#8217;/g, "\u2019")
    .replace(/&#8220;/g, "\u201C")
    .replace(/&#8221;/g, "\u201D");
}

function readHtml(url) {
  const file = path.join(DIST, url.replace(/^\//, ''), 'index.html');
  if (!fs.existsSync(file)) {
    console.warn('MISSING:', file);
    return null;
  }
  return fs.readFileSync(file, 'utf8');
}

function extractMeta(html) {
  const title = (html.match(/<title>([^<]+)<\/title>/) || [])[1] || '';
  const desc = (html.match(/<meta\s+name="description"\s+content="([^"]+)"/) || [])[1] || '';
  const canonical = (html.match(/<link\s+rel="canonical"\s+href="([^"]+)"/) || [])[1] || '';
  return { title: decodeEntities(title), description: decodeEntities(desc), canonical };
}

function extractMain(html) {
  const main = (html.match(/<main[^>]*>([\s\S]*?)<\/main>/) || [])[1] || '';
  return main;
}

function stripTags(html) {
  return decodeEntities(
    html
      .replace(/<script[\s\S]*?<\/script>/g, '')
      .replace(/<style[\s\S]*?<\/style>/g, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/\s+/g, ' ')
      .trim()
  );
}

function parseBlocks(mainHtml) {
  // Split by section boundaries, strip tags per chunk, keep hierarchy
  const blocks = [];
  const sectionRe = /<section[^>]*>([\s\S]*?)<\/section>/g;
  let m;
  while ((m = sectionRe.exec(mainHtml))) {
    blocks.push(m[1]);
  }
  if (blocks.length === 0) blocks.push(mainHtml);
  return blocks;
}

function extractStructure(sectionHtml) {
  // Extract headings and text content preserving order
  const items = [];
  const tokenRe = /<(h[1-6]|p|li|summary|strong|em|table|tr|th|td)[^>]*>([\s\S]*?)<\/\1>/gi;
  let m;
  while ((m = tokenRe.exec(sectionHtml))) {
    const tag = m[1].toLowerCase();
    const text = stripTags(m[2]);
    if (!text || text.length < 2) continue;
    items.push({ tag, text });
  }
  return items;
}

const PARA_STYLE = {
  run: { font: 'Calibri', size: 22 },
  paragraph: { spacing: { after: 120, line: 280 } },
};

function p(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, ...opts.run })],
    ...opts.para,
  });
}

function heading(text, level) {
  const map = {
    1: HeadingLevel.HEADING_1,
    2: HeadingLevel.HEADING_2,
    3: HeadingLevel.HEADING_3,
    4: HeadingLevel.HEADING_4,
  };
  return new Paragraph({
    heading: map[level] || HeadingLevel.HEADING_3,
    children: [new TextRun({ text, bold: true })],
    spacing: { before: level === 1 ? 300 : 200, after: level === 1 ? 200 : 120 },
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: 'bullets', level: 0 },
    children: [new TextRun({ text })],
  });
}

function metaLine(label, value) {
  return new Paragraph({
    children: [
      new TextRun({ text: label + ': ', bold: true }),
      new TextRun({ text: value }),
    ],
    spacing: { after: 80 },
  });
}

function buildSection(category, slug, html) {
  const meta = extractMeta(html);
  const main = extractMain(html);
  const sections = parseBlocks(main);
  const url = `${SITE}/${category}/${slug}`;

  const children = [];
  children.push(heading(`${category}/${slug}`, 1));
  children.push(metaLine('URL', url));
  children.push(metaLine('Meta title', meta.title));
  children.push(metaLine('Meta description', meta.description));
  children.push(p('', { para: { spacing: { after: 200 } } }));

  // Extract and write each section
  for (const sectionHtml of sections) {
    const items = extractStructure(sectionHtml);
    if (items.length === 0) continue;

    // skip navigation/footer repeat content (heuristic)
    const joined = items.map(i => i.text).join(' ').slice(0, 200);
    if (/securities and advisory services|FINRA|SIPC|Osaic Wealth/i.test(joined) && items.length < 6) continue;

    let lastTag = '';
    let inList = false;
    for (const item of items) {
      // dedupe consecutive identical
      if (item.text === lastTag) continue;
      lastTag = item.text;

      if (/^h[1-2]$/.test(item.tag)) {
        children.push(heading(item.text, 2));
        inList = false;
      } else if (/^h[3-4]$/.test(item.tag)) {
        children.push(heading(item.text, 3));
        inList = false;
      } else if (item.tag === 'summary') {
        children.push(new Paragraph({
          children: [new TextRun({ text: 'Q: ' + item.text, bold: true })],
          spacing: { before: 120, after: 40 },
        }));
      } else if (item.tag === 'li') {
        children.push(bullet(item.text));
        inList = true;
      } else if (item.tag === 'p') {
        children.push(p(item.text, { para: { spacing: { after: 120 } } }));
        inList = false;
      }
    }
  }

  // page break for next page
  children.push(new Paragraph({ children: [new PageBreak()] }));
  return children;
}

function buildHub(category, title) {
  const url = `${SITE}/${category}`;
  const html = readHtml(category);
  if (!html) return [];
  const meta = extractMeta(html);
  const children = [];
  children.push(heading(title + ' (hub)', 1));
  children.push(metaLine('URL', url));
  children.push(metaLine('Meta title', meta.title));
  children.push(metaLine('Meta description', meta.description));
  const main = extractMain(html);
  const items = extractStructure(main);
  for (const item of items) {
    if (/^h[1-2]$/.test(item.tag)) children.push(heading(item.text, 2));
    else if (/^h[3-4]$/.test(item.tag)) children.push(heading(item.text, 3));
    else if (item.tag === 'p') children.push(p(item.text));
    else if (item.tag === 'li') children.push(bullet(item.text));
  }
  children.push(new Paragraph({ children: [new PageBreak()] }));
  return children;
}

function buildCover() {
  return [
    new Paragraph({
      heading: HeadingLevel.HEADING_1,
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: 'PlanWell Financial Planning', bold: true, size: 40 })],
      spacing: { before: 2000, after: 200 },
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: 'SEO Phase 1 Content for Compliance Review', size: 32 })],
      spacing: { after: 400 },
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }), size: 24, italics: true })],
      spacing: { after: 1200 },
    }),
    heading('What this document contains', 2),
    p('This document contains all page copy for 40 new SEO pages built for planwellfp.com, grouped by category:'),
    bullet('15 federal agency pages (/federal-agencies/{agency}) plus the hub page'),
    bullet('10 decision guides (/guides/{slug}) plus the hub page'),
    bullet('15 new city location pages (/locations/{city})'),
    p(''),
    heading('How to read this document', 2),
    p('Each URL appears as a Heading 1 section. Under each URL you will find:'),
    bullet('The live URL (not yet pushed to production)'),
    bullet('Meta title and meta description (what appears in Google search results)'),
    bullet('Full body copy as rendered, including headings, paragraphs, lists, and FAQs'),
    bullet('FAQ items are labeled with "Q:" prefix followed by the question, with the answer paragraph immediately below'),
    p(''),
    heading('Pages not included', 2),
    p('The 14 existing, previously-approved city location pages (Atlanta, Colorado Springs, Dallas-Fort Worth, Denver, Fort Meade, Honolulu, Huntsville, Maryland, Norfolk, Northern Virginia, San Antonio, San Diego, Tampa, Washington DC) are not included. Their content did not change, only the underlying page template was refactored to reuse shared components. The "Typical [City] Advisors" comparison card label was softened to "Many [City] Advisors" across all 29 location pages (existing and new) as a compliance improvement.'),
    p(''),
    heading('Standing disclosures', 2),
    p('Every page wraps in a shared BaseLayout that already emits the full Osaic Wealth, FINRA, and SIPC compliance footer, plus the non-affiliation disclaimer regarding OPM and federal agencies. These appear on every live page but are not repeated in this document to keep the review focused on new copy.'),
    p('Each of the 10 decision guides now ends with a standing educational disclaimer stating that the content is not tax, legal, or investment advice and that readers should consult qualified professionals. That disclaimer is captured below in each guide section.'),
    p(''),
    heading('Questions?', 2),
    p('Direct any questions about this content to David Fei or Brennan Rhule at PlanWell Financial Planning.'),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

async function main() {
  const body = [];
  body.push(...buildCover());

  // Agencies
  body.push(heading('Federal Agency Pages', 1));
  body.push(p('15 pages plus one hub page. Target audience: federal civilian employees searching for agency-specific retirement guidance.'));
  body.push(new Paragraph({ children: [new PageBreak()] }));
  body.push(...buildHub('federal-agencies', 'Federal Agencies'));
  for (const slug of AGENCIES) {
    const html = readHtml(`federal-agencies/${slug}`);
    if (!html) continue;
    body.push(...buildSection('federal-agencies', slug, html));
  }

  // Guides
  body.push(heading('Decision Guides', 1));
  body.push(p('10 pages plus one hub page. Target audience: federal employees making specific retirement decisions.'));
  body.push(new Paragraph({ children: [new PageBreak()] }));
  body.push(...buildHub('guides', 'Decision Guides'));
  for (const slug of GUIDES) {
    const html = readHtml(`guides/${slug}`);
    if (!html) continue;
    body.push(...buildSection('guides', slug, html));
  }

  // New locations
  body.push(heading('New City Location Pages', 1));
  body.push(p('15 new city pages. Target audience: federal employees in major federal hubs outside the 14 cities already covered.'));
  body.push(new Paragraph({ children: [new PageBreak()] }));
  for (const slug of NEW_LOCATIONS) {
    const html = readHtml(`locations/${slug}`);
    if (!html) continue;
    body.push(...buildSection('locations', slug, html));
  }

  const doc = new Document({
    creator: 'PlanWell Financial Planning',
    title: 'SEO Phase 1 Content for Compliance Review',
    styles: {
      default: { document: { run: { font: 'Calibri', size: 22 } } },
      paragraphStyles: [
        { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 32, bold: true, font: 'Calibri', color: '1E3A5F' },
          paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 } },
        { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 28, bold: true, font: 'Calibri', color: '1E3A5F' },
          paragraph: { spacing: { before: 240, after: 160 }, outlineLevel: 1 } },
        { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 24, bold: true, font: 'Calibri', color: '333333' },
          paragraph: { spacing: { before: 180, after: 120 }, outlineLevel: 2 } },
        { id: 'Heading4', name: 'Heading 4', basedOn: 'Normal', next: 'Normal', quickFormat: true,
          run: { size: 22, bold: true, italics: true, font: 'Calibri' },
          paragraph: { spacing: { before: 120, after: 80 }, outlineLevel: 3 } },
      ],
    },
    numbering: {
      config: [
        { reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '\u2022', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      ],
    },
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
        },
      },
      headers: {
        default: new Header({ children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: 'PlanWell SEO Phase 1 — Compliance Review', size: 18, italics: true, color: '666666' })],
        })] }),
      },
      footers: {
        default: new Footer({ children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: 'Page ', size: 18, color: '666666' }), new TextRun({ children: [PageNumber.CURRENT], size: 18, color: '666666' })],
        })] }),
      },
      children: body,
    }],
  });

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(OUT, buffer);
  console.log('Wrote:', OUT);
  console.log('Size:', (buffer.length / 1024).toFixed(1) + ' KB');
  console.log('Body elements:', body.length);
}

main().catch((e) => { console.error(e); process.exit(1); });
