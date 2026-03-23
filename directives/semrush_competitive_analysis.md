# SEMrush Competitive Analysis

## Goal
Run periodic competitive SEO analysis comparing PlanWell Federal Planning against key competitors, tracking organic keyword rankings, traffic trends, and backlink profiles.

## Target Domains
- **planwellfp.com** (primary)
- **stwserve.com** (STW Serve - competitor)
- **hawsfederal.com** (HAWS Federal Advisors - competitor)

## Tool
`execution/semrush_client.py`

## Workflows

### Quick Check (30 seconds)
```bash
python execution/semrush_client.py --quick
```
Returns high-level organic/paid metrics for planwellfp.com. Use for daily spot-checks.

### Full Competitive Report (2-3 minutes)
```bash
python execution/semrush_client.py --report
```
Generates a comprehensive markdown report at `.tmp/SEMRUSH_REPORT.md` covering:
1. Domain overview comparison (rank, traffic, keywords, cost)
2. Top organic keywords per domain (position, volume, CPC, difficulty)
3. Organic competitor discovery for planwellfp.com
4. Backlink profile comparison across all domains
5. Keyword research for key federal planning search terms

### Single Domain Deep Dive
```bash
python execution/semrush_client.py --domain stwserve.com
```
Overview, top keywords, and backlink profile for one domain.

### Keyword Research
```bash
python execution/semrush_client.py --keyword "federal retirement planning"
```
Volume, CPC, competition, and result count for a single keyword.

## Key Federal Planning Keywords to Track
- federal retirement planning
- FERS retirement calculator
- TSP withdrawal strategies
- federal employee benefits
- FEHB retirement
- federal sick leave retirement

## Schedule
- **Weekly:** Full report (Monday mornings)
- **Ad-hoc:** Before content planning sessions, after publishing new blog posts
- **Monthly:** Archive report to Google Drive for trend tracking

## API Details
- **Auth:** API key in `.env` as `SEMRUSH_API_KEY`
- **Rate Limits:** API units consumed per request; monitor usage at semrush.com dashboard
- **Response Format:** Semicolon-separated values (parsed by `csv.DictReader`)
- **Base URL:** `https://api.semrush.com/`

## Edge Cases & Lessons Learned
- SEMrush returns `ERROR 50 :: NOTHING FOUND` for domains with very low traffic; handle gracefully
- Response delimiter is semicolon (`;`), not tab or comma
- Export column names in responses differ from parameter names (e.g., `Or` param -> `Organic Keywords` header)
- Backlinks API uses `target` and `target_type` params instead of `domain`
- Some domains may have zero paid data; don't treat as errors

## Output
- **Deliverable:** `.tmp/SEMRUSH_REPORT.md` (regenerated each run)
- **Usage:** Feed into content strategy decisions, blog topic selection, competitive positioning
