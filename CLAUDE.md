# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Balencia City v3 is a premium 3D cinematic web experience for the SIA Life Coach platform. It renders a scroll-driven fly-through of a 12-structure virtual city (SIA Tower + 11 district buildings), each representing a life-coaching domain (fitness, finance, relationships, etc.). The city is presented as a 17-scene scroll journey with animated camera transitions, energy pipelines between structures, and interactive district overlays.

## Commands

```bash
# Development (from repo root)
cd apps/balencia && npm run dev          # Vite dev server on localhost:3005

# Build (runs tsc --noEmit then vite build)
npm run build                            # From repo root (delegates to apps/balencia)
cd apps/balencia && npm run build        # Directly

# Preview production build
cd apps/balencia && npm run preview      # Serves on localhost:3006

# Asset sync (copies GLB models from modules/ → public/models/)
cd apps/balencia && npm run sync:assets  # Also runs automatically as predev/prebuild

# QA scripts (Playwright-based session validation)
cd apps/balencia && npm run qa:session84 # Example — each session has its own qa script
```

There is no linter or test runner configured. The build script (`scripts/build.mjs`) runs `tsc --noEmit` for type-checking before `vite build`.

## Architecture

### Monorepo Layout

- **`apps/balencia/`** — The Vite + React + Three.js web application (the only runtime app)
- **`modules/00-11/`** — Blender source files and exported GLB models per district (exterior, interior, screenshots, SPEC.md, REVIEW.md)
- **`shared/`** — Blender Python scripts (lighting rigs, material library, export pipeline) and `city-layout-v2.json` (authoritative district positions)
- **`energy-system/`** — Energy pipeline and cross-connection GLB assets, shader params, pulse ring
- **`assembly/`** — Full-city assembly screenshots, performance reports, scroll verification images
- **`prompts/`** — Session prompt templates used during the Blender MCP build workflow

### Web App (`apps/balencia/src/`)

**Rendering stack**: React 19, @react-three/fiber (R3F) v9, @react-three/drei, Three.js 0.176, GSAP + Lenis for scroll-driven animation, Zustand for state, Tailwind CSS v4, Framer Motion for UI transitions.

**Key data flow**:
1. `useBalenciaScrollTimeline` (hook) — Binds Lenis smooth-scroll to a GSAP timeline scrubbed by ScrollTrigger. Maps scroll position (0–1) to one of 17 scenes.
2. `useScrollStore` (Zustand) — Central state: `sceneIndex`, `progress`, `sceneLocalProgress`, `activeDistrict`, `activeInteriorId`, `activeEnergyIds`, overlay text. All scene-derived state computed here.
3. `scroll-scenes.ts` — Defines all 17 `ScrollScene` objects with camera positions, scroll breakpoints, interior thresholds, energy activation, and overlay copy.
4. `CityExperience` → `CityScene` — R3F Canvas entry point. Renders structures, interiors, energy assets, atmosphere, labels, and post-processing.

**Asset pipeline**:
- `src/lib/asset-manifest.json` — Source of truth for all GLB paths, district colors, and positions
- `scripts/sync-assets.mjs` — Copies GLBs from `modules/` and `energy-system/` into `public/models/` based on the manifest
- `city-layout-v2.ts` imports `shared/city-layout-v2.json` for authoritative runtime positions (overrides manifest positions)
- All GLBs loaded via `useGLTF` with Draco decompression (`/draco/` decoder path)

**Material system** (`lib/materials.ts`):
- 7-slot naming convention: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`
- Material names in GLBs are auto-classified by regex pattern matching
- `applyBalenciaMaterialOverrides` re-skins every mesh at runtime based on district color and active state

**District metadata** (`lib/district-metadata.ts`):
- `DISTRICT_PROFILES` — Per-district visual config: label placement, pad shape, motif, activity tone, preview text
- Label layout overrides per scene for overview, focused, and active views

### Build Phases

The project follows a strict sequential build order documented in `BUILD-ORDER.md`:
- Phases 1–4: Structure modeling in Blender (one module at a time, exterior before interior)
- Phase 5: Energy system (pipelines, mist, cross-connections, AI pulse ring)
- Phase 6: Full assembly verification
- Phase 7: Web app integration (scroll timeline, materials, labels, post-processing)
- Phase 8: Exterior polish passes
- Phase 9: App-experience repairs (tracked in `BALENCIA-CURRENT-AUDIT.md`)
- Phase 10: LOD and optimization (tracked in `apps/balencia/PHASE-10-BACKLOG.md`)

### Key Conventions

- 12 structures identified by slug: `sia-tower`, `fitness`, `yoga`, `finance`, `knowledgebase`, `chat`, `leaderboard`, `relationships`, `career`, `recovery`, `analytics`, `nutrition`
- Scene indices 1–17; overview scenes are 1, 15, 17; SIA focus scenes are 2, 3; district scenes are 4–14
- Brand colors defined in `BRAND_COLORS` constant — ink (#0A0A0F) is the base dark, energy (#FF5E00) is the signature orange
- Each structure has overview exterior, hero exterior (higher LOD for focused scenes), and interior GLBs
- `QUALITY-RUBRIC.md` defines 8 quality gates that every asset must pass

### Deployment

Deployed on Railway. Config in `railway.json` — builds with Railpack, serves the Vite preview server on `$PORT`.

### Custom Skills

The `.agents/skills/` directory contains orchestration skills for the multi-phase build workflow (`balencia-build`, `balencia-structure-team`, `balencia-energy-team`, `balencia-assembly-team`, `balencia-app-team`, `balencia-qa`, etc.). These automate session prompting and progress tracking.
