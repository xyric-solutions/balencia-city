---
name: balencia-energy-team
description: "Build and review Balencia City energy pipelines, AI pulse geometry, cross-district gold connections, and shader handoff notes. Use when connecting SIA Tower to districts, building energy-system assets, or entering Phase 5."
---

# Balencia Energy Team

## Purpose

Build the visual nervous system after structures are approved: SIA-to-district pipelines, special delivery effects, cross-district gold connections, and the AI pulse ring.

## Required Context

- Read `PROGRESS.md` and `BUILD-ORDER.md` to confirm Phase 5 is valid.
- Read `energy-system/SPEC.md` and, for cross-connections, `energy-system/cross-connections/SPEC.md`.
- Read the target module `SPEC.md` for the energy delivery style.
- Read `MASTER-CONTEXT.md` section `energy` and `shared/energy-pipeline-utils.py` before geometry work.
- Use approved structure GLBs from `modules/*/{exterior,interior}/approved/` for endpoint positions.

## Workflow

1. Verify SIA Tower and the target district are approved before building a pipeline.
2. Build hard pipelines, warm mist, faint thread, waterfall, or lightning delivery based on the module SPEC.
3. Add ground energy veins at each endpoint and ensure pipeline materials use the `energy` slot.
4. Build cross-district gold connections only after all relevant districts are approved.
5. Document shader and runtime parameters in `energy-system/SHADER-PARAMS.md` when shader work begins.
6. Run the Energy Integration Check from `QUALITY-RUBRIC.md` before promoting any energy asset.

## Tooling Rules

- Use Blender MCP only when live Blender tools are available. Do not install Blender MCP automatically.
- If Blender is unavailable, prepare a precise build prompt or static audit instead of pretending visual QA was performed.
- Treat role labels like `DESIGN-05`, `DESIGN-07`, and `DESIGN-08` as responsibilities, not guaranteed tools.

## Outputs

- Pipeline drafts: `energy-system/pipelines/drafts/`.
- Approved pipelines: `energy-system/pipelines/approved/`.
- Approved cross-connections: `energy-system/cross-connections/approved/`.
- Approved pulse geometry: `energy-system/pulse/approved/`.
- QA results: `energy-system/REVIEW.md`.
