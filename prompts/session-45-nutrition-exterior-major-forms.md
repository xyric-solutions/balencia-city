# Session 45: Nutrition - Organic Farm-Structure - Exterior Major Forms

## Quick Context

- Project: Balencia City v3, an interactive cinematic 3D city.
- Aesthetic: dark premium night architecture, Apple spatial computing clarity, UE5 archviz weight.
- Avoid: toy proportions, neon overload, daytime, cartoon, suburban scale.
- Sky/world: Ink-blue `#0A0A0F`; surfaces stay dark and premium.
- SIA Tower: central 100+ floor anchor, roughly 40u tall; every district remains clearly shorter.
- Materials: runtime reads exact slot names: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Export later: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center.
- This session saves a draft `.blend`; export waits for the detail session.

## Session Scope

- Module: #11 Nutrition - Organic Farm-Structure.
- Position: Phase 4, Step 4.4.
- District color: Warm Amber `#D97706`.
- Floors: 12.
- Focus: Primary silhouette geometry and major architectural forms only.
- Budget: Under 60% of Exterior 12K-18K tris; target below 10.8K tris.
- Energy slots: energy=true, holo=false.
- This session: exterior major forms. Next session: detail, polish, dark-first proof, export.

## Architectural Identity

The Nutrition Farm-Structure is Balencia's only visibly alive building. It should read
as a stepped vertical farm, with horizontal planting terraces and cascading green
life softened by warm amber grow lights. The form bridges organic agriculture and
metropolitan architecture: a dark structural pyramid softened by rounded tier edges,
greenhouse insertions, irrigation channels, and an open market base.

Silhouette signature:

- A 12-floor stepped pyramid profile, wide at the base and smaller at the roof.
- Green farm layers and cascading plant curtains on tier edges.
- Amber grow-light bands wrapping each terrace.
- Two to three glass greenhouse volumes attached to the facade.
- An open-sided ground market volume under the farm body.
- A roof kitchen chimney/vent cap and an orange hard-pipeline receiver.

It must not resemble Relationships' low garden pavilion, Recovery's cloud lake,
Analytics' data cathedral, Yoga's floating domes, or Finance's crystalline tower.

## Scene Preparation

1. Clear the Blender scene completely.
2. Run `shared/lighting-rig.py` to establish the cinematic three-light setup.
3. Run `shared/material-library.py` with `#D97706`, `include_energy=True`, `include_holo=False`.
4. Verify only allowed material slots are present: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`.
5. Confirm world background remains near `#0A0A0F`.

## What To Build

Build only the major silhouette elements:

- Tiered main structure: 12 rounded floors stepping back into a farm-pyramid profile.
- Vertical farm layers: broad planting beds on the terrace ledges.
- Cascading green plant curtains: simplified, chunky foliage geometry spilling over tier edges.
- Amber grow light strips: warm horizontal bands above every farm tier.
- Glass greenhouse sections: 2-3 transparent facade enclosures with simple internal racks.
- Open market area: a covered but open-sided ground-level gathering space.
- Produce display masses: warm amber-lit display blocks visible in the market opening.
- Roof kitchen chimney/ventilation stack with a vent cap.
- Water irrigation channels: thin dark groove/channel geometry along tier edges.
- Energy pipeline terminus: orange hard socket only; no final Phase 5 pipeline.

## Material Assignment

| Surface | Slot | Notes |
|---------|------|-------|
| Tiered structure walls | base | Warm-toned dark surface, roughness 0.80 |
| Farm bed surfaces on tiers | detail | Flat planting surfaces, roughness 0.60 |
| Cascading plant geometry | accent | Green with faint amber emission at edges |
| Amber grow light strips | emissive | `#D97706` warm amber, horizontal bands per tier |
| Glass greenhouse enclosures | glass | Transparent sections, alpha 0.86, amber tint |
| Internal hydroponic racks | detail | Shelving geometry inside greenhouses |
| Open market ground level | base | Covered space, warm-toned ground surface |
| Produce display shelves | accent | Amber-lit small display forms near entrance |
| Kitchen chimney/ventilation | detail | Cylindrical roof element, industrial |
| Water irrigation channels | detail | Thin groove geometry along tier edges |
| Energy pipeline terminus | energy | `#FF5E00` orange where SIA pipeline connects |

## Build Workflow

1. Build the ground market slab, open columns, and canopy first.
2. Stack the 12 rounded tier volumes above the market, each floor stepping inward.
3. Add broad farm-bed surfaces on every terrace ledge.
4. Add amber grow-light bands along front, rear, and side edges.
5. Add simplified cascading plant curtains on front and side tiers.
6. Add 2-3 greenhouse volumes and their internal rack silhouettes.
7. Add the roof chimney/vent cap and the orange hard-pipeline receiver socket.
8. Add primary irrigation channels along selected tier edges.
9. Take front, three-quarter, and distance screenshots.
10. Save the `.blend` to `modules/11-nutrition/exterior/drafts/`.
11. Write metrics JSON with per-object and category triangle counts.

## QA Gates For This Session

Gate 1 - Silhouette Clarity:

- Reads as a vertical farm/terraced nutrition district at 200px.
- Unique among all approved structures: not a cloud, garden pavilion, data cathedral, arena, crystal, or tower cluster.
- SIA Tower remains unmistakably taller.
- Roof vent, greenhouse boxes, grow bands, and stepped farm profile are clear.

Gate 2 - Architectural Scale:

- Reads as a 12-floor metropolitan farm-structure, not a small greenhouse.
- Floor indicators are visible through the stacked terraces and grow-light bands.
- At least three sub-elements are visible: market base, tiered body, greenhouse volumes, plant curtains, roof vent, and energy socket.
- Primary volumes are articulated before detail approval.

## What Not To Do

- Do not build the Nourishment Hall interior.
- Do not export GLB or promote any approved asset in this session.
- Do not add the final SIA pipeline.
- Do not download or import reference models.
- Do not over-detail individual leaves, produce, signage, or tiny irrigation fittings.

## End Criteria

- Draft `.blend` saved as `nutrition-s45-major-forms.blend`.
- Three screenshots saved under `modules/11-nutrition/screenshots/`.
- Metrics saved as `session45-metrics.json`.
- REVIEW updated with Session 45 build notes and Gates 1-2 QA.
- PROGRESS advanced to Session 46, Nutrition exterior detail, only after QA approval.
