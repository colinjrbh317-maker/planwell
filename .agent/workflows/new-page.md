---
description: How to add a new page with SEO and performance optimizations
---

# Adding New Pages to PlanWell Website

When adding new pages to the PlanWell site, follow these standards to ensure SEO and performance optimization is applied automatically.

## 1. Page Setup

Create your new page in `src/pages/` using the BaseLayout:

```astro
---
import { Image } from 'astro:assets';
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout 
  title="Your Page Title - Keywords Here"
  description="150-160 character description with primary keywords for SERP display."
>
  <!-- Your page content -->
</BaseLayout>
```

## 2. Required Meta Props

Always include these BaseLayout props:

| Prop | Required | Description |
|------|----------|-------------|
| `title` | Yes | Page title (50-60 chars ideal) - appears in browser tab and SERPs |
| `description` | Yes | Meta description (150-160 chars) - appears in search results |
| `canonical` | No | Override canonical URL if needed (auto-generated from path) |
| `ogImage` | No | Custom OG image path (defaults to /og-default.png) |
| `noindex` | No | Set to true for pages that shouldn't be indexed |

## 3. Image Optimization

Always use Astro's Image component for images:

```astro
import { Image } from 'astro:assets';
import myImage from '../assets/images/my-image.jpg';

<!-- Hero/above-fold images (LCP) -->
<Image 
  src={myImage} 
  alt="Descriptive alt text"
  width={600}
  height={400}
  loading="eager"
  format="webp"
  quality={80}
/>

<!-- Below-fold images -->
<Image 
  src={myImage} 
  alt="Descriptive alt text"
  width={400}
  height={300}
  loading="lazy"
  format="webp"
  quality={85}
/>
```

**Rules:**
- Above-fold images: `loading="eager"` for LCP optimization
- Below-fold images: `loading="lazy"` for performance
- Always use `format="webp"` for optimal compression
- Always specify `width` and `height` to prevent CLS

## 4. Performance Best Practices

- Use `data-animate` for scroll animations (handled by BaseLayout)
- Keep above-fold content minimal for fast FCP
- Avoid large JavaScript bundles
- Inline critical CSS is handled automatically by BaseLayout

## 5. Schema Markup

BaseLayout automatically includes:
- FinancialService schema with service catalog
- WebSite schema
- WebPage schema for current page

For special page types (blog articles, FAQs), consider adding page-specific schema.

## 6. Sitemap

The sitemap is auto-generated at build time by `@astrojs/sitemap`. New pages are included automatically. For priority adjustments, modify `astro.config.mjs`.

// turbo
## 7. Build and Verify

```bash
npm run build
```

Check the build output for any image optimization or SEO warnings.
