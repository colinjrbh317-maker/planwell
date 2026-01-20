# Getting Started with GSD on PlanWell

Quick reference guide for using the GET SHIT DONE framework on the PlanWell website.

## What is GSD?

GSD is a context engineering system that prevents "context rot" (AI output degradation as context fills up) through:
- **Phase-based development** - Structured workflow for features
- **XML-formatted plans** - Optimized for Claude's processing
- **Fresh context per task** - Parallel execution without context collision
- **Atomic git commits** - Clean, traceable history

## Quick Start

### Adding a New Feature

```bash
# 1. Add a new phase
/gsd:add-phase "Feature Name: Brief description"

# 2. Plan the implementation (research + create task list)
/gsd:plan-phase N

# 3. Execute the plan (tasks run in fresh contexts)
/gsd:execute-phase N

# 4. Verify it works
npm run build
npm run preview

# 5. (Optional) Mark milestone complete
/gsd:complete-milestone
```

### Quick Fix (No Full Planning)

```bash
# For small changes, styling fixes, typos
/gsd:quick "Update button styling on contact page for mobile"
```

## Common Commands

| Command | When to Use |
|---------|-------------|
| `/gsd:help` | View all available commands |
| `/gsd:add-phase "Name"` | Start a new feature phase |
| `/gsd:plan-phase N` | Research and create detailed task plan |
| `/gsd:execute-phase N` | Run the tasks in the plan |
| `/gsd:quick "Task"` | Ad-hoc execution without full planning |
| `/gsd:verify-work N` | User acceptance testing checklist |
| `/gsd:pause-work` | Save state and stop |
| `/gsd:resume-work` | Continue from saved state |
| `/gsd:complete-milestone` | Finalize phase with release tag |

## When to Use GSD vs. Automation Scripts

### Use GSD For:
- ✅ New pages (calculators, services, locations)
- ✅ UI components (forms, widgets, navigation)
- ✅ Frontend features (interactive elements)
- ✅ Content structure (Sanity schemas)
- ✅ Code refactoring
- ✅ Styling updates

### Use Directives/Execution For:
- 🔧 Email automation
- 🔧 Webhook handlers
- 🔧 CMS batch operations
- 🔧 Background jobs
- 🔧 API integrations

**Rule of thumb:** If it changes what users see on the website → GSD. If it automates a business process → Directives.

See [.planning/INTEGRATION_GUIDE.md](.planning/INTEGRATION_GUIDE.md) for detailed decision matrix.

## Example Workflow: Adding a New Calculator

```bash
# 1. Create the phase
/gsd:add-phase "Roth IRA Calculator: Contribution limits and growth projections"

# 2. Plan implementation
/gsd:plan-phase 4

# GSD will research:
# - Existing calculator patterns in src/pages/
# - Astro component structure
# - Sanity integration approach
# - SEO optimization patterns

# Then create XML task plan:
# - Task 1: Create page structure
# - Task 2: Implement calculation logic
# - Task 3: Add form validation
# - Task 4: Style for mobile
# - Task 5: Add SEO metadata

# 3. Execute tasks in parallel
/gsd:execute-phase 4

# GSD spawns fresh agents for each task:
# - Agent 1: Creates src/pages/roth-ira-calculator.astro
# - Agent 2: Implements calc functions
# - Agent 3: Adds validation
# - Agent 4: Responsive CSS
# - Agent 5: Meta tags and schema

# Each agent works in fresh 200k token context
# Results merged with atomic commits

# 4. Verify
npm run build
npm run preview
# Visit http://localhost:4321/roth-ira-calculator

# 5. Complete
/gsd:complete-milestone
# Creates release tag, archives phase plan
```

## Project Files

### GSD Metadata (In Project Root)
- `PROJECT.md` - Vision and overview
- `REQUIREMENTS.md` - Feature requirements (V1 done, V2 planning)
- `ROADMAP.md` - Phase breakdown
- `STATE.md` - Current decisions and blockers

### Planning Directory
- `.planning/phase-N/PLAN.md` - XML task specifications
- `.planning/phase-N/SUMMARY.md` - Phase completion summary
- `.planning/research/` - Codebase analysis (gitignored)
- `.planning/quick/` - Ad-hoc execution logs (gitignored)

### Framework Installation
- `.claude/commands/gsd/` - Slash commands
- `.claude/agents/` - Planner, executor, verifier agents
- `.claude/get-shit-done/` - Core framework

## Tips & Best Practices

### 1. Keep Phases Focused
❌ Bad: `/gsd:add-phase "Complete website redesign"`
✅ Good: `/gsd:add-phase "Homepage: Hero section redesign with video"`

**Why:** Smaller phases = better context management, clearer commits

### 2. Plan Before Executing
❌ Bad: Jump straight to `/gsd:execute-phase` without planning
✅ Good: Always run `/gsd:plan-phase` first

**Why:** Planning phase does research, creates verified task specs, prevents hallucination

### 3. Use `/gsd:quick` for Minor Changes
✅ `/gsd:quick "Fix typo in about page title"`
✅ `/gsd:quick "Update footer copyright year to 2026"`
✅ `/gsd:quick "Adjust calculator button color to match brand"`

**Why:** Avoids overhead of full phase planning for trivial changes

### 4. Verify After Each Phase
```bash
npm run build        # Check for build errors
npm run preview      # Manual testing
```

**Why:** Catches issues early before they compound

### 5. Document Decisions in STATE.md
When making implementation choices, update STATE.md:
```markdown
## Phase 4: Roth IRA Calculator

**Decision:** Used client-side calculation instead of API
**Rationale:** No sensitive data, faster UX, reduces server load
**Trade-off:** Can't persist calculation history without auth
```

**Why:** Future phases benefit from past context

### 6. Split Complex Features
If a phase plan has 5+ tasks or affects 10+ files, split it:

```bash
# Too big:
/gsd:add-phase "Resources Library: Complete implementation"

# Better:
/gsd:add-phase "Resources Library: Schema and data model"
/gsd:add-phase "Resources Library: Listing page"
/gsd:add-phase "Resources Library: Resource detail pages"
/gsd:add-phase "Resources Library: Search and filters"
```

## Tech Stack Reminders

**Framework:** Astro 5.16.5
- Static site generator
- Pages in `src/pages/` map to URLs
- Components in `src/components/`
- Layouts in `src/layouts/`

**CMS:** Sanity
- Schema: Author, Category, BlogPost
- Client: `src/lib/sanity.ts`
- GROQ queries for data fetching

**Styling:** Tailwind CSS + Custom CSS
- Global styles: `src/styles/global.css`
- Component styles: scoped `<style>` tags

**TypeScript:** Strict mode enabled
- Type checking at build time
- Astro provides `.d.ts` types

## Verification Checklist

After completing a phase:

- [ ] Build succeeds: `npm run build`
- [ ] No TypeScript errors
- [ ] No console errors in browser
- [ ] Mobile responsive (test in DevTools)
- [ ] Links work correctly
- [ ] Forms validate properly
- [ ] Images optimized and loading
- [ ] SEO meta tags present
- [ ] Sitemap includes new pages
- [ ] Git commits are atomic and descriptive

## Troubleshooting

### GSD command not found
**Solution:** Restart Claude Code session to load `.claude/commands/`

### Phase execution fails mid-way
**Solution:**
```bash
/gsd:resume-work      # Continue from last checkpoint
# or
/gsd:pause-work       # Save state
# Review STATE.md for errors
# Fix issues manually if needed
/gsd:resume-work
```

### Context rot still happening
**Solution:** Phase is too large. Split into 2-3 smaller phases with clearer boundaries.

### Build errors after GSD execution
**Solution:**
1. Check build output for specific errors
2. Fix manually or use `/gsd:quick "Fix build error in [file]"`
3. Update STATE.md with learnings
4. Run `npm run build` again

### Git commits not atomic
**Solution:** Ensure `~/.claude/settings.json` has auto-approval configured:
```json
{
  "auto_approve_commands": ["git status", "git diff", "git log", "git add", "git commit"]
}
```

## Resources

- [Full Integration Guide](.planning/INTEGRATION_GUIDE.md) - Detailed system architecture
- [GSD GitHub Repo](https://github.com/glittercowboy/get-shit-done) - Official documentation
- [PROJECT.md](../PROJECT.md) - PlanWell project overview
- [ROADMAP.md](../ROADMAP.md) - Feature development phases

## Support

Issues or questions about:
- **GSD framework:** Check `/gsd:help` or GitHub issues
- **PlanWell architecture:** See PROJECT.md and existing code
- **Integration decisions:** Review INTEGRATION_GUIDE.md

## Version

- GSD Framework: 1.8.0
- Installed: 2026-01-20
- Project: PlanWell Financial Planning Website
- Integration Type: Brownfield (existing project)
