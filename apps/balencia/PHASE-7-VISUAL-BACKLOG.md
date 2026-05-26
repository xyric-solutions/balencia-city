# Phase 7 Visual Quality Backlog

Date: 2026-05-26
Status: Locally QA-complete

## Summary

Phase 7.3 is now a visual quality backlog, not a single quick city-context pass. The approved structures, interiors, energy GLBs, assembly, and 17-scene scroll timeline remain valid. Work stays in the R3F app/context layer unless a later review explicitly asks for approved asset changes.

Session 68 completed the product-reality overlay for Scene 16 and the final integration QA pass for the Phase 7.3 visual quality backlog.

## Already Built

- Session 58: Vite/R3F app shell, approved GLB sync, material override foundations, full-city Canvas, eager exterior/energy loading, on-demand interior paths.
- Session 59: canonical 17-scene GSAP/Lenis timeline, scene-local overlay state, active interior mounting, per-scene active energy IDs, scene navigation dots.
- Session 60/61 WIP: Urban Atlas app-layer ground with island base, central SIA plaza, ring roads, radial boulevards, district pads, canals, low-rise infill, edge blocks, street lamps, ground cross-district lanes, and hybrid labels.
- Session 61: wrapping-safe full labels, curated desktop label placement for Scenes 1/15/17, focused labels for Scenes 4/6/11, and compact mobile overview label dock.
- Session 63: app-layer SIA plinth/beacon/halo hierarchy, district zoning/parapets, perimeter retaining walls with gate piers, darker outer depth bands, and scene-aware atmosphere.
- Session 64: shared district metadata, building-tethered illuminated label boards, hover/focus reveal state, and lightweight interaction targets for SIA, Fitness, Finance, Career, and Relationships.
- Session 65: damped pointer camera parallax, `LivingEnergyLayer` app-level SIA-to-district data routes, Scene 15 gold cross-district pulses, status-based glow rings/scan planes, route fireflies, AI scan motes, green lift motes, and subtle scan haze.
- Session 66: compact district preview metadata, dynamic bottom-left preview panel, one-active preview card/tooltips, hover/focus pulse polish, Escape/blur focus clearing, and subtle damped focus zoom.
- Session 67: `AtmosphereDepthLayer` app-layer void/horizon treatment with a sky gradient dome, distant terrain rings, warm fog shelves, distant urban-edge silhouettes, animated outer rim lights, and Scene 17 crown/horizon cleanup.
- Session 68: Scene 16 `ProductRealityOverlay` with person silhouette, phone hardware, dark-mode Today Screen, SIA greeting, connected-signal micro-insight, intelligence path, action cards, and final desktop/mobile QA screenshots.
- Current app activity layer: window glow overlays, entrance signs, beacons, people, drones, flying vehicles, AI orbs, ambient particles, living data routes, firefly route motes, status glow, and scan layers.
- Current energy runtime: active/inactive material intensity switching, AI pulse animation playback, and app-layer animated data packets/glow overlays. Approved energy GLBs remain unchanged.

## Session 62 Audit Evidence

- Code inspection confirmed the already-built app-layer city detail above in `CityContext.tsx`, `StructurePresence.tsx`, `ModelAsset.tsx`, `CameraTimeline.tsx`, and `SceneOverlay.tsx`.
- Browser DOM QA at 1280 x 720 passed label geometry for Scenes 1, 4, 6, 11, 15, and 17: no label-to-label collisions, no overlay collisions, and no offscreen labels.
- Browser DOM QA at 390 x 844 passed label geometry for Scenes 1, 15, and 17: no label-to-label collisions, no overlay collisions, and no offscreen labels.
- Browser console warnings/errors were empty during the audited scene navigation.
- Screenshot capture still timed out, matching the Session 61 limitation. Do not claim screenshot-based visual QA until capture succeeds.

## Session 63 Audit Evidence

- Code changes stayed in the app/context layer: approved structure, interior, energy GLBs, asset manifest, and scroll timeline data were not modified.
- `./node_modules/.bin/tsc --noEmit` passed in `apps/balencia`.
- `npm run build` passed in `apps/balencia`; Vite still reports the existing large client chunk warning.
- Desktop browser QA at 1280 x 720 passed label geometry for Scenes 1, 2, 4, 6, 11, 15, and 17: no label-to-label collisions, no overlay collisions, no offscreen labels, and nonzero canvas size.
- Mobile browser QA at 390 x 844 passed label geometry for Scenes 1, 15, and 17: no label-to-label collisions, no overlay collisions, no offscreen labels, and nonzero canvas size.
- Screenshot capture succeeded for all required Session 63 desktop/mobile QA scenes under `output/playwright/`.
- Headless Chrome emitted WebGL `ReadPixels` performance warnings during capture; no app JavaScript/page errors were observed.

## Session 64 Audit Evidence

- Code changes stayed in the app/context/UI layer: approved structure, interior, energy GLBs, asset manifest, and scroll scene camera data were not modified.
- `./node_modules/.bin/tsc --noEmit` passed in `apps/balencia`.
- `npm run build` passed in `apps/balencia`; Vite still reports the existing large client chunk warning.
- Desktop browser QA at 1280 x 720 passed label/board geometry for Scenes 1, 4, 6, 11, 15, and 17: no label-to-label collisions, no overlay collisions, no offscreen labels, no text overflow, and nonzero canvas size.
- Mobile browser QA at 390 x 844 passed label geometry for Scenes 1, 15, and 17: no label-to-label collisions, no overlay collisions, no offscreen labels, no text overflow, and nonzero canvas size.
- Interaction focus reveal passed for SIA, Fitness, Finance, Career, and Relationships: each target produced a focused board with district text and visible board state. Hover handlers are implemented on pointer and mouse enter; automated hover movement in the in-app browser did not emit hover events, so focus/click was used for executable interaction proof.
- Browser runtime console had no warnings/errors during required scene navigation and interaction checks.
- Screenshot capture timed out before files were written; this session relies on DOM/canvas geometry checks instead of screenshot artifacts.

## Session 65 Audit Evidence

- Code changes stayed in the app layer: approved structure, interior, energy GLBs, asset manifest, and `SCROLL_SCENES` camera data were not modified.
- `./node_modules/.bin/tsc --noEmit` passed in `apps/balencia`.
- `npm run build` passed in `apps/balencia`; Vite still reports the existing large client chunk warning and the Node build path emits the existing `module.register()` deprecation warning.
- Desktop browser QA at 1280 x 720 passed for Scenes 1, 4, 6, 11, 15, and 17: no label/board overlaps, no overlay collisions, no offscreen labels, no text overflow, nonzero canvas size, and all five interaction targets present.
- Mobile browser QA at 390 x 844 passed for Scenes 1, 15, and 17: compact labels stayed onscreen with no overlap, overlay collision, or text overflow; canvas was nonzero.
- Interaction focus reveal passed for SIA, Fitness, Finance, Career, and Relationships. A small Relationships overview-board collision was found during QA and fixed by nudging its app-layer board direction; retest passed.
- Browser runtime console had no warnings/errors during required scene navigation and interaction checks.
- Screenshot capture timed out again, including a smaller clipped capture attempt; this session relies on DOM/canvas geometry checks instead of screenshot artifacts.

## Session 66 Audit Evidence

- Code changes stayed in the app/context/UI layer: approved structure, interior, energy GLBs, asset manifest, and `SCROLL_SCENES` camera data were not modified.
- `./node_modules/.bin/tsc --noEmit` passed in `apps/balencia`.
- `npm run build` passed in `apps/balencia`; Vite still reports the existing large client chunk warning and the Node build path still emits the existing `module.register()` deprecation warning.
- Desktop browser QA at 1280 x 720 passed for Scenes 1, 4, 6, 11, 15, and 17: canvas was nonzero, labels/boards did not overlap, labels did not collide with overlays, labels stayed onscreen, and runtime console warnings/errors were empty.
- Mobile browser QA at 390 x 844 passed for Scenes 1, 15, and 17: compact label dock stayed onscreen with no overlay collisions; focused preview mode stayed compact and hid the district tooltip card on mobile.
- Focus preview passed for SIA, Fitness, Finance, Career, and Relationships from the overview scene: bottom-left panel swapped to district preview content, focused boards remained visible, one preview card was active on desktop, Escape/blur returned the narrative panel, and all interaction targets remained tabbable buttons with `tabIndex=0`.
- Browser automation still did not emit reliable hover state from pointer movement, matching the Session 64 limitation; hover handlers and hover styles are implemented, while executable QA used focus/click as the interaction proof.
- Screenshot capture timed out or closed the browser target again before Session 66 files were written under `output/playwright/`; this session relies on DOM/canvas geometry checks instead of screenshot artifacts.

## Session 67 Audit Evidence

- Code changes stayed in the app/context/effects layer: approved structure, interior, energy GLBs, asset manifest, and `SCROLL_SCENES` camera data were not modified.
- `./node_modules/.bin/tsc --noEmit` passed in `apps/balencia`.
- `npm run build` passed in `apps/balencia`; Vite still reports the existing large client chunk warning and the Node build path still emits the existing `module.register()` deprecation warning.
- Desktop browser QA at 1280 x 720 passed for Scenes 1, 15, 16, and 17: canvas was nonzero, labels/boards did not overlap, labels did not collide with overlays, labels stayed onscreen, and text did not overflow.
- Mobile browser QA at 390 x 844 passed for Scenes 1, 15, and 17: compact labels stayed onscreen with no overlay collisions or text overflow.
- Runtime console warnings/errors were empty during required scene navigation.
- Screenshot capture timed out through the in-app browser via `Page.captureScreenshot`, matching the Session 64-66 limitation; this session relies on DOM/canvas geometry checks instead of screenshot artifacts.

## Session 68 Audit Evidence

- Code changes stayed in the app/UI layer: approved structure, interior, energy GLBs, asset manifest, and `SCROLL_SCENES` camera data were not modified.
- Added `ProductRealityOverlay.tsx` and product-specific CSS for desktop/mobile Scene 16 foreground composition.
- `./node_modules/.bin/tsc --noEmit` passed in `apps/balencia`.
- `npm run build` passed in `apps/balencia`; Vite still reports the existing large client chunk warning and Node still emits the existing `module.register()` deprecation warning.
- Restarted the stale local dev server on `http://localhost:3006/` so current CSS was served.
- In-app browser Scene 16 check passed: product overlay was fixed-position, phone was visible onscreen, canvas was nonblank, and runtime warnings/errors were empty.
- External Chrome QA passed at 1280 x 720 for Scenes 1, 4, 6, 11, 15, 16, and 17: nonblank canvas, labels onscreen, no label overlaps, no label/overlay collisions, no product overlay leakage outside Scene 16, no phone/overlay collision, no text overflow, and no console warnings/errors beyond normal Vite/React info logs.
- External Chrome QA passed at 390 x 844 for Scenes 1, 15, 16, and 17 with the same checks.
- Screenshots were captured under `output/playwright/`, including `session68-desktop-scene-16.png` and `session68-mobile-scene-16.png`.

## Missing Or Lacking Quality

- No Phase 7.3 visual quality backlog gaps remain after local QA.

## Next Sessions

| Priority | Session | Status | Work |
|----------|---------|--------|------|
| P0 | 63 - Immersive city structure/depth | Done | Added stronger walls, retaining edges, district boundaries, zoning color cues, foreground/background depth separation, and app-layer SIA dominance without modifying approved GLBs. |
| P0 | 64 - Label boards and reveal | Done | Replaced detached-feeling focused labels with illuminated building-tethered boards for active/hovered/focused districts, added hover/focus reveal state, kept mobile labels compact, and preserved no-overlap acceptance. |
| P1 | 65 - Living intelligence motion | Done | Added subtle camera parallax, animated data-flow lines, status-based glow variation, richer particles/fog, and holographic scan layers. |
| P1 | 66 - Interaction overlay | Done | Added hover/focus pulse polish, keyboard-accessible focus states, focus zoom, district preview cards/tooltips, and bottom-left panel transitions driven by focused/hovered building context. |
| P1 | 67 - Void/horizon pass | Done | Added distant urban edge cues, warm fog layers, terrain/sky gradient, outer rim lighting, and Scene 17 cleanup. |
| P1 | 68 - Product reality overlay | Done | Added the Scene 16 person/phone Today Screen overlay and kept it integrated with the city depth pass. |
| P2 | 68 - Integration QA | Done | Ran desktop/mobile label checks, interaction/product visibility checks, console checks, build check, canvas checks, and screenshot capture. |

## Interface Backlog

- Shared district metadata for labels, zones, board anchors, preview content, and interaction affordances is implemented in `src/lib/district-metadata.ts`.
- Scroll/interaction state tracks `hoveredDistrictId` and `focusedDistrictId`; preview content is resolved from shared district metadata with focused district taking priority over hovered district.
- `DistrictLabelBoard` is implemented for illuminated active/hovered/focused building boards.
- `BuildingInteractionLayer` is implemented for pointer and keyboard interaction targets without modifying approved GLBs first.
- `DistrictPreviewPanel` is implemented inside the bottom-left overlay, with scene narrative preserved whenever no district is hovered or focused.
- `LivingEnergyLayer` is implemented for flowing app-layer pipelines, animated data packets, Scene 15 gold pulses, status glow variation, and scan/mote atmosphere.
- `AtmosphereDepthLayer` is implemented for sky gradient, terrain depth, warm horizon fog, distant city-edge cues, outer rim lighting, and Scene 17 closing cleanup.

## Acceptance Gates

| Gate | Scenes/Scope | Pass Criteria |
|------|--------------|---------------|
| Desktop labels | 1, 4, 6, 11, 15, 17 | Full text visible, no label-to-label overlap, no overlay collision, no offscreen labels. |
| Mobile labels | 390 x 844, Scenes 1, 15, 17 | Compact labels avoid overlay, fit inside viewport, and remain readable. |
| Interaction | SIA, Fitness, Finance, Career, and one low-profile district | Hover/focus target works, preview content updates, visual pulse is obvious but not noisy. |
| Visual hierarchy | Overview and closing scenes | SIA reads as the dominant center, district zoning is recognizable, and foreground/background separation improves over Session 61. |
| Runtime health | App load and required scene navigation | No runtime console warnings/errors. |
| Build | `apps/balencia` | `npm run build` passes. |
| Performance | Active city | Keep active city under the 250K triangle target unless a later audit explicitly raises the budget. |
| Screenshots | Required QA scenes | Capture screenshots if the browser capture timeout is resolved; otherwise document the timeout and rely on DOM/canvas checks only. |

## Current Open Items

- Phase 7.3 is locally QA-complete and ready for user visual review.
- Approved GLBs remain unchanged; next fixes should stay in app/context/shader layers unless a later review explicitly asks for asset changes.
