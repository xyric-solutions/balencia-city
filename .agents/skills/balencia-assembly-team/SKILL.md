---
name: balencia-assembly-team
description: "Assemble and verify the full Balencia City after all structures and energy assets are approved. Use for full-city orbital layout, 17-scene camera verification, city-wide cohesion, and Phase 6 assembly QA."
---

# Balencia Assembly Team

## Purpose

Place all approved structures and energy assets into the full city, verify scale and skyline cohesion, capture scroll-journey camera checks, and prepare the scene for the R3F app phase.

## Required Context

- Confirm Phase 6 readiness in `PROGRESS.md` and `BUILD-ORDER.md`.
- Read `MASTER-CONTEXT.md` sections `quick-context`, `structures`, `layout`, and `appendix-b`.
- Read `SCROLL-JOURNEY.md` for all 17 scene targets.
- Read `QUALITY-RUBRIC.md`, especially Gate 6 and assembly performance guidance.
- Use approved GLBs only from module and energy `approved/` folders.

## Workflow

1. Verify all 12 structures have approved exterior and interior GLBs before final assembly.
2. Place structures at orbital positions from `MASTER-CONTEXT.md` and preserve SIA Tower dominance.
3. Add approved pipelines, special delivery geometry, cross-connections, and pulse geometry.
4. Capture overview, skyline, cardinal, and 17 scene-specific screenshots.
5. Audit total triangle count, file size, material consistency, detail density, and scene readability.
6. Write assembly findings to `assembly/REVIEW.md` and performance notes to `assembly/performance-reports/` when generated.

## Tooling Rules

- Use Blender MCP only when live Blender tools are available. Do not install Blender MCP automatically.
- If visual tooling is unavailable, report that assembly QA cannot be completed and provide a static readiness checklist.
- Treat any named role as a responsibility; continue locally if that role is not a callable tool.

## Outputs

- Draft assembly scene: `assembly/drafts/full-city-assembly.blend`.
- Screenshots: `assembly/screenshots/` and `assembly/scroll-verification/`.
- Performance reports: `assembly/performance-reports/`.
- Final verdict: `assembly/REVIEW.md`.
