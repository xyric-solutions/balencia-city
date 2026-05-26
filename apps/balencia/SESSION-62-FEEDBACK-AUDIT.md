# Phase 7 Session 62 Feedback Audit

Date: 2026-05-25  
Scope: Documentation and backlog reset based on user feedback, actual app code, and browser DOM QA.

## Verdict

Phase 7.3 remains active and not approved. The current app is stronger than the older docs imply, but it still needs a focused immersive polish sequence before final Phase 7 approval.

## What Is Actually Built

- Urban Atlas ground layer: irregular city island, SIA civic plaza, ring roads, radial boulevards, district pads, canals, edge context, street lamps, low-rise infill, and ground cross-district lanes.
- Label layer: full-name labels, curated desktop overview label positions for Scenes 1/15/17, focused labels for Scenes 4/6/11, and mobile overview dock.
- World activity layer: people, AI orbs, drones, flying vehicles, animated ambient particles, window glow overlays, entrance signs, and building beacons.
- Runtime energy layer: approved energy assets load, active energy IDs switch by scene, energy material intensity changes by active state, and AI pulse animation actions play.

## Audit Evidence

- Code inspection covered `src/components/scenes/CityContext.tsx`, `src/components/scenes/StructurePresence.tsx`, `src/components/scenes/ModelAsset.tsx`, `src/components/scenes/CameraTimeline.tsx`, and `src/components/ui/SceneOverlay.tsx`.
- Desktop browser DOM QA at 1280 x 720 passed for Scenes 1, 4, 6, 11, 15, and 17:
  - 0 label-to-label overlaps.
  - 0 label-to-overlay collisions.
  - 0 offscreen labels.
- Mobile browser DOM QA at 390 x 844 passed for Scenes 1, 15, and 17:
  - 0 label-to-label overlaps.
  - 0 label-to-overlay collisions.
  - 0 offscreen labels.
- Browser console warnings/errors were empty during the audited scene navigation.

## Known Verification Limitation

Screenshot capture still times out in the current browser/runtime path, matching the Session 61 limitation. This audit should not be treated as screenshot-based visual QA. A later Integration QA pass should retry screenshots and, if capture still fails, record the timeout explicitly.

## Feedback Mapped To Backlog

| Feedback | Current State | Backlog Decision |
|----------|---------------|------------------|
| Add walls for immersion and structure | Some perimeter edge blocks and district pads exist, but walls/retaining edges are not strong enough | Session 63 P0 |
| Labels feel detached | Labels are readable and collision-safe, but mostly screen-space or simple leader-line labels | Session 64 P0 |
| Add camera parallax | Scroll camera smoothing exists, but no idle/parallax life layer | Session 65 P1 |
| Improve depth separation | Fog and activity exist, but dark palette still needs stronger depth/rim/zoning | Session 63 P0 and Session 67 P1 |
| Animated data-flow lines | Energy assets exist, but no custom flowing shader/data-line layer | Session 65 P1 |
| Glow intensity based on activity/status | Active material intensity exists by scene, but no district status model | Session 65 P1 |
| Ambient particles/fog/scans | Ambient particles and fog exist; scans and layered atmospheric depth are missing | Session 65/67 P1 |
| SIA should feel dominant | Asset remains central, but app-level hierarchy needs stronger glow/framing/depth | Session 63 P0 |
| Reduce label overlap on smaller screens | Mobile dock currently passes DOM geometry checks, but must be preserved through redesign | Session 64 and Session 68 |
| Add interaction states | No building hover/focus/pulse/preview system exists | Session 66 P1 |
| District zoning colors | Motif colors exist, but zoning is not yet systematic enough for fast recognition | Session 63 P0 |
| Dynamic bottom-left panel | Overlay stays scene-driven and isolated from hover/focus context | Session 66 P1 |

## Next Recommended Session

Session 63: immersive city structure/depth. Keep approved GLBs unchanged and work in the app/context layer first.
