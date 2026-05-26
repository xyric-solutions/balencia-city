# Session 71: Exterior Finish Audit + SIA Pilot Polish

## Quick Context

- Project: Balencia City v3, an interactive cinematic 3D city.
- Phase: 8.3 City Spread And Exterior Finish.
- Current state: Session 70 approved the layout-v2 assembly and energy rebase.
- User feedback driver: the spread is better, but some exteriors still read unfinished.
- Materials: runtime reads exact slot names: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Export: GLB Draco level 6, Y-up, no cameras/lights, origin at bottom-centered city coordinates.
- Performance guardrail: active city must remain under 250K tris.

## Session Scope

- Audit all 12 approved exterior GLBs against stricter Phase 8 finish signals.
- Produce the first v2 exterior polish pass for SIA Tower.
- Preserve SIA layout origin, crown/pipeline endpoint alignment, app paths, and city-layout-v2 positions.
- Sync the approved SIA v2 GLB into the app model path.
- Render SIA evidence screenshots and a city exterior contact sheet.

## SIA Source And Outputs

- Source blend: `modules/00-sia-tower/exterior/drafts/sia-tower-session03-polish-export.blend`
- Draft blend: `modules/00-sia-tower/exterior/drafts/sia-tower-session71-v2-polish.blend`
- Draft GLB: `modules/00-sia-tower/exterior/drafts/sia-tower-ext-v2-draft-s71.glb`
- Approved GLB: `modules/00-sia-tower/exterior/approved/sia-tower-ext.glb`
- App model path: `apps/balencia/public/models/structures/00-sia-tower/sia-tower-ext.glb`
- Metrics: `modules/00-sia-tower/exterior/drafts/session71-v2-metrics.json`
- QA import: `modules/00-sia-tower/exterior/drafts/session71-qa-import.json`
- Audit report: `assembly/audit/session-71-exterior-finish-audit.md`

## Audit Criteria

- Base/body/crown are readable in dark-first mode.
- Facades have real articulation, not only flat slabs or broad planes.
- Entrances, rooftops/crowns, and ground/base treatments feel deliberate.
- Materials use only the seven runtime slots.
- File size and triangle density are appropriate for the structure's visual role.
- SIA remains the dominant central hero and all district polish stays queued.

## SIA Polish Elements

- Add facade mullions and 100-floor scale ticks on all four faces.
- Add restrained warm window markers that read from Scene 2 and Scene 15.
- Add civic base buttresses, entrance side towers, canopy, threshold glow, and deep entry shadow.
- Add ground/plaza energy spokes and a cleaner outer energy collar.
- Add crown precision rings, crystalline ribs, beacon intensity rings, and spire tip polish.
- Add 11 pipeline socket clamps and orange departure cores while preserving endpoint alignment.
- Add skyline scale fins so SIA reads in dark-first view without relying only on emissive orange.

## QA Gates

- SIA v2 GLB imports cleanly with zero invalid material slots.
- SIA v2 stays under 30K triangles and 500 KB.
- No cameras or lights are exported in the GLB.
- Root/origin remains compatible with existing app and assembly placement.
- Dark-first screenshot still reads as SIA Tower.
- App build passes after the source model is updated.

## Do Not Do

- Do not alter `shared/city-layout-v2.json`.
- Do not rebuild or retarget baked energy endpoints.
- Do not polish Fitness/Finance or later districts in this session.
- Do not change the 17-scene camera timeline unless QA exposes a SIA-specific issue.
- Do not invent new material names outside the seven-slot system.

## End Criteria

- Session 71 build script exists and runs in Blender.
- Audit JSON/Markdown exists for all exterior assets.
- SIA v2 draft/approved GLB, metrics, QA import report, and screenshots exist.
- App asset manifest session advances to 71 and build passes.
- `PROGRESS.md`, SIA `REVIEW.md`, Phase 8 backlog, and Session 71 report reflect the completed work.
