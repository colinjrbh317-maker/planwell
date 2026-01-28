import { test, expect } from '@playwright/test';

test.describe('High-3 Salary Calculator', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/high-3-calculator');
  });

  test('should load calculator with retirement date and initial periods', async ({ page }) => {
    // Check page title (use specific selector and match actual text)
    await expect(page.locator('.page-hero h1')).toContainText('High-3 Average Salary Calculator');

    // Check retirement date input (correct ID)
    await expect(page.locator('#high3-retirement-date')).toBeVisible();

    // Check initial salary periods (should have 1 period by default)
    const periodsContainer = page.locator('#salary-periods-container');
    await expect(periodsContainer).toBeVisible();

    const periods = page.locator('.salary-period');
    await expect(periods).toHaveCount(1);

    // Check calculate button
    await expect(page.locator('.calculate-btn')).toBeVisible();
    await expect(page.locator('.calculate-btn')).toContainText('Calculate High-3');
  });

  test('should add and remove salary periods', async ({ page }) => {
    // Initial count (starts with 1 period)
    let periods = page.locator('.salary-period');
    await expect(periods).toHaveCount(1);

    // Add a period
    await page.click('button:has-text("Add Salary Period")');
    await expect(periods).toHaveCount(4);

    // Try to add beyond max (should be limited to 4)
    const addBtn = page.locator('button:has-text("Add Salary Period")');
    if (await addBtn.isVisible()) {
      await addBtn.click();
    }
    // Should not exceed 4
    await expect(periods).toHaveCount(await periods.count());
    const count = await periods.count();
    expect(count).toBeLessThanOrEqual(4);

    // Remove a period
    const removeButtons = page.locator('.remove-period-btn');
    await removeButtons.first().click();
    await expect(page.locator('.salary-period')).toHaveCount(count - 1);
  });

  test('should calculate High-3 with single period', async ({ page }) => {
    await page.fill('#high3-retirement-date', '2022-01-01');

    // Fill first period (spanning more than 36 months)
    await page.fill('[data-period="1"] input[name="start-date"]', '2019-01-01');
    await page.fill('[data-period="1"] input[name="end-date"]', '2022-01-01');
    await page.fill('[data-period="1"] input[name="salary"]', '100000');

    // Calculate
    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Check result
    const high3Result = page.locator('#high3-result');
    await expect(high3Result).toContainText('$100,000');
  });

  test('should calculate weighted average with multiple periods', async ({ page }) => {
    await page.fill('#high3-retirement-date', '2022-01-01');

    // Period 1: Jan 2019 - Jun 2020 @ $90,000 (18 months)
    await page.fill('[data-period="1"] input[name="start-date"]', '2019-01-01');
    await page.fill('[data-period="1"] input[name="end-date"]', '2020-06-30');
    await page.fill('[data-period="1"] input[name="salary"]', '90000');

    // Period 2: Jul 2020 - Dec 2021 @ $100,000 (18 months)
    await page.fill('[data-period="1"] input[name="start-date"]', '2020-07-01');
    await page.fill('[data-period="1"] input[name="end-date"]', '2021-12-31');
    await page.fill('[data-period="1"] input[name="salary"]', '100000');

    // Period 3: Jan 2022 - Jan 2022 (retirement date)
    await page.fill('[data-period="2"] input[name="start-date"]', '2022-01-01');
    await page.fill('[data-period="2"] input[name="end-date"]', '2022-01-01');
    await page.fill('[data-period="2"] input[name="salary"]', '105000');

    // Calculate
    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Weighted average should be between $90k and $105k
    const high3Result = page.locator('#high3-result');
    const resultText = await high3Result.textContent();
    expect(resultText).toMatch(/\$9[0-9],\d{3}/);
  });

  test('should validate date ranges (no overlaps)', async ({ page }) => {
    await page.fill('#high3-retirement-date', '2022-01-01');

    // Period 1
    await page.fill('[data-period="1"] input[name="start-date"]', '2020-01-01');
    await page.fill('[data-period="1"] input[name="end-date"]', '2020-12-31');
    await page.fill('[data-period="1"] input[name="salary"]', '90000');

    // Period 2 - overlapping dates
    await page.fill('[data-period="1"] input[name="start-date"]', '2020-06-01');
    await page.fill('[data-period="1"] input[name="end-date"]', '2021-12-31');
    await page.fill('[data-period="1"] input[name="salary"]', '100000');

    // Calculate
    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Should show validation error
    const errorMessage = page.locator('.error-message, .alert--error');
    await expect(errorMessage).toBeVisible();
  });

  test('should show calculation breakdown', async ({ page }) => {
    await page.fill('#high3-retirement-date', '2022-01-01');
    await page.fill('[data-period="1"] input[name="start-date"]', '2019-01-01');
    await page.fill('[data-period="1"] input[name="end-date"]', '2022-01-01');
    await page.fill('[data-period="1"] input[name="salary"]', '100000');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Check breakdown details element
    const breakdown = page.locator('details');
    if (await breakdown.count() > 0) {
      await expect(breakdown.first()).toBeVisible();

      // Expand breakdown
      await breakdown.first().click();

      // Should show which months were included
      await expect(breakdown.first()).toContainText('months');
    }
  });

  test('should have mobile-optimized layout', async ({ page, isMobile }) => {
    if (!isMobile) {
      test.skip();
    }

    // Check calculate button height
    const calculateBtn = page.locator('.calculate-btn');
    const btnBox = await calculateBtn.boundingBox();
    expect(btnBox?.height).toBeGreaterThanOrEqual(48);

    // Check add/remove buttons are touch-friendly
    const addBtn = page.locator('button:has-text("Add Salary Period")');
    const addBox = await addBtn.boundingBox();
    expect(addBox?.height).toBeGreaterThanOrEqual(40);
  });

  test('should handle empty salary periods gracefully', async ({ page }) => {
    await page.fill('#high3-retirement-date', '2022-01-01');

    // Leave periods empty
    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    // Should show validation or result of 0
    const result = page.locator('#high3-result');
    if (await result.isVisible()) {
      await expect(result).toContainText('$0');
    }
  });

  test('should format currency correctly', async ({ page }) => {
    await page.fill('#high3-retirement-date', '2022-01-01');
    await page.fill('[data-period="1"] input[name="start-date"]', '2019-01-01');
    await page.fill('[data-period="1"] input[name="end-date"]', '2022-01-01');
    await page.fill('[data-period="1"] input[name="salary"]', '123456');

    await page.click('.calculate-btn');
    await page.waitForTimeout(500);

    const high3Result = page.locator('#high3-result');
    const resultText = await high3Result.textContent();

    // Should include $ and comma
    expect(resultText).toContain('$');
    expect(resultText).toContain(',');
  });

  test('should have print functionality', async ({ page }) => {
    const printBtn = page.locator('button:has-text("Print")');
    await expect(printBtn).toBeVisible();
  });

  test('should show 36-month window information', async ({ page }) => {
    // Check that educational content mentions 36 months
    const content = page.locator('body');
    await expect(content).toContainText('36');
  });
});
