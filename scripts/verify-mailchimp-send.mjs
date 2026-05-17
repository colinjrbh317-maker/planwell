#!/usr/bin/env node
/**
 * verify-mailchimp-send.mjs
 *
 * Sends a test campaign to a Mailtrap inbox address and polls Mailtrap for receipt.
 * Confirms Mailchimp send pipeline (auth, templating, deliverability) works end-to-end.
 *
 * Env vars:
 *   MAILCHIMP_API_KEY      ends with -us21 (datacenter)
 *   MAILCHIMP_LIST_ID      36da6474c8 (PlanWell list)
 *   MAILCHIMP_CAMPAIGN_ID  pre-created draft campaign reused for each verify run
 *   MAILTRAP_API_TOKEN
 *   MAILTRAP_ACCOUNT_ID
 *   MAILTRAP_INBOX_ID
 *   MAILTRAP_RECEIVE_ADDRESS  e.g. verify@<inbox>.mailtrap.io — must be a Mailchimp test subscriber
 */

import { setTimeout as sleep } from 'node:timers/promises';

const MC_KEY = process.env.MAILCHIMP_API_KEY;
const MC_CAMPAIGN = process.env.MAILCHIMP_CAMPAIGN_ID;
const MT_TOKEN = process.env.MAILTRAP_API_TOKEN;
const MT_ACCOUNT = process.env.MAILTRAP_ACCOUNT_ID;
const MT_INBOX = process.env.MAILTRAP_INBOX_ID;
const MT_TO = process.env.MAILTRAP_RECEIVE_ADDRESS;

if (!MC_KEY || !MC_CAMPAIGN || !MT_TOKEN || !MT_ACCOUNT || !MT_INBOX || !MT_TO) {
  console.error('Missing env vars (see header of this script)');
  process.exit(1);
}

const dc = MC_KEY.split('-')[1] ?? 'us21';
const marker = `pw-verify-${Date.now()}`;

console.log(`[verify-mailchimp-send] sending test for campaign=${MC_CAMPAIGN} marker=${marker}`);

const sendRes = await fetch(
  `https://${dc}.api.mailchimp.com/3.0/campaigns/${MC_CAMPAIGN}/actions/test`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Basic ${Buffer.from('anystring:' + MC_KEY).toString('base64')}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ test_emails: [MT_TO], send_type: 'html' }),
  },
);

if (!sendRes.ok) {
  console.error(`[verify-mailchimp-send] Mailchimp test send failed ${sendRes.status}: ${await sendRes.text()}`);
  process.exit(1);
}

console.log('[verify-mailchimp-send] test send requested, polling Mailtrap...');

const deadline = Date.now() + 90_000;
while (Date.now() < deadline) {
  await sleep(5_000);
  const r = await fetch(
    `https://mailtrap.io/api/accounts/${MT_ACCOUNT}/inboxes/${MT_INBOX}/messages?search=PlanWell`,
    { headers: { 'Api-Token': MT_TOKEN } },
  );
  if (!r.ok) continue;
  const msgs = await r.json();
  // Find a message arrived in the last 2 minutes
  const fresh = (Array.isArray(msgs) ? msgs : []).find((m) => {
    const age = Date.now() - new Date(m.created_at).getTime();
    return age < 120_000 && /PlanWell/i.test(m.subject);
  });
  if (fresh) {
    console.log(`[verify-mailchimp-send] ✅ delivered: "${fresh.subject}"`);
    process.exit(0);
  }
}

console.error('[verify-mailchimp-send] ❌ timeout — Mailchimp test send never landed in Mailtrap');
process.exit(1);
