# Session 69 Report: City Layout v2 Spread Prototype

Date: 2026-05-26
Status: Done

## Summary

Session 69 implemented the Phase 8 app-side spread prototype. The city now uses `shared/city-layout-v2.json` as the layout source, with district centers spread around the full circular island and a verified minimum spacing of 36.4u.

## Changes

- Added `shared/city-layout-v2.json` and `src/lib/city-layout-v2.ts`.
- Retargeted approved structure runtime positions through the shared layout while preserving original GLB source assets.
- Updated the app asset manifest to reference the new layout source and v2 positions.
- Retargeted overview/focused cameras for Scenes 1, 4-17 to the wider city.
- Expanded island, road rings, canals, perimeter walls, atmosphere depth, vehicle/drone paths, and app-layer pulse/fog radii.
- Updated desktop overview labels for Scenes 1, 15, and 17, with no label/overlay collisions in final QA.
- Hid old baked endpoint energy GLBs in the app until Session 70 rebakes energy routes from the new layout.

## QA

| Check | Result |
|-------|--------|
| Minimum district spacing | PASS - 36.4u, Fitness/Yoga |
| `./node_modules/.bin/tsc --noEmit` | PASS |
| `npm run build` | PASS |
| Desktop screenshots | PASS - Scenes 1, 15, 17 captured under `output/playwright/` |
| Mobile screenshots | PASS - Scenes 1, 15, 17 captured under `output/playwright/` |
| Desktop labels | PASS - 12 labels, no label overlaps, no overlay collisions, no offscreen labels |
| Mobile labels | PASS - 12 labels, no label overlaps, no overlay collisions, no offscreen labels |
| Console | PASS - no warning/error messages during checked scenes |

Existing build notes: Vite still reports the known large client chunk warning, and Node still emits the existing `module.register()` deprecation warning.

## Next

Session 70 should update the Blender assembly and Phase 5 energy scripts to read `shared/city-layout-v2.json`, rebuild all baked endpoint energy assets, rerun 17-scene verification, and only then restore baked energy GLBs in the app.

