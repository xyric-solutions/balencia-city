# Balencia City v3 — Session 7: Fitness District Exterior (Detail + Polish + Export)

## CONTEXT

You are continuing the FIRST district of Balencia City v3 — the Fitness Gym Megastructure.
Session 6 established the major forms: tapered angular body, three cantilevers, exposed
steel framework, stepped foundation, and rooftop crown. All 5 quality gates passed. The
silhouette is approved — **do NOT change the primary massing or proportions**.

This is Session 7. You will add the detail layer that brings the building to life, polish
every surface, then decimate and export the final GLB. After this session the Fitness
exterior is DONE.

## READ THESE FILES FIRST

Before doing anything, read all four of these files completely:
1. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/MASTER-CONTEXT.md`
2. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/SPEC.md`
3. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/QUALITY-RUBRIC.md`
4. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/export-pipeline.py`

## AESTHETIC IDENTITY (same as all sessions)

- Inspiration: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz
- NOT: Lego proportions, neon overload, photorealism, daytime, cartoon
- Night scene, ink-blue sky (#0A0A0F), warm amber fog
- Dark sophistication: base surfaces are #1E1E28, never pure black #000000
- Fitness district color: Forest Green `#34A853` — used ONLY on emissive/energy slots

## SESSION 6 OUTPUT (What You're Starting From)

Load the Session 6 .blend file:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/exterior/drafts/fitness-session06.blend`

The scene contains 16 mesh objects, 3 lights, and 6 materials. **1,116 triangles** used.
The final exterior budget is **12,000-18,000 tris** — you have ~11,000-17,000 tris to
spend on detail. Do NOT exceed 18,000.

### Existing Geometry (DO NOT MODIFY PROPORTIONS)

| Object | Description | Material |
|--------|-------------|----------|
| `Fitness_Foundation_Step1` | Bottom step, 12x12 | base |
| `Fitness_Foundation_Step2` | Top step, 11x11 | base |
| `Fitness_Body_Glass` | Tapered frustum (10x10 base → 7.6x7.6 top) | glass |
| `Fitness_Body_Ledges` | 12 horizontal ledge bands | base |
| `Fitness_Body_Mullions` | 12 vertical divider strips (3/face) | base |
| `Fitness_Cantilever_F10` | Floor 10, extends ±X, 2.2 units | base + detail (underside) |
| `Fitness_Cantilever_F20` | Floor 20, extends all 4 faces, 2.5 units | base + detail (underside) |
| `Fitness_Cantilever_F30` | Floor 30, extends ±Y, 2.2 units | base + detail (underside) |
| `Fitness_Corner_Columns` | 4 vertical columns at corners | detail |
| `Fitness_Horizontal_Beams` | 12 beams at cantilever heights | detail |
| `Fitness_Roof_Surface` | Flat roof slab | base |
| `Fitness_Mech_Housing_01-04` | 4 rooftop mechanical housings | detail |
| `Fitness_Pipeline_Hardpoint` | Roof center hardpoint | energy |

### Key Dimensions (locked from Session 6)

| Element | Value |
|---------|-------|
| Body base half-width | 5.0 (10x10 footprint) |
| Body top half-width | 3.8 (7.6x7.6 footprint) |
| Body Z range | 0.8 to 12.0 |
| Foundation Z range | 0.0 to 0.8 |
| Cantilever F10 center | Z=4.9, extends ±X by 2.2 |
| Cantilever F20 center | Z=8.9, extends all 4 faces by 2.5 |
| Cantilever F30 center | Z=11.9, extends ±Y by 2.2 |
| Total rooftop Z | ~12.2 |

The taper interpolation formula:
```
hw_at_z = 5.0 + (3.8 - 5.0) * (z - 0.8) / (12.0 - 0.8)
```

## WHAT TO BUILD (THIS SESSION)

Add these 5 detail elements, then polish and export. Every element references the SPEC.md
material assignment table.

### 1. Green Energy Strips (30 Horizontal Emissive Bands)

This is the Fitness District's signature visual feature — forest green energy lines on
every floor edge.

- **30 thin horizontal strips**, one per floor, running the full perimeter of each facade
- Each strip is at the TOP edge of each floor plate (every ~0.37 units from Z=0.8 to Z=12.0)
- Strip dimensions: full face width, ~0.04 units tall, flush with or ~0.02 units proud of wall
- These sit ON TOP of the existing ledge geometry — they are the energy layer
- The strips must follow the body taper (narrower at top, wider at bottom)
- Material: **`emissive`** — this is what makes the building glow green when active
- At inactive state the emissive strips are very subtle (emission_strength 0.06) — they
  should barely register. Do NOT make them bright. The runtime will crank them up.

**Critical**: The strips should create a rhythmic horizontal banding pattern. When you look
at the building, you should count approximately 30 fine lines. They emphasize the building's
stacked, compressed power.

**Triangle budget for strips**: Keep each strip as a single flat quad (2 tris). 30 strips x
4 faces = 120 quads = ~240 tris. Simple is better here.

### 2. Outdoor Athletic Track (Ground Level)

A running track wraps the building perimeter at ground level.

- Flat ring/track surface at Z=0.02 (just above ground plane, below foundation)
- Inner edge: matches or slightly exceeds the foundation footprint (~6.5 units from center)
- Outer edge: ~8.0-8.5 units from center (track width ~1.5-2 units)
- Shape: rectangular with rounded corners, OR simple rectangular ring
- Material for track surface: **`base`** (dark ground surface)
- **Track light lanes**: 2-3 thin lines embedded in the track surface running its length
- Light lane material: **`energy`** — these are orange (#FF5E00) from the SIA pipeline
- Keep the track geometry simple — it's a background element, not a hero piece

**Triangle budget**: Track ring ~24-48 tris. Light lanes ~24-48 tris. Total: ~50-100 tris.

### 3. Triangular Entrance Portal

The entrance is a dramatic architectural statement — two heavy angled beams forming a
triangular opening on the -Y face (front) of the building.

- Two thick beams (~0.4x0.4 cross-section) angling inward from the foundation level to
  meet at approximately Z=4.0 (floor 10 area)
- The beams start at the outer edges of the foundation (-Y face) and lean inward to meet
  at center, forming a triangle/A-frame shape
- The opening between the beams is the entrance — approximately 3-4 units wide at base,
  narrowing to a point at Z=4.0
- Beams should be angular and heavy, not decorative — these are structural
- Material: **`accent`** — faint green emission from edges (0.24 strength)
- Add a small threshold/step at the base of the portal: a flat slab at Z=0.02

**Triangle budget**: 2 beams x ~12 tris + threshold ~12 tris = ~36 tris.

### 4. Trophy / Achievement Display Wall

Near the entrance, an illuminated display panel shows achievement indicators.

- Located on the -Y face (front facade), adjacent to the entrance portal
- One side of the entrance (e.g., +X side of the portal at ground/floor-1 level)
- A flat rectangular panel (~2 units wide x 1.5 units tall) mounted on the facade
- Slightly proud of the wall surface (~0.05 units forward)
- Subdivide the panel into a 3x2 or 4x3 grid of smaller rectangles to suggest individual
  trophy/display slots
- Material: **`emissive`** — green-lit illuminated rectangles
- Keep it simple — this is a detail read, not a hero element

**Triangle budget**: ~24-48 tris.

### 5. Window Frame Detail (All Facades)

The existing mullions and glass body create the panel structure. Add window frame
articulation to make the facade read as individual windows rather than a flat glass wall.

- On each facade, between the existing vertical mullions, add horizontal frame members
  at each floor height (aligned with the existing ledge bands)
- These create a grid pattern: vertical mullions + horizontal frames = window grid
- Each horizontal frame is a thin strip (~0.08 units tall, same depth as mullions)
- This divides each glass panel column into individual floor-height windows
- Material: **`base`** (same as mullions — structural dark metal framing)

**Triangle budget**: 4 faces x ~12 horizontal frames x ~12 tris each = ~576 tris.
This is the largest detail element — manage carefully.

**Alternative (if over budget)**: Add horizontal frames only on the front (-Y) and one
side (+X) face. The back and remaining side are less visible and can stay as-is.

## DIMENSIONS REFERENCE FOR DETAIL PLACEMENT

Use these formulas to position detail elements that follow the body taper:

```python
z_bot = 0.8
z_top = 12.0
hw_bot = 5.0
hw_top = 3.8

def hw_at_z(z):
    t = (z - z_bot) / (z_top - z_bot)
    return hw_bot + (hw_top - hw_bot) * t
```

## WORKFLOW

Follow this exact sequence. The first half adds detail, the second half polishes and
exports. Take viewport screenshots at marked checkpoints.

### Step 1: Load the Session 6 File

1. Open the saved .blend file:
   `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/exterior/drafts/fitness-session06.blend`
2. Verify the scene: 16 mesh objects, 3 lights, 6 materials, ~1,116 tris
3. The lighting rig and materials from Session 6 are already in the file — do NOT recreate them
4. Set viewport to Material Preview mode with scene lights and scene world enabled

### Step 2: Add Green Energy Strips (30 Bands)

- Create 30 thin horizontal quads at each floor height, wrapping all 4 facades
- Each strip follows the body taper at its Z height
- All strips in a single mesh object: `Fitness_Energy_Strips`
- Material: `emissive`
- Verify: from a distance, do you see ~30 fine horizontal green lines on the facade?
  They should be subtle at inactive emission (0.06) but clearly countable

### Step 3: Add the Athletic Track

- Create the ground-level track ring: `Fitness_Athletic_Track`
- Create the embedded light lanes: `Fitness_Track_Lanes`
- Materials: track = `base`, lanes = `energy`
- The track should frame the building at ground level without competing with it

### Step 4: Add the Entrance Portal

- Create the two A-frame beams: `Fitness_Entrance_Portal`
- Create the threshold slab: `Fitness_Entrance_Threshold`
- Materials: portal = `accent`, threshold = `base`
- Position on the -Y face (front of building)
- The portal should feel heavy and structural — two massive beams leaning inward

### Step 5: Add the Trophy Wall

- Create the display panel: `Fitness_Trophy_Wall`
- Material: `emissive`
- Position adjacent to the entrance on the -Y face
- Subdivide into a grid of smaller display rectangles

### Step 6: Add Window Frame Detail

- Create horizontal frame members between mullions: `Fitness_Window_Frames`
- Material: `base`
- Align with existing ledge band heights
- This creates a readable window grid on each facade

### --- CHECKPOINT 1: DETAIL REVIEW ---
**Take viewport screenshots (front view + 3/4 angle).**

Evaluate:
- Can you count ~30 green energy strips on the facade?
- Does the entrance portal read as a dramatic triangular opening?
- Is the trophy wall visible but not dominant?
- Does the window grid add depth to the facade without making it noisy?
- Does the athletic track frame the building at ground level?

### Step 7: Detail Polish Pass

Look critically at the building and fix:

1. **Energy strip visibility**: If the green strips are invisible, they're too thin or
   the emission is too weak in preview. Increase strip height slightly (up to 0.06 units)
   if needed. If they're too bright/thick, reduce. They should be a subtle rhythm.

2. **Entrance portal weight**: The beams should look HEAVY. If they look like tent poles,
   increase their cross-section. They should feel like they could support the building.

3. **Facade density balance**: The front (-Y) face should have the most detail (portal,
   trophy wall, window frames, energy strips). The back (+Y) face can be simpler. If the
   detail is uniform on all sides, consider removing some from the back to save tris.

4. **Material slot accuracy**: Verify every new object against the SPEC material table:
   - Energy strips → `emissive` (NOT `energy`)
   - Track surface → `base`
   - Track lanes → `energy`
   - Portal beams → `accent`
   - Trophy wall → `emissive`
   - Window frames → `base`

5. **Ground plane read**: The track, entrance threshold, and foundation steps should
   create a clear ground-level composition. Nothing should float.

### --- CHECKPOINT 2: POLISH REVIEW ---
**Take viewport screenshots from all angles including ground-up.**

### Step 8: Triangle Budget Check

Count total triangles and verify:
```python
total = sum(len(o.data.polygons) * 2 for o in bpy.data.objects if o.type == 'MESH')
print(f"Total: {total} tris (budget: 12,000-18,000)")
```

If over 18,000: identify the largest objects and simplify. Window frames and energy strips
are the first candidates for reduction (fewer faces, skip back facade).

If under 12,000: the building might be too simple. Consider adding:
- More articulation to the cantilever undersides
- Additional small mechanical details on the roof
- Subtle panel lines on the foundation steps

### Step 9: Apply Transforms + Verify Materials

Before export, ensure:
```python
# Select all mesh objects and apply transforms
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Verify all materials
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        for slot in obj.data.materials:
            assert slot.name in {"base","accent","glass","detail","emissive","energy"}, \
                f"{obj.name} has invalid material: {slot.name}"
```

### Step 10: Import SIA Tower for Cohesion Check (Gate 6)

Import the approved SIA Tower GLB for a side-by-side comparison:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/exterior/approved/sia-tower-ext.glb`

**Important**: When importing, move ONLY the root empty to X=20. Do NOT move the children —
they are parented and will follow automatically. Moving both parent and children causes
double-offset.

```python
bpy.ops.import_scene.gltf(filepath=sia_path)
for obj in bpy.context.selected_objects:
    if obj.parent is None:
        obj.location.x = 20
```

Take a side-by-side screenshot. Verify:
- Consistent material darkness
- Consistent detail density (Fitness shouldn't be dramatically busier than SIA)
- Scale relationship correct (SIA ~3x taller)
- Both feel like the same dark premium city
- Green energy strips on Fitness are subtle, not overpowering

Delete the SIA Tower import after comparison.

### --- CHECKPOINT 3: COHESION CHECK ---
**Take side-by-side screenshot.**

### Step 11: Export GLB

Use the export pipeline script:
```python
# Read and exec the export pipeline
exec(open("/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/export-pipeline.py").read())

# Export
export_glb(
    output_path="/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/exterior/approved/fitness-ext.glb",
    root_name="fitness",
    max_tris=18000,
    max_size_kb=350,
)
```

**The export pipeline will automatically:**
1. Apply all transforms
2. Per-object decimation (preserves objects under 500 tris)
3. Set origins to bottom-center
4. Remove cameras and lights
5. Parent all geometry under a root `fitness` empty
6. Verify materials (7-slot)
7. Export as Draco-compressed GLB (level 6)
8. Print triangle count and file size

**After export**, verify the output:
- File exists at the `approved/` path
- File size is 100-350 KB
- Triangle count is 12,000-18,000

### Step 12: Post-Export Verification

Re-import the exported GLB into a clean scene to verify it loads correctly:
```python
# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import the exported GLB
bpy.ops.import_scene.gltf(filepath="/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/exterior/approved/fitness-ext.glb")

# Verify
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        print(f"{obj.name}: {len(obj.data.polygons)*2} tris, materials: {[m.name for m in obj.data.materials if m]}")
```

Take a final screenshot of the re-imported GLB to confirm it looks correct.

### --- CHECKPOINT 4: FINAL EXPORT VERIFICATION ---
**Take screenshot of re-imported GLB.**

## QUALITY GATES (Session 7 — Full Exterior)

ALL of these must pass. These are the complete Gates 1-6 from the Quality Rubric.

### Gate 1: Silhouette Clarity [CRITICAL]
- [ ] Identifiable as angular gym megastructure at 200px viewport height
- [ ] Unique outline — cantilevers create non-vertical silhouette
- [ ] Clear roofline/crown with mechanical housings
- [ ] Test: show silhouette unlabeled — viewer identifies function in 3 seconds

### Gate 2: Architectural Scale
- [ ] Reads as 30-floor megastructure (NOT suburban)
- [ ] 30 energy strips visible as floor indicators
- [ ] 5+ distinct sub-elements (base, body, cantilevers, steel frame, roof, portal, track)
- [ ] Window grid visible on facade

### Gate 3: Material System Compliance
- [ ] All materials use the 6-slot naming (base, accent, glass, detail, emissive, energy)
- [ ] Surface area: base ~50-55%, glass ~10-18%, detail ~12-18%, emissive ~3-8%
- [ ] `emissive` = green energy strips + trophy wall
- [ ] `accent` = entrance portal beams ONLY
- [ ] `energy` = pipeline hardpoint + track lanes ONLY
- [ ] No unnamed materials, no materials outside the 6-slot set

### Gate 4: Dark-First Test
- [ ] With all emissive at 0, building reads as recognizable form
- [ ] No bright or saturated surfaces when inactive
- [ ] Green (#34A853) appears ONLY on emissive and accent slots
- [ ] Orange (#FF5E00) appears ONLY on energy slot
- [ ] Overall tone matches Ink-900 (#0A0A0F) environment

### Gate 5: Technical Budget
- [ ] Triangle count: 12,000-18,000
- [ ] File size (after Draco level 6): 100-350 KB
- [ ] Origin at bottom-center, Y=0
- [ ] All transforms applied
- [ ] No cameras or lights in export
- [ ] GLB re-imports cleanly

### Gate 6: Cohesion Check
- [ ] Side-by-side with SIA Tower: consistent material darkness
- [ ] Consistent detail density (not dramatically busier than SIA)
- [ ] Scale relationship correct (SIA ~3x taller)
- [ ] Both feel like the same dark premium civilization

## WHAT TO SAVE

### Blender file (working file with detail):
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/exterior/drafts/fitness-session07.blend`

### Exported GLB (final approved exterior):
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/exterior/approved/fitness-ext.glb`

### Screenshots:
Save to `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/screenshots/`:
- `session07-front.png` — front elevation showing portal + energy strips
- `session07-3quarter.png` — 3/4 angle showing full detail
- `session07-ground-up.png` — ground-level looking up
- `session07-cohesion.png` — side-by-side with SIA Tower
- `session07-export-verify.png` — re-imported GLB verification

## WHAT NOT TO DO

- **Do NOT change the major forms or proportions** — they are approved from Session 6
- Do NOT rebuild the body, cantilevers, foundation, or steel framework
- No interior modeling (Session 8)
- No energy pipeline from SIA Tower (Phase 5)
- No searching for or downloading reference 3D models
- No holo material (Fitness doesn't use it)
- Do NOT make the green energy strips bright — they must be subtle at inactive state
- Do NOT exceed 18,000 triangles
- Do NOT skip the export pipeline script — it handles decimation, origins, and cleanup

## SESSION END CRITERIA

This session is DONE when:
1. All 5 detail elements are added (energy strips, track, portal, trophy wall, window frames)
2. The building has been polished (detail pass complete)
3. Side-by-side cohesion check with SIA Tower passes
4. All 6 quality gates pass
5. GLB exported to `approved/fitness-ext.glb` (12K-18K tris, 100-350 KB)
6. GLB re-import verification passes
7. 5 screenshots saved
8. Working .blend saved to `drafts/fitness-session07.blend`

## SESSION ROADMAP (For Reference)

| Session | Focus | Status |
|---------|-------|--------|
| 1-3 | SIA Tower Exterior (Forms → Detail → Export) | DONE (Approved) |
| 4 | SIA Tower Interior (Neural Core Atrium) | DONE (Approved) |
| 5 | Integration Test (Scenes 1/2/3 camera verification) | DONE (Passed) |
| 6 | Fitness Exterior — Major Forms | DONE (Approved) |
| **-> 7** | **Fitness Exterior — Detail + Polish + Export GLB (this session)** | **NOW** |
| 8 | Fitness Interior — Holographic Workout Arena | Next |
| 9 | Yoga Exterior — Major Forms | Queued |
| 10 | Yoga Exterior — Detail + Polish + Export GLB | Queued |
| 11 | Yoga Interior — Meditation Dome | Queued |
| 12 | Finance Exterior — Major Forms | Queued |
| 13 | Finance Exterior — Detail + Polish + Export GLB | Queued |
| 14 | Finance Interior — Advisory Space | Queued |
| 15 | Phase 2 Integration Test — SIA + 3 Districts | Queued |

## SCENE 4 REFERENCE (What This Building Looks Like in the Scroll Journey)

At 20% scroll (Scene 4), the camera approaches the Fitness District:

**Exterior**: Angular gym megastructure with green energy strips on every floor, exposed
steel framework, cantilevers creating an aggressive silhouette. An outdoor athletic track
wraps the perimeter with green light lanes. The entrance features two heavy angled beams
forming a triangular portal.

**Text overlay**: "Your body tells a story every day. I read every chapter."

**Mood**: Active, energized, powerful — this is the aggressive counterpoint to Yoga's calm.
