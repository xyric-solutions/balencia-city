---
name: balencia-structure-team
description: "Build and quality-gate one Balencia City structure through exterior, interior, and integration. Use for requests like build the next structure, build module NN-name, continue Balencia structure work, or run the structure lifecycle behind /balencia-build."
---

# Balencia Structure Team

## Purpose

Build one district through its lifecycle: exterior major forms, exterior detail and export, QA, interior, QA, and integration with the approved city set.

## Required Context

- Read `PROGRESS.md` and `BUILD-ORDER.md` to confirm the target module and phase.
- Read `modules/{NN}-{slug}/SPEC.md` in full and `modules/{NN}-{slug}/REVIEW.md` for prior sessions or fix instructions.
- Load only relevant `MASTER-CONTEXT.md` sections:
  - Exterior: `quick-context`, target row from `structures`, material slot definitions, `constraints`.
  - Interior: `quick-context`, `interiors`.
  - Integration: `quick-context`, `structures`, `layout`.
- Read `QUALITY-RUBRIC.md` before QA or promotion.

## Workflow

1. Confirm the current phase from `PROGRESS.md`; do not skip build order.
2. For exterior major forms, create the primary silhouette, scale markers, and 3+ distinct sub-elements before detail work.
3. For exterior detail/export, load the previous exterior `.blend`, add SPEC-driven details, apply the 7-slot material system, export a GLB, and validate against Gates 1-5 plus Gate 6 when 2+ structures exist.
4. For interiors, start a fresh scene, build the room shell, focal point, 4-8 props, `light_0`, `light_1`, `light_2`, and `camera_target`, then validate Gates 3-5 and 7.
5. For integration, import the new approved GLBs with prior approved structures, verify cohesion and scene readability, then update the module `REVIEW.md` and `PROGRESS.md` only after approval.

## Tooling Rules

- Use Blender MCP only when tools such as `execute_blender_code` are available in the current session.
- If Blender MCP is not available, do not install it automatically. Stop and state the needed setup or request approval.
- If named role agents like `DESIGN-05` or `DESIGN-08` are unavailable, perform the equivalent responsibilities locally or generate a handoff prompt.

## Outputs

- Drafts belong in `modules/{NN}-{slug}/{exterior|interior}/drafts/`.
- Approved exports belong in `modules/{NN}-{slug}/{exterior|interior}/approved/` only after QA approval.
- Screenshots belong in `modules/{NN}-{slug}/screenshots/`.
- `REVIEW.md` must record session metrics, screenshots, gate results, exceptions, and final verdict.
