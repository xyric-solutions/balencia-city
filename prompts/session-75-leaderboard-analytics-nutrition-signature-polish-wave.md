# Session 75: Leaderboard + AI Analytics + Nutrition Signature Exterior Polish Wave

## Session Scope

- **Phase**: 8.7 City Spread And Exterior Finish
- **Modules**: #06 Leaderboard & Competition, #10 AI Analytics, #11 Nutrition
- **Focus**: Upgrade the remaining signature exterior GLBs to the Phase 8 finish bar
- **Preserve**: Origins, bottom-center alignment, city-layout-v2 positions, app paths, approved interior paths, and baked energy endpoint assumptions
- **Do not modify**: `shared/city-layout-v2.json`, scroll camera data, approved interiors, energy GLBs, or app scene logic

## Context

Sessions 71-74 completed SIA, Fitness, Finance, Yoga, Recovery, Relationships, Knowledgebase, Chat, and Career v2 exterior polish. The remaining signature districts are already approved and distinctive, but they need a final additive finish pass so the full city reads complete in the Phase 8 spread layout.

The three targets are close to their original 12K-18K exterior budgets, so Session 75 uses the same Phase 8 exterior-finish exception applied in the previous waves: preserve silhouette and energy assumptions while allowing a controlled 18K-20.5K finish band. Keep active city triangles under the 250K guardrail.

## Build Requirements

1. Import the current approved exterior GLBs for Leaderboard, AI Analytics, and Nutrition.
2. Normalize material slot names to the approved runtime set: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
3. Add additive Phase 8 geometry only. Avoid moving existing structure origins or changing major silhouettes.
4. Keep each export inside the Session 75 Phase 8 finish band: 18K-20.5K tris and 100-400 KB.
5. Export Draco level 6 GLBs with Y-up, no cameras/lights, and one clean root named after the approved asset.
6. Promote successful draft GLBs to both module approved paths and app public model paths.
7. Render front, three-quarter, and dark-first evidence screenshots for each module.
8. Render a 12-structure exterior finish contact sheet.
9. Run `npm run build` in `apps/balencia`.
10. Verify local app/model serving for the promoted GLBs.

## Design Targets

- **Leaderboard & Competition**: Preserve the open-top arena silhouette while adding rim winner plinths, rank glyphs, victory-pillar crown hardware, seating rail detail, arch plates, competitor lane medals, and stronger lightning receiver branchwork.
- **AI Analytics**: Preserve the data-cathedral massing while adding animated-looking forecast glyph fields, arch halos, buttress fiber bundles, observation guard detail, spire telemetry rings, and denser living-wall chart articulation.
- **Nutrition**: Preserve the stepped vertical-farm pyramid while adding terrace planter detail, greenhouse mullion depth, hanging vine/leaf clusters, market produce polish, irrigation droplet hardware, and warmer roof vent finish.

## Acceptance Criteria

- All three GLBs reimport cleanly.
- No invalid material slots appear.
- No cameras or lights are exported.
- Each promoted GLB has one root named after the approved asset.
- BBox min Z remains at 0.0 or within tolerance.
- Approved/app GLB paths are updated.
- Evidence screenshots and audit reports are written.
- `PROGRESS.md`, `BUILD-ORDER.md`, module `REVIEW.md` files, `apps/balencia/PHASE-8-BACKLOG.md`, and `apps/balencia/SESSION-75-REPORT.md` are updated after QA passes.
