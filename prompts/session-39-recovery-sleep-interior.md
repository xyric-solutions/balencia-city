# Session 39: Recovery & Sleep -- Floating Dreamscape -- Interior

## Quick Context

- Project: Balencia City v3, an interactive cinematic 3D city.
- Aesthetic: dark premium night architecture, Apple spatial computing clarity, UE5 archviz weight.
- Avoid: Lego proportions, neon overload, photorealism, daytime, cartoon, suburban scale.
- Sky/world: Ink-blue `#0A0A0F`; surfaces stay dark and premium.
- SIA Tower: central 100+ floor anchor, roughly 40u tall; all districts remain clearly shorter.
- Materials: runtime reads exact slot names: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Export: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center.
- Scripts: run `shared/lighting-rig.py`, then `shared/material-library.py` with the district hex.

## Session Scope

- Module: #09 Recovery & Sleep -- Floating Dreamscape.
- Position: Phase 4, Step 4.2.
- District color: Ethereal Indigo `#6366F1`.
- Focus: single interior room -- focal element, props, runtime empties, screenshots, export.
- Budget: Interior 4K-8K tris; file budget 50-180 KB.
- Energy slots: energy=true, holo=false.
- Previous session: Session 38 approved the Recovery exterior at 14,488 tris and 131,648-byte GLB.

## Room Description

The interior is a continuous flowing space with no hard walls or sharp corners.
Every surface curves gently into the next. Recovery pods line the perimeter:
translucent cocoon-shaped capsules large enough for one person, each glowing
with slow-cycling light from deep indigo to soft silver. Biometric data displays
as gentle floating symbols above each pod.

A central sleep brain hologram dominates the space. It is a large translucent
brain form showing REM, deep, and light sleep phases as flowing color waves,
not clinical display panels. It should pulse visually at a 60 BPM rhythm.
Slow particles drift through the space like suspended dream fragments.
Emotional reset nooks are carved into the curved walls, with single seats and
orbiting light points. Breathing wall sections visibly reference a 4-second
expand/contract cycle in muted indigo.

## Focal Element

The central sleep brain hologram is the hero object. It should be approximately
3m wide, translucent, and immediately recognizable as a sleep-state brain even
at low poly count. Allocate the highest detail here: paired lobes, REM/deep/light
wave bands, a heartbeat/pulse ring language, and a camera target at its center.

## Required Props

- Recovery pods: 4-6 translucent cocoon capsules along the perimeter.
- Biometric data symbols above pods: small floating geometric indicators.
- Dream particles: 15-20 tiny geometric shapes drifting through the foreground.
- Emotional reset nooks: 2 curved wall alcoves with single-seat forms.
- Orbiting light points around nooks: 3-4 small emissive spheres per nook.
- Breathing wall sections: 2 curved wall panels showing expansion/contraction.
- Floor surface: soft center-to-edge gradient using layered dark/glass/accent rings.

## Required Empties

- `light_0`: above sleep brain hologram, muted indigo key light, very low intensity.
- `light_1`: inside recovery pod cluster, warm silver fill.
- `light_2`: floor-level center, ground-up accent.
- `camera_target`: center of the sleep brain hologram at eye height, looking slightly upward.

## Material Assignment

Use only the shared Balencia slot names:

| Surface | Slot | Notes |
|---------|------|-------|
| Room shell/floor/ceiling | base | Dark, smooth, continuous |
| Floor rings and breathing pulse bands | accent | Muted indigo, restrained |
| Recovery pods and sleep brain shell | glass | Translucent indigo/silver |
| Plinths, cradles, seats, wall shadows | detail | Dark physical support geometry |
| Sleep phase lines, pod rings, particles | emissive | Soft indigo/silver glow |
| Minimal orange pulse accents | energy | Present but very subtle |

Do not create `holo`; Recovery does not opt into that slot.

## Workflow

1. Start a fresh Blender scene.
2. Run shared lighting and material setup with `#6366F1`, `include_energy=True`, `include_holo=False`.
3. Build the curved room shell: floor basin, curved back/side walls, ceiling canopy, open front.
4. Build the gradient floor rings and breathing wall sections.
5. Build the sleep brain hologram first: lobes, pulse rings, sleep phase waves, plinth.
6. Build 4-6 recovery pods around the perimeter with cocoon shells and slow-cycle rings.
7. Add biometric symbols above every pod.
8. Add 15-20 dream particles in foreground/midground/background.
9. Add 2 emotional reset nooks with seats, aura fields, and orbiting light points.
10. Add runtime empties: `light_0`, `light_1`, `light_2`, `camera_target`.
11. Render overview, entry, focal, topdown, and dark-first screenshots.
12. Export `interior/drafts/recovery-int-draft-s39.glb` with Draco level 6.
13. Import-validate the GLB: materials, tris, file size, bbox, transforms, cameras/lights, empties.
14. Promote to `interior/approved/recovery-int.glb` only after QA passes.

## Quality Gates

- Gate 3: valid material slots only; `energy` present; `holo` absent.
- Gate 4: with emissions at 0, room still reads as Recovery interior: brain, pods, nooks, walls, floor rings.
- Gate 5: 4K-8K tris, 50-180 KB GLB, bottom-centered import bbox, no cameras/lights, clean transforms.
- Gate 7: clear focal point, complete room shell, 4-8 prop categories, and exact runtime empties.

## End Criteria

- Source blend saved as `modules/09-recovery-sleep/interior/drafts/recovery-int-session39.blend`.
- Draft GLB saved as `interior/drafts/recovery-int-draft-s39.glb`.
- Approved GLB promoted to `interior/approved/recovery-int.glb`.
- Metrics saved as `interior/drafts/session39-metrics.json`.
- Import QA saved as `interior/drafts/session39-qa-import.json`.
- Screenshots saved under `modules/09-recovery-sleep/screenshots/`.
- `REVIEW.md` records Session 39 build and QA approval.
- `PROGRESS.md` advances to Recovery integration, Session 40.
