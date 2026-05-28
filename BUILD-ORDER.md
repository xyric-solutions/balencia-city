# Balencia City v3 — Build Order

Strict sequential build. ONE module at a time. No skipping. No parallel building.

## Phase 1: SIA Tower (The Anchor)
**Why first**: Hero structure. 100+ floors. Appears in Scenes 1, 2, 3. Every pipeline originates here. If SIA Tower isn't excellent, nothing else matters.

| Step | Task | Session Type |
|------|------|-------------|
| 1.1 | SIA Tower exterior | Exterior |
| 1.2 | SIA Tower interior (Neural Core Atrium) | Interior |
| 1.3 | Integration test (place in scene, verify scale) | Integration |

## Phase 2: First 3 Districts (Establish Range)
**Why these**: Three maximally different architectural languages. Builds the full modeling palette.

| Step | District | Architecture | Why This Order |
|------|----------|-------------|---------------|
| 2.1 | Fitness (#01) | Angular gym megastructure | Tests hard geometry, aggressive forms |
| 2.2 | Yoga & Wellbeing (#02) | Floating organic sanctuary | Tests soft curves, organic forms |
| 2.3 | Finance (#03) | Crystalline faceted tower | Tests premium precision, faceted geometry |

## Phase 3: Middle 4 Districts (Technical Challenges)
**Why this order**: Most technically demanding structures.

| Step | District | Architecture | Why This Order |
|------|----------|-------------|---------------|
| 3.1 | Knowledgebase (#04) | Ancient-meets-future library | Material gradient: stone base → floating tech top |
| 3.2 | Chat & Communication (#05) | Multi-tower connected hub | Multi-structure composition + sky-bridges |
| 3.3 | Leaderboard (#06) | Arena colosseum | Amphitheater geometry, open-top structure |
| 3.4 | Career (#08) | Tower cluster | Multi-tower + elevator tubes + sky-bridges |

## Phase 4: Final 4 Districts (Refined Execution)
**Why last**: Benefits from accumulated experience. These require either restraint or complexity.

| Step | District | Architecture | Why This Order |
|------|----------|-------------|---------------|
| 4.1 | Relationships (#07) | Low garden ecosystem | Quality from restraint — the anti-tower |
| 4.2 | Recovery & Sleep (#09) | Floating cloud dreamscape | Most ethereal, no sharp edges, delicate |
| 4.3 | AI Analytics (#10) | Data cathedral | Facade IS data — most visually complex |
| 4.4 | Nutrition (#11) | Organic farm-structure | Bridges organic and architectural |

## Phase 5: Energy System
**After all structures**: Pipelines need accurate endpoint positions from approved structures.

| Step | Asset | Description |
|------|-------|-------------|
| 5.1 | Hard pipelines (x8) | Visible tubes: Fitness, Career, Finance, Communication, Leaderboard, Knowledgebase, Analytics, Nutrition |
| 5.2 | Warm mist (x2) | Particle cloud: Yoga/Wellbeing, Relationships |
| 5.3 | Faint thread (x1) | Nearly invisible: Recovery/Sleep |
| 5.4 | Special: Waterfall | Knowledgebase — energy cascades downward |
| 5.5 | Special: Lightning bolt | Leaderboard — dramatic burst at apex |
| 5.6 | Cross-district gold (x6+) | Golden #F59E0B lines between districts |
| 5.7 | AI Pulse ring | Expanding orange ring, 8-second cycle |

## Phase 6: Assembly
| Step | Task |
|------|------|
| 6.1 | Place all 12 structures in Blender orbital layout |
| 6.2 | Verify scale/spacing, skyline elevation |
| 6.3 | Add all pipelines and connections |
| 6.4 | Screenshot at each of 17 scroll scene camera positions |
| 6.5 | Color balance check: 60% orange, 30% green, 10% purple |
| 6.6 | Performance audit: total tris, total file size |

## Phase 7: App Integration
| Step | Task |
|------|------|
| 7.1 | Scaffold Vite + R3F project |
| 7.2 | Build 17-scene scroll timeline (GSAP + Lenis) |
| 7.3 | City legibility pass: Urban Atlas ground, district pads, boulevards, hybrid labels |
| 7.4 | Energy pipeline shader system (flowing particles) |
| 7.5 | AI Pulse expanding ring (8-sec cycle) |
| 7.6 | Cross-district gold connections |
| 7.7 | Overlay system (text, labels, insight cards) |
| 7.8 | Performance optimization (LOD, progressive loading) |
| 7.9 | Full end-to-end scroll test |

### Phase 7.3 Visual Quality Sub-Passes

| Step | Task | Status |
|------|------|--------|
| 7.3A | Label legibility: full-name labels, curated overview placement, mobile dock | Done |
| 7.3B | Feedback audit and backlog reset: compare actual app state to user feedback, record missing quality, and reset next-session order | Done |
| 7.3C | Immersive city structure/depth: stronger walls, retaining edges, district boundaries, zoning colors, foreground/background separation, SIA hierarchy | Done |
| 7.3D | Label boards and reveal system: illuminated building-tethered boards, hover/focus reveal, mobile spacing logic, reduced detached-label feeling | Done |
| 7.3E | Living intelligence motion: subtle camera parallax, animated data-flow lines, status-based glow variation, richer particles/fog/holographic scans | Done |
| 7.3F | Interaction overlay: hover pulse, keyboard focus, focus zoom, district preview cards/tooltips, dynamic bottom-left info panel | Done |
| 7.3G | Void and horizon: distant edge, warm fog, terrain/sky gradient, outer rim lighting, Scene 17 cleanup | Done |
| 7.3H | Product reality overlay: Scene 16 person/phone Today Screen overlay with city visible behind it | Done |
| 7.3I | Integration QA: desktop/mobile label checks, interaction checks, console, build, performance budget, screenshots if capture timeout is resolved | Done |

### Phase 7.3 Interface Backlog

| Interface | Purpose | Status |
|-----------|---------|--------|
| Shared district metadata | Labels, zones, activity/status, board anchors, preview copy, and interaction affordances in one source instead of buried scene component constants | Done |
| Interaction store state | Track hovered/focused district and active preview content alongside scroll scene state | Done |
| `DistrictLabelBoard` | App-layer illuminated/tethered labels for active and hovered districts | Done |
| `BuildingInteractionLayer` | Pointer and keyboard interaction targets without modifying approved GLBs first | Done |
| `DistrictPreviewPanel` | Dynamic replacement behavior for the bottom-left info panel when a building is hovered or focused | Done |
| `LivingEnergyLayer` | Shader/animation layer for flowing pipelines, data pulses, and status glow variation | Done |
| `AtmosphereDepthLayer` | App-layer sky gradient, terrain depth, horizon fog, distant edge cues, outer rim lighting, and closing cleanup | Done |

## Phase 8: City Spread And Exterior Finish

| Step | Task | Status |
|------|------|--------|
| 8.1 | City layout v2 spread prototype: shared layout source, wider app positions, expanded island/rings, retargeted cameras/labels, stale baked energy hidden | Done (Session 69) |
| 8.2 | Assembly and energy layout rebase: rebuild full-city Blender assembly and all endpoint energy GLBs from `shared/city-layout-v2.json` | Done (Session 70) |
| 8.3 | Exterior finish audit plus SIA pilot polish | Done (Session 71) |
| 8.4 | Fitness + Finance exterior polish wave | Done (Session 72) |
| 8.5 | Yoga + Recovery + Relationships organic polish wave | Done (Session 73) |
| 8.6 | Knowledgebase + Chat + Career urban polish wave | Done (Session 74) |
| 8.7 | Leaderboard + Analytics + Nutrition signature polish wave | Done (Session 75) |
| 8.8 | Final Phase 8 city QA contact sheets and performance review | Done (Session 76) |

## Phase 9: App Experience Repair

Source audit: `BALENCIA-CURRENT-AUDIT.md`. Run these sessions sequentially. Start with app-layer interaction, camera, label, flow, and QA harness work before considering any new model work.

| Step | Session | Task | Priority | Status |
|------|---------|------|----------|--------|
| 9.1 | 77 | P0 Interaction Truth Pass: add missing district interaction targets, gate targets by overview/active scene relevance, align hit areas, and prove Knowledgebase never shows Finance copy | P0 | Done |
| 9.2 | 78 | P0 SIA Interior Rewrite: make Scene 3 read as entering SIA Tower with clear atrium, neural core, city model, walls/platforms, and midpoint interior read | P0 | Done |
| 9.3 | 79 | Label Anchoring And Naming Pass: attach labels to model anchors where practical and standardize naming across labels, panels, nav, and overlays | P1 | Done |
| 9.4 | 80 | Interior Reveal Pass, Scenes 4-8: tune Fitness, Yoga, Finance, Knowledgebase, and Chat exterior-to-interior starts, thresholds, and midpoints | P1 | Done |
| 9.5 | 81 | Interior Reveal Pass, Scenes 9-14: tune Leaderboard, Relationships, Career, Recovery, Analytics, and Nutrition exterior-to-interior starts, thresholds, and midpoints | P1 | Done |
| 9.6 | 82 | Full Journey Flow Pass: smooth the complete 17-scene scroll, especially SIA to Fitness, Analytics to Nutrition, Climax to Product, and Product to Closing | P1 | Done |
| 9.7 | 83 | QA Evidence Harness: restore stable DOM, canvas, console, and visual capture evidence for heavy WebGL scenes | P1/P2 | Done |
| 9.8 | 84 | Final Demo Readiness Audit: re-score the repaired app, require 12 / 12 interaction coverage, 0 console warnings/errors, no P0s, and target overall score at or above 8.0 / 10 | P1/P2 | Done |

## Phase 10: Architectural Completion And Facade LOD

Source backlog: `apps/balencia/PHASE-10-BACKLOG.md`. Run after the Phase 9 final demo readiness audit. Preserve the current overview exteriors as LODs and introduce richer focused-scene hero exteriors only where the completion gate requires them.

| Step | Session | Task | Priority | Status |
|------|---------|------|----------|--------|
| 10.1 | 85 | Completion Audit: capture baseline front, 3/4, ground-up, dark-first, and app hero-camera evidence for all 12 exteriors; score construction-read risk explicitly | P1 | Done |
| 10.2 | 86 | Pilot Wave: Finance, SIA Tower, and Knowledgebase architectural completion hero exteriors | P1 | Done |
| 10.3 | 87 | Urban/Vertical Wave: Fitness, Chat, Career, and AI Analytics facade/base/crown completion | P1 | Done |
| 10.4 | 88 | Organic/Signature Wave: Yoga, Recovery, Relationships, Leaderboard, and Nutrition completion without over-busying silhouettes | P1 | Done |
| 10.5 | 89 | Final Phase 10 QA: before/after contact sheets, scroll hero views, GLB QA, LOD loading, and performance review | P1/P2 | Next |

## Per-Module Workflow (applies to every structure)
```
Exterior → Exterior Review (all applicable exterior gates) → Interior → Interior Review → Integration Test
```
No step can be skipped. Failure at any gate → fix → re-run ALL gates.
