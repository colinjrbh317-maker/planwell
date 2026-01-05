"""
Clean article content by removing old website hyperlinks.

This script:
1. Removes all links to planwellfp.com (converts to plain text)
2. Removes hyperlinks wrapping images
3. Preserves the text content

Usage:
    python execution/clean_article_links.py
"""

import re
import os

def clean_article_content(content):
    """Remove old website links and image hyperlinks from article content."""

    # Pattern to match <a> tags with planwellfp.com links
    # Keep the inner text, remove the link
    old_site_pattern = r'<a[^>]*href="https?://(?:www\.)?planwellfp\.com[^"]*"[^>]*>(.*?)</a>'
    content = re.sub(old_site_pattern, r'\1', content, flags=re.IGNORECASE | re.DOTALL)

    # Pattern to match <a> tags wrapping <img> tags (image hyperlinks)
    # Keep the image, remove the link wrapper
    img_link_pattern = r'<a[^>]*>\s*(<img[^>]*>)\s*</a>'
    content = re.sub(img_link_pattern, r'\1', content, flags=re.IGNORECASE | re.DOTALL)

    # Also handle cases where img is followed by text inside the link
    img_link_pattern2 = r'<a[^>]*>(<img[^>]*>.*?)</a>'
    content = re.sub(img_link_pattern2, r'\1', content, flags=re.IGNORECASE | re.DOTALL)

    # Remove promotional/ad images from old website
    # These are typically webinar ads, retirement workshop ads, etc.
    promo_img_patterns = [
        r'<img[^>]*src="[^"]*planwellfp\.com[^"]*(?:Webinar-Ad|Secure-Your-Retirement|Workshop-Ad|Ad-for-Articles)[^"]*"[^>]*(?:/>|>)',
        r'<img[^>]*(?:alt="[^"]*(?:Webinar Ad|Workshop Ad|Click to Register|Click to view)[^"]*")[^>]*src="[^"]*planwellfp\.com[^"]*"[^>]*(?:/>|>)',
    ]
    for pattern in promo_img_patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)

    # Remove any remaining old site images (convert to local fallback or remove)
    # Pattern: img tags with planwellfp.com src
    old_img_pattern = r'<img[^>]*src="https?://(?:www\.)?planwellfp\.com[^"]*"[^>]*(?:/>|>)'
    content = re.sub(old_img_pattern, '', content, flags=re.IGNORECASE)

    # Remove "Sources:" sections that only contain old site URLs
    sources_pattern = r'<p>Sources:</p>\s*<p>https?://(?:www\.)?planwellfp\.com[^<]*</p>'
    content = re.sub(sources_pattern, '', content, flags=re.IGNORECASE)

    # Replace plain text mentions of the old domain with generic reference
    content = re.sub(r'at planwellfp\.com', 'on our website', content, flags=re.IGNORECASE)
    content = re.sub(r'planwellfp\.com', 'our website', content, flags=re.IGNORECASE)

    return content

def process_articles_file(file_path):
    """Process the articles.ts file and clean all article content."""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all content fields and clean them
    # Pattern matches: content: `...`
    def replace_content(match):
        original_content = match.group(1)
        cleaned_content = clean_article_content(original_content)
        return f'content: `{cleaned_content}`'

    content_pattern = r'content: `(.*?)`(?=,?\s*\n\s*\})'
    updated_content = re.sub(content_pattern, replace_content, content, flags=re.DOTALL)

    # Count changes
    old_links_before = len(re.findall(r'href="https?://(?:www\.)?planwellfp\.com', content, re.IGNORECASE))
    old_links_after = len(re.findall(r'href="https?://(?:www\.)?planwellfp\.com', updated_content, re.IGNORECASE))

    print(f"Old website links found: {old_links_before}")
    print(f"Old website links after cleanup: {old_links_after}")
    print(f"Links removed: {old_links_before - old_links_after}")

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f"\nUpdated: {file_path}")

if __name__ == '__main__':
    # Path to articles file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    articles_path = os.path.join(project_dir, 'src', 'data', 'articles.ts')

    if os.path.exists(articles_path):
        process_articles_file(articles_path)
    else:
        print(f"Error: Articles file not found at {articles_path}")
