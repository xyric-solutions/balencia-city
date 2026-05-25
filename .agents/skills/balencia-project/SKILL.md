---
name: balencia-project
description: "Project context for Balencia City v3. Use when working in /Users/hamza/Desktop/balencia-city-v3, auditing progress, interpreting module specs and reviews, orienting build order, or preparing Balencia structure, energy, assembly, QA, or app workflows."
---

# Balencia Project

## Source Of Truth

- Work from the repo root: `/Users/hamza/Desktop/balencia-city-v3`.
- Read `PROGRESS.md` first for current state, then `BUILD-ORDER.md`, `MASTER-CONTEXT.md`, `QUALITY-RUBRIC.md`, and the target module `SPEC.md` or `REVIEW.md`.
- Prefer repo-relative paths in instructions and artifacts. Treat older copied workspace paths as stale aliases for this workspace.
- Treat files in `/Users/hamza/Downloads` as source drafts only. Do not modify them unless the user explicitly asks.

## Current Orientation

- At skill creation time, `PROGRESS.md` reported 10 of 12 structures complete, 10 approved exteriors, 10 approved interiors, 0 energy pipelines, 0 cross-connections, and assembly not started.
- The next batch was `10-ai-analytics/exterior-major-forms`; `11-nutrition` was queued after that.
- There were 20 approved module GLBs under `modules/*/{exterior,interior}/approved/`, covering modules `00` through `09`.
- Always re-read `PROGRESS.md` before giving status or starting work; this section is an orientation snapshot, not a permanent source of truth.

## Core Rules

- Build one module at a time in the order defined by `BUILD-ORDER.md`.
- Do not start a module interior before its exterior is approved.
- Apply the 7-slot material system exactly: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Run the relevant quality gates from `QUALITY-RUBRIC.md` before promoting assets to `approved/`.
- Keep generated prompts and skill instructions concise. Load `MASTER-CONTEXT.md` selectively by section anchors when possible.

## Tooling Preflight

- For Blender work, verify that a live Blender tool is available, such as `execute_blender_code`, or that an approved fallback runner exists.
- Do not install Blender MCP automatically. If Blender MCP is missing, stop clearly and state what setup or approval is needed.
- This workspace has `/Applications/Blender.app`, but `blender` may not be on PATH. Check before running command-line Blender workflows.

## Related Skills

- Use `$balencia-build` or `/balencia-build` aliases for build-loop orchestration.
- Use `$balencia-status` or `/balencia-status` aliases for read-only dashboard reporting.
- Use `$balencia-qa` or `/balencia-qa` aliases for module, city, or energy quality review.
- Use the team skills for focused lifecycle guidance: `$balencia-structure-team`, `$balencia-energy-team`, `$balencia-assembly-team`, and `$balencia-app-team`.
