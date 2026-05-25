# Session 40: Recovery & Sleep - Integration Test

## Quick Context

- Project: Balencia City v3 - interactive cinematic 3D city, not a website.
- Aesthetic: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz.
- Sky: Ink-blue `#0A0A0F`; surfaces near `#1E1E28`; warm amber fog.
- Brand balance: 60% burnt orange `#FF5E00`, 30% forest green `#34A853`, 10% royal purple `#7F24FF`.
- SIA Tower remains the absolute center and tallest structure.
- Materials use the 7-slot runtime system: base, accent, glass, detail, emissive, energy, holo.
- Export convention: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center.

## Session Scope

- Module: #09 Recovery & Sleep - Floating Dreamscape
- Phase position: Phase 4, Step 4.2
- Current phase: integration
- Current session: 40
- Focus: Verify Recovery exterior and interior alignment, Scene 12 camera readability, and cohesion with SIA, Fitness, Yoga, Finance, Knowledgebase, Chat, Leaderboard, Relationships, and Career.
- This is a verification session. Do not create new module geometry.

## Approved Assets To Load

This module:

- Exterior: `modules/09-recovery-sleep/exterior/approved/recovery-ext.glb`
- Interior: `modules/09-recovery-sleep/interior/approved/recovery-int.glb`

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

The exact city layout is finalized in Phase 6. For this integration pass, preserve the Session 38 Recovery cohesion position: a western dreamscape district with separation from Career and a visible but extremely light route from SIA to the top thread receiver.

## Alignment Checks

Verify the Recovery exterior and interior together:

- Interior fits within the cloud/lake exterior envelope without obvious shell clipping.
- Exterior and interior origins align on the same bottom-center plane.
- Interior scale matches exterior scale without rescaling.
- The open/windowed side of the Neural Recovery Chamber supports the Scene 12 floating approach.
- `light_0`, `light_1`, and `light_2` are inside the interior volume.
- `camera_target` is inside the room and points to the sleep brain hologram focal element.
- Mesh rotations and scales are clean after import; transforms do not create unexpected shifts.

## Scene 12 Camera Checks

Scene 12: Recovery & Sleep District.

- Scroll: approximately 76%.
- Camera: floating approach, then push into chamber.
- Visible: cloud structure over mirror lake, recovery pods, sleep brain hologram, dream particles, breathing walls.
- Text context: "Recovery isn't downtime. It's when I do my deepest work - connecting today's patterns to tomorrow's plan."
- Pipeline context: future faint thread from SIA, barely visible, not a hard tube.

Capture:

- Floating approach shot: cloud shell, mirror lake, light pillars, wisps, and top receiver readable.
- Chamber push shot: interior cutaway view toward sleep brain hologram, recovery pods, dream particles, and breathing wall.
- SIA-to-Recovery thread route shot: clear future faint-thread corridor without implying a visible tube.
- Recovery three-quarter shot: close verification of ethereal cloud-over-lake identity.
- Wide skyline shot: all ten approved structures visible for Gate 6.

## Gate 6 Cohesion Criteria

- Material darkness is consistent across modules.
- Detail density is comparable and appropriate to each architectural language.
- Scale relationships are correct; SIA dominates, Career remains tallest district, and Recovery remains deliberately soft and low.
- Architectural variety remains clear: spire, gym megastructure, sanctuary, crystalline tower, library cathedral, communication hub, arena colosseum, garden pavilion, professional tower cluster, dream cloud.
- All structures feel like the same dark premium city.

## Deliverables

- Run `shared/lighting-rig.py` before screenshots.
- Save integration blend: `modules/09-recovery-sleep/integration-session-40.blend`.
- Save metrics JSON: `modules/09-recovery-sleep/integration-session-40-report.json`.
- Save screenshots in `modules/09-recovery-sleep/screenshots/`.
- Update `modules/09-recovery-sleep/REVIEW.md` with Session 40 results and QA verdict.
- Update `PROGRESS.md` only after the integration check passes.
