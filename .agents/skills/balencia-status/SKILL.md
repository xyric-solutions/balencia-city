---
name: balencia-status
description: "Read-only Balencia City build dashboard. Use when the user types /balencia-status, asks what is done, what is next, current module state, failing gates, approved assets, energy status, assembly status, or app readiness."
---

# Balencia Status

## Alias

Treat `/balencia-status` as the human-facing alias for this skill. `$balencia-status` may be invoked explicitly.

## Read-Only Rule

Do not modify files, run Blender exports, move assets, or update progress while using this skill.

## Inputs

Read:

- `PROGRESS.md`
- `BUILD-ORDER.md`
- `modules/*/REVIEW.md`
- `energy-system/REVIEW.md` if present
- `assembly/REVIEW.md` if present

Optionally count approved GLBs with `find modules -path '*/approved/*.glb' -print` as a consistency check.

## Dashboard Output

Report:

- Structure counts, approved exteriors, approved interiors, energy pipelines, cross-connections, assembly, and app status.
- Current phase, module, step, session, and `next_batch`.
- Structure table with exterior, interior, pipeline, integrated, and status columns.
- Last 5 session log rows from `PROGRESS.md`.
- Any active or unresolved `FAIL`, `NEEDS FIX`, or conditional approval notes from module reviews.
- Any mismatch between `PROGRESS.md` counts and approved GLB files.

## Current Snapshot Format

Use this shape unless the user asks for something else:

```markdown
# Balencia City v3 - Build Status

## Progress
- Structures: N/12 complete
- Exteriors: N/12 approved
- Interiors: N/12 approved
- Energy Pipelines: N/11
- Cross-Connections: N/6+
- Assembly: status
- App: status

## Current Phase
- Phase: ...
- Module: ...
- Step: ...
- Session: ...

## Next Batch
- ...
```

## Cautions

- Prefer `PROGRESS.md` as the canonical dashboard, but flag inconsistencies found in reviews or assets.
- Do not imply visual QA was run unless Blender or screenshots were actually inspected in this turn.
