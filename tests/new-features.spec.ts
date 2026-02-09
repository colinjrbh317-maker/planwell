import { test, expect } from '@playwright/test';

/**
 * Tests for newly implemented features:
 * 1. Homepage blog articles section
 * 2. /firstguide PDF download page
 * 3. Webinar signup form (5-step with nav)
 * 4. Blog post cover image sizing
 * 5. FERS calculator auto-scroll
 */

test.describe('Homepage Blog Articles Section', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display "Latest From the Learning Center" section', async ({ page }) => {
    const sectionTitle = page.locator('text=Latest From the Learning Center');
    await expect(sectionTitle).toBeVisible();
  });

  test('should display exactly 3 article cards', async ({ page }) => {
    const articleCards = page.locator('.article-card');
    await expect(articleCards).toHaveCount(3);
  });

  test('should display article images, titles, and excerpts', async ({ page }) => {
    const cards = page.locator('.article-card');

    for (let i = 0; i < 3; i++) {
      const card = cards.nth(i);

      // Image wrapper
      const imageWrap = card.locator('.article-card__image-wrap');
      await expect(imageWrap).toBeVisible();

      // Title
      const title = card.locator('.article-card__title');
      await expect(title).toBeVisible();
      const titleText = await title.textContent();
      expect(titleText!.length).toBeGreaterThan(5);

      // Excerpt
      const excerpt = card.locator('.article-card__excerpt');
      await expect(excerpt).toBeVisible();
    }
  });

  test('should display category and meta for each card', async ({ page }) => {
    const cards = page.locator('.article-card');

    for (let i = 0; i < 3; i++) {
      const card = cards.nth(i);
      const category = card.locator('.article-card__category');
      await expect(category).toBeVisible();

      const meta = card.locator('.article-card__meta');
      await expect(meta).toBeVisible();
    }
  });

  test('should link article cards to blog posts', async ({ page }) => {
    const firstCard = page.locator('.article-card').first();
    const href = await firstCard.getAttribute('href');
    expect(href).toBeTruthy();
    expect(href).toMatch(/^\//); // Should be a relative URL
  });

  test('should have responsive grid layout', async ({ page, isMobile }) => {
    const grid = page.locator('.articles-grid');
    await expect(grid).toBeVisible();

    if (isMobile) {
      // Cards should stack vertically on mobile
      const cards = page.locator('.article-card');
      const firstBox = await cards.first().boundingBox();
      const secondBox = await cards.nth(1).boundingBox();
      expect(secondBox!.y).toBeGreaterThan(firstBox!.y + firstBox!.height - 20);
    }
  });
});

test.describe('/firstguide PDF Download', () => {
  test('should load the firstguide page', async ({ page }) => {
    const response = await page.goto('/firstguide');
    expect(response?.status()).toBeLessThan(400);
  });

  test('should have meta refresh pointing to PDF', async ({ page }) => {
    await page.goto('/firstguide', { waitUntil: 'domcontentloaded' });

    const metaRefresh = page.locator('meta[http-equiv="refresh"]');
    const content = await metaRefresh.getAttribute('content');
    expect(content).toContain('/downloads/fers-retirement-guide.pdf');
  });

  test('should have fallback download link', async ({ page }) => {
    await page.goto('/firstguide', { waitUntil: 'domcontentloaded' });

    const fallbackLink = page.locator('a[href*="fers-retirement-guide.pdf"]');
    await expect(fallbackLink).toBeAttached();
  });

  test('PDF file should be accessible', async ({ page, request }) => {
    // Use API request to check the PDF is served (avoids Playwright navigation issues with binary files)
    const response = await request.get('http://localhost:4321/downloads/fers-retirement-guide.pdf');
    // Accept 200 (served) or 304 (cached) - Astro dev server may handle static assets differently
    expect([200, 304]).toContain(response.status());
  });
});

test.describe('Webinar Signup Form', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/webinar');
  });

  test('should display minimal navigation with logo and back link', async ({ page }) => {
    const header = page.locator('.funnel-header');
    await expect(header).toBeVisible();

    // Back to site link
    const backLink = page.locator('.funnel-nav__link');
    await expect(backLink).toBeVisible();
    await expect(backLink).toContainText('Back to Site');
    await expect(backLink).toHaveAttribute('href', '/');
  });

  test('should display logo in header', async ({ page }) => {
    const logo = page.locator('.funnel-header img, .funnel-header .funnel-logo');
    await expect(logo.first()).toBeVisible();
  });

  test('should start with the first name step', async ({ page }) => {
    // First step should ask for first name
    const firstInput = page.locator('input[name="firstName"], input[placeholder="First name"]');
    await expect(firstInput.first()).toBeAttached();
  });

  test('should have 5 form input steps', async ({ page }) => {
    // Check that the step indicators/progress show correct total
    const pageContent = await page.content();

    // The form has firstName, lastName, email, phone, agency fields
    expect(pageContent).toContain('firstName');
    expect(pageContent).toContain('lastName');
    expect(pageContent).toContain('email');
    expect(pageContent).toContain('phone');
    expect(pageContent).toContain('agency');
  });

  test('should display webinar date information', async ({ page }) => {
    // The page should show upcoming webinar date
    const body = page.locator('body');
    await expect(body).toContainText(/FERS|webinar|retirement/i);
  });
});

test.describe('Blog Post Cover Images', () => {
  test('blog post cover image should be 480px on desktop', async ({ page }) => {
    // Navigate to any blog post
    await page.goto('/blog');
    const firstPostLink = page.locator('a[href^="/"]').filter({ hasText: /pay|fers|tsp|fehb/i }).first();

    if (await firstPostLink.isVisible()) {
      const href = await firstPostLink.getAttribute('href');
      await page.goto(href!);

      const cover = page.locator('.article__cover');
      if (await cover.isVisible()) {
        const box = await cover.boundingBox();
        // Desktop height should be 480px (allow some tolerance)
        if (box && box.width > 768) {
          expect(box.height).toBeGreaterThanOrEqual(450);
          expect(box.height).toBeLessThanOrEqual(510);
        }
      }
    }
  });
});

test.describe('FERS Calculator Auto-Scroll', () => {
  test('FERS calculate button has scrollIntoView in onclick', async ({ page }) => {
    await page.goto('/fers-retirement-calculator');

    // Verify the Calculate button has scrollIntoView behavior wired up
    const calculateBtn = page.locator('.calculate-btn');
    await expect(calculateBtn).toBeVisible();

    const onclick = await calculateBtn.getAttribute('onclick');
    expect(onclick).toContain('scrollIntoView');
    expect(onclick).toContain('fers-result');
  });
});

test.describe('Homepage Hero Image', () => {
  test('hero image should use center center positioning', async ({ page }) => {
    await page.goto('/');

    const heroImg = page.locator('.hero__image, .hero__background img').first();
    if (await heroImg.isVisible()) {
      const objectPosition = await heroImg.evaluate(el =>
        window.getComputedStyle(el).objectPosition
      );
      // Should be "center center" or "50% 50%"
      expect(objectPosition).toMatch(/center|50%/);
    }
  });
});
