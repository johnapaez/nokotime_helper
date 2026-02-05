# Documentation Guide

**Purpose**: Standards and best practices for documenting work in software projects  
**Audience**: All developers, AI agents (Cursor, GitHub Copilot, Windsurf, Codex, etc.)  
**Last Updated**: 2026-01-28

> **Note**: This is a generic guide designed to be copied and adapted to any project. Save this in your project's `/docs` folder or root directory.

---

## Quick Start

When documenting your work, follow these standards for consistency:

- **Session logs**: `docs/feature-tracking/[feature]/sessions/YYYY-MM-DD-description.md`
- **Feature docs**: `docs/feature-details/[FeatureName].md`
- **Progress tracking**: `docs/feature-tracking/[feature]/[Feature]-Progress.md`
- **Setup guides**: `docs/infrastructure/[Technology]Setup.md`

See [Directory Structure](#directory-structure) below for full organization.

---

## Directory Structure

```
/docs/
├── README.md                          # Documentation navigation hub
├── TechnicalArchitecture.md           # System architecture
├── CommonPatterns.md                  # Shared patterns and conventions
│
├── [Component/Module]Overview.md      # Component-specific docs
│
├── feature-details/                   # Permanent feature docs
│   ├── [FeatureName].md
│   └── ...
│
├── feature-tracking/                  # Active development (temporary)
│   └── [feature-name]/
│       ├── README.md
│       ├── [Feature]-Progress.md      # Current status
│       └── sessions/                  # Session logs
│           ├── YYYY-MM-DD-[description].md
│           └── YYYY-MM-[month]-sessions-summary.md
│
├── infrastructure/                    # Setup & troubleshooting
│   ├── [Technology]Setup.md
│   ├── [Technology]Troubleshooting.md
│   └── [Technology]MigrationSummary.md
│
└── [Topic]-QuickReference.md          # Quick lookup references
```

**Adapt to your project**: This is a recommended structure. Adjust based on your project size and needs. Small projects might use a simplified structure; microservices might organize by service.

---

## File Naming Conventions

### Standard Documentation Files

| Type | Pattern | Example |
|------|---------|---------|
| Component/Module | `[Name].md` or `[Name]Overview.md` | `Authentication.md` |
| Technical reference | `[Topic]-Architecture-Reference.md` | `API-Architecture-Reference.md` |
| Quick reference | `[Topic]-QuickReference.md` | `CSS-Variables-QuickReference.md` |
| Progress tracking | `[Feature]-Progress.md` | `MobileApp-Progress.md` |
| Rollout tracking | `[Feature]-Rollout.md` | `NewCheckout-Rollout.md` |
| Setup guides | `[Technology]Setup.md` | `DockerSetup.md` |
| Troubleshooting | `[Technology]Troubleshooting.md` | `DatabaseTroubleshooting.md` |
| Feature details | `[FeatureName].md` | `TwoFactorAuth.md` |

### Session Logs and Tracking

| Type | Pattern | Example |
|------|---------|---------|
| Session logs | `YYYY-MM-DD-[brief-description].md` | `2026-01-28-api-endpoint-refactor.md` |
| Monthly summaries | `YYYY-MM-[month]-sessions-summary.md` | `2026-01-january-sessions-summary.md` |

### Naming Rules

- **Dates**: Always use `YYYY-MM-DD` format
- **Multi-word files**: 
  - Use hyphens in session logs: `2026-01-28-payment-api-refactor.md`
  - Use PascalCase in feature-details: `TwoFactorAuth.md`
- **Be descriptive**: `2026-01-28-payment-api-refactor.md` not `2026-01-28-work.md`

---

## Document Templates

### Session Log Template

Use this template when documenting development sessions:

```markdown
# [Brief Description]

**Date**: YYYY-MM-DD
**Author**: [Your Name]
**Focus**: [Main area of work]
**Status**: [In Progress | Complete | Blocked]

---

## Overview

[What was worked on during this session]

## Implementation Details

### [Component/Area 1]
[Technical details of changes]

### [Component/Area 2]
[Technical details of changes]

## Files Modified

- `path/to/file1.ext` - [Brief description of changes]
- `path/to/file2.ext` - [Brief description of changes]

## Testing & Validation

- ✅ [Test scenario 1]
- ✅ [Test scenario 2]
- 🔲 [Pending test]

## Next Steps

1. [Follow-up item 1]
2. [Follow-up item 2]

## Architecture Decisions

### [Decision 1]
**Rationale**: [Why this approach was chosen]
**Alternatives Considered**: [Other options]

## Notes

[Any additional observations or context]
```

### Feature Documentation Template (Dual-Audience)

Use this for documenting features in `feature-details/`:

```markdown
# [Feature Name]

**Status**: [Enabled | Beta | Development | Planned]
**Last Updated**: YYYY-MM-DD

---

## What Is This?

[Non-technical explanation for product managers, QA, stakeholders]

### Benefits
- [User benefit 1]
- [User benefit 2]

### Visual Examples

[Screenshots, diagrams, or visual demonstrations]

### How to Use

[Non-technical usage instructions]

---

## Technical Documentation

### Architecture

[Technical design and implementation approach]

### Implementation Details

[Code locations, key classes/functions, technical specifics]

### Configuration

[Settings, flags, environment variables]

### Code Examples

```language
[Code samples]
```

### Testing

[How to test this feature]

## Related Documentation

- [Architecture doc]
- [API reference]
```

### Progress/Status Document Template

Use this for tracking initiatives:

```markdown
# [Initiative Name] - Progress

**Status**: [In Progress | On Hold | Complete]
**Completion**: XX%
**Last Updated**: YYYY-MM-DD

---

## Current Status

[Brief summary of where things stand]

### Completion Overview

- ✅ [Completed item 1]
- ✅ [Completed item 2]
- ⚠️ [In progress item 1]
- ⚠️ [In progress item 2]
- 🔲 [Pending item 1]
- 🔲 [Pending item 2]

## Next Steps (Priority Order)

1. **[High priority task]**
   - [Details or subtasks]

2. **[Medium priority task]**
   - [Details or subtasks]

## Recent Updates

### YYYY-MM-DD
- [Update 1]
- [Update 2]

## Quick Links

- [Related documentation]
- [Technical reference]
```

---

## Status Indicators

Use these consistently across all documentation:

- ✅ Complete / Done / Working / Verified
- ⚠️ In Progress / Warning / Needs Attention
- 🔲 Pending / Not Started / Checkbox
- ❌ Blocked / Failed / Error
- 📝 Draft / Documentation
- 🔧 Configuration / Setup
- 🧪 Testing / Experimental / Beta

---

## Documentation Best Practices

### 1. Lifecycle-Based Organization

- **Permanent documentation** → `feature-details/`, root-level docs
- **Temporary documentation** → `feature-tracking/` for active development
- **Archive or delete** completed feature-tracking folders to keep docs clean

### 2. Dual-Audience Approach

When documenting features:
- **Top section**: User-friendly, non-technical (for product, QA, stakeholders)
- **Bottom section**: Technical details (for developers)

This allows multiple teams to use the same documentation effectively.

### 3. Session Logs

Create session logs to document development work:

**When to create**:
- After each significant development session
- When making architectural decisions
- When encountering and solving complex problems

**What to include**:
- What was done and why
- Files modified
- Testing status
- Architecture decisions and rationale
- Next steps

**Monthly summaries**:
- When you have 5+ sessions in a month, create a summary
- Archive older session logs when no longer actively referenced

### 4. Cross-Referencing

- Use `README.md` files as navigation hubs
- Include "Related Documentation" sections in docs
- Link status docs to reference docs
- Create bidirectional links between related features

### 5. Keep Documentation Current

- Add "Last Updated" dates to all docs
- Update docs when code changes
- Mark outdated docs with Status: "Archived" or "Deprecated"
- Remove obsolete documentation promptly

---

## Quick Decision Guide

**Creating a session log?**
→ Use Session Log Template  
→ Save in `docs/feature-tracking/[feature]/sessions/YYYY-MM-DD-description.md`

**Documenting a new feature?**
→ Use Feature Documentation Template  
→ Save in `docs/feature-details/[FeatureName].md`

**Tracking progress on an initiative?**
→ Use Progress/Status Template  
→ Save in `docs/feature-tracking/[feature]/[Feature]-Progress.md`

**Writing setup instructions?**
→ Create guide in `docs/infrastructure/[Technology]Setup.md`

**Creating quick reference?**
→ Name it `docs/[Topic]-QuickReference.md`

**Documenting component-specific information?**
→ Add to or create `docs/[ComponentName]Overview.md`

---

## For AI Agents

When an AI agent (Cursor, GitHub Copilot, Windsurf, Codex, etc.) is assisting with development:

### Always:
1. **Read this guide first** when asked to document work
2. **Follow naming conventions** exactly as specified
3. **Use the appropriate template** for the type of documentation
4. **Include all required sections** from templates (can omit non-applicable sections)
5. **Use consistent status indicators** (✅, ⚠️, 🔲, etc.)
6. **Update "Last Updated"** dates

### Session Logs:
- Create after development sessions
- Document WHY decisions were made, not just WHAT changed
- Include all modified files
- Note testing status
- List concrete next steps

### Feature Documentation:
- Structure for dual audience (non-technical first, technical second)
- Include visual examples where helpful
- Link to related documentation

### Progress Tracking:
- Update regularly as work progresses
- Keep completion percentages current
- Prioritize next steps
- Link to detailed session logs

---

## Adapting for Your Project

This guide is designed to be adaptable to different project types and sizes:

### For Smaller Projects
Use a simplified structure:
```
/docs/
├── README.md
├── Architecture.md
├── Setup.md
└── feature-details/
```

### For Microservices
Organize by service:
```
/docs/
├── README.md
├── architecture/
│   ├── SystemOverview.md
│   └── [Service]Architecture.md
├── [service-name]/
│   ├── README.md
│   ├── API.md
│   └── Setup.md
└── infrastructure/
```

### For Multi-Module Applications
Organize by module:
```
/docs/
├── README.md
├── TechnicalArchitecture.md
├── [module-a]/
│   └── [Module docs]
├── [module-b]/
│   └── [Module docs]
└── shared/
    └── CommonPatterns.md
```

The key is maintaining **consistency** in naming and structure once you choose an approach.

---

## Getting Started Checklist

When setting up documentation in a new project:

- [ ] Create `/docs/` directory
- [ ] Create `docs/README.md` as navigation hub
- [ ] Set up `docs/feature-details/` for permanent docs
- [ ] Set up `docs/feature-tracking/` for active work
- [ ] Copy this `DocumentationGuide.md` to your docs folder
- [ ] Customize examples to match your project
- [ ] Add "Last Updated" dates to existing docs
- [ ] Standardize existing filenames to conventions
- [ ] Update `docs/README.md` to reference this guide
- [ ] Share with your team and AI agents

---

## Using This Guide

### For New Projects
1. Copy this file to your project's `/docs` directory
2. Customize the examples to match your technology stack
3. Reference it in your `docs/README.md`
4. Share with your team

### For Existing Projects
1. Review your current documentation structure
2. Gradually migrate to these conventions
3. Update existing docs to follow naming standards
4. Create missing documentation using templates

### For AI Agents
Instruct AI agents to read this guide:
```
"Read docs/DocumentationGuide.md and create a session log for today's work"
```

All AI coding assistants (Cursor, Copilot, Windsurf, Codex) can follow these standards.

---

## Questions?

For questions about this guide or to suggest improvements:
- Review existing documentation in your project for examples
- Refer to `docs/README.md` for navigation
- Adapt the templates to your project's needs
- Share improvements with your team

**Remember**: Consistent documentation helps everyone - developers, AI agents, and future team members!

---

## Sharing This Guide

This is a generic, project-agnostic guide. Feel free to:
- ✅ Copy to any project
- ✅ Customize for your needs
- ✅ Share with your team
- ✅ Adapt templates to your conventions
- ✅ Use with any AI coding assistant

The goal is consistency across projects while allowing flexibility for project-specific needs.
