# Session 30: Career - Professional Tower Cluster - Exterior Detail, Polish & Export

## Quick Context

- Project: Balencia City v3 - interactive cinematic 3D city.
- Aesthetic: dark, premium, night, warm cinematic atmosphere.
- Avoid: toy proportions, neon overload, daytime, suburban scale.
- Sky: Ink-blue `#0A0A0F`; surfaces: `#1E1E28`.
- SIA Tower: 100+ floors, about 40u tall, absolute center.
- District buildings: 20-40 floors and always shorter than SIA.
- Materials: 7-slot system: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Export: GLB, Draco level 6, Y-up, no cameras/lights, origin bottom-center.
- Scripts: run `shared/lighting-rig.py`, then `shared/material-library.py` with district color.

## Master Context Slice

Career row:

| # | Name | Color | Hex | Floors | GLB Filename |
|---|------|-------|-----|--------|--------------|
| 08 | Career | Electric Blue | `#3B82F6` | 40 | `career-towers.glb` |

Career identity:

- Career is a clean professional tower cluster and the tallest district structure.
- It must read as professional ascent: vertical thrust, bridges, elevator tubes, observation deck, and upward crowns.
- It must not resemble Chat and Communication. Chat uses signal pod and antenna language; Career uses corporate tower cluster language.

Material slot definitions:

| Slot | Purpose |
|------|---------|
| `base` | Dark structural tower facades, plaza, main bodies |
| `accent` | Electric-blue architectural trims, ascent fins, small district-color marks |
| `glass` | Bridge enclosures, elevator tubes, observation deck, lobby facade, window panels |
| `detail` | Structural rails, mullions, supports, brackets, metal elements |
| `emissive` | Blue LED floor-joint bands and readable light strips |
| `energy` | Orange SIA conduit hardpoint only in this exterior pass |
| `holo` | Not used for Career |

Slot usage:

- Uses `energy`: Yes
- Uses `holo`: No

Technical constraints:

- District exterior budget: 15K-20K tris.
- Previous session total: 4,940 tris.
- Remaining budget: 15,060 tris.
- Final export must stay under 20K tris and 400 KB.
- Save `.blend` to `modules/08-career/exterior/drafts/`.
- Export draft GLB to `modules/08-career/exterior/drafts/career-ext-draft-s30.glb`.
- Promote approved GLB to `modules/08-career/exterior/approved/career-ext.glb` only after gates pass.
- No interior modeling.
- No final SIA pipeline geometry.

## Previous Session State

Blend file: `modules/08-career/exterior/drafts/career-s29-major-forms.blend`

Session 29 built:

- A 40-floor main tapered tower with floor-joint bands and upward edge strips.
- Three secondary tapered towers at 34, 30, and 27 floors.
- Three enclosed skybridges at different heights.
- Exterior transparent elevator tubes on the main and west secondary towers.
- Double-height main lobby, networking plaza slab, blue circulation paths.
- Crown observation deck, roof fins, and orange SIA hardpoint marker.

Session 29 QA:

- Gate 1 passed: silhouette reads as a professional tower cluster.
- Gate 2 passed: scale reads as high-rise metropolitan architecture.
- No fixes are required before detail work.

## Session Scope

- Module: #08 Career - Professional Tower Cluster.
- Position: Phase 3, Step 3.4.
- District Color: Electric Blue `#3B82F6`.
- Focus: detail elements, polish, material compliance, dark-first proof, export, and cohesion check.
- Final budget: 15K-20K tris.
- Target final utilization: roughly 17K-19K tris with real architectural articulation.

## Detail Elements To Add

Add the detail that was intentionally deferred from Session 29:

- Dark floor-plate ledges behind the blue LED bands on every tower floor.
- Dark spandrel facade panels so the structure reads in dark-first mode.
- Window/glass panel rhythm on all tower faces.
- Metal mullions and vertical corporate facade rails.
- Skybridge ribs, enclosed frame hardware, and bridge underbraces.
- Elevator tube collars, brackets, service ladders, and cab details.
- Observation-deck rail posts, underside braces, and executive crown trim.
- Lobby glass framing and main entry header detail.
- Networking plaza tile grid, route strips, node pads, and base connectors.
- Crown hardpoint refinement: orange socket remains a hardpoint, not the final pipeline.

## Material Targets

- Keep `base` near 50-55% by adding structural ledges and dark facade panels.
- Keep `accent` near 10-15% through blue trim, ascent arrows, and edge hardware.
- Bring `glass` to 10-18% through window panes, skybridge panels, lobby glass, and elevator tubes.
- Bring `detail` to 12-18% through mullions, rails, collars, trusses, and brackets.
- Keep `emissive` to 3-8%; do not turn every surface into glow.
- Keep `energy` to 0-5%; only the SIA hardpoint should use it.
- Do not create `holo` material or holo geometry.

## Build Workflow

1. Load `career-s29-major-forms.blend`.
2. Re-run the shared viewport lighting rig.
3. Ensure material-library slots exist for `#3B82F6`, `include_energy=True`, `include_holo=False`.
4. Normalize all mesh material slots to the allowed six Career slots.
5. Add facade ledges, glass rhythm, panels, mullions, bridge hardware, elevator hardware, observation deck details, plaza detail, and hardpoint polish.
6. Save the detail `.blend`.
7. Render front, three-quarter, distance, and dark-first screenshots.
8. Apply world transforms, center the structure at bottom-origin, parent under `career-ext`.
9. Export Draco GLB to the draft path.
10. Copy the passing GLB to approved.
11. Import the approved GLB in a clean scene and write validation metrics.
12. Import all approved exteriors plus Career for the all-eight cohesion screenshot.
13. Write `session30-metrics.json` and `session30-qa-import.json`.

## Polish Checklist

- All mesh objects use allowed material slots only.
- No default gray or unnamed materials.
- No `holo` material.
- Proportions remain a professional tower cluster and not a signal/antenna district.
- SIA remains tallest in the cohesion screenshot.
- Bridge and elevator details are attached to existing major forms.
- Dark-first screenshot remains readable with emission set to zero.
- Total tris fall within the 15K-20K exterior budget.
- Exported GLB has no cameras or lights.
- Exported GLB opens through the Blender glTF importer.
- Root origin is bottom-center and mesh transforms are applied.

## QA Gates For This Session

Gate 1 - Silhouette Clarity:

- Career remains identifiable at thumbnail scale.
- The outline stays distinct from Communication, Leaderboard, Finance, and SIA.
- Crown observation deck, elevator tubes, bridges, and tower cluster remain legible.

Gate 2 - Architectural Scale:

- Reads as 20-40 floor high-rise architecture.
- Floor ledges and bands make the 40/34/30/27-floor scale readable.
- Major form articulation remains intact after detail.

Gate 3 - Material Compliance:

- Runtime slot names match the 7-slot convention.
- Career uses `energy` but not `holo`.
- Material distribution falls within acceptable ranges or is documented.

Gate 4 - Dark-First Test:

- With all emission strengths set to zero, the Career cluster still reads through dark geometry, glass, ledges, mullions, and massing.
- Blue is restricted to accent/emissive/energy-bearing slots.

Gate 5 - Technical Budget:

- Triangles within 15K-20K.
- GLB file size within 120-400 KB.
- No cameras or lights in export.
- Origin bottom-center; transforms applied.

Gate 6 - Cohesion Check:

- Import alongside approved structures 00-06.
- Career should read as the tallest district but clearly shorter than SIA.
- Detail density should sit between Chat's multi-part hub and Leaderboard's arena polish.
- Material darkness should match the approved city language.

## What Not To Do

- Do not build the interior command hub.
- Do not build the final SIA hard pipeline.
- Do not add antennas or signal dishes.
- Do not add arena, cathedral, crystal, garden, or cloud motifs.
- Do not download or import reference models.

## End Criteria

- `career-s30-detail-export.blend` exists.
- `career-ext-draft-s30.glb` exists.
- `career-ext.glb` is promoted to approved after QA.
- Four screenshots exist:
  - `s30_front_elevation.png`
  - `s30_three_quarter.png`
  - `s30_distance_view.png`
  - `s30_dark_first.png`
- Cohesion screenshot exists: `s30_cohesion_all8.png`.
- `session30-metrics.json` and `session30-qa-import.json` exist.
- REVIEW.md records the build and QA approval.
- PROGRESS.md advances to session 31 interior only after all gates pass.
