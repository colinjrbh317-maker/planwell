#!/usr/bin/env python3
"""
Incremental WordPress to Astro Migration

Fetches all published posts from the WordPress REST API, compares slugs against
the existing articles.ts, and adds only the missing articles.

Usage:
    python migrate_missing_articles.py              # Dry run (shows missing articles)
    python migrate_missing_articles.py --apply      # Apply: download covers + update articles.ts
"""

import os
import re
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from html import unescape
from typing import Optional
import requests
from dotenv import load_dotenv

load_dotenv()

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
ARTICLES_TS = PROJECT_DIR / "src" / "data" / "articles.ts"
COVERS_DIR = PROJECT_DIR / "public" / "images" / "blog" / "covers"
TMP_DIR = PROJECT_DIR.parent / ".tmp"

# WordPress API
WP_API_URL = "https://www.planwellfp.com/wp-json/wp/v2"


def strip_html(html: str) -> str:
    """Remove HTML tags and decode entities."""
    clean = re.sub(r'<[^>]+>', '', html)
    return unescape(clean).strip()


def clean_content(html: str) -> str:
    """Convert WordPress HTML to clean HTML (strip classes, styles, IDs)."""
    clean = re.sub(r'\sclass="[^"]*"', '', html)
    clean = re.sub(r'\sstyle="[^"]*"', '', clean)
    clean = re.sub(r'\sid="[^"]*"', '', clean)
    clean = re.sub(r'\sdata-[a-z_-]+="[^"]*"', '', clean)
    clean = re.sub(r'<p>\s*</p>', '', clean)
    clean = re.sub(r'<div>\s*</div>', '', clean)
    clean = re.sub(r'\n\s*\n', '\n', clean)
    return clean.strip()


def get_existing_slugs() -> set:
    """Parse existing article slugs from articles.ts."""
    content = ARTICLES_TS.read_text(encoding='utf-8')
    # Match the top-level keys in the articles object: '  'slug-here': {'
    slugs = re.findall(r"^\s+'([a-z0-9-]+)':\s*\{", content, re.MULTILINE)
    return set(slugs)


def fetch_all_wp_posts() -> list[dict]:
    """Fetch all published posts from WordPress REST API."""
    posts = []
    page = 1

    print("Fetching posts from WordPress API...")

    while True:
        try:
            response = requests.get(
                f"{WP_API_URL}/posts",
                params={
                    'per_page': 100,
                    'page': page,
                    'status': 'publish',
                    '_embed': '',
                },
                timeout=30,
            )

            if response.status_code == 400:
                break

            response.raise_for_status()
            batch = response.json()

            if not batch:
                break

            posts.extend(batch)
            print(f"  Page {page}: {len(batch)} posts")
            page += 1

        except requests.exceptions.RequestException as e:
            print(f"  Error fetching page {page}: {e}")
            break

    print(f"  Total WordPress posts: {len(posts)}")
    return posts


def map_author(wp_author_name: str) -> tuple[str, str]:
    """Map WordPress author to PlanWell slug and display name."""
    name_lower = wp_author_name.lower()

    if 'brennan' in name_lower:
        return 'brennan-rhule', 'Brennan Rhule, CFP\u00ae, ChFEBC\u2120, AIF\u00ae'
    elif 'david' in name_lower:
        return 'david-fei', 'David Fei, CFP\u00ae, ChFEBC\u2120, AIF\u00ae'
    elif 'ben' in name_lower or 'derge' in name_lower:
        return 'ben-derge', 'Ben Derge'
    else:
        return 'planwell-team', 'PlanWell Team'


def map_category(wp_category: str) -> str:
    """Map WordPress category to PlanWell category."""
    mapping = {
        'fers': 'FERS',
        'tsp': 'TSP & Investing',
        'fehb': 'FEHB & Medicare',
        'medicare': 'FEHB & Medicare',
        'social security': 'Social Security',
        'tax': 'Tax Strategy',
        'fegli': 'FEGLI & Life Insurance',
        'news': 'Federal News',
        'federal': 'Federal News',
    }

    cat_lower = wp_category.lower()
    for key, value in mapping.items():
        if key in cat_lower:
            return value

    return 'FERS'


def estimate_read_time(content: str) -> str:
    """Estimate read time from word count (200 WPM)."""
    words = len(strip_html(content).split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"


def download_cover(url: str, slug: str) -> Optional[str]:
    """Download cover image from WordPress, return local path."""
    if not url:
        return None

    COVERS_DIR.mkdir(parents=True, exist_ok=True)

    ext = '.jpg'
    if '.png' in url.lower():
        ext = '.png'
    elif '.webp' in url.lower():
        ext = '.webp'

    output_path = COVERS_DIR / f"{slug}{ext}"

    if output_path.exists():
        print(f"    Cover exists: {slug}{ext}")
        return f"/images/blog/covers/{slug}{ext}"

    try:
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"    Downloaded: {slug}{ext}")
        return f"/images/blog/covers/{slug}{ext}"
    except Exception as e:
        print(f"    Failed to download cover for {slug}: {e}")
        return None


def convert_wp_post(wp_post: dict) -> dict:
    """Convert a WordPress post to PlanWell article format."""
    embedded = wp_post.get('_embedded', {})

    # Author
    wp_author_name = ''
    wp_authors = embedded.get('author', [])
    if wp_authors and isinstance(wp_authors[0], dict):
        wp_author_name = wp_authors[0].get('name', '')
    if not wp_author_name:
        wp_author_name = 'PlanWell Team'

    author_slug, author_display = map_author(wp_author_name)

    # Category — check all categories, pick most specific (skip generic "Fed Employee")
    wp_terms = embedded.get('wp:term', [[]])
    wp_categories = wp_terms[0] if wp_terms else []
    category = 'FERS'  # default
    if wp_categories:
        for cat_obj in wp_categories:
            if isinstance(cat_obj, dict):
                cat_name = cat_obj.get('name', '')
                if cat_name.lower() not in ('fed employee', 'uncategorized', ''):
                    category = map_category(cat_name)
                    break

    # Featured image URL
    featured_image = ''
    wp_media = embedded.get('wp:featuredmedia', [])
    if wp_media and isinstance(wp_media[0], dict):
        featured_image = wp_media[0].get('source_url', '')

    # Date
    published_date = wp_post.get('date', '')
    if published_date:
        try:
            dt = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
            formatted_date = dt.strftime('%B %d, %Y')
        except Exception:
            formatted_date = published_date[:10]
    else:
        formatted_date = 'Unknown'

    # Content
    content_html = wp_post.get('content', {}).get('rendered', '')
    cleaned = clean_content(content_html)

    # Title and excerpt
    title = strip_html(wp_post.get('title', {}).get('rendered', 'Untitled'))
    excerpt = strip_html(wp_post.get('excerpt', {}).get('rendered', ''))[:200]

    slug = wp_post.get('slug', '')

    return {
        'slug': slug,
        'title': title,
        'excerpt': excerpt,
        'content': cleaned,
        'category': category,
        'author': author_slug,
        'authorDisplay': author_display,
        'date': formatted_date,
        'readTime': estimate_read_time(content_html),
        'featuredImage': featured_image,
    }


def escape_ts_string(s: str) -> str:
    """Escape a string for TypeScript single-quoted string."""
    return s.replace("\\", "\\\\").replace("'", "\\'").replace('\n', ' ')


def escape_ts_template(s: str) -> str:
    """Escape a string for TypeScript template literal."""
    return s.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')


def generate_ts_entries(articles: list[dict]) -> str:
    """Generate TypeScript entry strings for the articles."""
    entries = []

    for article in articles:
        image = article.get('localImage', f"/images/blog/covers/{article['slug']}.jpg")

        entry = f"""  '{article["slug"]}': {{
    slug: '{article["slug"]}',
    title: '{escape_ts_string(article["title"])}',
    excerpt: '{escape_ts_string(article["excerpt"])}',
    category: '{article["category"]}',
    author: '{article["author"]}',
    authorDisplay: '{escape_ts_string(article["authorDisplay"])}',
    date: '{article["date"]}',
    readTime: '{article["readTime"]}',
    image: '{image}',
    content: `{escape_ts_template(article["content"])}`
  }},"""
        entries.append(entry)

    return '\n'.join(entries)


def insert_into_articles_ts(new_entries_ts: str) -> None:
    """Insert new article entries at the top of the articles object in articles.ts."""
    content = ARTICLES_TS.read_text(encoding='utf-8')

    # Find the opening of the articles object
    marker = "export const articles: Record<string, Article> = {\n"
    idx = content.find(marker)
    if idx == -1:
        print("ERROR: Could not find articles object in articles.ts")
        sys.exit(1)

    insert_pos = idx + len(marker)

    new_content = content[:insert_pos] + new_entries_ts + '\n' + content[insert_pos:]

    ARTICLES_TS.write_text(new_content, encoding='utf-8')
    print(f"  Updated articles.ts")


def main():
    parser = argparse.ArgumentParser(description="Incremental WordPress migration")
    parser.add_argument("--apply", action="store_true", help="Apply changes (download covers + update articles.ts)")
    args = parser.parse_args()

    # Step 1: Get existing slugs
    print("\n=== Step 1: Reading existing articles.ts ===")
    existing_slugs = get_existing_slugs()
    print(f"  Existing articles: {len(existing_slugs)}")

    # Step 2: Fetch all WordPress posts
    print("\n=== Step 2: Fetching WordPress posts ===")
    wp_posts = fetch_all_wp_posts()

    if not wp_posts:
        print("ERROR: No posts fetched from WordPress. Check API accessibility.")
        sys.exit(1)

    # Step 3: Find missing articles
    print("\n=== Step 3: Computing diff ===")
    missing_posts = []
    for post in wp_posts:
        slug = post.get('slug', '')
        if slug and slug not in existing_slugs:
            missing_posts.append(post)

    if not missing_posts:
        print("  No missing articles found! Site is up to date.")
        return

    print(f"  Missing articles: {len(missing_posts)}")

    # Step 4: Convert missing posts
    print("\n=== Step 4: Converting missing posts ===")
    articles = []
    for post in missing_posts:
        article = convert_wp_post(post)
        articles.append(article)
        print(f"  [{article['date']}] {article['title'][:60]}...")
        print(f"    Author: {article['authorDisplay']} -> {article['author']}")
        print(f"    Category: {article['category']} | Read time: {article['readTime']}")

    # Sort by date (newest first)
    articles.sort(key=lambda a: datetime.strptime(a['date'], '%B %d, %Y') if a['date'] != 'Unknown' else datetime.min, reverse=True)

    if not args.apply:
        print(f"\n=== DRY RUN: {len(articles)} articles would be added ===")
        print("Run with --apply to download covers and update articles.ts")
        return

    # Step 5: Download cover images
    print("\n=== Step 5: Downloading cover images ===")
    for article in articles:
        if article.get('featuredImage'):
            local_path = download_cover(article['featuredImage'], article['slug'])
            if local_path:
                article['localImage'] = local_path

    # Step 6: Generate TypeScript and insert
    print("\n=== Step 6: Updating articles.ts ===")
    ts_entries = generate_ts_entries(articles)
    insert_into_articles_ts(ts_entries)

    # Step 7: Summary
    print(f"\n=== Migration Complete ===")
    print(f"  Articles added: {len(articles)}")
    print(f"  Total articles now: {len(existing_slugs) + len(articles)}")

    # Save migration log
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    log_path = TMP_DIR / "migration_log.json"
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'articles_added': len(articles),
        'slugs': [a['slug'] for a in articles],
    }
    with open(log_path, 'w') as f:
        json.dump(log_data, f, indent=2)
    print(f"  Log saved to: {log_path}")


if __name__ == "__main__":
    main()
