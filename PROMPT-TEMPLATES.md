---
type: prompt-templates
title: Balencia City v3 — Interpolatable Session Prompt Templates
status: Active
project: balencia-city-v3
owner: hamza
last_updated: 2026-05-23
kb_summary: 5 interpolatable prompt templates for /balencia-build dynamic prompt assembly.
---

# Balencia City v3 — Prompt Templates

> These templates are consumed by the `/balencia-build` command. They are never used
> directly. The build command assembles a full prompt by combining:
>
> - **Tier 1** (~12 lines): Quick Context block from MASTER-CONTEXT.md
> - **Tier 2** (~30-50 lines): Relevant MASTER-CONTEXT sections loaded by `<!-- section:X -->` anchors
> - **Tier 3** (~90-140 lines): One of the templates below, interpolated with SPEC/REVIEW variables
>
> Assembled prompt target: 150-200 lines total.

---

## Context Loading Map

Which MASTER-CONTEXT `<!-- section:X -->` anchors each template needs (Tier 2):

| Template | Required Sections |
|----------|-------------------|
| A: Exterior Major Forms | `quick-context`, `materials`, `constraints`, `lighting` |
| B: Exterior Detail + Polish + Export | `quick-context`, `materials`, `constraints` |
| C: Interior | `quick-context`, `materials`, `interiors`, `constraints` |
| D: Integration Test | `quick-context`, `structures`, `layout`, `build-sequence` |
| E: Combined Exterior | `quick-context`, `materials`, `constraints`, `lighting` |

---

## Variable Extraction Guide

Where the build command finds each variable:

### From SPEC.md — Identity Block

```yaml
# Parse the Identity section at the top of each module's SPEC.md
NN:            Module number from "**Module**: #NN"
MODULE_NAME:   Full name from the H1 heading (e.g., "Fitness District -- Gym Megastructure" → "Fitness")
SLUG:          Kebab-case from folder name (e.g., "01-fitness" → "fitness")
HEX:           Color hex from "**Color**: Name `#XXXXXX`"
COLOR_NAME:    Color name from "**Color**: Name `#XXXXXX`"
FLOORS:        Floor count from "**Floors**: N"
EXT_BUDGET:    Exterior tri budget from "**Tri Budget**: Exterior XXXK-XXXK"
INT_BUDGET:    Interior tri budget from "**Tri Budget**: ... Interior XXXK-XXXK"
ENERGY_STYLE:  Delivery style from "**Energy Delivery**: ..."
USES_ENERGY:   True if "energy" appears in SPEC material table or Identity
USES_HOLO:     True if "holo" appears in SPEC material table or Identity
```

### From SPEC.md — Content Blocks

```yaml
# Extract multi-line content from specific SPEC.md sections
EXTERIOR_DESCRIPTION:  The paragraph(s) under "## Exterior Architecture > ### Description"
KEY_ELEMENTS:          The bulleted list under "### Key Architectural Elements"
SILHOUETTE_MARKERS:    The paragraph under "### Silhouette Markers"
MATERIAL_TABLE:        The markdown table under "### Material Assignment"
INTERIOR_DESCRIPTION:  The paragraph(s) under "## Interior > ### Description"
FOCAL_POINT:           The paragraph under "### Focal Point"
PROPS_LIST:            The bulleted list under "### Supporting Props"
LIGHT_EMPTIES:         The bulleted list under "### Light Empties"
CAMERA_TARGET:         The paragraph under "### Camera Target"
```

### From REVIEW.md — Previous Session State

```yaml
# Extract from the module's REVIEW.md after a completed session
PREV_SESSION:       Summary block written at end of previous session (tri count, object list, notes)
BLEND_PATH:         Path to .blend file recorded in REVIEW.md
PREV_TRIS:          Total triangle count from previous session
FIX_INSTRUCTIONS:   Content from "### Fix Instructions" if QA gate failed (empty string if none)
SESSION_NUMBER:      Current session number from PROGRESS.md frontmatter
```

### Computed at Assembly Time

```yaml
PHASE_POSITION:      Derived from BUILD-ORDER.md (e.g., "Phase 2, Module 2 of 3")
REMAINING_BUDGET:    EXT_BUDGET max minus PREV_TRIS (only relevant for Template B)
```

---

## Template A: Exterior Major Forms

> **Purpose**: First exterior session — build primary silhouette geometry only.
> **When**: Module has no prior exterior work. Starting from empty scene.
> **Target body**: ~100 lines.

```
# Session {SESSION_NUMBER}: {MODULE_NAME} — Exterior Major Forms

## Session Scope

- **Module**: #{NN} {MODULE_NAME}
- **Position**: {PHASE_POSITION}
- **District Color**: {COLOR_NAME} `{HEX}`
- **Floors**: {FLOORS}
- **Focus**: Primary silhouette geometry — major architectural forms ONLY
- **Budget**: Under 60% of {EXT_BUDGET} tris (leave headroom for detail session)
- **Energy slots**: energy={USES_ENERGY}, holo={USES_HOLO}
- This session: major forms. Next session: detail, polish, decimation, export.

## Architectural Identity

{EXTERIOR_DESCRIPTION}

**Silhouette signature**: {SILHOUETTE_MARKERS}

This structure must be visually distinct from every previously built module. Compare
silhouettes after construction — if this building could be mistaken for any neighbor
at 200px viewport height, the forms need more differentiation.

## Scene Preparation

1. Clear the Blender scene completely (remove default cube, camera, light).
2. Run `shared/lighting-rig.py` to establish the 3-point cinematic rig.
3. Run `shared/material-library.py` with color `{HEX}`, include_energy={USES_ENERGY}, include_holo={USES_HOLO}.
4. Verify the scene contains exactly 3 lights and the correct number of materials.
5. Confirm world background is set to `#0A0A0F`.

If the lighting script fails on your Blender version, set up lights manually per
MASTER-CONTEXT Section 6.

## What To Build

Build ONLY these major form elements. No fine decorative detail yet.

{KEY_ELEMENTS}

**Dimensions guidance**: This is a {FLOORS}-floor structure. Using the SIA Tower as
reference (~40 units for 100+ floors), this building should stand approximately
{FLOORS} * 0.4 = ~{FLOORS * 0.4} units tall. Adjust proportions until the building
reads as a metropolitan megastructure, not a suburban house.

For each element:
- Build the primary volume first (box, cylinder, or custom mesh)
- Apply subdivision or smoothing only where the SPEC calls for organic forms
- Name the object descriptively (e.g., `main_body`, `crown`, `entrance_portal`)
- Assign the correct material slot immediately after creation

**Critical**: Major forms define the silhouette. Get the proportions and relative
scales right before moving on. If the overall shape does not read correctly from
a distance, no amount of detail will save it.

## Material Assignment

{MATERIAL_TABLE}

Assign materials as you build — do not defer to the end. Material slot names must
match exactly: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
The runtime app overrides all material properties by these names. Geometry quality
matters; baked textures do not.

## Workflow

Follow this exact sequence. Do not skip steps.

1. **Clear scene** — remove all default objects.
2. **Lighting** — run lighting-rig.py, verify 3 lights present.
3. **Materials** — run material-library.py with `{HEX}`, verify material count.
4. **Build element 1** (primary structural body) — assign materials.
5. **Build element 2** (secondary structure / crown) — assign materials.
6. **Build remaining elements** — one at a time, materials assigned on creation.
7. **Checkpoint screenshot** — front elevation view. Does the silhouette read?
8. **Silhouette evaluation** — take screenshots from 3 angles:
   - Front elevation (identifies floor count and vertical proportion)
   - 3/4 angle (reveals depth and cantilevers/overhangs)
   - Distance view (tests recognition at thumbnail scale)
9. **Proportion iteration** — if any angle fails the silhouette test, adjust
   scales and retake. Do not proceed until the form reads correctly.
10. **Scale comparison** (recommended) — import a previously approved structure,
    place offset at (30, 0, 0), verify relative heights and material darkness
    consistency. Delete the import after comparison.

## Session Scope — What NOT To Do

Do not attempt any of the following in this session:
- No fine decorative detail (trim, signage, secondary ornamentation)
- No interior modeling
- No energy pipeline geometry
- No decimation or GLB export
- No downloading reference models (build from scratch)
- No prop-level objects (furniture, equipment, vegetation)

## End Criteria

This session is DONE when:
- [ ] 3+ viewport screenshots taken from different angles
- [ ] Silhouette is distinctive — cannot be confused with any previously built module
- [ ] Building reads as a {FLOORS}-floor megastructure (not suburban scale)
- [ ] All objects have materials assigned from the 7-slot set
- [ ] Total tris are under 60% of {EXT_BUDGET} budget
- [ ] The .blend file is saved to `modules/{NN}-{SLUG}/exterior/drafts/`

## Post-Session

Update `modules/{NN}-{SLUG}/REVIEW.md`:
- Record total tri count per object
- Record .blend file path
- List screenshots taken and their locations
- Note any proportion decisions or deviations from SPEC
- Describe what the detail session (Template B) will add
```

---

## Template B: Exterior Detail + Polish + Export

> **Purpose**: Second exterior session — add detail, polish geometry, decimate to budget, export GLB.
> **When**: Major forms session (Template A) is complete. REVIEW.md has previous session state.
> **Target body**: ~110 lines.

```
# Session {SESSION_NUMBER}: {MODULE_NAME} — Exterior Detail, Polish & Export

## Session Scope

- **Module**: #{NN} {MODULE_NAME}
- **Position**: {PHASE_POSITION}
- **District Color**: {COLOR_NAME} `{HEX}`
- **Focus**: Detail elements, polish, decimation, GLB export
- **Final Budget**: {EXT_BUDGET} tris (hard cap — export will be rejected above this)
- **Previous session tris**: {PREV_TRIS}
- **Remaining budget**: {REMAINING_BUDGET} tris available for detail geometry

## Previous Session State

**Blend file**: `{BLEND_PATH}`

{PREV_SESSION}

Load the .blend file above. Verify the scene matches the previous session summary
before making any changes. If objects are missing or tri counts differ significantly,
investigate before proceeding.

### QA Fix Instructions

{FIX_INSTRUCTIONS}

> If the block above is empty, no QA fixes are required — proceed with detail work.
> If fix instructions are present, complete ALL fixes FIRST before adding new detail.
> Take a screenshot after fixes to confirm resolution.

## Detail Elements To Add

Add these elements that were intentionally deferred from the major forms session.
Each element should enhance the building's character without breaking the established
silhouette.

Candidates from SPEC (add what is appropriate within remaining budget):
- Decorative trim and edge details on primary surfaces
- Signage geometry (illuminated panel placeholders for emissive slot)
- Secondary structural elements (brackets, supports, connectors)
- Ground-level detail (entrance features, walkways, planters)
- Crown/rooftop detail (mechanical housing, antenna, beacon mounts)
- Facade subdivision (window mullions, panel lines, floor edge markers)
- Any SPEC elements not built in the major forms session

**Budget discipline**: Each detail element should be estimated before building.
If adding an element would exceed {REMAINING_BUDGET} tris, skip it or simplify.
Detail serves the silhouette — it should not compete with major forms.

## Polish Checklist

After all detail is added, verify each item:

- [ ] All materials assigned — no default gray or unnamed materials remain
- [ ] Material names match slot regex patterns exactly
- [ ] Proportions still read correctly — detail has not distorted the silhouette
- [ ] No floating geometry (all elements visually connected or intentionally hovering)
- [ ] No overlapping faces (z-fighting visible in viewport)
- [ ] No inverted normals (check with face orientation overlay)
- [ ] All objects named descriptively (not "Cube.001", "Cylinder.003")
- [ ] Origin of the entire structure is at bottom-center (0, 0, 0), Y-up
- [ ] All transforms applied (Ctrl+A → All Transforms on every object)
- [ ] Building reads correctly with emissive at 0 (dark-first test)

## Decimation & Budget

Decimate per-object to bring total within {EXT_BUDGET}:

1. Run `get_scene_info` to list all objects with tri counts.
2. Identify the highest-tri objects — these are decimation candidates.
3. Apply Decimate modifier (Collapse mode) per object. Start with ratio 0.8, adjust.
4. **CRITICAL**: Per-object decimation ONLY. Never join meshes then decimate.
5. After each decimation, check:
   - Does the object's silhouette still read? If not, undo and use a gentler ratio.
   - Are sharp architectural edges preserved? Use "Triangulate" or edge crease if needed.
6. Small detail objects (railings, antennas) tolerate heavier decimation than the main body.
7. Verify total tris across all objects falls within {EXT_BUDGET}.
8. Take a final screenshot — compare to pre-decimation screenshot for quality loss.

## Export

1. Run `shared/export-pipeline.py` with max_tris set to the upper bound of {EXT_BUDGET}.
2. The script applies Draco compression level 6, Y-up, strips cameras and lights.
3. Verify the exported GLB:
   - File size within SPEC budget
   - Opens without errors
   - No cameras or lights embedded
   - Origin at bottom-center
4. Save GLB to `modules/{NN}-{SLUG}/exterior/drafts/{SLUG}-ext-draft-{SESSION_NUMBER}.glb`

## Workflow

1. **Load .blend** from `{BLEND_PATH}`.
2. **Apply QA fixes** (if any) — screenshot after.
3. **Add detail elements** — one at a time, assign materials immediately.
4. **Checkpoint screenshot** — 3/4 angle showing new detail.
5. **Run polish checklist** — fix any issues found.
6. **Decimate** — per-object, verify silhouette after each.
7. **Export GLB** — run export-pipeline.py.
8. **Final screenshots** — front elevation, 3/4 angle, distance view.
9. **Save .blend** to drafts folder.

## Session Scope — What NOT To Do

- No interior modeling (separate session, Template C)
- No energy pipeline geometry (Phase 5)
- No placing this structure into the city layout (Integration Test, Template D)

## End Criteria

This session is DONE when:
- [ ] All detail elements from SPEC are added (or documented as cut for budget)
- [ ] Polish checklist is fully passed
- [ ] Total tris within {EXT_BUDGET}
- [ ] GLB exported with Draco compression, verified
- [ ] 3+ final screenshots taken
- [ ] .blend and .glb saved to correct paths

## Post-Session

Update `modules/{NN}-{SLUG}/REVIEW.md`:
- Record final tri count per object
- Record .blend and .glb file paths
- List detail elements added and any elements cut for budget
- Note decimation ratios applied per object
- Mark exterior QA gates ready for review
```

---

## Template C: Interior

> **Purpose**: Build the single interior room for a module.
> **When**: Exterior is APPROVED (not just drafted — must pass all QA gates).
> **Target body**: ~120 lines.

```
# Session {SESSION_NUMBER}: {MODULE_NAME} — Interior

## Session Scope

- **Module**: #{NN} {MODULE_NAME}
- **Position**: {PHASE_POSITION}
- **District Color**: {COLOR_NAME} `{HEX}`
- **Focus**: Single interior room — focal element, props, empties, export
- **Budget**: {INT_BUDGET} tris (separate GLB from exterior)
- **Energy slots**: energy={USES_ENERGY}, holo={USES_HOLO}

## Room Description

{INTERIOR_DESCRIPTION}

The interior is loaded on demand when the user scrolls into this district's scene.
It should feel like a curated peek inside — intimate but connected to the larger city.
Warm ambient lighting through the open/windowed wall creates silhouette depth against
the city night.

## Focal Element

{FOCAL_POINT}

This is the hero object of the room. It must be:
- Clearly the center of attention — the eye lands here first
- Positioned where the `camera_target` empty will point
- The highest-detail object in the room (allocate ~25-30% of interior tri budget)
- Recognizable at low poly count — silhouette clarity over surface detail

Build the focal element FIRST, before any props. If the focal element does not
command attention on its own, no arrangement of props will fix it.

## Props List

{PROPS_LIST}

Props are supporting elements that establish the room's function and atmosphere.

For each prop:
- Build at minimal viable detail — the silhouette must be readable, not photorealistic
- Allocate roughly equal tri budget per prop (~5-10% of {INT_BUDGET} each)
- Name objects descriptively (e.g., `bookshelf_01`, `desk_main`)
- Assign materials immediately on creation
- Place props to frame the focal element, not compete with it

**Arrangement principle**: Props should guide the viewer's eye toward the focal element.
Place larger props at the periphery, smaller ones closer to the focal point. Leave
breathing room — an interior that feels cluttered fails the design intent.

## Required Empties

These empties define where the runtime app places lights and aims the camera.
They are exported in the GLB but carry no geometry.

### Light Empties (3 required)

{LIGHT_EMPTIES}

Create 3 empties named exactly `light_0`, `light_1`, `light_2`. Place them at the
positions described above. The runtime app reads these positions to set up interior
lighting — incorrect placement means bad lighting in the final experience.

### Camera Target (1 required)

{CAMERA_TARGET}

Create 1 empty named exactly `camera_target`. Place it at the described position.
This is where the interior camera will aim — the composition of the entire room
view depends on this placement.

## Material Assignment

{MATERIAL_TABLE}

Use the same 7-slot naming system as exteriors. The runtime overrides all material
properties by slot name. Interior materials use the same slots but may have different
surface distribution (more `detail` for furniture, less `base` for walls).

## Scene Preparation

1. Start a FRESH Blender scene — do not model the interior inside the exterior .blend.
2. Run `shared/lighting-rig.py` (or set up manually if script has compatibility issues).
3. Run `shared/material-library.py` with color `{HEX}`, include_energy={USES_ENERGY}, include_holo={USES_HOLO}.
4. Verify lights and materials are present before building.

The interior is a SEPARATE GLB from the exterior. It will be loaded independently
at runtime and positioned programmatically inside the exterior shell.

## Workflow

Follow this exact sequence:

1. **Clear scene** — fresh start, no geometry from previous work.
2. **Lighting + materials** — run setup scripts, verify.
3. **Build room shell**:
   - Floor plane (flat, sized to SPEC dimensions)
   - 3 walls (back + 2 sides) — simple box geometry, appropriate height
   - Ceiling (flat plane matching floor)
   - **One wall open or windowed** — this lets city light in and connects
     the interior to the exterior world. Which wall is open depends on
     where the exterior camera approaches from.
   - Assign `base` material to floor, walls, ceiling.
4. **Build focal element** — the hero object. Assign materials. Position at
   the room's visual center.
5. **Take checkpoint screenshot** — does the focal element command attention?
   If not, adjust scale or position before adding props.
6. **Build props** — add 4-8 props one at a time. Assign materials. Arrange
   to frame the focal element.
7. **Place empties** — `light_0`, `light_1`, `light_2`, `camera_target`.
   Verify names are exact.
8. **Material audit** — every object has a named material from the 7-slot set.
   No default gray, no unnamed materials.
9. **Dark-first test** — set all emissive to 0. Does the room read as a
   recognizable space? District color should appear only on emissive/accent slots.
10. **Decimate** — per-object to {INT_BUDGET}. Focal element gets gentler
    decimation; background props can be more aggressive.
11. **Export GLB** — run `shared/export-pipeline.py`. Verify empties are present
    in the export (they should be — empties export as nodes).
12. **Final screenshots** — from camera_target perspective and from the open wall
    looking in.

## Session Scope — What NOT To Do

- No exterior modifications (exterior is approved and locked)
- No energy pipeline geometry (Phase 5)
- No modeling multiple rooms (one room per module)
- No high-poly surface detail (props should be silhouette-readable, not photorealistic)

## End Criteria

This session is DONE when:
- [ ] Room shell complete (floor, 3 walls, ceiling, 1 open/windowed wall)
- [ ] Focal element built and clearly dominant
- [ ] 4-8 props placed, each identifiable by silhouette
- [ ] `light_0`, `light_1`, `light_2` empties placed at logical positions
- [ ] `camera_target` empty placed at focal point
- [ ] All materials assigned from 7-slot set
- [ ] Dark-first test passed
- [ ] Total tris within {INT_BUDGET}
- [ ] GLB exported and verified (empties present, no cameras/lights)
- [ ] .blend and .glb saved to `modules/{NN}-{SLUG}/interior/drafts/`

## Post-Session

Update `modules/{NN}-{SLUG}/REVIEW.md`:
- Record interior tri count per object
- Record .blend and .glb file paths
- Confirm empty names and positions
- Mark interior QA gates (Gate 3, 4, 5, 7) ready for review
```

---

## Template D: Integration Test

> **Purpose**: Verify exterior + interior work together and check scroll-journey camera scenes.
> **When**: Both exterior and interior are APPROVED for this module.
> **Target body**: ~70 lines.

```
# Session {SESSION_NUMBER}: {MODULE_NAME} — Integration Test

## Session Scope

- **Module**: #{NN} {MODULE_NAME}
- **Position**: {PHASE_POSITION}
- **Focus**: Verify ext + int alignment, camera scene checks, cohesion with neighbors

This is a verification session, not a build session. No new geometry is created.
The goal is to confirm that this module's assets work correctly in context.

## Structures To Load

Import ALL of these approved GLBs into a single Blender scene:

**This module:**
- Exterior: `modules/{NN}-{SLUG}/exterior/approved/{SLUG}-ext.glb`
- Interior: `modules/{NN}-{SLUG}/interior/approved/{SLUG}-int.glb`

**Previously approved structures (for cohesion check):**
Load every structure listed as "Approved" in PROGRESS.md. Place each at its orbital
position from MASTER-CONTEXT Section 3 (City Layout). If exact positions are not yet
defined, use approximate spacing of 30-40 units from the SIA Tower center.

## Alignment Checks

Verify all of the following:

- [ ] Interior fits inside exterior shell — no geometry clipping through walls
- [ ] Interior origin aligns with exterior origin (bottom-center, same Y=0 plane)
- [ ] Interior scale matches exterior scale (1:1 — no rescaling needed)
- [ ] The open/windowed wall of the interior faces outward toward the city
- [ ] Light empties (`light_0`, `light_1`, `light_2`) are inside the room volume
- [ ] `camera_target` empty is inside the room and points at the focal element
- [ ] Applying all transforms on both GLBs produces no unexpected shifts

## Scene Camera Positions

Set up cameras at the positions specified in SCROLL-JOURNEY.md for scenes featuring
this module. For each relevant scene:

1. Position the camera at the described location and angle.
2. Take a viewport screenshot at 1920x1080.
3. Verify:
   - [ ] The target structure is centered or prominently framed
   - [ ] The building reads clearly at this camera distance
   - [ ] No other structure unexpectedly blocks the view
   - [ ] The emotional tone matches the scene description (dramatic, serene, etc.)
   - [ ] Energy pipeline path (if visible in this scene) has a clear arc route
4. Score the scene composition: Pass / Needs Adjustment / Fail.
5. Document any adjustments needed (camera angle, structure position, scale tweak).

## Cohesion Check

If 2+ structures are now approved, verify cross-module consistency:

- [ ] Material darkness is consistent — no building is noticeably brighter or flatter
- [ ] Detail density is comparable — no building has 10x more surface detail than its neighbor
- [ ] Scale relationships are correct — taller buildings read taller, SIA Tower dominates
- [ ] Architectural variety is maintained — each building has a distinct silhouette language
- [ ] All structures feel like they belong to the same dark, premium, cinematic city

Take a wide-angle screenshot showing all approved structures together. This is the
"skyline test" — does the city feel cohesive and varied simultaneously?

## Workflow

1. **Import all approved GLBs** — exterior + interior for this module, all previous modules.
2. **Run lighting-rig.py** — consistent lighting for fair comparison.
3. **Alignment verification** — check int/ext fit, origins, scale.
4. **Camera scene screenshots** — set up each relevant scene camera, screenshot, score.
5. **Cohesion comparison** — skyline test with all structures visible.
6. **Document results** — record scores, issues, and adjustment recommendations.

## Post-Session

Update `modules/{NN}-{SLUG}/REVIEW.md`:
- Record integration test result: PASS / CONDITIONAL PASS / FAIL
- List any alignment issues found and whether they were resolved
- Record scene scores with screenshot paths

Update `PROGRESS.md`:
- Mark module integration status
- Note any city-level adjustments needed (spacing, rotation, scale)
- If this completes a phase, note phase completion date
```

---

## Template E: Combined Exterior (Major Forms + Detail + Export)

> **Purpose**: Single-session exterior build for simpler structures.
> **When**: Module has < 6 key architectural elements AND < 15K tri budget.
> **Combines**: Template A (major forms) + Template B (detail + polish + export).
> **Target body**: ~140 lines.

```
# Session {SESSION_NUMBER}: {MODULE_NAME} — Combined Exterior Build

## Session Scope

- **Module**: #{NN} {MODULE_NAME}
- **Position**: {PHASE_POSITION}
- **District Color**: {COLOR_NAME} `{HEX}`
- **Floors**: {FLOORS}
- **Focus**: Complete exterior in one session — forms, detail, polish, export
- **Budget**: {EXT_BUDGET} tris (hard cap)
- **Energy slots**: energy={USES_ENERGY}, holo={USES_HOLO}
- This module qualifies for combined build (< 6 elements, < 15K budget).

## Architectural Identity

{EXTERIOR_DESCRIPTION}

**Silhouette signature**: {SILHOUETTE_MARKERS}

This structure must be visually distinct from every previously built module.
The silhouette test applies at every checkpoint — if the building could be confused
with any neighbor at 200px viewport height, stop and differentiate.

## Scene Preparation

1. Clear the Blender scene completely (remove default cube, camera, light).
2. Run `shared/lighting-rig.py` to establish the 3-point cinematic rig.
3. Run `shared/material-library.py` with color `{HEX}`, include_energy={USES_ENERGY}, include_holo={USES_HOLO}.
4. Verify the scene contains exactly 3 lights and the correct number of materials.
5. Confirm world background is set to `#0A0A0F`.

If the lighting script fails on your Blender version, set up lights manually per
MASTER-CONTEXT Section 6.

## Phase 1: Major Forms

Build the primary structural elements that define this building's silhouette.

{KEY_ELEMENTS}

**Dimensions guidance**: This is a {FLOORS}-floor structure. Using the SIA Tower as
reference (~40 units for 100+ floors), this building should stand approximately
{FLOORS} * 0.4 = ~{FLOORS * 0.4} units tall. Adjust until it reads as a metropolitan
megastructure.

For each element:
- Build the primary volume first
- Name the object descriptively
- Assign the correct material slot immediately
- Focus on proportions and relative scale — detail comes in Phase 2

## Checkpoint 1: Silhouette Test

Take viewport screenshots from 3 angles:
- Front elevation (vertical proportion, floor count readability)
- 3/4 angle (depth, overhangs, cantilevers)
- Distance view (recognition at thumbnail scale)

**Gate**: Does the silhouette read as a unique building? Is it distinctly different
from every previously approved structure? If not, adjust major forms before proceeding.
Do NOT add detail to a flawed silhouette.

## Phase 2: Detail Layer

With the silhouette confirmed, add secondary elements:
- Decorative trim and edge details
- Signage geometry (emissive slot placeholders)
- Facade subdivision (window mullions, panel lines)
- Ground-level features (entrance detail, planters, walkways)
- Crown/rooftop detail (mechanical housing, beacons)
- Any remaining SPEC elements not covered in Phase 1

**Budget awareness**: Track tri count as you add detail. Each element should be
estimated before building. Stop adding detail when you reach 85% of {EXT_BUDGET}
to leave margin for decimation rounding.

## Checkpoint 2: Detail Verification

Take a 3/4 angle screenshot. Verify:
- [ ] Detail enhances the silhouette without breaking it
- [ ] All materials assigned — no default gray remaining
- [ ] Material slot names match the 7-slot regex patterns
- [ ] Building still reads correctly at distance (detail is subordinate to form)

## Phase 3: Polish + Export

### Polish

- [ ] No floating geometry
- [ ] No overlapping faces or z-fighting
- [ ] No inverted normals
- [ ] All objects named descriptively
- [ ] Origin at bottom-center (0, 0, 0), Y-up
- [ ] All transforms applied (Ctrl+A → All Transforms)
- [ ] Dark-first test passed (readable with all emissive at 0)
- [ ] District color appears ONLY on accent/emissive/energy/holo — never on base or detail

### Decimation

1. List all objects with tri counts (`get_scene_info`).
2. Apply per-object Decimate modifier (Collapse mode).
3. **Never join meshes then decimate** — this destroys architectural detail.
4. Test silhouette after each decimation — if shape is lost, undo and reduce less.
5. Small detail objects tolerate heavier decimation than the main body.
6. Target: total tris within {EXT_BUDGET}.

### Export

1. Run `shared/export-pipeline.py` with the upper bound of {EXT_BUDGET}.
2. Verify GLB:
   - File size within SPEC budget
   - Opens without errors
   - No cameras or lights embedded
   - Origin at bottom-center
3. Save to `modules/{NN}-{SLUG}/exterior/drafts/{SLUG}-ext-draft-{SESSION_NUMBER}.glb`

### Final Screenshots

Take 3 final screenshots:
- Front elevation (post-decimation)
- 3/4 angle (post-decimation)
- Scale comparison with a previously approved structure (recommended)

## Material Assignment

{MATERIAL_TABLE}

Material slot names are the runtime override keys. Name them exactly as specified.
Geometry quality is what matters — the app overrides all material properties.

## Session Scope — What NOT To Do

- No interior modeling (separate session, Template C)
- No energy pipeline geometry (Phase 5)
- No city-layout placement (Integration Test, Template D)
- No downloading reference models (build from scratch)

## End Criteria

This session is DONE when:
- [ ] Silhouette is distinctive at 200px viewport height
- [ ] Building reads as a {FLOORS}-floor megastructure
- [ ] All SPEC elements built (or documented as cut for budget)
- [ ] All materials assigned from 7-slot set
- [ ] Polish checklist fully passed
- [ ] Total tris within {EXT_BUDGET}
- [ ] GLB exported with Draco compression, verified
- [ ] 3+ final screenshots taken
- [ ] .blend and .glb saved to `modules/{NN}-{SLUG}/exterior/drafts/`

## Post-Session

Update `modules/{NN}-{SLUG}/REVIEW.md`:
- Record final tri count per object
- Record .blend and .glb file paths
- List all elements built and any elements cut for budget
- Note decimation ratios applied
- Mark exterior QA gates ready for review (Gates 1-5)
```
