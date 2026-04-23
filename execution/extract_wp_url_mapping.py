#!/usr/bin/env python3
"""
Extract WordPress URL mapping from the WP SQL backup.

Parses the wp_lz68px0kk1_posts table for every published post/page and
outputs a CSV mapping of old WP URLs to their expected Astro slug.

The output feeds:
  1. vercel.json 301 redirects for canonical consolidation
  2. Backlink reclamation (detecting dead-target backlinks)
  3. Content gap audit (what WP posts weren't migrated)

Usage:
    python3 extract_wp_url_mapping.py

Writes to:
    .tmp/wp_url_mapping.csv     all published WP URLs with migration status
    .tmp/wp_url_mapping.json    structured JSON for other scripts
"""

import json
import os
import re
import sys
import csv
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
SQL_DUMP = PROJECT_DIR / "BACKUP" / "backup.sql"
OUTPUT_CSV = PROJECT_DIR / ".tmp" / "wp_url_mapping.csv"
OUTPUT_JSON = PROJECT_DIR / ".tmp" / "wp_url_mapping.json"
ASTRO_ARTICLES = PROJECT_DIR / "planwell-site" / "src" / "data" / "articles.ts"
ASTRO_PAGES = PROJECT_DIR / "planwell-site" / "src" / "pages"
TABLE_PREFIX = "wp_lz68px0kk1_"

SITE_BASE = "https://www.planwellfp.com"


def parse_sql_values(line):
    """Parse MySQL INSERT INTO ... VALUES (...),(...),... into row strings."""
    values_match = re.search(r'VALUES\s*', line)
    if not values_match:
        return []

    data = line[values_match.end():]
    rows = []
    i = 0

    while i < len(data):
        if data[i] == '(':
            depth = 1
            i += 1
            start = i
            in_string = False
            escape_next = False

            while i < len(data) and depth > 0:
                ch = data[i]
                if escape_next:
                    escape_next = False
                    i += 1
                    continue
                if ch == '\\':
                    escape_next = True
                    i += 1
                    continue
                if ch == "'" and not in_string:
                    in_string = True
                    i += 1
                    continue
                if ch == "'" and in_string:
                    if i + 1 < len(data) and data[i+1] == "'":
                        i += 2
                        continue
                    in_string = False
                    i += 1
                    continue
                if not in_string:
                    if ch == '(':
                        depth += 1
                    elif ch == ')':
                        depth -= 1
                i += 1

            rows.append(data[start:i-1])
        else:
            i += 1

    return rows


def extract_fields(row_str):
    """Extract field values from one row string into a list."""
    fields = []
    i = 0
    while i < len(row_str):
        while i < len(row_str) and row_str[i] in (' ', ','):
            i += 1
        if i >= len(row_str):
            break
        if row_str[i] == "'":
            i += 1
            chars = []
            while i < len(row_str):
                ch = row_str[i]
                if ch == '\\' and i + 1 < len(row_str):
                    nx = row_str[i+1]
                    replacements = {"'": "'", '"': '"', '\\': '\\',
                                    'n': '\n', 'r': '\r', 't': '\t', '0': '\0'}
                    chars.append(replacements.get(nx, nx))
                    i += 2
                    continue
                if ch == "'" and i + 1 < len(row_str) and row_str[i+1] == "'":
                    chars.append("'")
                    i += 2
                    continue
                if ch == "'":
                    i += 1
                    break
                chars.append(ch)
                i += 1
            fields.append(''.join(chars))
        elif row_str[i:i+4] == 'NULL':
            fields.append(None)
            i += 4
        else:
            start = i
            while i < len(row_str) and row_str[i] not in (',', ')'):
                i += 1
            fields.append(row_str[start:i].strip())
    return fields


def load_astro_slugs():
    """Enumerate all Astro routes so we can mark migration status per WP URL."""
    slugs = set()

    # 1) Static .astro pages
    if ASTRO_PAGES.exists():
        for path in ASTRO_PAGES.rglob('*.astro'):
            rel = path.relative_to(ASTRO_PAGES)
            parts = list(rel.parts[:-1])
            stem = rel.stem
            # skip dynamic routes
            if stem.startswith('[') or any(p.startswith('[') for p in parts):
                continue
            if stem == 'index':
                slug = '/' + '/'.join(parts) if parts else '/'
            else:
                slug = '/' + '/'.join(parts + [stem])
            slug = slug.rstrip('/') or '/'
            slugs.add(slug)

    # 2) Blog post slugs from articles.ts (dynamic [slug].astro route)
    if ASTRO_ARTICLES.exists():
        text = ASTRO_ARTICLES.read_text(encoding='utf-8', errors='replace')
        # Match slug: 'xyz' or slug: "xyz"
        for match in re.finditer(r"slug\s*:\s*['\"]([^'\"]+)['\"]", text):
            slug = match.group(1).strip('/')
            if slug:
                slugs.add('/' + slug)

    return slugs


def main():
    if not SQL_DUMP.exists():
        print(f'ERROR: SQL dump not found at {SQL_DUMP}')
        sys.exit(1)

    print(f'Reading {SQL_DUMP} ({SQL_DUMP.stat().st_size / 1024 / 1024:.1f} MB)')
    print(f'Table prefix: {TABLE_PREFIX}')

    # wp_posts columns (in order):
    # ID, post_author, post_date, post_date_gmt, post_content, post_title,
    # post_excerpt, post_status, comment_status, ping_status, post_password,
    # post_name, to_ping, pinged, post_modified, post_modified_gmt,
    # post_content_filtered, post_parent, guid, menu_order, post_type,
    # post_mime_type, comment_count
    POST_NAME_IDX = 11
    POST_STATUS_IDX = 7
    POST_TYPE_IDX = 20
    POST_TITLE_IDX = 5
    POST_DATE_IDX = 2
    POST_ID_IDX = 0

    target_table = f'{TABLE_PREFIX}posts'
    posts = []

    with open(SQL_DUMP, 'r', encoding='utf-8', errors='replace') as f:
        for line_no, line in enumerate(f, 1):
            if not line.startswith('INSERT INTO'):
                continue
            if target_table not in line:
                continue
            for row_str in parse_sql_values(line):
                fields = extract_fields(row_str)
                if len(fields) < 21:
                    continue
                status = fields[POST_STATUS_IDX]
                post_type = fields[POST_TYPE_IDX]
                if status != 'publish':
                    continue
                if post_type not in ('post', 'page'):
                    continue
                slug = fields[POST_NAME_IDX]
                if not slug:
                    continue
                posts.append({
                    'id': fields[POST_ID_IDX],
                    'slug': slug,
                    'post_type': post_type,
                    'title': fields[POST_TITLE_IDX] or '',
                    'date': fields[POST_DATE_IDX] or '',
                })

    print(f'Parsed {len(posts)} published WP posts/pages')

    # Dedupe by slug (posts can be revised and reappear)
    seen = {}
    for p in posts:
        # keep earliest date (original publish)
        if p['slug'] not in seen or p['date'] < seen[p['slug']]['date']:
            seen[p['slug']] = p
    posts = list(seen.values())
    posts.sort(key=lambda p: p['slug'])

    astro_slugs = load_astro_slugs()
    print(f'Found {len(astro_slugs)} Astro routes for cross-reference')

    # Build output rows
    out_rows = []
    missing = 0
    matched = 0
    for p in posts:
        slug = p['slug']
        old_url = f'{SITE_BASE}/{slug}/'
        expected_new = f'/{slug}'
        migration_status = 'migrated' if expected_new in astro_slugs else 'missing'
        if migration_status == 'missing':
            missing += 1
        else:
            matched += 1
        out_rows.append({
            'wp_id': p['id'],
            'slug': slug,
            'post_type': p['post_type'],
            'title': p['title'],
            'wp_date': p['date'],
            'old_url_with_slash': old_url,
            'old_url_www_slash': f'https://www.planwellfp.com/{slug}/',
            'old_url_nonwww_slash': f'https://planwellfp.com/{slug}/',
            'old_url_www_noslash': f'https://www.planwellfp.com/{slug}',
            'old_url_nonwww_noslash': f'https://planwellfp.com/{slug}',
            'expected_astro_slug': expected_new,
            'migration_status': migration_status,
        })

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(out_rows),
            'matched': matched,
            'missing': missing,
            'rows': out_rows,
        }, f, indent=2)

    print()
    print(f'  Migrated to Astro: {matched}')
    print(f'  Missing from Astro: {missing}')
    print(f'  Output CSV: {OUTPUT_CSV}')
    print(f'  Output JSON: {OUTPUT_JSON}')
    print()
    if missing > 0:
        print('Sample of MISSING slugs (not yet migrated):')
        shown = 0
        for r in out_rows:
            if r['migration_status'] == 'missing':
                print(f'  [{r["post_type"]}] {r["slug"]}')
                shown += 1
                if shown >= 20:
                    remaining = missing - shown
                    if remaining > 0:
                        print(f'  ... and {remaining} more')
                    break


if __name__ == '__main__':
    main()
