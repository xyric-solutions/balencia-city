# Session 46: Nutrition - Organic Farm-Structure - Exterior Detail, Polish & Export

## Quick Context

- Project: Balencia City v3, an interactive cinematic 3D city.
- Aesthetic: dark premium night architecture, Apple spatial computing clarity, UE5 archviz weight.
- Avoid: toy proportions, neon overload, daytime, cartoon, suburban greenhouse scale.
- Sky/world: Ink-blue `#0A0A0F`; structural surfaces stay dark and premium.
- SIA Tower: central 100+ floor anchor, roughly 40u tall; all districts remain clearly shorter.
- Materials: runtime reads exact slot names: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Export: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center.

## Session Scope

- Module: #11 Nutrition - Organic Farm-Structure.
- Position: Phase 4, Step 4.4.
- District color: Warm Amber `#D97706`.
- Focus: exterior detail, market/greenhouse polish, material proof, dark-first proof, cohesion proof, Draco GLB export.
- Final budget: Exterior 12K-18K tris; hard reject above 18K.
- Previous session tris: 10,552.
- Remaining budget: 7,448 tris.
- Source blend: `modules/11-nutrition/exterior/drafts/nutrition-s45-major-forms.blend`.
- Output blend: `modules/11-nutrition/exterior/drafts/nutrition-s46-detail-export.blend`.
- Output GLB: `modules/11-nutrition/exterior/drafts/nutrition-ext-draft-s46.glb`.
- Energy slots: energy=true, holo=false.

## Previous Session State

Session 45 approved Gates 1-2. It established the 12-floor rounded farm-pyramid
body, open market base, greenhouse volumes, cascading plant curtains, amber
grow-light bands, irrigation channels, roof kitchen vent, and rear SIA hard
pipeline receiver socket.

Preserve the living vertical-farm silhouette. This pass increases detail density
and technical readiness without changing the approved stepped profile.

## QA Fix Instructions

No failed Gates 1-2 fixes are required. Preserve the green/amber living-farm read
while strengthening dark-first legibility and documenting any material distribution
exception caused by Nutrition's SPEC-mandated plant coverage.

## Detail Elements To Add

- Tier edge polish: dark shadow ledges, farm-bed dividers, terrace lips, and floor indicators.
- Greenhouse detail: deeper mullions, internal hydroponic racks, seedling trays, and warm roof caps.
- Foliage refinement: varied vine strands, leaf planes, and cascading plant density without hiding the stepped form.
- Irrigation hardware: thin troughs, downspouts, valve nodes, and visible water-routing detail.
- Open market polish: produce crates, amber-lit stall faces, canopy braces, and entrance signage placeholders.
- Roof and socket polish: vent fins, guard rails, service pads, receiver lugs, and restrained orange energy detail.
- Dark-first proof: enough base/detail structure remains readable with all emission set to zero.
- All-built-structures cohesion proof with SIA plus modules 01-11 exterior assets.

## Material Assignment

| Surface | Slot | Notes |
|---------|------|-------|
| Tiered structure walls and market base | base | Warm dark structural mass, inactive-readable |
| Cascading plants and produce forms | accent | Green living elements, SPEC-critical identity |
| Greenhouse enclosures | glass | Amber-tinted transparent volumes |
| Farm beds, mullions, irrigation, vent, rails | detail | Dark mechanical/agricultural detail |
| Amber grow lights and market light strips | emissive | Warm amber `#D97706`, restrained until active |
| SIA hard-pipeline receiver | energy | Orange `#FF5E00`, receiver only |

## Workflow

1. Load `nutrition-s45-major-forms.blend`.
2. Normalize material slots to exactly `base`, `accent`, `glass`, `detail`, `emissive`, `energy`; no `holo`.
3. Add terrace, greenhouse, foliage, irrigation, market, roof, and receiver details.
4. Verify final source tris land inside 12K-18K before export.
5. Save `nutrition-s46-detail-export.blend`.
6. Render final front, three-quarter, distance, and dark-first screenshots.
7. Export packed Draco GLB to drafts, copy to approved only after validation passes.
8. Re-import the GLB and verify materials, transforms, file size, and no lights/cameras.
9. Render all-twelve exterior cohesion screenshot with SIA plus modules 01-11.
10. Write `session46-metrics.json` and `session46-qa-import.json`.

## QA Gates

Gate 3 - Material Compliance:

- Only `base`, `accent`, `glass`, `detail`, `emissive`, and `energy` are present.
- No default gray or unnamed materials remain.
- Nutrition may require a documented plant-coverage exception because the visible living farm is SPEC-critical.

Gate 4 - Dark-First Test:

- With emission strength set to zero, the stepped terraces, market base, greenhouse boxes, roof vent, and plant silhouettes still read.
- Amber should not carry the whole design.

Gate 5 - Technical Budget:

- Final exterior tris must be between 12K and 18K.
- GLB must fit the 100-350 KB exterior file budget.
- Export must have bottom-centered origin, applied transforms, and no cameras/lights.

Gate 6 - Cohesion Check:

- Place Nutrition with all approved exterior structures through Analytics.
- Verify consistent dark material tone, skyline scale, and detail density.
- SIA remains the tallest landmark.

## What Not To Do

- Do not build the Nourishment Hall interior.
- Do not model the Phase 5 SIA-to-Nutrition pipeline.
- Do not alter approved neighboring modules.

## End Criteria

- Detail `.blend`, draft GLB, approved GLB, metrics JSON, and QA import JSON are saved.
- Four Nutrition screenshots plus one all-built-structures cohesion screenshot exist.
- `REVIEW.md` records Session 46 actions, metrics, screenshots, gate results, and verdict.
- `PROGRESS.md` advances to Session 47 / Nutrition interior only after approval.
