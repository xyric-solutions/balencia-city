# Session 24: Chat & Communication - Integration Test

## Quick Context

- Project: Balencia City v3 - interactive cinematic 3D city, not a website.
- Aesthetic: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz.
- Sky: Ink-blue `#0A0A0F`; surfaces near `#1E1E28`; warm amber fog.
- Brand balance: 60% burnt orange `#FF5E00`, 30% forest green `#34A853`, 10% royal purple `#7F24FF`.
- SIA Tower remains the absolute center and tallest structure.
- Materials use the 7-slot runtime system: base, accent, glass, detail, emissive, energy, holo.
- Export convention: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center.

## Session Scope

- Module: #05 Chat & Communication - Hyper-Connected Hub
- Phase position: Phase 3, Step 3.2
- Current phase: integration
- Current session: 24
- Focus: Verify Chat exterior and interior alignment, Scene 8 camera readability, and cohesion with SIA, Fitness, Yoga, Finance, and Knowledgebase.
- This is a verification session. Do not create new module geometry.

## Approved Assets To Load

This module:

- Exterior: `modules/05-chat-communication/exterior/approved/chat-ext.glb`
- Interior: `modules/05-chat-communication/interior/approved/chat-int.glb`

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

## Approximate Orbital Placement

- SIA Tower: `(0, 0, 0)`
- Fitness: `(25, 25, 0)`
- Yoga & Wellbeing: `(35, 10, 0)`
- Finance: `(35, -5, 0)`
- Knowledgebase: `(30, -20, 0)`
- Chat & Communication: `(18, -34, 0)`

The exact city layout is finalized in Phase 6. For this integration pass, use 30-40 unit ring spacing from SIA and preserve the southeast communication-hub read.

## Alignment Checks

Verify the Chat exterior and interior together:

- Interior fits within the exterior/plaza envelope without obvious wall clipping.
- Exterior and interior origins align on the same bottom-center plane.
- Interior scale matches exterior scale without rescaling.
- The open/windowed wall of the Communication Nexus faces outward toward the south ring approach.
- `light_0`, `light_1`, and `light_2` are inside the interior volume.
- `camera_target` is inside the room and points to the conversation-thread focal web.
- Mesh rotations and scales are clean after import; transforms do not create unexpected shifts.

## Scene 8 Camera Checks

Scene 8: Chat & Communication District.

- Scroll: approximately 48%.
- Camera: multi-tower sweep to push into nexus.
- Visible: interconnected towers with signal lights, then conversation threads, calling towers, and holographic whiteboards.
- Text context: "Every conversation teaches me something about you. I listen to understand, not just respond."

Capture:

- Exterior sweep shot: Chat cluster prominent, sky-bridges and antennas readable.
- Nexus push shot: open-wall view toward conversation-thread focal web.
- SIA-to-Chat pipeline route shot: clear future hard-pipeline arc corridor.
- Wide skyline shot: all six approved structures visible for Gate 6.

## Gate 6 Cohesion Criteria

- Material darkness is consistent across modules.
- Detail density is comparable and appropriate to each architectural language.
- Scale relationships are correct; SIA dominates.
- Architectural variety remains clear: spire, gym megastructure, sanctuary, crystalline tower, library cathedral, communication hub.
- All structures feel like the same dark premium city.

## Deliverables

- Run `shared/lighting-rig.py` before screenshots.
- Save integration blend: `modules/05-chat-communication/integration-session-24.blend`.
- Save metrics JSON: `modules/05-chat-communication/integration-session-24-report.json`.
- Save screenshots in `modules/05-chat-communication/screenshots/`.
- Update `modules/05-chat-communication/REVIEW.md` with Session 24 results and QA verdict.
- Update `PROGRESS.md` only after the integration check passes.
