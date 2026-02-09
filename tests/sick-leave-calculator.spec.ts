import { test, expect } from '@playwright/test';

test.describe('Sick Leave Conversion Calculator', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/sick-leave-conversion-calculator');
  });

  test('should load calculator with sick leave hours input', async ({ page }) => {
    // Check page title (use specific selector)
    await expect(page.locator('.page-hero h1')).toContainText('Sick Leave Conversion Calculator');

    // Check input field
    await expect(page.locator('#sickleave-hours')).toBeVisible();

    // Check default value (2087)
    const defaultValue = await page.locator('#sickleave-hours').inputValue();
    expect(defaultValue).toBe('2087');

    // Check calculate button
    await expect(page.locator('.calculate-btn')).toBeVisible();
  });

  test('should convert 2087 hours to 1 year', async ({ page }) => {
    await page.fill('#sickleave-hours', '2087');

    // Real-time conversion should happen automatically
    await page.waitForTimeout(500);

    // Check result
    const serviceCredit = page.locator('#service-credit');
    await expect(serviceCredit).toContainText('1 year');

    // Check total months
    const totalMonths = page.locator('#total-months');
    await expect(totalMonths).toContainText('12 months');
  });

  test('should convert 174 hours to 1 month', async ({ page }) => {
    await page.fill('#sickleave-hours', '174');
    await page.waitForTimeout(500);

    const serviceCredit = page.locator('#service-credit');
    await expect(serviceCredit).toContainText('1 month');
  });

  test('should show months and days without rounding (441 hours)', async ({ page }) => {
    // 441 hours = 2 months, 16 days (no rounding up to 3 months)
    await page.fill('#sickleave-hours', '441');
    await page.waitForTimeout(500);

    const serviceCredit = page.locator('#service-credit');
    await expect(serviceCredit).toContainText('2 months');
    await expect(serviceCredit).toContainText('16 days');
  });

  test('should show months and days for 400 hours', async ({ page }) => {
    // 400 hours = 2 months, 9 days
    await page.fill('#sickleave-hours', '400');
    await page.waitForTimeout(500);

    const serviceCredit = page.locator('#service-credit');
    await expect(serviceCredit).toContainText('2 months');
    await expect(serviceCredit).toContainText('9 days');
  });

  test('should handle amounts over 2087 hours (multiple years)', async ({ page }) => {
    // 4174 hours = 2 years
    await page.fill('#sickleave-hours', '4174');
    await page.waitForTimeout(500);

    const serviceCredit = page.locator('#service-credit');
    await expect(serviceCredit).toContainText('2 year');

    const totalMonths = page.locator('#total-months');
    await expect(totalMonths).toContainText('24 months');
  });

  test('should handle 0 hours', async ({ page }) => {
    await page.fill('#sickleave-hours', '0');
    await page.waitForTimeout(500);

    const serviceCredit = page.locator('#service-credit');
    await expect(serviceCredit).toContainText('0 months');
  });

  test('should handle decimal hours', async ({ page }) => {
    await page.fill('#sickleave-hours', '2087.5');
    await page.waitForTimeout(500);

    // Should still calculate correctly
    const serviceCredit = page.locator('#service-credit');
    await expect(serviceCredit).toBeVisible();
  });

  test('should update in real-time on input change', async ({ page }) => {
    // Type in input
    await page.fill('#sickleave-hours', '500');

    // Wait briefly (real-time update should be instant)
    await page.waitForTimeout(300);

    // Result should update without clicking calculate
    const serviceCredit = page.locator('#service-credit');
    await expect(serviceCredit).not.toContainText('1 year, 0 months');
  });

  test('should show educational information about conversion', async ({ page }) => {
    // Check that educational content is present
    const content = page.locator('.calculator__note');
    await expect(content).toBeVisible();
    await expect(content).toContainText('2,087 hours');
    await expect(content).toContainText('work year');
  });

  test('should have link to FERS calculator', async ({ page }) => {
    // Use specific selector in calculator note section
    const fersLink = page.locator('.calculator__note a[href*="fers"]').first();
    await expect(fersLink).toBeVisible();
  });

  test('should have mobile-optimized input', async ({ page, isMobile }) => {
    if (!isMobile) {
      test.skip();
    }

    // Check input uses numeric keyboard (inputmode="numeric")
    const input = page.locator('#sickleave-hours');
    const inputMode = await input.getAttribute('inputmode');
    expect(inputMode).toBe('numeric');

    // Check button size
    const calculateBtn = page.locator('.calculate-btn');
    const btnBox = await calculateBtn.boundingBox();
    expect(btnBox?.height).toBeGreaterThanOrEqual(48);
  });

  test('should handle negative numbers gracefully', async ({ page }) => {
    // Dismiss the alert that fires for negative numbers
    page.on('dialog', dialog => dialog.dismiss());

    await page.fill('#sickleave-hours', '-100');
    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Result should still show previous valid value or default (not crash)
    const serviceCredit = page.locator('#service-credit');
    await expect(serviceCredit).toBeVisible();
  });

  test('should display calculation example in educational section', async ({ page }) => {
    // Check that example is shown (441 hours → 2 months and 16 days)
    const content = page.locator('.calculator__note');
    await expect(content).toContainText('441');
    await expect(content).toContainText('2 months and 16 days');
  });

  test('should have print functionality', async ({ page }) => {
    const printBtn = page.locator('button:has-text("Print")');
    await expect(printBtn).toBeVisible();
  });

  test('should show result summary with converted time', async ({ page }) => {
    await page.fill('#sickleave-hours', '2087');
    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // 2087 hours = 1 year; result-note shows the formatted conversion
    const resultNote = page.locator('#result-note');
    await expect(resultNote).toContainText('1 year');
    await expect(resultNote).toContainText('additional service credit');
  });

  test('should format results correctly', async ({ page }) => {
    // Test singular vs plural
    await page.fill('#sickleave-hours', '174'); // 1 month
    await page.waitForTimeout(500);
    let serviceCredit = page.locator('#service-credit');
    await expect(serviceCredit).toContainText('1 month'); // Not "months"

    // Test years and months
    await page.fill('#sickleave-hours', '2261'); // 1 year 1 month
    await page.waitForTimeout(500);
    await expect(serviceCredit).toContainText('1 year');
    await expect(serviceCredit).toContainText('1 month');
  });

  test('should show conversion note with service credit details', async ({ page }) => {
    await page.fill('#sickleave-hours', '500');
    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    const resultNote = page.locator('#result-note');
    await expect(resultNote).toContainText('500');
    await expect(resultNote).toContainText('additional service credit');
  });

  test('should auto-scroll to results when Calculate is clicked', async ({ page }) => {
    await page.fill('#sickleave-hours', '500');

    // Click calculate button (which triggers scroll)
    await page.click('.calculate-btn');
    await page.waitForTimeout(1000);

    // Result section should be visible in viewport
    const resultSection = page.locator('#sickleave-result');
    await expect(resultSection).toBeInViewport();
  });
});
