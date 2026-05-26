# Phase 8 City Spread And Exterior Finish Backlog

Date: 2026-05-26
Status: In progress

## Summary

Phase 8 responds to user visual review after Session 68. The app passed local QA, but the city composition read too clustered and several approved exteriors need a higher-finish pass to feel like completed premium 3D architecture.

## Completed

| Session | Work | Status |
|---------|------|--------|
| 69 | City layout v2 spread prototype | Done |
| 70 | Assembly and energy layout rebase | Done |
| 71 | Exterior finish audit plus SIA pilot polish | Done |
| 72 | Fitness + Finance exterior polish wave | Done |
| 73 | Yoga + Recovery + Relationships organic polish wave | Done |
| 74 | Knowledgebase + Chat + Career urban polish wave | Done |
| 75 | Leaderboard + AI Analytics + Nutrition signature polish wave | Done |

Session 69 added `shared/city-layout-v2.json`, retargeted app structure positions to the wider layout, expanded the island/road/atmosphere context, updated overview cameras and label layouts, hid stale baked endpoint energy GLBs, and kept app-layer living routes active from the new positions.

Session 70 rebuilt all baked endpoint energy assets and the full-city Blender assembly from `shared/city-layout-v2.json`, restored the baked energy GLBs in the app, rendered 7 overview and 17 scroll-verification frames, and approved the rebase at 176,183 active city tris with 36.4005u minimum district spacing.

Session 71 audited all 12 approved exterior GLBs against stricter Phase 8 finished-model criteria, produced the first approved v2 polish pass for SIA Tower, promoted the updated SIA exterior to the app, and rendered the SIA evidence set plus a normalized 12-structure exterior contact sheet. SIA moved from 6,956 tris / 12 objects to 14,844 tris / 357 objects and remains approved with a Phase 8 density exception.

Session 72 polished Fitness and Finance exteriors and promoted both v2 GLBs to approved/app paths. Fitness moved to 16,402 tris / 45 objects / 103.8 KB with stronger facade bands, glass, entry, track, rooftop, and hardpoint finish. Finance moved to 15,370 tris / 205 objects / 248.8 KB with stronger crystalline floor rings, recessed glass, base, entry ticker, crown data ring, observation deck, and hardpoint finish.

Session 73 polished Yoga, Recovery, and Relationships exteriors and promoted all three v2 GLBs to approved/app paths. Yoga moved to 16,052 tris / 154 objects / 247.2 KB with stronger platform lamellae, dome bands, vines, and water detail. Recovery moved to 17,412 tris / 11 objects / 147.3 KB with stronger lake ripples, contour ribbons, pillar halos, star jewels, and wisps. Relationships moved to 17,170 tris / 10 objects / 128.2 KB with stronger moat rings, terrace lips, rose canopy, bridge articulation, and roof gathering signals.

Session 74 polished Knowledgebase, Chat, and Career exteriors and promoted all three v2 GLBs to approved/app paths. Knowledgebase moved to 15,204 tris / 7 objects / 102.0 KB with stronger archive columns, vault arches, holo catalog panels, waterfall strands, and civic crown signals. Chat moved to 20,052 tris / 7 objects / 158.1 KB with stronger signal bands, outward screens, antenna crowns, bridge sleeves, status nodes, and conversation plaza tiles. Career moved to 20,288 tris / 6 objects / 113.4 KB with crisper floor joints, elevator tubes/cars, corner fins, executive deck rails, and networking plaza paths.

Session 75 polished Leaderboard, AI Analytics, and Nutrition exteriors and promoted all three v2 GLBs to approved/app paths. Leaderboard moved to 19,928 tris / 6 objects / 151.5 KB with stronger rim plinths, rank glyphs, victory crown hardware, seating rails, arch score plates, medals, and lightning receiver branchwork while preserving its no-holo exterior material set. AI Analytics moved to 19,411 tris / 7 objects / 124.4 KB with denser forecast panels, arch halos, buttress fiber bundles, observation guard detail, spire telemetry rings, and living-wall streams. Nutrition moved to 19,876 tris / 6 objects / 121.7 KB with green plant accent restored, stronger terrace planters, greenhouse mullions, vine clusters, market crates, irrigation nodes, and amber roof/grow-light finish.

## Next Sessions

| Priority | Session | Work |
|----------|---------|------|
| P0 | 76 - Final city QA | Rebuild contact sheets, compare before/after, confirm breathing room, finished exterior read, label clarity, and performance. |

## Acceptance Gates

| Gate | Scope | Pass Criteria |
|------|-------|---------------|
| Layout spread | Full city | Minimum district-center spacing stays at or above 36u, with visible breathing room in Scenes 1, 15, and 17. |
| Energy alignment | Assembly/app | No baked energy route points to old Session 56 endpoints. |
| Exterior finish | Each v2 exterior | Reads complete in dark-first view: base/body/crown, facade articulation, entrance, lighting, rooftop/crown treatment, and district-specific finish. |
| App QA | Desktop/mobile | No label overlaps, overlay collisions, offscreen labels, console warnings/errors, or blank canvas in required scenes. |
| Performance | Active city | Stay under the 250K active triangle cap unless a later audit explicitly raises the budget. |
