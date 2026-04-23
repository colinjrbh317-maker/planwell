#!/usr/bin/env python3
"""
SEO Monthly Report Generator

Runs on-demand (or via cron) to produce an SEO health snapshot combining:
  - GA4 landing-page traffic and conversion deltas
  - SEMrush domain overview and top keyword movements

Outputs markdown to .tmp/seo_reports/ with one file per run. Safe to re-run
since each report is dated.

Usage:
    python3 seo_monthly_report.py                  # default: last 30 days vs prior 30
    python3 seo_monthly_report.py --weeks 4        # last 4 weeks
    python3 seo_monthly_report.py --send-email     # also mail to Colin (uses .env SMTP)

Notes on credits:
    SEMrush API is credit-priced. This script caps requests to the minimum
    needed for a monthly snapshot: one domain_ranks call for planwellfp.com
    plus one domain_organic call limited to 500 keywords. If you want a full
    delta report, run semrush_client directly with larger limits.
"""

import argparse
import os
import sys
import csv
from datetime import datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent.parent
REPORT_DIR = PROJECT_DIR / '.tmp' / 'seo_reports'
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Make the execution/ dir importable when run directly
sys.path.insert(0, str(SCRIPT_DIR))


def format_period(days_back: int):
    end = datetime.utcnow().date()
    start = end - timedelta(days=days_back - 1)
    prior_end = start - timedelta(days=1)
    prior_start = prior_end - timedelta(days=days_back - 1)
    return (
        start.strftime('%Y-%m-%d'),
        end.strftime('%Y-%m-%d'),
        prior_start.strftime('%Y-%m-%d'),
        prior_end.strftime('%Y-%m-%d'),
    )


def pull_ga4_snapshot(current_range, prior_range):
    """Returns (current_top_pages, prior_top_pages) or None if GA4 not accessible."""
    try:
        from ga4_client import GA4Client
    except Exception as e:
        print(f'  GA4 import failed: {e}')
        return None, None

    try:
        client = GA4Client()
    except Exception as e:
        print(f'  GA4 auth failed: {e}')
        return None, None

    try:
        current = client.get_top_pages(current_range[0], current_range[1], limit=20)
        prior = client.get_top_pages(prior_range[0], prior_range[1], limit=20)
        return current, prior
    except Exception as e:
        print(f'  GA4 fetch failed: {e}')
        return None, None


def pull_semrush_snapshot():
    """Returns (overview_dict, top_keywords_list) or (None, None) on failure."""
    try:
        from semrush_client import get_domain_overview, get_organic_keywords
    except Exception as e:
        print(f'  SEMrush import failed: {e}')
        return None, None

    try:
        overview = get_domain_overview('planwellfp.com')
        if 'error' in overview:
            return overview, None
        keywords = get_organic_keywords('planwellfp.com', limit=50)
        return overview, keywords
    except Exception as e:
        print(f'  SEMrush fetch failed: {e}')
        return None, None


def format_ga4_section(current, prior, current_range, prior_range):
    if not current:
        return '## GA4 Traffic\n\n_GA4 data not available this run. Check credentials and property access._\n'

    # Build a URL => (sessions, conversions) dict for each window
    def to_map(rows):
        m = {}
        for r in rows:
            url = r.get('pagePath') or r.get('page_path') or r.get('url') or ''
            if not url:
                continue
            sessions = int(r.get('sessions') or 0)
            conversions = int(r.get('conversions') or r.get('keyEvents') or 0)
            m[url] = {'sessions': sessions, 'conversions': conversions}
        return m

    cur_map = to_map(current)
    pri_map = to_map(prior) if prior else {}

    lines = []
    lines.append('## GA4 Traffic and Conversions')
    lines.append('')
    lines.append(f'- Current window: {current_range[0]} to {current_range[1]}')
    lines.append(f'- Prior window:   {prior_range[0]} to {prior_range[1]}')
    lines.append('')
    lines.append('| Landing Page | Sessions (now) | Sessions (prior) | Delta | Conversions (now) | CR% |')
    lines.append('|--------------|---------------:|-----------------:|------:|------------------:|----:|')

    # Sort current by sessions desc
    sorted_pages = sorted(cur_map.items(), key=lambda kv: -kv[1]['sessions'])
    for url, cur_data in sorted_pages[:20]:
        cur_s = cur_data['sessions']
        cur_c = cur_data['conversions']
        pri_s = pri_map.get(url, {}).get('sessions', 0)
        delta = cur_s - pri_s
        delta_pct = (delta / pri_s * 100) if pri_s else 0
        cr = (cur_c / cur_s * 100) if cur_s else 0
        delta_str = f'{delta:+,} ({delta_pct:+.1f}%)' if pri_s else 'new'
        lines.append(
            f'| `{url}` | {cur_s:,} | {pri_s:,} | {delta_str} | {cur_c:,} | {cr:.2f}% |'
        )

    # Flag pages with traffic but zero conversion
    zero_conv = [(u, d) for u, d in sorted_pages[:20] if d['sessions'] > 500 and d['conversions'] == 0]
    if zero_conv:
        lines.append('')
        lines.append('### Conversion leaks (500+ sessions, zero key events)')
        for url, d in zero_conv:
            lines.append(f'- `{url}` — {d["sessions"]:,} sessions, 0 conversions')

    lines.append('')
    return '\n'.join(lines)


def format_semrush_section(overview, keywords):
    if not overview:
        return '## SEMrush\n\n_SEMrush data not available this run. Likely out of API credits or connectivity issue._\n'

    lines = []
    lines.append('## SEMrush Organic Snapshot')
    lines.append('')
    lines.append('| Metric | Value |')
    lines.append('|--------|-------|')
    lines.append(f'| SEMrush Rank | {overview.get("rank", "n/a"):,} |')
    lines.append(f'| Organic Keywords | {overview.get("organic_keywords", 0):,} |')
    lines.append(f'| Organic Traffic (est.) | {overview.get("organic_traffic", 0):,} |')
    lines.append(f'| Organic Traffic Value | ${overview.get("organic_cost", 0):,.2f} |')
    lines.append('')

    if keywords:
        lines.append('### Top 20 organic keywords')
        lines.append('')
        lines.append('| Keyword | Pos | Volume | CPC | KD |')
        lines.append('|---------|----:|-------:|----:|---:|')
        for kw in keywords[:20]:
            lines.append(
                f'| {kw["keyword"]} | {kw["position"]} | {kw["volume"]:,} '
                f'| ${kw["cpc"]:.2f} | {kw["difficulty"]} |'
            )
        lines.append('')

        # Position distribution summary
        top3 = sum(1 for k in keywords if 1 <= k['position'] <= 3)
        top10 = sum(1 for k in keywords if 1 <= k['position'] <= 10)
        top20 = sum(1 for k in keywords if 1 <= k['position'] <= 20)
        lines.append('### Position distribution (from sampled keywords)')
        lines.append(f'- Top 3:  {top3}')
        lines.append(f'- Top 10: {top10}')
        lines.append(f'- Top 20: {top20}')
        lines.append('')

    return '\n'.join(lines)


def format_priorities_section():
    """Evergreen priorities the plan keeps us accountable to."""
    return '''## Weekly Priorities (from the SEO plan)

1. Monitor SEMrush Position Tracking visibility. Target: 3.67% -> 8% in 90 days.
2. Watch top-20 keywords drifting toward top 10. Refresh on-page SEO for any that slip.
3. Check GA4 conversion rate on the 6 calculator pages. Any under 1.0% for 4 consecutive weeks triggers CTA A/B test review.
4. Verify vercel.json www-to-non-www redirect still firing (302 chain audit via `curl -IL https://www.planwellfp.com/fers-retirement-calculator`).
5. Re-run this script Monday morning and forward to Brennan/David.

'''


def main():
    parser = argparse.ArgumentParser(description='PlanWell SEO monthly report')
    parser.add_argument('--days', type=int, default=30, help='Days in current window')
    parser.add_argument('--label', type=str, default=None, help='Optional report label')
    args = parser.parse_args()

    cur_start, cur_end, prior_start, prior_end = format_period(args.days)
    current_range = (cur_start, cur_end)
    prior_range = (prior_start, prior_end)

    print(f'SEO Monthly Report')
    print(f'  Current: {cur_start} to {cur_end}')
    print(f'  Prior:   {prior_start} to {prior_end}')
    print()

    print('Fetching GA4 snapshot...')
    ga4_current, ga4_prior = pull_ga4_snapshot(current_range, prior_range)

    print('Fetching SEMrush snapshot...')
    sem_overview, sem_keywords = pull_semrush_snapshot()

    timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H%M')
    label = f'_{args.label}' if args.label else ''
    output_path = REPORT_DIR / f'seo_report_{timestamp}{label}.md'

    sections = []
    sections.append(f'# PlanWell SEO Report')
    sections.append(f'')
    sections.append(f'**Generated:** {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}')
    sections.append(f'**Window:** last {args.days} days vs prior {args.days} days')
    sections.append('')
    sections.append('---')
    sections.append('')
    sections.append(format_ga4_section(ga4_current, ga4_prior, current_range, prior_range))
    sections.append('---')
    sections.append('')
    sections.append(format_semrush_section(sem_overview, sem_keywords))
    sections.append('---')
    sections.append('')
    sections.append(format_priorities_section())
    sections.append('---')
    sections.append('')
    sections.append(f'_Generated by `execution/seo_monthly_report.py`._')

    output_path.write_text('\n'.join(sections), encoding='utf-8')
    print(f'  Report saved to: {output_path}')
    print()

    # Also print a short summary to stdout
    if sem_overview and 'error' not in sem_overview:
        print(f'  Organic traffic (est.): {sem_overview.get("organic_traffic", 0):,}')
        print(f'  Organic keywords: {sem_overview.get("organic_keywords", 0):,}')
    if ga4_current:
        print(f'  GA4 pages tracked: {len(ga4_current)}')


if __name__ == '__main__':
    main()
