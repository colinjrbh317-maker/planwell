import { test, expect } from '@playwright/test';

/**
 * Tests for site-wide updates:
 * 1. Fee-Based terminology (replacing Fee-Only)
 * 2. Learning Center navigation (replacing Blog)
 * 3. Services page card ordering (Federal Benefits Report first)
 * 4. Homepage hero with new image and fade effects
 */

test.describe('Homepage Updates', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('hero section displays correctly', async ({ page }) => {
    // Check hero section exists
    const hero = page.locator('.hero');
    await expect(hero).toBeVisible();

    // Check hero background image exists (may be positioned differently on mobile)
    const heroBackground = page.locator('.hero__background');
    await expect(heroBackground).toBeAttached();

    // Check hero content displays
    const heroContent = page.locator('.hero__content');
    await expect(heroContent).toBeVisible();

    // Check main title text
    await expect(page.locator('.hero__title-main')).toContainText('Retire with Confidence');
    await expect(page.locator('.hero__title-accent')).toContainText('Fed-Expert Financial Blueprint');
  });

  test('hero shows Fee-Based in trust badges', async ({ page }) => {
    const trustSection = page.locator('.hero__trust');
    await expect(trustSection).toBeVisible();

    // Should show Fee-Based, not Fee-Only
    await expect(trustSection).toContainText('Fee-Based');
    await expect(trustSection).not.toContainText('Fee-Only');
  });

  test('hero CTA button is visible', async ({ page }) => {
    const ctaButton = page.locator('.hero__cta a.btn--primary');
    await expect(ctaButton).toBeVisible();
    await expect(ctaButton).toContainText('Reserve My Free Federal Retirement Workshop Seat');
  });

  test('hero process link is visible', async ({ page }) => {
    const processLink = page.locator('.hero__process-link');
    await expect(processLink).toBeVisible();
    await expect(processLink).toContainText('How our 3-step process works');
  });
});

test.describe('Navigation Updates', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('navigation shows Learning Center instead of Blog', async ({ page }) => {
    const nav = page.locator('.nav__links');

    // Should show Learning Center
    await expect(nav).toContainText('Learning Center');

    // Should NOT show Blog as a nav item
    const navLinks = page.locator('.nav__link');
    const linkTexts = await navLinks.allTextContents();
    const hasBlogLink = linkTexts.some(text => text.trim() === 'Blog');
    expect(hasBlogLink).toBe(false);
  });

  test('Learning Center link navigates to /blog', async ({ page }) => {
    const learningCenterLink = page.locator('.nav__link', { hasText: 'Learning Center' });
    await expect(learningCenterLink).toHaveAttribute('href', '/blog');
  });
});

test.describe('Services Page Updates', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/services');
  });

  test('Federal Benefits Report is the first service card', async ({ page }) => {
    // Get all service cards
    const serviceCards = page.locator('.services-grid .service-card');

    // First card should be Federal Benefits Report
    const firstCard = serviceCards.first();
    await expect(firstCard).toContainText('Federal Benefits Report');

    // First card should have the featured styling
    await expect(firstCard).toHaveClass(/service-card--featured/);
  });

  test('Federal Benefits Report has No Cost badge', async ({ page }) => {
    const firstCard = page.locator('.services-grid .service-card').first();
    const badge = firstCard.locator('.service-card__badge');
    await expect(badge).toContainText('No Cost');
  });

  test('Federal Benefits Report shows "No cost report" price', async ({ page }) => {
    const firstCard = page.locator('.services-grid .service-card').first();
    const price = firstCard.locator('.service-card__price');
    await expect(price).toContainText('No cost report');
  });

  test('Comprehensive Planning is the second service card', async ({ page }) => {
    const serviceCards = page.locator('.services-grid .service-card');
    const secondCard = serviceCards.nth(1);
    await expect(secondCard).toContainText('Comprehensive Financial Planning');
  });

  test('fee section shows updated insurance language', async ({ page }) => {
    const feeSection = page.locator('.fee-section');
    await expect(feeSection).toContainText('Our revenue comes from the clients we service');
    await expect(feeSection).toContainText('we are in your corner');
    await expect(feeSection).toContainText('We disclose our fees upfront');
  });

  test('fee section does NOT show Fee-Only, Always', async ({ page }) => {
    const feeSection = page.locator('.fee-section');
    await expect(feeSection).not.toContainText('Fee-Only, Always');
  });

  test('only Fiduciary card is shown (not Fee-Only card)', async ({ page }) => {
    const feeCards = page.locator('.fee-card');

    // Should only have one fee card
    await expect(feeCards).toHaveCount(1);

    // It should be the Fiduciary card
    await expect(feeCards.first()).toContainText('What "Fiduciary" Means');
  });

  test('uses Fee-based terminology', async ({ page }) => {
    // Check the lead text uses fee-based
    const leadText = page.locator('.section-header .lead').first();
    await expect(leadText).toContainText('Fee-based');

    // Should not contain Fee-only
    await expect(page.locator('body')).not.toContainText('Fee-only');
    await expect(page.locator('body')).not.toContainText('Fee-Only');
  });
});

test.describe('Fee-Based Terminology Site-Wide', () => {
  test('homepage uses Fee-Based not Fee-Only', async ({ page }) => {
    await page.goto('/');
    const body = page.locator('body');
    await expect(body).toContainText('Fee-Based');
    await expect(body).not.toContainText('Fee-Only');
  });

  test('services page uses Fee-Based not Fee-Only', async ({ page }) => {
    await page.goto('/services');
    const body = page.locator('body');
    await expect(body).not.toContainText('Fee-Only');
  });

  test('comprehensive planning page uses Fee-Based', async ({ page }) => {
    await page.goto('/services/comprehensive-planning');
    const body = page.locator('body');
    await expect(body).toContainText('Fee-Based');
    await expect(body).not.toContainText('Fee-Only');
  });
});

test.describe('Visual Regression - Hero Section', () => {
  test('hero background covers right portion on desktop', async ({ page, browserName }, testInfo) => {
    // Skip this test on mobile/tablet projects - it's specifically for desktop viewport
    if (testInfo.project.name.includes('Mobile') || testInfo.project.name.includes('Tablet')) {
      test.skip();
      return;
    }

    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/');

    const heroBackground = page.locator('.hero__background');
    await expect(heroBackground).toBeVisible();

    // Take screenshot for visual verification
    await expect(page.locator('.hero')).toHaveScreenshot('hero-desktop.png', {
      maxDiffPixelRatio: 0.1,
    });
  });

  test('hero adapts on tablet', async ({ page }) => {
    await page.setViewportSize({ width: 1024, height: 768 });
    await page.goto('/');

    const hero = page.locator('.hero');
    await expect(hero).toBeVisible();
  });

  test('hero adapts on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/');

    const hero = page.locator('.hero');
    await expect(hero).toBeVisible();

    // Content should be full width on mobile
    const heroContent = page.locator('.hero__content');
    await expect(heroContent).toBeVisible();
  });
});
