# Session 27: Leaderboard & Competition -- Arena Colosseum — Interior

## Session Scope

- Module: #06 Leaderboard & Competition
- Position: Phase 3, Step 3.3
- District color: Bright Coral `#FB7185`
- Focus: Single interior room, focal leaderboard, props, runtime empties, export
- Budget: Interior 5K-10K tris
- Energy slots: energy=Yes, holo=No

## Room Description

Build the arena interior as a bowl-shaped competition floor with tiered seating
rising on all sides and an open-sky rim above. The room is a separate GLB loaded
on demand when the user scrolls into the Leaderboard scene. It should feel like a
curated competition space inside the approved colosseum exterior, with dark
structural mass readable before any glow.

## Focal Element

The central 3D holographic leaderboard is a cylindrical projection about 4m wide
and 6m tall at the dead center of the competition floor. It shows rank positions
and score shifts with real low-poly geometry. Use `glass`, `emissive`, `accent`,
and `energy`; do not create a `holo` material because the master slot table marks
Leaderboard as energy-only.

## Props

- Achievement towers: 8-10 vertical perimeter pillars with varied heights and glow
- Head-to-head competition zones: two paired floor circle markings with challenge lines
- Team challenge platforms: two raised rectangular platforms with 5v5 seating
- Orbiting challenge cards: 4-6 translucent rectangles around the central leaderboard
- Milestone light bloom emitters: two soft golden/coral expanding sphere forms
- Progression monuments: two ascending stepped structures with brighter upper steps
- Tiered seating rows: concentric low-poly rings rising from floor to rim

## Runtime Empties

- `light_0`: above competition floor center through the open sky
- `light_1`: behind the leaderboard cylinder for coral backlight
- `light_2`: achievement tower perimeter for warm gold accent light
- `camera_target`: center of competition floor at human chest height, aimed at the leaderboard

## Build Rules

1. Start from a fresh Blender scene, not the exterior blend.
2. Run `shared/lighting-rig.py`.
3. Run `shared/material-library.py` with `#FB7185`, `include_energy=True`, `include_holo=False`.
4. Build the room shell first: floor, curved walls, partial ceiling/rim, one open/windowed side.
5. Build the central leaderboard before props and make it visually dominant.
6. Place props around the perimeter so they frame the focal cylinder.
7. Export only meshes and runtime empties. No cameras or lights in the GLB.
8. Save draft outputs under `modules/06-leaderboard-competition/interior/drafts/`.
9. Promote to `interior/approved/leaderboard-int.glb` only after QA passes.

## End Criteria

- Room shell complete with floor, wall panels, partial open-sky ceiling rim, and open front
- Focal cylindrical leaderboard clearly dominant
- All seven supporting prop categories represented
- Required empties exported with exact names
- Materials use only the valid slot names and no `holo`
- Dark-first screenshot proves geometry remains readable with emissions disabled
- Total tris within 5K-10K and GLB size within 60-200 KB
