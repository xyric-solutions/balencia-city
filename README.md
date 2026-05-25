# Balencia City v3

Premium 3D cinematic city — SIA Life Coach civilization.
12 structures (SIA Tower + 11 districts), 17-scene scroll journey.

## Quick Start

1. Read `MASTER-CONTEXT.md` (the bible — read every session)
2. Read `BUILD-ORDER.md` for current phase
3. Check `PROGRESS.md` for what's done/next
4. Start a session using `SESSION-TEMPLATES.md`

## Before ANY Session

1. Open Blender with MCP addon enabled
2. Run `shared/lighting-rig.py` via `execute_blender_code`
3. Run `shared/material-library.py` with district color hex
4. Read the target module's `SPEC.md`
5. Collect reference images in `modules/NN-name/references/`

## Session Types
1. Exterior — Build outside of one structure
2. Interior — Build inside (after exterior approved)
3. Energy Pipeline — Build SIA→district connection
4. Cross-Connection — Build gold district↔district lines
5. Integration — Verify new structure with all approved ones
6. Scroll Verification — Test 17 camera positions

## Key Rules
- ONE module at a time. No parallel building.
- Exterior MUST be approved before starting interior.
- Every structure passes 7 quality gates before moving on.
- Per-object decimation only (never join-then-decimate).
- 7-slot material system: base, accent, glass, detail, emissive, energy, holo.

## Structure
See folder tree in MASTER-CONTEXT.md Section 9.
