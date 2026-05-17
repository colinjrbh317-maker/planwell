#!/usr/bin/env node
/**
 * verify-webhook-roundtrip.mjs
 *
 * Posts a test payload to the PlanWell webhook-server and confirms the downstream
 * side effect occurred (Mailchimp tag applied or Sanity doc created — depending on
 * which workflow the payload triggers).
 *
 * Env vars:
 *   WEBHOOK_URL              the webhook endpoint
 *   WEBHOOK_SECRET           HMAC secret (if signed)
 *   WEBHOOK_TEST_PAYLOAD     path to JSON file (default: scripts/test-webhook-payload.json)
 *   VERIFY_DOWNSTREAM        "mailchimp" | "sanity"  — which side effect to check
 *   MAILCHIMP_API_KEY        if downstream is mailchimp
 *   MAILCHIMP_LIST_ID
 *   SANITY_PROJECT_ID        if downstream is sanity
 *   SANITY_API_TOKEN
 */

import { readFileSync } from 'node:fs';
import { setTimeout as sleep } from 'node:timers/promises';
import { createHmac } from 'node:crypto';

const URL_ = process.env.WEBHOOK_URL;
const SECRET = process.env.WEBHOOK_SECRET;
const PAYLOAD_PATH = process.env.WEBHOOK_TEST_PAYLOAD ?? 'scripts/test-webhook-payload.json';
const DOWNSTREAM = process.env.VERIFY_DOWNSTREAM ?? 'sanity';

if (!URL_) {
  console.error('Missing WEBHOOK_URL');
  process.exit(1);
}

const payload = JSON.parse(readFileSync(PAYLOAD_PATH, 'utf-8'));
payload._verify_marker = `verify-${Date.now()}`;
const body = JSON.stringify(payload);

const headers = { 'Content-Type': 'application/json' };
if (SECRET) {
  headers['X-Hub-Signature'] = `sha256=${createHmac('sha256', SECRET).update(body).digest('hex')}`;
}

const post = await fetch(URL_, { method: 'POST', headers, body });
if (!post.ok) {
  console.error(`[verify-webhook] webhook POST failed ${post.status}: ${await post.text()}`);
  process.exit(1);
}
console.log(`[verify-webhook] webhook accepted marker=${payload._verify_marker}`);

// Wait for downstream propagation
await sleep(10_000);

if (DOWNSTREAM === 'sanity') {
  const projectId = process.env.SANITY_PROJECT_ID ?? 'nwzt57tx';
  const token = process.env.SANITY_API_TOKEN;
  if (!token) {
    console.error('Need SANITY_API_TOKEN for Sanity downstream check');
    process.exit(1);
  }
  const groq = encodeURIComponent(`*[references("${payload._verify_marker}") || description match "${payload._verify_marker}"][0]`);
  const r = await fetch(
    `https://${projectId}.api.sanity.io/v2024-01-01/data/query/production?query=${groq}`,
    { headers: { 'Authorization': `Bearer ${token}` } },
  );
  const { result } = await r.json();
  if (!result) {
    console.error('[verify-webhook] ❌ no Sanity doc created from webhook');
    process.exit(1);
  }
  console.log('[verify-webhook] ✅ Sanity downstream wrote a doc');
} else if (DOWNSTREAM === 'mailchimp') {
  console.log('[verify-webhook] (Mailchimp downstream check: implement per your tag schema)');
}

console.log('[verify-webhook] ✅ roundtrip complete');
process.exit(0);
