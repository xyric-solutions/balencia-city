# Balencia City v3 — Session 4: SIA Tower Interior (Neural Core Atrium)

## CONTEXT

You are building the INTERIOR of the SIA Life Coach Tower — the Neural Core Atrium. This is
the heart of the entire Balencia City: a vast cylindrical space where all 11 district pipelines
converge. The camera enters this space during Scene 3 of the 17-scene scroll journey, making
it one of the most visually important moments in the experience.

The SIA Tower exterior is APPROVED (Session 3, 2026-05-22). The exterior GLB is at:
`modules/00-sia-tower/exterior/approved/sia-tower-ext.glb`

Session 4 builds the complete interior in one session. The Neural Core Atrium is a cylindrical
room with a floating holographic city model at its center, observation platforms at multiple
heights, and 11 corridor entrances at ground level radiating outward to each district.

This session will:
1. Build the cylindrical room shell (floor, walls, ceiling with oculus opening)
2. Build the central holographic city model (focal point)
3. Add 6 supporting props (data panels, platforms, corridors, orbs, particles, light bridges)
4. Place 3 light empties and 1 camera target empty
5. Run Quality Rubric (Gates 3-5, 7) and fix any failures
6. Export the approved interior GLB

## READ THESE FILES FIRST

Before doing anything, read all four of these files completely:
1. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/MASTER-CONTEXT.md`
2. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/SPEC.md`
3. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/export-pipeline.py`
4. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/QUALITY-RUBRIC.md`

## START FRESH

This is a NEW Blender scene — do NOT open the exterior .blend file. Start clean.

1. Clear the Blender scene completely
2. Run the lighting rig: `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/lighting-rig.py`
3. Run the material library: `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/material-library.py`
   Call: `create_materials("#FF5E00", include_energy=True, include_holo=True)`

## AESTHETIC IDENTITY (same as exterior sessions)

- Inspiration: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz
- NOT: Lego proportions, neon overload, photorealism, daytime, cartoon
- Night scene mood even indoors — dark walls lit by focal glow and accent uplighting
- Dark sophistication: base surfaces are #1E1E28, never pure black #000000
- The atrium is a dark cylindrical chamber with warm holographic light at its center —
  a cathedral to AI, not a brightly-lit office lobby

## INTERIOR DIMENSIONS

The interior exists INSIDE the tower body, which spans Z=4 to Z=44 with a footprint
tapering from 7x7 (bottom) to 5x5 (top). The interior atrium is cylindrical:

| Element | Value | Notes |
|---------|-------|-------|
| Atrium shape | Cylinder | Centered at origin (0, 0) |
| Atrium radius | 3.0 | Fits inside the 7x7→5x5 tower body (min inner hw = 2.5, so r=3.0 at base tapering) |
| Floor level | Z = 4.0 | Same as tower body base |
| Ceiling level | Z = 42.0 | 2 units below the crown transition at Z=44 |
| Atrium height | 38 units | ~95 floors worth of vertical space |
| Wall segments | 24-32 | Enough to read as cylindrical at viewport scale |
| Open wall/oculus | One section of ceiling is an open oculus or one wall section is windowed | Lets exterior light in; connects interior to city visually |

Use these Z heights for vertical element placement:
- Ground level: Z = 4.0 (floor)
- Lower third: Z = 4 to Z = 16.7
- Middle third (city model zone): Z = 16.7 to Z = 29.3
- Upper third: Z = 29.3 to Z = 42.0
- City model center: Z ≈ 19.2 (40% of atrium height above floor: 4 + 0.4 × 38 = 19.2)

## WHAT TO BUILD (THIS SESSION)

Build all elements in this order. Each subsection includes geometry specs, material, and
object naming.

### 1. Room Shell (Floor + Cylinder Wall + Ceiling)

The atrium enclosure. Three objects:

**1a. Floor Disc**
- Circular disc at Z = 4.0
- Radius: 3.0 (matches atrium)
- Segments: 32
- Material: `base`
- Object name: `INT_Floor`
- Estimated tris: ~60

**1b. Cylindrical Wall**
- Open cylinder (no caps) from Z = 4.0 to Z = 42.0
- Radius: 3.0, segments: 32
- Normals face INWARD (we're inside the cylinder looking in)
- Material: `base`
- Object name: `INT_Wall`
- Estimated tris: ~128 (32 segments × 1 ring × 2 tris/quad, or add 2-3 height subdivisions for ~256)

**1c. Ceiling with Oculus**
- Circular disc at Z = 42.0 with a central hole (oculus)
- Outer radius: 3.0, inner radius (oculus): 1.0
- The oculus lets warm light from above filter down onto the city model
- Segments: 32
- Material: `base`
- Object name: `INT_Ceiling`
- Estimated tris: ~128

**Room shell total: ~350-450 tris**

### 2. Central Holographic City Model (FOCAL POINT)

This is the hero element — a miniature holographic representation of the entire Balencia
City floating at the center of the atrium. Since we can't model all 12 buildings in
miniature within our tri budget, create an ABSTRACT representation:

**Geometry**: A cluster of geometric shapes suggesting a miniature city:
- One tall central spire (representing SIA Tower) — a thin tapered hex prism, ~2 units tall
- 6-8 smaller blocks/prisms at varying heights arranged in a ring around it (representing
  districts) — simple box geometry, heights 0.5-1.2 units
- A circular base disc beneath the cluster (the "holographic platform")
- The whole assembly should be ~3 units tall and ~2.5 units wide

**Position**: Centered at (0, 0, 19.2) — 40% up the atrium height

**Material**:
- Mini city blocks: `holo` (semi-transparent, orange glow)
- Central mini-spire: `emissive` (brighter glow to draw the eye)
- Platform disc: `glass` (dark, reflective base)

**Object name**: `INT_City_Model` (can be one joined object or a few)
**Estimated tris**: 300-600

### 3. Holographic Data Panels (3-4 curved screens on walls)

Large curved panels mounted on the cylindrical wall, displaying (in the final app)
district status information. For the GLB, these are simple curved plane geometry.

**Geometry**: 4 curved rectangular planes, each:
- Width: ~1.5 units (subtending ~30° of the cylinder)
- Height: ~4 units tall
- Slight concave curve matching the cylinder wall radius
- Offset 0.15 units inward from the wall (floating in front of it)

**Positions**: Evenly distributed around the cylinder at 90° intervals:
- Panel 1: facing +X (at Y=0, X=+2.85)
- Panel 2: facing +Y (at X=0, Y=+2.85)
- Panel 3: facing -X (at Y=0, X=-2.85)
- Panel 4: facing -Y (at X=0, Y=-2.85) — skip this one if it conflicts with the
  entrance corridor below; use 3 panels instead

**Z position**: Center each panel at Z ≈ 28 (upper third, above the city model)

**Material**: `holo` (semi-transparent holographic screens)
**Object name**: `INT_Data_Panels`
**Estimated tris**: 100-200 (4 panels × ~6 tris each, or more if subdivided for curvature)

### 4. Floating Observation Platforms (3 disc platforms at different heights)

Simple circular disc platforms at three different heights, giving vertical rhythm to the
atrium. In the final app, these have characters standing on them.

**Geometry**: 3 flat circular discs:
- Radius: 0.6-0.8 units each
- Thickness: 0.08 units (thin slab)
- Segments: 12-16

**Positions** (offset from center so they don't obscure the city model):
- Platform 1 (lowest): position (1.5, 0.8, 10) — lower third
- Platform 2 (middle): position (-1.0, 1.5, 22) — near city model height
- Platform 3 (highest): position (0.5, -1.2, 34) — upper third

**Material**: `detail` (structural dark metal)
**Object name**: `INT_Platforms`
**Estimated tris**: ~100

### 5. Corridor Entrance Frames (11 arched doorways at ground level)

11 arched doorway frames radiating outward from the atrium at ground level. Each represents
the entrance to a district's energy pipeline corridor. In the final R3F app, each frame
glows in its district color; for the GLB export, all use the `detail` material.

**Geometry**: Each corridor entrance is a simple arch shape:
- Width: ~0.8 units
- Height: ~2.0 units (from Z=4.0 to Z=6.0)
- Depth: 0.15 units (thin frame)
- Shape: Two vertical pillars + a semicircular arch top (or simple rectangle for budget)

**Positions**: Distributed evenly around the cylinder perimeter at ground level:
- 11 entrances at angles: 0°, 32.7°, 65.5°, 98.2°, 130.9°, 163.6°, 196.4°, 229.1°,
  261.8°, 294.5°, 327.3° (360° / 11 = 32.73° spacing)
- Each placed at radius 2.85 (just inside the wall), oriented radially outward
- One entrance should align with the -Y axis (matching the exterior entrance archway)

**Material**: `detail`
**Object name**: `INT_Corridors`
**Estimated tris**: 400-800 (11 frames × ~40-70 tris each)

### 6. Purple AI Orbs (3-4 floating spheres)

Small glowing spheres representing AI consciousness nodes, drifting at varying heights
throughout the atrium. Simple UV spheres.

**Geometry**: 4 UV spheres, radius 0.12-0.18 each, segments 8 (low-poly sphere)
**Positions**: Scattered asymmetrically:
- Orb 1: (0.8, 0.5, 12)
- Orb 2: (-0.6, -0.9, 24)
- Orb 3: (0.3, 1.1, 30)
- Orb 4: (-1.0, 0.2, 17)

**Material**: `emissive` — NOTE: In the final app these will be overridden to purple
(#7F24FF). For the GLB export, use the standard `emissive` material (burnt orange).
The R3F runtime handles the color swap.

**Object name**: `INT_AI_Orbs`
**Estimated tris**: ~200 (4 × ~50 tris per low-poly sphere)

### 7. Particle Emitter Zone (Vertical column of tiny spheres)

A vertical column of tiny spheres representing the rising particle effect — orange/amber
points of light ascending continuously. In the final app this is a particle system; for
the GLB we create placeholder geometry.

**Geometry**: A vertical column of 15-20 tiny spheres (radius 0.04-0.06):
- Scattered within a cylinder of radius 0.8, from Z = 5 to Z = 40
- Random-ish X/Y positions within the radius, evenly-ish distributed vertically
- Use icospheres (subdivision 1) for minimal tri count

**Position**: Centered roughly at (0, 0) — the central vertical axis

**Material**: `emissive`
**Object name**: `INT_Particles`
**Estimated tris**: ~300-500 (20 icospheres × ~20 tris each)

### 8. Light Bridges (Connecting floating platforms)

Thin glowing flat strips connecting the 3 observation platforms, creating visual pathways
through the vertical space.

**Geometry**: 3 flat rectangular strips:
- Width: 0.3 units
- Thickness: 0.02 units (paper-thin)
- Length: varies (straight line between connected platforms)

**Connections**:
- Bridge 1: Platform 1 (1.5, 0.8, 10) → Platform 2 (-1.0, 1.5, 22)
- Bridge 2: Platform 2 (-1.0, 1.5, 22) → Platform 3 (0.5, -1.2, 34)
- Bridge 3: Platform 3 (0.5, -1.2, 34) → Platform 1 (1.5, 0.8, 10) — completing the loop

**Material**: `emissive`
**Object name**: `INT_Light_Bridges`
**Estimated tris**: ~36 (3 bridges × 4 quads × 2 tris + some cap faces)

### 9. Light Empties (3 empties — marker positions for R3F lighting)

These are Empty objects (not meshes) that mark where dynamic lights should be placed at
runtime. They are NOT exported as geometry — they export as nodes in the GLB hierarchy.

**Empties**:
- `light_0`: Position (0, 0, 19.2) — center of atrium at city-model height. Warm key.
- `light_1`: Position (0, 0, 40.0) — upper atrium near ceiling. Cool fill from above.
- `light_2`: Position (0, -2.5, 5.0) — ground level near -Y corridor entrance. Orange accent.

**Type**: Plain Axes, display size 0.5
**These are Empties, NOT lights** — do not create Light objects for these.

### 10. Camera Target Empty

One empty marking the camera's focal point in the R3F app.

**Position**: (0, 0, 19.2) — same as light_0, at the center of the city model
**Name**: `camera_target`
**Type**: Plain Axes, display size 0.3

## WORKFLOW

Follow this exact sequence. Do not skip steps.

### Step 1: Scene Setup
- Clear the Blender scene
- Run lighting rig and material library (with `include_energy=True, include_holo=True`)
- Verify all 7 materials exist: base, accent, glass, detail, emissive, energy, holo
- Take a screenshot to confirm clean starting state

### Step 2: Build Room Shell
- Create INT_Floor (disc at Z=4)
- Create INT_Wall (open cylinder Z=4 to Z=42, normals inward)
- Create INT_Ceiling (annular disc at Z=42 with oculus hole r=1.0)
- Assign `base` material to all three
- Take a screenshot from inside the cylinder looking up

### Step 3: Build the City Model (Focal Point)
- Create the abstract miniature city cluster at (0, 0, 19.2)
- Central mini-spire + 6-8 surrounding blocks + platform disc
- Assign `holo` to blocks, `emissive` to central spire, `glass` to platform
- This is the HERO — it should feel like a glowing holographic diorama floating in darkness
- Take a screenshot showing the city model from a 3/4 angle inside the atrium

### --- CHECKPOINT 1 ---
**Take viewport screenshot from inside the atrium looking at the city model.**
The room shell should create a dark cylindrical enclosure. The city model should float
at center, glowing warm orange through the holo/emissive materials. The oculus above
should create a circle of light on the ceiling.

### Step 4: Add Data Panels
- Create 3-4 curved holographic panels on the upper wall area
- Assign `holo` material
- Verify they float slightly in front of the wall

### Step 5: Add Observation Platforms + Light Bridges
- Create 3 disc platforms at different heights
- Create 3 thin bridges connecting them
- Assign `detail` to platforms, `emissive` to bridges

### Step 6: Add Corridor Entrances
- Create 11 arched frames at ground level, evenly spaced around the cylinder
- Align one entrance with the -Y axis (exterior entrance)
- Assign `detail` material

### Step 7: Add AI Orbs + Particle Column
- Create 4 small spheres at scattered positions
- Create 15-20 tiny icospheres in a vertical column at center
- Assign `emissive` to both

### --- CHECKPOINT 2 ---
**Take viewport screenshot from inside the atrium, positioned at ground level looking up.**
All elements should be visible: room shell, city model glowing at center, data panels
on walls, platforms with bridges, corridor entrances at the base, orbs floating,
particles rising vertically.

### Step 8: Place Empties
- Create light_0 at (0, 0, 19.2) — city model height
- Create light_1 at (0, 0, 40.0) — upper atrium
- Create light_2 at (0, -2.5, 5.0) — ground level
- Create camera_target at (0, 0, 19.2)
- All as Plain Axes empties (NOT light objects)

### Step 9: Quality Gate Verification

Run through each gate. State PASS or FAIL with evidence.

**Gate 3 — Material System Compliance**
- [ ] All mesh objects have materials from the 7-slot set
- [ ] No unnamed or rogue materials
- [ ] Verify each object → material mapping:

| Object | Material |
|--------|----------|
| INT_Floor | base |
| INT_Wall | base |
| INT_Ceiling | base |
| INT_City_Model (blocks) | holo |
| INT_City_Model (spire) | emissive |
| INT_City_Model (platform) | glass |
| INT_Data_Panels | holo |
| INT_Platforms | detail |
| INT_Corridors | detail |
| INT_AI_Orbs | emissive |
| INT_Particles | emissive |
| INT_Light_Bridges | emissive |

**Gate 4 — Dark-First Test**
- [ ] Set ALL emission strengths to 0
- [ ] Take a screenshot — room shell, platforms, corridors should still read as architecture
- [ ] No surface is bright when inactive
- [ ] Restore all emissions after test

Emission restore values:
- accent: 0.24, glass: 0.08, emissive: 0.20, energy: 0.10, holo: 0.50

**Gate 5 — Technical Budget**
- [ ] Total triangles within 10K-15K
- [ ] All transforms applied (Ctrl+A)
- [ ] Origin at bottom-center
- [ ] No cameras or lights in export (empties are OK)

**Gate 7 — Interior-Specific**
- [ ] Clear focal point: central city model is unmistakably the hero element
- [ ] Light empties at logical positions: light_0 at focal, light_1 above, light_2 ground
- [ ] camera_target empty at focal point (0, 0, 19.2)
- [ ] 4-8 props present, each identifiable (data panels, platforms, corridors, orbs, particles, bridges = 6)
- [ ] Complete room shell (floor + wall + ceiling with oculus opening)
- [ ] Interior materials use same 7-slot system as exterior

### --- CHECKPOINT 3 ---
**Report gate results: PASS/FAIL for each gate (3, 4, 5, 7).**
If any gate FAILS, fix the issue before proceeding. After fixing, re-run ALL gates.

### Step 10: Pre-Export Preparation
1. Apply all transforms on every mesh object
2. Clean up any stray geometry
3. Verify empties are named correctly (light_0, light_1, light_2, camera_target)
4. Save the .blend file FIRST (export is destructive):
   `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/interior/drafts/sia-tower-int-session04.blend`

### Step 11: GLB Export

Use the export pipeline. Note the interior-specific budget:

```python
import sys
sys.path.insert(0, "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared")
import export_pipeline

export_pipeline.export_glb(
    output_path="/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/interior/approved/sia-tower-int.glb",
    root_name="sia-tower-int",
    max_tris=15000,
    max_size_kb=300,
)
```

**IMPORTANT**: Save the .blend BEFORE running the export pipeline. The pipeline removes
cameras/lights and reparents objects, modifying the scene destructively.

**NOTE for Blender 4.x/5.x**: If the export pipeline's `export_glb()` function fails due
to deprecated glTF parameters, run the pipeline steps manually:
1. Apply transforms
2. Remove cameras and lights (keep empties!)
3. Set origins to bottom-center
4. Parent under root empty
5. Verify materials
6. Export GLB with: `bpy.ops.export_scene.gltf(filepath=..., export_format='GLB', export_draco_mesh_compression_enable=True, export_draco_mesh_compression_level=6, export_yup=True, export_normals=True, export_materials='EXPORT', export_cameras=False, export_lights=False)`

After export, verify:
- [ ] GLB file exists in `interior/approved/`
- [ ] File size is under 300 KB
- [ ] Triangle count is under 15,000
- [ ] No warnings from material verification
- [ ] Empties (light_0, light_1, light_2, camera_target) are included in the GLB hierarchy

### --- CHECKPOINT 4 ---
**Report: GLB file path, triangle count, file size in KB.**

### Step 12: Final Screenshots

Save final screenshots from inside the atrium:

1. **Overview interior** (camera at (2, -2, 14), looking at city model)
   - Shows room shell, city model, corridor entrances, ground-level perspective
   - Save to: `modules/00-sia-tower/screenshots/session04-interior-overview.png`

2. **City model close-up** (camera at (1, -1, 19), looking at (0, 0, 19.2))
   - Hero shot of the holographic city model floating in the dark atrium
   - Save to: `modules/00-sia-tower/screenshots/session04-interior-city-model.png`

3. **Looking up** (camera at (0, 0, 5), looking straight up toward oculus)
   - Vertical drama: platforms, bridges, data panels, particles rising, oculus at top
   - Save to: `modules/00-sia-tower/screenshots/session04-interior-looking-up.png`

4. **Ground level corridor view** (camera at (0, -2.5, 5.5), looking at -Y corridor entrance)
   - Shows corridor frame, city model above, other entrances visible
   - Save to: `modules/00-sia-tower/screenshots/session04-interior-corridor.png`

### Step 13: Save Final .blend

Save the Blender file (WITH lighting and materials, before export strips them):
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/interior/drafts/sia-tower-int-session04.blend`

### Step 14: Update REVIEW.md

Update the Interior Review section in `modules/00-sia-tower/REVIEW.md`:
- Check off Gates 3, 4, 5, 7 as PASS (with evidence)
- Set Interior Approved with today's date
- Add Session 4 details (object count, tri count, GLB size)

## QUALITY GATES (Session 4 — Interior)

Before ending this session, verify ALL of these:

- [ ] **Gate 3 — Materials**: All objects use correct 7-slot materials. No default gray.
      No unnamed materials. Mapping matches table above exactly.
- [ ] **Gate 4 — Dark-First**: With emissions at 0, room shell and props read as architecture.
      City model is visible as geometry even without glow. No bright surfaces when inactive.
- [ ] **Gate 5 — Technical**: Triangle count under 15K. GLB under 300 KB. Origin at
      bottom-center. Transforms applied. No cameras/lights exported (empties are OK).
- [ ] **Gate 7 — Interior**: Clear focal point (city model). Light empties at logical
      positions. camera_target at focal point. 6 identifiable props. Complete room shell
      with oculus opening.

## TRIANGLE BUDGET BREAKDOWN

| Object | Material | Estimated Tris | Purpose |
|--------|----------|---------------|---------|
| `INT_Floor` | `base` | ~60 | Circular floor disc |
| `INT_Wall` | `base` | ~256 | Cylindrical wall (normals inward) |
| `INT_Ceiling` | `base` | ~128 | Ceiling with oculus hole |
| `INT_City_Model` | `holo`/`emissive`/`glass` | 300-600 | Central holographic city (focal point) |
| `INT_Data_Panels` | `holo` | 100-200 | 3-4 curved holographic screens |
| `INT_Platforms` | `detail` | ~100 | 3 floating observation discs |
| `INT_Corridors` | `detail` | 400-800 | 11 arched entrance frames |
| `INT_AI_Orbs` | `emissive` | ~200 | 4 floating AI spheres |
| `INT_Particles` | `emissive` | 300-500 | 15-20 tiny rising spheres |
| `INT_Light_Bridges` | `emissive` | ~36 | 3 thin connecting strips |

**Estimated total: 1,900-2,900 tris** (well within 15K budget — room for detail)

If you come in well under 5K tris, consider:
- Adding more height subdivisions to the wall for smoother curvature
- Adding more corridor arch detail (semicircular tops)
- Adding a second ring of mini-buildings to the city model
- Adding subtle floor rings/grooves around the corridors

## NAMING CONVENTIONS

All interior objects use the `INT_` prefix to distinguish from exterior `SIA_` objects.

Empties do NOT use a prefix — they use the standard names:
- `light_0`, `light_1`, `light_2`
- `camera_target`

## WHAT NOT TO DO

These belong in other sessions or phases. Do NOT attempt them now:

- No exterior geometry — the exterior is done and approved
- No actual light objects — use empties only (R3F handles lighting at runtime)
- No particle systems or animation — geometry placeholders only
- No texture baking or image textures — the 7-slot system handles all materials
- No per-district corridor coloring — runtime handles color overrides
- No physics or rigid body — static geometry only
- No joining all objects into one mesh — keep them separate for per-object material assignment
- No R3F/Three.js integration (Phase 7)

## AFTER SESSION 4

When this session is complete:
1. The GLB at `interior/approved/sia-tower-int.glb` is the production interior asset
2. Update `REVIEW.md` — check off Gates 3-5, 7, set Interior Approved with today's date
3. The SIA Tower module is now FULLY COMPLETE (exterior + interior both approved)
4. Phase 2 (First 3 districts: Fitness, Yoga, Finance) can begin
5. Energy Pipeline sessions require both SIA Tower and target district to be approved

## SESSION ROADMAP (For Reference)

| Session | Focus | Status |
|---------|-------|--------|
| 1 | Exterior — Major Forms | DONE |
| 2 | Exterior — Architectural Detail | DONE |
| 3 | Exterior — Polish, Holo Mark, Export GLB | DONE (Approved) |
| **-> 4** | **Interior — Neural Core Atrium** | **NOW** |
| 5 | Integration Test — Scene 1/2/3 camera verification | Queued |
