#!/usr/bin/env python3
"""
Build a Google Search Console disavow file from SEMrush referring-domain data.

Inputs:
    .tmp/planwellfp_refdomains.csv    (from semrush_client get_backlinks_refdomains)
    Downloads/Latest Links Apr 22 2026.csv   (recent crawl list, optional)

Output:
    .tmp/disavow-planwellfp.txt       (submit to Google via GSC Disavow Tool)
    .tmp/disavow-review.csv           (human-readable audit with reason codes)

Heuristics (domains flagged as toxic):
  - Authority score <= 5 (bottom tier; almost always scraper/PBN/spam)
  - Known spam-platform TLDs or hostnames (gridinsoft, buzzfile scrapers, etc.)
  - Non-English or geo-mismatched domains with low-authority (US federal audience)
  - Auto-generated "tool" sites (online virus scanners, domain lookup farms)
  - Adult, gambling, pharma spam signatures

Anything flagged "review" is NOT disavowed automatically; human review first.
Things flagged "disavow" are added to the disavow file.

Usage:
    python3 disavow_file_builder.py
"""

import csv
import re
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
REFDOMAINS_CSV = PROJECT_DIR / '.tmp' / 'planwellfp_refdomains.csv'
LATEST_LINKS_CSV = Path.home() / 'Downloads' / 'Latest Links Apr 22 2026.csv'
DISAVOW_FILE = PROJECT_DIR / '.tmp' / 'disavow-planwellfp.txt'
REVIEW_FILE = PROJECT_DIR / '.tmp' / 'disavow-review.csv'

# Hard-disavow patterns: exact substrings that indicate spam
SPAM_SUBSTRINGS = [
    'gridinsoft.com',
    'online-virus-scanner',
    'domain.glass',
    'buzzfile.com',
    'sur.ly',
    'similarweb.com/similar-sites',
    'statscrop',
    'woorank.com',
    'hypestat',
    'ecologialoja.com.br',
    'barcelonadesignweek',
    'assurances.gov.gh',
    'xuandyeh',
    'edu.dmz',
    'webstatsdomain',
    'sitelike',
    'siteworthchecker',
    '.cn/',
    '.ru/',
    '.tk',
    '.ga/',
    '.ml/',
    '.cf/',
    '.tokyo',
    '.xyz',
    '.top',
    'casino',
    'poker',
    'viagra',
    'cialis',
    'pharmacy',
    'bitcoin',
    'crypto',
    'nsfw',
    'adult',
    '.porn',
    'seoscore',
    'similar-web-sites',
]

# Domains/patterns to REVIEW but not auto-disavow (might be legit but suspicious)
REVIEW_SUBSTRINGS = [
    'wordpress.com',
    'blogspot.com',
    'medium.com',
    'reddit.com',
    'quora.com',
]


def classify(row):
    """
    Classify a referring domain as 'disavow', 'review', or 'keep'.
    Returns tuple (verdict, reason).

    row keys: domain_ascore, domain, backlinks_num, ip, country, first_seen, last_seen
    """
    domain = row.get('domain', '').lower().strip()
    if not domain:
        return ('keep', 'empty-domain')

    try:
        score = int(row.get('domain_ascore', '0') or '0')
    except ValueError:
        score = 0

    try:
        backlinks = int(row.get('backlinks_num', '0') or '0')
    except ValueError:
        backlinks = 0

    country = (row.get('country', '') or '').lower().strip()

    # 1) Hard spam substring match
    for needle in SPAM_SUBSTRINGS:
        if needle in domain:
            return ('disavow', f'spam-pattern:{needle}')

    # 2) Zero-authority with multiple backlinks = toxic link farm
    if score == 0 and backlinks >= 3:
        return ('disavow', 'zero-authority-multi-backlinks')

    # 3) Bottom-tier authority (<=5) with suspicious country/TLD
    if score <= 5:
        suspicious_tlds = ('.ru', '.cn', '.tk', '.ga', '.ml', '.cf', '.xyz', '.top', '.icu', '.click', '.work', '.live')
        if any(domain.endswith(tld) or tld + '/' in domain for tld in suspicious_tlds):
            return ('disavow', f'low-auth-suspicious-tld:{score}')
        # Non-English country codes + tiny authority often = scraper
        if country and country not in ('us', 'gb', 'ca', 'au'):
            return ('disavow', f'low-auth-geo-mismatch:{country},score={score}')
        # Pure low authority with multiple backlinks
        if backlinks >= 5:
            return ('disavow', f'low-auth-multi-backlinks:score={score}')

    # 4) Review-list patterns
    for needle in REVIEW_SUBSTRINGS:
        if needle in domain and score < 30:
            return ('review', f'review-pattern:{needle}')

    # 5) Authority 6-15, many backlinks, non-US: review
    if 6 <= score <= 15 and backlinks >= 10 and country and country not in ('us', 'gb', 'ca', 'au'):
        return ('review', f'mid-low-auth-geo-mismatch:{country},score={score}')

    return ('keep', f'keep:score={score}')


def extract_recent_spam_hosts():
    """
    Parse the Latest Links CSV and extract unique hostnames of likely spam sources.
    These domains may not be in the refdomains export yet.
    """
    if not LATEST_LINKS_CSV.exists():
        return set()

    spam_hosts = set()
    with open(LATEST_LINKS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if not row:
                continue
            url = row[0].strip().strip('"')
            m = re.match(r'https?://([^/]+)', url)
            if not m:
                continue
            host = m.group(1).lower()
            # Strip "www." and locale subdomains
            host_core = re.sub(r'^(www|de|fr|es|it|nl|pl|ru|ja|sr|cn|kr|tr|ar|he|sv|no)\.', '', host)
            for needle in SPAM_SUBSTRINGS:
                if needle in host_core or needle in host:
                    spam_hosts.add(host_core)
                    break
    return spam_hosts


def main():
    if not REFDOMAINS_CSV.exists():
        print(f'ERROR: refdomains CSV not found at {REFDOMAINS_CSV}')
        print('Run: python3 -c "from semrush_client import get_backlinks_refdomains; get_backlinks_refdomains(\'planwellfp.com\', max_rows=10000, out_csv=\'.tmp/planwellfp_refdomains.csv\')"')
        sys.exit(1)

    print(f'Reading {REFDOMAINS_CSV}')

    disavow_domains = set()
    review_rows = []
    counts = {'disavow': 0, 'review': 0, 'keep': 0}

    with open(REFDOMAINS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            verdict, reason = classify(row)
            counts[verdict] += 1
            row_with_verdict = dict(row)
            row_with_verdict['verdict'] = verdict
            row_with_verdict['reason'] = reason
            review_rows.append(row_with_verdict)
            if verdict == 'disavow':
                disavow_domains.add(row['domain'])

    # Augment with Latest Links spam hosts
    recent_spam = extract_recent_spam_hosts()
    for host in recent_spam:
        if host not in disavow_domains:
            disavow_domains.add(host)
            review_rows.append({
                'domain_ascore': '0',
                'domain': host,
                'backlinks_num': '?',
                'ip': '',
                'country': '',
                'first_seen': '',
                'last_seen': '',
                'verdict': 'disavow',
                'reason': 'recent-spam-from-latest-links',
            })
            counts['disavow'] += 1

    # Write disavow file (Google format)
    DISAVOW_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DISAVOW_FILE, 'w', encoding='utf-8') as f:
        f.write('# PlanWell Financial Planning — disavow file\n')
        f.write(f'# Generated: auto from SEMrush refdomains + recent-links spam patterns\n')
        f.write(f'# Total domains disavowed: {len(disavow_domains)}\n')
        f.write('# Submit via: https://search.google.com/search-console/disavow-links\n')
        f.write('#\n')
        f.write('# Each line is a root domain; Google will disregard all links from the domain and its subdomains.\n')
        f.write('#\n\n')
        for domain in sorted(disavow_domains):
            f.write(f'domain:{domain}\n')

    # Write review CSV
    with open(REVIEW_FILE, 'w', encoding='utf-8', newline='') as f:
        if review_rows:
            writer = csv.DictWriter(f, fieldnames=list(review_rows[0].keys()))
            writer.writeheader()
            writer.writerows(review_rows)

    print()
    print(f'  Disavow: {counts["disavow"]:,} domains')
    print(f'  Review:  {counts["review"]:,} domains (manual check recommended)')
    print(f'  Keep:    {counts["keep"]:,} domains')
    print()
    print(f'  Disavow file: {DISAVOW_FILE}')
    print(f'  Review CSV:   {REVIEW_FILE}')
    print()
    print('Top 20 disavowed domains by reason:')
    reason_counts = {}
    for r in review_rows:
        if r.get('verdict') == 'disavow':
            reason = r.get('reason', 'unknown')
            reason_key = reason.split(':')[0]
            reason_counts[reason_key] = reason_counts.get(reason_key, 0) + 1
    for reason, count in sorted(reason_counts.items(), key=lambda x: -x[1])[:20]:
        print(f'  {count:4d}  {reason}')


if __name__ == '__main__':
    main()
