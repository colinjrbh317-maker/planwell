#!/usr/bin/env node
/**
 * verify-n8n-health.mjs
 *
 * Checks n8n instance health and validates that critical workflows are active + their
 * last execution succeeded. Designed to run before AND after any workflow edit.
 *
 * Env vars:
 *   N8N_BASE_URL    e.g. https://n8n.planwellfp.com
 *   N8N_API_KEY     X-N8N-API-KEY header
 *   N8N_CRITICAL_WORKFLOW_IDS  comma-separated workflow IDs that MUST be active + healthy
 */

const BASE = process.env.N8N_BASE_URL;
const KEY = process.env.N8N_API_KEY;
const CRITICAL = (process.env.N8N_CRITICAL_WORKFLOW_IDS ?? '').split(',').map((s) => s.trim()).filter(Boolean);

if (!BASE || !KEY) {
  console.error('Missing env: N8N_BASE_URL, N8N_API_KEY');
  process.exit(1);
}

const headers = { 'X-N8N-API-KEY': KEY, 'Content-Type': 'application/json' };
let failures = 0;

// 1. Health
const healthRes = await fetch(`${BASE}/healthz`).catch(() => null);
if (!healthRes || !healthRes.ok) {
  console.error(`[verify-n8n-health] ❌ /healthz unreachable`);
  process.exit(1);
}
console.log('[verify-n8n-health] ✅ n8n is up');

// 2. Critical workflows active?
for (const id of CRITICAL) {
  const r = await fetch(`${BASE}/api/v1/workflows/${id}`, { headers });
  if (!r.ok) {
    console.error(`  ❌ workflow ${id}: ${r.status}`);
    failures++;
    continue;
  }
  const wf = await r.json();
  if (!wf.active) {
    console.error(`  ❌ workflow ${id} (${wf.name}): NOT active`);
    failures++;
    continue;
  }
  console.log(`  ✅ ${wf.name} active`);
}

// 3. Recent execution status
for (const id of CRITICAL) {
  const r = await fetch(`${BASE}/api/v1/executions?workflowId=${id}&limit=1`, { headers });
  if (!r.ok) continue;
  const { data } = await r.json();
  if (!data || data.length === 0) {
    console.log(`  ⚠️  ${id}: no executions yet (skipping)`);
    continue;
  }
  const exec = data[0];
  if (exec.finished && !exec.stoppedAt) continue;
  if (exec.status === 'error' || (exec.stoppedAt && !exec.finished)) {
    console.error(`  ❌ ${id}: last execution failed at ${exec.stoppedAt}`);
    failures++;
  }
}

if (failures > 0) {
  console.error(`\n[verify-n8n-health] ❌ ${failures} failure(s)`);
  process.exit(1);
}
console.log('\n[verify-n8n-health] ✅ all checks pass');
process.exit(0);
