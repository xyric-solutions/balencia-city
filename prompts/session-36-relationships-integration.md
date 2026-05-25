# Session 36: Relationships - Integration Test

## Quick Context

- Project: Balencia City v3 - interactive cinematic 3D city, not a website.
- Aesthetic: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz.
- Sky: Ink-blue `#0A0A0F`; surfaces near `#1E1E28`; warm amber fog.
- Brand balance: 60% burnt orange `#FF5E00`, 30% forest green `#34A853`, 10% royal purple `#7F24FF`.
- SIA Tower remains the absolute center and tallest structure.
- Materials use the 7-slot runtime system: base, accent, glass, detail, emissive, energy, holo.
- Export convention: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center.

## Session Scope

- Module: #07 Relationships - Garden Ecosystem
- Phase position: Phase 4, Step 4.1
- Current phase: integration
- Current session: 36
- Focus: Verify Relationships exterior and interior alignment, Scene 10 camera readability, and cohesion with SIA, Fitness, Yoga, Finance, Knowledgebase, Chat, Leaderboard, and Career.
- This is a verification session. Do not create new module geometry.

## Approved Assets To Load

This module:

- Exterior: `modules/07-relationships/exterior/approved/relationships-ext.glb`
- Interior: `modules/07-relationships/interior/approved/relationships-int.glb`

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
- Career exterior: `modules/08-career/exterior/approved/career-ext.glb`
- Career interior: `modules/08-career/interior/approved/career-int.glb`

## Approximate Orbital Placement

- SIA Tower: `(0, 0, 0)`
- Fitness: `(25, 25, 0)`
- Yoga & Wellbeing: `(35, 10, 0)`
- Finance: `(35, -5, 0)`
- Knowledgebase: `(30, -20, 0)`
- Chat & Communication: `(18, -34, 0)`
- Leaderboard & Competition: `(-8, -44, 0)`
- Career: `(-28, -34, 0)`
- Relationships: `(7, -58, 0)`

The exact city layout is finalized in Phase 6. For this integration pass, preserve the Session 34 Relationships cohesion position: a southern low garden district with separation from Leaderboard/Chat and a visible warm-mist corridor from SIA to the roof diffuser.

## Alignment Checks

Verify the Relationships exterior and interior together:

- Interior fits within the low pavilion/moat exterior envelope without obvious wall clipping.
- Exterior and interior origins align on the same bottom-center plane.
- Interior scale matches exterior scale without rescaling.
- The open/windowed wall of the Connection Gardens faces the outer-ring Scene 10 approach.
- `light_0`, `light_1`, and `light_2` are inside the interior volume.
- `camera_target` is inside the room and points to the family bonding dome focal element.
- Mesh rotations and scales are clean after import; transforms do not create unexpected shifts.

## Scene 10 Camera Checks

Scene 10: Relationships District.

- Scroll: approximately 62%.
- Camera: gentle descent, then push into gardens.
- Visible: low curved garden ecosystem, connection gardens, family dome, trust vines, memory walkways.
- Text context: "The people in your life shape your health more than any workout. I track those connections too."
- Pipeline context: future warm mist delivery from SIA, not a hard tube.

Capture:

- Gentle descent shot: low pavilion, moat, bridges, cascading terraces, domes, and roof mist receiver readable.
- Connection gardens push shot: interior cutaway view toward family bonding dome, rose paths, benches, vines, and memory timeline.
- SIA-to-Relationships mist route shot: clear future warm-mist corridor without implying a hard pipeline.
- Relationships three-quarter shot: close verification of anti-tower garden identity.
- Wide skyline shot: all nine approved structures visible for Gate 6.

## Gate 6 Cohesion Criteria

- Material darkness is consistent across modules.
- Detail density is comparable and appropriate to each architectural language.
- Scale relationships are correct; SIA dominates, Career remains tallest district, Relationships remains deliberately shortest.
- Architectural variety remains clear: spire, gym megastructure, sanctuary, crystalline tower, library cathedral, communication hub, arena colosseum, professional tower cluster, garden pavilion.
- All structures feel like the same dark premium city.

## Deliverables

- Run `shared/lighting-rig.py` before screenshots.
- Save integration blend: `modules/07-relationships/integration-session-36.blend`.
- Save metrics JSON: `modules/07-relationships/integration-session-36-report.json`.
- Save screenshots in `modules/07-relationships/screenshots/`.
- Update `modules/07-relationships/REVIEW.md` with Session 36 results and QA verdict.
- Update `PROGRESS.md` only after the integration check passes.
