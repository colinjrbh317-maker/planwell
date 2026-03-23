"""
SEMrush API Client
==================
Competitive analysis and keyword research for PlanWell Federal Planning.

API Docs: https://developer.semrush.com/api/
Auth: API key as query parameter
Response Format: Semicolon-separated values (first row = headers)
"""

import os
import csv
import io
import sys
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

SEMRUSH_API_KEY = os.environ.get('SEMRUSH_API_KEY', '')
BASE_URL = 'https://api.semrush.com/'


def _parse_response(response_text):
    """
    Parse SEMrush semicolon-separated response into list of dicts.
    First row is always headers. Returns empty list on error responses.
    """
    if not response_text or response_text.startswith('ERROR'):
        print(f'SEMrush API error: {response_text[:200]}')
        return []

    reader = csv.DictReader(io.StringIO(response_text.strip()), delimiter=';')
    return [row for row in reader]


def _request(params):
    """Make a request to the SEMrush API with the given params."""
    params['key'] = SEMRUSH_API_KEY

    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        if resp.status_code != 200:
            print(f'SEMrush HTTP error: {resp.status_code} - {resp.text[:200]}')
            return ''
        return resp.text
    except Exception as e:
        print(f'SEMrush request failed: {e}')
        return ''


def get_domain_overview(domain, db='us'):
    """
    Get high-level domain metrics: organic/paid traffic, keywords, cost.

    Args:
        domain: Domain to analyze (e.g., 'planwellfp.com')
        db: Database/country code (default 'us')

    Returns:
        dict with organic_keywords, organic_traffic, organic_cost,
        paid_keywords, paid_traffic, paid_cost, rank
    """
    params = {
        'type': 'domain_ranks',
        'export_columns': 'Dn,Rk,Or,Ot,Oc,Ad,At,Ac',
        'domain': domain,
        'database': db,
    }

    rows = _parse_response(_request(params))
    if not rows:
        return {'domain': domain, 'error': 'No data returned'}

    row = rows[0]
    return {
        'domain': row.get('Domain', domain),
        'rank': _safe_int(row.get('Rank', '0')),
        'organic_keywords': _safe_int(row.get('Organic Keywords', '0')),
        'organic_traffic': _safe_int(row.get('Organic Traffic', '0')),
        'organic_cost': _safe_float(row.get('Organic Cost', '0')),
        'paid_keywords': _safe_int(row.get('Adwords Keywords', '0')),
        'paid_traffic': _safe_int(row.get('Adwords Traffic', '0')),
        'paid_cost': _safe_float(row.get('Adwords Cost', '0')),
    }


def get_organic_keywords(domain, db='us', limit=50):
    """
    Get top organic keywords for a domain with positions and traffic.

    Args:
        domain: Domain to analyze
        db: Database/country code
        limit: Max keywords to return

    Returns:
        list of dicts with keyword, position, volume, cpc, url,
        traffic_pct, competition, difficulty
    """
    params = {
        'type': 'domain_organic',
        'display_limit': limit,
        'export_columns': 'Ph,Po,Nq,Cp,Ur,Tr,Tc,Co,Kd',
        'domain': domain,
        'database': db,
    }

    rows = _parse_response(_request(params))
    results = []
    for row in rows:
        results.append({
            'keyword': row.get('Keyword', ''),
            'position': _safe_int(row.get('Position', '0')),
            'volume': _safe_int(row.get('Search Volume', '0')),
            'cpc': _safe_float(row.get('CPC', '0')),
            'url': row.get('Url', ''),
            'traffic_pct': _safe_float(row.get('Traffic (%)', '0')),
            'traffic_cost': _safe_float(row.get('Traffic Cost (%)', '0')),
            'competition': _safe_float(row.get('Competition', '0')),
            'difficulty': _safe_int(row.get('Keyword Difficulty', '0')),
        })
    return results


def get_domain_competitors(domain, db='us', limit=10):
    """
    Get organic competitors sharing keyword overlap.

    Args:
        domain: Domain to analyze
        db: Database/country code
        limit: Max competitors to return

    Returns:
        list of dicts with domain, common_keywords, organic_keywords,
        organic_traffic, organic_cost
    """
    params = {
        'type': 'domain_organic_organic',
        'display_limit': limit,
        'export_columns': 'Dn,Cr,Np,Or,Ot,Oc,Ad',
        'domain': domain,
        'database': db,
    }

    rows = _parse_response(_request(params))
    results = []
    for row in rows:
        results.append({
            'domain': row.get('Domain', ''),
            'common_keywords': _safe_int(row.get('Common Keywords', '0')),
            'se_keywords': _safe_int(row.get('Organic Keywords', '0')),
            'organic_keywords': _safe_int(row.get('Organic Keywords', '0')),
            'organic_traffic': _safe_int(row.get('Organic Traffic', '0')),
            'organic_cost': _safe_float(row.get('Organic Cost', '0')),
            'paid_keywords': _safe_int(row.get('Adwords Keywords', '0')),
        })
    return results


def get_backlink_overview(domain):
    """
    Get backlink profile summary for a domain.

    Args:
        domain: Domain to analyze

    Returns:
        dict with total_backlinks, referring_domains, referring_urls, etc.
    """
    # Backlinks API uses a separate base URL
    params = {
        'type': 'backlinks_overview',
        'target': domain,
        'target_type': 'root_domain',
        'export_columns': 'total,domains_num,urls_num,ips_num,follows_num,nofollows_num,texts_num,images_num',
        'key': SEMRUSH_API_KEY,
    }

    try:
        resp = requests.get('https://api.semrush.com/analytics/v1/', params=params, timeout=30)
        if resp.status_code != 200:
            # Backlinks may not be available on all SEMrush plans
            return {'domain': domain, 'error': f'Backlinks API unavailable (HTTP {resp.status_code})'}
        raw = resp.text
    except Exception as e:
        return {'domain': domain, 'error': str(e)}

    rows = _parse_response(raw)
    if not rows:
        return {'domain': domain, 'error': 'No data returned'}

    row = rows[0]
    return {
        'domain': domain,
        'total_backlinks': _safe_int(row.get('total', '0')),
        'referring_domains': _safe_int(row.get('domains_num', '0')),
        'referring_urls': _safe_int(row.get('urls_num', '0')),
        'referring_ips': _safe_int(row.get('ips_num', '0')),
        'follow_links': _safe_int(row.get('follows_num', '0')),
        'nofollow_links': _safe_int(row.get('nofollows_num', '0')),
        'text_links': _safe_int(row.get('texts_num', '0')),
        'image_links': _safe_int(row.get('images_num', '0')),
    }


def get_keyword_overview(keyword, db='us'):
    """
    Get search metrics for a specific keyword.

    Args:
        keyword: Keyword phrase to look up
        db: Database/country code

    Returns:
        dict with keyword, volume, cpc, competition, results, trend
    """
    params = {
        'type': 'phrase_this',
        'phrase': keyword,
        'export_columns': 'Ph,Nq,Cp,Co,Nr,Td',
        'database': db,
    }

    rows = _parse_response(_request(params))
    if not rows:
        return {'keyword': keyword, 'error': 'No data returned'}

    row = rows[0]
    return {
        'keyword': row.get('Keyword', keyword),
        'volume': _safe_int(row.get('Search Volume', '0')),
        'cpc': _safe_float(row.get('CPC', '0')),
        'competition': _safe_float(row.get('Competition', '0')),
        'results': _safe_int(row.get('Number of Results', '0')),
        'trend': row.get('Trends', ''),
    }


def generate_report(domains=None):
    """
    Generate a full competitive analysis report for the given domains.
    Calls all analysis functions and formats as markdown.

    Args:
        domains: List of domains to analyze (defaults to PlanWell + competitors)

    Returns:
        str: Markdown-formatted report
    """
    if domains is None:
        domains = ['planwellfp.com', 'stwserve.com', 'hawsfederal.com']

    report_lines = [
        f'# SEMrush Competitive Analysis Report',
        f'**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}',
        f'**Domains:** {", ".join(domains)}',
        '',
        '---',
        '',
    ]

    # --- Domain Overviews ---
    report_lines.append('## Domain Overview Comparison')
    report_lines.append('')
    report_lines.append('| Metric | ' + ' | '.join(domains) + ' |')
    report_lines.append('|--------|' + '|'.join(['--------'] * len(domains)) + '|')

    overviews = {}
    for domain in domains:
        print(f'  Fetching overview for {domain}...')
        overviews[domain] = get_domain_overview(domain)

    metrics = [
        ('SEMrush Rank', 'rank'),
        ('Organic Keywords', 'organic_keywords'),
        ('Organic Traffic', 'organic_traffic'),
        ('Organic Cost ($)', 'organic_cost'),
        ('Paid Keywords', 'paid_keywords'),
        ('Paid Traffic', 'paid_traffic'),
        ('Paid Cost ($)', 'paid_cost'),
    ]

    for label, key in metrics:
        values = []
        for domain in domains:
            val = overviews[domain].get(key, 'N/A')
            if isinstance(val, float):
                values.append(f'${val:,.2f}' if 'cost' in key.lower() else f'{val:,.2f}')
            elif isinstance(val, int):
                values.append(f'{val:,}')
            else:
                values.append(str(val))
        report_lines.append(f'| {label} | ' + ' | '.join(values) + ' |')

    report_lines.append('')

    # --- Organic Keywords per Domain ---
    for domain in domains:
        report_lines.append(f'## Top Organic Keywords: {domain}')
        report_lines.append('')

        print(f'  Fetching keywords for {domain}...')
        keywords = get_organic_keywords(domain, limit=20)

        if keywords:
            report_lines.append('| Keyword | Pos | Volume | CPC | Difficulty |')
            report_lines.append('|---------|-----|--------|-----|------------|')
            for kw in keywords:
                report_lines.append(
                    f'| {kw["keyword"]} | {kw["position"]} | '
                    f'{kw["volume"]:,} | ${kw["cpc"]:.2f} | {kw["difficulty"]} |'
                )
        else:
            report_lines.append('*No keyword data available.*')

        report_lines.append('')

    # --- Competitors for Primary Domain ---
    primary = domains[0]
    report_lines.append(f'## Organic Competitors: {primary}')
    report_lines.append('')

    print(f'  Fetching competitors for {primary}...')
    competitors = get_domain_competitors(primary)

    if competitors:
        report_lines.append('| Competitor | Common KWs | Organic KWs | Organic Traffic |')
        report_lines.append('|------------|------------|-------------|-----------------|')
        for comp in competitors:
            report_lines.append(
                f'| {comp["domain"]} | {comp["common_keywords"]:,} | '
                f'{comp["organic_keywords"]:,} | {comp["organic_traffic"]:,} |'
            )
    else:
        report_lines.append('*No competitor data available.*')

    report_lines.append('')

    # --- Backlink Profiles ---
    report_lines.append('## Backlink Profile Comparison')
    report_lines.append('')
    report_lines.append('| Metric | ' + ' | '.join(domains) + ' |')
    report_lines.append('|--------|' + '|'.join(['--------'] * len(domains)) + '|')

    backlinks = {}
    for domain in domains:
        print(f'  Fetching backlinks for {domain}...')
        backlinks[domain] = get_backlink_overview(domain)

    bl_metrics = [
        ('Total Backlinks', 'total_backlinks'),
        ('Referring Domains', 'referring_domains'),
        ('Referring URLs', 'referring_urls'),
        ('Follow Links', 'follow_links'),
        ('Nofollow Links', 'nofollow_links'),
    ]

    for label, key in bl_metrics:
        values = []
        for domain in domains:
            val = backlinks[domain].get(key, 'N/A')
            values.append(f'{val:,}' if isinstance(val, int) else str(val))
        report_lines.append(f'| {label} | ' + ' | '.join(values) + ' |')

    report_lines.append('')

    # --- Key Keyword Research ---
    report_lines.append('## Keyword Research: Key Federal Planning Terms')
    report_lines.append('')

    target_keywords = [
        'federal retirement planning',
        'FERS retirement calculator',
        'TSP withdrawal strategies',
        'federal employee benefits',
        'FEHB retirement',
        'federal sick leave retirement',
    ]

    report_lines.append('| Keyword | Volume | CPC | Competition | Results |')
    report_lines.append('|---------|--------|-----|-------------|---------|')

    for kw in target_keywords:
        print(f'  Researching keyword: {kw}...')
        data = get_keyword_overview(kw)
        if 'error' not in data:
            report_lines.append(
                f'| {data["keyword"]} | {data["volume"]:,} | '
                f'${data["cpc"]:.2f} | {data["competition"]:.2f} | '
                f'{data["results"]:,} |'
            )
        else:
            report_lines.append(f'| {kw} | N/A | N/A | N/A | N/A |')

    report_lines.append('')
    report_lines.append('---')
    report_lines.append(f'*Report generated by semrush_client.py on {datetime.now().strftime("%Y-%m-%d")}*')

    report_text = '\n'.join(report_lines)

    # Save to root .tmp directory
    output_path = Path(__file__).parent.parent.parent / '.tmp' / 'SEMRUSH_REPORT.md'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_text, encoding='utf-8')
    print(f'\nReport saved to: {output_path}')

    return report_text


# --- Helpers ---

def _safe_int(val):
    """Safely convert a string to int, returning 0 on failure."""
    try:
        return int(float(str(val).replace(',', '').strip()))
    except (ValueError, TypeError):
        return 0


def _safe_float(val):
    """Safely convert a string to float, returning 0.0 on failure."""
    try:
        return float(str(val).replace(',', '').strip())
    except (ValueError, TypeError):
        return 0.0


if __name__ == '__main__':
    if not SEMRUSH_API_KEY:
        print('ERROR: SEMRUSH_API_KEY not found in .env')
        sys.exit(1)

    if '--report' in sys.argv:
        print('Generating full competitive analysis report...\n')
        generate_report()

    elif '--quick' in sys.argv:
        print('Quick overview: planwellfp.com\n')
        overview = get_domain_overview('planwellfp.com')
        for k, v in overview.items():
            print(f'  {k}: {v}')

    elif '--domain' in sys.argv:
        idx = sys.argv.index('--domain')
        if idx + 1 < len(sys.argv):
            domain = sys.argv[idx + 1]
            print(f'Deep dive: {domain}\n')

            print('--- Overview ---')
            overview = get_domain_overview(domain)
            for k, v in overview.items():
                print(f'  {k}: {v}')

            print('\n--- Top Keywords ---')
            keywords = get_organic_keywords(domain, limit=20)
            for kw in keywords:
                print(f'  [{kw["position"]}] {kw["keyword"]} '
                      f'(vol: {kw["volume"]}, cpc: ${kw["cpc"]:.2f})')

            print('\n--- Backlinks ---')
            bl = get_backlink_overview(domain)
            for k, v in bl.items():
                print(f'  {k}: {v}')
        else:
            print('Usage: --domain DOMAIN')

    elif '--keyword' in sys.argv:
        idx = sys.argv.index('--keyword')
        if idx + 1 < len(sys.argv):
            keyword = sys.argv[idx + 1]
            print(f'Keyword overview: {keyword}\n')
            data = get_keyword_overview(keyword)
            for k, v in data.items():
                print(f'  {k}: {v}')
        else:
            print('Usage: --keyword "KEYWORD PHRASE"')

    else:
        print('SEMrush API Client')
        print('=' * 40)
        print('Usage:')
        print('  --quick              Domain overview for planwellfp.com')
        print('  --report             Full competitive report (3 domains)')
        print('  --domain DOMAIN      Single domain deep dive')
        print('  --keyword "PHRASE"   Single keyword overview')
