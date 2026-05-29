# Phase 10 Architectural Completion And Facade LOD Backlog

Date: 2026-05-27
Status: Complete; Sessions 85-89 approved

## Summary

Phase 10 upgrades the 12 approved exteriors from readable landmark concepts into stylized-premium finished architectural models. The target is not realism for its own sake; the target is architectural completion: finished facade envelopes, solid bases, resolved crowns, believable floor rhythm, integrated exoskeletons, and less visible construction-frame read.

Primary approval comes from the actual scroll hero cameras. Standalone contact sheets remain required as evidence, but hidden orbit-view detail should not drive the work at the expense of the app journey.

## Runtime LOD Policy

- Current approved exteriors remain the overview LOD for Scenes 1, 15, and 17.
- Focused structure scenes use `exteriorHero` when it exists on a structure manifest entry, and fall back to `exterior` when it does not.
- Hero exteriors are loaded on demand for the focused district instead of being included in the eager overview preload list.
- Scene 16 remains product/street context unless a later audit proves it needs a district hero exterior.
- Overview active city should stay at or below 250K drawn tris; focused hero scenes may reach 270K drawn tris with one richer exterior loaded.

Example manifest shape for a future hero exterior:

```json
"exteriorHero": {
  "name": "finance-ext-hero",
  "sourcePath": "modules/03-finance/exterior/approved/finance-ext-hero.glb",
  "publicPath": "models/structures/03-finance/finance-ext-hero.glb",
  "runtimePath": "/models/structures/03-finance/finance-ext-hero.glb"
}
```

## Sessions

| Step | Session | Name | Goal | Acceptance |
|---|---:|---|---|---|
| 10.1 | 85 | Completion Audit | Capture baseline front, 3/4, ground-up, dark-first, and app hero-camera evidence for all 12 exteriors. | Done - each structure has construction-read score, target notes, and before evidence; 0 hero exteriors built. |
| 10.2 | 86 | Pilot Wave: Finance, SIA, Knowledgebase | Prove the new quality bar on the most scaffold-like or central models. | Done - Finance, SIA Tower, and Knowledgebase hero exteriors pass Gate 8, LOD fallback, app hero evidence, GLB QA, runtime asset loading, and performance gates. |
| 10.3 | 87 | Urban/Vertical Wave | Upgrade Fitness, Chat, Career, and AI Analytics facade systems. | Done - Fitness, Chat, Career, and AI Analytics hero exteriors pass Gate 8, GLB QA, app hero evidence, LOD loading, and performance gates. |
| 10.4 | 88 | Organic/Signature Wave | Upgrade Yoga, Recovery, Relationships, Leaderboard, and Nutrition without over-busying silhouettes. | Done - Yoga, Recovery, Relationships, Leaderboard, and Nutrition hero exteriors pass Gate 8, GLB QA, app hero evidence, LOD loading, and performance gates. |
| 10.5 | 89 | Final Phase 10 QA | Rebuild evidence, verify LOD loading, and score the completed city. | Done - final score 9.6 / 10, overview city remains 225,847 tris, max focused hero scene is 243,219 / 270,000 tris, 12 / 12 hero and overview GLBs pass runtime reachability, and 0 scaffold/unfinished-read blockers remain. |

## Completion Standard

- Facade: layered glass/metal/panel systems behind any exoskeleton or energy frame.
- Base: complete plinth, entry threshold, civic edge, and district-specific ground connection.
- Crown: resolved roofline, cap, equipment, beacon, canopy, or signature terminal detail.
- Scale: repeated floor, deck, mullion, terrace, or ledge cues visible in the app hero camera.
- Materials: only the 7 approved slots; no new material taxonomy for Phase 10.
- Evidence: front, 3/4, ground-up, dark-first, app hero-camera before/after, and contact-sheet comparison.

## Explicit Non-Goals

- Do not rewrite interiors except for visible exterior threshold/entrance geometry needed for completion.
- Do not move district origins, layout positions, or baked energy endpoints.
- Do not replace the Balencia stylized identity with generic archviz realism.
