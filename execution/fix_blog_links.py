"""
Fix Internal Blog Links
=========================
Scans articles.ts for <strong>text</strong> patterns that match known article
topics and wraps them in <a href="/slug"> tags.

Rules:
- Only links phrases NOT already inside an <a> tag
- Only links the first occurrence of each phrase per article (avoid link spam)
- Never self-links (won't link to the same article)
- Case-insensitive matching
- Skips CTA phrases like "Reach Out to Us!" and "Sign up for..."

Usage:
    python fix_blog_links.py              # Dry run (shows changes)
    python fix_blog_links.py --apply      # Apply changes to articles.ts
"""

import re
import sys
from pathlib import Path

ARTICLES_PATH = Path(__file__).parent.parent / 'src' / 'data' / 'articles.ts'

# Keyword → slug mapping (ordered by specificity, most specific first)
LINK_MAP = [
    # Pay & Compensation
    ("2026 pay raise", "/2026-federal-pay-raise-1-0-percent"),
    ("2026 federal pay raise", "/2026-federal-pay-raise-1-0-percent"),
    ("federal pay raise", "/2026-federal-pay-raise-1-0-percent"),
    ("GS pay scale", "/2026-gs-pay-scale-table-estimates-after-1-0-federal-pay-raise-announced"),
    ("GS-12 pay scale", "/gs-12-pay-scale-the-complete-salary-guide"),
    ("locality pay", "/2026-federal-employee-pay-raise-update-locality-pay-and-historical-chart"),

    # FERS Pension & Retirement
    ("FERS annuity calculation", "/simplify-your-fers-pension-calculation"),
    ("FERS pension calculation", "/simplify-your-fers-pension-calculation"),
    ("FERS annuity", "/simplify-your-fers-pension-calculation"),
    ("FERS Supplement", "/fers-supplement-warning-federal-retirement-timeline-and-earnings-limits"),
    ("FERS annuity supplement", "/fers-supplement-warning-federal-retirement-timeline-and-earnings-limits"),
    ("special retirement supplement", "/fers-supplement-warning-federal-retirement-timeline-and-earnings-limits"),
    ("high-3 average salary", "/federal-retirement-high-5-off-the-table-calculate-your-high-3-salary"),
    ("high-3 salary", "/federal-retirement-high-5-off-the-table-calculate-your-high-3-salary"),
    ("High-3", "/federal-retirement-high-5-off-the-table-calculate-your-high-3-salary"),
    ("minimum retirement age", "/best-dates-to-retire-from-federal-employee-retirement-system-fers-in-2026"),
    ("best dates to retire", "/best-dates-to-retire-from-federal-employee-retirement-system-fers-in-2026"),
    ("sick leave conversion", "/fers-sick-leave-conversion-chart"),
    ("unused sick leave", "/fers-retirement-information-federal-employees-unused-sick-leave"),
    ("survivor benefits", "/survivor-benefits-how-widows-can-claim-social-security-benefits"),

    # TSP
    ("TSP contribution limit", "/tsp-and-401k-plan-tax-change-new-rule-for-catch-up-contributions"),
    ("Roth TSP", "/roth-tsp-is-this-federal-retirement-account-right-for-you"),
    ("TSP rollover", "/tsp-rollover-how-to-transfer-thrift-savings-plan-to-ira"),
    ("TSP withdrawal", "/thrift-savings-plan-tsp-calculator-taxes-and-withdrawals-in-retirement"),
    ("C Fund", "/tsp-talk-c-fund-return-thrift-savings-plan-investment-outlook"),
    ("Thrift Savings Plan", "/thrift-savings-plan-top-10-tsp-mistakes-federal-employees-make"),

    # FEHB & Health
    ("FEHB premium", "/2026-fehb-premiums-increased-rates-for-federal-employee-health-benefits"),
    ("FEHB open season", "/fehb-open-season-health-benefits-mistakes-for-federal-employees-to-avoid"),
    ("FEHB and Medicare", "/maximizing-your-retirement-benefits-with-fehb-and-medicare"),
    ("IRMAA", "/2026-irmaa-brackets-anticipated-changes-to-medicare-costs"),

    # COLA & Adjustments
    ("2026 COLA", "/2026-fers-cola-cost-of-living-adjustment-for-federal-pensions"),
    ("COLA adjustment", "/2026-fers-cola-cost-of-living-adjustment-for-federal-pensions"),
    ("cost-of-living adjustment", "/2026-fers-cola-cost-of-living-adjustment-for-federal-pensions"),

    # Other
    ("backdoor Roth", "/demystifying-the-backdoor-roth-ira-a-strategic-guide"),
    ("Roth conversion", "/roth-conversion-guide-for-2024-tax-year-conversion-rules-for-roth-ira"),
    ("OPM backlog", "/opm-retirement-processing-time-backlog-august-2025"),
    ("return to office", "/federal-employees-the-end-of-remote-work-and-managing-return-to-office"),
    ("Schedule F", "/schedule-f-positions-trump-executive-order-impact-on-federal-employees"),
    ("government shutdown", "/guide-for-feds-how-federal-employees-can-prepare-for-a-government-shutdown"),
]

# Phrases to skip (CTAs, generic text)
SKIP_PHRASES = [
    "reach out to us",
    "sign up for",
    "contact us",
    "schedule a call",
    "book a call",
    "click here",
    "learn more",
]


def is_already_linked(content, match_start, match_end):
    """Check if a match is already inside an <a> tag."""
    # Look backward for an unclosed <a tag
    before = content[:match_start]
    last_a_open = before.rfind('<a ')
    last_a_close = before.rfind('</a>')

    if last_a_open > last_a_close:
        # We're inside an <a> tag
        return True
    return False


def process_article(slug, content):
    """Process a single article's content and add internal links."""
    changes = []
    linked_slugs = set()  # Track which target slugs we've already linked to

    for phrase, target_slug in LINK_MAP:
        # Don't self-link
        if target_slug.strip('/') == slug:
            continue

        # Only link each target once per article
        if target_slug in linked_slugs:
            continue

        # Skip CTA-like phrases
        if any(skip.lower() in phrase.lower() for skip in SKIP_PHRASES):
            continue

        # Find <strong>phrase</strong> pattern (case-insensitive)
        pattern = re.compile(
            r'<strong>(' + re.escape(phrase) + r'[^<]*?)</strong>',
            re.IGNORECASE
        )

        for match in pattern.finditer(content):
            start = match.start()
            end = match.end()
            matched_text = match.group(1)

            # Skip if already linked
            if is_already_linked(content, start, end):
                continue

            # Create replacement
            replacement = f'<a href="{target_slug}"><strong>{matched_text}</strong></a>'
            content = content[:start] + replacement + content[end:]

            changes.append({
                'phrase': matched_text,
                'target': target_slug,
                'article': slug,
            })
            linked_slugs.add(target_slug)
            break  # Only first occurrence per phrase

    return content, changes


def main():
    apply_changes = '--apply' in sys.argv

    # Read the file
    text = ARTICLES_PATH.read_text(encoding='utf-8')

    all_changes = []

    # Find all article content blocks
    # Pattern: 'slug-name': { ... content: `...` ... }
    article_pattern = re.compile(
        r"'([a-z0-9-]+)':\s*\{[^}]*?content:\s*`(.*?)`",
        re.DOTALL
    )

    new_text = text
    offset = 0  # Track offset as we make replacements

    for match in article_pattern.finditer(text):
        slug = match.group(1)
        original_content = match.group(2)

        new_content, changes = process_article(slug, original_content)

        if changes:
            all_changes.extend(changes)

            if apply_changes:
                # Calculate position with offset
                content_start = match.start(2) + offset
                content_end = match.end(2) + offset

                new_text = new_text[:content_start] + new_content + new_text[content_end:]
                offset += len(new_content) - len(original_content)

    # Report
    print(f"\n{'='*60}")
    print(f"Internal Blog Link Fixer")
    print(f"{'='*60}")
    print(f"\nFound {len(all_changes)} linkable phrases across articles:\n")

    for i, change in enumerate(all_changes[:30], 1):
        print(f"  {i}. [{change['article']}]")
        print(f"     \"{change['phrase']}\" → {change['target']}")

    if len(all_changes) > 30:
        print(f"\n  ... and {len(all_changes) - 30} more")

    print(f"\nTotal: {len(all_changes)} links to add")

    if apply_changes:
        ARTICLES_PATH.write_text(new_text, encoding='utf-8')
        print(f"\nChanges applied to {ARTICLES_PATH}")
    else:
        print(f"\nDry run — use --apply to write changes")


if __name__ == '__main__':
    main()
