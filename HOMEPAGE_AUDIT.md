# PlanWell Homepage SEO & Conversion Audit

**File:** `src/pages/index.astro`
**Date:** 2026-03-19

---

## 1. Title Tag

**Current:**
```
Federal Retirement Planning for FERS & CSRS Employees
```

**Assessment:** The title is descriptive but misses high-commercial-intent keywords. It reads like a category label, not a value proposition. It does not include "financial planner for federal employees," which is a buyer-intent keyword. It also lacks the brand name, which hurts branded search CTR.

**Recommended:**
```
Federal Employee Financial Planner | FERS & CSRS Retirement Planning | PlanWell
```

**Code change** (line 68 of `index.astro`):
```astro
<!-- BEFORE -->
<BaseLayout
  title="Federal Retirement Planning for FERS & CSRS Employees"

<!-- AFTER -->
<BaseLayout
  title="Federal Employee Financial Planner | FERS & CSRS Retirement Planning | PlanWell"
```

**Why:** Targets "federal employee financial planner" (commercial intent), retains "FERS" and "CSRS" (informational qualifiers), and adds brand name for recognition in SERPs.

---

## 2. Meta Description

**Current:**
```
Expert FERS retirement planning from CFP® and ChFEBC℠ advisors. Free workshops and fee-based financial planning for federal employees.
```

**Assessment:** Solid. Mentions credentials, free workshops, and fee-based model. However, it could be stronger by including a social proof number and a clearer call to action. The special characters (registered marks) may not render in all SERPs.

**Recommended:**
```
Fiduciary financial planning for federal employees from CFP and ChFEBC advisors. Free 3-hour FERS workshops attended by 10,000+ feds. Fee-based, no commissions.
```

**Code change** (line 69):
```astro
<!-- BEFORE -->
  description="Expert FERS retirement planning from CFP® and ChFEBC℠ advisors. Free workshops and fee-based financial planning for federal employees."

<!-- AFTER -->
  description="Fiduciary financial planning for federal employees from CFP and ChFEBC advisors. Free 3-hour FERS workshops attended by 10,000+ feds. Fee-based, no commissions."
```

**Why:** Adds "fiduciary" (trust signal and search term), "10,000+" (social proof in SERP), "no commissions" (addresses objection), and "financial planning for federal employees" (keyword match).

---

## 3. H1 and Hero Content

**Current H1:**
```html
<h1 class="hero__title">
  <span class="hero__title-main">Retire on Your Terms.</span>
  <span class="hero__title-accent">Federal Benefits Made Simple.</span>
</h1>
```

**Assessment:** The H1 is emotionally resonant but contains zero target keywords. "Retire on Your Terms" could be about any retirement. "Federal Benefits Made Simple" is better but still generic. Google uses the H1 heavily for topic signals. This page should rank for "financial planner for federal employees," "FERS retirement planning," and "federal retirement advisor" -- none of those phrases appear in the H1.

**Current subtitle:**
```
Our team of Fed-Experts have helped thousands of feds turn complex federal benefits into a confident retirement.
```

**Assessment:** Good emotional copy but no keyword density. "Fed-Experts" is a made-up term that won't match any search query.

**Recommended H1:**
```html
<h1 class="hero__title">
  <span class="hero__title-main">Your Federal Retirement, Planned Right.</span>
  <span class="hero__title-accent">Fiduciary Financial Planning for Federal Employees.</span>
</h1>
```

**Recommended subtitle:**
```html
<p class="hero__subtitle">
  CFP® and ChFEBC℠ advisors who specialize in FERS retirement planning.
  Free workshops, personalized reports, and fee-based guidance — no commissions, ever.
</p>
```

**Why:** The accent line now contains the exact-match phrase "Financial Planning for Federal Employees." The subtitle adds "FERS retirement planning" and "fee-based" as secondary keyword matches while maintaining a clear value prop.

---

## 4. FAQ Schema

**Current FAQs (4):**
1. When can I retire under FERS?
2. How much will my FERS pension be?
3. What should I do with my TSP when I retire?
4. Do you charge for the FERS retirement workshop?

**Assessment:** Good start. These target informational queries. However, there are no FAQs about PlanWell itself (brand queries, trust queries) or about choosing an advisor (commercial-intent queries). Adding 5-6 more FAQs that target long-tail commercial keywords will increase SERP real estate and address buyer objections.

**Recommended additions (add to the `faqSchema` mainEntity array AND the visible FAQ section):**

### FAQ 5: "How do I choose a financial planner for federal employees?"
```javascript
{
  "@type": "Question",
  "name": "How do I choose a financial planner for federal employees?",
  "acceptedAnswer": {
    "@type": "Answer",
    "text": "Look for three things: federal benefits expertise (the ChFEBC℠ designation), fiduciary duty (legally required to act in your interest), and a fee-based model (no commissions from product sales). PlanWell advisors hold CFP®, ChFEBC℠, and AIF® credentials and operate as fiduciaries. We recommend interviewing at least two advisors and asking about their experience with FERS, TSP rollovers, and FEHB-to-Medicare transitions."
  }
}
```

### FAQ 6: "Is PlanWell a fiduciary?"
```javascript
{
  "@type": "Question",
  "name": "Is PlanWell a fiduciary?",
  "acceptedAnswer": {
    "@type": "Answer",
    "text": "Yes. PlanWell advisors are legally bound fiduciaries, meaning we must act in your best interest at all times. We are fee-based and do not earn commissions from product sales. This is different from many federal benefits advisors who are compensated by insurance companies. Our only incentive is helping you make the best decisions for your retirement."
  }
}
```

### FAQ 7: "What is a ChFEBC℠ (Chartered Federal Employee Benefits Consultant)?"
```javascript
{
  "@type": "Question",
  "name": "What is a ChFEBC℠ (Chartered Federal Employee Benefits Consultant)?",
  "acceptedAnswer": {
    "@type": "Answer",
    "text": "The ChFEBC℠ is a professional designation for financial advisors who specialize in federal employee benefits. It requires completing coursework on FERS, CSRS, TSP, FEHB, FEGLI, Social Security coordination, and survivor benefits. Both PlanWell co-founders hold this designation along with the CFP® (Certified Financial Planner) and AIF® (Accredited Investment Fiduciary) credentials."
  }
}
```

### FAQ 8: "How much does PlanWell's financial planning service cost?"
```javascript
{
  "@type": "Question",
  "name": "How much does PlanWell's financial planning service cost?",
  "acceptedAnswer": {
    "@type": "Answer",
    "text": "Our 3-hour FERS workshop is completely free. For personalized financial planning, we offer fee-based services with transparent pricing — no hidden costs or commissions. During your free 1-on-1 consultation, we'll explain our fee structure and help you determine if comprehensive planning is right for your situation. You're never pressured to buy anything."
  }
}
```

### FAQ 9: "What's the difference between FERS and CSRS retirement?"
```javascript
{
  "@type": "Question",
  "name": "What's the difference between FERS and CSRS retirement?",
  "acceptedAnswer": {
    "@type": "Answer",
    "text": "FERS (Federal Employees Retirement System) is a three-part system: a defined benefit pension, Social Security, and the Thrift Savings Plan (TSP). CSRS (Civil Service Retirement System) provides a larger pension but no Social Security coverage or automatic TSP matching. CSRS was replaced by FERS in 1987, though some employees remain under CSRS or CSRS Offset. Our advisors are experienced with both systems."
  }
}
```

**Visible FAQ HTML to add** (insert after the existing 4th `<details>` block in the FAQ section):

```html
<details class="faq-item" data-animate="fade-in-up">
  <summary class="faq-item__question">
    <span>How do I choose a financial planner for federal employees?</span>
    <svg class="faq-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
  </summary>
  <div class="faq-item__answer">
    <p>Look for federal benefits expertise (the ChFEBC℠ designation), fiduciary duty, and a fee-based model with no commissions. We recommend interviewing at least two advisors and asking about their experience with FERS, TSP rollovers, and FEHB-to-Medicare transitions.</p>
  </div>
</details>

<details class="faq-item" data-animate="fade-in-up">
  <summary class="faq-item__question">
    <span>Is PlanWell a fiduciary?</span>
    <svg class="faq-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
  </summary>
  <div class="faq-item__answer">
    <p>Yes. PlanWell advisors are legally bound fiduciaries. We are fee-based and do not earn commissions from product sales — our only incentive is helping you make the best decisions for your retirement.</p>
  </div>
</details>

<details class="faq-item" data-animate="fade-in-up">
  <summary class="faq-item__question">
    <span>What is a ChFEBC℠ credential?</span>
    <svg class="faq-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
  </summary>
  <div class="faq-item__answer">
    <p>The Chartered Federal Employee Benefits Consultant (ChFEBC℠) designation is for financial advisors who specialize in federal employee benefits — covering FERS, CSRS, TSP, FEHB, FEGLI, Social Security coordination, and survivor benefits. Both PlanWell co-founders hold this credential.</p>
  </div>
</details>

<details class="faq-item" data-animate="fade-in-up">
  <summary class="faq-item__question">
    <span>How much does financial planning with PlanWell cost?</span>
    <svg class="faq-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
  </summary>
  <div class="faq-item__answer">
    <p>Our FERS workshop is completely free. For personalized planning, we offer fee-based services with transparent pricing and no commissions. During your free 1-on-1 consultation, we explain our fee structure with no pressure.</p>
  </div>
</details>

<details class="faq-item" data-animate="fade-in-up">
  <summary class="faq-item__question">
    <span>What's the difference between FERS and CSRS?</span>
    <svg class="faq-item__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
  </summary>
  <div class="faq-item__answer">
    <p>FERS is a three-part system (pension, Social Security, TSP) while CSRS provides a larger pension but no Social Security or TSP matching. CSRS was replaced by FERS in 1987. Our advisors are experienced with both systems.</p>
  </div>
</details>
```

---

## 5. Internal Links Audit

**Current internal links on homepage:**

| Link | Target | Present? |
|------|--------|----------|
| Free Federal Employee Webinars | `/webinars` | Yes |
| Book a 1-on-1 Call | `/book-call` | Yes |
| Get the Answers at Our Free Workshop | `/webinars` | Yes |
| Explore Our Services | `/services` | Yes |
| Reserve My Free Workshop Seat | `/webinars` | Yes |
| Learn More About Us | `/about` | Yes |
| View All Articles | `/blog` | Yes |
| Free FERS Workshop | `/webinars` | Yes |
| Book a 1-on-1 Call | `/book-call` | Yes |
| 3 recent blog articles | `/{slug}` | Yes |

**Missing high-value internal links:**

| Target | Page Exists? | Priority |
|--------|-------------|----------|
| `/financial-planner-for-federal-employees` | **Yes** | HIGH |
| `/federal-retirement-webinars` | **Yes** | HIGH |
| `/calculators` | **Yes** | HIGH |
| `/services/fers-retirement-planning` | Yes | MEDIUM |
| `/services/tsp-management` | Yes | MEDIUM |
| `/services/fehb-medicare` | Yes | MEDIUM |
| `/services/tax-planning` | Yes | MEDIUM |
| `/services/survivor-benefits` | Yes | MEDIUM |
| `/services/comprehensive-planning` | Yes | MEDIUM |
| `/testimonials` | Yes | MEDIUM |
| `/fers-retirement-calculator` | Yes | LOW |
| `/about/our-credentials` | Yes | LOW |

### Recommended Internal Link Additions

**A. Add a "Tools & Calculators" link in the Solution/Benefits section.** After the "Explore Our Services" button (line 301), add a second CTA:

```html
<!-- BEFORE -->
<div class="section-cta">
  <a href="/services" class="btn btn--secondary btn--lg">Explore Our Services</a>
</div>

<!-- AFTER -->
<div class="section-cta">
  <a href="/services" class="btn btn--secondary btn--lg">Explore Our Services</a>
  <a href="/calculators" class="btn btn--ghost btn--lg" style="margin-left: var(--space-4); border: 2px solid var(--color-navy); color: var(--color-navy);">Try Our Free Calculators</a>
</div>
```

**B. Link "/financial-planner-for-federal-employees" from the hero subtitle or trust bar.** Add a contextual text link in the subtitle:

```html
<!-- Option: Add as a text link below the hero trust bar -->
<p style="margin-top: var(--space-4); font-size: var(--text-sm);">
  <a href="/financial-planner-for-federal-employees" style="color: var(--color-gold); text-decoration: underline;">
    Why choose a specialized financial planner for federal employees?
  </a>
</p>
```

**C. Link "/federal-retirement-webinars" from the Process section.** The "Attend Our Free Workshop" step (line 315-317) should link to the webinar info page:

```html
<!-- BEFORE -->
<h3>Attend Our Free Workshop</h3>
<p>3 hours covering FERS pension, TSP, FEHB, Medicare, Social Security, and survivor benefits.</p>

<!-- AFTER -->
<h3>Attend Our Free Workshop</h3>
<p>3 hours covering FERS pension, TSP, FEHB, Medicare, Social Security, and survivor benefits. <a href="/federal-retirement-webinars" style="color: var(--color-gold); text-decoration: underline;">See what's covered</a>.</p>
```

**D. Link individual service pages from the Benefits grid.** Each benefit card maps to a service page. Add inline links:

```html
<!-- Example for "How to Handle Your TSP" card -->
<h3>How to Handle Your TSP</h3>
<p>A clear strategy for withdrawals that minimizes taxes and maximizes income. <a href="/services/tsp-management" style="color: var(--color-gold);">Learn more</a></p>

<!-- Example for "FEHB + Medicare Coordination" card -->
<h3>FEHB + Medicare Coordination</h3>
<p>The right plan at the right time so you're never overpaying or uncovered. <a href="/services/fehb-medicare" style="color: var(--color-gold);">Learn more</a></p>

<!-- Example for "Survivor Benefits Decision" card -->
<h3>Survivor Benefits Decision</h3>
<p>Should you elect full, partial, or none? We'll show you the math. <a href="/services/survivor-benefits" style="color: var(--color-gold);">Learn more</a></p>

<!-- Example for "Your Tax-Smart Withdrawal Plan" card -->
<h3>Your Tax-Smart Withdrawal Plan</h3>
<p>Roth conversions, bracket management, and strategies to keep more of what you've earned. <a href="/services/tax-planning" style="color: var(--color-gold);">Learn more</a></p>
```

**E. Link to /testimonials from the Final CTA section.** Reinforce social proof:

```html
<!-- Add after "Join thousands of federal employees..." paragraph -->
<p class="final-cta__text">
  Join thousands of federal employees who stopped guessing and started planning.
  <a href="/testimonials" style="color: var(--color-navy-dark); text-decoration: underline; font-weight: 600;">Read their stories</a>.
</p>
```

---

## 6. "As Seen In" Section

**Current implementation:**
- Label: "As Featured In" (small, uppercase, gray text)
- 8 logos: CNBC, MSN, FedSmith, GovExec, Microsoft Start, CEO Weekly, New York Weekly, NewsBreak
- Auto-scrolling carousel with grayscale filter and 70% opacity
- Positioned immediately below the hero

**Assessment:** The placement is correct (directly below hero is standard). However:

1. **Too subtle.** Grayscale + 70% opacity makes logos barely visible. Users scroll past without registering.
2. **No heading weight.** "As Featured In" is styled as a label (`--text-sm`), not a trust signal.
3. **Missing anchor logos.** If PlanWell has been on CNBC, that's a top-tier credential -- it should be more prominent.

**Recommendations:**

```css
/* Make logos more visible */
.logo-carousel__item img {
  height: 50px;
  width: auto;
  object-fit: contain;
  filter: grayscale(100%);
  opacity: 0.85;           /* was 0.7 */
  transition: all 0.3s;
}

.logo-carousel__item img:hover {
  filter: grayscale(0%);
  opacity: 1;
}
```

Consider adding a static count above the carousel:

```html
<p class="logo-carousel__label">Trusted by 10,000+ Federal Employees · As Featured In</p>
```

---

## 7. Social Proof

**Current social proof elements:**
- Hero trust bar: "Fiduciary | Fee-Based | CFP® Certified" (small, gray text)
- Team section: Credential badges (CFP®, ChFEBC℠, AIF®)
- "As Featured In" logo carousel
- Final CTA: "Join thousands of federal employees..."
- FAQ: "Over 10,000 federal employees have attended" (only in schema JSON, NOT visible on page)

**What's missing:**
1. **No testimonials on homepage.** The `/testimonials` page exists but zero quotes appear on the homepage. This is a major conversion gap.
2. **No specific numbers above the fold.** "Thousands" is vague. "10,000+" is in the schema but not visible to users.
3. **No star ratings or review widgets.**
4. **Credential badges in the hero are text-only.** They should be more visually prominent.

**Recommended: Add a testimonial strip between the Process and Team sections.**

```html
<!-- Social Proof / Testimonial Section -->
<section class="section section--gray">
  <div class="container">
    <h2 class="section-title">What Federal Employees Say</h2>

    <div class="testimonial-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: var(--space-6); max-width: 1000px; margin: 0 auto;">
      <blockquote style="background: var(--color-white); padding: var(--space-6); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); border-top: 4px solid var(--color-gold);">
        <p style="color: var(--color-gray-600); font-size: var(--text-base); line-height: 1.6; margin-bottom: var(--space-4);">"The workshop answered questions I didn't even know I had. I learned more in 3 hours than in 20 years of working for the government."</p>
        <footer style="font-weight: var(--font-semibold); color: var(--color-navy); font-size: var(--text-sm);">— GS-14, Department of Defense</footer>
      </blockquote>

      <blockquote style="background: var(--color-white); padding: var(--space-6); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); border-top: 4px solid var(--color-gold);">
        <p style="color: var(--color-gray-600); font-size: var(--text-base); line-height: 1.6; margin-bottom: var(--space-4);">"David and Brennan found $40,000 in tax savings I would have missed. Their fee paid for itself many times over."</p>
        <footer style="font-weight: var(--font-semibold); color: var(--color-navy); font-size: var(--text-sm);">— Retired GS-15, VA</footer>
      </blockquote>

      <blockquote style="background: var(--color-white); padding: var(--space-6); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); border-top: 4px solid var(--color-gold);">
        <p style="color: var(--color-gray-600); font-size: var(--text-base); line-height: 1.6; margin-bottom: var(--space-4);">"Finally, advisors who actually understand FERS. Not generic retirement advice — real federal benefits expertise."</p>
        <footer style="font-weight: var(--font-semibold); color: var(--color-navy); font-size: var(--text-sm);">— GS-13, Department of Interior</footer>
      </blockquote>
    </div>

    <div class="section-cta">
      <a href="/testimonials" class="btn btn--secondary btn--lg">Read More Reviews</a>
    </div>
  </div>
</section>
```

**Note:** Replace the placeholder quotes above with actual testimonials from the `/testimonials` page.

**Also recommended: Add a stats bar to the hero or just below it.**

```html
<!-- Add after hero__trust div, inside hero__content -->
<div style="display: flex; gap: var(--space-8); margin-top: var(--space-6); flex-wrap: wrap;">
  <div>
    <span style="display: block; font-size: var(--text-2xl); font-weight: var(--font-bold); color: var(--color-gold);">10,000+</span>
    <span style="font-size: var(--text-sm); color: var(--color-gray-300);">Workshop Attendees</span>
  </div>
  <div>
    <span style="display: block; font-size: var(--text-2xl); font-weight: var(--font-bold); color: var(--color-gold);">20+</span>
    <span style="font-size: var(--text-sm); color: var(--color-gray-300);">Years Experience</span>
  </div>
  <div>
    <span style="display: block; font-size: var(--text-2xl); font-weight: var(--font-bold); color: var(--color-gold);">3</span>
    <span style="font-size: var(--text-sm); color: var(--color-gray-300);">Credentials Per Advisor</span>
  </div>
</div>
```

---

## 8. CTA Optimization

**Current CTAs and their targets:**

| CTA Text | Target | Location | Type |
|----------|--------|----------|------|
| Free Federal Employee Webinars | `/webinars` | Hero (primary) | Lead gen |
| Book a 1-on-1 Call | `/book-call` | Hero (secondary) | Sales |
| Get the Answers at Our Free Workshop | `/webinars` | Problem section | Lead gen |
| Explore Our Services | `/services` | Benefits section | Info |
| Reserve My Free Workshop Seat | `/webinars` | Process section | Lead gen |
| Learn More About Us | `/about` | Team section | Info |
| View All Articles | `/blog` | Articles section | Info |
| Free FERS Workshop | `/webinars` | Final CTA | Lead gen |
| Book a 1-on-1 Call | `/book-call` | Final CTA | Sales |
| Get Our Newsletter | Modal trigger | Final CTA | Lead gen |

**Assessment:**
- 4 of 9 CTAs go to `/webinars` -- good repetition but all use different text, which could be more consistent
- Only 2 CTAs go to `/book-call` (the highest-value conversion)
- "Explore Our Services" and "Learn More About Us" are low-commitment CTAs that dilute conversion focus
- "Get Our Newsletter" is the lowest-value CTA and occupies equal visual weight in the final CTA section
- No CTA mentions calculators, which are high-engagement, low-friction tools

**Recommendations:**

1. **Make "Book a 1-on-1 Call" more prominent.** It's the highest-value action but appears as a secondary ghost button. Consider making it primary in at least one section.

2. **Add urgency/specificity to webinar CTAs.** Instead of generic "Free Workshop" language:
   ```html
   <!-- More specific -->
   <a href="/webinars" class="btn btn--primary btn--lg">Register for Our Free 3-Hour FERS Workshop</a>
   ```

3. **Replace "Learn More About Us" with a higher-value CTA:**
   ```html
   <!-- BEFORE -->
   <a href="/about" class="btn btn--secondary btn--lg">Learn More About Us</a>

   <!-- AFTER -->
   <a href="/about/our-credentials" class="btn btn--secondary btn--lg">See Our Credentials</a>
   ```

4. **Reorder Final CTA buttons to put the highest-value action first:**
   ```html
   <div class="final-cta__buttons">
     <a href="/book-call" class="btn btn--navy btn--lg">Book a Free Consultation</a>
     <a href="/webinars" class="btn btn--outline-dark btn--lg">Attend a Free Workshop</a>
   </div>
   ```
   (Drop the newsletter button from the final CTA -- it dilutes the two primary conversion paths.)

---

## Summary: Priority Action Items

### High Priority (do first)
1. **Update title tag** to include "Financial Planner for Federal Employees" and brand name
2. **Rewrite H1** to include at least one target keyword phrase
3. **Add 5 new FAQs** targeting commercial long-tail keywords (fiduciary, ChFEBC, cost, choosing a planner)
4. **Add internal links** to `/financial-planner-for-federal-employees`, `/federal-retirement-webinars`, and `/calculators`
5. **Add testimonials section** to the homepage with 2-3 real quotes

### Medium Priority
6. **Update meta description** with social proof number and "fiduciary"
7. **Add stats bar** to hero (10,000+ attendees, 20+ years, credentials)
8. **Link benefit cards** to their corresponding `/services/*` pages
9. **Increase logo carousel opacity** from 0.7 to 0.85

### Low Priority
10. **Reorder final CTA** buttons (Book Call first, Workshop second, drop newsletter)
11. **Replace "Learn More About Us"** with "See Our Credentials" linking to `/about/our-credentials`
12. **Add hover effect** to logo carousel (grayscale to color on hover)

---

## Estimated SEO Impact

| Change | Expected Impact |
|--------|----------------|
| Title tag with commercial keyword | +15-25% CTR from SERP for target terms |
| H1 with keyword | Improved topical relevance for "financial planner for federal employees" |
| 5 new FAQ schema entries | 2-4 additional SERP features (People Also Ask, rich snippets) |
| Internal links to new pages | Faster indexing of `/financial-planner-for-federal-employees` and `/federal-retirement-webinars`; improved crawl equity distribution |
| Testimonials on homepage | +5-15% conversion rate improvement (industry benchmarks for social proof) |
| Stats in hero | Reduced bounce rate from trust signals above the fold |
