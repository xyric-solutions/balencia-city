---
type: master-context
title: Balencia City v3 — Master Context
status: Active
project: balencia-city-v3
owner: hamza
last_updated: 2026-05-22
kb_summary: Single source of truth for the Balencia City v3 cinematic 3D city project.
---

# Balencia City v3 — Master Context

> Load this document at the start of every modeling session.
> It is the single source of truth for vision, structures, materials, constraints, and build sequence.

---

<!-- section:quick-context -->
## Quick Context (For Build Agents)

- **Project**: Balencia City v3 — interactive cinematic 3D city (NOT a website)
- **Aesthetic**: Blade Runner 2049 warmth + Apple spatial computing + UE5 archviz. Dark, premium, night.
- **Avoid**: Lego proportions, neon overload, photorealism, daytime, cartoon, suburban scale
- **Sky**: Ink-blue #0A0A0F. Surfaces: #1E1E28 (never pure black). Fog: warm amber
- **Brand**: 60% Burnt Orange #FF5E00, 30% Forest Green #34A853, 10% Royal Purple #7F24FF
- **SIA Tower**: 100+ floors, ~40u tall, absolute center. Every district < 2.5x shorter
- **Materials**: 7-slot system (base, accent, glass, detail, emissive, energy, holo). Slot name = runtime override key
- **Export**: GLB Draco level 6, Y-up, no cameras/lights, origin bottom-center, per-object decimation only
- **Scripts**: Run lighting-rig.py first, then material-library.py with district hex

---

<!-- section:vision -->
## 1. Vision and Aesthetic Identity

Balencia City v3 is **not** a website, dashboard, or UI prototype. It is an **interactive cinematic world** — a premium 3D city visualization representing the SIA Life Coach platform. Users scroll through a 17-scene journey that demonstrates how AI connects every dimension of human life.

**Central message**: "Every dimension of human life becomes stronger when powered by intelligent AI."

### Inspiration Pillars

| Draw From | Avoid |
|-----------|-------|
| Blade Runner 2049 warmth (amber fog, volumetric shafts) | Lego or toy-like proportions |
| Apple spatial computing (clean geometry, soft glass) | Neon overload or generic cyberpunk |
| UE5 architectural visualization (precise detail, cinematic cameras) | Photorealistic simulation |
| Dark sophistication, night-time grandeur | Daytime scenes, suburban scale |

### Brand Colors

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary (60%) | Burnt Orange | `#FF5E00` | Energy veins, SIA Tower glow, primary accents |
| Secondary (30%) | Forest Green | `#34A853` | Success states, achievement indicators, nature districts |
| Tertiary (10%) | Royal Purple | `#7F24FF` | AI/coach elements, intelligence indicators |

### Typography

| Font | Usage |
|------|-------|
| **Sora** | System-wide — all UI, labels, HUD elements |
| **Chillax** | Logo wordmark only — never for body text |

### Sky and Atmosphere

- **Zenith**: Ink-blue (`#0A0A0F`) with scattered stars
- **Horizon**: Warm amber gradient blending upward into purple-indigo
- **Aurora**: Subtle orange-purple bands drifting slowly across the upper sky
- **Fog**: Exponential distance fog, warm amber tint, density tuned per scene

### Scale Rules

- SIA Tower: **100+ floors** — the unmistakable dominant landmark
- District buildings: **20-40 floors** — metropolitan skyscrapers, NOT suburban houses
- The city feels like a dense, vertical metropolis at all times

---

<!-- section:structures -->
## 2. The 12 Structures

| # | Name | Color | Hex | Floors | GLB Filename |
|---|------|-------|-----|--------|--------------|
| 00 | SIA Life Coach Tower | Burnt Orange | `#FF5E00` | 100+ | `sia-tower.glb` |
| 01 | Fitness | Forest Green | `#34A853` | 30 | `fitness-gym.glb` |
| 02 | Yoga and Wellbeing | Sage | `#6EE7B7` | 25 | `yoga-sanctuary.glb` |
| 03 | Finance | Rich Gold | `#F59E0B` | 35 | `finance-tower.glb` |
| 04 | Knowledgebase | Royal Purple | `#7F24FF` | 30 | `knowledgebase-library.glb` |
| 05 | Chat and Communication | Burnt Orange | `#FF5E00` | 28 | `chat-hub.glb` |
| 06 | Leaderboard and Competition | Bright Coral | `#FB7185` | 30 | `leaderboard-arena.glb` |
| 07 | Relationships | Warm Rose | `#F43F5E` | 15 | `relationships-garden.glb` |
| 08 | Career | Electric Blue | `#3B82F6` | 40 | `career-towers.glb` |
| 09 | Recovery and Sleep | Ethereal Indigo | `#6366F1` | 20 | `recovery-dreamscape.glb` |
| 10 | AI Analytics | Teal | `#14B8A6` | 30 | `analytics-cathedral.glb` |
| 11 | Nutrition | Warm Amber | `#D97706` | 25 | `nutrition-farm.glb` |

Each structure has a distinct architectural personality:
- **Fitness** (01): Angular, aggressive geometry — cantilevers, exposed structural beams
- **Yoga and Wellbeing** (02): Organic, flowing curves — living walls, soft arches
- **Finance** (03): Crystalline precision — faceted glass, sharp edges, mathematical symmetry
- **Knowledgebase** (04): Grand library cathedral — tall arched windows, layered tiers
- **Communication** (05): Signal-tower aesthetic — antenna arrays, interconnected nodes
- **Leaderboard** (06): Arena/colosseum hybrid — tiered seating, dramatic apex
- **Relationships** (07): Garden pavilion — open, welcoming, lower profile, warm
- **Career** (08): Twin corporate towers — the tallest district, bridged at top
- **Recovery** (09): Dreamlike cocoon — smooth, closed, minimal openings, serene
- **Analytics** (10): Data cathedral — geometric lattice, exposed framework
- **Nutrition** (11): Vertical farm tower — terraced levels, greenhouse panels

---

<!-- section:layout -->
## 3. City Layout

```
                          N
                          |
              [Nutrition]   [Fitness]
                    \         /
         [Analytics]  \     /  [Yoga]
                  \    \   /    /
                   --------—--------
        [Recovery] |  CENTRAL  | [Finance]
                   |   PLAZA   |
                   |  SIA      |
                   |  TOWER    |
        [Career]   |           | [Knowledge]
                   --------—--------
                  /    /   \    \
       [Leaderboard] /     \ [Communication]
                    /         \
            [Relationships]   [Chat]
                          |
                          S
```

> Diagram is conceptual. Exact orbital positions will be finalized during Phase 6 (Assembly).

### Spatial Parameters

| Parameter | Value |
|-----------|-------|
| Central plaza diameter | 400m |
| Full city diameter | ~1.2km |
| SIA Tower position | Absolute center (0, 0, 0) |
| District arrangement | Orbital ring around tower |
| Street material | Dark obsidian with orange energy grid veins |
| Plaza surface | Polished dark stone with embedded orange energy channels |
| Boulevard style | Pedestrian-scale, tree-lined with ambient lighting |

---

<!-- section:materials -->
## 4. Material System (7-Slot)

The app overrides **ALL** material properties at runtime by slot name. Geometry is king — baked textures are irrelevant. Name every material in Blender to match these slot names exactly.

### Slot Definitions

| Slot | Regex Pattern | Surface % | Purpose |
|------|---------------|-----------|---------|
| `base` | `base\|wall\|body\|structure` | 50-55% | Structural surfaces (walls, floors, main body) |
| `accent` | `accent\|highlight\|trim` | 10-15% | District-colored architectural elements |
| `glass` | `glass\|window\|transparent` | 10-18% | Windows, glass panels, transparent surfaces |
| `detail` | `detail\|prop\|furniture` | 12-18% | Columns, railings, props, decorative trim |
| `emissive` | `emissive\|light\|glow\|led` | 3-8% | LEDs, signage, light strips, beacons |
| `energy` | `energy\|pipeline\|conduit\|vein` | 0-5% | Energy pipelines connecting to SIA Tower (opt-in) |
| `holo` | `holo\|holographic\|biolum` | 0-5% | Holographic and bioluminescent elements (opt-in) |

### Inactive State (Default)

| Slot | Color | Roughness | Metallic | Emission | Other |
|------|-------|-----------|----------|----------|-------|
| `base` | `#1E1E28` | 0.8 | 0.05 | 0 | — |
| `accent` | `#2A2A38` | 0.5 | 0.1 | 0 | — |
| `glass` | `#0F0F18` | 0.1 | 0.3 | 0 | Alpha 0.86 |
| `detail` | `#16161E` | 0.6 | 0.15 | 0 | — |
| `emissive` | District color | 0.3 | 0.0 | 0.06 | — |
| `energy` | `#FF5E00` | 0.2 | 0.0 | 0.1 | — |
| `holo` | District color | 0.1 | 0.0 | 0.15 | Alpha 0.4 |

### Active State (When district is highlighted or scroll-focused)

| Slot | Changes From Inactive |
|------|-----------------------|
| `base` | No change |
| `accent` | Color becomes district hex, emissive 0.3 |
| `glass` | Warm interior emissive 0.25 |
| `detail` | No change |
| `emissive` | District color emissive 1.2, `toneMapped: false` |
| `energy` | `#FF5E00` emissive 1.5, UV scroll animation, `toneMapped: false` |
| `holo` | District color alpha 0.6, emissive 0.8 |

### Slot Usage by Structure

Most structures use slots 1-5 plus `energy` (6 slots total). Slots 6-7 are opt-in:

| Structure | Uses `energy` | Uses `holo` |
|-----------|:-------------:|:-----------:|
| SIA Tower | Yes | Yes |
| Fitness | Yes | No |
| Yoga and Wellbeing | Yes | Yes |
| Finance | Yes | No |
| Knowledgebase | Yes | Yes |
| Communication | Yes | No |
| Leaderboard | Yes | No |
| Relationships | Yes | No |
| Career | Yes | No |
| Recovery and Sleep | Yes | No |
| Analytics | Yes | No |
| Nutrition | Yes | No |

---

<!-- section:constraints -->
## 5. Technical Constraints

### Polygon Budgets

| Asset Type | Triangle Count | File Size |
|------------|---------------|-----------|
| SIA Tower exterior | 20K-30K tris | 200-500 KB |
| District exteriors | 10K-20K tris | 80-400 KB |
| Interiors | 4K-15K tris | 50-300 KB (loaded on demand) |
| Energy pipelines | 500-1.5K tris each | 10-40 KB |
| **Total scene** | **180K-250K tris** | **2-5 MB** |

### Export Requirements

| Parameter | Value |
|-----------|-------|
| Format | glTF Binary (.glb) |
| Compression | Draco, level 6 |
| Axis | Y-up |
| Origin | Bottom-center of each structure |
| Transforms | All applied (Ctrl+A in Blender) |
| Cameras/Lights | None exported — set up in R3F |

### Decimation Rules

- **Per-object decimation ONLY** — never join meshes then decimate (destroys architectural detail)
- Preserve sharp edges on architectural features
- Test silhouette readability after decimation — if the shape is lost, undo and reduce less aggressively
- Small detail objects (antennas, railings) can tolerate heavier decimation than main body geometry

---

<!-- section:lighting -->
## 6. Lighting and Post-Processing

### 3-Point Cinematic Rig

| Light | Type | Position | Color | Intensity | Notes |
|-------|------|----------|-------|-----------|-------|
| Key Light | Sun | [-8, 20, -6] | `#FFE4CC` | 0.8 | Warm directional, slight downward angle |
| Rim Light | Spot | [10, 18, -14] | `#FF5E00` | 200W | Burnt Orange edge separation, blend 0.9 |
| Fill Light | Area | [5, 15, 10] | `#1a1a40` | Soft | Deep blue-purple ambient fill |

### Environment

| Parameter | Value |
|-----------|-------|
| World background | `#0A0A0F` (near-black) |
| Camera FOV | 45 degrees |
| Fog type | FogExp2 |
| Fog color | Warm amber tint |

### Post-Processing Stack (R3F EffectComposer)

| Effect | Purpose | Notes |
|--------|---------|-------|
| Bloom | Emissive glow on energy, accents, signs | Threshold ~0.8, strength tuned per scene |
| Vignette | Cinematic edge darkening | Subtle, offset ~0.3 |
| SSAO | Ambient occlusion for depth | Gentle, radius tuned to scene scale |
| FogExp2 | Atmospheric depth | Warm amber, density varies by camera distance |

---

<!-- section:energy -->
## 7. Energy System Overview

### Neural Light Pipelines

Orange energy conduits (`#FF5E00`) flow from the SIA Tower crown to every district. 11 pipelines total, following arced paths through the air above the city.

#### Energy Delivery Styles

| Style | Districts | Description |
|-------|-----------|-------------|
| **Hard pipeline** | Fitness, Career, Finance, Communication, Leaderboard, Knowledgebase, Analytics | Solid glowing tube with flowing light particles |
| **Warm mist** | Yoga and Wellbeing, Relationships | Particle cloud dispersal — no hard tube, energy arrives as a soft warm fog |
| **Faint thread** | Recovery and Sleep | Barely visible whisper of light — the gentlest delivery |

#### Special Delivery Overrides

| District | Override | Description |
|----------|----------|-------------|
| Knowledgebase | Waterfall | Energy cascades downward from above the building, flowing like liquid light |
| Leaderboard | Lightning bolt | Dramatic burst entry at the apex — energy arrives with a sharp crack of light |

### AI Pulse System (City Heartbeat)

Every 8 seconds, the SIA Tower crown emits an expanding orange ring of light:

| Time | Event |
|------|-------|
| T = 0.0s | Pulse originates at crown — orange intensifies at tower apex |
| T = 0.5s | Ring of light begins expanding outward from crown |
| T = 2.0s | Ring reaches inner district ring |
| T = 4.0s | All districts briefly brighten in response |
| T = 6.0s | Ring dissipates at city perimeter |
| T = 8.0s | Cycle repeats |

This heartbeat is always running. It communicates that SIA Tower is alive and continuously powering the city.

### Cross-District Gold Connections

Golden lines (`#F59E0B`) fire between districts when cross-pillar intelligence is active. These represent the AI recognizing connections across life domains (e.g., fitness recovery informing sleep patterns).

- Lines arc gracefully between connected district rooftops
- Floating insight cards appear at connection midpoints (translucent glass with brief text)
- Connections are transient — they fire, hold for 2-3 seconds, then fade

---

<!-- section:interiors -->
## 8. Interior Specifications

Each district has one interior room, loaded on demand when the user scrolls into that district's scene.

### Interior Requirements

| Requirement | Details |
|-------------|---------|
| Material system | Same 7-slot system as exteriors |
| Light empties | `light_0`, `light_1`, `light_2` — placed at logical light source positions in the room |
| Camera target | One empty named `camera_target` at the focal point of the room |
| Props | 4-8 module-specific props per room (e.g., dumbbells for Fitness, bookshelves for Knowledgebase) |
| Focal element | One clearly defined center-of-attention piece per room (the hero object) |
| Room shell | Complete enclosure: floor, walls, ceiling. One wall is open or windowed for exterior light |
| Polygon budget | 4K-15K tris |
| File size | 50-300 KB |

### Interior Design Principles

- Interiors should feel like a curated peek inside the district — intimate but connected to the larger city
- Warm ambient lighting through the open/windowed wall creates silhouette depth
- Props should be recognizable at low poly counts — silhouette clarity over surface detail
- The focal element should be positioned where the camera target empty points

---

<!-- section:build-sequence -->
## 9. Build Sequence and Rationale

Seven phases, strictly sequential. Each structure follows: **Exterior, Review, Interior, Review, Integration Test**. No skipping.

### Phase Overview

| Phase | Name | Structures | Rationale |
|-------|------|------------|-----------|
| 1 | **SIA Tower** | Module 00 | Hero landmark. Sets the quality bar and visual standard for everything else |
| 2 | **First 3 Districts** | 01 Fitness, 02 Yoga, 03 Finance | Establishes the full modeling range: angular (Fitness), organic (Yoga), crystalline (Finance) |
| 3 | **Middle 4** | 04 Knowledgebase, 05 Communication, 06 Leaderboard, 08 Career | Technical challenges: cathedral arches, antenna arrays, arena tiers, twin towers |
| 4 | **Final 4** | 07 Relationships, 09 Recovery, 10 Analytics, 11 Nutrition | Refined execution with established patterns |
| 5 | **Energy System** | All pipelines, pulse, connections | Requires approved structure positions from Phase 6 planning |
| 6 | **Assembly** | Full city integration | Place all structures, verify 17-scene camera paths, full city screenshot review |
| 7 | **App Integration** | R3F scroll experience | Connect 3D scene to web app with scroll-driven camera, UI overlays, loading system |

### Per-Structure Workflow

```
1. Review this MASTER-CONTEXT for structure specs
2. Run shared/lighting-rig.py in Blender
3. Run shared/material-library.py with district color
4. Model exterior geometry
5. Apply 7-slot materials by name
6. Decimate per-object to budget
7. Export GLB with Draco compression
8. Visual review (viewport screenshot)
9. Model interior (same material system)
10. Export interior GLB
11. Integration test in R3F viewer
```

---

<!-- section:tech-stack -->
## 10. Tech Stack

### 3D Pipeline (Blender)

| Tool | Purpose |
|------|---------|
| Blender 4.x | Primary modeling and scene composition |
| Blender MCP addon | Claude agent integration via `uvx blender-mcp` |
| `shared/lighting-rig.py` | Standard 3-point cinematic lighting setup |
| `shared/material-library.py` | 7-slot material system with district color parameter |
| `shared/export-pipeline.py` | Draco-compressed GLB export with validation |
| `shared/energy-pipeline-utils.py` | Energy conduit geometry generation |

### Web Application (Phase 7)

| Package | Purpose |
|---------|---------|
| Vite | Build tool and dev server |
| React 19 | UI framework |
| TypeScript | Type safety |
| Three.js | 3D rendering engine |
| React Three Fiber (R3F) | React renderer for Three.js |
| drei | R3F helpers (loaders, controls, effects) |
| @react-three/postprocessing | Bloom, DOF, Vignette, SSAO |
| GSAP + ScrollTrigger | Scroll-driven camera animation |
| Lenis | Smooth scroll behavior |
| Framer Motion | UI overlay animations (text, panels) |
| Zustand | Global state management |
| Tailwind CSS | Utility-first styling for UI overlays |

---

<!-- section:tools -->
## 11. Tools and MCP Setup

### Session Startup Checklist

Every modeling session requires:

1. Blender is open with MCP addon enabled
2. Blender MCP server running via `uvx blender-mcp`
3. Run `shared/lighting-rig.py` first (establishes consistent lighting)
4. Run `shared/material-library.py` with the target district color hex
5. Load this MASTER-CONTEXT document

### Available Blender MCP Tools

| Tool | Purpose |
|------|---------|
| `execute_blender_code` | Run Python scripts in Blender (primary tool for all modeling) |
| `get_viewport_screenshot` | Visual preview at key milestones (costs tokens — use strategically) |
| `get_scene_info` | Inspect full scene state (objects, counts, hierarchy) |
| `get_object_info` | Inspect individual object properties |
| `search_sketchfab_models` | Find CC-BY reference models on Sketchfab |
| `download_sketchfab_model` | Import Sketchfab model into scene |
| `search_polyhaven_assets` | Find HDRIs, PBR textures, 3D models on Poly Haven |
| `download_polyhaven_asset` | Import Poly Haven asset into scene |
| `generate_hyper3d_model_via_text` | AI text-to-3D for complex sub-components |
| `generate_hunyuan3d_model` | Alternative AI 3D generation |

### Claude Skills Used

| Skill ID | Name | When |
|----------|------|------|
| DESIGN-05 | Blender 3D Artist | Primary agent for all modeling sessions |
| DESIGN-07 | 3D Shaders and Materials | Material system development, energy shaders |
| EXPERT-01 | Senior Frontend Engineer | Phase 7 R3F application |
| EXPERT-05 | Full-Stack Engineer | Phase 7 integration and deployment |

---

<!-- section:gotchas -->
## 12. Known Gotchas

### React Three Fiber

| Issue | Cause | Fix |
|-------|-------|-----|
| WebGL context destroyed on hot reload | React StrictMode double-mounts and unmounts | Do NOT use `<StrictMode>` in `main.tsx` |
| Animations frozen | `frameloop="demand"` pauses the render loop | Use `frameloop="always"` |
| EffectComposer crash | Null child effects inside EffectComposer | Always null-check before rendering effects |
| Draco loader fails | Decoder WASM not found | Place Draco decoder files in `/public/draco/` |

### Blender and Export

| Issue | Cause | Fix |
|-------|-------|-----|
| Detail lost after decimation | Meshes were joined before decimating | Per-object decimation ONLY — never join then decimate |
| Materials look wrong in app | Baked textures from Blender are ignored | All materials are overridden at runtime by slot name — geometry is what matters |
| AI-generated mesh is unusable | Robo3D/Hyper3D output has bad topology | Use AI generation for sub-components only, then clean up. Never for whole buildings |
| Frame drops with 12 structures | Too many tris loaded at once | Implement LOD (Level of Detail) — progressive loading based on camera distance |

### General

| Issue | Cause | Fix |
|-------|-------|-----|
| Large GLB files | No compression applied | Always export with Draco compression level 6 |
| Objects offset in scene | Transforms not applied | `Ctrl+A` (Apply All Transforms) before export, origin at bottom-center |
| Inconsistent lighting between sessions | Lighting rig not loaded | Always run `shared/lighting-rig.py` first |

---

<!-- section:brand -->
## 13. Brand Compliance

### Color Distribution

| Weight | Color | Hex | Where It Appears |
|--------|-------|-----|------------------|
| 60% | Burnt Orange | `#FF5E00` | Energy veins, SIA Tower glow, primary accents, pipeline particles |
| 30% | Forest Green | `#34A853` | Achievement indicators, nature districts, success states |
| 10% | Royal Purple | `#7F24FF` | AI orbs, coach indicators, intelligence visualization |

### Surface Colors

| Surface | Color | Hex | Notes |
|---------|-------|-----|-------|
| Dark surfaces | Ink-900 | `#0A0A0F` | Near-black. Never use pure `#000000` |
| Base structure | Dark charcoal | `#1E1E28` | Warm undertone, not cold gray |
| Sky zenith | Ink-blue | `#0A0A0F` | Matches world background |

### Typography Rules

- Sora everywhere in the application
- Chillax for the SIA wordmark only
- Sentence case for all text (not Title Case, not ALL CAPS)

### Tone and Visual Language

| Do | Do Not |
|----|--------|
| Warm light blooms for celebration | Confetti of any kind |
| Period carries energy | Exclamation marks |
| Continuous stroke lines | Fading or broken lines |
| Stylized warm silhouettes for people | Photorealistic human models |
| Premium, subtle holographic signage | Loud, garish neon |

---

<!-- section:world-activity -->
## 14. World Activity Systems

The city is **never static**. At any moment, the following systems are visible and in motion:

### Vehicles and Drones

| Element | Count | Behavior |
|---------|-------|----------|
| Flying vehicles | 3-5 visible | Follow light-rail paths between districts, smooth arcing trajectories |
| Delivery drones | 2-4 visible | Smaller, lower altitude, orange navigation lights blinking |

### Human Activity

| Element | Description |
|---------|-------------|
| Pedestrian silhouettes | Stylized warm-toned figures walking boulevards, recognizable but abstracted |
| Working silhouettes | Figures at desks or workstations visible through glass walls |
| Connecting silhouettes | Pairs and groups interacting in plazas and gardens |

### AI Presence

| Element | Description |
|---------|-------------|
| Purple AI orbs | Small floating spheres (`#7F24FF`) accompanying some human silhouettes — the AI coach made visible |
| AI orb behavior | Hover near shoulder height, pulse gently, occasionally drift ahead as if guiding |

### Ambient Particles

| Zone | Particle Color | Behavior |
|------|---------------|----------|
| Energy zones (near pipelines) | Orange (`#FF5E00`) | Firefly-like, drift along pipeline paths |
| AI zones (near SIA Tower, Analytics) | Purple (`#7F24FF`) | Slower, more deliberate floating patterns |
| Nature zones (Yoga, Nutrition, Relationships) | Green (`#34A853`) | Organic, gentle rising and falling |

### Environmental Dynamics

| District Type | Weather/Atmosphere |
|---------------|-------------------|
| Wellness districts (Yoga, Relationships) | Calm — minimal particle motion, soft ambient light |
| Active districts (Fitness, Leaderboard, Career) | Energized — faster particles, sharper light pulses |
| Reflective districts (Recovery, Sleep) | Gentle mist — low visibility particles, dreamlike haze |
| Holographic signage | District-themed content, premium and subtle, warm color temperature |

---

<!-- section:appendix-a -->
## Appendix A: File Structure

```
balencia-city-v3/
├── MASTER-CONTEXT.md           ← This file (load every session)
├── shared/
│   ├── lighting-rig.py         # 3-point cinematic lighting setup
│   ├── material-library.py     # 7-slot material system
│   ├── export-pipeline.py      # Draco GLB export with validation
│   └── energy-pipeline-utils.py # Energy conduit geometry helpers
├── modules/
│   ├── 00-sia-tower/           # SIA Life Coach Tower
│   ├── 01-fitness/             # Fitness district
│   ├── 02-yoga/                # Yoga and Wellbeing district
│   ├── 03-finance/             # Finance district
│   ├── 04-knowledgebase/       # Knowledgebase district
│   ├── 05-communication/       # Chat and Communication district
│   ├── 06-leaderboard/         # Leaderboard and Competition district
│   ├── 07-relationships/       # Relationships district
│   ├── 08-career/              # Career district
│   ├── 09-recovery/            # Recovery and Sleep district
│   ├── 10-analytics/           # AI Analytics district
│   └── 11-nutrition/           # Nutrition district
├── energy-system/              # Pipelines, pulse, cross-district connections
└── assembly/                   # Full city scene, 17-scene verification
```

Each module folder will contain:
- `exterior.blend` — Blender source file
- `interior.blend` — Interior Blender source file
- `<name>.glb` — Exported exterior GLB
- `<name>-interior.glb` — Exported interior GLB
- `notes.md` — Per-module design decisions and review log

---

<!-- section:appendix-b -->
## Appendix B: 17-Scene Journey (Reference)

The scroll experience progresses through these scenes. Exact camera positions and transitions are defined during Phase 6-7.

| Scene | Name | Focus |
|-------|------|-------|
| 1 | Arrival | Wide establishing shot — city emerges from darkness |
| 2 | SIA Tower Reveal | Camera rises to reveal the full tower, crown pulsing |
| 3 | City Heartbeat | First AI pulse expands across the city |
| 4 | Fitness District | Fly into angular gym structure |
| 5 | Yoga Sanctuary | Gentle drift into organic wellness space |
| 6 | Finance Tower | Sharp approach to crystalline financial district |
| 7 | Knowledgebase | Descend into grand library cathedral |
| 8 | Communication Hub | Orbit signal-tower cluster |
| 9 | Leaderboard Arena | Dramatic swoop into competition space |
| 10 | Relationships Garden | Slow glide through warm garden pavilion |
| 11 | Career Towers | Rise between twin corporate towers |
| 12 | Recovery Dreamscape | Drift into serene cocoon |
| 13 | Analytics Cathedral | Fly through geometric data lattice |
| 14 | Nutrition Farm | Sweep across terraced vertical farm |
| 15 | Cross-District Intelligence | Gold connections fire across the city |
| 16 | Full City Panorama | Wide orbital shot showing everything connected |
| 17 | SIA Tower Return | Camera returns to tower crown — call to action |

---

<!-- section:appendix-c -->
## Appendix C: Quick Reference Card

**For every modeling session, remember:**

- Load this document first
- Run `shared/lighting-rig.py` before modeling
- Run `shared/material-library.py` with the district hex color
- Name materials by slot: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`
- Decimate per-object, never after joining
- Export with Draco level 6, Y-up, no cameras, no lights
- Apply all transforms, origin at bottom-center
- Take viewport screenshots at key milestones only (geometry done, materials done, final)
- Geometry is king. Baked textures are irrelevant. The app overrides all materials at runtime.
