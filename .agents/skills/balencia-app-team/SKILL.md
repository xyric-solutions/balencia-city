---
name: balencia-app-team
description: "Build the Balencia City React Three Fiber scroll experience after assembly is approved. Use for Phase 7 app scaffolding, GLB loading, 17-scene camera timeline, shaders, UI overlays, and web performance QA."
---

# Balencia App Team

## Purpose

Turn approved Balencia assets into the production web experience: a 17-scene cinematic scroll journey using Vite, React, Three.js, React Three Fiber, GSAP, Lenis, Zustand, and post-processing.

## Required Context

- Confirm Phase 7 readiness in `PROGRESS.md` and `BUILD-ORDER.md`; assembly should be approved first.
- Read `SCROLL-JOURNEY.md`, `MASTER-CONTEXT.md` sections `materials`, `energy`, `tech-stack`, and `gotchas`.
- Read `energy-system/SHADER-PARAMS.md` if it exists.
- Locate the app scaffold in `app/`, `apps/balencia/`, or create one only when the user asks to implement the app.

## Workflow

1. Scaffold or update a Vite React TypeScript app only after assembly assets are ready or the user explicitly asks for an early prototype.
2. Place approved GLBs under the app public model path and configure Draco decoder assets under `public/draco/`.
3. Implement GLB loading, material slot overrides, and preload paths before scene choreography.
4. Build the 17-scene scroll timeline from `SCROLL-JOURNEY.md` with GSAP ScrollTrigger and Lenis.
5. Add energy flow, pulse ring, gold connections, post-processing, overlays, and state management.
6. Verify desktop and mobile performance, loading budget, browser behavior, and end-to-end scroll readability.

## Runtime Gotchas

- Do not wrap the R3F `Canvas` in React StrictMode if it causes WebGL context churn.
- Null-check post-processing effects before passing them to an EffectComposer.
- Keep `frameloop="always"` for smooth scroll-driven animation.
- Match runtime material overrides by the 7-slot names defined in `MASTER-CONTEXT.md`.

## Outputs

- Preferred app path: `apps/balencia/`; fallback path: `app/`.
- Public assets: `public/models/` and `public/draco/`.
- Source structure: `src/components/scenes/`, `src/components/ui/`, `src/components/effects/`, `src/hooks/`, and `src/store/`.
- QA evidence: build output, browser screenshots, performance notes, and any known limitations.
