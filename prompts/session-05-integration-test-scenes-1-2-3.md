# Balencia City v3 — Session 5: Integration Test (Scenes 1, 2, 3 Camera Verification)

## CONTEXT

You are running the FIRST integration test for Balencia City v3. The SIA Tower is now
fully complete — exterior and interior both approved. Before moving to Phase 2 (districts),
we must verify that the two approved GLBs work together and that Scenes 1, 2, and 3 of the
17-scene scroll journey will actually read correctly on camera.

This is NOT a modeling session. No new geometry is created. This session:
1. Imports both approved SIA Tower GLBs into a single Blender scene
2. Sets up 3 camera positions matching Scenes 1, 2, and 3 from the Scroll Journey
3. Renders a verification frame for each scene
4. Evaluates whether the tower reads correctly at each camera angle
5. Documents any issues that need fixing before Phase 2 begins

If something looks wrong (scale, proportions, darkness, silhouette), we fix it NOW — not
after 11 more districts are built to the same standard.

## READ THESE FILES FIRST

Before doing anything, read all five of these files completely:
1. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/MASTER-CONTEXT.md`
2. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/SCROLL-JOURNEY.md`
3. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/SPEC.md`
4. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/REVIEW.md`
5. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/QUALITY-RUBRIC.md`

## APPROVED ASSETS

Both SIA Tower GLBs are production-approved and ready for import:

| Asset | Path | Tris | Size |
|-------|------|------|------|
| Exterior | `modules/00-sia-tower/exterior/approved/sia-tower-ext.glb` | 6,956 | 47 KB |
| Interior | `modules/00-sia-tower/interior/approved/sia-tower-int.glb` | 2,626 | 82 KB |

The exterior GLB includes: Base Platform, Tower Glass, Tower Ledges, Crown, Spire,
Exoskeleton, Energy Rings (x10), Junction Ring, Entrance Arch, Ground Veins, Holo Mark,
Crown Beacon — 12 objects total.

The interior GLB includes: Floor, Wall, Ceiling (with oculus), City Model cluster (14 objects),
Data Panels (3), Platforms (3), Light Bridges (3), Corridors (33 objects — 11 frames x 3 parts),
AI Orbs (4), Particles (18) — 81 mesh objects + 4 empties (light_0, light_1, light_2,
camera_target).

## AESTHETIC IDENTITY (same as all sessions)

- Inspiration: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz
- NOT: Lego proportions, neon overload, photorealism, daytime, cartoon
- Night scene, ink-blue sky (#0A0A0F), warm amber fog
- Dark sophistication: base surfaces are #1E1E28, never pure black #000000
- SIA Tower is a 100+ floor dark glass monolith — the tallest structure by 2.5x

## SIA TOWER DIMENSIONS (For Reference)

| Element | Value |
|---------|-------|
| Tower base platform | Z = 0 to Z = 4 |
| Tower body | Z = 4 to Z = 44 (tapered 7x7 → 5x5) |
| Crown | Z = 44 to Z = 50.5 |
| Beacon | Z = 50.5 to Z = 63 |
| Total height | 63 units |
| Interior atrium | Cylinder r=3.0, Z=4 to Z=42 |
| Interior focal point | (0, 0, 19.2) |
| Entrance | -Y face, Z=4 to Z=6 |
| City position | Absolute center (0, 0, 0) |

## THE 3 SCENES TO VERIFY

### Scene 1 — The Civilization Revealed (0% scroll)

**What the viewer sees**: Ultra-wide aerial shot slowly descending. The entire city should
be visible — but right now only SIA Tower exists. That's fine. What matters is that the tower
reads as a dominant landmark from a high wide angle.

**Camera setup**:
- Position: (0, -120, 80) — high and far back, looking down at the city
- Look-at: (0, 0, 25) — roughly mid-tower height
- FOV: 45 degrees
- The camera is distant — the tower should be a small but powerful silhouette

**What must read**:
- [x] Tower silhouette is identifiable even at this distance
- [x] Crown and beacon create a unique roofline
- [x] Ground veins visible radiating from base (even faintly)
- [x] The scene feels vast and empty (intentionally — districts fill in later)
- [x] Dark night atmosphere with warm amber accent

**Save to**: `assembly/screenshots/scene-01-aerial-hero.png`

### Scene 2 — SIA Tower Exterior (7% scroll)

**What the viewer sees**: Ground-level looking up at the SIA Tower. The tower dominates the
frame. This is the power reveal — the viewer feels small beside a 100+ floor monolith.

**Camera setup**:
- Position: (5, -15, 3) — street level, slightly off-axis
- Look-at: (0, 0, 35) — looking up toward the crown
- FOV: 55 degrees (slightly wide for dramatic perspective)

**What must read**:
- [x] Tower dominates the frame — feels massive and powerful
- [x] Entrance archway visible on -Y face (Z=4-6)
- [x] Exoskeleton lattice wrapping the body
- [x] Energy rings visible on the facade
- [x] Crown and beacon visible at the top
- [x] Holo SIA mark visible above entrance
- [x] Ground veins radiating from base
- [x] Ground-up perspective creates a sense of monumental scale

**Save to**: `assembly/screenshots/scene-02-exterior-ground-up.png`

### Scene 3 — Inside SIA Tower / Neural Core (13% scroll)

**What the viewer sees**: Camera pushes through the entrance, rises through the atrium.
The holographic city model floats at the center. This is the wonder moment.

For this scene we need the INTERIOR GLB. The camera starts near ground level at the entrance
and rises to reveal the full atrium space.

**Camera setup — two verification angles**:

**3a. Entrance push-through** (start of scene):
- Position: (0, -2.0, 5.5) — just inside the -Y entrance, slightly above floor
- Look-at: (0, 0, 19.2) — looking up toward the city model
- FOV: 65 degrees

**3b. Rising atrium reveal** (mid-scene):
- Position: (1.0, -1.0, 15.0) — rising, offset from center
- Look-at: (0, 0, 22) — looking up past the city model toward the oculus
- FOV: 60 degrees

**What must read**:
- [x] Cylindrical atrium walls enclose the space
- [x] Holographic city model clearly visible as the hero focal point
- [x] Corridor entrances visible at ground level
- [x] Platforms and light bridges create vertical rhythm
- [x] Data panels visible on upper walls
- [x] AI orbs and particles add atmosphere
- [x] Oculus opening at ceiling lets light in
- [x] Overall mood: dark cathedral to AI, warm holographic glow at center

**Save to**:
- `assembly/screenshots/scene-03a-entrance-push.png`
- `assembly/screenshots/scene-03b-atrium-rising.png`

## WORKFLOW

Follow this exact sequence. Do not skip steps.

### Step 1: Scene Setup

1. Clear the Blender scene completely
2. Run the lighting rig: `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/lighting-rig.py`
3. Set world background to ink-blue (#0A0A0F)
4. Set render engine to EEVEE with bloom enabled

### Step 2: Import Exterior GLB

1. Import: `modules/00-sia-tower/exterior/approved/sia-tower-ext.glb`
2. Verify the tower is centered at origin (0, 0, 0)
3. If not centered, move the root empty to (0, 0, 0)
4. Verify total height reaches ~63 units (beacon tip)
5. Take a viewport screenshot to confirm import

### Step 3: Scene 1 Verification (Aerial Hero)

1. Create a camera named `Cam_Scene_01`
2. Position at (0, -120, 80), looking at (0, 0, 25), FOV 45
3. Set as active camera
4. Render and save to `assembly/screenshots/scene-01-aerial-hero.png`
5. Evaluate: Does the tower read as a dominant city landmark from this distance?

**If it doesn't read**:
- Tower too small at this distance → Consider reducing camera distance to (0, -80, 60)
- Silhouette lost → Increase beacon emission or add a subtle world fog
- Too dark to see anything → Adjust lighting rig sun angle

### --- CHECKPOINT 1 ---
**Show the Scene 1 render. Does the tower read at this aerial distance?**

### Step 4: Scene 2 Verification (Exterior Ground-Up)

1. Create a camera named `Cam_Scene_02`
2. Position at (5, -15, 3), looking at (0, 0, 35), FOV 55
3. Set as active camera
4. Render and save to `assembly/screenshots/scene-02-exterior-ground-up.png`
5. Evaluate: Does the tower feel like a 100+ floor monolith from ground level?

**If it doesn't read**:
- Doesn't feel tall enough → Move camera closer to the base, decrease FOV to 45
- Entrance not visible → Rotate camera slightly toward -Y face
- Too dark / can't see detail → Add a subtle warm fill light at camera position
- Exoskeleton not visible → Boost accent emission slightly for verification

### --- CHECKPOINT 2 ---
**Show the Scene 2 render. Does the tower dominate the frame and feel massive?**

### Step 5: Import Interior GLB

1. Import: `modules/00-sia-tower/interior/approved/sia-tower-int.glb`
2. The interior should align with the exterior — the atrium lives inside the tower body
3. Verify the interior root is positioned so that:
   - Interior floor (Z=4) aligns with the tower body base (Z=4)
   - Interior walls (r=3.0) sit inside the tower body footprint
   - Interior entrance (-Y) aligns with exterior entrance arch (-Y)
4. Take a viewport screenshot showing both exterior and interior together

**Alignment check**: The interior cylinder (r=3.0) fits inside the tower body (7x7 base).
Both share the same origin (0, 0, 0). If both GLBs were exported with origin at (0, 0, 0),
they should overlap correctly by default.

### Step 6: Add Interior Preview Lighting

The exterior lighting rig does NOT illuminate enclosed interiors. For Scene 3 verification,
add temporary interior lights:

Run the interior lighting rig:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/interior-lighting-rig.py`

Call:
```python
import interior_lighting_rig
interior_lighting_rig.setup_interior_lighting(
    focal_point=(0, 0, 19.2),
    floor_z=4.0,
    ceiling_z=42.0,
    radius=3.0,
)
interior_lighting_rig.boost_emissions_for_preview()
```

This adds point/area/spot lights inside the atrium and boosts emission values to
preview levels so the interior is visible in EEVEE renders. These lights do NOT affect
the GLB exports — they are Blender-only.

### Step 7: Scene 3a Verification (Entrance Push-Through)

1. Create a camera named `Cam_Scene_03a`
2. Position at (0, -2.0, 5.5), looking at (0, 0, 19.2), FOV 65
3. Set as active camera
4. Render and save to `assembly/screenshots/scene-03a-entrance-push.png`
5. Evaluate: Can you see the city model glowing ahead as you enter the atrium?

**If it doesn't read**:
- City model not visible → Boost holo/emissive emission strengths
- Walls invisible → Add more wall-wash lights or boost base emission
- Corridor frames lost → They're subtle — acceptable if the overall space reads
- Too bright → Reduce interior key light energy

### Step 8: Scene 3b Verification (Rising Atrium Reveal)

1. Create a camera named `Cam_Scene_03b`
2. Position at (1.0, -1.0, 15.0), looking at (0, 0, 22), FOV 60
3. Set as active camera
4. Render and save to `assembly/screenshots/scene-03b-atrium-rising.png`
5. Evaluate: Does the atrium reveal feel like ascending through a dark cathedral?

**If it doesn't read**:
- No vertical drama → Try wider FOV (70) or lower camera position
- City model too small → Move camera closer to center axis
- Can't see oculus → Tilt camera look-at higher (0, 0, 35)
- Platforms/bridges invisible → Boost detail emission slightly

### --- CHECKPOINT 3 ---
**Show both Scene 3 renders. Does the interior feel like an AI cathedral?**

### Step 9: Transition Test (Exterior → Interior Continuity)

This is a CRITICAL verification. In the scroll experience, the camera moves smoothly from
Scene 2 (ground level, looking up) to Scene 3 (pushing through the entrance). The viewer
must NOT feel a jarring cut.

Create a transition camera path:
1. Camera `Cam_Transition` at (0, -12, 4), looking at (0, 0, 19.2), FOV 55
   - This is mid-approach: viewer is walking toward the entrance
2. Render and save to `assembly/screenshots/scene-02-to-03-transition.png`
3. Evaluate: From this position, can you see:
   - The entrance archway framing the view?
   - A hint of the interior glow through the entrance?
   - The tower body rising above?

**If the transition breaks**:
- Entrance too small to see interior → May need to widen the entrance arch in a fix session
- No interior glow visible from outside → Boost interior emission or add an emissive
  element just inside the entrance (visible from outside)
- Exterior and interior feel like different scenes → Alignment issue, check GLB positions

### --- CHECKPOINT 4 ---
**Show the transition render. Is there visual continuity from exterior to interior?**

### Step 10: Scale Sanity Check

With both GLBs imported, verify proportional sanity:

1. Check tower total height: should be ~63 units (base to beacon tip)
2. Check interior atrium height: should be 38 units (Z=4 to Z=42)
3. Check the interior fits inside the exterior footprint
4. Check that the interior floor aligns with the exterior base
5. Take a wireframe/X-ray viewport screenshot showing both models overlapping

If there are scale or alignment mismatches, document them precisely — they will need to
be fixed in the GLB export settings.

**Save to**: `assembly/screenshots/session05-alignment-xray.png`

## QUALITY GATES (Session 5 — Integration Test)

### Gate 6 — Cohesion Check (Partial — SIA Tower Only)

With only one structure, this is a limited check. But verify:
- [ ] Tower reads correctly at 3 different distances (aerial, mid, ground)
- [ ] Dark-first aesthetic holds across all camera angles
- [ ] No unintended bright spots or material issues visible at render resolution
- [ ] Exterior and interior assets are spatially compatible (overlap correctly)

### Scene Readability Check

For each scene render, grade on a 1-5 scale:

| Scene | Criterion | Score |
|-------|-----------|-------|
| Scene 1 | Tower identifiable as a landmark at aerial distance | /5 |
| Scene 1 | Unique silhouette (crown + beacon) reads clearly | /5 |
| Scene 2 | Tower feels like 100+ floor monolith from ground | /5 |
| Scene 2 | Architectural detail visible (exoskeleton, rings, arch) | /5 |
| Scene 3a | Interior space reads as an enclosed atrium | /5 |
| Scene 3a | City model is clearly the focal point | /5 |
| Scene 3b | Vertical drama present (cathedral effect) | /5 |
| Scene 3b | Multiple interior elements visible (platforms, panels, particles) | /5 |
| Transition | Visual continuity from exterior to interior | /5 |

**Pass threshold**: All scores must be 3/5 or higher. Any score below 3 triggers a fix task.

## RENDER SETTINGS

Use EEVEE for all verification renders:

```python
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.film_transparent = False
scene.eevee.use_bloom = True
scene.eevee.bloom_threshold = 0.8
scene.eevee.bloom_intensity = 0.3
```

## OUTPUT FILES

All screenshots go to the assembly directory (this is a city-level verification, not a
module-level screenshot):

```
assembly/screenshots/
├── scene-01-aerial-hero.png
├── scene-02-exterior-ground-up.png
├── scene-02-to-03-transition.png
├── scene-03a-entrance-push.png
├── scene-03b-atrium-rising.png
└── session05-alignment-xray.png
```

## WHAT TO SAVE

1. Save the Blender scene with all cameras and both imported GLBs:
   `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/assembly/drafts/integration-test-session05.blend`
2. This .blend becomes the seed for the Phase 6 full assembly scene

## FIX LOG

Document any issues found during verification. Each issue gets a severity and fix plan:

| Issue | Severity | Fix Plan | Session |
|-------|----------|----------|---------|
| (fill in during session) | Critical / Medium / Minor | Description | Which session fixes it |

**Critical**: Must fix before starting Phase 2
**Medium**: Fix in a dedicated patch session before Phase 6 assembly
**Minor**: Acceptable for now, revisit during Phase 6 polish

## WHAT NOT TO DO

- No new geometry creation — this is a verification session
- No modifications to the approved GLBs (they are production assets)
- No R3F code — that's Phase 7
- No district modeling — Phase 2 starts after this verification passes
- No energy pipelines — Phase 5
- Do NOT join, decimate, or re-export the GLBs
- Do NOT worry about empty city around the tower — districts fill in later

## AFTER SESSION 5

When this session is complete:

1. All 5 scene verification renders are saved to `assembly/screenshots/`
2. Fix log documents any issues with severity ratings
3. The integration .blend is saved to `assembly/drafts/`
4. REVIEW.md Gate 6 is updated (partial — SIA Tower cohesion)
5. If all scenes score 3/5+: **Phase 1 is COMPLETE — proceed to Phase 2**
6. If any scene scores below 3: schedule a fix session before Phase 2

### What Phase 2 Looks Like

Phase 2 builds the first 3 districts (Fitness, Yoga, Finance). Each district follows the
same workflow: Exterior sessions → Review → Interior session → Review → Integration test.
The SIA Tower integration .blend from this session becomes the baseline — each new district
gets added and verified against it.

## SESSION ROADMAP (For Reference)

| Session | Focus | Status |
|---------|-------|--------|
| 1 | Exterior — Major Forms | DONE |
| 2 | Exterior — Architectural Detail | DONE |
| 3 | Exterior — Polish, Holo Mark, Export GLB | DONE (Approved) |
| 4 | Interior — Neural Core Atrium | DONE (Approved) |
| **→ 5** | **Integration Test — Scene 1/2/3 Camera Verification** | **NOW** |
| 6+ | Phase 2 — First 3 Districts (Fitness, Yoga, Finance) | Queued |
