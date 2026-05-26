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

Session 69 added `shared/city-layout-v2.json`, retargeted app structure positions to the wider layout, expanded the island/road/atmosphere context, updated overview cameras and label layouts, hid stale baked endpoint energy GLBs, and kept app-layer living routes active from the new positions.

Session 70 rebuilt all baked endpoint energy assets and the full-city Blender assembly from `shared/city-layout-v2.json`, restored the baked energy GLBs in the app, rendered 7 overview and 17 scroll-verification frames, and approved the rebase at 176,183 active city tris with 36.4005u minimum district spacing.

Session 71 audited all 12 approved exterior GLBs against stricter Phase 8 finished-model criteria, produced the first approved v2 polish pass for SIA Tower, promoted the updated SIA exterior to the app, and rendered the SIA evidence set plus a normalized 12-structure exterior contact sheet. SIA moved from 6,956 tris / 12 objects to 14,844 tris / 357 objects and remains approved with a Phase 8 density exception.

Session 72 polished Fitness and Finance exteriors and promoted both v2 GLBs to approved/app paths. Fitness moved to 16,402 tris / 45 objects / 103.8 KB with stronger facade bands, glass, entry, track, rooftop, and hardpoint finish. Finance moved to 15,370 tris / 205 objects / 248.8 KB with stronger crystalline floor rings, recessed glass, base, entry ticker, crown data ring, observation deck, and hardpoint finish.

## Next Sessions

| Priority | Session | Work |
|----------|---------|------|
| P1 | 73 - Yoga + Recovery + Relationships polish wave | Improve dome/glass/water/garden/mist finishing so organic districts feel deliberate and complete. |
| P1 | 74 - Knowledgebase + Chat + Career polish wave | Strengthen facade density, windows, bridges, crowns, signage, and occupied-city details. |
| P1 | 75 - Leaderboard + Analytics + Nutrition polish wave | Bring arena, data cathedral, and vertical farm closer to the inspiration quality with distinctive exterior finishing. |
| P0 | 76 - Final city QA | Rebuild contact sheets, compare before/after, confirm breathing room, finished exterior read, label clarity, and performance. |

## Acceptance Gates

| Gate | Scope | Pass Criteria |
|------|-------|---------------|
| Layout spread | Full city | Minimum district-center spacing stays at or above 36u, with visible breathing room in Scenes 1, 15, and 17. |
| Energy alignment | Assembly/app | No baked energy route points to old Session 56 endpoints. |
| Exterior finish | Each v2 exterior | Reads complete in dark-first view: base/body/crown, facade articulation, entrance, lighting, rooftop/crown treatment, and district-specific finish. |
| App QA | Desktop/mobile | No label overlaps, overlay collisions, offscreen labels, console warnings/errors, or blank canvas in required scenes. |
| Performance | Active city | Stay under the 250K active triangle cap unless a later audit explicitly raises the budget. |
