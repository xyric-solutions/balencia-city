# Phase 7 Session 60 Plan

Date: 2026-05-25  
Scope: City legibility pass for the Balencia City v3 R3F app.

Status: Initial pass / review pending

## Audit Finding

The approved structures, interiors, energy assets, assembly, and Session 59 scroll timeline remain valid. User review found a Phase 7 readability issue: from the first overview, the current ground plane reads as an abstract circular diagram rather than a relatable city. District identities also need explicit naming beyond the scene overlay.

## Visual Direction

- Build an app-level Urban Atlas ground system: central SIA civic plaza, ring roads, radial boulevards, district pads, sidewalks, canals or reflective strips, street lamps, and low-rise city-block infill.
- Keep the premium dark-first Balencia language. Use mostly non-emissive obsidian, charcoal, warm stone, glass, and subtle green or blue cues; reserve strong orange for energy infrastructure and wayfinding.
- Add hybrid labels using module-plus-place language:
  - SIA tower
  - Fitness complex
  - Yoga sanctuary
  - Finance bank
  - Knowledgebase library
  - Chat hub
  - Competition arena
  - Relationships garden
  - Career towers
  - Recovery and sleep
  - AI analytics
  - Nutrition farm

## Acceptance Criteria

- Scene 1 reads as a city within 3 seconds, not just a diagram of objects on a disk.
- Scenes 4, 6, and 11 clearly show active-district labels and district-specific ground cues.
- Scene 15 shows key district labels without clutter and preserves the cross-pillar revelation.
- Scene 17 remains clean, premium, and legible as the closing city view.
- Approved GLBs are not modified; changes stay in the app/context layer.
- Added procedural geometry targets less than 25K triangles and keeps active city geometry below the existing 250K ceiling.

## Required QA Screenshots

- Desktop: Scene 1, Scene 4, Scene 6, Scene 11, Scene 15, Scene 17.
- Mobile 390 x 844: Scene 1 and Scene 15, verifying labels do not collide with the overlay.
- Browser console: no errors or warnings after loading and scene navigation.

## Review Notes From User Screenshot

- Several district labels are truncated or too narrow for their full names.
- Overview labels need curated placement instead of relying only on projected 3D positions.
- The ground pass is improving the city read, but needs smaller structures, walls, district boundaries, and street-level detail in later sessions.
- The outer black void needs a premium horizon/edge treatment so the city no longer feels isolated in empty space.
- Session 60 remains review pending until the Session 61-64 backlog is completed and QA screenshots pass.

## Follow-Up Backlog

- Session 61: Label legibility pass.
- Session 62: City life and ground detail.
- Session 63: Void and horizon pass.
- Session 64: Integration QA and documentation closeout.

## Next Step After Review

Run Session 61 before resuming energy shader work: repair label wrapping, placement, desktop overview layout, and mobile overview behavior.
