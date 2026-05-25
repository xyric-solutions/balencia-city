# Session 41: AI Analytics - Data Cathedral - Exterior Major Forms

## Quick Context

- Project: Balencia City v3, an interactive cinematic 3D city.
- Aesthetic: dark premium night architecture, Apple spatial computing clarity, UE5 archviz weight.
- Avoid: toy proportions, neon overload, daytime, cartoon, suburban scale.
- Sky/world: Ink-blue `#0A0A0F`; surfaces stay dark and premium.
- SIA Tower: central 100+ floor anchor, roughly 40u tall; all districts remain clearly shorter.
- Materials: runtime reads exact slot names: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Export later: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center.
- This session saves a draft `.blend`; export waits for the detail session.

## Session Scope

- Module: #10 AI Analytics - Data Cathedral.
- Position: Phase 4, Step 4.3.
- District color: Teal `#14B8A6`.
- Floors: 30.
- Focus: Primary silhouette geometry and major architectural forms only.
- Budget: Under 60% of Exterior 12K-18K tris; target below 10.8K tris.
- Energy slots: energy=true, holo=true because the module SPEC assigns stained-glass data windows to `holo`.
- This session: exterior major forms. Next session: detail, polish, dark-first proof, export.

## Architectural Identity

The Data Cathedral is tall, pointed, and cathedral-like, but its facade is alive with data.
Its walls should read as dark architectural surfaces overlaid with teal dashboard flows,
large pointed-arch data windows, and vertical data-waterfall light at the entrance.

Silhouette signature:

- A central cathedral body with a tall pointed roofline and spire.
- Flying buttress data conduits reaching to ground anchors on both sides.
- Large pointed-arch holographic data windows.
- Vertical teal data-waterfall entrance strips.
- Observation platforms on the buttress arms.
- A teal beacon at the spire apex and a separate orange SIA hard-pipeline socket.

It must not resemble Career's clean tower cluster, Knowledgebase's library stacks,
Finance's faceted crystal, or Chat's signal-pod composition.

## Scene Preparation

1. Clear the Blender scene completely.
2. Run `shared/lighting-rig.py` to establish the cinematic three-light setup.
3. Run `shared/material-library.py` with `#14B8A6`, `include_energy=True`, `include_holo=True`.
4. Verify exactly the allowed materials are present: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
5. Confirm world background remains near `#0A0A0F`.

## What To Build

Build only the major silhouette elements:

- Cathedral-style main structure: 30-floor central nave/body, tall and pointed.
- Side aisle masses: lower flanking volumes that make the building read as a cathedral, not a single tower.
- Central spire/pinnacle with teal data beacon at the apex.
- Flying buttress data conduits: 4-6 structural arcs extending outward from body to ground anchors.
- Buttress base anchors at ground level.
- Stained-glass-style data windows: 6-8 large pointed-arch `holo` panels.
- Facade data displays: broad teal chart/dashboard overlays and floor-scale bands.
- Teal LED data streams: vertical flowing paths on the exterior walls.
- Data-waterfall entrance framing: two vertical teal cascades flanking the doorway.
- Observation platforms on buttresses.
- Energy pipeline terminus: orange hard socket only; no final Phase 5 pipeline.

## Material Assignment

| Surface | Slot | Notes |
|---------|------|-------|
| Cathedral main walls | base | Dark structural surface |
| Side aisle and foundation masses | base | Keep inactive tone dark |
| Facade data display overlays | emissive | Teal charts and dashboard panels |
| Teal data streams | emissive | Use restrained teal during major forms; detail session may rebalance slot usage |
| Flying buttress conduits | detail | Dark structural arcs with teal edge glow |
| Stained glass data windows | holo | Translucent teal pointed-arch panels |
| Spire/pinnacle structure | detail | Dark metal pointed crown |
| Data beacon at apex | emissive | Teal pulse marker |
| Data-waterfall entrance | emissive | Vertical teal cascades |
| Energy pipeline terminus | energy | Orange hard-pipeline receiver only |

## Build Workflow

1. Build the foundation, central cathedral body, side aisles, and pointed roof first.
2. Add 30-floor scale bands so the body reads as a metropolitan data tower.
3. Add the central spire and teal beacon.
4. Add left and right flying buttress arcs with ground anchor blocks.
5. Add observation platforms attached to selected buttress arms.
6. Add pointed-arch holographic data windows on front and side facades.
7. Add broad facade dashboard panels and restrained teal data-flow strips.
8. Add the data-waterfall entrance frame.
9. Add the orange SIA hard-pipeline receiver socket without extending a pipeline.
10. Take front, three-quarter, and distance screenshots.
11. Save the `.blend` to `modules/10-ai-analytics/exterior/drafts/`.
12. Write metrics JSON with per-object and category triangle counts.

## QA Gates For This Session

Gate 1 - Silhouette Clarity:

- Reads as a data cathedral at 200px.
- Unique among all approved structures: not a tower cluster, arena, cloud, garden, crystal, or signal hub.
- SIA Tower remains unmistakably taller.
- The crown/spire and buttresses are clear.

Gate 2 - Architectural Scale:

- Reads as a 30-floor metropolitan megastructure.
- Floor indicators, data bands, and tall vertical massing are visible.
- At least three sub-elements are visible: foundation/body, roof/spire, buttresses, arch windows, entrance waterfall, data panels.
- Primary volumes are articulated before detail approval.

## What Not To Do

- Do not build the Data Sanctum interior.
- Do not export GLB or promote any approved asset in this session.
- Do not add the final SIA pipeline.
- Do not download or import reference models.
- Do not over-detail tiny charts; preserve budget for Session 42.

## End Criteria

- Draft `.blend` saved as `analytics-s41-major-forms.blend`.
- Three screenshots saved under `modules/10-ai-analytics/screenshots/`.
- Metrics saved as `session41-metrics.json`.
- REVIEW updated with Session 41 build notes and Gates 1-2 QA.
- PROGRESS advanced to Session 42, AI Analytics exterior detail, only after QA approval.
