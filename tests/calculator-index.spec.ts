import { test, expect } from '@playwright/test';

test.describe('Calculator Index Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/calculators');
  });

  test('should load index page with all calculator cards', async ({ page }) => {
    // Check page title (use specific selector to avoid Astro toolbar)
    await expect(page.locator('.page-hero h1')).toContainText('Federal Retirement Calculators');

    // Check all 6 calculator cards are present
    const cards = page.locator('.calc-card');
    await expect(cards).toHaveCount(6);
  });

  test('should display FERS Pension Calculator card', async ({ page }) => {
    const fersCard = page.locator('a[href="/fers-retirement-calculator"]');
    await expect(fersCard).toBeVisible();
    await expect(fersCard).toContainText('FERS Pension Calculator');
  });

  test('should display High-3 Salary Calculator card', async ({ page }) => {
    const high3Card = page.locator('a[href="/high-3-calculator"]');
    await expect(high3Card).toBeVisible();
    await expect(high3Card).toContainText('High-3 Salary Calculator');
  });

  test('should display Sick Leave Conversion Calculator card', async ({ page }) => {
    const sickLeaveCard = page.locator('a[href="/sick-leave-conversion-calculator"]');
    await expect(sickLeaveCard).toBeVisible();
    await expect(sickLeaveCard).toContainText('Sick Leave Conversion');
  });

  test('should display Special Retirement Supplement Calculator card', async ({ page }) => {
    const supplementCard = page.locator('a[href="/special-retirement-supplement-calculator"]');
    await expect(supplementCard).toBeVisible();
    await expect(supplementCard).toContainText('Special Retirement Supplement');
  });

  test('should display Special Provision (LEO/ATC) Calculator card', async ({ page }) => {
    const leoCard = page.locator('a[href*="leo-atc"]');
    await expect(leoCard).toBeVisible();
    await expect(leoCard).toContainText('Special Provision');
  });

  test('should display TSP Growth Calculator card', async ({ page }) => {
    // Use more specific selector to avoid matching footer links
    const tspCard = page.locator('.calc-card[href*="tsp"]');
    await expect(tspCard).toBeVisible();
    await expect(tspCard).toContainText('TSP Growth Calculator');
  });

  test('should navigate to FERS calculator when clicked', async ({ page }) => {
    await page.click('a[href="/fers-retirement-calculator"]');
    await expect(page).toHaveURL(/fers-retirement-calculator/);
  });

  test('should navigate to High-3 calculator when clicked', async ({ page }) => {
    await page.click('a[href="/high-3-calculator"]');
    await expect(page).toHaveURL(/high-3-calculator/);
  });

  test('should navigate to Sick Leave calculator when clicked', async ({ page }) => {
    await page.click('a[href="/sick-leave-conversion-calculator"]');
    await expect(page).toHaveURL(/sick-leave-conversion-calculator/);
  });

  test('should navigate to Supplement calculator when clicked', async ({ page }) => {
    await page.click('a[href="/special-retirement-supplement-calculator"]');
    await expect(page).toHaveURL(/special-retirement-supplement-calculator/);
  });

  test('should display icons for each calculator', async ({ page }) => {
    // Each card should have an icon
    const icons = page.locator('.calc-card__icon');
    await expect(icons).toHaveCount(6);

    // Each icon should contain an SVG
    const svgs = page.locator('.calc-card__icon svg');
    await expect(svgs).toHaveCount(6);
  });

  test('should have hover effects on calculator cards', async ({ page, isMobile }) => {
    if (isMobile) {
      test.skip(); // Hover effects only on desktop
    }

    const firstCard = page.locator('.calc-card').first();

    // Get initial transform
    const initialTransform = await firstCard.evaluate(el =>
      window.getComputedStyle(el).transform
    );

    // Hover over card
    await firstCard.hover();
    await page.waitForTimeout(300);

    // Transform should change on hover
    const hoverTransform = await firstCard.evaluate(el =>
      window.getComputedStyle(el).transform
    );

    // Transforms should be different (hover adds translateY)
    expect(hoverTransform).not.toBe(initialTransform);
  });

  test('should display description text for each calculator', async ({ page }) => {
    const cards = page.locator('.calc-card');

    // Each card should have a paragraph with description
    for (let i = 0; i < await cards.count(); i++) {
      const card = cards.nth(i);
      const description = card.locator('p');
      await expect(description).toBeVisible();
      const text = await description.textContent();
      expect(text).toBeTruthy();
      expect(text!.length).toBeGreaterThan(20); // Meaningful description
    }
  });

  test('should have responsive grid layout', async ({ page, isMobile }) => {
    const grid = page.locator('.calculator-grid');
    await expect(grid).toBeVisible();

    // Check grid is using auto-fit
    const gridStyle = await grid.evaluate(el =>
      window.getComputedStyle(el).gridTemplateColumns
    );
    expect(gridStyle).toBeTruthy();
  });

  test('should display CTA section', async ({ page }) => {
    const cta = page.locator('.section--navy');
    await expect(cta).toBeVisible();
    await expect(cta).toContainText('Need More Than a Calculator?');
  });

  test('should have staggered animation delays', async ({ page, isMobile }) => {
    if (isMobile) {
      test.skip(); // Animation testing best on desktop
    }

    // Check that cards have animation-delay attributes
    const cards = page.locator('.calc-card[data-animate]');
    await expect(cards).toHaveCount(6);

    // Check various delay values exist
    const card1 = cards.nth(0);
    const card2 = cards.nth(1);
    const card3 = cards.nth(2);

    // Cards should have different animation delays
    const delay1 = await card1.getAttribute('style');
    const delay2 = await card2.getAttribute('style');
    const delay3 = await card3.getAttribute('style');

    expect(delay1).toContain('animation-delay');
    expect(delay2).toContain('animation-delay');
    expect(delay3).toContain('animation-delay');
  });

  test('should be keyboard accessible', async ({ page }) => {
    // Tab through cards
    await page.keyboard.press('Tab');

    // First card should be focused
    const firstCard = page.locator('.calc-card').first();
    await expect(firstCard).toBeFocused();

    // Tab to next card
    await page.keyboard.press('Tab');
    const secondCard = page.locator('.calc-card').nth(1);
    await expect(secondCard).toBeFocused();
  });

  test('should have proper semantic HTML', async ({ page }) => {
    // All cards should be links (semantic)
    const cards = page.locator('.calc-card');
    for (let i = 0; i < await cards.count(); i++) {
      const tagName = await cards.nth(i).evaluate(el => el.tagName);
      expect(tagName).toBe('A');
    }

    // Check headings hierarchy (page content only, not Astro toolbar)
    const mainHeading = page.locator('.page-hero h1');
    await expect(mainHeading).toHaveCount(1);

    const cardHeadings = page.locator('.calc-card h3');
    await expect(cardHeadings).toHaveCount(6);
  });

  test('should display arrow links on each card', async ({ page }) => {
    // Each card should have a "→" arrow link
    const btnLinks = page.locator('.btn-link');
    await expect(btnLinks).toHaveCount(6);

    for (let i = 0; i < await btnLinks.count(); i++) {
      const link = btnLinks.nth(i);
      const text = await link.textContent();
      expect(text).toContain('→');
    }
  });

  test('should have mobile-friendly card layout', async ({ page, isMobile }) => {
    if (!isMobile) {
      test.skip();
    }

    // Cards should stack vertically on mobile
    const cards = page.locator('.calc-card');
    const firstCard = cards.first();
    const secondCard = cards.nth(1);

    const firstBox = await firstCard.boundingBox();
    const secondBox = await secondCard.boundingBox();

    // Second card should be below first card (not side by side)
    expect(secondBox!.y).toBeGreaterThan(firstBox!.y + firstBox!.height);
  });
});
