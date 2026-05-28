# DEV-07 Reference: Deep Expertise

Loaded on demand for detailed patterns, examples, and guidance.

---

## Examples

### Feature Addition

```
feat(auth): add password reset flow

Implemented complete password reset functionality with email
verification, secure token generation (1-hour expiry), and
rate limiting to prevent abuse.

- Added /api/auth/forgot-password endpoint
- Created PasswordReset email template
- Added rate limiter (3 requests per hour)

Refs: S01-05
```

### Bug Fix

```
fix(api): handle null user in session check

Session middleware was crashing when accessing protected routes
with an expired token. Now gracefully redirects to login.

Refs: NS-042
```

### Refactor

```
refactor(db): extract query builders to separate module

Moved inline SQL query construction to dedicated QueryBuilder
class to improve testability and reduce duplication across
repository files.
```

### Simple Change

```
docs: update API authentication section
```

---

## Scope Detection Guide

| File Path | Suggested Scope |
|-----------|----------------|
| `src/components/` | `ui` |
| `src/api/` | `api` |
| `tests/` | `test` |
| `lib/auth/` | `auth` |
| `lib/db/` | `db` |
| `*.config.*` | `config` |
| Cross-cutting | omit scope |

## Type Selection Guide

| Change | Type |
|--------|------|
| New endpoint | `feat` |
| Fixed null pointer | `fix` |
| Moved code around | `refactor` |
| Updated README | `docs` |
| Fixed linting | `style` |
| Added unit tests | `test` |
| Updated deps | `chore` |
| Optimized query | `perf` |
