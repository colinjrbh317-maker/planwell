# Meta Ads Campaign Management

## Purpose
Manage Meta (Facebook/Instagram) ad campaigns for PlanWell webinar registration cycles. Semi-automated: Buff generates creative + copy, stages as PAUSED campaigns, Colin reviews and publishes.

## Inputs
- Webinar date, topic, cycle ID
- Ad budget ($20/day default, split: $8 cold-interest, $6 cold-lookalike, $4 warm-retarget, $2 warm-email)
- Creative assets (generated via nano-banana-pro)

## Tools/Scripts
- `execution/meta_ads_client.py` — Meta Marketing API
- `nano-banana-pro` skill — Image generation
- `direct-response-copy` skill — Ad copy
- `marketing-psychology` skill — Hook selection

## Audience Targeting Presets

### Cold - Interest
Ages 40-62. Interests: "federal government", "Thrift Savings Plan", "FERS", "Federal Employees Retirement System", "government employees", "retirement planning", "OPM". Exclude: current clients (custom audience).

### Cold - Lookalike
1% lookalike of Mailchimp subscriber list.

### Warm - Retarget
Facebook Pixel visitors (last 30 days) who visited /webinar or /webinars but didn't register.

### Warm - Email
Custom audience from Mailchimp subscriber list who haven't registered for current cycle.

## Creative Guidelines

### Image Specs
- 1080x1080 (feed)
- 1080x1920 (stories/reels)
- 1200x628 (right column)

### Brand
- Navy: #000d3e
- Gold: #d1a437
- Off-white: #f8f9fa
- Always include PlanWell logo

### Creative Types
- stat-callout
- question-hook
- authority/credentials
- social-proof
- urgency/countdown

### Copy Constraints
- Headlines: max 40 characters
- Primary text: max 125 characters (mobile optimization)
- Psychology rotation by phase: Launch (social proof), Build (scarcity), Push (FOMO), Final (urgency)

## Campaign Naming Convention
`{cycle-id}-{audience}-{creative-type}`
Example: `mar2026-cold-interest-stat-callout`

## Performance Benchmarks
| Metric | Target | Action |
|--------|--------|--------|
| CPR (cost per registration) | $15-20 | — |
| CTR | >1.0% | — |
| CPR > $30 after 48 hours | Kill | Pause ad set |
| CPR < $12 | Boost | Increase budget 20% |

## Budget Scaling Playbook
| Daily Budget | Strategy |
|-------------|----------|
| $20/day | Test 4 creatives across 2 audiences |
| $30/day | Add lookalike expansion + retarget |
| $50/day | Full funnel + video ads (from podcast clips) |

## Cycle Phase Schedule
| Phase | Days Before Webinar | Ad Focus |
|-------|-------------------|----------|
| Launch | -21 to -14 | Awareness, social proof, authority |
| Build | -14 to -7 | Urgency, limited spots |
| Push | -7 to -2 | FOMO, countdown, bandwagon |
| Final | -2 to 0 | Last call, regret avoidance |
| Post | +1 to +5 | Retarget no-shows for next cycle |

## Process

### Step 1: Generate Creative Assets
1. Determine cycle phase based on days until webinar
2. Select creative types appropriate for phase
3. Generate images via nano-banana-pro at all three specs
4. Generate copy via direct-response-copy skill with psychology hooks

### Step 2: Stage Campaigns
1. Create campaign in Meta via `execution/meta_ads_client.py`
2. Set audience targeting per preset
3. Upload creatives and copy
4. Set daily budget per audience split
5. Stage as PAUSED — do NOT publish

### Step 3: Colin Reviews & Publishes
1. Colin reviews staged campaigns in Ads Manager
2. Approves or requests changes
3. Publishes approved campaigns

### Step 4: Monitor & Optimize
1. Check performance daily against benchmarks
2. Apply kill/boost thresholds automatically
3. Refresh creative if CTR drops below 0.8%
4. Shift budget toward best-performing audiences

## Environment Variables
```
META_APP_ID
META_APP_SECRET
META_ACCESS_TOKEN
META_AD_ACCOUNT_ID
META_PIXEL_ID=1064203284941145
META_PAGE_ID
```

## Edge Cases
- **Budget exhausted mid-cycle**: Prioritize retarget (highest conversion), pause cold
- **Low CTR across all creatives**: Refresh creative, don't just increase budget
- **Compliance**: No guaranteed returns language, include "educational workshop" framing
- **Holiday cycles**: Increase budget 30% for January (New Year resolution) and September (back from summer)
- **API rate limits**: Respect Meta API limits, batch requests where possible
- **Ad rejection**: Review Meta policies, adjust copy/imagery, resubmit

## Updates Log
- 2026-03-19: Initial creation
