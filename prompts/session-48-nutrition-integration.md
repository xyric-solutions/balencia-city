# Session 48: Nutrition - Integration Test

## Quick Context

- Project: Balencia City v3 - interactive cinematic 3D city, not a website.
- Aesthetic: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz.
- Sky: Ink-blue `#0A0A0F`; surfaces near `#1E1E28`; warm amber fog.
- Brand balance: 60% burnt orange `#FF5E00`, 30% forest green `#34A853`, 10% royal purple `#7F24FF`.
- SIA Tower remains the absolute center and tallest structure.
- Materials use the 7-slot runtime system: base, accent, glass, detail, emissive, energy, holo.
- Export convention: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center.

## Session Scope

- Module: #11 Nutrition - Organic Farm-Structure
- Phase position: Phase 4, Step 4.4
- Current phase: integration
- Current session: 48
- Focus: Verify Nutrition exterior and interior alignment, Scene 14 camera readability, future hard-pipeline route, and cohesion with all eleven previously approved structures.
- This is a verification session. Do not create new module geometry.

## Approved Assets To Load

This module:

- Exterior: `modules/11-nutrition/exterior/approved/nutrition-ext.glb`
- Interior: `modules/11-nutrition/interior/approved/nutrition-int.glb`

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
- Relationships exterior: `modules/07-relationships/exterior/approved/relationships-ext.glb`
- Relationships interior: `modules/07-relationships/interior/approved/relationships-int.glb`
- Career exterior: `modules/08-career/exterior/approved/career-ext.glb`
- Career interior: `modules/08-career/interior/approved/career-int.glb`
- Recovery exterior: `modules/09-recovery-sleep/exterior/approved/recovery-ext.glb`
- Recovery interior: `modules/09-recovery-sleep/interior/approved/recovery-int.glb`
- AI Analytics exterior: `modules/10-ai-analytics/exterior/approved/analytics-ext.glb`
- AI Analytics interior: `modules/10-ai-analytics/interior/approved/analytics-int.glb`

## Approximate Orbital Placement

- SIA Tower: `(0, 0, 0)`
- Fitness: `(26, 25, 0)`
- Yoga & Wellbeing: `(36, 10, 0)`
- Finance: `(35, -6, 0)`
- Knowledgebase: `(31, -22, 0)`
- Chat & Communication: `(19, -36, 0)`
- Leaderboard & Competition: `(-8, -45, 0)`
- Relationships: `(8, -59, 0)`
- Career: `(-30, -34, 0)`
- Recovery & Sleep: `(-43, -8, 0)`
- AI Analytics: `(-31, 14, 0)`
- Nutrition: `(-12, 39, 0)`

The exact city layout is finalized in Phase 6. For this integration pass, place Nutrition in the north/northwest living-farm slot between AI Analytics and Fitness, with a clear future hard-pipeline corridor from SIA to the orange receiver.

## Alignment Checks

Verify the Nutrition exterior and interior together:

- Interior origin aligns with exterior origin on the same bottom-center plane.
- Interior scale matches exterior scale without rescaling.
- Interior width and height fit the vertical-farm envelope; the Nourishment Hall may extend beyond the compact exterior depth as a documented cinematic cutaway/readability exception.
- The open/windowed side supports the Scene 14 hall push toward the living market.
- `light_0`, `light_1`, and `light_2` are inside the interior volume.
- `camera_target` is inside the room and points to the living market focal element.
- Mesh rotations and scales are clean after import; transforms do not create unexpected shifts.

## Scene 14 Camera Checks

Scene 14: Nutrition District.

- Scroll: approximately 88%.
- Camera: farm tier approach, then push into Nourishment Hall.
- Visible: vertical farms with amber grow lights, greenhouse sections, open market base, Nourishment Hall, nutrition holograms, living market, chef prep zones.
- Pipeline context: future hard pipeline from SIA with a clear arced route to the Nutrition receiver, but no final Phase 5 pipeline geometry yet.

Capture:

- Farm tier approach shot: stepped green/amber vertical-farm identity readable.
- Nourishment Hall push shot: interior cutaway toward communal tables and living market.
- SIA-to-Nutrition hard-pipeline route shot: clear future corridor from SIA to the receiver.
- Nutrition three-quarter shot: close verification of farm-structure silhouette.
- Wide skyline shot: all twelve approved modules visible for Gate 6.

## Gate 6 Cohesion Criteria

- Material darkness is consistent across modules.
- Detail density is comparable and appropriate to each architectural language.
- Scale relationships are correct; SIA dominates, Career remains tallest district, and Nutrition reads as a lower tiered farm-structure by design.
- Architectural variety remains clear: central tower, gym megastructure, sanctuary, crystalline tower, library cathedral, communication hub, arena colosseum, garden pavilion, professional tower cluster, dream cloud, data cathedral, vertical farm.
- All structures feel like the same dark premium city.

## Deliverables

- Run `shared/lighting-rig.py` before screenshots.
- Save integration blend: `modules/11-nutrition/integration-session-48.blend`.
- Save metrics JSON: `modules/11-nutrition/integration-session-48-report.json`.
- Save screenshots in `modules/11-nutrition/screenshots/`.
- Update `modules/11-nutrition/REVIEW.md` with Session 48 results and QA verdict.
- Update `PROGRESS.md` only after the integration check passes.
