# Session 74: Knowledgebase + Chat + Career Urban Exterior Polish Wave

## Session Scope

- **Phase**: 8.6 City Spread And Exterior Finish
- **Modules**: #04 Knowledgebase, #05 Chat & Communication, #08 Career
- **Focus**: Upgrade already-approved urban/civic exterior GLBs to the Phase 8 finish bar
- **Preserve**: Origins, bottom-center alignment, city-layout-v2 positions, app paths, approved interior paths, and baked energy endpoint assumptions
- **Do not modify**: `shared/city-layout-v2.json`, scroll camera data, approved interiors, energy GLBs, or app scene logic

## Context

The city layout v2 spread is approved, and Sessions 72 and 73 completed the first five Phase 8 exterior polish waves after SIA. The next visual cluster is the urban/civic group: Knowledgebase, Chat, and Career. They are approved and integrated, but need a final surface/detail pass so they read as completed premium 3D architecture in the app.

## Build Requirements

1. Import the current approved exterior GLBs for Knowledgebase, Chat, and Career.
2. Normalize material slot names to the approved runtime set: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
3. Add additive Phase 8 geometry only. Avoid moving existing structure origins or changing major silhouettes.
4. Keep all exports inside Phase 8 exterior budget: target 15K-20.5K tris and 100-400 KB for this already-dense urban group.
5. Export Draco level 6 GLBs with Y-up, no cameras/lights, and one clean root named after the approved asset.
6. Promote successful draft GLBs to both module approved paths and app public model paths.
7. Render front, three-quarter, and dark-first evidence screenshots for each module.
8. Render a 12-structure exterior finish contact sheet.
9. Run `npm run build` in `apps/balencia`.
10. Verify local app/model serving for the promoted GLBs.

## Design Targets

- **Knowledgebase**: Add stronger classical column sleeves/fluting, recessed archive arches, vault steps, holo catalog panels, data-waterfall strands, reservoir basin, and crown beacon detail.
- **Chat & Communication**: Add live floor signal bands, outward holo screens, antenna crowns, bridge sleeves, inner signal threads, bridge status nodes, and plaza conversation tiles.
- **Career**: Add crisper blue floor joints, upward corner fins, visible elevator tubes/cars, executive observation deck rails, and networking plaza paths.

## Acceptance Criteria

- All three GLBs reimport cleanly.
- No invalid material slots appear.
- No cameras or lights are exported.
- Each promoted GLB has exactly one root named after the approved asset.
- BBox min Z remains at 0.0 or within tolerance.
- Approved/app GLB paths are updated.
- Evidence screenshots and audit reports are written.
- `PROGRESS.md`, `BUILD-ORDER.md`, module `REVIEW.md` files, and `apps/balencia/SESSION-74-REPORT.md` are updated.
