#!/usr/bin/env node
/**
 * verify-calculators.mjs
 *
 * Property-based tests for PlanWell financial calculators using fast-check.
 * Runs 1000 random valid inputs per calculator and asserts mathematical invariants.
 *
 * This is the single highest-value verification for PlanWell — calculator output
 * drives client retirement decisions. A wrong number = real client harm.
 *
 * Run: node scripts/verify-calculators.mjs
 */

import fc from 'fast-check';

// Lazy import calculators — adjust paths to your actual module structure.
// If the calculators live in TS files, run via `tsx scripts/verify-calculators.mjs`
// or compile to JS first. Placeholder imports below — replace with real ones.
let calculators;
try {
  calculators = await import('../src/lib/calculators/index.js');
} catch (e) {
  try {
    calculators = await import('../src/lib/calculators/index.ts');
  } catch {
    console.error('[verify-calculators] Could not import src/lib/calculators. Adjust import path in this script.');
    console.error('Expected: src/lib/calculators/index.{js,ts} exporting { fers, supplement, high3, sickLeave }');
    process.exit(1);
  }
}

const ITERATIONS = parseInt(process.env.VERIFY_ITERATIONS ?? '1000', 10);
let failures = 0;

function run(name, prop) {
  try {
    fc.assert(prop, { numRuns: ITERATIONS, verbose: false });
    console.log(`  ✅ ${name}`);
  } catch (e) {
    failures++;
    console.error(`  ❌ ${name}\n     ${e.message?.split('\n').slice(0, 3).join('\n     ')}`);
  }
}

console.log(`[verify-calculators] running ${ITERATIONS} iterations per invariant`);

// === FERS Pension ===
if (calculators.fers) {
  console.log('\nFERS pension invariants:');

  run('non-negative for valid inputs', fc.property(
    fc.integer({ min: 5, max: 50 }),   // years of service
    fc.integer({ min: 30000, max: 250000 }), // high-3 salary
    fc.integer({ min: 50, max: 75 }),  // retirement age
    (yos, salary, age) => {
      const r = calculators.fers({ yearsOfService: yos, high3Salary: salary, retirementAge: age });
      return Number.isFinite(r.annualPension) && r.annualPension >= 0;
    },
  ));

  run('monotonic in years of service (more years → bigger pension)', fc.property(
    fc.integer({ min: 5, max: 40 }),
    fc.integer({ min: 30000, max: 200000 }),
    fc.integer({ min: 62, max: 70 }),
    (yos, salary, age) => {
      const a = calculators.fers({ yearsOfService: yos, high3Salary: salary, retirementAge: age });
      const b = calculators.fers({ yearsOfService: yos + 1, high3Salary: salary, retirementAge: age });
      return b.annualPension >= a.annualPension;
    },
  ));

  run('monotonic in salary (higher salary → bigger pension)', fc.property(
    fc.integer({ min: 10, max: 40 }),
    fc.integer({ min: 30000, max: 150000 }),
    fc.integer({ min: 62, max: 70 }),
    (yos, salary, age) => {
      const a = calculators.fers({ yearsOfService: yos, high3Salary: salary, retirementAge: age });
      const b = calculators.fers({ yearsOfService: yos, high3Salary: salary + 10000, retirementAge: age });
      return b.annualPension >= a.annualPension;
    },
  ));

  run('no NaN/Infinity for any valid input', fc.property(
    fc.integer({ min: 5, max: 50 }),
    fc.integer({ min: 30000, max: 250000 }),
    fc.integer({ min: 50, max: 75 }),
    (yos, salary, age) => {
      const r = calculators.fers({ yearsOfService: yos, high3Salary: salary, retirementAge: age });
      return Object.values(r).every((v) => typeof v !== 'number' || (Number.isFinite(v) && !Number.isNaN(v)));
    },
  ));
}

// === FERS Supplement ===
if (calculators.supplement) {
  console.log('\nSupplement invariants:');

  run('positive for retirees under 62 with valid YOS', fc.property(
    fc.integer({ min: 20, max: 35 }),
    fc.integer({ min: 50000, max: 150000 }),
    fc.integer({ min: 55, max: 61 }),
    (yos, salary, age) => {
      const r = calculators.supplement({ yearsOfService: yos, high3Salary: salary, retirementAge: age });
      return r.annualSupplement > 0;
    },
  ));

  run('zero at 62 and above (supplement stops at SS age)', fc.property(
    fc.integer({ min: 20, max: 35 }),
    fc.integer({ min: 50000, max: 150000 }),
    fc.integer({ min: 62, max: 75 }),
    (yos, salary, age) => {
      const r = calculators.supplement({ yearsOfService: yos, high3Salary: salary, retirementAge: age });
      return r.annualSupplement === 0;
    },
  ));
}

// === High-3 Salary ===
if (calculators.high3) {
  console.log('\nHigh-3 invariants:');

  run('always equals average of three input salaries', fc.property(
    fc.integer({ min: 30000, max: 200000 }),
    fc.integer({ min: 30000, max: 200000 }),
    fc.integer({ min: 30000, max: 200000 }),
    (s1, s2, s3) => {
      const r = calculators.high3({ year1Salary: s1, year2Salary: s2, year3Salary: s3 });
      return Math.abs(r.high3 - (s1 + s2 + s3) / 3) < 0.01;
    },
  ));
}

// === Sick Leave ===
if (calculators.sickLeave) {
  console.log('\nSick leave conversion invariants:');

  run('non-negative months from non-negative hours', fc.property(
    fc.integer({ min: 0, max: 5000 }),
    (hours) => {
      const r = calculators.sickLeave({ unusedHours: hours });
      return r.additionalMonths >= 0 && Number.isFinite(r.additionalMonths);
    },
  ));

  run('monotonic in unused hours', fc.property(
    fc.integer({ min: 0, max: 4999 }),
    (hours) => {
      const a = calculators.sickLeave({ unusedHours: hours });
      const b = calculators.sickLeave({ unusedHours: hours + 1 });
      return b.additionalMonths >= a.additionalMonths;
    },
  ));
}

if (failures > 0) {
  console.error(`\n[verify-calculators] ❌ ${failures} invariant(s) failed`);
  process.exit(1);
}

console.log('\n[verify-calculators] ✅ all calculator invariants hold');
process.exit(0);
