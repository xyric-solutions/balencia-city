# Session 38: Recovery & Sleep -- Exterior Detail, Polish & Export

## Quick Context

- Project: Balencia City v3, an interactive cinematic 3D city.
- Aesthetic: dark premium night architecture, Apple spatial computing clarity, UE5 archviz weight.
- Avoid: Lego proportions, neon overload, photorealism, daytime, cartoon, suburban scale.
- Sky/world: Ink-blue `#0A0A0F`; surfaces stay dark and premium.
- SIA Tower: central 100+ floor anchor, roughly 40u tall; all districts remain clearly shorter.
- Materials: runtime reads exact slot names: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Export: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center.
- This session completes the Recovery exterior and prepares it for the interior session.

## Session Scope

- Module: #09 Recovery & Sleep -- Floating Dreamscape
- Position: Phase 4, Step 4.2
- District color: Ethereal Indigo `#6366F1`
- Focus: exterior detail, polish, material balancing, dark-first proof, export.
- Final budget: Exterior 10K-15K tris; hard cap 15K.
- Previous session tris: 8,288.
- Remaining budget: 6,712 tris.
- Previous blend: `modules/09-recovery-sleep/exterior/drafts/recovery-s37-major-forms.blend`.
- Energy slots: energy=true, holo=false.

## Previous Session State

Session 37 built the Recovery major forms: mirror-still lake, five indigo light
pillars, smooth concave underside, overlapping translucent cloud lobes, nested
inner shell glow, twelve star points, five trailing wisps, and a minimal orange
top thread receiver. Gates 1-2 passed. No QA fixes are required.

The detail pass must preserve the identity: a soft floating cloud over a mirror
lake with no domes, no walkways, no facade grids, no hard towers, and no visible
floor separations.

## Architectural Identity

The Recovery Dreamscape is the most ethereal structure in Balencia City: a
cloud-like organic form hovering above a mirror-still lake on soft indigo light
pillars. Every surface curves, every corner is rounded, and every transition is
smooth. The exterior should feel like a continuous sleep cloud with nested glass
shells, sparse star lights, trailing wisps, and a barely visible SIA thread
reception point.

Silhouette signature: floating cloud over mirror lake. It must remain distinct
from Yoga's domes/platforms, Relationships' garden pavilion/moat, Career's tower
cluster, and Finance's crystal geometry.

## Detail Elements To Add

- Finer shell-layer articulation: dark crescent seams and smooth inner shadow
  surfaces that reveal layered glass without creating facade floors.
- Cloud-lobe transition polish: soft contour ribbons and underside shadow panels
  that make the lobes feel merged instead of separate spheres.
- Lake reflection polish: dark lake bed visible through glass, subtle reflection
  ellipses, mirrored star glints, and still-water edge refinement.
- Pillar glow hardware: soft ripple collars, cloud-contact halos, and quiet
  receptor pads at the beam endpoints.
- Wisp taper refinement: add small fading beads and terminal taper pieces along
  existing wisps without turning them into cables.
- Star-light cleanup: keep the distribution sparse, jewel-like, and non-grid.
- Energy receiver polish: refine only the district-side top wisp; do not build
  the final Phase 5 SIA energy thread.

## Material Assignment

| Surface | Slot | Notes |
|---------|------|-------|
| Outer translucent shell | glass | Muted indigo tint, smooth alpha read |
| Inner translucent shell | glass | Slightly denser nested translucent mass |
| Indigo light pillars | emissive | `#6366F1` at restrained intensity |
| Mirror-still lake surface | glass | Reflective flat water plane |
| Lake bed and underside shadows | base | Dark architectural mass visible through glass |
| Shell gaps and contour seams | detail | Dark voids separating nested shell layers |
| Star lights and aurora glow | emissive | Sparse indigo/silver glow markers |
| Trailing wisps | accent | Soft indigo tapering forms, no hard pipes |
| Energy thread terminus | energy | Minimal orange receiver only |

## Workflow

1. Load `recovery-s37-major-forms.blend`.
2. Verify the scene matches the prior summary: 59 mesh objects and about 8,288 tris.
3. Normalize material slots to exactly `base`, `accent`, `glass`, `detail`, `emissive`, `energy`; no `holo`.
4. Add detail elements in the order listed above, assigning materials immediately.
5. Keep every added feature organic, low contrast, and rounded.
6. Run the polish checklist: no default materials, no unconnected accidental floats,
   no z-fighting, no hard facade bands, no visible floors.
7. Verify the final source triangle count is between 10K and 15K.
8. Save the detailed source blend as `recovery-s38-detail-export.blend`.
9. Capture final front, three-quarter, distance, and dark-first screenshots.
10. Export a Draco GLB to `exterior/drafts/recovery-ext-draft-s38.glb`.
11. Validate the GLB: no cameras/lights, no rogue materials, no holo, min z = 0,
    no non-identity mesh transforms, file size in budget.
12. If gates pass, copy the GLB to `exterior/approved/recovery-ext.glb`.
13. Capture all-ten exterior cohesion proof with SIA plus all approved districts.
14. Write `session38-metrics.json` and `session38-qa-import.json`.
15. Update REVIEW and PROGRESS only after QA passes.

## Quality Targets

- Gate 1: still reads as Recovery's floating dream cloud at thumbnail scale.
- Gate 2: civic-scale, 20-floor-equivalent form without visible floors.
- Gate 3: valid material slots only; no `holo`; dark structural/base mass is
  visible enough to satisfy dark-first readability.
- Gate 4: with emissive strengths at zero, the lake, underside, shell layers,
  pillars, and wisps remain legible as architecture.
- Gate 5: 10K-15K tris, 80-300 KB GLB, bottom-centered origin, clean import.
- Gate 6: sits coherently beside the nine approved exteriors while remaining the
  softest and most ethereal district.

## Do Not Do

- Do not model the Recovery interior.
- Do not add recovery pods, sleep brain hologram, or interior props.
- Do not add the final Phase 5 energy pipeline from SIA.
- Do not add domes, walkways, rails, visible floors, hard towers, or crystal spikes.
- Do not download or import external reference models.

## End Criteria

- `recovery-s38-detail-export.blend` saved.
- `recovery-ext-draft-s38.glb` exported and validated.
- `recovery-ext.glb` promoted to approved after Gates 1-6 pass.
- Screenshots saved under `modules/09-recovery-sleep/screenshots/`.
- `REVIEW.md` records Session 38 build and QA.
- `PROGRESS.md` advances to Session 39, Recovery interior.
