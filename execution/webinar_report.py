"""
Webinar Report CLI
==================
Queries Mailchimp tags to show registration and attendance counts per webinar.

Usage:
    python webinar_report.py              # Show all webinars
    python webinar_report.py --webinar apr-10-2026   # Single webinar detail
    python webinar_report.py --json       # JSON output for piping
"""

import sys
import json
import argparse
from datetime import datetime, date
from pathlib import Path

# Ensure sibling imports work
sys.path.insert(0, str(Path(__file__).parent))
from mailchimp_client import get_members_by_tag

# ── Known webinars (same list the scheduler uses) ──────────────────────────

KNOWN_WEBINARS = [
    {'id': 'mar-27-2026', 'type': 'tsp', 'date': '2026-03-27', 'title': 'TSP Investment Strategies'},
    {'id': 'apr-10-2026', 'type': 'fers', 'date': '2026-04-10', 'title': 'FERS Retirement Workshop'},
    {'id': 'apr-17-2026', 'type': 'tsp', 'date': '2026-04-17', 'title': 'TSP Investment Strategies'},
    {'id': 'may-01-2026', 'type': 'fers', 'date': '2026-05-01', 'title': 'FERS Retirement Workshop'},
    {'id': 'may-22-2026', 'type': 'fers', 'date': '2026-05-22', 'title': 'FERS Retirement Workshop'},
    {'id': 'jun-12-2026', 'type': 'fers', 'date': '2026-06-12', 'title': 'FERS Retirement Workshop'},
]

# ── Payout tiers ────────────────────────────────────────────────────────────

PAYOUT_TIERS = [
    (100, '$3,000'),
    (75,  '$2,000'),
    (50,  '$1,250'),
    (35,  '$400'),
    (0,   '$0'),
]


def get_payout_tier(attended_count):
    """Map attendance count to payout tier."""
    for threshold, payout in PAYOUT_TIERS:
        if attended_count >= threshold:
            return payout
    return '$0'


def days_label(webinar_date, today):
    """Return a human-readable label like 'in 4 days' or 'past'."""
    delta = (webinar_date - today).days
    if delta > 1:
        return f'in {delta} days'
    elif delta == 1:
        return 'tomorrow'
    elif delta == 0:
        return 'today'
    else:
        return 'past'


def format_date_short(d):
    """Format date as 'Mar 27, 2026'."""
    return d.strftime('%b %-d, %Y')


def query_webinar(webinar, today):
    """Query Mailchimp for a single webinar's stats."""
    wtype = webinar['type']
    wid = webinar['id']
    wdate_str = webinar['date']
    wdate = date.fromisoformat(wdate_str)
    is_past = wdate < today

    # Registration tag: {type}-registered-{id}
    reg_tag = f'{wtype}-registered-{wid}'
    registered = get_members_by_tag(reg_tag)
    reg_count = len(registered)

    attended_count = None
    noshow_count = None

    if is_past:
        # Attended tag: webinar-attended-{date}
        att_tag = f'webinar-attended-{wdate_str}'
        attended = get_members_by_tag(att_tag)
        attended_count = len(attended)

        # No-show tag: webinar-noshow-{date}
        ns_tag = f'webinar-noshow-{wdate_str}'
        noshows = get_members_by_tag(ns_tag)
        noshow_count = len(noshows)

    return {
        'id': wid,
        'type': wtype,
        'title': webinar['title'],
        'date': wdate_str,
        'is_past': is_past,
        'days_label': days_label(wdate, today),
        'registered': reg_count,
        'attended': attended_count,
        'noshow': noshow_count,
    }


def print_report(results, today):
    """Print the formatted box-drawing report."""
    W = 62  # inner width

    def line(text=''):
        if text:
            return f'\u2551  {text:<{W - 2}}\u2551'
        return f'\u2551{" " * W}\u2551'

    print(f'\u2554{"=" * W}\u2557')
    title = f'PlanWell Webinar Report \u2014 {today.isoformat()}'
    print(f'\u2551{title:^{W}}\u2551')
    print(f'\u2560{"=" * W}\u2563')

    total_registered = 0
    total_attended = 0
    attended_webinars = 0
    most_recent_past_attended = None

    for r in results:
        print(line())
        header = f"{r['title']} \u2014 {format_date_short(date.fromisoformat(r['date']))} ({r['days_label']})"
        print(line(header))

        att_str = str(r['attended']) if r['attended'] is not None else '--'
        ns_str = str(r['noshow']) if r['noshow'] is not None else '--'

        print(line(f"\u251c\u2500 Registered: {r['registered']}"))
        print(line(f"\u251c\u2500 Attended:   {att_str}"))
        print(line(f"\u2514\u2500 No-show:    {ns_str}"))

        total_registered += r['registered']
        if r['attended'] is not None:
            total_attended += r['attended']
            attended_webinars += 1
            most_recent_past_attended = r['attended']

    print(line())
    print(f'\u2560{"=" * W}\u2563')

    avg_rate = round((total_attended / total_registered * 100)) if total_registered > 0 and attended_webinars > 0 else 0
    payout = get_payout_tier(most_recent_past_attended or 0)

    summary1 = f'Total registered (all): {total_registered}  |  Total attended: {total_attended}'
    summary2 = f'Avg attendance rate: {avg_rate}%     |  Payout tier: {payout}'
    print(line(summary1))
    print(line(summary2))
    print(f'\u255a{"=" * W}\u255d')


def main():
    parser = argparse.ArgumentParser(description='PlanWell Webinar Report')
    parser.add_argument('--webinar', type=str, help='Show single webinar by ID (e.g., apr-10-2026)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    today = date.today()

    # Filter to single webinar if requested
    webinars = KNOWN_WEBINARS
    if args.webinar:
        webinars = [w for w in KNOWN_WEBINARS if w['id'] == args.webinar]
        if not webinars:
            print(f'Error: webinar "{args.webinar}" not found.')
            print(f'Known IDs: {", ".join(w["id"] for w in KNOWN_WEBINARS)}')
            sys.exit(1)

    # Sort: upcoming first (by date), then past
    webinars_sorted = sorted(webinars, key=lambda w: w['date'])

    # Query each webinar
    results = []
    for w in webinars_sorted:
        try:
            result = query_webinar(w, today)
            results.append(result)
        except Exception as e:
            print(f'Warning: failed to query {w["id"]}: {e}', file=sys.stderr)
            results.append({
                'id': w['id'],
                'type': w['type'],
                'title': w['title'],
                'date': w['date'],
                'is_past': date.fromisoformat(w['date']) < today,
                'days_label': days_label(date.fromisoformat(w['date']), today),
                'registered': 0,
                'attended': None,
                'noshow': None,
                'error': str(e),
            })

    if args.json:
        output = {
            'report_date': today.isoformat(),
            'webinars': results,
            'totals': {
                'registered': sum(r['registered'] for r in results),
                'attended': sum(r['attended'] for r in results if r['attended'] is not None),
                'past_webinars': sum(1 for r in results if r['is_past']),
            },
        }
        # Add payout info
        past_results = [r for r in results if r['attended'] is not None]
        if past_results:
            most_recent = past_results[-1]
            output['payout'] = {
                'most_recent_attended': most_recent['attended'],
                'tier': get_payout_tier(most_recent['attended']),
            }
        print(json.dumps(output, indent=2))
    else:
        print_report(results, today)


if __name__ == '__main__':
    main()
