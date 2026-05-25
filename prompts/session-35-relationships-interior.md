# Session 35: Relationships -- Interior

## Session Scope

- **Module**: #07 Relationships
- **Position**: Phase 4.1, interior after approved exterior
- **District Color**: Warm Rose `#F43F5E`
- **Focus**: Single interior room -- focal element, props, empties, export
- **Budget**: Interior 4K-8K tris
- **Energy slots**: energy=true, holo=false

## Room Description

The interior is a garden-first space -- more landscape than architecture.
Walking paths wind through the room, lined with rose-colored energy threads
whose brightness varies with bond strength. AI relationship insight benches sit
along the paths with small transparent displays showing connection data.

A family bonding dome occupies the central space: a transparent dome-within-a-
room where warm rose threads connect the people within, visible through the
glass shell. Trust vines climb the walls and ceiling; memory timeline walkways
wrap the perimeter with abstract light moments. Empathy alcoves hold paired
seating and overlapping light fields.

The interior is loaded on demand when the user scrolls into this district's
scene. It should feel intimate, warm, and connected to the broader city night.

## Focal Element

Family bonding dome -- a transparent glass dome approximately 5m in diameter at
the room center, containing warm rose connection threads that visibly link the
positions within. This is the emotional heart of the space and the camera target.

## Props List

- Walking paths with rose energy threads: curved ground paths with emissive strip edges
- AI insight benches: 4 simple seat forms with small glass displays above
- Trust vines on walls/ceiling: organic tendril geometry of varying thickness
- Memory timeline holograms: 5-6 soft abstract light shapes flanking perimeter paths
- Empathy space alcoves: 2 recessed nooks with paired seating and overlapping light fields
- Family bonding dome: transparent glass hemisphere at center with interior thread geometry
- Low planter beds along paths: organic curved forms with rose-tinted vegetation accents

## Required Empties

- `light_0`: Inside family bonding dome -- warm rose key light radiating through glass
- `light_1`: Along memory timeline walkway -- soft amber accent for nostalgic warmth
- `light_2`: General ceiling fill -- diffused warm light, low intensity
- `camera_target`: Entrance of the central family bonding dome at eye height

## Material Assignment

Use the same 7-slot naming system as exteriors:

| Surface | Slot | Notes |
|---------|------|-------|
| Room shell floor, walls, ceiling | base | Dark garden architecture |
| Path trims, vine nodes, rose accents | accent | Warm rose inactive accents |
| Bonding dome, insight displays, aura fields | glass | Transparent warm glass |
| Benches, planters, vine trunks, ribs | detail | Furniture and garden structure |
| Rose connection threads, path edges | emissive | Soft relationship glow |
| Warm connection core and selected bond lines | energy | Opt-in energy slot, no hard pipeline |

## Workflow

1. Start a fresh Blender scene.
2. Run `shared/lighting-rig.py`.
3. Run `shared/material-library.py` with `#F43F5E`, `include_energy=True`, `include_holo=False`.
4. Build an enclosed garden room shell with one open/windowed front wall.
5. Build the family bonding dome first and verify it dominates the composition.
6. Add paths, benches, trust vines, memory timeline moments, empathy alcoves, and planter beds.
7. Add exact runtime empties: `light_0`, `light_1`, `light_2`, `camera_target`.
8. Render overview, entry, focal, topdown, and dark-first screenshots.
9. Export `relationships-int-draft-s35.glb` with Draco compression.
10. Import-check the GLB and promote to `interior/approved/relationships-int.glb` only if Gates 3, 4, 5, and 7 pass.

## End Criteria

- Room shell complete: floor, walls, ceiling, one open/windowed wall
- Family bonding dome built and clearly dominant
- 4-8 supporting prop categories present and identifiable
- Runtime empties placed and exported
- Materials use valid slots only: base, accent, glass, detail, emissive, energy
- No holo slot
- Dark-first screenshot readable
- Total tris within 4K-8K
- GLB size within 50-180 KB
- `.blend`, `.glb`, screenshots, metrics, and QA JSON saved under module artifacts
