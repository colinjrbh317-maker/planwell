# Post-Webinar Send Runbook (Next Cycle)

Goal: send Day-1 attendee + Day-1 no-show emails within 1 business day of the webinar, without Colin in the loop.

## Prereqs (one-time, already done for 2026-04)

- `execution/tag_cycle_cohort.py` exists
- `campaigns/nurture/2026-04-cycle/` has the two reviewed .md templates
- Mailchimp API key set in `.env`

## Steps (per cycle, ~15 minutes)

### 1. Download the Zoom attendee report

In Zoom → Reports → Webinar → pick the webinar → export "Registration and Attendee Report" as CSV.

Save it to a new folder at the PLAN WELL root:
```
PLAN WELL/webinar-YYYY-MM-DD-debrief/
  └── Meeting History {Month DD YYYY}.csv
```

### 2. Copy the previous cycle's email templates

```bash
cp -r planwell-site/campaigns/nurture/2026-04-cycle planwell-site/campaigns/nurture/YYYY-MM-cycle
```

Open the two `.md` files and update:
- Date references ("Friday" / "Friday's workshop")
- Cycle frontmatter (`cycle: YYYY-MM`, `tag: webinar-attended-YYYY-MM-cycle`)
- Any topic-specific details if the workshop was different (FERS vs TSP etc.)

### 3. Dry-run the cohort tagger

```bash
cd planwell-site
python execution/tag_cycle_cohort.py \
  --cycle YYYY-MM-cycle \
  --csv "../webinar-YYYY-MM-DD-debrief/Meeting History {name}.csv" \
  --dry-run
```

Check the output:
- Attendee count looks right (usually 20-30 for a FERS workshop)
- No-show count looks right (usually 40-60)
- Zero test/debug emails
- Zero panelists (David, Brennan)
- Any hot leads who emailed us directly → add their email to `ALWAYS_EXCLUDE` in `tag_cycle_cohort.py` before re-running

### 4. Push tags to Mailchimp

Re-run without `--dry-run`:
```bash
python execution/tag_cycle_cohort.py \
  --cycle YYYY-MM-cycle \
  --csv "../webinar-YYYY-MM-DD-debrief/Meeting History {name}.csv"
```

Verify in Mailchimp UI:
- `webinar-attended-YYYY-MM-cycle` tag count matches dry-run
- `webinar-noshow-YYYY-MM-cycle` tag count matches dry-run

### 5. Create the two Mailchimp campaigns

In Mailchimp → Campaigns → Create → Regular Email.

**Campaign 1: Attendee Day 1**
- Audience: PlanWell main audience
- Segment: Contacts with tag `webinar-attended-YYYY-MM-cycle`
- From name: `PlanWell Financial Planning`
- From email: `info@planwellfp.com` (NOT david.fei@)
- Reply-to: `info@planwellfp.com`
- Subject: (copy from the .md file's Subject section)
- Preheader: (copy from the .md file's Preheader section)
- Body: paste the Body section into Mailchimp's template editor. Replace `{{FNAME}}` with Mailchimp's `*|FNAME|*` merge tag.

**Campaign 2: No-Show Day 1**
- Same setup, tag `webinar-noshow-YYYY-MM-cycle`, copy from the no-show .md file.

### 6. Test send → live send

1. In each campaign: Send Test → your own email address
2. Open both tests in your inbox. Check:
   - Sender reads `PlanWell Financial Planning <info@planwellfp.com>`
   - Your first name rendered correctly (not `*|FNAME|*`)
   - Booking link goes to `app.greminders.com/c/brennan-rhule`
   - Footer has unsubscribe + physical address
   - No em dashes, no "recording" references
3. If all good → Schedule or Send on both campaigns

### 7. Log the send

Add a line to `campaigns/nurture/SEND_LOG.md`:
```
| Date | Cycle | Attendees | No-shows | Notes |
| 2026-MM-DD | YYYY-MM-cycle | N | N | |
```

## Things that can go wrong

- **Brennan got duplicate confirmation during pre-webinar and missed this send** → check the dup-skip bug status (Part B of the velvet-mixing-giraffe plan). Until that's fixed, Mailchimp may silently suppress re-signups.
- **Mailchimp rejects the send for "too many contacts without opt-in"** → the webinar registration handler must be adding subscribers with explicit status. Check `webinar_nurture_handler.py` Mailchimp upsert.
- **A hot lead (like Joseph Silva) gets the drip instead of a human reply** → add them to `ALWAYS_EXCLUDE` in `tag_cycle_cohort.py` BEFORE tagging.
- **Sender shows as david.fei@ instead of info@** → `FROM_EMAIL` default not set. See Part B5 of the velvet-mixing-giraffe plan.

## Who to ask

- **Copy questions:** Colin
- **Compliance / disclosures:** David
- **Mailchimp access:** Colin has admin, Brennan has editor
