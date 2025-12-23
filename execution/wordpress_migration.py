#!/usr/bin/env python3
"""
WordPress to Astro/Sanity Migration Script

Fetches blog posts from the WordPress REST API and prepares them for import
into the PlanWell Astro site and Sanity CMS.

Usage:
    # Fetch and preview posts
    python wordpress_migration.py --preview

    # Export to JSON for Astro
    python wordpress_migration.py --export-json

    # Generate cover images for all posts
    python wordpress_migration.py --generate-covers

    # Full migration (fetch, convert, export)
    python wordpress_migration.py --full
"""

import os
import sys
import json
import re
import argparse
from datetime import datetime
from pathlib import Path
from html import unescape
from typing import Optional
import requests
from dotenv import load_dotenv

load_dotenv()

# WordPress API endpoint
WP_API_URL = "https://www.planwellfp.com/wp-json/wp/v2"

# Output paths
OUTPUT_DIR = Path(__file__).parent.parent / ".tmp"
ARTICLES_OUTPUT = OUTPUT_DIR / "wordpress_articles.json"
ASTRO_DATA_FILE = Path(__file__).parent.parent / "src" / "data" / "articles.ts"


def strip_html(html: str) -> str:
    """Remove HTML tags and decode entities."""
    clean = re.sub(r'<[^>]+>', '', html)
    return unescape(clean).strip()


def html_to_clean_content(html: str) -> str:
    """Convert WordPress HTML to cleaner HTML for rendering."""
    # Remove WordPress-specific classes and attributes
    clean = re.sub(r'\sclass="[^"]*"', '', html)
    clean = re.sub(r'\sstyle="[^"]*"', '', html)
    clean = re.sub(r'\sid="[^"]*"', '', html)

    # Remove empty paragraphs
    clean = re.sub(r'<p>\s*</p>', '', clean)

    # Clean up whitespace
    clean = re.sub(r'\n\s*\n', '\n', clean)

    return clean.strip()


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    slug = text.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')


def fetch_all_posts() -> list[dict]:
    """Fetch all published posts from WordPress REST API."""
    posts = []
    page = 1

    print("Fetching posts from WordPress...")

    while True:
        try:
            response = requests.get(
                f"{WP_API_URL}/posts",
                params={
                    'per_page': 100,
                    'page': page,
                    'status': 'publish',
                    '_embed': True  # Include author, categories, featured media
                },
                timeout=30
            )

            if response.status_code == 400:
                # No more pages
                break

            response.raise_for_status()
            batch = response.json()

            if not batch:
                break

            posts.extend(batch)
            print(f"  Fetched page {page}: {len(batch)} posts")
            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break

    print(f"Total posts fetched: {len(posts)}")
    return posts


def fetch_categories() -> dict[int, str]:
    """Fetch all categories and return id->name mapping."""
    try:
        response = requests.get(
            f"{WP_API_URL}/categories",
            params={'per_page': 100},
            timeout=30
        )
        response.raise_for_status()
        categories = response.json()
        return {cat['id']: cat['name'] for cat in categories}
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return {}


def fetch_authors() -> dict[int, dict]:
    """Fetch all authors and return id->info mapping."""
    try:
        response = requests.get(
            f"{WP_API_URL}/users",
            params={'per_page': 100},
            timeout=30
        )
        response.raise_for_status()
        authors = response.json()
        return {
            author['id']: {
                'name': author['name'],
                'slug': author['slug']
            }
            for author in authors
        }
    except Exception as e:
        print(f"Error fetching authors: {e}")
        return {}


def map_author_to_planwell(wp_author_name: str) -> str:
    """Map WordPress author to PlanWell author slug."""
    name_lower = wp_author_name.lower()

    if 'brennan' in name_lower:
        return 'brennan-rhule'
    elif 'david' in name_lower:
        return 'david-fei'
    elif 'ben' in name_lower or 'derge' in name_lower:
        return 'ben-derge'
    else:
        return 'planwell-team'


# Cover image download directory
COVERS_DIR = Path(__file__).parent.parent / "public" / "images" / "blog" / "covers"


def download_cover_image(url: str, slug: str) -> Optional[str]:
    """Download a cover image from WordPress and save locally."""
    if not url:
        return None

    COVERS_DIR.mkdir(parents=True, exist_ok=True)

    # Determine file extension from URL
    ext = '.jpg'
    if '.png' in url.lower():
        ext = '.png'
    elif '.webp' in url.lower():
        ext = '.webp'

    output_path = COVERS_DIR / f"{slug}{ext}"

    # Skip if already downloaded
    if output_path.exists():
        return f"/images/blog/covers/{slug}{ext}"

    try:
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"  Downloaded: {slug}{ext}")
        return f"/images/blog/covers/{slug}{ext}"
    except Exception as e:
        print(f"  Failed to download {slug}: {e}")
        return None


def map_category_to_planwell(wp_category: str) -> str:
    """Map WordPress category to PlanWell category."""
    category_mapping = {
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
    for key, value in category_mapping.items():
        if key in cat_lower:
            return value

    return 'FERS'  # Default


def estimate_read_time(content: str) -> str:
    """Estimate read time based on word count."""
    words = len(strip_html(content).split())
    minutes = max(1, round(words / 200))  # Assuming 200 WPM
    return f"{minutes} min read"


def fetch_media_url(media_id: int) -> str:
    """Fetch media URL by ID from WordPress API."""
    if not media_id:
        return ''
    try:
        response = requests.get(
            f"{WP_API_URL}/media/{media_id}",
            timeout=15
        )
        if response.status_code == 200:
            media = response.json()
            return media.get('source_url', '')
    except Exception:
        pass
    return ''


def convert_to_article(wp_post: dict, categories: dict, authors: dict) -> dict:
    """Convert WordPress post to PlanWell article format."""
    # Extract embedded data
    embedded = wp_post.get('_embedded', {})

    # Get author - try embedded first, fallback to authors dict
    wp_author_name = ''
    wp_authors = embedded.get('author', [])
    if wp_authors and isinstance(wp_authors[0], dict):
        wp_author_name = wp_authors[0].get('name', '')

    # Fallback: use author ID lookup if embedded didn't work
    if not wp_author_name:
        author_id = wp_post.get('author')
        if author_id and author_id in authors:
            wp_author_name = authors[author_id].get('name', 'PlanWell Team')
        else:
            wp_author_name = 'PlanWell Team'

    # Get category - try embedded first, fallback to categories dict
    wp_terms = embedded.get('wp:term', [[]])
    wp_categories = wp_terms[0] if wp_terms else []
    if wp_categories and isinstance(wp_categories[0], dict):
        wp_category = wp_categories[0].get('name', 'FERS')
    else:
        # Fallback to category ID lookup
        cat_ids = wp_post.get('categories', [])
        wp_category = categories.get(cat_ids[0], 'FERS') if cat_ids else 'FERS'

    # Get featured image - try embedded first, fallback to direct fetch
    featured_image = ''
    wp_media = embedded.get('wp:featuredmedia', [])
    if wp_media and isinstance(wp_media[0], dict):
        featured_image = wp_media[0].get('source_url', '')

    # Fallback: fetch media URL directly if embedded didn't work
    if not featured_image:
        media_id = wp_post.get('featured_media', 0)
        if media_id:
            featured_image = fetch_media_url(media_id)

    # Parse date
    published_date = wp_post.get('date', '')
    if published_date:
        try:
            dt = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
            formatted_date = dt.strftime('%B %d, %Y')
        except:
            formatted_date = published_date[:10]
    else:
        formatted_date = 'Unknown'

    # Get content
    content_html = wp_post.get('content', {}).get('rendered', '')
    clean_content = html_to_clean_content(content_html)

    # Build article
    return {
        'slug': wp_post.get('slug', slugify(wp_post.get('title', {}).get('rendered', ''))),
        'title': strip_html(wp_post.get('title', {}).get('rendered', 'Untitled')),
        'excerpt': strip_html(wp_post.get('excerpt', {}).get('rendered', ''))[:200],
        'content': clean_content,
        'category': map_category_to_planwell(wp_category),
        'author': map_author_to_planwell(wp_author_name),
        'authorDisplay': wp_author_name,
        'date': formatted_date,
        'dateISO': published_date,
        'readTime': estimate_read_time(content_html),
        'featuredImage': featured_image,
        'wpId': wp_post.get('id'),
    }


def export_to_json(articles: list[dict], output_path: Path) -> None:
    """Export articles to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(articles)} articles to {output_path}")


def generate_articles_ts(articles: list[dict]) -> str:
    """Generate TypeScript code for articles.ts."""
    ts_code = '''// Article data migrated from WordPress
// Generated by wordpress_migration.py

import type { Author } from './authors';
import { getAuthorByName } from './authors';

export interface Article {
  slug: string;
  title: string;
  excerpt: string;
  content: string;
  category: string;
  author: string;
  authorDisplay: string;
  date: string;
  readTime: string;
  image: string;
}

export const articles: Record<string, Article> = {
'''

    for article in articles:
        # Escape content for TypeScript string
        content_escaped = article['content'].replace('`', '\\`').replace('${', '\\${')
        excerpt_escaped = article['excerpt'].replace("'", "\\'").replace('\n', ' ')
        title_escaped = article['title'].replace("'", "\\'")

        # Use local image path if downloaded, otherwise construct from slug
        if article.get('localImage'):
            image_path = article['localImage']
        else:
            # Determine extension from featured image URL
            feat_img = article.get('featuredImage', '')
            if '.png' in feat_img.lower():
                ext = '.png'
            elif '.webp' in feat_img.lower():
                ext = '.webp'
            else:
                ext = '.jpg'
            image_path = f"/images/blog/covers/{article['slug']}{ext}"

        ts_code += f'''  '{article["slug"]}': {{
    slug: '{article["slug"]}',
    title: '{title_escaped}',
    excerpt: '{excerpt_escaped}',
    category: '{article["category"]}',
    author: '{article["author"]}',
    authorDisplay: '{article["authorDisplay"]}',
    date: '{article["date"]}',
    readTime: '{article["readTime"]}',
    image: '{image_path}',
    content: `{content_escaped}`
  }},
'''

    ts_code += '''}

export function getArticleSlugs(): string[] {
  return Object.keys(articles);
}

export function getArticle(slug: string): Article | undefined {
  return articles[slug];
}

export function getArticlesByCategory(category: string): Article[] {
  return Object.values(articles).filter(a => a.category === category);
}

export function getArticlesByAuthor(authorSlug: string): Article[] {
  return Object.values(articles).filter(a => a.author === authorSlug);
}

export function getRecentArticles(limit: number = 6): Article[] {
  return Object.values(articles).slice(0, limit);
}
'''

    return ts_code


def preview_posts(posts: list[dict], categories: dict, authors: dict) -> None:
    """Print a preview of fetched posts."""
    print("\n" + "="*60)
    print("WORDPRESS POSTS PREVIEW")
    print("="*60)

    for i, post in enumerate(posts[:10], 1):
        article = convert_to_article(post, categories, authors)
        print(f"\n{i}. {article['title']}")
        print(f"   Slug: {article['slug']}")
        print(f"   Category: {article['category']}")
        print(f"   Author: {article['authorDisplay']} -> {article['author']}")
        print(f"   Date: {article['date']}")
        print(f"   Read Time: {article['readTime']}")
        print(f"   Excerpt: {article['excerpt'][:100]}...")

    if len(posts) > 10:
        print(f"\n... and {len(posts) - 10} more posts")


def download_all_covers(articles: list[dict]) -> dict:
    """Download all cover images from WordPress."""
    print("\nDownloading cover images from WordPress...")
    results = {}
    total = len(articles)

    for i, article in enumerate(articles, 1):
        if article.get('featuredImage'):
            local_path = download_cover_image(article['featuredImage'], article['slug'])
            if local_path:
                results[article['slug']] = local_path
                article['localImage'] = local_path

        if i % 50 == 0:
            print(f"  Progress: {i}/{total}")

    print(f"Downloaded {len(results)} cover images")
    return results


def main():
    parser = argparse.ArgumentParser(description="WordPress to PlanWell migration")
    parser.add_argument("--preview", action="store_true", help="Preview fetched posts")
    parser.add_argument("--export-json", action="store_true", help="Export to JSON")
    parser.add_argument("--export-ts", action="store_true", help="Export to TypeScript")
    parser.add_argument("--download-covers", action="store_true", help="Download cover images from WordPress")
    parser.add_argument("--generate-covers", action="store_true", help="Generate cover images with AI")
    parser.add_argument("--full", action="store_true", help="Full migration with WordPress covers")

    args = parser.parse_args()

    if not any([args.preview, args.export_json, args.export_ts, args.download_covers, args.generate_covers, args.full]):
        parser.print_help()
        return

    # Fetch data
    posts = fetch_all_posts()
    categories = fetch_categories()
    authors = fetch_authors()

    if not posts:
        print("No posts found. Check if the WordPress API is accessible.")
        return

    # Convert all posts
    articles = [convert_to_article(p, categories, authors) for p in posts]

    if args.preview or args.full:
        preview_posts(posts, categories, authors)

    # Download covers from WordPress (preferred method)
    if args.download_covers or args.full:
        download_all_covers(articles)

    if args.export_json or args.full:
        export_to_json(articles, ARTICLES_OUTPUT)

    if args.export_ts or args.full:
        ts_code = generate_articles_ts(articles)
        ASTRO_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(ASTRO_DATA_FILE, 'w', encoding='utf-8') as f:
            f.write(ts_code)
        print(f"Exported TypeScript to {ASTRO_DATA_FILE}")

    if args.generate_covers:
        # Import and run cover generation (only if explicitly requested)
        try:
            from generate_blog_cover import batch_generate

            cover_articles = [
                {'slug': a['slug'], 'title': a['title'], 'content': a['content']}
                for a in articles
            ]
            batch_generate(cover_articles)
        except ImportError:
            print("Error: generate_blog_cover.py not found")
            print("Run cover generation separately after migration")


if __name__ == "__main__":
    main()
