# Session 42: AI Analytics - Data Cathedral - Exterior Detail, Polish & Export

## Quick Context

- Project: Balencia City v3, an interactive cinematic 3D city.
- Aesthetic: dark premium night architecture, Apple spatial computing clarity, UE5 archviz weight.
- Avoid: toy proportions, neon overload, daytime, cartoon, suburban scale.
- Sky/world: Ink-blue `#0A0A0F`; surfaces stay dark and premium.
- SIA Tower: central 100+ floor anchor, roughly 40u tall; all districts remain clearly shorter.
- Materials: runtime reads exact slot names: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Export: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center.

## Session Scope

- Module: #10 AI Analytics - Data Cathedral.
- Position: Phase 4, Step 4.3.
- District color: Teal `#14B8A6`.
- Focus: exterior detail, polish, dark-first proof, cohesion proof, Draco GLB export.
- Final budget: Exterior 12K-18K tris; hard reject above 18K.
- Previous session tris: 5,251.
- Remaining budget: 12,749 tris.
- Source blend: `modules/10-ai-analytics/exterior/drafts/analytics-s41-major-forms.blend`.
- Output blend: `modules/10-ai-analytics/exterior/drafts/analytics-s42-detail-export.blend`.
- Output GLB: `modules/10-ai-analytics/exterior/drafts/analytics-ext-draft-s42.glb`.

## Previous Session State

Session 41 approved Gates 1-2. It established the 30-floor tapered cathedral body,
side aisles, pointed nave roof, central spire and beacon, six flying buttress data
conduits, pointed holographic data windows, dashboard panels, data-waterfall
entrance, observation platforms, and the orange SIA hard-pipeline receiver socket.

Preserve the cathedral silhouette. This pass increases detail density and technical
readiness without changing the major profile.

## QA Fix Instructions

No failed Gates 1-2 fixes are required. Continue with detail work. Preserve the
SPEC-driven `holo` slot for stained-glass data windows even though the older master
slot-usage table lists Analytics as no-holo.

## Detail Elements To Add

- Denser living-wall chart articulation on front, side, and rear facades.
- Facade panel depth: dark floor ledges, vertical ribs, and recessed panel shadows.
- Stronger pointed-arch window frames, mullions, scan lines, and sill/shoulder marks.
- Dark gothic data-lattice overlay on the upper nave and side facades.
- Flying buttress hardware: collars, cable braces, wall sockets, anchor plates, and
  observation-platform railings.
- Crown/spire polish: nested beacon rings, data fins, and small lattice rods.
- Data-waterfall entrance detail: falling packet clusters, threshold rails, and
  teal side channels.
- Ground-level analytics plaza traces and restrained orange hard-socket emphasis.
- Roof/ridge ribbing that reinforces the cathedral reading in dark-first mode.

## Material Assignment

| Surface | Slot | Notes |
|---------|------|-------|
| Cathedral walls, side aisles, plaza slabs | base | Dark structural mass, inactive-readable |
| Muted teal trim and panel accents | accent | District color only in restrained details |
| Dark display backing panels | glass | Dark translucent data-screen surfaces |
| Buttresses, ribs, frames, collars, rails | detail | Structural dark metal |
| Teal charts, streams, beacon, waterfall | emissive | District teal, restrained until active |
| SIA hard-pipeline receiver | energy | Orange `#FF5E00`, receiver only |
| Pointed data-window panels | holo | Translucent teal holographic cathedral glass |

## Workflow

1. Load `analytics-s41-major-forms.blend`.
2. Normalize the seven material slots and retune Analytics material darkness.
3. Add facade panel depth and living-wall data detail.
4. Add arch frame reinforcement and buttress hardware.
5. Add crown, entrance, plaza, and roof polish.
6. Verify total tris land inside 12K-18K before export.
7. Save `analytics-s42-detail-export.blend`.
8. Render final front, three-quarter, distance, and dark-first screenshots.
9. Export packed Draco GLB to drafts, copy to approved only after validation passes.
10. Re-import the GLB and verify materials, transforms, file size, and no lights/cameras.
11. Render an all-built-structures cohesion screenshot with SIA plus modules 01-10.
12. Write `session42-metrics.json` and `session42-qa-import.json`.

## QA Gates

Gate 3 - Material Compliance:

- Only `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, and `holo` are present.
- No default gray or unnamed materials remain.
- Analytics keeps SPEC-authorized `holo` for data windows and `energy` for the hard receiver.

Gate 4 - Dark-First Test:

- With emission strength set to zero, the cathedral must still read from massing,
  buttress arcs, arch windows, roofline, and spire.
- Teal should not carry the whole design.

Gate 5 - Technical Budget:

- Final exterior tris must be between 12K and 18K.
- GLB must fit the 100-350 KB exterior file budget.
- Export must have bottom-centered origin, applied transforms, and no cameras/lights.

Gate 6 - Cohesion Check:

- Place Analytics with all approved structures through Recovery.
- Verify consistent dark material tone, skyline scale, and detail density.
- SIA remains the tallest landmark.

## What Not To Do

- Do not build the Data Sanctum interior.
- Do not model the Phase 5 SIA-to-Analytics pipeline.
- Do not start Nutrition.
- Do not alter approved neighboring modules.

## End Criteria

- Detail `.blend`, draft GLB, approved GLB, metrics JSON, and QA import JSON are saved.
- Four Analytics screenshots plus one all-built-structures cohesion screenshot exist.
- REVIEW records Session 42 actions, metrics, screenshots, gate results, and verdict.
- PROGRESS advances to Session 43 / AI Analytics interior only after approval.
