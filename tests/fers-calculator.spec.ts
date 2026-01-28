import { test, expect } from '@playwright/test';

test.describe('FERS Pension Calculator', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/fers-retirement-calculator');
  });

  test('should load calculator page with all form fields', async ({ page }) => {
    // Check page title (use specific selector to avoid Astro toolbar h1 elements)
    await expect(page.locator('.page-hero h1')).toContainText('FERS Pension Calculator');

    // Check all input fields are present
    await expect(page.locator('#retirement-type')).toBeVisible();
    await expect(page.locator('#high3')).toBeVisible();
    await expect(page.locator('#birthdate')).toBeVisible();
    await expect(page.locator('#scd')).toBeVisible();
    await expect(page.locator('#retirement-date')).toBeVisible();
    await expect(page.locator('#sick-leave-hours')).toBeVisible();
    await expect(page.locator('#military-years')).toBeVisible();
    await expect(page.locator('#military-months')).toBeVisible();

    // Check calculate button
    await expect(page.locator('.calculate-btn')).toBeVisible();
    await expect(page.locator('.calculate-btn')).toContainText('Calculate My Pension');
  });

  test('should calculate Normal Retirement pension correctly', async ({ page }) => {
    // Fill form for Normal Retirement
    await page.selectOption('#retirement-type', 'normal');
    await page.fill('#high3', '100000');
    await page.fill('#birthdate', '1960-01-01');
    await page.fill('#scd', '1990-01-01');
    await page.fill('#retirement-date', '2022-01-01');
    await page.fill('#sick-leave-hours', '0');
    await page.fill('#military-years', '0');
    await page.fill('#military-months', '0');

    // Click calculate
    await page.click('.calculate-btn');

    // Wait for results
    await page.waitForTimeout(500);

    // Check eligibility status shows eligible
    const eligibilityStatus = page.locator('.eligibility-status');
    await expect(eligibilityStatus).toContainText('Eligible');

    // Check pension amount is displayed
    const annualPension = page.locator('#annual-pension');
    await expect(annualPension).toBeVisible();

    // Basic calculation: ~32 years * 100000 * 1.0% = ~$32,000
    const pensionText = await annualPension.textContent();
    expect(pensionText).toMatch(/\$3[0-5],\d{3}/); // Between $30k-$35k
  });

  test('should calculate with sick leave conversion', async ({ page }) => {
    await page.selectOption('#retirement-type', 'normal');
    await page.fill('#high3', '100000');
    await page.fill('#birthdate', '1960-01-01');
    await page.fill('#scd', '1990-01-01');
    await page.fill('#retirement-date', '2022-01-01');
    await page.fill('#sick-leave-hours', '2087'); // 1 year
    await page.fill('#military-years', '0');
    await page.fill('#military-months', '0');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Check that sick leave credit is shown
    const sickLeaveCredit = page.locator('#sick-leave-credit');
    await expect(sickLeaveCredit).toContainText('1 year');

    // Total service should include sick leave
    const totalService = page.locator('#total-service');
    await expect(totalService).toBeVisible();
  });

  test('should validate eligibility for VERA retirement', async ({ page }) => {
    await page.selectOption('#retirement-type', 'vera');
    await page.fill('#high3', '80000');
    await page.fill('#birthdate', '1975-01-01'); // Age 47
    await page.fill('#scd', '2005-01-01'); // 17 years
    await page.fill('#retirement-date', '2022-01-01');
    await page.fill('#sick-leave-hours', '0');
    await page.fill('#military-years', '0');
    await page.fill('#military-months', '0');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Should show not eligible (need 20 years or 25 years)
    const eligibilityStatus = page.locator('.eligibility-status');
    await expect(eligibilityStatus).toContainText('Not eligible');
  });

  test('should apply 1.1% multiplier for age 62+ with 20+ years', async ({ page }) => {
    await page.selectOption('#retirement-type', 'normal');
    await page.fill('#high3', '100000');
    await page.fill('#birthdate', '1960-01-01');
    await page.fill('#scd', '1982-01-01'); // 40 years
    await page.fill('#retirement-date', '2022-01-01'); // Age 62
    await page.fill('#sick-leave-hours', '0');
    await page.fill('#military-years', '0');
    await page.fill('#military-months', '0');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Check multiplier is shown
    const breakdown = page.locator('.calculation-breakdown');
    await expect(breakdown).toContainText('1.1%');

    // Pension should be higher with 1.1% multiplier
    const annualPension = page.locator('#annual-pension');
    const pensionText = await annualPension.textContent();
    expect(pensionText).toMatch(/\$4[0-9],\d{3}/); // Around $40k+ with 1.1%
  });

  test('should have mobile-optimized layout on small screens', async ({ page, isMobile }) => {
    if (!isMobile) {
      test.skip();
    }

    // Check sticky calculate button on mobile
    const calculateBtn = page.locator('.calculate-btn');
    await expect(calculateBtn).toBeVisible();

    // Check button is large enough for touch (min 48px)
    const btnBox = await calculateBtn.boundingBox();
    expect(btnBox?.height).toBeGreaterThanOrEqual(48);

    // Check inputs have adequate size
    const high3Input = page.locator('#high3');
    const inputBox = await high3Input.boundingBox();
    expect(inputBox?.height).toBeGreaterThanOrEqual(40);
  });

  test('should show calculation breakdown', async ({ page }) => {
    await page.selectOption('#retirement-type', 'normal');
    await page.fill('#high3', '100000');
    await page.fill('#birthdate', '1960-01-01');
    await page.fill('#scd', '1990-01-01');
    await page.fill('#retirement-date', '2022-01-01');
    await page.fill('#sick-leave-hours', '0');
    await page.fill('#military-years', '0');
    await page.fill('#military-months', '0');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Check breakdown details element
    const breakdown = page.locator('details.calculation-breakdown');
    await expect(breakdown).toBeVisible();

    // Expand breakdown
    await breakdown.click();

    // Check breakdown content
    await expect(breakdown.locator('summary')).toContainText('Show Calculation');
  });

  test('should have print functionality', async ({ page }) => {
    // Check print button exists
    const printBtn = page.locator('button:has-text("Print")');
    await expect(printBtn).toBeVisible();
  });

  test('should link to High-3 and Sick Leave calculators', async ({ page }) => {
    // Check links exist
    const high3Link = page.locator('a[href*="high-3-calculator"]');
    const sickLeaveLink = page.locator('a[href*="sick-leave"]');

    await expect(high3Link).toBeVisible();
    await expect(sickLeaveLink).toBeVisible();
  });
});
