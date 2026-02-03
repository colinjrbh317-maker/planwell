import { test, expect } from '@playwright/test';

test.describe('About Dropdown Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display About dropdown button with chevron icon', async ({ page, isMobile }) => {
    // On mobile, open the hamburger menu first
    if (isMobile) {
      await page.click('.nav__toggle');
      await expect(page.locator('.nav__menu')).toHaveClass(/is-open/);
    }

    const aboutButton = page.locator('.nav__link--dropdown');
    await expect(aboutButton).toBeVisible();
    await expect(aboutButton).toContainText('About');

    // Check chevron icon exists
    const chevron = aboutButton.locator('.nav__dropdown-icon');
    await expect(chevron).toBeVisible();
  });

  test('should show dropdown on hover (desktop)', async ({ page, isMobile }) => {
    if (isMobile) {
      test.skip();
    }

    const dropdownItem = page.locator('.nav__item--has-dropdown');
    const dropdown = page.locator('.nav__dropdown');

    // Initially hidden
    await expect(dropdown).not.toBeVisible();

    // Hover to reveal
    await dropdownItem.hover();
    await expect(dropdown).toBeVisible();

    // Check all three links
    await expect(dropdown.locator('a')).toHaveCount(3);
    await expect(dropdown).toContainText('About PlanWell');
    await expect(dropdown).toContainText('Our Credentials');
    await expect(dropdown).toContainText('Financial Blueprint');
  });

  test('should navigate to About PlanWell from dropdown', async ({ page, isMobile }) => {
    if (isMobile) {
      // Mobile: open menu first
      await page.click('.nav__toggle');
      await page.click('.nav__link--dropdown');
    } else {
      await page.locator('.nav__item--has-dropdown').hover();
    }

    await page.click('a[href="/about"]');
    await expect(page).toHaveURL(/\/about$/);
  });

  test('should navigate to Our Credentials from dropdown', async ({ page, isMobile }) => {
    if (isMobile) {
      await page.click('.nav__toggle');
      await page.click('.nav__link--dropdown');
    } else {
      await page.locator('.nav__item--has-dropdown').hover();
    }

    await page.click('a[href="/about/our-credentials"]');
    await expect(page).toHaveURL(/\/about\/our-credentials/);
  });

  test('should navigate to Financial Blueprint from dropdown', async ({ page, isMobile }) => {
    if (isMobile) {
      await page.click('.nav__toggle');
      await page.click('.nav__link--dropdown');
    } else {
      await page.locator('.nav__item--has-dropdown').hover();
    }

    await page.click('a[href="/about/financial-blueprint"]');
    await expect(page).toHaveURL(/\/about\/financial-blueprint/);
  });

  test('should toggle dropdown on mobile with click', async ({ page, isMobile }) => {
    if (!isMobile) {
      test.skip();
    }

    // Open mobile menu
    await page.click('.nav__toggle');
    await expect(page.locator('.nav__menu')).toHaveClass(/is-open/);

    // Click dropdown button
    const dropdownItem = page.locator('.nav__item--has-dropdown');
    const dropdownButton = page.locator('.nav__link--dropdown');
    await dropdownButton.click();

    // Dropdown should be visible
    await expect(dropdownItem).toHaveClass(/is-open/);
  });

  test('should rotate chevron when dropdown is open', async ({ page, isMobile }) => {
    if (isMobile) {
      test.skip();
    }

    const dropdownItem = page.locator('.nav__item--has-dropdown');
    const chevron = page.locator('.nav__dropdown-icon');

    // Hover to open
    await dropdownItem.hover();
    await page.waitForTimeout(300);

    // Check rotation transform is applied
    const transform = await chevron.evaluate(el =>
      window.getComputedStyle(el).transform
    );
    expect(transform).not.toBe('none');
  });
});

test.describe('Our Credentials Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/about/our-credentials');
  });

  test('should load page with correct title', async ({ page }) => {
    await expect(page).toHaveTitle(/Our Credentials|The PlanWell Difference/);
  });

  test('should display hero section', async ({ page }) => {
    const hero = page.locator('.page-hero');
    await expect(hero).toBeVisible();
    await expect(hero).toContainText('Expert Credentials That Matter');
    await expect(hero).toContainText('Less than 1%');
  });

  test('should display three credential cards', async ({ page }) => {
    const cards = page.locator('.credential-card');
    await expect(cards).toHaveCount(3);
  });

  test('should display CFP credential card', async ({ page }) => {
    const cfpCard = page.locator('.credential-card').filter({ hasText: 'CFP' }).first();
    await expect(cfpCard).toBeVisible();
    await expect(cfpCard).toContainText('Certified Financial Planner');
    await expect(cfpCard).toContainText('Bachelor\'s degree');
    await expect(cfpCard).toContainText('6,000+ hours');
  });

  test('should display AIF credential card', async ({ page }) => {
    const aifCard = page.locator('.credential-card').filter({ hasText: 'AIF' }).first();
    await expect(aifCard).toBeVisible();
    await expect(aifCard).toContainText('Accredited Investment Fiduciary');
    await expect(aifCard).toContainText('fiduciary duty');
  });

  test('should display ChFEBC credential card', async ({ page }) => {
    const chfebcCard = page.locator('.credential-card').filter({ hasText: 'ChFEBC' }).first();
    await expect(chfebcCard).toBeVisible();
    await expect(chfebcCard).toContainText('Chartered Federal Employee Benefits Consultant');
    await expect(chfebcCard).toContainText('FERS');
    await expect(chfebcCard).toContainText('TSP');
  });

  test('should have badge icons for each credential', async ({ page }) => {
    const badges = page.locator('.credential-card__badge');
    await expect(badges).toHaveCount(3);

    // Each badge should have an SVG
    for (let i = 0; i < 3; i++) {
      const svg = badges.nth(i).locator('svg');
      await expect(svg).toBeVisible();
    }
  });

  test('should have hover effect on credential cards (desktop)', async ({ page, isMobile }) => {
    if (isMobile) {
      test.skip();
    }

    const card = page.locator('.credential-card').first();

    // Get initial border color
    const initialBorder = await card.evaluate(el =>
      window.getComputedStyle(el).borderColor
    );

    // Hover
    await card.hover();
    await page.waitForTimeout(300);

    // Border should change to gold on hover
    const hoverBorder = await card.evaluate(el =>
      window.getComputedStyle(el).borderColor
    );
    expect(hoverBorder).not.toBe(initialBorder);
  });

  test('should display Why It Matters section', async ({ page }) => {
    const whySection = page.locator('.why-matters');
    await expect(whySection).toBeVisible();
    await expect(whySection).toContainText('Fiduciary');
  });

  test('should display stat cards', async ({ page }) => {
    const statCards = page.locator('.stat-card');
    await expect(statCards.first()).toBeVisible();
    await expect(statCards).toHaveCount(3);
    await expect(page.locator('.stat-number').first()).toContainText('<1%');
  });

  test('should display CTA section', async ({ page }) => {
    const cta = page.locator('.section--navy');
    await expect(cta).toBeVisible();
    await expect(cta).toContainText('Work With Credentialed Experts');
  });

  test('should have working CTA buttons', async ({ page }) => {
    const workshopBtn = page.locator('.section--navy .btn--primary');
    await expect(workshopBtn).toBeVisible();
    await expect(workshopBtn).toContainText('Free FERS Workshop');

    const scheduleBtn = page.locator('.section--navy .btn--white');
    await expect(scheduleBtn).toBeVisible();
    await expect(scheduleBtn).toContainText('Schedule a Call');
  });

  test('should have responsive layout on mobile', async ({ page, isMobile }) => {
    if (!isMobile) {
      test.skip();
    }

    // Cards should stack vertically
    const cards = page.locator('.credential-card');
    const firstCard = cards.first();
    const secondCard = cards.nth(1);

    const firstBox = await firstCard.boundingBox();
    const secondBox = await secondCard.boundingBox();

    // Second card should be below first
    expect(secondBox!.y).toBeGreaterThan(firstBox!.y + firstBox!.height - 20);
  });

  test('should have scroll animations', async ({ page }) => {
    const animatedElements = page.locator('[data-animate="fade-in-up"]');
    await expect(animatedElements.first()).toBeVisible();
  });
});

test.describe('Financial Blueprint Page', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/about/financial-blueprint');
  });

  test('should load page with correct title', async ({ page }) => {
    await expect(page).toHaveTitle(/Financial Blueprint|Fed-Expert/);
  });

  test('should display hero section', async ({ page }) => {
    const hero = page.locator('.page-hero');
    await expect(hero).toBeVisible();
    await expect(hero).toContainText('Fed-Expert Financial Blueprint');
  });

  test('should display three blueprint steps', async ({ page }) => {
    const steps = page.locator('.blueprint-step');
    await expect(steps).toHaveCount(3);
  });

  test('should display Discovery step', async ({ page }) => {
    const discoveryStep = page.locator('.blueprint-step').first();
    await expect(discoveryStep).toBeVisible();
    await expect(discoveryStep).toContainText('Discovery');
    await expect(discoveryStep).toContainText('Leave & Earnings Statement');
  });

  test('should display Benefits Report step', async ({ page }) => {
    const reportStep = page.locator('.blueprint-step').nth(1);
    await expect(reportStep).toBeVisible();
    await expect(reportStep).toContainText('Benefits Report');
    await expect(reportStep).toContainText('22-page');
  });

  test('should display Partnership step', async ({ page }) => {
    const partnershipStep = page.locator('.blueprint-step').nth(2);
    await expect(partnershipStep).toBeVisible();
    await expect(partnershipStep).toContainText('Partnership');
    await expect(partnershipStep).toContainText('ongoing');
  });

  test('should have step numbers 1, 2, 3', async ({ page }) => {
    const stepNumbers = page.locator('.blueprint-step__number');
    await expect(stepNumbers).toHaveCount(3);
    await expect(stepNumbers.nth(0)).toContainText('1');
    await expect(stepNumbers.nth(1)).toContainText('2');
    await expect(stepNumbers.nth(2)).toContainText('3');
  });

  test('should have icons for each step', async ({ page }) => {
    const icons = page.locator('.blueprint-step__icon');
    await expect(icons).toHaveCount(3);

    // Each icon should have an SVG
    for (let i = 0; i < 3; i++) {
      const svg = icons.nth(i).locator('svg');
      await expect(svg).toBeVisible();
    }
  });

  test('should display 10 area badges in Benefits Report step', async ({ page }) => {
    const badges = page.locator('.area-badge');
    await expect(badges).toHaveCount(10);

    // Check specific badges
    await expect(page.locator('.area-badge').filter({ hasText: 'FERS/CSRS Pension' })).toBeVisible();
    await expect(page.locator('.area-badge').filter({ hasText: 'TSP Strategy' })).toBeVisible();
    await expect(page.locator('.area-badge').filter({ hasText: 'Medicare Coordination' })).toBeVisible();
  });

  test('should display timeline connecting line (desktop)', async ({ page, isMobile }) => {
    if (isMobile) {
      test.skip();
    }

    const timeline = page.locator('.blueprint-steps');
    await expect(timeline).toBeVisible();

    // Check for the ::before pseudo-element (connecting line)
    const hasBefore = await timeline.evaluate(el => {
      const before = window.getComputedStyle(el, '::before');
      return before.content !== 'none' && before.display !== 'none';
    });
    expect(hasBefore).toBe(true);
  });

  test('should display webinar promo section', async ({ page }) => {
    const webinarSection = page.locator('.webinar-promo');
    await expect(webinarSection).toBeVisible();
    await expect(webinarSection).toContainText('Federal Retirement Workshops');
    await expect(webinarSection).toContainText('3-hour FERS webinars');
  });

  test('should display workshop card', async ({ page }) => {
    const workshopCard = page.locator('.workshop-card');
    await expect(workshopCard).toBeVisible();
    await expect(workshopCard).toContainText('FERS Retirement Planning');
    await expect(workshopCard).toContainText('3-Hour Comprehensive Webinar');
  });

  test('should display CTA section', async ({ page }) => {
    const cta = page.locator('.section--navy');
    await expect(cta).toBeVisible();
    await expect(cta).toContainText('Ready to Get Your Blueprint');
  });

  test('should have working CTA buttons', async ({ page }) => {
    const contactBtn = page.locator('.section--navy .btn--primary');
    await expect(contactBtn).toBeVisible();
    await expect(contactBtn).toContainText('Contact Us');

    const webinarBtn = page.locator('.section--navy .btn--white');
    await expect(webinarBtn).toBeVisible();
    await expect(webinarBtn).toContainText('Join a Webinar');
  });

  test('should have responsive layout on mobile', async ({ page, isMobile }) => {
    if (!isMobile) {
      test.skip();
    }

    // Steps should stack with icon centered above content
    const firstStep = page.locator('.blueprint-step').first();
    const icon = firstStep.locator('.blueprint-step__icon');
    const content = firstStep.locator('.blueprint-step__content');

    const iconBox = await icon.boundingBox();
    const contentBox = await content.boundingBox();

    // Icon should be above content
    expect(iconBox!.y).toBeLessThan(contentBox!.y);
  });

  test('should have scroll animations', async ({ page }) => {
    const animatedElements = page.locator('[data-animate="fade-in-up"]');
    await expect(animatedElements.first()).toBeVisible();
  });
});

test.describe('About Pages SEO', () => {
  test('Our Credentials page has proper meta tags', async ({ page }) => {
    await page.goto('/about/our-credentials');

    // Check meta description
    const description = await page.locator('meta[name="description"]').getAttribute('content');
    expect(description).toContain('Less than 1%');
    expect(description).toContain('CFP');

    // Check canonical URL
    const canonical = await page.locator('link[rel="canonical"]').getAttribute('href');
    expect(canonical).toContain('/about/our-credentials');

    // Check Open Graph
    const ogTitle = await page.locator('meta[property="og:title"]').getAttribute('content');
    expect(ogTitle).toContain('Credentials');
  });

  test('Financial Blueprint page has proper meta tags', async ({ page }) => {
    await page.goto('/about/financial-blueprint');

    // Check meta description
    const description = await page.locator('meta[name="description"]').getAttribute('content');
    expect(description).toContain('3-step');
    expect(description).toContain('federal employees');

    // Check canonical URL
    const canonical = await page.locator('link[rel="canonical"]').getAttribute('href');
    expect(canonical).toContain('/about/financial-blueprint');

    // Check Open Graph
    const ogTitle = await page.locator('meta[property="og:title"]').getAttribute('content');
    expect(ogTitle).toContain('Blueprint');
  });
});
