# GSD + Automation Integration Guide

This document explains how the GET SHIT DONE (GSD) framework integrates with PlanWell's existing automation infrastructure.

## System Architecture

PlanWell uses **two complementary meta-systems**:

### 1. GSD Framework (Website Development)
- **Purpose:** Structured feature development for the website
- **Location:** `.claude/`, `.planning/`
- **Workflow:** Phase-based planning → execution → verification
- **Output:** Website features, UI components, pages, content structure

### 2. Existing Automation (Operations)
- **Purpose:** Business process automation and operations
- **Location:** `directives/`, `execution/`, `n8n-workflows/`
- **Workflow:** SOPs → AI orchestration → deterministic Python scripts
- **Output:** Email campaigns, webhooks, CMS operations, scheduled jobs

## Decision Matrix: When to Use Which System

### Use GSD For:

| Task Type | Examples |
|-----------|----------|
| **New Pages** | New calculator types, service pages, location pages |
| **UI Components** | Custom React components, Astro components, layout updates |
| **Frontend Features** | Interactive widgets, form improvements, navigation changes |
| **Content Structure** | Sanity schema updates, new content types, data models |
| **Code Refactoring** | Component reorganization, code quality improvements |
| **Styling Updates** | CSS changes, responsive design fixes, theme updates |

**Command Pattern:**
```bash
/gsd:add-phase "Feature Name: Brief Description"
/gsd:plan-phase N
/gsd:execute-phase N
```

### Use Directives/Execution For:

| Task Type | Examples |
|-----------|----------|
| **Email Automation** | Nurture sequences, drip campaigns, transactional emails |
| **Webhook Handlers** | Form submissions, calendar integrations, CRM updates |
| **CMS Operations** | Batch content migrations, automated publishing, data imports |
| **Background Jobs** | Scheduled tasks, data syncing, report generation |
| **API Integrations** | Third-party service connections, data transformations |

**Command Pattern:**
```bash
# Update directive
vim directives/webinar_nurture.md

# Modify execution script
vim execution/webinar_emails.py

# Test
python execution/webinar_emails.py --test

# Commit
git commit -m "Add welcome email template to webinar sequence"
```

## Integration Workflows

### Scenario 1: Simple Website Feature
**Example:** Add new FERS calculator page

1. **Use GSD exclusively:**
   ```bash
   /gsd:add-phase "FERS Calculator: Advanced retirement planning tool"
   /gsd:plan-phase 2
   /gsd:execute-phase 2
   ```

2. **GSD handles:**
   - Creating `src/pages/fers-advanced-calculator.astro`
   - Adding calculation logic
   - Implementing UI with Astro components
   - Updating navigation/sitemap

3. **Verify:**
   ```bash
   npm run build
   npm run preview
   ```

### Scenario 2: Pure Automation Task
**Example:** Add new email template to webinar nurture sequence

1. **Use directives/execution exclusively:**
   - Update `directives/webinar_nurture.md` with template requirements
   - Modify `execution/webinar_emails.py` to add template
   - Test: `python execution/webinar_emails.py --dry-run`
   - Commit: `git commit -m "Add day-3 follow-up template"`

2. **No GSD needed** - this is operational automation, not website development

### Scenario 3: Complex Feature Spanning Both Systems
**Example:** New webinar registration flow with landing page + email automation

#### Part 1: Website (Use GSD)
```bash
/gsd:add-phase "Webinar Registration: Landing page with form and CTA"
/gsd:plan-phase 3
/gsd:execute-phase 3
```

**GSD implements:**
- Landing page: `src/pages/webinar/register.astro`
- Registration form component
- Sanity schema for webinar data
- Form submission handler (client-side)

#### Part 2: Automation (Use Directives)
1. Create `directives/webinar_registration.md`:
   - Define registration confirmation email
   - Specify reminder email schedule
   - Document CRM sync requirements

2. Create `execution/webinar_registration_handler.py`:
   - Process form submissions
   - Send confirmation emails
   - Update CRM
   - Schedule reminders

3. Test and deploy separately

#### Integration Point:
- Reference both in `STATE.md` for full context
- Form submission calls webhook that triggers `execution/webinar_registration_handler.py`
- GSD phase notes automation requirements for future reference

## Git Workflow

### GSD Commits (Atomic, Auto-Generated)
GSD creates atomic commits for each completed task:

```
git commit -m "Task 3: Implement webinar registration form component

- Created RegistrationForm.astro with validation
- Added form state management
- Integrated with Sanity webhook endpoint
- Styled for mobile responsiveness"
```

### Manual Commits (Automation Updates)
Traditional commits for directive/execution changes:

```
git commit -m "Add registration confirmation email to webinar automation

Updated directives/webinar_registration.md with template requirements
Implemented confirmation email in execution/webinar_registration_handler.py
Tested with sample data"
```

## Directory Structure

```
planwell-site/
├── .claude/                    # GSD framework installation
│   ├── commands/gsd/          # GSD slash commands
│   ├── agents/                # Multi-agent orchestration
│   └── get-shit-done/         # Core framework
│
├── .planning/                  # GSD project metadata
│   ├── INTEGRATION_GUIDE.md   # This file
│   ├── GETTING_STARTED.md     # Quick reference
│   ├── research/              # Codebase analysis (gitignored)
│   └── phase-*/               # Phase plans and summaries
│
├── directives/                 # SOPs for automation
│   ├── blog_cover_generation.md
│   ├── call_booking.md
│   └── webinar_nurture.md
│
├── execution/                  # Python automation scripts
│   ├── calendar_handler.py
│   ├── email_sender.py
│   └── webinar_emails.py
│
├── src/                        # Website source code
│   ├── pages/                 # Astro pages (GSD modifies)
│   ├── components/            # UI components (GSD modifies)
│   └── lib/                   # Utilities (GSD modifies)
│
├── PROJECT.md                  # GSD project overview
├── REQUIREMENTS.md             # Feature requirements
├── ROADMAP.md                  # Phase breakdown
└── STATE.md                    # Current state & decisions
```

## Best Practices

### For Website Development (GSD)
1. **Always use `/gsd:plan-phase` before execution** - prevents context rot
2. **Keep phases focused** - max 2-3 tasks per phase
3. **Verify after each phase** - run `npm run build` to catch errors early
4. **Document decisions in STATE.md** - capture implementation choices
5. **Use `/gsd:quick` for minor tweaks** - styling fixes, typo corrections

### For Automation (Directives)
1. **Update directives first** - define requirements before coding
2. **Test scripts directly** - use `--dry-run` or `--test` flags
3. **Keep execution deterministic** - avoid AI logic in Python scripts
4. **Self-anneal on failures** - fix bugs, update directives with learnings
5. **Commit incrementally** - small, focused commits for operations

### For Hybrid Projects
1. **Plan architecture first** - decide system boundaries before starting
2. **Reference cross-system** - note in STATE.md when features depend on automation
3. **Test integration points** - verify webhooks, API calls, data flows
4. **Document dependencies** - make relationships between systems explicit

## Troubleshooting

### Problem: GSD tries to modify automation scripts
**Solution:** GSD should focus on website code only. If it attempts to modify `directives/` or `execution/`, clarify boundaries:
```
"This is operational automation, not website development.
Use the existing directive/execution workflow instead."
```

### Problem: Confusion about which system to use
**Solution:** Ask these questions:
1. Does it change what users see on the website? → **GSD**
2. Does it automate a business process? → **Directives**
3. Both? → **Split into two separate workflows**

### Problem: GSD context rot on complex features
**Solution:** Break into smaller phases:
```bash
# Instead of one huge phase:
/gsd:add-phase "Complete Resources Library"

# Break into multiple focused phases:
/gsd:add-phase "Resources Library: Schema and data model"
/gsd:add-phase "Resources Library: Listing page with filters"
/gsd:add-phase "Resources Library: Individual resource pages"
```

### Problem: Automation script needs website changes
**Solution:** Complete website changes first (GSD), then automation:
1. Use GSD to add form/page/component
2. Deploy and verify
3. Create directive and execution script
4. Test integration
5. Document in STATE.md

## Reference

### GSD Commands
- `/gsd:help` - List all available commands
- `/gsd:new-project` - Initialize project (already done)
- `/gsd:map-codebase` - Analyze existing code (already done)
- `/gsd:add-phase` - Add new development phase
- `/gsd:plan-phase N` - Research and create phase plan
- `/gsd:execute-phase N` - Run tasks in phase plan
- `/gsd:verify-work N` - Test and verify phase completion
- `/gsd:quick` - Ad-hoc lightweight execution
- `/gsd:pause-work` - Save state for later
- `/gsd:resume-work` - Continue previous session

### Automation Commands
- `python execution/script_name.py --help` - View script usage
- `python execution/script_name.py --dry-run` - Test without executing
- `python execution/script_name.py --test` - Run with test data
- Check `directives/` for specific workflow SOPs

### Key Files
- `PROJECT.md` - GSD project overview and vision
- `REQUIREMENTS.md` - Feature requirements and scope
- `ROADMAP.md` - Phase breakdown
- `STATE.md` - Current decisions and blockers
- `.planning/GETTING_STARTED.md` - Quick reference guide

## Summary

**Simple Rule:** Website features → GSD. Business automation → Directives.

Both systems make development more reliable by preventing context rot and ensuring consistent execution. They complement each other without overlapping.

When in doubt, ask: "Am I changing what users see on the website?" If yes, use GSD. If no, use directives.
