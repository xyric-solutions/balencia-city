# Balencia City Visual Quality Upgrade Plan

## Problem Statement

All 12 district buildings in the Balencia City 3D web experience currently render as flat, wireframe-like sketches instead of polished, cinematic structures. The geometry is solid (225K+ approved tris across all buildings), but the **rendering pipeline** strips away all visual richness. The result looks like rough placeholder art instead of a finished product.

## Root Cause Analysis

After a full audit of the rendering stack, these are the root causes ranked by visual impact:

1. **Material override destroys all surface variation** — `apps/balencia/src/lib/materials.ts` line 140-164: `applyAppearance()` replaces every mesh material with flat scalar colors. No `envMapIntensity` property exists. Every surface becomes a single solid color with uniform roughness/metalness.

2. **No environment map** — `apps/balencia/src/components/scenes/CityExperience.tsx`: No HDRI, no cubemap, no `<Environment>` component. Glass and metallic surfaces have nothing to reflect — they render as dark flat planes.

3. **No shadow mapping** — No `castShadow`/`receiveShadow` on any mesh or light. Buildings have zero shadow depth. No `shadows` prop on the Canvas.

4. **Excessively rough/non-metallic materials** — Base roughness=0.8, metalness=0.05. Everything looks like chalky matte paint instead of architectural materials.

5. **No ambient occlusion** — Neither baked AO maps nor screen-space AO post-processing. No darkening in crevices means no perceived form.

6. **Minimal post-processing** — `apps/balencia/src/components/effects/PostProcessing.tsx` has only Bloom + Vignette. No SSAO, no color grading, no contrast enhancement.

7. **Inactive buildings nearly invisible** — Base color #1E1E28 with emissive intensity 0.01 makes inactive buildings almost completely black.

## Inspiration Reference

The target aesthetic (from provided concept art) features:
- Rich architectural detail with proper PBR materials (varying roughness, metalness)
- Glass buildings with visible environment reflections and warm interior glow
- Volumetric lighting with atmospheric haze and golden hour warmth
- Shadow depth giving form and grounding to structures
- Detailed ground surfaces with subtle reflectivity
- Particle effects (dust, light motes) catching light
- A premium, cinematic sci-fi city aesthetic

## Tech Stack

- React 19, @react-three/fiber v9, @react-three/drei ^10.0.0
- Three.js ^0.176.0
- @react-three/postprocessing ^3.0.0, postprocessing ^6.36.0
- GSAP + Lenis (scroll), Zustand (state), Tailwind CSS v4

## Constraints

- Performance budget: 250K tris overview, 270K focused scene
- Models are GLB with Draco compression loaded via `useGLTF`
- The 7-slot material naming convention must be preserved (base, accent, glass, detail, emissive, energy, holo)
- Dark aesthetic should remain but be less extreme — buildings must be recognizable even when inactive
- Must work on desktop and mobile
- All improvements are code-side — no Blender re-export needed

---

## Session 1: Environment Map + Material PBR Overhaul

**Goal**: Add environment reflections and tune material properties so surfaces have visible depth, specularity, and glass reflects light. This is the single highest-impact change.

### File 1: `apps/balencia/src/lib/materials.ts`

#### Change 1A: Add `envMapIntensity` to the SlotAppearance type (line 27-36)

**Current code (line 27-36):**
```typescript
type SlotAppearance = {
  color: string;
  roughness: number;
  metalness: number;
  emissive: string;
  emissiveIntensity: number;
  opacity: number;
  transparent: boolean;
  toneMapped: boolean;
};
```

**Target code:**
```typescript
type SlotAppearance = {
  color: string;
  roughness: number;
  metalness: number;
  emissive: string;
  emissiveIntensity: number;
  opacity: number;
  transparent: boolean;
  toneMapped: boolean;
  envMapIntensity: number;
};
```

#### Change 1B: Update PBR values in `getSlotAppearance` (lines 64-135)

For each material slot inside the `inactive` object, update these specific properties:

**base slot (lines 65-74):**
- `roughness`: 0.8 → **0.62**
- `metalness`: 0.05 → **0.12**
- `emissiveIntensity`: change `active ? 0.018 : 0.01` → `active ? 0.018 : 0.03`
- Add: `envMapIntensity: 0.4`

**accent slot (lines 75-84):**
- `roughness`: 0.5 → **0.38**
- `metalness`: 0.1 → **0.35**
- Add: `envMapIntensity: 0.6`

**glass slot (lines 85-94):**
- `roughness`: 0.16 → **0.05**
- `metalness`: 0.22 → **0.92**
- `emissiveIntensity`: change `active ? 0.18 : 0.035` → `active ? 0.18 : 0.06`
- Add: `envMapIntensity: 1.8`

**detail slot (lines 95-104):**
- `roughness`: 0.6 → **0.48**
- `metalness`: 0.15 → **0.2**
- Add: `envMapIntensity: 0.3`

**emissive slot (lines 105-114):**
- No changes to existing values
- Add: `envMapIntensity: 0.1`

**energy slot (lines 115-124):**
- No changes to existing values
- Add: `envMapIntensity: 0.15`

**holo slot (lines 125-134):**
- No changes to existing values
- Add: `envMapIntensity: 0.5`

#### Change 1C: Apply envMapIntensity in `applyAppearance` (line 140-164)

**Add this block after the emissiveIntensity block (after line 157):**
```typescript
if ("envMapIntensity" in standard) {
  standard.envMapIntensity = appearance.envMapIntensity;
}
```

#### Change 1D: Update `applyEnergyMaterialOverrides` spread (line 197)

The spread `{ ...appearance, emissiveIntensity: ... }` will automatically include `envMapIntensity` from the slot appearance, so no change needed here.

### File 2: `apps/balencia/src/components/scenes/CityExperience.tsx`

#### Change 1E: Add Environment import (line 1)

Add `Environment` to the drei import. Currently there is no drei import in this file, so add:
```typescript
import { Environment } from "@react-three/drei";
```

#### Change 1F: Add Environment component inside Canvas (after line 98)

After `<Atmosphere />` (line 98), add:
```tsx
<Environment preset="night" environmentIntensity={0.35} />
```

This uses the `dikhololo_night_1k.hdr` HDRI preset — a dark nighttime environment with subtle points of light, appropriate for the sci-fi city aesthetic. `background={false}` is the default so the existing sky dome is preserved. `environmentIntensity={0.35}` keeps reflections subtle.

#### Change 1G: Add tone mapping exposure (line 95)

After `gl.outputColorSpace = THREE.SRGBColorSpace;` (line 95), add:
```typescript
gl.toneMappingExposure = 1.15;
```

This slightly boosts overall luminance to compensate for the dark environment map.

### Session 1 Verification

1. Run `cd apps/balencia && npm run dev`
2. Open localhost:3005 in browser
3. Scroll to Scene 1 (overview): inactive buildings should be visible dark shapes, not black voids
4. Scroll to Scene 4+ (focused district): glass surfaces should show visible reflections from the HDRI
5. Check accent trim pieces — they should catch light and have visible specularity
6. Check Performance panel in DevTools — no frame rate regression expected (env map is a single cubemap lookup per fragment)
7. Run `cd apps/balencia && npm run build` to verify TypeScript compiles

---

## Session 2: Shadow System

**Goal**: Buildings cast shadows onto the ground and each other, adding form depth and spatial grounding.

### File 1: `apps/balencia/src/components/scenes/CityExperience.tsx`

#### Change 2A: Add shadows to Canvas (line 76)

Add `shadows="soft"` prop to the `<Canvas>` element. This enables `THREE.VSMShadowMap` (soft edges, good performance).

**Current (line 76):**
```tsx
<Canvas
  className="city-canvas"
  frameloop="always"
```

**Target:**
```tsx
<Canvas
  className="city-canvas"
  frameloop="always"
  shadows="soft"
```

#### Change 2B: Update directional light to cast shadows (line 28)

**Current (line 28):**
```tsx
<directionalLight position={[-8, 22, 10]} color="#FFE4CC" intensity={warmKeyIntensity} />
```

**Target:**
```tsx
<directionalLight
  position={[-8, 22, 10]}
  color="#FFE4CC"
  intensity={warmKeyIntensity}
  castShadow
  shadow-mapSize-width={1024}
  shadow-mapSize-height={1024}
  shadow-camera-near={0.5}
  shadow-camera-far={80}
  shadow-camera-left={-60}
  shadow-camera-right={60}
  shadow-camera-top={60}
  shadow-camera-bottom={-60}
  shadow-bias={-0.0004}
  shadow-normalBias={0.02}
/>
```

Only the directional key light casts shadows. The spotlight and point lights do NOT cast shadows — this is a standard performance trade-off.

### File 2: `apps/balencia/src/components/scenes/ModelAsset.tsx`

#### Change 2C: Enable shadows on structure meshes (inside ApprovedStructure, line 25-27)

**Current useEffect (lines 25-27):**
```typescript
useEffect(() => {
  applyBalenciaMaterialOverrides(gltf.scene, structure.hex, active);
}, [active, gltf.scene, structure.hex]);
```

**Target:**
```typescript
useEffect(() => {
  applyBalenciaMaterialOverrides(gltf.scene, structure.hex, active);
  gltf.scene.traverse((child) => {
    if ((child as THREE.Mesh).isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });
}, [active, gltf.scene, structure.hex]);
```

#### Change 2D: Enable shadows on interior meshes (inside ApprovedInterior, line 46-48)

Same pattern — add the traverse after `applyBalenciaMaterialOverrides` in the useEffect.

### File 3: `apps/balencia/src/components/scenes/CityContext.tsx`

#### Change 2E: Ensure ground meshes receive shadows

Find all ground-level `<mesh>` elements (island ground, district pads, roads, civic plaza) and ensure they have `receiveShadow` prop. Some may already have it — verify and add where missing.

### Session 2 Verification

1. Run dev server, scroll to Scene 1: buildings should cast visible soft shadows on the ground
2. Scroll to focused scenes: shadow softness visible at edges (VSM)
3. Check for shadow acne (flickering dots) — if present, adjust `shadow-bias` and `shadow-normalBias`
4. Check for peter-panning (shadows detached from objects) — if present, reduce bias magnitude
5. Check Performance panel: frame time should stay under 16ms on desktop
6. Run build to verify TypeScript compiles

---

## Session 3: Post-Processing Stack

**Goal**: Add screen-space ambient occlusion for micro-shadow form definition, color grading for cinematic warmth, and contrast enhancement.

### File 1: `apps/balencia/src/components/effects/PostProcessing.tsx`

#### Change 3A: Replace entire file contents

**Current (full file):**
```tsx
import { Bloom, EffectComposer, Vignette } from "@react-three/postprocessing";

export function BalenciaPostProcessing() {
  return (
    <EffectComposer multisampling={0}>
      <Bloom intensity={0.72} luminanceThreshold={0.24} luminanceSmoothing={0.68} mipmapBlur />
      <Vignette offset={0.22} darkness={0.46} />
    </EffectComposer>
  );
}
```

**Target:**
```tsx
import {
  Bloom,
  BrightnessContrast,
  EffectComposer,
  HueSaturation,
  N8AO,
  Vignette,
} from "@react-three/postprocessing";

export function BalenciaPostProcessing() {
  return (
    <EffectComposer multisampling={0}>
      <N8AO
        aoRadius={2.5}
        distanceFalloff={0.8}
        intensity={1.8}
        quality="medium"
        halfRes
        color="#0A0A0F"
      />
      <Bloom
        intensity={0.68}
        luminanceThreshold={0.22}
        luminanceSmoothing={0.65}
        mipmapBlur
      />
      <BrightnessContrast brightness={0.02} contrast={0.12} />
      <HueSaturation hue={0} saturation={0.08} />
      <Vignette offset={0.24} darkness={0.52} />
    </EffectComposer>
  );
}
```

**Effect-by-effect rationale:**

- **N8AO** (modern, fast alternative to SSAO): `aoRadius=2.5` catches building crevices and window recesses. `halfRes=true` halves the resolution for performance. `color="#0A0A0F"` tints AO toward the brand ink color. `intensity=1.8` is aggressive but appropriate for a dark scene where AO defines form. `distanceFalloff=0.8` fades AO at distance.

- **Bloom**: Slightly lower threshold (0.22 vs 0.24) catches more emissive surfaces. Intensity slightly reduced (0.68 vs 0.72) because the new materials have more visual information that bloom can obscure.

- **BrightnessContrast**: `contrast=0.12` deepens shadows and brightens highlights for more dynamic range. `brightness=0.02` is a tiny lift to compensate for AO darkening.

- **HueSaturation**: `saturation=0.08` makes district colors slightly more vivid.

- **Vignette**: Slightly darker (0.52 vs 0.46) for more cinematic framing.

### Session 3 Verification

1. Run dev server, scroll to a focused building: AO darkening should be visible in window recesses, floor plate edges, ground-building junctions
2. Check that bloom still highlights energy/emissive elements without over-bleeding
3. Overall image should feel warmer and higher contrast
4. Check Performance panel: total post-processing should add <3ms
5. Look for banding artifacts from half-res AO — if visible, try `quality="high"` or remove `halfRes`
6. Run build to verify TypeScript compiles

---

## Session 4: Lighting Refinement + Ground Polish

**Goal**: Balance lighting to reduce harsh contrast, add a fill light so shadowed sides aren't pitch black, and make ground surfaces more reflective.

### File 1: `apps/balencia/src/components/scenes/CityExperience.tsx`

#### Change 4A: Warm and brighten ambient/hemisphere lights (lines 26-27)

**Current (line 26):**
```tsx
<ambientLight intensity={isOverview ? 0.3 : 0.27} color="#282335" />
```
**Target:**
```tsx
<ambientLight intensity={isOverview ? 0.34 : 0.31} color="#2D2840" />
```

**Current (line 27):**
```tsx
<hemisphereLight args={["#FFE4CC", "#08080D", isOverview ? 0.36 : 0.32]} />
```
**Target:**
```tsx
<hemisphereLight args={["#FFD4B0", "#08080D", isOverview ? 0.38 : 0.35]} />
```

#### Change 4B: Warm the key light color (line 28)

Change the directional light color from `"#FFE4CC"` to `"#FFD8B0"` (more golden).

#### Change 4C: Add fill light (after line 28 / after the directional light)

Add a new directional light from the opposite side to fill shadows:
```tsx
<directionalLight position={[6, 14, -8]} color="#1E2844" intensity={0.4} />
```

This is a cool-toned fill light that prevents shadowed sides from being completely black while maintaining the warm/cool contrast of cinematic lighting.

### File 2: `apps/balencia/src/components/scenes/CityContext.tsx`

#### Change 4D: Enhance ground surface materials

Find the ground surface meshStandardMaterial instances and update their properties. The specific meshes to target are:

- **Main island ground** (the large base circle): Add `metalness={0.08}` `roughness={0.78}` `envMapIntensity={0.15}`
- **Road ring surfaces** (FlatRing geometries with road colors): Update to `metalness={0.14}` `roughness={0.55}` (wet-road sheen)
- **Canal/water strip surfaces**: Update to `metalness={0.35}` `envMapIntensity={0.4}` (water-like reflection)
- **Civic plaza center**: Update to `metalness={0.24}` `roughness={0.38}` (polished stone)

Note: You'll need to read CityContext.tsx first to find the exact mesh/material locations. The file uses `SURFACE` color constants (lines 31-49) for different ground types.

### Session 4 Verification

1. Run dev server, rotate camera around a building: the shadowed side should now show subtle cool fill light instead of being pitch black
2. Ground surfaces should show faint reflections from the environment map
3. Roads should have a subtle wet-look sheen
4. Overall scene should feel warmer and more inviting while keeping the dark aesthetic
5. Check that the fill light doesn't wash out the dramatic key light contrast
6. Run build to verify TypeScript compiles

---

## Session 5: Atmospheric Effects + Particles

**Goal**: Add volumetric atmosphere, floating dust/light particles, and a light beacon from SIA tower for a "living city" feel.

### File 1: `apps/balencia/src/components/scenes/AtmosphereDepthLayer.tsx`

#### Change 5A: Add low-altitude golden fog ring

In the `HorizonFogShelves` component (or as a new child of `AtmosphereDepthLayer`), add a new fog ring mesh:
- Position: y=0.3 (ground level)
- Geometry: ring with inner radius matching island boundary, outer radius extending ~30 units beyond
- Material: `color="#FFB066"`, `opacity=0.04`, `blending: THREE.AdditiveBlending`, `transparent: true`, `depthWrite: false`
- Purpose: Simulates warm atmospheric scattering at ground level

#### Change 5B: Enhance horizon warm glow

In the `SkyGradientDome` vertex color computation, increase the warm band at the horizon. The `horizonOrange` color (currently something like `#35170E`) should be slightly more vivid — try `#3D1D12`. This simulates city light pollution bouncing off atmospheric moisture.

### File 2: New component or addition to `LivingEnergyLayer.tsx`

#### Change 5C: Add floating dust/light particle field

Create a point cloud of warm-white particles spread across the city:
- Count: ~200-300 particles
- Color: `#FFE4CC` (warm cream, matching the key light)
- Size: 0.1-0.15 (small enough to read as dust, large enough to catch bloom)
- Position distribution: spread across the city footprint (x/z: ±80 units), concentrated at low altitude (y: 0.3-8.0)
- Animation: slow upward drift (0.002 units/frame) with slight sine-wave lateral motion
- Material: `AdditiveBlending`, `toneMapped: false`, `transparent: true`, `opacity: 0.6`
- These particles will catch the bloom post-processing and create a sparkling, alive atmosphere

#### Change 5D: Add volumetric light cone from SIA tower

Create a simple visual effect suggesting a light beam from the SIA tower crown:
- Geometry: `CylinderGeometry` (narrow at bottom, wider at top, or vice versa)
- Position: centered on SIA tower (check `shared/city-layout-v2.json` for SIA position, approximately [0, 0, 0])
- Height: extends from tower crown (~y=33) upward ~40 units
- Material: `AdditiveBlending`, `color="#FF5E00"`, `opacity=0.03-0.05`, `transparent: true`, `depthWrite: false`, `side: THREE.DoubleSide`
- Animation: slow rotation (0.003 rad/frame) and subtle breathing (opacity oscillates ±20% via sine wave)
- This is NOT true volumetric rendering — it's a semi-transparent mesh that looks volumetric when combined with bloom

### Session 5 Verification

1. Run dev server, look at the horizon: should see a warm atmospheric glow
2. Look at the city from overview: floating dust particles should be visible, catching the bloom
3. SIA tower should have a visible upward light cone/beacon
4. Particles should NOT be distracting — they should add subtle ambiance
5. Check for particle popping (particles appearing/disappearing abruptly) — if present, fade particles near the edges of the distribution
6. Run build to verify TypeScript compiles

---

## Session 6: Scene-Aware Tuning + Performance Guard

**Goal**: Make post-processing adapt per scene type, add depth-of-field for focused building scenes, and add performance fallbacks for weaker devices.

### File 1: `apps/balencia/src/components/effects/PostProcessing.tsx`

#### Change 6A: Make post-processing scene-aware

Import `useScrollStore` and read `sceneIndex`. Adjust effect parameters based on scene type:

```tsx
import { useScrollStore } from "../../store/useScrollStore";

export function BalenciaPostProcessing() {
  const sceneIndex = useScrollStore((state) => state.sceneIndex);
  const isOverview = sceneIndex === 1 || sceneIndex === 15 || sceneIndex === 17;
  const isFocused = sceneIndex >= 4 && sceneIndex <= 14;

  // Scale AO by scene type
  const aoRadius = isOverview ? 3.5 : 2.0;
  const aoIntensity = isOverview ? 1.5 : 2.0;
  const aoQuality = isOverview ? "low" : "medium";

  // Scale bloom by scene type
  const bloomIntensity = isOverview ? 0.62 : 0.72;
  const bloomThreshold = isOverview ? 0.28 : 0.2;

  return (
    <EffectComposer multisampling={0}>
      <N8AO aoRadius={aoRadius} distanceFalloff={0.8} intensity={aoIntensity} quality={aoQuality} halfRes color="#0A0A0F" />
      <Bloom intensity={bloomIntensity} luminanceThreshold={bloomThreshold} luminanceSmoothing={0.65} mipmapBlur />
      <BrightnessContrast brightness={0.02} contrast={0.12} />
      <HueSaturation hue={0} saturation={0.08} />
      <Vignette offset={0.24} darkness={isOverview ? 0.48 : 0.54} />
    </EffectComposer>
  );
}
```

#### Change 6B: Add optional Depth of Field for focused scenes

For focused building scenes (4-14), conditionally add DOF:
```tsx
{isFocused && (
  <DepthOfField focusDistance={0.02} focalLength={0.04} bokehScale={2.5} />
)}
```

Import `DepthOfField` from `@react-three/postprocessing`. Place it after Bloom in the effect stack.

**Note**: DOF is the most expensive post-processing effect. If it causes frame drops, it can be removed or gated behind a quality tier check.

### File 2: `apps/balencia/src/lib/materials.ts`

#### Change 6C: Add device quality tier detection

Add a utility function to detect GPU capability:

```typescript
export function getDeviceQualityTier(): "high" | "medium" | "low" {
  if (typeof navigator === "undefined") return "high";
  const canvas = document.createElement("canvas");
  const gl = canvas.getContext("webgl2") || canvas.getContext("webgl");
  if (!gl) return "low";
  const debugInfo = gl.getExtension("WEBGL_debug_renderer_info");
  const renderer = debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : "";
  if (/Mali|Adreno|PowerVR|Apple GPU/i.test(renderer)) return "medium";
  if (/Intel|Iris/i.test(renderer)) return "medium";
  return "high";
}
```

This can be called once at app startup and used to scale `envMapIntensity` values:
- high: full values as designed in Session 1
- medium: envMapIntensity * 0.6
- low: envMapIntensity * 0.3

### File 3: `apps/balencia/src/components/scenes/CityExperience.tsx`

#### Change 6D: Scale environment and shadow quality by device tier

```tsx
const tier = useMemo(() => getDeviceQualityTier(), []);
const envIntensity = tier === "high" ? 0.35 : tier === "medium" ? 0.21 : 0.1;
const shadowMapSize = tier === "high" ? 1024 : tier === "medium" ? 512 : 256;
```

Apply these to the `<Environment>` component and shadow map size on the directional light.

#### Change 6E: Scene-aware environment intensity

Adjust environment intensity based on scene type for better visual focus:
- Overview scenes (1, 15, 17): `environmentIntensity={0.3}`
- SIA focus scenes (2, 3): `environmentIntensity={0.4}`
- District focused scenes (4-14): `environmentIntensity={0.35}`

### Session 6 Verification

1. Run dev server, scroll through all 17 scenes: transitions should feel smooth with no visual popping
2. Focused building scenes (4-14): background should have subtle bokeh blur from DOF
3. Overview scenes: AO should use wider radius, bloom should be softer
4. Test on a mobile device or throttled GPU: frame rate should stay above 30fps
5. If DOF causes frame drops, remove it and note in the session log
6. Run build to verify TypeScript compiles

---

## File Reference Summary

| File | Sessions | Role |
|------|----------|------|
| `apps/balencia/src/lib/materials.ts` | 1, 6 | Material PBR properties, envMapIntensity, device tier |
| `apps/balencia/src/components/scenes/CityExperience.tsx` | 1, 2, 4, 6 | Canvas config, Environment, lighting, shadows |
| `apps/balencia/src/components/effects/PostProcessing.tsx` | 3, 6 | Full post-processing stack |
| `apps/balencia/src/components/scenes/ModelAsset.tsx` | 2 | Shadow enable on building meshes |
| `apps/balencia/src/components/scenes/CityContext.tsx` | 2, 4 | Ground surface materials, shadow receive |
| `apps/balencia/src/components/scenes/AtmosphereDepthLayer.tsx` | 5 | Fog layers, horizon glow |
| `apps/balencia/src/components/scenes/LivingEnergyLayer.tsx` | 5 | Particles, light cone |
| `apps/balencia/src/store/useScrollStore.ts` | 6 (read only) | Scene index for conditional rendering |

## Dependencies (already installed)

- `@react-three/drei` ^10.0.0 — provides `Environment` component with HDRI presets
- `@react-three/postprocessing` ^3.0.0 — provides `N8AO`, `BrightnessContrast`, `HueSaturation`, `DepthOfField`
- `postprocessing` ^6.36.0 — underlying library for post-processing effects
- `three` ^0.176.0 — Three.js core

## Session Execution Order

Sessions MUST be executed in order (1 → 2 → 3 → 4 → 5 → 6). Each session builds on the previous:
- Session 2 (shadows) benefits from Session 1's environment map for shadow/light interplay
- Session 3 (SSAO) needs Session 1's materials to have detail worth occluding
- Session 4 (lighting) needs Sessions 1-3 in place to properly balance
- Session 5 (atmosphere) needs the full lighting/material stack to look correct
- Session 6 (tuning) adjusts everything from Sessions 1-5

## Post-Session Verification Checklist (run after every session)

1. `cd apps/balencia && npm run dev` — start dev server
2. Open localhost:3005 in browser
3. Scroll through all 17 scenes — check for visual regressions
4. Test overview (scene 1) and focused (scene 4-14) views
5. Open DevTools Performance panel — verify frame time <16ms desktop
6. `cd apps/balencia && npm run build` — verify TypeScript compiles with no errors
7. Take a screenshot and compare against previous session's output
