# Session 23: Chat & Communication -- Hyper-Connected Hub -- Interior

## Session Scope

- Module: #05 Chat & Communication -- Hyper-Connected Hub
- Position: Phase 3, Step 3.2
- District Color: Burnt Orange `#FF5E00`
- Focus: Single interior room -- focal element, props, empties, export
- Budget: Interior 5K-10K tris, 60-200 KB GLB
- Energy slots: energy=Yes, holo=No
- Exterior status: Approved in Session 22A/22B, do not modify exterior

## Quick Context

- Project: Balencia City v3, an interactive cinematic 3D city
- Aesthetic: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz
- Mood: dark, premium, warm night, not cartoon or daytime
- Sky: Ink-blue `#0A0A0F`
- Main surfaces: `#1E1E28`, never pure black
- Brand mix: 60% Burnt Orange, 30% Forest Green, 10% Royal Purple
- SIA Tower: central 100+ floor anchor, every district remains shorter
- Material system: base, accent, glass, detail, emissive, energy, holo
- Slot names are runtime override keys and must be exact
- Export: GLB binary, Draco level 6, Y-up, no cameras or lights
- Origin: bottom-center, Y=0 plane
- Required scripts: `shared/lighting-rig.py`, then `shared/material-library.py`

## Interior Requirements

- One room only, loaded on demand during this district scene
- Same 7-slot material system as exteriors
- Create `light_0`, `light_1`, `light_2`
- Create one empty named `camera_target`
- Add 4-8 identifiable module-specific prop groups
- Build a clear center-of-attention focal element
- Complete room shell: floor, walls, ceiling
- One wall must be open or windowed for exterior light
- Props should frame the focal element rather than compete with it
- Props should be readable by silhouette at low poly count
- Dark-first readability matters more than glow strength

## Room Description

The main tower pod ground floor opens into a communication nexus.

The room is circular and built around visible conversation. Conversation threads
manifest as floating burnt-orange light ribbons that arc between active stations.
The threads should feel like a physical web of communication flow above the
central collaboration zone.

Voice and video calling towers stand at four cardinal points. They are tall
cylindrical booths with translucent walls and life-size remote participant
projections visible inside.

A central collaboration zone contains holographic whiteboards: large translucent
panels floating at varying angles with abstract notation and diagram marks.

Messages appear as glowing particles traveling along guided paths between
stations. The ceiling is an open lattice showing the underside of a sky-bridge
connection to an adjacent pod.

The word "holographic" in the spec should be interpreted through glass,
emissive, and energy geometry for this module. Do not create or assign the
`holo` material; Communication uses energy but not holo.

## Focal Element

The focal element is the floating conversation-thread web.

It must be the first thing the eye sees:

- Build it before surrounding props
- Place it above the collaboration table
- Aim `camera_target` at its center
- Use the highest-detail geometry allocation here
- Use layered arcs, rings, node points, and message particles
- Keep it readable when emissive strength is set to 0
- Avoid pure glow-only detail that disappears in dark-first QA

The hero object should read as connection, not decoration.

## Props List

1. Voice/video calling towers:
   Four cylindrical booths at cardinal points with glass walls, frames, and
   human-scale emissive projection silhouettes.

2. Holographic whiteboards:
   Three large translucent panels at different angles with notation marks.
   Use glass, accent frames, and emissive linework, not the holo slot.

3. Message particle paths:
   Curved overhead paths between booths with small message packets moving along
   them. Use energy sparingly and keep surface area controlled.

4. Central collaboration table:
   Large circular table below the conversation web. Add a ring, low support,
   and subtle floor uplight detail.

5. Seated pods:
   Six to eight compact seat forms around the table. Use simple silhouettes:
   seat pan, back, side arms, dark material.

6. Sky-bridge underside lattice:
   Ceiling grid and service ribs that imply the underside of the exterior
   sky-bridge connection. It should be structural, not decorative clutter.

7. Communication wall panels:
   Dark wall interface panels around the room perimeter with sparse orange
   accents and inactive screen surfaces.

## Required Empties

- `light_0`: Center of nexus at ceiling height, warm orange key light from above
- `light_1`: Behind calling towers, orange rim light for projection glow
- `light_2`: Under collaboration table, soft orange uplight from below
- `camera_target`: Center of the collaboration zone at standing height, aimed at
  the conversation-thread web

## Material Assignment

Use only these slots:

- `base`: room shell, floor, walls, ceiling, dark panels
- `accent`: restrained burnt-orange trims and structural highlights
- `glass`: calling-booth walls, whiteboards, front/windowed wall
- `detail`: frames, furniture, lattice, booth hardware, ribs
- `emissive`: conversation ribbons, projections, whiteboard marks, active screens
- `energy`: guided message paths and packet nodes

Do not use `holo`.

## Build Sequence

1. Start a fresh Blender scene.
2. Run `shared/lighting-rig.py`.
3. Run `shared/material-library.py` with `#FF5E00`, energy enabled, holo disabled.
4. Build the circular room shell.
5. Add a windowed/open front wall that connects visually to the city.
6. Add floor channels and wall articulation so dark-first mode has geometry.
7. Build the conversation-thread web above the collaboration table.
8. Add central collaboration table below it.
9. Add four calling booths at cardinal points.
10. Add whiteboards, message paths, seats, wall panels, and ceiling lattice.
11. Place `light_0`, `light_1`, `light_2`, and `camera_target`.
12. Run a material audit: every mesh has one of the approved slot names.
13. Run a dark-first screenshot with emissive strengths set to 0.
14. Confirm no object uses the `holo` material.
15. Confirm total tris are in the 5K-10K range.
16. Save `.blend` in `modules/05-chat-communication/interior/drafts/`.
17. Export draft `.glb` in `modules/05-chat-communication/interior/drafts/`.
18. Export selection must include mesh objects and empties only.
19. Export must exclude cameras and lights.
20. Capture final overview, entrance, topdown, and dark-first screenshots.

## End Criteria

- Room shell complete
- Focal element clearly dominant
- 4-8 prop groups present and identifiable
- `light_0`, `light_1`, `light_2` placed logically
- `camera_target` placed at the conversation web
- All materials use approved slot names
- Energy present, holo absent
- Dark-first test passes
- Total tris within 5K-10K
- GLB size within 60-200 KB or has a documented small variance
- GLB imports cleanly with empties present
- REVIEW.md can be updated with Session 23 build and QA results
