# PlanWell Popup Audit & Optimization Plan

**Date:** March 19, 2026
**Current Component:** `src/components/NewsletterPopup.astro`

---

## Current Implementation Analysis

### What It Does Now
- Fixed center-screen modal with blurred overlay
- Triggers after **7 seconds** on homepage only
- Shows max **3 times** per user (localStorage)
- Collects: name + email
- Offer: "Get Your Free Federal Retirement Guide"
- Submits to Railway webhook → Mailchimp
- GA4 event tracking on submit

### Screenshot Assessment
The popup is clean and well-designed visually. The PlanWell design system is applied correctly (navy/gold, Outfit font, proper spacing). The issue isn't aesthetics — it's **strategy, timing, and targeting**.

---

## 7 Problems With the Current Popup

### 1. Timed Trigger Is the Worst Trigger for This Audience
**Problem:** 7-second auto-fire interrupts visitors before they've engaged. Federal employees visiting a financial planning site are research-oriented, skeptical, and trust-sensitive. Getting hit with a popup before reading anything feels like a sales ambush.

**Data:** Exit-intent popups convert 2-4x higher than timed popups in financial services because they catch people who have already consumed content and are about to leave.

### 2. Vague Offer — "Free Federal Retirement Guide" Means Nothing
**Problem:** What guide? How many pages? What topics? "Guide" is the most overused lead magnet word on the internet. Federal employees receive dozens of "guides" from TSP, OPM, FEHB — another generic one doesn't stand out.

The description also mixes two different offers: "weekly insights" (newsletter) AND "comprehensive retirement planning guide" (lead magnet). The visitor doesn't know which one they're getting.

### 3. Too Many Form Fields
**Problem:** Name + email = 2 fields. Every additional field beyond email reduces conversion by 25-50%. For a lead magnet download, email alone is sufficient. You can collect name later in the welcome sequence or when they register for the webinar.

### 4. No Page Context Awareness
**Problem:** The popup is homepage-only and shows the same generic offer regardless of what the visitor is interested in. Someone deep in a TSP calculator should get a TSP-specific offer. Someone reading a FEHB article should get a healthcare-in-retirement offer.

### 5. Three Dismissals Before Stopping Is Too Aggressive
**Problem:** If someone closes the popup once, they've made a decision. Showing it 2 more times signals desperation and erodes the trust PlanWell is trying to build. For financial services, 1 dismissal = stop. Use softer re-engagement instead (inline CTAs, slide-in, banner).

### 6. No Exit-Intent Trigger
**Problem:** The single highest-converting popup trigger in financial services — catching visitors as they're about to leave — isn't used at all. Exit-intent has lower annoyance because it only fires when the visitor is already disengaging.

### 7. The Webinar Is a Better Offer Than a Newsletter
**Problem:** PlanWell's strongest conversion asset is the free 3-hour webinar. It's specific, high-value, time-bound, and directly leads to paid services. A generic "retirement guide" newsletter signup competes with and dilutes the webinar funnel. The popup should drive webinar registrations on most pages, not newsletter signups.

---

## Recommended Strategy: Context-Aware Smart Popup System

### Core Principle
**The popup offer should match what the visitor is already interested in, and trigger only when they've shown engagement or are about to leave.**

### Three Popup Variants

#### Variant A: Webinar Registration (Default — most pages)
- **Trigger:** Exit-intent OR 60% scroll depth (whichever comes first)
- **Where:** Homepage, service pages, about pages, location pages
- **Headline:** "Your FERS Questions Answered — For Free"
- **Subtext:** "Join [X] federal employees at our next 3-hour retirement workshop. [Date]. No cost, no obligation."
- **Form:** Email only
- **CTA:** "Save My Seat"
- **Why:** The webinar is the #1 conversion asset. Every page should funnel toward it unless there's a better contextual offer.

#### Variant B: Calculator/Tool Lead Magnet (Calculator pages)
- **Trigger:** After the user has completed a calculation (interaction-based)
- **Where:** All 7 calculator pages
- **Headline:** "Want a Personalized Analysis — Not Just an Estimate?"
- **Subtext:** "Our calculators give you a starting point. A 22-page personalized benefits report gives you the full picture. Free after attending our workshop."
- **Form:** Email only
- **CTA:** "Get My Personalized Report"
- **Why:** Someone who just used a calculator is actively researching their retirement. They're warm. Bridge them to the next step (webinar → report).

#### Variant C: Content-Specific Lead Magnet (Blog posts)
- **Trigger:** Exit-intent only (they've read content, now leaving)
- **Where:** Blog posts, matched by category
- **Logic:** Read the page's category tag and serve a matching offer:
  - **TSP articles** → "Free TSP Allocation Cheat Sheet"
  - **FERS articles** → "FERS Retirement Eligibility Quick-Check"
  - **FEHB/Medicare articles** → "FEHB + Medicare Coordination Checklist"
  - **Tax articles** → "Federal Retirement Tax Savings Worksheet"
  - **Default/other** → Fall back to Variant A (webinar)
- **Form:** Email only
- **CTA:** "Send Me the [Cheat Sheet/Checklist/Worksheet]"
- **Why:** Content-specific offers convert 3-5x higher than generic ones because they match the visitor's demonstrated interest.

### Trigger Rules (All Variants)

| Trigger | Condition | Why |
|---------|-----------|-----|
| Exit-intent | Mouse moves toward browser chrome (desktop) | Catches departing visitors without interrupting |
| Scroll depth | 60%+ page scrolled (mobile fallback) | Mobile doesn't have exit-intent; scroll depth = engagement signal |
| Post-interaction | After calculator use or form abandon | Highest intent signal available |
| Cool-down | 1 dismissal = don't show again for 14 days | Respects user choice, rebuilds trust |
| Frequency | Max 1 popup per session | Never interrupt twice in one visit |
| Suppression | Don't show if already registered for webinar or newsletter | Check localStorage for prior conversion |

### What NOT To Do
- No timed popups on any page
- No popups on the webinar registration page (they're already converting)
- No popups on /book-call (they're already converting)
- No popups on /privacy or /terms
- Never show the popup to someone who has already submitted any form

---

## Implementation Plan

### Phase 1: Replace Current Popup (Immediate)
1. Rewrite `NewsletterPopup.astro` → `SmartPopup.astro`
2. Implement exit-intent detection (desktop) + scroll depth (mobile)
3. Default to Variant A (webinar registration)
4. Change form to email-only
5. Reduce max views from 3 to 1 per 14-day period
6. Add suppression for already-converted users
7. Track variant + trigger type in GA4 events

### Phase 2: Add Contextual Variants (Week 2)
1. Add page-type detection (calculator, blog category, service, etc.)
2. Implement Variant B for calculator pages
3. Implement Variant C for blog posts (category-matched)
4. Create the actual lead magnet PDFs (cheat sheets, checklists)

### Phase 3: Add Slide-In Alternative (Week 3)
1. For returning visitors who dismissed the popup, show a subtle bottom-right slide-in instead
2. Much less intrusive, catches visitors on return visits
3. Same contextual offer matching as the popup

---

## Copy Recommendations by Variant

### Variant A (Webinar — Default)
```
Headline: Your FERS Questions — Answered Free
Subtext:  Join our next 3-hour retirement workshop on [dynamic date].
          10,000+ federal employees have attended. Zero cost. Zero pressure.
CTA:      Save My Seat →
Privacy:  We'll send your Zoom link. That's it. Unsubscribe anytime.
```

### Variant B (Calculator Follow-Up)
```
Headline: Want the Full Picture?
Subtext:  Online calculators give you estimates. Our 22-page personalized
          benefits report gives you exact numbers for YOUR situation.
          Free after our workshop.
CTA:      Register for Free Workshop →
Privacy:  Join 10,000+ feds who got their exact retirement numbers.
```

### Variant C Examples (Blog Context)

**TSP articles:**
```
Headline: Your TSP Allocation — Simplified
Subtext:  Get our 1-page TSP fund allocation guide based on your
          years to retirement. Used by 3,000+ federal employees.
CTA:      Send Me the Guide →
```

**FERS articles:**
```
Headline: Are You Eligible to Retire?
Subtext:  Quick-check your FERS retirement eligibility in 60 seconds.
          MRA+30, 60/20, and 62/5 — all in one printable sheet.
CTA:      Get the Eligibility Checker →
```

**FEHB/Medicare articles:**
```
Headline: FEHB + Medicare: Don't Overpay
Subtext:  Our coordination checklist shows you exactly what to do at 65.
          The wrong timing costs federal retirees $2,000+/year.
CTA:      Get the Checklist →
```
