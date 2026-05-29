---
skill_id: "DEV-07"
name: "Commit Message Generator"
version: "v2.1"
category: "development"
description: "Generate clear, structured commit messages following conventional commits format. Use when committing code changes, especially multi-file changes that need structured messages. Includes Xyric story/task tracking integration and Co-Authored-By attribution."
---

# DEV-07: Commit Message Generator

## Purpose

Generate clear, structured commit messages with AI-powered summaries. Follows conventional commits format and integrates with Xyric's story/task tracking.

## Philosophy

**Commit messages are documentation that ships with the code.** Six months from now, `git log` and `git blame` are the primary tools for understanding why code changed. A good commit message saves hours of archaeology. A bad one — "fix stuff", "update code" — forces the reader to reverse-engineer intent from diffs.

**Write for the future reader, not the present author.** The person reading the commit already knows it changed code (they can see the diff). What they need is WHY: what problem was being solved, what decision was made, what trade-off was accepted. The subject says WHAT happened. The body says WHY it matters.

**One commit, one purpose.** A commit that "adds auth and fixes sidebar and updates deps" is three commits pretending to be one. Atomic commits make `git bisect` useful, make reverts safe, and make code review possible. If the subject needs "and", split the commit.

## When to Activate

**Triggers**:
- `/commit` slash command
- "Generate a commit message"
- "What should I commit as?"
- "Summarize my changes for commit"
- Before staging significant changes

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types (Required)

| Type | Use When |
|------|----------|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `refactor` | Code restructuring (no behavior change) |
| `docs` | Documentation only |
| `style` | Formatting, whitespace (no logic change) |
| `test` | Adding or updating tests |
| `chore` | Build, config, dependencies |
| `perf` | Performance improvements |

### Scope (Optional)

Area of codebase affected. Examples: `auth`, `api`, `ui`, `db`, `config`

### Subject Line Rules

- Imperative mood ("add" not "added" or "adds")
- No period at end
- Max 50 characters
- Lowercase start

### Body (Required for non-trivial changes)

- Explain WHAT changed and WHY
- Wrap at 72 characters
- Use bullet points for multiple changes
- Focus on business impact, not just code changes

### Footer (When applicable)

- `Refs: S01-05` - Story reference
- `Refs: NS-001` - Task reference
- `Fixes: #123` - Issue reference
- `BREAKING CHANGE:` - For breaking changes

## Workflow

### Step 1: Analyze Changes

```bash
git diff --staged
git status
```

Understand: what files changed, what functionality was added/modified/removed, user's intent.

### Step 2: Determine Type

Match changes to the most appropriate type.

### Step 3: Identify Scope

Look at the primary area affected.

### Step 4: Write Subject

Summarize in imperative form, max 50 chars.

### Step 5: Write Body

For non-trivial changes: explain motivation, describe changes at high level, note important decisions.

### Step 6: Add References

Link to stories/tasks if applicable. Check branch name for story ID.

## Xyric Rules

1. **Never invent details** - Only describe what actually changed
2. **Business language** - "Enable users to reset passwords" not "Add POST endpoint"
3. **Be specific** - "Fix null check in UserService.getProfile()" not "Fix bug"
4. **Keep subject concise** - Details go in body, not subject
5. **Link to tracking** - Always reference stories/tasks when applicable

## Integration

| Skill | Integration |
|-------|-------------|
| DEV-01 | After code review, generate commit for approved changes |
| EXPERT-13 | Reference story IDs from generated stories |

## Before/After Examples

### Bad: Vague, past tense, no body
```
Updated auth code
```

### Good: Specific, imperative, explains why
```
fix(auth): handle expired token in session middleware

Session middleware crashed on protected routes when the JWT had
expired, returning a 500 instead of redirecting to login. Now
checks token expiry before accessing user claims.

Refs: NS-042
```

---

### Bad: Mixed concerns, no scope
```
Add login page and fix header and update packages
```

### Good: Split into three atomic commits
```
feat(auth): add login page with email/password form

Refs: S02-01
```
```
fix(ui): prevent header overlap on mobile viewports
```
```
chore: update React to 19.1 and Tailwind to 4.1
```

---

### Bad: File list in subject, no business context
```
Changed UserService.ts, AuthController.ts, and middleware.ts
```

### Good: Business impact front and center
```
feat(auth): enable SSO login via company SAML provider

Adds SAML 2.0 support so enterprise users can log in with their
corporate credentials instead of creating separate accounts.
Reduces onboarding friction for B2B customers.

Refs: S03-12
```

## Anti-Patterns

| Anti-Pattern | Why It Fails | Do Instead |
|---|---|---|
| Vague subjects ("Update code", "Fix stuff", "WIP") | Future reader learns nothing from `git log` | Be specific: what changed and where |
| Past tense ("Added feature") | Breaks conventional commits convention, inconsistent with imperative git style | Use imperative: "add feature" |
| File lists in subject | Wastes 50-char budget, conveys no intent | Name the feature/fix; put file details in body if needed |
| Omitting scope on clearly-scoped changes | Harder to filter `git log --grep` by area | Add scope: `feat(auth):`, `fix(api):` |
| Giant multi-concern commits | Cannot bisect, cannot revert safely, cannot review meaningfully | One commit per logical change |
| Skipping body on significant changes | Diff shows what changed but not why — intent is lost | Always explain motivation for non-trivial changes |
| Invented details not in the diff | Misleads future readers, erodes trust in commit history | Only describe what actually changed |

## Success Criteria

- [ ] Type matches the nature of the change (not just `chore` for everything)
- [ ] Subject is imperative mood, lowercase, no period, 50 chars or fewer
- [ ] Scope reflects the affected area (or omitted for cross-cutting changes)
- [ ] Body explains WHAT and WHY for non-trivial changes
- [ ] Body lines wrap at 72 characters
- [ ] Footer references stories/tasks when applicable
- [ ] One logical change per commit — no mixed concerns
- [ ] Uses business language ("enable password reset") over implementation language ("add POST endpoint")
