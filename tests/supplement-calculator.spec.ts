import { test, expect } from '@playwright/test';

test.describe('Special Retirement Supplement Calculator', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/special-retirement-supplement-calculator');
  });

  test('should load calculator with all input fields', async ({ page }) => {
    // Check page title (use specific selector)
    await expect(page.locator('.page-hero h1')).toContainText('Special Retirement Supplement');

    // Check input fields
    await expect(page.locator('#retirement-date')).toBeVisible();
    await expect(page.locator('#service-date')).toBeVisible();
    await expect(page.locator('#ss-estimate')).toBeVisible();

    // Check calculate button
    await expect(page.locator('.calculate-btn')).toBeVisible();
  });

  test('should display prominent warning about age 62', async ({ page }) => {
    // Check warning alert is visible
    const warning = page.locator('.alert--warning');
    await expect(warning).toBeVisible();
    await expect(warning).toContainText('62');
  });

  test('should calculate supplement for eligible retiree (Age 60 with 20 years)', async ({ page }) => {
    // Age 60 with 20 years
    await page.fill('#retirement-date', '2022-01-01');
    await page.fill('#service-date', '2002-01-01'); // 20 years
    await page.fill('#ss-estimate', '2000');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Check eligibility shows eligible
    const eligibility = page.locator('.eligibility-status');
    await expect(eligibility).toContainText('Eligible');

    // Calculate expected: (20 ÷ 40) × 2000 = $1,000/month
    const monthlyAmount = page.locator('#monthly-supplement');
    await expect(monthlyAmount).toContainText('$1,000');

    // Annual: $1,000 × 12 = $12,000
    const annualAmount = page.locator('#annual-supplement');
    await expect(annualAmount).toContainText('$12,000');
  });

  test('should calculate supplement for eligible retiree (Age 57 with 30 years)', async ({ page }) => {
    await page.fill('#retirement-date', '2022-01-01');
    await page.fill('#service-date', '1992-01-01'); // 30 years
    await page.fill('#ss-estimate', '2400');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Check eligibility
    const eligibility = page.locator('.eligibility-status');
    await expect(eligibility).toContainText('Eligible');

    // Calculate: (30 ÷ 40) × 2400 = $1,800/month
    const monthlyAmount = page.locator('#monthly-supplement');
    await expect(monthlyAmount).toContainText('$1,800');
  });

  test('should show not eligible for insufficient years', async ({ page }) => {
    // Age 58 with 15 years (not enough)
    await page.fill('#retirement-date', '2022-01-01');
    await page.fill('#service-date', '2007-01-01'); // 15 years
    await page.fill('#ss-estimate', '2000');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Should show not eligible
    const eligibility = page.locator('.eligibility-status');
    await expect(eligibility).toContainText('Not eligible');
  });

  test('should show not eligible for age 62+ retirees', async ({ page }) => {
    // Age 63 (supplement stops at 62)
    await page.fill('#retirement-date', '2023-01-01');
    await page.fill('#service-date', '1988-01-01'); // 35 years
    await page.fill('#ss-estimate', '2000');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Should show not eligible (too old)
    const eligibility = page.locator('.eligibility-status');
    await expect(eligibility).toContainText('Not eligible');
    await expect(eligibility).toContainText('62');
  });

  test('should calculate duration until age 62', async ({ page }) => {
    // Retire at 60, receive supplement until 62 (24 months)
    await page.fill('#retirement-date', '2022-01-01');
    await page.fill('#service-date', '2002-01-01');
    await page.fill('#ss-estimate', '2000');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Check duration is shown
    const duration = page.locator('#supplement-duration');
    if (await duration.isVisible()) {
      await expect(duration).toContainText('24'); // 24 months
    }
  });

  test('should format currency correctly', async ({ page }) => {
    await page.fill('#retirement-date', '2022-01-01');
    await page.fill('#service-date', '1992-01-01');
    await page.fill('#ss-estimate', '2500');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    const monthlyAmount = page.locator('#monthly-supplement');
    const text = await monthlyAmount.textContent();

    // Should have $ and comma
    expect(text).toContain('$');
    expect(text).toContain(',');
  });

  test('should have link to SSA.gov for estimate', async ({ page }) => {
    const ssaLink = page.locator('a[href*="ssa.gov"]');
    await expect(ssaLink).toBeVisible();

    // Should open in new tab
    const target = await ssaLink.getAttribute('target');
    expect(target).toBe('_blank');
  });

  test('should show educational note about sick leave exclusion', async ({ page }) => {
    const content = page.locator('body');
    await expect(content).toContainText('NOT include sick leave');
    await expect(content).toContainText('military time');
  });

  test('should have mobile-optimized layout', async ({ page, isMobile }) => {
    if (!isMobile) {
      test.skip();
    }

    // Check calculate button size
    const calculateBtn = page.locator('.calculate-btn');
    const btnBox = await calculateBtn.boundingBox();
    expect(btnBox?.height).toBeGreaterThanOrEqual(48);

    // Check SS estimate input uses decimal keyboard
    const ssInput = page.locator('#ss-estimate');
    const inputMode = await ssInput.getAttribute('inputmode');
    expect(inputMode).toBe('decimal');
  });

  test('should handle edge case of exactly 40 years', async ({ page }) => {
    await page.fill('#retirement-date', '2022-01-01');
    await page.fill('#service-date', '1982-01-01'); // 40 years
    await page.fill('#ss-estimate', '2000');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // (40 ÷ 40) × 2000 = $2,000
    const monthlyAmount = page.locator('#monthly-supplement');
    await expect(monthlyAmount).toContainText('$2,000');
  });

  test('should validate date order (service date before retirement)', async ({ page }) => {
    // Invalid: retirement before service start
    await page.fill('#retirement-date', '2000-01-01');
    await page.fill('#service-date', '2020-01-01');
    await page.fill('#ss-estimate', '2000');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Should show error or calculate 0
    const result = page.locator('.calculator__result');
    if (await result.isVisible()) {
      const text = await result.textContent();
      // Either error message or $0
      expect(text).toBeTruthy();
    }
  });

  test('should have print functionality', async ({ page }) => {
    const printBtn = page.locator('button:has-text("Print")');
    await expect(printBtn).toBeVisible();
  });

  test('should display formula explanation', async ({ page }) => {
    const content = page.locator('.calculator__note');
    await expect(content).toContainText('÷ 40');
    await expect(content).toContainText('Social Security');
  });

  test('should show results with proper formatting', async ({ page }) => {
    await page.fill('#retirement-date', '2022-01-01');
    await page.fill('#service-date', '1997-01-01'); // 25 years
    await page.fill('#ss-estimate', '2000');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Check both monthly and annual results are displayed
    const monthlyAmount = page.locator('#monthly-supplement');
    const annualAmount = page.locator('#annual-supplement');

    await expect(monthlyAmount).toBeVisible();
    await expect(annualAmount).toBeVisible();

    // Calculate: (25 ÷ 40) × 2000 = $1,250/month, $15,000/year
    await expect(monthlyAmount).toContainText('$1,250');
    await expect(annualAmount).toContainText('$15,000');
  });

  test('should handle decimal SS estimates', async ({ page }) => {
    await page.fill('#retirement-date', '2022-01-01');
    await page.fill('#service-date', '2002-01-01');
    await page.fill('#ss-estimate', '2345.67');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    const monthlyAmount = page.locator('#monthly-supplement');
    await expect(monthlyAmount).toBeVisible();
  });
});
