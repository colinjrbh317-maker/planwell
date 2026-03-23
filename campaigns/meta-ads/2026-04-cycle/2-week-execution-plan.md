# PlanWell Meta Ads — 2-Week Execution Plan
**Start:** Monday, March 23, 2026
**Budget:** $20/day ($280 over 2 weeks)
**Goal:** Launch first multi-offer campaign, establish baselines, identify winning creative

---

## WEEK 1: Setup + Launch (March 23-29)

### Monday, March 23 — Infrastructure Day (Colin)

**Morning:**
- [ ] Get Meta Business Manager API credentials from Brennan (META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN, META_AD_ACCOUNT_ID, META_PAGE_ID)
- [ ] Add credentials to `.env`
- [ ] Verify Facebook Pixel fires correctly on /webinar registration confirmation (check Events Manager → Test Events)
- [ ] Create conversion event "Lead" in Events Manager if not already set

**Afternoon:**
- [ ] Upload Mailchimp subscriber list as Custom Audience in Meta Business Manager
- [ ] Create 1% Lookalike Audience from subscriber list
- [ ] Create Website Visitor Custom Audience (Pixel, last 30 days)
- [ ] Set up exclusion audience: existing webinar registrants (if trackable via Pixel)

### Tuesday, March 24 — Creative Upload + Campaign Build (Colin + Buff)

**Buff does:**
- [ ] Stage PAUSED campaign via meta_ads_client.py (once API keys are in .env)
- [ ] Generate 2 more creative variants if needed based on Colin's feedback

**Colin does (in Meta Ads Manager):**
- [ ] Upload the top 4 image creatives:
  - v3 Concerned Fed (emotion → webinar)
  - v3 Calculator Screenshot (native → calculator offer)
  - v3 Before/After (contrast → webinar)
  - v2 Lifestyle Kitchen (aspirational → webinar)
- [ ] Build Campaign 1: **"PlanWell — Webinar Registration"**
  - Objective: Leads (or Conversions if Pixel has enough data)
  - Ad Set A: Cold-Interest ($6/day) — ages 40-62, federal gov interests
  - Ad Set B: Warm-Retarget ($4/day) — Pixel 30-day visitors
  - 2 ads per ad set (Concerned Fed + Before/After for cold; Calculator + Lifestyle for warm)
- [ ] Build Campaign 2: **"PlanWell — Free Guide"**
  - Objective: Leads
  - Ad Set C: Cold-Interest ($3/day) — same targeting as above
  - 1 ad: Concerned Fed image + guide-focused copy from copy.md
- [ ] Build Campaign 3: **"PlanWell — Calculator"**
  - Objective: Traffic (drive to /calculators, pixel them for retargeting later)
  - Ad Set D: Cold-Interest ($2/day)
  - 1 ad: Calculator Screenshot + calculator copy
- [ ] Set all campaigns to START Wednesday March 25
- [ ] Double-check: landing page URLs correct, UTM parameters added

**UTM Template:**
```
?utm_source=facebook&utm_medium=paid&utm_campaign={campaign_name}&utm_content={ad_name}
```

### Wednesday, March 25 — Launch Day

- [ ] All 3 campaigns go live at midnight
- [ ] Colin checks Ads Manager at 10am — verify all ads are "Active" (not "In Review" or "Rejected")
- [ ] If any ads rejected: check copy for compliance issues (no guaranteed returns language, no "you will" promises)
- [ ] Do NOT touch anything for 48 hours — let Meta's algorithm learn

### Thursday, March 26 — Send Video Scripts to Brennan/David

- [ ] Email video-scripts.md to Brennan and David
- [ ] Highlight Scripts #1 and #3 as top priority
- [ ] Ask them to record by end of next week
- [ ] Offer to hop on a 15-min call to walk through recording tips

### Friday, March 28 — First Data Check (48 hours post-launch)

- [ ] Pull initial metrics from Ads Manager:
  - Impressions per ad set
  - CTR per ad
  - Cost per click
  - Any conversions (registrations or guide downloads)
  - Frequency (should be <1.5 at this point)
- [ ] **Kill rules** (apply now):
  - Any ad with CTR < 0.5% after 1,000 impressions → pause
  - Any ad set with CPC > $5 → pause
- [ ] **Don't kill yet** (too early):
  - CPR/CPA — need more data, wait until Week 2
- [ ] Document results in a quick note

### Saturday/Sunday — Let It Run
- Do nothing. Algorithm is learning. Don't make changes on weekends.

---

## WEEK 2: Optimize + Scale (March 30 - April 5)

### Monday, March 30 — Week 1 Review + Optimization

**Pull full Week 1 report:**
- [ ] Total spend
- [ ] Total impressions, clicks, CTR by ad set
- [ ] Conversions (webinar registrations, guide downloads, calculator visits)
- [ ] Cost per result by campaign
- [ ] Best and worst performing ads

**Optimization decisions:**

| Scenario | Action |
|----------|--------|
| An ad has CTR > 1.5% | This is a winner. Keep it. |
| An ad has CTR 0.8-1.5% | Acceptable. Let it run another week. |
| An ad has CTR < 0.8% after 2,000+ impressions | Kill it. Replace with new creative. |
| An ad set has CPR < $15 | Winning ad set. Increase budget by 20% ($1-2/day). |
| An ad set has CPR $15-25 | On benchmark. Keep running. |
| An ad set has CPR > $25 | Underperforming. Reduce budget or pause. |
| Cold-Interest outperforms Cold-Lookalike | Expected early. Lookalikes need more data. |
| Guide campaign has lower CPA than Webinar | Expected. Guide is lower commitment. Watch nurture conversion later. |
| Calculator campaign drives traffic but no registrations | That's fine — goal is pixel pool. Check retarget conversions. |

**Creative refresh (Buff generates):**
- [ ] 2 new image variants of the winning concept
- [ ] If videos are recorded: upload and create video ad sets

### Tuesday, March 31 — Implement Changes

- [ ] Pause underperformers
- [ ] Boost winners (increase budget 20%, NOT more)
- [ ] Upload any new creatives
- [ ] Add new ads to winning ad sets
- [ ] Wait 48 hours again

### Wednesday, April 1 — Email Nurture Check

- [ ] Review Mailchimp: any new subscribers from Guide campaign?
- [ ] Verify tags are being applied correctly (source-meta-ad)
- [ ] Check if newsletter→webinar funnel emails are queued for these new subscribers
- [ ] Send newsletter announcement for next webinar to full list (if not already scheduled)

### Thursday, April 2 — Mid-Week Data Check

- [ ] Pull metrics again
- [ ] Compare Week 2 performance vs Week 1
- [ ] Check frequency — if any ad is >3.0, it's fatigued → swap creative
- [ ] Check: are retarget ads converting better than cold? (They should be)

### Friday, April 4 — Week 2 Report + Next Cycle Planning

**Compile full 2-week report:**
- [ ] Total spend: $280
- [ ] Total webinar registrations from ads
- [ ] Total guide downloads from ads
- [ ] Total calculator visits from ads
- [ ] Blended CPR (cost per registration)
- [ ] Best performing creative (which concept won?)
- [ ] Best performing ad set (which audience won?)
- [ ] Best performing offer (webinar vs guide vs calculator)

**Decisions for next cycle:**
- [ ] Which creative concept to double down on
- [ ] Which offer to scale
- [ ] Whether to increase budget (if CPR is profitable)
- [ ] Video ad status (did Brennan/David record?)
- [ ] Plan Week 3-4 creative refresh

---

## Budget Summary

| Week | Daily | Total | Split |
|------|-------|-------|-------|
| Week 1 | $15/day (ramp up) | $105 | Webinar $10, Guide $3, Calculator $2 |
| Week 2 | $20/day (full) | $140 | Shift budget toward winners |
| **Total** | — | **$245-280** | — |

**Note:** Start at $15/day Week 1 to let algorithm learn with smaller spend. Scale to $20/day Week 2 once you have data. This protects against burning budget on unproven creative.

---

## What Colin Sends to Brennan This Week

**Email 1 (Monday):** The Brennan email draft (.tmp/brennan_email_draft.md) — covers SEO work, growth plan, discovery questions

**Email 2 (Thursday):** Video scripts email:
> "Hey Brennan and David — we're launching Meta ads this week and want to add video to the mix. Attached are 6 short scripts (25-30 seconds each). iPhone recording is perfect. I'd recommend starting with Script 1 ('The $127K Mistake') and Script 3 ('I See This Every Week'). Happy to hop on a quick call to walk through recording tips if helpful."

---

## Success Metrics (What "Good" Looks Like After 2 Weeks)

| Metric | Target | Great |
|--------|--------|-------|
| Webinar registrations from ads | 5-10 | 15+ |
| Guide downloads | 10-20 | 30+ |
| Calculator page visits | 30-50 | 100+ |
| Blended CPR (webinar) | < $25 | < $15 |
| Cost per guide download | < $10 | < $5 |
| CTR (best ad) | > 1.0% | > 2.0% |
| New Mailchimp subscribers (from guide) | 10-20 | 30+ |

**The real win:** After 2 weeks, you know which creative concept, which audience, and which offer works. That data is worth more than the $280 in ad spend. Cycle 2 starts with proven assets instead of guessing.
