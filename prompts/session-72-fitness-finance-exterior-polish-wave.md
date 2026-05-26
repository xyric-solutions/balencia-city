# Session 72: Fitness + Finance Exterior Polish Wave

## Quick Context

- Project: Balencia City v3, an interactive cinematic 3D city.
- Phase: 8.4 City Spread And Exterior Finish.
- Current state: Session 71 approved the SIA Tower v2 pilot polish and queued Fitness + Finance.
- User feedback driver: the wider city now breathes, but several exteriors still need finished premium architecture.
- Materials: runtime reads exact slot names: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Export: GLB Draco level 6, Y-up, no cameras/lights, origin-compatible with existing app and assembly placement.
- Performance guardrail: active city remains under the 250K triangle cap.

## Session Scope

- Polish Fitness and Finance approved exterior assets only.
- Preserve district origins, app runtime paths, city-layout-v2 positions, and baked energy endpoint assumptions.
- Sync the two approved v2 GLBs into the app public model paths.
- Render module evidence screenshots and a refreshed exterior contact sheet.
- Do not rebuild layout, cameras, interiors, or energy assets in this session.

## Fitness Source And Outputs

- Source blend: `modules/01-fitness/exterior/drafts/fitness-session07.blend`
- Draft blend: `modules/01-fitness/exterior/drafts/fitness-session72-v2-polish.blend`
- Draft GLB: `modules/01-fitness/exterior/drafts/fitness-ext-v2-draft-s72.glb`
- Approved GLB: `modules/01-fitness/exterior/approved/fitness-ext.glb`
- App model path: `apps/balencia/public/models/structures/01-fitness/fitness-ext.glb`
- Metrics: `modules/01-fitness/exterior/drafts/session72-v2-metrics.json`
- QA import: `modules/01-fitness/exterior/drafts/session72-qa-import.json`

## Finance Source And Outputs

- Source blend: `modules/03-finance/exterior/drafts/finance-exterior-s14.blend`
- Draft blend: `modules/03-finance/exterior/drafts/finance-session72-v2-polish.blend`
- Draft GLB: `modules/03-finance/exterior/drafts/finance-ext-v2-draft-s72.glb`
- Approved GLB: `modules/03-finance/exterior/approved/finance-ext.glb`
- App model path: `apps/balencia/public/models/structures/03-finance/finance-ext.glb`
- Metrics: `modules/03-finance/exterior/drafts/session72-v2-metrics.json`
- QA import: `modules/03-finance/exterior/drafts/session72-qa-import.json`

## Fitness Polish Elements

- Add 30 readable green floor-edge bands so the 30-floor gym scale is explicit.
- Add large activity glass panels and dark structural reveals on all major faces.
- Add exposed corner steel, diagonal bracing, and cantilever power lips.
- Deepen the triangular entrance portal with shadow, green threshold scan, and trophy panels.
- Add ground athletic track energy lanes around the base.
- Add rooftop mechanical housings and a roof pipeline collar without moving the existing hardpoint logic.

## Finance Polish Elements

- Raise the low-density crystalline exception into the preferred 12K-18K Phase 8 range.
- Add 35 octagonal gold floor-edge rings for floor scale and financial precision.
- Add recessed plate-glass panels, gold window frames, and shadow reveals across the faceted body.
- Strengthen the wide stable base with octagonal steps, pilasters, and gold index markers.
- Add a deeper geometric entry, market ticker panel, and small ticker glyphs.
- Add crown data rings, market panels, observation deck underbracing, and roof pipeline collar.

## QA Gates

- Both GLBs import cleanly with zero invalid material slots.
- Both assets stay within 12K-18K triangles and 100-350 KB.
- No cameras or lights export.
- Dark-first screenshots still read as Fitness and Finance without relying only on emissive surfaces.
- App build passes after model sync.

## Do Not Do

- Do not alter `shared/city-layout-v2.json`.
- Do not retarget baked energy endpoints.
- Do not modify interiors.
- Do not change the 17-scene camera timeline.
- Do not invent material names outside the seven-slot system.

## End Criteria

- Session 72 build script runs in Blender.
- Fitness and Finance v2 draft/approved GLBs, metrics, QA import reports, and screenshots exist.
- App public model paths contain the approved v2 GLBs.
- Session 72 audit/report and contact sheet exist.
- `PROGRESS.md`, `BUILD-ORDER.md`, module reviews, Phase 8 backlog, and app manifest reflect Session 72.
