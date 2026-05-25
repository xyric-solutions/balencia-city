# Session 37: Recovery & Sleep -- Floating Dreamscape -- Exterior Major Forms

## Quick Context

- Project: Balencia City v3, an interactive cinematic 3D city.
- Aesthetic: dark premium night architecture, Apple spatial computing clarity, UE5 archviz weight.
- Avoid: Lego proportions, neon overload, photorealism, daytime, cartoon, suburban scale.
- Sky/world: Ink-blue `#0A0A0F`; surfaces stay dark and premium.
- SIA Tower: central 100+ floor anchor, roughly 40u tall; all districts remain clearly shorter.
- Materials: runtime reads exact slot names: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Export later: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center.
- This session saves a draft `.blend`; export waits for the detail session.

## Session Scope

- Module: #09 Recovery & Sleep -- Floating Dreamscape
- Position: Phase 4, Step 4.2
- District color: Ethereal Indigo `#6366F1`
- Floors: Undefined continuous form; scale should read as about 20 floors without visible floor separations.
- Focus: Primary silhouette geometry only.
- Budget: Under 60% of Exterior 10K-15K tris; target below 9K tris.
- Energy slots: energy=true, holo=false.
- This session: exterior major forms. Next session: detail, polish, dark-first proof, export.

## Architectural Identity

The Recovery Dreamscape is the most ethereal structure in Balencia City: a cloud-like
organic form hovering above a mirror-still lake on pillars of soft indigo light.
There are no sharp edges anywhere on this building. Every surface curves, every
corner is rounded, every transition is smooth. The form should look like merged
soft cloud masses wrapped in translucent shell layers, with aurora-like glow
visible from inside.

Silhouette signature: floating cloud over mirror lake, with no domes, no walkways,
and no visible structural floors. It must be immediately distinct from Yoga's
domes-on-platform language and Relationships' low garden/moat pavilion language.

## Scene Preparation

1. Clear the scene completely.
2. Run `shared/lighting-rig.py` to establish the cinematic three-light setup.
3. Run `shared/material-library.py` with `#6366F1`, `include_energy=True`, `include_holo=False`.
4. Verify exactly the allowed materials are present: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`.
5. Confirm world background remains near `#0A0A0F`.

## What To Build

Build only the major silhouette elements:

- Cloud-like main form: 2-3 merged organic lobes, no hard edges.
- Indigo light pillars: 4-6 vertical emissive beams rising from lake to building.
- Mirror-still lake: flat reflective plane below, visually distinct from Yoga's lake.
- Soft translucent shell layers: two nested shell groups with visible gap/depth.
- No visible floor separations: keep the cloud surface continuous.
- Faint star-like surface lights: placeholder scale markers embedded into shell.
- Trailing wisps: 3-5 tapering tendrils extending from shell edges.
- Aurora-like interior glow: muted indigo and silver mass visible through glass.
- Energy thread reception point: barely visible orange wisp at top.
- Underside smooth concave surface: a soft shadowed belly reflected by the lake.

## Material Assignment

| Surface | Slot | Notes |
|---------|------|-------|
| Outer translucent shell | glass | Muted indigo tint, alpha feel, smooth |
| Inner translucent shell | glass | Slightly more opaque nested mass |
| Indigo light pillars | emissive | `#6366F1` at restrained intensity |
| Mirror-still lake surface | glass | Flat reflective plane |
| Star-like surface lights | emissive | Tiny muted indigo points |
| Trailing wisps | accent | Tapering indigo form, no hard pipe |
| Aurora interior glow | emissive | Muted indigo/silver glow mass |
| Energy thread terminus | energy | Minimal orange wisp only |
| Cloud form base surfaces | base | Smooth dark concave underside |
| Shell gap between layers | detail | Dark separation between nested shells |

## Workflow

1. Build the lake and dark under-shadow first so the floating relationship is clear.
2. Build 4-6 vertical indigo light pillars from lake to cloud underside.
3. Build the dark smooth underside as a concave/ellipsoid support shadow.
4. Build the outer cloud shell as overlapping organic lobes in `glass`.
5. Build the inner nested shell/glow mass set slightly smaller and higher.
6. Add a visible shell gap with dark `detail` separator geometry.
7. Add sparse star-like emissive points to show scale without becoming facade floors.
8. Add 3-5 soft tapering wisps at the edges.
9. Add the barely visible SIA energy thread reception point at the top.
10. Take front, three-quarter, and distance screenshots.
11. Save the `.blend` to `modules/09-recovery-sleep/exterior/drafts/`.
12. Write metrics JSON with per-object and category triangle counts.

## Quality Targets

- Gate 1: silhouette must read as a floating dream cloud over a mirror lake at 200px.
- Gate 1: must not resemble Yoga domes, Finance crystal, Career towers, or Relationships garden pavilion.
- Gate 2: reads as civic-scale architecture despite having no visible floor bands.
- Gate 2: includes 3+ legible sub-elements: lake, light pillars, underside, cloud shells, wisps, top energy receiver.
- Mesh count and tris stay comfortably below the 9K major-forms cap.
- All mesh materials use only the allowed slot names, with `holo` absent.

## Do Not Do

- Do not model the interior recovery pods or sleep brain.
- Do not add the final Phase 5 SIA energy pipeline.
- Do not export or promote a GLB in this session.
- Do not add sharp towers, domes, hard walkways, railings, facade grids, or visible floors.
- Do not download or import external reference models.

## End Criteria

- Draft `.blend` saved as `recovery-s37-major-forms.blend`.
- Three screenshots saved under `modules/09-recovery-sleep/screenshots/`.
- Metrics saved as `session37-metrics.json`.
- REVIEW updated with Session 37 build notes and Gates 1-2 QA.
- PROGRESS advanced to Session 38, Recovery exterior detail.
