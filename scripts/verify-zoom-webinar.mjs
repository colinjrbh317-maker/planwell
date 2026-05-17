#!/usr/bin/env node
/**
 * verify-zoom-webinar.mjs
 *
 * Submits the PlanWell webinar registration form (or hits the API directly) and
 * queries the Zoom Server-to-Server OAuth API to confirm the registrant landed.
 *
 * Env vars:
 *   ZOOM_ACCOUNT_ID
 *   ZOOM_CLIENT_ID
 *   ZOOM_CLIENT_SECRET
 *   ZOOM_TEST_WEBINAR_ID   a dedicated test webinar (recurring or perpetual draft)
 *   BASE_URL               default https://planwellfp.com (or your preview URL)
 */

import { setTimeout as sleep } from 'node:timers/promises';

const ACCOUNT = process.env.ZOOM_ACCOUNT_ID;
const CLIENT = process.env.ZOOM_CLIENT_ID;
const SECRET = process.env.ZOOM_CLIENT_SECRET;
const WEBINAR = process.env.ZOOM_TEST_WEBINAR_ID;
const BASE = process.env.BASE_URL ?? 'http://localhost:4321';

if (!ACCOUNT || !CLIENT || !SECRET || !WEBINAR) {
  console.error('Missing Zoom env: ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, ZOOM_CLIENT_SECRET, ZOOM_TEST_WEBINAR_ID');
  process.exit(1);
}

// 1. Get OAuth token
const tokenRes = await fetch('https://zoom.us/oauth/token', {
  method: 'POST',
  headers: {
    'Authorization': `Basic ${Buffer.from(`${CLIENT}:${SECRET}`).toString('base64')}`,
    'Content-Type': 'application/x-www-form-urlencoded',
  },
  body: `grant_type=account_credentials&account_id=${ACCOUNT}`,
});
if (!tokenRes.ok) {
  console.error(`[verify-zoom] OAuth failed: ${await tokenRes.text()}`);
  process.exit(1);
}
const { access_token } = await tokenRes.json();

// 2. Submit registration
const marker = `verify-${Date.now()}`;
const email = `verify+${marker}@mailtrap.inbox`;
const reg = await fetch(`${BASE}/api/webinar/register`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    webinarId: WEBINAR,
    first_name: 'Verify',
    last_name: marker,
    email,
  }),
});
if (!reg.ok) {
  console.error(`[verify-zoom] registration form POST failed: ${reg.status}`);
  process.exit(1);
}

// 3. Wait for Zoom to register
await sleep(10_000);

// 4. Query Zoom for the registrant
const zr = await fetch(`https://api.zoom.us/v2/webinars/${WEBINAR}/registrants?status=approved`, {
  headers: { 'Authorization': `Bearer ${access_token}` },
});
if (!zr.ok) {
  console.error(`[verify-zoom] Zoom API failed: ${zr.status}`);
  process.exit(1);
}
const { registrants } = await zr.json();
const found = registrants?.find((r) => r.email === email);
if (!found) {
  console.error(`[verify-zoom] ❌ registrant ${email} not found in Zoom`);
  process.exit(1);
}

console.log(`[verify-zoom] ✅ registrant landed in Zoom: ${found.email}`);
process.exit(0);
