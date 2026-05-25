# Session 43: AI Analytics - Interior

## Session Scope

- **Module**: #10 AI Analytics
- **Position**: Phase 4, step 4.3 interior after approved Analytics exterior
- **District Color**: Teal `#14B8A6`
- **Focus**: Single interior room - Data Sanctum
- **Budget**: Interior 5K-10K tris, 60-200 KB GLB
- **Energy slots**: energy=true, holo=true per module SPEC data visualization language

## Quick Context

- Balencia City v3 is a cinematic interactive 3D city, dark and premium.
- The app overrides material properties by exact slot names: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Start from a fresh Blender scene. Do not modify the approved Analytics exterior.
- Interior exports are separate GLBs loaded on demand.
- Required runtime nodes: `light_0`, `light_1`, `light_2`, and `camera_target`.

## Room Description

The Data Sanctum is a cathedral nave reinterpreted as a data visualization temple.
Massive 3D charts float through a tall vertical room. The hero object is a
life-analytics timeline running the full length of the nave: a topographic data
terrain using orange for effort, green for achievement, and purple for AI assistance.

The space must also include a neural network graph wall, 365-day habit heatmaps,
emotional wave patterns, prediction model trees, a ceiling city system map, and
query pedestals.

## Focal Element

Build the life-analytics timeline first. It should be the visual center of the
room, roughly 15m long by 3m wide by 2m tall in scene scale. The viewer should
understand that the room is an analytics cathedral even without labels.

## Supporting Props

- Floating 3D charts: bar charts, scatter plots, or line charts at varying heights.
- Neural network graph wall: large wall panel with teal nodes and firing links.
- 365-day habit heatmaps: two gridded wall panels with varying intensity cells.
- Emotional wave wall: continuous sine-wave geometry on a side wall.
- Prediction model trees: two branching upward structures showing future paths.
- Ceiling city system map: overhead panel showing the Balencia district network.
- Data interaction pedestals: three standing query stations.

## Required Empties

- `light_0`: above the timeline center, teal key source for the terrain.
- `light_1`: near the neural graph wall, intense teal backlight source.
- `light_2`: at ceiling map level, ambient down-light source.
- `camera_target`: at the life-analytics timeline focal point.

## Material Notes

- `base`: room shell, floor, walls, ceiling.
- `detail`: ribs, rails, pedestals, inactive graph lines.
- `glass`: translucent room panels and data backplates.
- `emissive`: teal active data surfaces and neural nodes.
- `energy`: orange effort metrics and SIA-energy compatible markers.
- `accent`: green achievement metrics.
- `holo`: purple AI-assistance metrics and holographic map elements.

## Workflow

1. Clear scene and set up Balencia lighting/materials.
2. Build room shell with floor, side walls, back wall, ceiling, and open entrance wall.
3. Build the life-analytics topographic terrain and metric streams.
4. Add floating charts, neural graph wall, heatmaps, emotional waves, prediction trees, ceiling map, and pedestals.
5. Place exact runtime empties.
6. Capture overview, entry, focal, topdown, and dark-first screenshots.
7. Consolidate meshes by group/material for compact GLB export.
8. Export Draco GLB and validate import hygiene.
9. Promote to approved only if Gates 3, 4, 5, and 7 pass.

## End Criteria

- Room shell complete with one open wall.
- Focal timeline clearly dominates the scene.
- Seven supporting prop families present and identifiable.
- Required empties present with exact names.
- All mesh materials use only the 7-slot system.
- Dark-first screenshot remains legible.
- Imported GLB has no cameras/lights, no rogue materials, identity mesh transforms, and budget-compliant tris/file size.
