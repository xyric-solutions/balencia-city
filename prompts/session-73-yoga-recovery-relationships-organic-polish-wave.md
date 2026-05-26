# Session 73: Yoga + Recovery + Relationships Organic Exterior Polish Wave

## Session Scope

- **Phase**: 8.5 City Spread And Exterior Finish
- **Modules**: #02 Yoga & Wellbeing, #09 Recovery & Sleep, #07 Relationships
- **Focus**: Upgrade already-approved organic exterior GLBs to the Phase 8 finish bar
- **Preserve**: Origins, bottom-center alignment, city-layout-v2 positions, app paths, approved interior paths, and baked energy endpoint assumptions
- **Do not modify**: `shared/city-layout-v2.json`, scroll camera data, approved interiors, energy GLBs, or app scene logic

## Context

The city layout v2 spread is approved, and Session 72 completed Fitness + Finance v2 exterior polish. The next weak visual cluster is the organic group: Yoga, Recovery, and Relationships. They are approved and distinctive, but need a final surface/detail pass so they read as deliberately finished beside SIA, Fitness, and Finance in the app.

## Build Requirements

1. Import the current approved exterior GLBs for Yoga, Recovery, and Relationships.
2. Normalize material slot names to the approved runtime set: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
3. Add additive Phase 8 geometry only. Avoid moving existing structure origins or changing major silhouettes.
4. Keep all exports inside Phase 8 exterior budget: 12K-18K tris and 80-350 KB unless an existing approved exception is explicitly documented.
5. Export Draco level 6 GLBs with Y-up, no cameras/lights, and one root named after the approved asset.
6. Promote successful draft GLBs to both module approved paths and app public model paths.
7. Render front, three-quarter, and dark-first evidence screenshots for each module.
8. Render a 12-structure exterior finish contact sheet.
9. Run `npm run build` in `apps/balencia`.
10. Verify local app/model serving for the promoted GLBs.

## Design Targets

- **Yoga**: Add layered platform lamellae, underside ribs, dome leaf skirts, holo breath bands, soft dome meridians, hanging vines, leaf clusters, and lake stepping stones.
- **Recovery**: Add lake sleep ripples, dark shadow shelves, soft-shell contour ribbons, pillar halos/sleeves, muted star jewels, and dissolving edge wisps.
- **Relationships**: Add moat reflection rings, garden terrace lips, rose canopy buds, dark leaf fans, bridge rail articulation, threshold glows, roof dome frames, and warm gathering cores.

## Acceptance Criteria

- All three GLBs reimport cleanly.
- No invalid material slots appear.
- No cameras or lights are exported.
- BBox min Z remains at 0.0 or within tolerance.
- Approved/app GLB paths are updated.
- Evidence screenshots and audit reports are written.
- `PROGRESS.md`, `BUILD-ORDER.md`, module `REVIEW.md` files, and `apps/balencia/SESSION-73-REPORT.md` are updated.
