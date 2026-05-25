# Session 47: Nutrition - Interior

## Session Scope

- Module: #11 Nutrition
- Position: Phase 4.4, final district interior before Nutrition integration
- District Color: Warm Amber `#D97706`
- Focus: Nourishment Hall interior - living market focal element, communal dining, nutrition data props, runtime empties, screenshots, GLB export, and QA
- Budget: Interior 5K-10K tris, 60-200 KB GLB
- Energy slots: energy=false for the interior; holo=true for nutrition breakdowns, tags, recipe guides, and water intake rings

## Room Description

The Nourishment Hall is a warm, inviting communal space centered around shared dining. Long communal tables run down the center of the room, wrapped in amber lighting and small holographic nutrition displays. The palette should feel warmer and more organic than the cooler Balencia interiors while staying dark, premium, and night-first.

At one end, an AI nutrition station scans meals and shows cross-day nutritional connections. The opposite end holds the living market: a multi-level floating shelf produce display with warm spotlights and holographic nutrition tags beside each item. One side wall carries an adaptive calorie display, and the back/side zones include chef prep stations with floating recipe panels. Hydration stations with carafe silhouettes and water-intake rings sit in the corners.

The interior is loaded on demand when the user scrolls into the Nutrition scene. It should feel like a curated peek inside the vertical farm: intimate, warm, and connected to the city night through one open wall.

## Focal Element

The living market is the hero object:

- Multi-level floating shelf produce display, about 6m wide and 3m deep
- Warm amber spotlights on every shelf
- Produce forms with readable silhouettes: rounded fruit, leafy bundles, crate clusters, and small greenhouse trays
- Holographic nutritional tag rectangles beside market items
- Positioned at the far end of the room, where `camera_target` points
- Highest-detail element in the interior

Build the living market first and keep the central table axis leading directly toward it.

## Props List

1. Communal dining tables: 2-3 long low table surfaces with bench seating on both sides
2. Holographic nutrition breakdowns: macro rings and micro bars beside table positions
3. AI nutrition scanning station: standing counter with overhead scan display
4. Living market floating shelves: multi-level produce display
5. Holographic nutritional tags on market items: tiny floating label panels
6. Adaptive calorie wall: large side-wall data display
7. Chef prep zones: 2 kitchen workstations with floating recipe guides
8. Hydration stations: 2 corner units with carafe forms and water intake rings

Props should frame the living market, not compete with it. Keep the center aisle readable from the entry camera.

## Required Empties

Create exact runtime empties:

- `light_0`: above communal tables, warm amber key light position
- `light_1`: above living market, focused shelf spotlight position
- `light_2`: behind adaptive calorie wall, amber backlight position
- `camera_target`: centered at seated dining height, looking down the table axis toward the living market

## Material Assignment

Use runtime material slot names exactly:

| Surface | Slot | Notes |
|---------|------|-------|
| Floor, walls, ceiling, table slabs | base | Dark warm foundation, no bright district color |
| Produce, plant accents, selected data-success marks | accent | Green organic identity and food silhouettes |
| Market shelf glass, scan panels, carafes | glass | Transparent warm-tinted surfaces |
| Benches, counters, shelf frames, kitchen hardware | detail | Dark furniture and structural detail |
| Amber grow lights, spotlights, table edge glows | emissive | Warm amber `#D97706` glow |
| Nutrition overlays, macro rings, water rings, recipe guides | holo | Translucent nutrition data overlays |

Do not use the `energy` slot in this interior. Hard pipeline geometry comes later in Phase 5.

## Workflow

1. Start a fresh Blender scene.
2. Load the shared lighting and material library using district hex `#D97706`, include_energy=false, include_holo=true.
3. Build the room shell: floor, three walls, ceiling, open front wall/windowed entry.
4. Build the living market focal element.
5. Build communal tables and benches down the center.
6. Add holographic nutrition breakdowns at table positions.
7. Add AI nutrition scanning station.
8. Add adaptive calorie wall.
9. Add chef prep zones and hydration stations.
10. Place `light_0`, `light_1`, `light_2`, and `camera_target`.
11. Capture overview, entry, focal, topdown, and dark-first screenshots.
12. Consolidate by group/material, save blend, export Draco GLB, re-import, and validate gates.

## QA Targets

Gate 3: Materials use only valid slots; `holo` is present; `energy` is absent; no default or rogue materials.

Gate 4: With all emission strengths set to 0, the room still reads as a Nourishment Hall: shell, tables, living market, side wall, and prep/hydration stations remain recognizable.

Gate 5: GLB is 5K-10K tris and 60-200 KB, with no cameras/lights in export, required empties present, and all mesh transforms identity after import.

Gate 7: Clear living-market focal point, 3 logical light empties, `camera_target`, 8 identifiable props, complete room shell with one open wall, and same runtime material system.

## Output Paths

- Draft blend: `modules/11-nutrition/interior/drafts/nutrition-int-session47.blend`
- Draft GLB: `modules/11-nutrition/interior/drafts/nutrition-int-draft-s47.glb`
- Approved GLB after QA: `modules/11-nutrition/interior/approved/nutrition-int.glb`
- Metrics: `modules/11-nutrition/interior/drafts/session47-metrics.json`
- Import QA: `modules/11-nutrition/interior/drafts/session47-qa-import.json`

## Locked Scope

- Do not modify Nutrition exterior.
- Do not add SIA pipeline geometry.
- Do not create multiple rooms.
- Do not exceed the interior budget with photorealistic produce detail.
