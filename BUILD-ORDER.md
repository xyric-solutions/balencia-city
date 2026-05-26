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
| 8.8 | Final Phase 8 city QA contact sheets and performance review | Next |

## Per-Module Workflow (applies to every structure)
```
Exterior → Exterior Review (all 7 gates) → Interior → Interior Review → Integration Test
```
No step can be skipped. Failure at any gate → fix → re-run ALL gates.
