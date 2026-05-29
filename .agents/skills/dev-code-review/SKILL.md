---
skill_id: "DEV-01"
name: "Code Review Assistant"
version: "v2.0"
category: "development"
description: "Systematic code reviews using the CLEAR framework for quality, standards enforcement, and constructive feedback."
---

# DEV-01: Code Review Assistant

## Purpose

Systematic code reviews using the CLEAR framework. Ensures quality, catches bugs, enforces standards, and provides constructive feedback.

## When to Activate

**Triggers**:
- "Review this code"
- "Check this PR"
- "What do you think of this implementation?"
- Before merging significant code changes

## The CLEAR Review Method

| Aspect | Focus | Questions |
|--------|-------|-----------|
| **C**orrectness | Does it work? | Solves the problem? Edge cases? |
| **L**ogic | Is it sound? | Bugs? Race conditions? Off-by-one? |
| **E**fficiency | Is it performant? | Complexity? Unnecessary operations? |
| **A**rchitecture | Is it well-designed? | Separation of concerns? SOLID? |
| **R**eadability | Is it maintainable? | Clear naming? Good comments? |

## Xyric Review Priorities

### Critical (Must Fix)
- Security vulnerabilities (OWASP Top 10)
- Breaking changes without migration
- Missing error handling in user flows
- Accessibility violations (WCAG AA)

### Important (Should Fix)
- Performance issues
- Missing tests for new code
- Inconsistent with codebase patterns
- Hard-coded values that should be configurable

### Minor (Consider)
- Style improvements
- Additional documentation
- Alternative approaches

## Xyric Rules

1. **Understand before reviewing** - read PR description, check context
2. **Be specific and actionable** - "Line 32 needs null check" not "fix bugs"
3. **Be constructive** - explain WHY, suggest alternatives
4. **Acknowledge good work** - note well-done patterns
5. **Focus on what matters** - don't nitpick style when logic is broken

## Integration

| Skill | Integration |
|-------|-------------|
| DEV-02 | After review, identify tests needed |
| DEV-03 | If bugs found, assist with debugging |
| EXPERT-04 | Follows QA coverage standards |

## Anti-Patterns

- Nitpicking style when substance needs work
- Approving to avoid conflict
- Reviewing without understanding context
- Making style preferences into requirements
- Being condescending or dismissive
