---
name: balencia-qa
description: "Run Balencia City quality review workflows. Use when the user types /balencia-qa, asks for module QA, city-wide cohesion QA, energy pipeline QA, standalone quality gates, or review of approved Balencia assets."
---

# Balencia QA

## Alias

Treat `/balencia-qa` as the human-facing alias for this skill. `$balencia-qa` may be invoked explicitly.

## Modes

- `{NN}-{slug}`: review a single module.
- `all`: review city-wide cohesion across approved structures.
- `energy`: review approved or draft energy-system assets.

## Shared Inputs

- Read `QUALITY-RUBRIC.md` for gates and energy checks.
- Read the target `SPEC.md` and `REVIEW.md`.
- For city-wide QA, read `MASTER-CONTEXT.md` layout and approved GLB paths.
- For energy QA, read `energy-system/SPEC.md` and target module energy delivery styles.

## Tooling Preflight

- Use live Blender tools only when available, such as `execute_blender_code`, viewport screenshots, or an approved command-line Blender runner.
- Do not install Blender MCP automatically.
- If visual tooling is unavailable, offer a static audit and clearly label it as not a full visual QA pass.
- Do not append to `REVIEW.md` unless the user requested an executed QA pass and the evidence supports the verdict.

## Single Module QA

1. Load the approved exterior and interior GLBs for the module, or draft GLBs if the user explicitly asks to review drafts.
2. Run Gates 1-7 as applicable:
   - Exterior: Gates 1-6.
   - Interior: Gates 3-5 and 7.
   - Integration: Gate 6.
3. Capture screenshots from relevant angles when visual tools are available.
4. Report PASS, APPROVED WITH EXCEPTIONS, or NEEDS FIX with gate-specific notes.

## City-Wide QA

1. Load approved exterior GLBs at orbital positions.
2. Run Gate 6 against material darkness, detail density, scale, and SIA Tower dominance.
3. Capture overview, cardinal, and top-down screenshots when possible.
4. Write or summarize findings for `assembly/REVIEW.md` only when the QA pass is actually executed.

## Energy QA

1. Load SIA Tower, target districts, and energy assets.
2. Verify endpoint connections, arced paths, delivery style, ground veins, material names, and special effects.
3. Report each pipeline or connection independently, then provide an overall verdict.
