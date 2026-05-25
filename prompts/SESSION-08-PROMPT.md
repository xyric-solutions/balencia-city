# Balencia City v3 — Session 8: Fitness Interior (Holographic Workout Arena)

## CONTEXT

You are building the interior of the Fitness District — a cavernous double-height workout
arena spanning floors 1-3. The exterior was approved in Session 7 (12,066 tris, 82 KB GLB).
The interior is a SEPARATE GLB that loads on demand when the user scrolls into Scene 4.

This is the first district interior after the SIA Tower Neural Core Atrium (Session 4).
The SIA interior is your quality reference — match its craft and material discipline.

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

## INTERIOR DESIGN PRINCIPLES (from MASTER-CONTEXT)

- Interiors feel like a curated peek inside the district — intimate but connected to the city
- Warm ambient lighting through the open/windowed wall creates silhouette depth
- Props should be recognizable at low poly counts — silhouette clarity over surface detail
- The focal element should be positioned where the camera target empty points

## WHAT YOU'RE BUILDING

### Room Description (from SPEC.md)

A cavernous double-height space spanning floors 1-3, open to a mezzanine level above. The
floor is segmented into distinct workout zones: synchronized weightlifting platforms with
real-time performance meters floating above each station, an AI-guided treadmill lane with
a holographic running partner projected ahead of the runner, and a boxing ring with
holographic stats orbiting the perimeter.

An upper mezzanine holds a yoga/stretching space overlooking the arena below. Energy pulse
floors react to movement with green light ripples. A massive body-performance analytics
dashboard dominates the back wall — a wide curved screen showing aggregate fitness data.

### Focal Point (HERO ELEMENT)

The massive body-performance analytics dashboard on the back wall — a wide curved
holographic screen (approximately 8m wide, 3m tall) displaying body metrics, workout
progress, and district-wide fitness data in green and orange.

This is the first thing the camera sees. It must read immediately as a dramatic data wall.

## TECHNICAL CONSTRAINTS

| Parameter | Value |
|-----------|-------|
| Triangle budget | 5,000 - 10,000 tris |
| File size budget | 60 - 200 KB (Draco level 6) |
| Material system | Same 6-slot: base, accent, glass, detail, emissive, energy |
| Holo material | NO — Fitness does not use holo |
| Light empties | 3 empties: `light_0`, `light_1`, `light_2` |
| Camera target | 1 empty: `camera_target` |
| Room shell | Complete: floor, walls, ceiling, one windowed wall |
| Props | 7 items (specified below) |

## ROOM DIMENSIONS AND LAYOUT

The interior represents floors 1-3 of the exterior building (Z=0.8 to Z=1.92 in exterior
scale). However, interior models use their OWN local coordinate system — they don't need to
match exterior Z values. The R3F runtime positions them independently.

### Suggested Local Coordinates

| Element | Position |
|---------|----------|
| Floor | Z = 0 |
| Mezzanine (floor 3 level) | Z = 4.0 |
| Ceiling | Z = 6.0 (double-height space) |
| Room width (X) | -6 to +6 (12 units wide) |
| Room depth (Y) | -6 to +6 (12 units deep) |
| Windowed wall | +Y face (faces toward the city) |
| Back wall (analytics dashboard) | -Y face |
| Entrance | -X face, ground level |

The room is roughly 12x12x6 units — a cavernous gym arena. The double-height ceiling
should feel imposing.

## WHAT TO BUILD

### Room Shell (5 elements)

1. **Floor** — flat slab at Z=0, 12x12 units
   - Material: `base`
   - Subdivide into a 4x4 grid of floor panels with thin gaps between (energy pulse floor)
   - The gap strips between panels: `emissive` (green light ripple zones)
   - Budget: ~100 tris (floor panels) + ~80 tris (gap strips)

2. **Ceiling** — flat slab at Z=6, 12x12 units
   - Material: `base`
   - Add exposed structural beams (3 running X-direction, 3 running Y-direction = grid)
   - Beams: `detail` material, ~0.3 units deep, ~0.2 units wide
   - Budget: ~50 tris (ceiling slab) + ~150 tris (beams)

3. **Back Wall (-Y)** — solid wall from Z=0 to Z=6
   - Material: `base`
   - The analytics dashboard is MOUNTED on this wall (separate object)
   - Budget: ~12 tris

4. **Side Walls (-X and +X)** — solid walls from Z=0 to Z=6
   - Material: `base`
   - -X wall has a doorway opening (entrance, ~2 units wide, ~2.5 units tall)
   - Budget: ~24 tris (2 walls) + ~12 tris (doorway framing)

5. **Windowed Wall (+Y)** — wall with large window openings
   - Lower section (Z=0 to Z=1): solid base wall, `base`
   - Upper section (Z=1 to Z=6): 3-4 large window panes, `glass`
   - This is where city light enters — the most important wall for atmosphere
   - Window frame members: `detail`
   - Budget: ~60 tris

### Focal Element: Analytics Dashboard (1 element)

6. **Body-Performance Analytics Dashboard**
   - Wide curved screen on the -Y (back) wall
   - Dimensions: ~8 units wide, ~3 units tall, slight concave curve
   - Position: centered on back wall, Z = 1.5 to 4.5 (spans most of the wall height)
   - The curve is subtle — maybe 6-8 segments across the width
   - Material: `emissive` (the main green-glowing hero element)
   - Add a thin frame/border around the screen: `detail`
   - Below the screen: a thin console shelf/ledge at Z=1.5: `base`
   - Budget: ~120 tris (curved screen) + ~50 tris (frame + console)

### Supporting Props (7 items)

7. **Weightlifting Platforms (3 stations)** — front-left area
   - Each platform: raised rectangular slab (~2x1.5 units, ~0.1 units high)
   - Material: `base`
   - Floating performance meter above each: small rectangular panel at ~Z=2.5
   - Meter material: `emissive` (green floating HUD elements)
   - Position: X = -4 to -1, Y = -4 to -1 (front-left quadrant)
   - Budget: 3 platforms × ~16 tris + 3 meters × ~4 tris = ~60 tris

8. **AI Treadmill Lane** — front-right area
   - Flat track surface (~1.5 units wide, ~6 units long, running along Y)
   - Material: `base` (track surface), with center lane line in `emissive`
   - A translucent running figure silhouette at one end (holographic partner)
   - Figure: extremely simplified — a flat cutout silhouette, ~5-8 quads
   - Figure material: `emissive` (green ghost runner)
   - Position: X = +2 to +4, Y = -4 to +2
   - Budget: ~30 tris (track) + ~16 tris (figure)

9. **Boxing Ring** — center-right area
   - Raised platform (~3x3 units, ~0.15 units high)
   - 4 corner posts (thin vertical cylinders, Z=0.15 to Z=1.5)
   - 3 horizontal ropes on each side (thin cylinders connecting posts)
   - Material: platform = `base`, posts = `detail`, ropes = `detail`
   - Position: X = +1 to +4, Y = +1 to +4 (back-right quadrant)
   - Budget: ~24 tris (platform) + ~96 tris (4 posts × 6-seg cylinders) + ~144 tris (12 ropes × 6-seg cylinders) = ~264 tris

10. **Upper Mezzanine Platform** — back area, elevated
    - Flat slab at Z=4.0, extending ~3 units from the back wall (-Y)
    - Width: ~10 units (nearly full room width)
    - Railing along the front edge (facing the arena): vertical posts + horizontal rail
    - Material: platform = `base`, railing = `detail`
    - Position: Y = -6 to -3, Z = 4.0
    - Budget: ~12 tris (slab) + ~120 tris (railing with posts)

11. **Energy Pulse Floor Panels** — integrated into main floor
    - Already included in the floor grid design (step 1)
    - The gap strips between floor panels serve as energy pulse zones
    - Material: `emissive`
    - No additional budget needed

12. **Equipment Rack** — along -X (entrance) wall
    - Vertical frame with horizontal bars (like a pull-up/squat rack)
    - Simple box frame: 2 uprights + 3 horizontal bars
    - Material: `detail`
    - Position: X = -5.5 to -5.0, Y = -2 to +2 (along the wall)
    - Budget: ~60 tris

13. **Hanging Heavy Bags (3)** — suspended from ceiling beams
    - 3 cylindrical bags hanging from short chains
    - Each bag: 6-sided cylinder, ~0.3 radius, ~1.2 tall
    - Chain: thin box or single quad from ceiling to bag top
    - Material: bag = `detail`, chain = `detail`
    - Position: scattered in the front half of the room, Z hanging from ~5.5 down to ~3.0
    - Budget: 3 bags × ~24 tris + 3 chains × ~4 tris = ~84 tris

### Required Empties (4 total)

14. **Light Empties** — placed at logical light source positions
    - `light_0`: Center of arena at double-height ceiling (0, 0, 5.5) — broad key light
    - `light_1`: Above boxing ring (+2.5, +2.5, 5.5) — focused ring spot
    - `light_2`: Behind analytics dashboard (0, -5.8, 3.0) — green backlight wall-wash

15. **Camera Target Empty**
    - `camera_target`: Center of the arena floor at chest height (0, 0, 1.2)
    - Framed to show weightlifting zone in foreground, boxing ring at midground,
      analytics dashboard wall in background. Mezzanine edge visible at top of frame.

## TRIANGLE BUDGET BREAKDOWN

| Element | Estimated Tris |
|---------|---------------|
| Floor (panels + pulse strips) | ~180 |
| Ceiling + beams | ~200 |
| Walls (back, sides, windowed) | ~110 |
| Analytics Dashboard (screen + frame) | ~170 |
| Weightlifting Platforms + Meters | ~60 |
| Treadmill Lane + Holo Figure | ~46 |
| Boxing Ring (platform + posts + ropes) | ~264 |
| Mezzanine (slab + railing) | ~132 |
| Equipment Rack | ~60 |
| Heavy Bags (3) | ~84 |
| **Subtotal** | **~1,306** |
| **Remaining for detail/polish** | **~3,700 - 8,700** |

You have significant headroom. Use it for:
- Proper 3D cross-sections on frame/railing elements (not flat quads)
- Glass panel subdivisions on the windowed wall
- Additional architectural detail (column supports, ventilation grilles)
- Dashboard screen subdivisions for a more readable data wall
- Additional small props if the room feels empty
- Wall panel articulation (recessed panels, grooves)

## MATERIAL ASSIGNMENT TABLE

| Surface | Slot | Notes |
|---------|------|-------|
| Floor panels, walls, ceiling slab | `base` | Dark structural surfaces |
| Ceiling beams, railing, posts, ropes, bags, rack, window frames | `detail` | Structural metal |
| Analytics dashboard screen, floating meters, pulse floor gaps, treadmill line, holo figure | `emissive` | #34A853 green glow |
| Window panes on +Y wall | `glass` | City light enters here |
| Dashboard frame/border (if distinct from detail) | `accent` | Faint green edge glow |
| Energy pipeline connection (if visible from interior) | `energy` | #FF5E00 orange |

**DO NOT use `holo` material** — Fitness does not use holo per SPEC.

## WORKFLOW

Follow this exact sequence.

### Step 1: Create New Blank Scene

1. Start from a clean Blender scene (File → New → General, or clear everything)
2. Run the material library:
   ```python
   exec(open("/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/material-library.py").read())
   create_materials("#34A853", include_energy=True, include_holo=False)
   ```
3. Run the interior lighting rig for preview:
   ```python
   exec(open("/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/interior-lighting-rig.py").read())
   setup_interior_lighting(
       focal_point=(0, -4, 3.0),     # analytics dashboard center
       floor_z=0.0,
       ceiling_z=6.0,
       radius=6.0,
   )
   boost_emissions_for_preview()
   ```
4. Set viewport to Material Preview with scene lights and scene world enabled
5. Delete the default cube

### Step 2: Build Room Shell

- Create floor, ceiling, back wall, side walls, windowed wall
- All walls are `base` except windowed wall which has `glass` panes
- The floor should have the energy pulse grid (subdivided panels with emissive gaps)
- Ceiling should have the exposed beam grid

### Step 3: Build Analytics Dashboard (Focal Element)

- Create the curved screen panel on the -Y wall
- Material: `emissive`
- Add frame border: `detail` or `accent`
- Add console shelf below: `base`
- This is the HERO — it should dominate the back wall

### Step 4: Build Mezzanine

- Elevated platform at Z=4.0
- Railing along the front edge with vertical posts
- This overlooks the arena below

### Step 5: Build Workout Zone Props

- 3 weightlifting platforms with floating performance meters
- AI treadmill lane with holographic running partner
- Boxing ring with posts and ropes
- Equipment rack along the wall
- 3 hanging heavy bags from ceiling

### Step 6: Place Empties

- 3 light empties (`light_0`, `light_1`, `light_2`)
- 1 camera target (`camera_target`)
- These are REQUIRED for the R3F runtime

### --- CHECKPOINT 1: INTERIOR REVIEW ---
**Take viewport screenshots (overview + dashboard close-up).**

Evaluate:
- Does the analytics dashboard dominate the back wall?
- Can you identify all 7 props?
- Does the room feel like a cavernous gym arena?
- Is the windowed wall letting (simulated) city light in?
- Does the mezzanine overlook feel right?

### Step 7: Detail + Polish Pass

1. **Prop readability**: Each prop should be identifiable by silhouette alone. If the
   boxing ring doesn't read as a boxing ring, add corner padding or rope tension detail.

2. **Dashboard presence**: The analytics screen should feel like the largest, most
   dramatic element in the room. If it's underwhelming, increase its size or add
   secondary monitor panels flanking it.

3. **Atmospheric depth**: The windowed wall should create clear light/dark contrast.
   The side away from the windows should be darker and more mysterious.

4. **Floor energy**: The emissive gap strips in the floor should create a subtle grid
   pattern that suggests reactive energy (green light ripples). They should be dim at
   inactive state (emission 0.06) but clearly visible.

5. **Material accuracy**: Verify every object against the material assignment table.

6. **Mezzanine weight**: The mezzanine should feel like a substantial concrete slab,
   not a floating platform. Add underside geometry or support columns if needed.

### --- CHECKPOINT 2: POLISH REVIEW ---
**Take screenshots from multiple angles.**

### Step 8: Triangle Budget Check

```python
total = sum(len(o.data.polygons) * 2 for o in bpy.data.objects if o.type == 'MESH')
print(f"Total: {total} tris (budget: 5,000-10,000)")
```

If under 5,000: add more architectural detail — wall panel articulation, additional
small props, more railing/frame detail.

If over 10,000: simplify the largest objects. Boxing ring ropes and heavy bags are
first candidates for reduction.

### Step 9: Import SIA Interior for Cohesion Check

Import the SIA Tower interior GLB:
```python
bpy.ops.import_scene.gltf(
    filepath="/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/interior/approved/sia-tower-int.glb"
)
# Move root to X=20
for obj in bpy.context.selected_objects:
    if obj.parent is None:
        obj.location.x = 20
```

Verify:
- Consistent material darkness between Fitness and SIA interiors
- Both feel like they belong to the same city
- Fitness should feel more raw/industrial; SIA should feel more refined/ceremonial
- Neither should be dramatically brighter or busier than the other

Delete the SIA import after comparison.

### --- CHECKPOINT 3: COHESION CHECK ---
**Take side-by-side screenshot.**

### Step 10: Apply Transforms + Verify

```python
# Apply transforms (mesh objects only)
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

# Verify empties exist
required_empties = ['light_0', 'light_1', 'light_2', 'camera_target']
for name in required_empties:
    obj = bpy.data.objects.get(name)
    assert obj is not None, f"Missing required empty: {name}"
    assert obj.type == 'EMPTY', f"{name} is not an empty: {obj.type}"
    print(f"  {name}: {obj.location}")

# Verify materials
VALID = {"base", "accent", "glass", "detail", "emissive", "energy"}
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        for mat in obj.data.materials:
            assert mat.name in VALID, f"{obj.name}: invalid material '{mat.name}'"
```

### Step 11: Export GLB

```python
exec(open("/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/export-pipeline.py").read())

export_glb(
    output_path="/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/interior/approved/fitness-int.glb",
    root_name="fitness-interior",
    max_tris=10000,
    max_size_kb=200,
)
```

**NOTE**: The export pipeline removes cameras and lights. The interior preview lights
(from interior-lighting-rig.py) will be stripped — that's correct. Only empties survive
export. The R3F runtime creates its own lights at the `light_0/1/2` empty positions.

**If the export_pipeline.py fails** due to Blender version issues (like `export_apply_modifiers`
or `export_colors` parameters), run the pipeline steps manually:
1. Apply transforms (mesh objects only, one at a time)
2. Remove cameras and lights
3. Set origins to bottom-center
4. Parent all objects under a `fitness-interior` root empty
5. Export with:
   ```python
   bpy.ops.export_scene.gltf(
       filepath=output_path,
       export_format='GLB',
       export_draco_mesh_compression_enable=True,
       export_draco_mesh_compression_level=6,
       export_yup=True,
       export_texcoords=True,
       export_normals=True,
       export_materials='EXPORT',
       export_cameras=False,
       export_lights=False,
   )
   ```

### Step 12: Post-Export Verification

Re-import the exported GLB into a clean scene:
```python
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

bpy.ops.import_scene.gltf(
    filepath="/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/interior/approved/fitness-int.glb"
)

# Verify
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        print(f"{obj.name}: mats={[m.name for m in obj.data.materials if m]}")
    elif obj.type == 'EMPTY':
        print(f"[EMPTY] {obj.name}: {obj.location}")
```

Confirm:
- All meshes re-import with correct materials
- All 4 empties are present (light_0, light_1, light_2, camera_target)
- No cameras or lights in the file

### --- CHECKPOINT 4: FINAL EXPORT VERIFICATION ---
**Take screenshot of re-imported GLB.**

## QUALITY GATES (Session 8 — Interior)

ALL of these must pass. These are Gates 3, 4, 5, 6, 7 from the Quality Rubric.

### Gate 3: Material System Compliance
- [ ] All materials use the 6-slot naming (base, accent, glass, detail, emissive, energy)
- [ ] `emissive` = dashboard screen, floating meters, pulse floor, treadmill line, holo figure
- [ ] `glass` = windowed wall panes ONLY
- [ ] `accent` = dashboard frame border (if used)
- [ ] No `holo` material (Fitness doesn't use it)
- [ ] No unnamed materials

### Gate 4: Dark-First Test
- [ ] With all emissive at 0, room reads as recognizable interior space
- [ ] No bright or saturated surfaces when inactive
- [ ] Green (#34A853) appears ONLY on emissive and accent slots
- [ ] Overall tone matches the dark environment

### Gate 5: Technical Budget
- [ ] Triangle count: 5,000-10,000
- [ ] File size (after Draco level 6): 60-200 KB
- [ ] Origin at bottom-center
- [ ] All transforms applied
- [ ] No cameras or lights in export
- [ ] GLB re-imports cleanly

### Gate 6: Cohesion Check
- [ ] Side-by-side with SIA interior: consistent material darkness
- [ ] Consistent detail density
- [ ] Both feel like interiors of the same city
- [ ] Fitness feels more raw/industrial, SIA more refined (correct differentiation)

### Gate 7: Interior-Specific
- [ ] Clear focal point — analytics dashboard dominates the back wall
- [ ] Light empties sensibly placed (light_0=ceiling center, light_1=boxing ring, light_2=dashboard backlight)
- [ ] camera_target empty at room's focal point (center floor, chest height)
- [ ] 7 props present, each identifiable by silhouette
- [ ] Complete room shell (floor, 3 solid walls, 1 windowed wall, ceiling)
- [ ] Interior materials use same 6-slot system as exterior

## WHAT TO SAVE

### Blender file:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/interior/drafts/fitness-int-session08.blend`

### Exported GLB:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/interior/approved/fitness-int.glb`

### Screenshots:
Save to `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/screenshots/`:
- `session08-overview.png` — wide view of full interior from entrance direction
- `session08-dashboard.png` — close-up of analytics dashboard (hero element)
- `session08-boxing-ring.png` — boxing ring and mezzanine visible
- `session08-cohesion.png` — side-by-side with SIA interior
- `session08-export-verify.png` — re-imported GLB verification

## WHAT NOT TO DO

- Do NOT model exterior geometry — this is interior only
- Do NOT use `holo` material — Fitness doesn't use it
- Do NOT create photorealistic props — silhouette clarity over surface detail
- Do NOT exceed 10,000 triangles
- Do NOT skip the empties (light_0, light_1, light_2, camera_target) — they're required
- Do NOT bake lights into the export — only empties survive
- Do NOT make the analytics dashboard small — it's the HERO, it dominates the wall
- Do NOT forget the windowed wall — it's critical for atmosphere
- Do NOT search for or download reference 3D models

## SESSION END CRITERIA

This session is complete when:
1. Room shell is complete (floor with energy grid, ceiling with beams, 3 walls + windowed wall)
2. Analytics dashboard is the clear focal point on the back wall
3. All 7 props are built and identifiable
4. 4 empties placed (3 lights + 1 camera target)
5. SIA interior cohesion check passes
6. All quality gates pass (Gates 3, 4, 5, 6, 7)
7. GLB exported to `approved/fitness-int.glb` (5K-10K tris, 60-200 KB)
8. GLB re-import verification passes
9. 5 screenshots saved
10. Working .blend saved to `drafts/fitness-int-session08.blend`

## SESSION ROADMAP (For Reference)

| Session | Focus | Status |
|---------|-------|--------|
| 1-3 | SIA Tower Exterior (Forms → Detail → Export) | DONE (Approved) |
| 4 | SIA Tower Interior (Neural Core Atrium) | DONE (Approved) |
| 5 | Integration Test (Scenes 1/2/3 camera verification) | DONE (Passed) |
| 6 | Fitness Exterior — Major Forms | DONE (Approved) |
| 7 | Fitness Exterior — Detail + Polish + Export GLB | DONE (Approved) |
| **-> 8** | **Fitness Interior — Holographic Workout Arena (this session)** | **NOW** |
| 9 | Yoga Exterior — Major Forms | Next |
| 10 | Yoga Exterior — Detail + Polish + Export GLB | Queued |
| 11 | Yoga Interior — Meditation Dome | Queued |
| 12 | Finance Exterior — Major Forms | Queued |
| 13 | Finance Exterior — Detail + Polish + Export GLB | Queued |
| 14 | Finance Interior — Advisory Space | Queued |
| 15 | Phase 2 Integration Test — SIA + 3 Districts | Queued |

## SCENE 4 INTERIOR REFERENCE (What This Room Looks Like in the Scroll Journey)

At 20% scroll (Scene 4), after the camera approaches the Fitness District exterior, it
transitions inside:

**Interior**: A cavernous double-height workout arena. Synchronized weightlifting stations
with floating green performance metrics. An AI treadmill with a ghostly holographic running
partner. A boxing ring surrounded by orbiting stats. A massive curved analytics dashboard
dominates the back wall, pulsing with body-performance data in green and orange. Above,
a mezzanine overlooks the arena. The floor pulses with green energy ripples.

**Mood**: Raw, powerful, industrial. This is where bodies are forged — the space should
feel muscular and intense, not polished and sterile.
