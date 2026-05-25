# Session 31: Career -- Interior

## Session Scope

- **Module**: #08 Career
- **Position**: Phase 3, Module 4 of 4
- **District Color**: Electric Blue `#3B82F6`
- **Focus**: Single interior room -- focal element, props, empties, export
- **Budget**: 5K-10K tris, 60-200 KB GLB
- **Energy slots**: energy=true, holo=false

## Quick Context

- Balencia City v3 is an interactive cinematic 3D city, not a website or dashboard.
- Aesthetic: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz.
- Avoid toy proportions, neon overload, photorealism, daytime, and suburban scale.
- Sky/background: ink-blue `#0A0A0F`; surfaces: dark premium `#1E1E28`.
- Materials use the 7-slot runtime override system.
- Slot names must be exact: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Career uses `energy` and does not use `holo`.
- Export GLB as Draco level 6, Y-up, no cameras/lights, bottom-centered origin.
- Run the shared lighting rig and material library before modeling.

## Relevant Material Rules

| Slot | Purpose |
|------|---------|
| `base` | Walls, floor, ceiling, broad structural surfaces |
| `accent` | Electric-blue trims and inactive district highlights |
| `glass` | Display surfaces, projection panels, skybridge glass |
| `detail` | Furniture, booth shells, rails, tree trunks, prop hardware |
| `emissive` | Blue LEDs, growth chart lines, task board strips |
| `energy` | Orange milestone markers, SIA power touchpoints |
| `holo` | Not used for Career |

## Interior Requirements

- Fresh scene only. Do not model inside the exterior file.
- One complete room shell: floor, back wall, two side walls, ceiling, one open/windowed front wall.
- One dominant focal object.
- Four to eight supporting prop categories.
- Three light empties named exactly `light_0`, `light_1`, `light_2`.
- One camera target empty named exactly `camera_target`.
- Props should frame the focal point and keep the room readable at low poly count.
- The room should remain readable when all emissions are set to zero.

## Room Description

The main tower ground floor operates as an executive command hub where professional
growth is visualized in every surface. AI career advisor workstations line the
perimeter with standing-desk forms and glass projection surfaces showing career
trajectory data. Growth charts dominate the walls as ascending blue lines with
orange milestone markers.

Deep-focus productivity zones occupy side alcoves with floating task boards. A
business strategy room sits at the rear with a 3D interactive map table projecting
market opportunities. Networking skybridge interiors are visible at the upper
level, where business card exchanges read as light-pulse transfers. Skill growth
trees branch upward from floor-mounted bases.

## Focal Element

Build the growth chart wall first. It is a wide display surface on the rear wall
with multiple ascending blue career trajectory lines and orange milestone markers.
It should be the visual anchor of the room and the point that `camera_target`
faces.

The focal element should consume roughly 25-30% of the interior triangle budget.
It must remain recognizable as a career progression chart from the entry camera
and in the dark-first screenshot.

## Supporting Props

- AI career advisor workstations: 4-6 standing desks with projection panels above.
- Growth chart wall: large curved or segmented display with ascending line graphics.
- Deep-focus productivity booths: 3 enclosed alcoves with floating task boards.
- 3D strategy table: large rear table with holographic terrain/map geometry.
- Skill growth trees: 2-3 vertical branching structures with glowing mastery nodes.
- Skybridge interior visible overhead: glass walkway with exchange pulse strips.
- Floor-embedded directional lighting: blue-lit path strips guiding circulation.

## Required Empties

- `light_0`: Center of command hub at ceiling, cool blue key light.
- `light_1`: Behind growth chart wall, intense blue backlight.
- `light_2`: At strategy table, warm focused spot for map projection.
- `camera_target`: Center of the command hub at standing eye height, facing the growth chart wall.

## Build Sequence

1. Clear the Blender scene completely.
2. Run `shared/lighting-rig.py`.
3. Run `shared/material-library.py` with `#3B82F6`, include_energy=true, include_holo=false.
4. Run the interior lighting rig for preview only.
5. Build the room shell:
   - Floor slab.
   - Back wall with display surface.
   - Two side walls.
   - Ceiling slab with open front.
   - Use `base` for primary enclosure.
6. Build the growth chart wall:
   - Wide glass display panel.
   - Multiple ascending blue line paths.
   - Orange milestone markers.
   - Vertical axis ticks and executive target marker.
7. Take a checkpoint screenshot mentally or with a render. The growth chart must read before props are added.
8. Build AI advisor workstations around the perimeter.
9. Build three productivity booths with task boards.
10. Build the strategy table and low-poly market terrain projection.
11. Build three skill growth trees with branching cylinders and mastery nodes.
12. Build the upper glass skybridge and exchange pulse strips.
13. Build floor-embedded directional paths.
14. Add `light_0`, `light_1`, `light_2`, and `camera_target` empties.
15. Audit material names and object names.
16. Dark-first test by setting all emission strengths to zero.
17. Export draft GLB with Draco compression.
18. Re-import and verify:
    - 5K-10K triangles.
    - 60-200 KB file size.
    - no cameras/lights.
    - required empties present.
    - mesh transforms identity.
    - bottom of bbox at z=0.

## What Not To Do

- Do not change the approved Career exterior.
- Do not add Phase 5 pipeline geometry.
- Do not use `holo` material for Career.
- Do not model multiple rooms.
- Do not add high-poly decorative surface detail.

## End Criteria

- Room shell complete.
- Growth chart wall is clearly dominant.
- All seven supporting prop categories are represented.
- Required runtime empties are exported.
- Materials are valid and Career-specific.
- Dark-first screenshot passes visually.
- Draft GLB passes import QA.
- Approved GLB is promoted to `interior/approved/career-int.glb`.
- `REVIEW.md` and `PROGRESS.md` are updated only after QA passes.
