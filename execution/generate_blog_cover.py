#!/usr/bin/env python3
"""
Blog Cover Photo Generator using Nano Banana Pro (Gemini 3 Pro Image)

Generates natural, clean cover images for blog articles based on their
title and content. Follows the directive at directives/blog_cover_generation.md

Usage:
    # Single article
    python generate_blog_cover.py --slug "article-slug" --title "Article Title" --content "Full content..."

    # Batch mode from JSON
    python generate_blog_cover.py --batch --input articles.json

    # Generate for all WordPress posts
    python generate_blog_cover.py --from-wordpress
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path
from typing import Optional, List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed.")
    print("Run: pip install google-genai python-dotenv")
    sys.exit(1)

# Initialize Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in environment variables")
    print("Add it to your .env file: GEMINI_API_KEY=your_key_here")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

# Output directory for cover images
OUTPUT_DIR = Path(__file__).parent.parent / "public" / "images" / "blog" / "covers"


def analyze_content_for_prompt(title: str, content: str) -> str:
    """
    Use GPT to analyze article content and generate an appropriate image prompt.
    Returns a descriptive prompt for natural, clean imagery.
    """
    # Extract key themes based on common federal retirement topics
    content_lower = (title + " " + content).lower()

    # Determine primary topic
    if any(word in content_lower for word in ["fers", "pension", "annuity", "opm"]):
        topic = "retirement_planning"
    elif any(word in content_lower for word in ["tsp", "thrift", "investing", "401k"]):
        topic = "investing"
    elif any(word in content_lower for word in ["tax", "irs", "deduction"]):
        topic = "tax"
    elif any(word in content_lower for word in ["social security", "ssa", "supplement"]):
        topic = "social_security"
    elif any(word in content_lower for word in ["fehb", "medicare", "health", "insurance"]):
        topic = "healthcare"
    elif any(word in content_lower for word in ["news", "update", "backlog", "opm"]):
        topic = "federal_news"
    else:
        topic = "general_finance"

    # Topic-specific prompt templates (natural, clean aesthetics)
    prompts = {
        "retirement_planning": f"""A peaceful scene of a mature professional enjoying a quiet morning moment,
perhaps looking out a window with soft natural light streaming in. A cup of coffee or tea nearby.
The atmosphere is calm, hopeful, and contemplative - representing the peace of mind that comes
with good retirement planning. Photorealistic, editorial photography style, warm color palette,
shallow depth of field. No text or words in the image.""",

        "investing": f"""A clean, minimalist scene of growth and prosperity - perhaps a healthy plant
on a modern desk near a window with morning sunlight, or a serene sunrise over gentle hills.
The mood is optimistic and forward-looking. Photorealistic, editorial style, natural lighting,
soft warm tones. No text, charts, or numbers visible.""",

        "tax": f"""A organized, calming workspace scene - neat papers, a quality pen, natural light
from a window. The feeling is one of clarity and control, not stress. Perhaps a home office
with plants and comfortable elements. Photorealistic, editorial photography, warm natural light.
No visible text or numbers.""",

        "social_security": f"""A warm, multigenerational scene suggesting family security - perhaps
hands of different ages, or a comfortable home setting with soft afternoon light. The mood is
reassuring and stable. Photorealistic, lifestyle photography style, natural warm tones,
intimate framing. No text in image.""",

        "healthcare": f"""A serene wellness scene - perhaps a peaceful outdoor setting, morning walk,
or comfortable living space with good natural light. The feeling is health, vitality, and
peace of mind. Photorealistic, lifestyle photography, soft natural lighting, calming colors.
No medical imagery or text.""",

        "federal_news": f"""A professional but approachable scene - perhaps the Capitol building or
Washington Monument at golden hour, seen from a distance with beautiful natural lighting.
Or a professional reading materials in a well-lit space. Clean, journalistic feel.
Photorealistic, editorial style. No text or headlines visible.""",

        "general_finance": f"""A scene representing clarity and good planning - perhaps a tidy desk
with natural light, a person looking confidently toward the future, or a peaceful morning
routine. The mood is calm, organized, and optimistic. Photorealistic, editorial photography,
warm natural tones. No text or numbers."""
    }

    base_prompt = prompts.get(topic, prompts["general_finance"])

    # Add article-specific context
    enhanced_prompt = f"""{base_prompt}

This image should evoke the feeling of the article titled: "{title}"
The overall aesthetic should be natural, authentic, and inviting - not corporate or stock-photo-like."""

    return enhanced_prompt


def generate_cover_image(slug: str, title: str, content: str, retry_count: int = 3) -> Optional[str]:
    """
    Generate a cover image for a blog article using Nano Banana Pro.

    Args:
        slug: URL-friendly article identifier
        title: Article title
        content: Article content for context
        retry_count: Number of retries on failure

    Returns:
        Path to saved image, or None on failure
    """
    # Create output directory if needed
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{slug}.png"

    # Generate prompt based on content
    prompt = analyze_content_for_prompt(title, content)

    print(f"Generating cover for: {title}")
    print(f"Slug: {slug}")
    print(f"Prompt preview: {prompt[:200]}...")

    for attempt in range(retry_count):
        try:
            # Use Nano Banana Pro for image generation
            response = client.models.generate_content(
                model="nano-banana-pro-preview",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                ),
            )

            # Extract and save image from response
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    # Data is already raw bytes, write directly
                    # Change extension to match mime type
                    mime_type = part.inline_data.mime_type
                    if 'jpeg' in mime_type or 'jpg' in mime_type:
                        output_path = output_path.with_suffix('.jpg')
                    with open(output_path, 'wb') as f:
                        f.write(part.inline_data.data)
                    print(f"Saved: {output_path} ({len(part.inline_data.data)} bytes)")
                    return str(output_path)

            print(f"Warning: No image in response for {slug}")

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retry_count - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    print(f"Failed to generate cover for: {slug}")
    return None


def batch_generate(articles: List[Dict]) -> Dict:
    """
    Generate covers for multiple articles.

    Args:
        articles: List of dicts with 'slug', 'title', 'content' keys

    Returns:
        Dict mapping slugs to output paths (or None for failures)
    """
    results = {}
    total = len(articles)

    for i, article in enumerate(articles, 1):
        print(f"\n[{i}/{total}] Processing: {article['title'][:50]}...")

        result = generate_cover_image(
            slug=article["slug"],
            title=article["title"],
            content=article.get("content", "")
        )
        results[article["slug"]] = result

        # Rate limiting - be nice to the API
        if i < total:
            time.sleep(2)

    # Summary
    successful = sum(1 for v in results.values() if v is not None)
    print(f"\n{'='*50}")
    print(f"Generation complete: {successful}/{total} successful")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Generate blog cover photos using Nano Banana Pro"
    )
    parser.add_argument("--slug", help="Article slug for single generation")
    parser.add_argument("--title", help="Article title")
    parser.add_argument("--content", help="Article content")
    parser.add_argument("--batch", action="store_true", help="Batch mode")
    parser.add_argument("--input", help="JSON file with articles for batch mode")
    parser.add_argument("--from-wordpress", action="store_true",
                       help="Generate for all WordPress posts")

    args = parser.parse_args()

    if args.batch and args.input:
        # Batch mode from JSON file
        with open(args.input) as f:
            articles = json.load(f)
        batch_generate(articles)

    elif args.from_wordpress:
        # Import WordPress migration module
        try:
            from wordpress_migration import fetch_all_posts, convert_to_article
            posts = fetch_all_posts()
            articles = [convert_to_article(p) for p in posts]
            batch_generate(articles)
        except ImportError:
            print("Error: wordpress_migration.py not found")
            sys.exit(1)

    elif args.slug and args.title:
        # Single article mode
        generate_cover_image(
            slug=args.slug,
            title=args.title,
            content=args.content or ""
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
