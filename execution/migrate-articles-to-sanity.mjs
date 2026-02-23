#!/usr/bin/env node
/**
 * Migration script: articles.ts → Sanity CMS
 *
 * Reads all blog articles from src/data/articles.ts and creates
 * corresponding post documents in Sanity with proper author/category
 * references and HTML body content.
 *
 * Prerequisites:
 *   1. Add SANITY_WRITE_TOKEN to planwell-site/.env
 *      (Create at: https://www.sanity.io/manage/project/nwzt57tx/api#tokens)
 *   2. npm install dotenv (if not already installed)
 *
 * Usage:
 *   node execution/migrate-articles-to-sanity.mjs
 *   node execution/migrate-articles-to-sanity.mjs --dry-run
 */

import { createClient } from '@sanity/client';
import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = resolve(__dirname, '..');

// Load .env manually (avoid extra dependency)
const envPath = resolve(PROJECT_ROOT, '.env');
const envContent = readFileSync(envPath, 'utf-8');
const envVars = {};
for (const line of envContent.split('\n')) {
  const trimmed = line.trim();
  if (!trimmed || trimmed.startsWith('#')) continue;
  const eqIdx = trimmed.indexOf('=');
  if (eqIdx > 0) {
    envVars[trimmed.slice(0, eqIdx)] = trimmed.slice(eqIdx + 1);
  }
}

const SANITY_TOKEN = envVars.SANITY_WRITE_TOKEN || process.env.SANITY_WRITE_TOKEN;
const DRY_RUN = process.argv.includes('--dry-run');

if (!SANITY_TOKEN && !DRY_RUN) {
  console.error('ERROR: SANITY_WRITE_TOKEN not found in .env');
  console.error('Create a token at: https://www.sanity.io/manage/project/nwzt57tx/api#tokens');
  console.error('Then add to .env: SANITY_WRITE_TOKEN=your_token_here');
  process.exit(1);
}

const client = SANITY_TOKEN ? createClient({
  projectId: 'nwzt57tx',
  dataset: 'production',
  token: SANITY_TOKEN,
  apiVersion: '2024-01-01',
  useCdn: false,
}) : null;

// Author slug → Sanity ID mapping
const AUTHOR_MAP = {
  'brennan-rhule': 'b679b295-7d48-42c5-bf71-8e4628bae27d',
  'david-fei': '35568447-ae76-472e-b335-1a05f32ddcbe',
  'ben-derge': 'f5b2e9bd-656d-4389-8572-c447085da9c8',
  'planwell-team': '9d0be71d-575a-4d7a-b2f5-8e04265598bf',
};

// Category name → Sanity ID mapping
const CATEGORY_MAP = {
  'FERS': 'c6901942-ee68-443c-a9c2-7f94c811d760',
  'TSP & Investing': '55a43ad1-9601-4403-baf2-b8b7dd299a61',
  'FEHB & Medicare': 'a63dca23-6e15-4fe2-879a-4280c96cb4dc',
  'Social Security': '9a6a0f07-f084-4480-8efb-934c37765d94',
  'Tax Strategy': '0c60cd6c-4eea-4252-8491-8a059cd669ea',
};

/**
 * Parse articles from articles.ts using regex extraction.
 * The file is a TypeScript module with a Record<string, Article> export.
 */
function parseArticles() {
  const filePath = resolve(PROJECT_ROOT, 'src/data/articles.ts');
  const content = readFileSync(filePath, 'utf-8');

  const articles = [];
  // Match each article entry: 'slug': { ... }
  // We use a state machine approach to handle nested template literals
  const lines = content.split('\n');
  let currentArticle = null;
  let braceDepth = 0;
  let inContent = false;
  let contentLines = [];
  let articleText = '';

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Detect article start: '  'some-slug': {'
    const slugMatch = line.match(/^\s+'([a-z0-9-]+)':\s*\{$/);
    if (slugMatch && braceDepth === 0) {
      currentArticle = slugMatch[1];
      braceDepth = 1;
      articleText = '';
      continue;
    }

    if (currentArticle) {
      articleText += line + '\n';

      // Count braces (rough — skip those in strings)
      for (const ch of line) {
        if (ch === '{') braceDepth++;
        if (ch === '}') braceDepth--;
      }

      if (braceDepth <= 0) {
        // End of article object — parse fields
        const article = { slug: currentArticle };

        const titleMatch = articleText.match(/title:\s*'([^']*(?:\\.[^']*)*)'/);
        if (titleMatch) article.title = titleMatch[1].replace(/\\'/g, "'");

        const excerptMatch = articleText.match(/excerpt:\s*'([^']*(?:\\.[^']*)*)'/);
        if (excerptMatch) article.excerpt = excerptMatch[1].replace(/\\'/g, "'");

        const categoryMatch = articleText.match(/category:\s*'([^']*)'/);
        if (categoryMatch) article.category = categoryMatch[1];

        const authorMatch = articleText.match(/author:\s*'([^']*)'/);
        if (authorMatch) article.author = authorMatch[1];

        const dateMatch = articleText.match(/date:\s*'([^']*)'/);
        if (dateMatch) article.date = dateMatch[1];

        const readTimeMatch = articleText.match(/readTime:\s*'([^']*)'/);
        if (readTimeMatch) article.readTime = readTimeMatch[1];

        const imageMatch = articleText.match(/image:\s*'([^']*)'/);
        if (imageMatch) article.image = imageMatch[1];

        // Extract content (template literal between backticks)
        const contentStart = articleText.indexOf('content: `');
        if (contentStart !== -1) {
          const start = contentStart + 'content: `'.length;
          const end = articleText.lastIndexOf('`');
          if (end > start) {
            article.content = articleText.slice(start, end);
          }
        }

        if (article.title) {
          articles.push(article);
        }

        currentArticle = null;
        braceDepth = 0;
      }
    }
  }

  return articles;
}

/**
 * Convert a date string like "February 20, 2026" to ISO datetime
 */
function parseDate(dateStr) {
  try {
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return null;
    return d.toISOString();
  } catch {
    return null;
  }
}

/**
 * Resolve author slug to Sanity reference ID
 */
function resolveAuthor(authorSlug) {
  // Direct match
  if (AUTHOR_MAP[authorSlug]) return AUTHOR_MAP[authorSlug];
  // Fuzzy match
  if (authorSlug.includes('brennan')) return AUTHOR_MAP['brennan-rhule'];
  if (authorSlug.includes('david')) return AUTHOR_MAP['david-fei'];
  if (authorSlug.includes('ben') || authorSlug.includes('derge')) return AUTHOR_MAP['ben-derge'];
  // Default fallback
  return AUTHOR_MAP['planwell-team'];
}

async function migrate() {
  console.log('=== PlanWell Article Migration to Sanity ===\n');

  if (DRY_RUN) {
    console.log('🏃 DRY RUN MODE — no documents will be created\n');
  }

  // Parse articles
  console.log('📖 Parsing articles from articles.ts...');
  const articles = parseArticles();
  console.log(`   Found ${articles.length} articles\n`);

  if (articles.length === 0) {
    console.error('ERROR: No articles parsed. Check articles.ts format.');
    process.exit(1);
  }

  // Check existing posts to avoid duplicates
  let existingSet = new Set();
  if (client) {
    console.log('🔍 Checking for existing posts in Sanity...');
    const existingSlugs = await client.fetch(
      `*[_type == "post"]{"slug": slug.current}`
    );
    existingSet = new Set(existingSlugs.map(p => p.slug));
    console.log(`   Found ${existingSet.size} existing posts\n`);
  }

  // Filter out already-migrated articles
  const toMigrate = articles.filter(a => !existingSet.has(a.slug));
  console.log(`📝 ${toMigrate.length} articles to migrate (${articles.length - toMigrate.length} already exist)\n`);

  if (DRY_RUN) {
    console.log('Sample articles to migrate:');
    for (const a of toMigrate.slice(0, 5)) {
      console.log(`  - ${a.title} (${a.slug})`);
      console.log(`    Author: ${a.author} → ${resolveAuthor(a.author)}`);
      console.log(`    Category: ${a.category} → ${CATEGORY_MAP[a.category] || 'UNKNOWN'}`);
      console.log(`    Content length: ${(a.content || '').length} chars`);
    }
    console.log(`\n... and ${Math.max(0, toMigrate.length - 5)} more`);
    return;
  }

  // Migrate in batches of 10
  const BATCH_SIZE = 10;
  let created = 0;
  let failed = 0;

  for (let i = 0; i < toMigrate.length; i += BATCH_SIZE) {
    const batch = toMigrate.slice(i, i + BATCH_SIZE);
    const transaction = client.transaction();

    for (const article of batch) {
      const authorId = resolveAuthor(article.author);
      const categoryId = CATEGORY_MAP[article.category];

      const doc = {
        _type: 'post',
        title: article.title,
        slug: { _type: 'slug', current: article.slug },
        excerpt: article.excerpt || '',
        publishedAt: parseDate(article.date),
        readTime: article.readTime || '',
        htmlBody: article.content || '',
        author: {
          _type: 'reference',
          _ref: authorId,
        },
      };

      if (categoryId) {
        doc.category = {
          _type: 'reference',
          _ref: categoryId,
        };
      }

      transaction.create(doc);
    }

    try {
      const result = await transaction.commit();
      created += batch.length;
      console.log(`✅ Batch ${Math.floor(i / BATCH_SIZE) + 1}: ${batch.length} articles created (${created}/${toMigrate.length})`);
    } catch (err) {
      failed += batch.length;
      console.error(`❌ Batch ${Math.floor(i / BATCH_SIZE) + 1} failed:`, err.message);

      // Fall back to individual creates
      for (const article of batch) {
        try {
          const authorId = resolveAuthor(article.author);
          const categoryId = CATEGORY_MAP[article.category];

          const doc = {
            _type: 'post',
            title: article.title,
            slug: { _type: 'slug', current: article.slug },
            excerpt: article.excerpt || '',
            publishedAt: parseDate(article.date),
            readTime: article.readTime || '',
            htmlBody: article.content || '',
            author: {
              _type: 'reference',
              _ref: authorId,
            },
          };

          if (categoryId) {
            doc.category = {
              _type: 'reference',
              _ref: categoryId,
            };
          }

          await client.create(doc);
          created++;
          failed--;
          console.log(`  ✅ Retried: ${article.title}`);
        } catch (retryErr) {
          console.error(`  ❌ Failed: ${article.title} — ${retryErr.message}`);
        }
      }
    }
  }

  // Publish all new posts
  if (created > 0) {
    console.log(`\n📤 Publishing ${created} new posts...`);
    const drafts = await client.fetch(
      `*[_type == "post" && _id in path("drafts.**")]{ _id }`
    );

    if (drafts.length > 0) {
      // Publish in batches of 25
      for (let i = 0; i < drafts.length; i += 25) {
        const batch = drafts.slice(i, i + 25);
        const transaction = client.transaction();
        for (const draft of batch) {
          const publishedId = draft._id.replace('drafts.', '');
          // Fetch the draft, create published version, delete draft
          const doc = await client.getDocument(draft._id);
          if (doc) {
            const { _id, _rev, _createdAt, _updatedAt, ...rest } = doc;
            transaction.createOrReplace({ ...rest, _id: publishedId });
            transaction.delete(draft._id);
          }
        }
        try {
          await transaction.commit();
          console.log(`  ✅ Published batch ${Math.floor(i / 25) + 1}`);
        } catch (err) {
          console.error(`  ❌ Publish batch failed:`, err.message);
        }
      }
    }
  }

  console.log(`\n=== Migration Complete ===`);
  console.log(`Created: ${created}`);
  console.log(`Failed: ${failed}`);
  console.log(`Total in Sanity: ${existingSet.size + created}`);
}

migrate().catch(err => {
  console.error('Migration error:', err);
  process.exit(1);
});
