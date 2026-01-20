# PlanWell Financial Planning Website

Production website for PlanWell Financial Planning, serving federal employees with retirement planning resources, calculators, and educational content.

## Technology Stack

- **Framework:** Astro 5.16.5 (static site generator)
- **CMS:** Sanity (headless CMS for blog content)
- **Language:** TypeScript with strict mode
- **Styling:** Tailwind CSS + Custom CSS
- **Package Manager:** npm

## Project Structure

```
planwell-site/
├── src/
│   ├── pages/              # Astro routing (file-based)
│   │   ├── index.astro     # Homepage
│   │   ├── about.astro
│   │   ├── services.astro
│   │   ├── contact.astro
│   │   ├── blog/           # Blog listing and posts
│   │   ├── calculators/    # FERS & TSP calculators
│   │   ├── webinars/       # Webinar pages
│   │   └── locations/      # Location-specific pages
│   ├── components/         # Reusable UI components
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   └── WebinarBanner.astro
│   ├── layouts/            # Page layouts
│   │   └── BaseLayout.astro
│   ├── lib/
│   │   └── sanity.ts       # Sanity CMS client & GROQ queries
│   ├── data/               # Static data files
│   ├── utils/              # Utility functions
│   ├── styles/
│   │   └── global.css      # Global styles
│   └── assets/             # Images, logos, SVGs
├── dist/                   # Build output (static HTML/CSS/JS)
├── public/                 # Static assets served as-is
├── directives/             # SOPs for automation workflows
├── execution/              # Python scripts for automation
├── .planning/              # GSD framework metadata
├── astro.config.mjs        # Astro configuration
├── PROJECT.md              # GSD project overview
└── package.json
```

## Development Commands

All commands run from the project root:

| Command | Action |
|---------|--------|
| `npm install` | Install dependencies |
| `npm run dev` | Start dev server at `localhost:4321` |
| `npm run build` | Build production site to `./dist/` |
| `npm run preview` | Preview production build locally |
| `npm run astro` | Run Astro CLI commands |

## Key Features

- **Blog System:** Sanity CMS-powered blog with categories, authors, tags
- **Calculators:** FERS retirement and TSP calculators
- **Webinar Pages:** Registration and information pages
- **Location Pages:** Denver, Atlanta, and other regional offices
- **SEO Optimized:** Automated sitemaps, meta tags, structured data
- **Responsive Design:** Mobile-first approach with accessibility

## Development Workflow

### Website Features (Use GSD Framework)

For adding new pages, UI components, or frontend features:

```bash
# Add a new development phase
/gsd:add-phase "Feature Name: Brief description"

# Plan implementation (research + create task list)
/gsd:plan-phase N

# Execute tasks in parallel with fresh contexts
/gsd:execute-phase N

# Verify
npm run build
npm run preview
```

**Quick fixes:**
```bash
/gsd:quick "Update button styling on contact page"
```

**Common GSD commands:**
- `/gsd:help` - View all commands
- `/gsd:add-phase` - Start new feature
- `/gsd:plan-phase N` - Research and plan
- `/gsd:execute-phase N` - Build feature
- `/gsd:quick` - Ad-hoc small changes

See [.planning/GETTING_STARTED.md](.planning/GETTING_STARTED.md) for detailed GSD guide.

### Automation & Operations (Use Directives)

For email workflows, webhooks, CMS operations:

1. Update directive: `directives/workflow_name.md`
2. Modify script: `execution/script_name.py`
3. Test: `python execution/script_name.py --test`
4. Commit changes

**Integration boundaries:**
- **GSD handles:** Website features, UI, pages, components, frontend code
- **Directives handle:** Email automation, webhooks, scheduled jobs, CRM integration

See [.planning/INTEGRATION_GUIDE.md](.planning/INTEGRATION_GUIDE.md) for system architecture.

## Sanity CMS

**Project:** nwzt57tx
**Dataset:** production

**Schema:**
- `blogPost` - Blog articles with portable text
- `author` - Author profiles with credentials
- `category` - Post categories with counts

**Queries:** See `src/lib/sanity.ts` for available GROQ queries.

## Environment Variables

Required in `.env`:

```env
PUBLIC_SANITY_PROJECT_ID=nwzt57tx
PUBLIC_SANITY_DATASET=production
SANITY_API_TOKEN=your_token_here
GOOGLE_SHEET_ID=your_sheet_id
```

## Build & Deployment

**Production build:**
```bash
npm run build
```

Generates static files to `dist/` directory ready for deployment to:
- Vercel
- Netlify
- GitHub Pages
- Any static hosting

**Current deployment:** Vercel (auto-deploy on push to main)

## Architecture

### Content Flow
1. **Content Creation:** Sanity Studio (cloud or local)
2. **Build Time:** Astro fetches content via GROQ queries
3. **Static Generation:** HTML pages generated with embedded content
4. **Deployment:** Static files served from CDN

### Styling Approach
- Tailwind CSS for utility classes
- Custom CSS in `src/styles/global.css` for brand variables
- Scoped component styles in `.astro` files
- Mobile-first responsive design

### SEO Strategy
- Automated sitemap generation (`@astrojs/sitemap`)
- Structured data (JSON-LD) in BaseLayout
- Meta tags and Open Graph in all pages
- Image optimization with Astro's Image component

## Adding New Pages

See `.agent/workflows/new-page.md` for detailed guide on:
- Page setup with BaseLayout
- Required meta props (title, description, canonical)
- Image optimization (eager vs. lazy loading)
- Performance best practices
- Schema markup

**Quick start:**
```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout
  title="Page Title - Keywords"
  description="150-160 character description for SEO"
>
  <!-- Your content -->
</BaseLayout>
```

## GSD Framework Integration

This project uses the GET SHIT DONE (GSD) framework to prevent context rot during feature development.

**What is GSD?**
- Meta-prompting system for structured development
- Phase-based workflow with XML-formatted plans
- Multi-agent execution with fresh contexts
- Atomic git commits for clean history

**Key files:**
- `PROJECT.md` - Project vision and overview
- `REQUIREMENTS.md` - Feature requirements
- `ROADMAP.md` - Development phases
- `STATE.md` - Current decisions and blockers
- `.planning/INTEGRATION_GUIDE.md` - System architecture
- `.planning/GETTING_STARTED.md` - Quick reference

**When to use:**
- Adding new calculators, pages, or features
- Building UI components
- Refactoring code
- Complex multi-file changes

**Installation:** Already configured in `.claude/`

## Automation Infrastructure

Beyond website development, this project includes:

**Directives (SOPs):**
- `directives/blog_cover_generation.md`
- `directives/call_booking.md`
- `directives/webinar_nurture.md`

**Execution Scripts:**
- Calendar integration
- Email automation
- Webhook handlers
- CMS migrations

**n8n Workflows:**
- Email campaign automation
- Form submission handling

See parent directory's `CLAUDE.md` for 3-layer architecture details.

## Git Workflow

**For website features (GSD):**
- Atomic commits per task
- Descriptive messages with context
- Co-authored by Claude Code

**For automation updates:**
- Traditional commits
- Clear, concise messages
- Manual staging

**Branches:**
- `main` - Production code
- Feature branches as needed

## Resources

- [Astro Documentation](https://docs.astro.build)
- [Sanity Documentation](https://www.sanity.io/docs)
- [GSD Framework](https://github.com/glittercowboy/get-shit-done)
- [Project Planning](.planning/GETTING_STARTED.md)

## Support

- **Website issues:** Check build logs and browser console
- **GSD questions:** See `.planning/GETTING_STARTED.md` or run `/gsd:help`
- **Automation issues:** Check directive documentation and script logs
- **CMS issues:** Verify Sanity credentials in `.env`

## License

Proprietary - PlanWell Financial Planning

---

**Version:** 1.0.0 (GSD integrated 2026-01-20)
**Maintainer:** PlanWell Financial Planning Team
