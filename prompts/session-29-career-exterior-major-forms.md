# Session 29: Career - Professional Tower Cluster - Exterior Major Forms

## Quick Context

- Project: Balencia City v3 - interactive cinematic 3D city.
- Aesthetic: dark, premium, night, warm cinematic atmosphere.
- Avoid: toy proportions, neon overload, daytime, suburban scale.
- Sky: Ink-blue `#0A0A0F`; surfaces: `#1E1E28`.
- SIA Tower: 100+ floors, about 40u tall, absolute center.
- District buildings: 20-40 floors and always shorter than SIA.
- Materials: 7-slot system: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Export discipline later: GLB, Draco level 6, Y-up, no cameras/lights, origin bottom-center.
- Scripts: run `shared/lighting-rig.py`, then `shared/material-library.py` with district color.

## Master Context Slice

Career row:

| # | Name | Color | Hex | Floors | GLB Filename |
|---|------|-------|-----|--------|--------------|
| 08 | Career | Electric Blue | `#3B82F6` | 40 | `career-towers.glb` |

Career identity:

- Career is a twin/corporate tower cluster and the tallest district structure.
- It should read as a professional ascent metaphor: vertical thrust, bridges, elevator tubes, and upward crowns.
- It must not resemble Chat and Communication. Chat is signal-tower/pod language; Career is clean corporate tower cluster language.

Material slot definitions:

| Slot | Purpose |
|------|---------|
| `base` | Dark structural tower facades, plaza, main bodies |
| `accent` | Electric-blue architectural edges, trims, upward fins |
| `glass` | Bridge enclosures, elevator tubes, observation deck, lobby facade |
| `detail` | Structural rails, supports, thin metal elements |
| `emissive` | Blue LED floor-joint bands and readable light strips |
| `energy` | Orange SIA conduit hardpoint only in this exterior pass |
| `holo` | Not used for Career |

Slot usage:

- Uses `energy`: Yes
- Uses `holo`: No

Technical constraints:

- District exterior budget: 15K-20K tris.
- Major-forms target: under 60% of max budget, so stay below 12K tris.
- Save `.blend` to `modules/08-career/exterior/drafts/`.
- No GLB export in this session.
- No interior modeling.
- No final SIA pipeline geometry.

## Session Scope

- Module: #08 Career - Professional Tower Cluster.
- Position: Phase 3, Step 3.4.
- District Color: Electric Blue `#3B82F6`.
- Floors: 20-40, with main tower 40 and secondary towers 25-35.
- Focus: primary silhouette geometry and major architectural forms only.
- This session: major forms.
- Next session: exterior detail, polish, decimation, dark-first proof, cohesion check, and GLB export.

## Architectural Identity

The Career district is a cluster of sleek interconnected towers where everything points upward.
The main tower reaches 40 floors and is flanked by secondary towers at 25-35 floors.
Every architectural line should direct the eye upward through tapered forms, vertical strips, and elevated bridges.

Enclosed sky-bridges connect the towers at multiple heights, creating visible links between career stages.
Transparent elevator tubes sit on the exterior so upward motion is legible from the outside.
Electric blue LED floor-joint lighting traces tower floors and reinforces scale.
The main crown carries an executive observation deck and an orange SIA energy hardpoint.
A ground networking plaza connects all tower bases.

Silhouette signature:

- Tallest district cluster.
- Main tower dominant at about 16u, still far below SIA Tower at about 40u.
- Three secondary towers at visibly different heights.
- Multiple enclosed bridges at different elevations.
- Visible exterior elevator tubes.
- Cantilevered glass observation deck at the main crown.
- Upward-pointing crown fins and vertical ascent lines.

## What To Build

Build only major form elements:

- Main tower: 40 floors, tallest, sleek tapered form, crown observation deck.
- Secondary towers: 2-3 at 25-35 floors, same design language but shorter.
- Enclosed sky-bridges between towers: 2-3 at different heights, glass-enclosed.
- Transparent elevator tubes on exterior: vertical glass cylinders on main plus one secondary tower.
- Blue LED floor-joint lighting: horizontal bands on all towers.
- Executive observation deck: cantilevered glass platform on main tower crown.
- Ground-level networking plaza: open flat area connecting all tower bases.
- Upward-pointing architectural elements: tapered edges and angled roof fins.
- Pipeline hardpoint on main tower crown for SIA energy conduit.
- Entry lobby visible at ground level: double-height glass facade on main tower.

## Proportion Guidance

- Use SIA Tower as the scale anchor: about 40u for 100+ floors.
- Main Career tower should be about 16u tall for 40 floors.
- Secondary towers should range from about 10.8u to 13.6u.
- The overall footprint should read as a cluster, not a single slab.
- Keep bridges high and clean so the cluster reads aspirational rather than industrial.
- Keep antennas out of the design; those belong to Communication.
- Keep the observation deck as the crown signature; do not use arena or cathedral forms.

## Build Workflow

1. Clear the Blender scene completely.
2. Run `shared/lighting-rig.py`.
3. Run `shared/material-library.py` with `#3B82F6`, `include_energy=True`, `include_holo=False`.
4. Verify lighting, materials, and world background.
5. Build the networking plaza and tower footprints.
6. Build the main tapered tower body.
7. Build three secondary tapered tower bodies.
8. Add readable floor-joint bands to every tower.
9. Add vertical edge strips and upward crown fins.
10. Add glass-enclosed sky-bridges at multiple heights.
11. Add the exterior glass elevator tubes.
12. Add the observation deck and entry lobby glass.
13. Add the orange crown energy hardpoint, but not the full SIA pipeline.
14. Save the draft `.blend`.
15. Capture front, three-quarter, and distance screenshots.
16. Write metrics to `session29-metrics.json`.

## QA Gates For This Session

Gate 1 - Silhouette Clarity:

- Career must be identifiable at thumbnail scale as a corporate tower cluster.
- It must be visually distinct from Communication, which has pod/signal/antenna language.
- SIA Tower must remain unmistakably taller.
- Crown and observation deck must be clear.

Gate 2 - Architectural Scale:

- Reads as a 20-40 floor megastructure, not a short office block.
- Floor indicators are visible.
- At least three sub-elements are visible: plaza/base, tower bodies, bridges, crown/deck/elevator tubes.
- Multi-part primary volumes are articulated before detail approval.

## What Not To Do

- Do not build interior workspace props.
- Do not export GLB.
- Do not create the final SIA pipeline.
- Do not add small decorative signage, furniture, or final facade ornament.
- Do not use `holo`.
- Do not download or import reference models.

## End Criteria

- Three screenshots exist:
  - `s29_front_elevation.png`
  - `s29_three_quarter.png`
  - `s29_distance_view.png`
- The structure is saved as `career-s29-major-forms.blend`.
- Total triangles are below 12K.
- All mesh materials use the 7-slot names.
- REVIEW.md records build metrics, screenshots, and Gate 1-2 QA.
- PROGRESS.md advances to session 30 exterior detail only after QA approval.
