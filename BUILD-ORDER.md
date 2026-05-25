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
| 7.3 | Energy pipeline shader system (flowing particles) |
| 7.4 | AI Pulse expanding ring (8-sec cycle) |
| 7.5 | Cross-district gold connections |
| 7.6 | Overlay system (text, labels, insight cards) |
| 7.7 | Performance optimization (LOD, progressive loading) |
| 7.8 | Full end-to-end scroll test |

## Per-Module Workflow (applies to every structure)
```
Exterior → Exterior Review (all 7 gates) → Interior → Interior Review → Integration Test
```
No step can be skipped. Failure at any gate → fix → re-run ALL gates.
