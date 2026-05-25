# Session 32: Career - Integration Test

## Quick Context

- Project: Balencia City v3 - interactive cinematic 3D city, not a website.
- Aesthetic: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz.
- Sky: Ink-blue `#0A0A0F`; surfaces near `#1E1E28`; warm amber fog.
- Brand balance: 60% burnt orange `#FF5E00`, 30% forest green `#34A853`, 10% royal purple `#7F24FF`.
- SIA Tower remains the absolute center and tallest structure.
- Materials use the 7-slot runtime system: base, accent, glass, detail, emissive, energy, holo.
- Export convention: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center.

## Session Scope

- Module: #08 Career - Professional Tower Cluster
- Phase position: Phase 3, Step 3.4
- Current phase: integration
- Current session: 32
- Focus: Verify Career exterior and interior alignment, Scene 11 camera readability, and cohesion with SIA, Fitness, Yoga, Finance, Knowledgebase, Chat, and Leaderboard.
- This is a verification session. Do not create new module geometry.

## Approved Assets To Load

This module:

- Exterior: `modules/08-career/exterior/approved/career-ext.glb`
- Interior: `modules/08-career/interior/approved/career-int.glb`

Previously approved modules:

- SIA exterior: `modules/00-sia-tower/exterior/approved/sia-tower-ext.glb`
- SIA interior: `modules/00-sia-tower/interior/approved/sia-tower-int.glb`
- Fitness exterior: `modules/01-fitness/exterior/approved/fitness-ext.glb`
- Fitness interior: `modules/01-fitness/interior/approved/fitness-int.glb`
- Yoga exterior: `modules/02-yoga-wellbeing/exterior/approved/yoga-ext.glb`
- Yoga interior: `modules/02-yoga-wellbeing/interior/approved/yoga-int.glb`
- Finance exterior: `modules/03-finance/exterior/approved/finance-ext.glb`
- Finance interior: `modules/03-finance/interior/approved/finance-int-approved-s15.glb`
- Knowledgebase exterior: `modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb`
- Knowledgebase interior: `modules/04-knowledgebase/interior/approved/knowledgebase-int.glb`
- Chat exterior: `modules/05-chat-communication/exterior/approved/chat-ext.glb`
- Chat interior: `modules/05-chat-communication/interior/approved/chat-int.glb`
- Leaderboard exterior: `modules/06-leaderboard-competition/exterior/approved/leaderboard-ext.glb`
- Leaderboard interior: `modules/06-leaderboard-competition/interior/approved/leaderboard-int.glb`

## Approximate Orbital Placement

- SIA Tower: `(0, 0, 0)`
- Fitness: `(25, 25, 0)`
- Yoga & Wellbeing: `(35, 10, 0)`
- Finance: `(35, -5, 0)`
- Knowledgebase: `(30, -20, 0)`
- Chat & Communication: `(18, -34, 0)`
- Leaderboard & Competition: `(-8, -44, 0)`
- Career: `(-28, -34, 0)`

The exact city layout is finalized in Phase 6. For this integration pass, preserve the Session 30 Career cohesion position: a southwest tower district with clear separation from Leaderboard and a visible hard-pipeline corridor from SIA to the Career crown hardpoint.

## Alignment Checks

Verify the Career exterior and interior together:

- Interior fits within the exterior tower-cluster/plaza envelope without obvious wall clipping.
- Exterior and interior origins align on the same bottom-center plane.
- Interior scale matches exterior scale without rescaling.
- The open/windowed wall of the command hub faces the outer-ring Scene 11 approach.
- `light_0`, `light_1`, and `light_2` are inside the interior volume.
- `camera_target` is inside the room and points to the growth chart focal wall.
- Mesh rotations and scales are clean after import; transforms do not create unexpected shifts.

## Scene 11 Camera Checks

Scene 11: Career District.

- Scroll: approximately 69%.
- Camera: ascending elevator view, then push into command hub.
- Visible: tower cluster pointing upward, career advisors, growth charts, strategy rooms, and sky-bridges.
- Text context: "Your career doesn't exist in isolation. I see how your sleep, stress, relationships power your performance."
- Pipeline context: future hard pipeline from SIA to Career crown hardpoint.

Capture:

- Ascending elevator shot: tower hierarchy, floor bands, exterior elevator tubes, skybridges, and observation deck readable.
- Command hub push shot: open-front view toward the growth chart wall, advisor workstations, strategy table, skill trees, and upper skybridge.
- SIA-to-Career pipeline route shot: clear future hard-pipeline arc corridor.
- Career three-quarter shot: close verification of tower cluster, bridges, elevator tubes, and crown.
- Wide skyline shot: all eight approved structures visible for Gate 6.

## Gate 6 Cohesion Criteria

- Material darkness is consistent across modules.
- Detail density is comparable and appropriate to each architectural language.
- Scale relationships are correct; SIA dominates and Career is tallest district.
- Architectural variety remains clear: spire, gym megastructure, sanctuary, crystalline tower, library cathedral, communication hub, arena colosseum, professional tower cluster.
- All structures feel like the same dark premium city.

## Deliverables

- Run `shared/lighting-rig.py` before screenshots.
- Save integration blend: `modules/08-career/integration-session-32.blend`.
- Save metrics JSON: `modules/08-career/integration-session-32-report.json`.
- Save screenshots in `modules/08-career/screenshots/`.
- Update `modules/08-career/REVIEW.md` with Session 32 results and QA verdict.
- Update `PROGRESS.md` only after the integration check passes.
