# Session 28: Leaderboard & Competition - Integration Test

## Quick Context

- Project: Balencia City v3 - interactive cinematic 3D city, not a website.
- Aesthetic: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz.
- Sky: Ink-blue `#0A0A0F`; surfaces near `#1E1E28`; warm amber fog.
- Brand balance: 60% burnt orange `#FF5E00`, 30% forest green `#34A853`, 10% royal purple `#7F24FF`.
- SIA Tower remains the absolute center and tallest structure.
- Materials use the 7-slot runtime system: base, accent, glass, detail, emissive, energy, holo.
- Export convention: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center.

## Session Scope

- Module: #06 Leaderboard & Competition - Arena Colosseum
- Phase position: Phase 3, Step 3.3
- Current phase: integration
- Current session: 28
- Focus: Verify Leaderboard exterior and interior alignment, Scene 9 camera readability, and cohesion with SIA, Fitness, Yoga, Finance, Knowledgebase, and Chat.
- This is a verification session. Do not create new module geometry.

## Approved Assets To Load

This module:

- Exterior: `modules/06-leaderboard-competition/exterior/approved/leaderboard-ext.glb`
- Interior: `modules/06-leaderboard-competition/interior/approved/leaderboard-int.glb`

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

## Approximate Orbital Placement

- SIA Tower: `(0, 0, 0)`
- Fitness: `(25, 25, 0)`
- Yoga & Wellbeing: `(35, 10, 0)`
- Finance: `(35, -5, 0)`
- Knowledgebase: `(30, -20, 0)`
- Chat & Communication: `(18, -34, 0)`
- Leaderboard & Competition: `(-8, -44, 0)`

The exact city layout is finalized in Phase 6. For this integration pass, preserve the Session 26 Leaderboard cohesion position: a south/southwest arena district with clear spacing from Chat and a visible corridor from SIA to the arena apex.

## Alignment Checks

Verify the Leaderboard exterior and interior together:

- Interior fits within the exterior arena envelope without obvious wall clipping.
- Exterior and interior origins align on the same bottom-center plane.
- Interior scale matches exterior scale without rescaling.
- The open-sky interior aligns with the open colosseum rim and does not imply a sealed roof.
- `light_0`, `light_1`, and `light_2` are inside the interior volume.
- `camera_target` is inside the room and points to the central holographic leaderboard.
- Mesh rotations and scales are clean after import; transforms do not create unexpected shifts.

## Scene 9 Camera Checks

Scene 9: Leaderboard & Competition District.

- Scroll: approximately 55%.
- Camera: approach like entering colosseum, then push into arena floor.
- Visible: futuristic colosseum, achievement towers, 3D leaderboard, competition zones, challenge cards, warm light blooms.
- Text context: "21 days. That's not a streak. That's a habit. And I saw it before you did."
- Pipeline context: future lightning bolt entry at arena apex.

Capture:

- Exterior approach shot: colosseum, entry arch, rim, beacons, and curved leaderboard panel prominent.
- Arena floor push shot: open-sky bowl, central leaderboard, achievement towers, and competition zones readable.
- SIA-to-Leaderboard lightning route shot: clear future arc corridor to the arena apex.
- Leaderboard three-quarter shot: close verification of colosseum silhouette and open rim.
- Wide skyline shot: all seven approved structures visible for Gate 6.

## Gate 6 Cohesion Criteria

- Material darkness is consistent across modules.
- Detail density is comparable and appropriate to each architectural language.
- Scale relationships are correct; SIA dominates.
- Architectural variety remains clear: spire, gym megastructure, sanctuary, crystalline tower, library cathedral, communication hub, arena colosseum.
- All structures feel like the same dark premium city.

## Deliverables

- Run `shared/lighting-rig.py` before screenshots.
- Save integration blend: `modules/06-leaderboard-competition/integration-session-28.blend`.
- Save metrics JSON: `modules/06-leaderboard-competition/integration-session-28-report.json`.
- Save screenshots in `modules/06-leaderboard-competition/screenshots/`.
- Update `modules/06-leaderboard-competition/REVIEW.md` with Session 28 results and QA verdict.
- Update `PROGRESS.md` only after the integration check passes.
