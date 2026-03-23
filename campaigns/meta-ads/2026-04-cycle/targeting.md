# Meta Ad Targeting — April 2026 Webinar Cycle

**Total Daily Budget:** $20/day
**Campaign Duration:** 21 days (3 weeks before webinar)
**Total Cycle Spend:** ~$420
**Expected Registrations:** 24-40 (at $10.50-$17.50 CPR)

---

## Ad Set 1: Cold — Interest Targeting

**Budget:** $8/day ($168 total)
**Objective:** Conversions → Lead (webinar registration)

**Demographics:**
- Location: United States
- Language: English
- Note: Age targeting prohibited for financial services (Meta policy)

**Interest Targeting (include ALL):**
- Federal government of the United States
- Thrift Savings Plan
- Federal Employees Retirement System
- Office of Personnel Management
- Government Accountability Office
- Military retirement
- Civil Service Retirement System
- Federal Employees Health Benefits
- United States federal civil service
- Government employees
- Retirement planning
- Civil service
- GS pay scale

**Employer Keyword Targeting (profile-based):**
- Department of Defense
- Department of Veterans Affairs
- Department of Homeland Security
- Internal Revenue Service
- Social Security Administration
- Department of Justice
- Federal Bureau of Investigation
- National Aeronautics and Space Administration
- Department of State
- Department of the Treasury

**Exclusions:**
- Custom audience: existing webinar registrants
- Custom audience: existing PlanWell clients

**Placement:** Automatic (Facebook Feed, Instagram Feed, Stories, Reels)

---

## Ad Set 2: Cold — Lookalike Audience

**Budget:** $6/day ($126 total)
**Objective:** Conversions → Lead

**Source:** 1% Lookalike of:
- Past webinar registrants (upload Mailchimp list)
- Website visitors who hit /webinar page (Pixel-based)

**Demographics:**
- Location: United States
- Note: Age targeting prohibited for financial services (Meta policy)

**Exclusions:** Same as Ad Set 1

---

## Ad Set 3: Warm — Retargeting

**Budget:** $4/day ($84 total)
**Objective:** Conversions → Lead

**Audience:** Custom audience from Facebook Pixel:
- Visited planwellfp.com in last 30 days
- OR visited /webinar, /webinars, /services, /calculators pages
- EXCLUDE: already registered (tracked via Pixel conversion event)

**Demographics:** No age restriction (Meta financial services policy; they already know us)

---

## Ad Set 4: Warm — Email List

**Budget:** $2/day ($42 total)
**Objective:** Conversions → Lead

**Audience:** Custom audience:
- Upload Mailchimp subscriber list (email match)
- EXCLUDE: already registered for this cycle (tag: webinar-registered-2026-04-cycle)

**Demographics:** No restrictions (they're already subscribers)

---

## Campaign Structure Summary

```
Campaign: PlanWell Webinar - FERS Workshop - 2026-04-cycle
├── Ad Set 1: Cold-Interest ($8/day)
│   ├── Ad 1A: Stat-callout + Loss aversion
│   ├── Ad 1B: Question-hook + Question copy
│   └── Ad 1C: Authority + Credentials copy
├── Ad Set 2: Cold-Lookalike ($6/day)
│   ├── Ad 2A: Social-proof + Social copy
│   └── Ad 2B: Stat-callout + Loss aversion
├── Ad Set 3: Warm-Retarget ($4/day)
│   ├── Ad 3A: Urgency + Countdown copy
│   └── Ad 3B: Social-proof + Testimonial
└── Ad Set 4: Warm-Email ($2/day)
    └── Ad 4A: Authority + Direct CTA
```

---

## Optimization Rules

| Metric | Threshold | Action |
|--------|-----------|--------|
| CPR > $25 | After 48 hours | Pause that ad |
| CPR > $30 | After 24 hours | Pause that ad set |
| CTR < 0.8% | After 1,000 impressions | Replace creative |
| CPR < $12 | After 48 hours | Increase budget 20% |
| Frequency > 3.0 | Any time | Refresh creative |

---

## Setup Checklist (Colin — one-time)

- [ ] Upload Mailchimp subscriber list as Custom Audience in Meta Business Manager
- [ ] Create 1% Lookalike from webinar registrant list
- [ ] Verify Pixel fires on /webinar registration confirmation
- [ ] Create conversion event "Lead" in Events Manager
- [ ] Add billing method to Ad Account
- [ ] Provide META_AD_ACCOUNT_ID, META_ACCESS_TOKEN to .env
