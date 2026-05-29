---
name: balencia-build
description: "Run the Balencia City build-loop workflow. Use when the user types /balencia-build, asks to build next, continue building Balencia, build a specific module, generate a build session prompt, or run looped structure, energy, assembly, or app work."
---

# Balencia Build

## Alias

Treat `/balencia-build` as the human-facing alias for this skill. `$balencia-build` may be invoked explicitly.

## State Read

1. Read `PROGRESS.md` and `BUILD-ORDER.md`.
2. Parse frontmatter fields: `current_module`, `current_phase`, `current_session`, `last_completed`, and `next_batch`.
3. If frontmatter is missing, scan the Structure Status table for the first module that is not complete.
4. Resolve arguments:
   - `next`: use `next_batch`.
   - `{NN}-{slug}`: target that module.
   - `session-{NN}-{slug}`: target that app repair session when `current_phase` is Phase 9.
   - `loop max=N`: repeat after successful QA, stopping at `N` iterations.
5. If `current_phase` starts with `phase-9`, read `BALENCIA-CURRENT-AUDIT.md` and the Phase 9 sections in `PROGRESS.md` and `BUILD-ORDER.md` before generating or executing the next session.
6. If `current_phase` starts with `phase-10`, read `apps/balencia/PHASE-10-BACKLOG.md` and the Phase 10 sections in `PROGRESS.md` and `BUILD-ORDER.md` before generating or executing the next session.

## Workflow Selection

- Phases 1-4: use `$balencia-structure-team`.
- Phase 5: use `$balencia-energy-team`.
- Phase 6: use `$balencia-assembly-team`.
- Phase 7: use `$balencia-app-team`.
- Phase 8: use the relevant structure, energy, assembly, or app team based on the session scope recorded in `BUILD-ORDER.md`.
- Phase 9: use `$balencia-app-team` for app-experience repairs unless the audit session explicitly proves model or assembly changes are required.
- For structure phases, map `exterior-major-forms`, `exterior-detail`, `interior`, and `integration` to the corresponding prompt template in `PROMPT-TEMPLATES.md`.
- Combined exterior may be used only when the target has no prior exterior sessions, fewer than 6 key architectural elements, and an exterior budget max of 15000 tris or less.

## Phase 9 App Repair Queue

Source of truth: `BALENCIA-CURRENT-AUDIT.md`. Execute these sessions sequentially. Keep Phase 9 scoped to app-layer interaction, camera, label, flow, and QA harness repair unless a later QA result requires model work.

| Session | next_batch | Name | Priority | Required outcome |
|---:|---|---|---|---|
| 77 | `session-77-p0-interaction-truth-pass` | Interaction Truth Pass | P0 | Add missing interaction targets, gate stale targets by overview/active scene relevance, align hit areas, and prove Knowledgebase hover/click never shows Finance copy. |
| 78 | `session-78-p0-sia-interior-rewrite` | SIA Interior Rewrite | P0 | Make Scene 3 read as entering and moving inside SIA Tower with a clear atrium, neural core, city model, and midpoint interior verdict. |
| 79 | `session-79-p1-label-anchoring-and-naming-pass` | Label Anchoring And Naming Pass | P1 | Attach labels to model anchors where practical and standardize naming across labels, panels, nav, and overlays. |
| 80 | `session-80-p1-interior-reveal-scenes-4-8` | Interior Reveal Pass, Scenes 4-8 | P1 | Tune Fitness, Yoga, Finance, Knowledgebase, and Chat scene starts, thresholds, and interior midpoints. |
| 81 | `session-81-p1-interior-reveal-scenes-9-14` | Interior Reveal Pass, Scenes 9-14 | P1 | Tune Leaderboard, Relationships, Career, Recovery, Analytics, and Nutrition scene starts, thresholds, and interior midpoints. |
| 82 | `session-82-p1-full-journey-flow-pass` | Full Journey Flow Pass | P1 | Smooth the complete 17-scene scroll, especially the SIA/Fitness, Analytics/Nutrition, Climax/Product, and Product/Closing transitions. |
| 83 | `session-83-p1-p2-qa-evidence-harness` | QA Evidence Harness | P1/P2 | Restore stable DOM, canvas, console, and visual capture evidence for the heavy WebGL app. |
| 84 | `session-84-final-demo-readiness-audit` | Final Demo Readiness Audit | P1/P2 | Re-score the repaired app, require 12 / 12 interaction coverage, 0 console warnings/errors, no P0s, and target an overall score at or above 8.0 / 10. |

Current next session: Session 89, `session-89-final-phase-10-qa`.

Session 89 task checklist:

- Continue Phase 10 Architectural Completion from `apps/balencia/PHASE-10-BACKLOG.md`.
- Run final Phase 10 QA across all 12 approved overview exteriors and all focused-scene hero exterior LODs.
- Preserve approved overview exteriors, hero exteriors, current layout positions, baked energy endpoints, Phase 9 app behavior, and the current overview LOD policy.
- Rebuild or verify before/after contact sheets, app hero-camera evidence, clean GLB reimport QA, `exteriorHero` manifest entries, runtime focused-scene loading, and performance budgets.
- Keep overview scenes under 250K drawn tris, focused hero scenes under 270K drawn tris, and require no structure to read as scaffolded or unfinished.

## Prompt Generation

1. Load `quick-context` plus only the needed `MASTER-CONTEXT.md` sections by anchor.
2. For Phases 1-6, read the module `SPEC.md` in full and the current `REVIEW.md` for previous sessions or fix instructions.
3. For Phase 7 or Phase 9 app work, read `SCROLL-JOURNEY.md`, `BALENCIA-CURRENT-AUDIT.md` when present, the relevant `apps/balencia/src` files, and the latest app/session report instead of a module `SPEC.md`.
4. Extract variables from the SPEC or audit, REVIEW/session report, current session number, material slot table when relevant, and build order.
5. Interpolate the chosen template from `PROMPT-TEMPLATES.md`, or create a concise app-repair prompt when no template fits.
6. Keep the final session prompt around 150-200 lines and avoid inlining unrelated context.

## Execution Safety

- In plan mode, only produce a plan or build prompt. Do not mutate files.
- For live Blender work, verify available tools such as `execute_blender_code` or an approved Blender runner.
- Do not install Blender MCP automatically. If the needed Blender tool is unavailable, stop and state the setup required.
- Use named roles like `DESIGN-05` and `DESIGN-08` only when corresponding tools or agents are actually available; otherwise perform the role locally or prepare a handoff prompt.
- After QA failure, include fix instructions in the next prompt and retry at most 2 times for the same gate before escalating.
- During Phase 9, do not modify approved GLBs, assembly Blender files, or historical progress artifacts unless the active session explicitly calls for it and QA evidence justifies the change.

## State Updates

Update `PROGRESS.md` and the module `REVIEW.md` only after an executed build and QA result justify the change. Recalculate summary counters from the Structure Status table and approved artifacts instead of hand-editing stale numbers.
For Phase 9, update `PROGRESS.md`, `BUILD-ORDER.md`, and the relevant app session report after each executed repair session. Advance `current_session` and `next_batch` only after the session's acceptance checks pass.
