# Balencia City v3 — Session 6: Fitness District Exterior (Major Forms)

## CONTEXT

You are building the FIRST district of Balencia City v3 — the Fitness Gym Megastructure.
This is the start of Phase 2. The SIA Tower (Module 00) is fully approved and serves as
the quality bar. Now we build the 11 districts that surround it.

The Fitness District is a 30-floor angular brutalist gym. Its architectural personality is
raw power — a clenched fist of steel and dark concrete. It is one of three districts being
built in Phase 2 (Fitness, Yoga, Finance), each establishing a different aesthetic range:
- **Fitness = Angular** (aggressive, cantilevers, exposed steel)
- Yoga = Organic (flowing, curves, floating)
- Finance = Crystalline (faceted, precise, sharp)

This is Session 6 of the project. We are ONLY building the primary silhouette geometry —
the proportions, major forms, and cantilever massing. No fine detail strips, no export.
Quality over speed.

## READ THESE FILES FIRST

Before doing anything, read all three of these files completely:
1. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/MASTER-CONTEXT.md`
2. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/SPEC.md`
3. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/QUALITY-RUBRIC.md`

## AESTHETIC IDENTITY (same as all sessions)

- Inspiration: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz
- NOT: Lego proportions, neon overload, photorealism, daytime, cartoon
- Night scene, ink-blue sky (#0A0A0F), warm amber fog
- Dark sophistication: base surfaces are #1E1E28, never pure black #000000
- Fitness district color: Forest Green `#34A853` — used ONLY on emissive/energy slots

## SCALE REFERENCE — SIA TOWER DIMENSIONS

The SIA Tower is the scale anchor. Everything is measured against it:

| Element | Value |
|---------|-------|
| SIA Tower total height | ~40 units (beacon tip) |
| SIA Tower floors | 100+ |
| SIA Tower body base | ~7x7 units |
| Tallest district allowed | ~16 units (SIA must be 2.5x taller) |

The Fitness District at 30 floors should be approximately **12-13 units tall** (rooftop).
This maintains the "SIA Tower dominates by 2.5x" visual ratio.

**Floor plate reference**: ~0.40 units per floor at this scale. Each horizontal band on the
facade represents one floor.

## WHAT TO BUILD (THIS SESSION ONLY)

This session focuses ONLY on the primary massing and silhouette. No green energy strips,
no athletic track detail, no trophy wall, no entrance portal. Those come in Session 7.

Build these 5 elements:

### 1. Reinforced Base / Foundation
- Stepped foundation visible at ground level (2 steps up)
- Wider footprint than the main body above (~12x12 units)
- Heavy, grounded, industrial — this building is planted, not floating
- Material slot: `base`

### 2. Main Tower Body (30 Floors)
- Angular form with sharp inward angles on the primary facades
- NOT a simple rectangular box — the walls angle inward slightly, creating a compressed,
  muscular form that feels like it's clenching
- Add horizontal ledge lines at regular intervals (every 2-3 floors, minimum 10 bands)
  to indicate floor plates. These are structural reads, not final detail.
- The body has large window openings framed by heavy structural members — suggest these
  with vertical divisions on each facade (4-6 columns of panels per face)
- Material slots: `glass` (window panels), `base` (structural frame/wall sections)

### 3. Three Cantilevers (Floors 10, 20, 30)
- These are the signature element — the building juts outward at three heights
- Each cantilever extends 1.5-2 units beyond the main body footprint
- They make the building wider at mid-height than at the base — the "clenched fist" effect
- The cantilevers should be angular slabs, not smooth curves
- Floor 10 cantilever: extends on two opposing faces (front/back or left/right)
- Floor 20 cantilever: extends on all four faces (widest point of the building)
- Floor 30 cantilever: extends on two faces (perpendicular to floor 10), also serves as
  the rooftop edge / crown
- Material slot: `base` (structural) with `detail` on the exposed steel undersides

### 4. Exposed Steel Framework
- At the corners and structural joints, the reinforced steel skeleton is visible
- This is NOT decorative — it looks like the building's bones are showing
- Corner columns running the full height of the building
- Horizontal beams at cantilever connection points
- Raw, industrial aesthetic — this building doesn't hide its structure
- Material slot: `detail`

### 5. Rooftop / Crown
- Flat rooftop with mechanical housing forms (3-4 boxy shapes = ventilation units)
- The floor 30 cantilever forms the rooftop edge, giving it a wider crown than base
- Energy pipeline connection hardpoint: a simple raised platform/socket on the roof center
  (this is where the SIA pipeline will connect in Phase 5)
- Material slot: `detail` (mechanical housings), `base` (rooftop surface)

## DIMENSIONS GUIDE

| Element | Approximate Size |
|---------|-----------------|
| Total height (rooftop) | 12-13 units |
| Base foundation footprint | ~12x12 units |
| Main body footprint | ~10x10 units |
| Cantilever extension | +1.5-2 units per side beyond body |
| Floor 20 (widest point) | ~14x14 units total including cantilevers |
| Floor height | ~0.40 units |
| Foundation height | ~0.8-1.0 units (2 steps) |
| Mechanical housings on roof | 1-2 units tall |

**Important**: These are guides, not rigid constraints. The building should FEEL right —
like a 30-floor muscular gym megastructure. If the proportions need to change to achieve
the right visual, change them. The silhouette matters more than the numbers.

## WORKFLOW

Follow this exact sequence. Do not skip steps. Take viewport screenshots at the
marked checkpoints.

### Step 1: Prepare the Scene

1. Clear the Blender scene completely (remove default cube, camera, light)
2. Set up the lighting rig manually (do NOT exec the shared script — it has a BLENDER_EEVEE_NEXT
   bug on this Blender version). Use this exact code:

```python
import bpy
import math
from mathutils import Vector

# World background
world = bpy.context.scene.world
if world is None:
    world = bpy.data.worlds.new("BalenciaWorld")
    bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs["Color"].default_value = (0.003, 0.003, 0.004, 1.0)  # #0A0A0F
bg.inputs["Strength"].default_value = 1.0

# Key Light (SUN)
key = bpy.data.lights.new("Key_Light", 'SUN')
key.color = (1.0, 0.894, 0.8)
key.energy = 0.8
key.use_shadow = True
key_obj = bpy.data.objects.new("Key_Light", key)
bpy.context.collection.objects.link(key_obj)
key_obj.location = (-8, 20, -6)
key_obj.rotation_euler = (math.radians(70), math.radians(-20), 0)

# Rim Light (SPOT) - Burnt Orange
rim = bpy.data.lights.new("Rim_Light", 'SPOT')
rim.color = (1.0, 0.369, 0.0)
rim.energy = 200
rim.spot_size = math.radians(45)
rim.spot_blend = 0.9
rim_obj = bpy.data.objects.new("Rim_Light", rim)
bpy.context.collection.objects.link(rim_obj)
rim_obj.location = (10, 18, -14)
d = Vector((0,0,-3)) - Vector((10,18,-14))
rim_obj.rotation_euler = d.to_track_quat('-Z','Y').to_euler()

# Fill Light (AREA)
fill = bpy.data.lights.new("Fill_Light", 'AREA')
fill.color = (0.102, 0.102, 0.251)
fill.energy = 50
fill.size = 20
fill_obj = bpy.data.objects.new("Fill_Light", fill)
bpy.context.collection.objects.link(fill_obj)
fill_obj.location = (5, 15, 10)
fill_obj.rotation_euler = (math.radians(60), 0, 0)

# EEVEE settings
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.film_transparent = False
eevee = bpy.context.scene.eevee
if hasattr(eevee, 'use_bloom'):
    eevee.use_bloom = True
    eevee.bloom_threshold = 0.4
    eevee.bloom_intensity = 0.6
if hasattr(eevee, 'use_ssr'):
    eevee.use_ssr = True
if hasattr(eevee, 'use_gtao'):
    eevee.use_gtao = True
    eevee.gtao_distance = 0.35
```

3. Create materials using the material library:
   Read and exec `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/material-library.py`
   Call: `create_materials("#34A853", include_energy=True, include_holo=False)`
   (Fitness does NOT use the holo slot)
4. Verify: scene should have 3 lights and 6 materials (base, accent, glass, detail, emissive, energy)

### Step 2: Build the Reinforced Base / Foundation
- Create the stepped foundation at ground level
- 2 steps rising from Z=0 to Z≈0.8-1.0
- Each step is wider than the one above (pyramid-like stepping)
- Top step matches the main body footprint
- Assign material: `base`

### Step 3: Build the Main Tower Body
- Create the angular main body rising from the foundation
- The walls angle slightly inward — NOT a straight vertical box
- Add horizontal ledge geometry at regular intervals (10+ bands minimum)
- Add vertical panel divisions on each facade (glass panels between structural members)
- The body rises from Z≈1.0 to Z≈12.0 (30 floors)
- Assign materials: `glass` for window panels, `base` for structural sections

**The critical question**: does this body feel like a compressed, muscular form? If it
looks like a normal office tower, add more angular inward lean. The walls should look
like they're under tension.

### Step 4: Build the Three Cantilevers
- Floor 10 (~Z=5): cantilever extends on 2 opposing faces
- Floor 20 (~Z=9): cantilever extends on all 4 faces (widest point)
- Floor 30 (~Z=12): cantilever extends on 2 faces perpendicular to floor 10
- Each cantilever is a thick angular slab that juts outward
- The undersides of cantilevers should have exposed steel framing visible
- Assign materials: `base` (top surfaces), `detail` (undersides/exposed steel)

### Step 5: Add the Exposed Steel Framework
- Corner columns running the full height
- Horizontal beams connecting at cantilever heights
- These should read as structural bones, not decoration
- Keep the geometry simple — straight beams, angular connections
- Assign material: `detail`

### Step 6: Build the Rooftop / Crown
- Flat rooftop surface at Z≈12-13
- 3-4 boxy mechanical housings (ventilation units) — simple cuboids
- Raised pipeline hardpoint at roof center (small platform, ~1x1 unit)
- The floor 30 cantilever overhangs create a distinctive crown silhouette
- Assign materials: `detail` (mechanical housings), `base` (roof surface)

### --- CHECKPOINT 1 ---
**Take viewport screenshot (front view).**
Does the building read as a 30-floor angular gym megastructure? Can you see the
clenched fist silhouette — inward-angled walls with jutting cantilevers?

### Step 7: Silhouette Evaluation
- Take a screenshot from 3/4 angle (showing two facades + cantilevers)
- Take a screenshot from a distance (should be identifiable even when small)
- Evaluate: at 200px viewport height, can you tell this is a DIFFERENT building from
  SIA Tower? Is the silhouette unique?
- Check: is there a clear hierarchy of base → body → cantilevers → crown?
- Check: do the three cantilevers create an aggressive, non-vertical silhouette?

### --- CHECKPOINT 2 ---
**Take viewport screenshots (3/4 view AND distance view).**

### Step 8: Proportion Adjustment (ITERATE — THIS IS THE MOST IMPORTANT STEP)

Look at the screenshots critically and ask:

1. **Does it look like a 30-floor building, or a 3-story warehouse?**
   - If too short/squat, increase the height or add more visible floor bands
   - If too tall/slender, it looks like a SIA clone — make it wider and stockier

2. **Do the cantilevers read?**
   - If they're too subtle, extend them further outward
   - If they're too thin, thicken them — they should look like structural power moves
   - The floor 20 cantilever (widest point) should be unmistakably wider than the base

3. **Does it feel angular and aggressive?**
   - If it looks like a normal building, increase the inward wall angle
   - The building should look like it's flexing, not standing straight

4. **Is the exposed steel framework visible?**
   - If the corner columns disappear into the body, make them slightly proud of the facade
   - The steel should read as structural bones, not trim

5. **Is the silhouette DIFFERENT from SIA Tower?**
   - SIA = vertical needle with symmetric crown
   - Fitness = stocky fist with asymmetric cantilevers at 3 heights
   - If they look similar in silhouette, something is wrong

Make adjustments and take another screenshot. **Repeat until the proportions feel right.**
Do NOT proceed until the silhouette is distinctive.

### --- CHECKPOINT 3 ---
**Take viewport screenshot from ground-level looking up.**
This mimics the approach view from Scene 4. The building should feel imposing and
muscular from below — cantilevers should overhang the viewer.

### Step 9: Scale Comparison (Optional but Recommended)

Import the approved SIA Tower exterior for a side-by-side comparison:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/exterior/approved/sia-tower-ext.glb`

Place the Fitness building at (25, 0, 0) — offset to the right of the SIA Tower at origin.
Take a viewport screenshot showing both buildings side-by-side.

**Check**:
- SIA Tower should be clearly ~2.5-3x taller
- Fitness should be clearly wider/stockier
- Both should feel like they belong to the same dark premium city
- Material darkness should be consistent between the two
- Detail density should be comparable (Fitness shouldn't be dramatically flatter or busier)

After comparison, delete the SIA Tower import (do not save it into the Fitness .blend).

### --- CHECKPOINT 4 ---
**Show the side-by-side comparison with SIA Tower.**

## QUALITY GATES (Session 6 — Major Forms Only)

Before ending this session, verify ALL of these:

- [ ] **Gate 1 — Silhouette**: Building is identifiable as a unique angular structure at
      200px height. Cantilevers create a distinctive non-vertical outline. Not confused
      with SIA Tower or any rectangular office building.
- [ ] **Gate 2 — Scale**: Reads as a 30-floor megastructure. Floor indicators visible on
      facade (10+ horizontal bands). Has 4+ distinct sub-elements (base, body, cantilevers,
      corner steel, roof mechanicals).
- [ ] **Gate 3 — Materials**: Every object has a material from the 7-slot set. No unnamed
      or default gray materials remaining.
- [ ] **Gate 4 — Dark-First**: The building reads as a dark, premium form. No surfaces are
      bright or saturated. Green (#34A853) appears ONLY on emissive/energy-assigned slots.
      Building looks at home in the ink-blue night cityscape.
- [ ] **Triangle Budget**: Under 8,000 tris at this stage (leaving budget for Session 7
      detail: green strips, track, entrance portal, trophy wall).

## WHAT TO SAVE

Save the Blender file to:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/exterior/drafts/fitness-session06.blend`

Take final viewport screenshots and save to:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/screenshots/`

Recommended screenshots:
- `session06-front.png` — front elevation
- `session06-3quarter.png` — 3/4 angle showing cantilevers
- `session06-ground-up.png` — ground-level looking up

Do NOT export GLB yet — that happens in Session 7 after all detail is added.

## WHAT NOT TO DO

These belong in later sessions. Do NOT attempt them now:

- No green energy strips on every floor edge (Session 7)
- No outdoor athletic track or track light lanes (Session 7)
- No triangular entrance portal with angled beams (Session 7)
- No trophy/achievement display wall (Session 7)
- No fine window frame detail (Session 7)
- No decimation or GLB export (Session 7)
- No interior modeling (Session 8)
- No energy pipeline from SIA Tower (Phase 5)
- No searching for or downloading reference 3D models (build from scratch)
- No trying to make it perfect on the first attempt — iterate on proportions instead

## SESSION END CRITERIA

This session is DONE when:
1. You have 3+ viewport screenshots showing the building from different angles
2. The silhouette is distinctive — angular, aggressive, clearly not SIA Tower
3. The clenched fist / cantilever form reads at every angle
4. All 5 quality gates above are checked
5. The .blend file is saved to the drafts folder
6. You can clearly describe what Session 7 will add (green strips, track, entrance
   portal, trophy wall, window detail, polish, decimation, GLB export)

## SESSION ROADMAP (For Reference)

| Session | Focus | Status |
|---------|-------|--------|
| 1-3 | SIA Tower Exterior (Forms → Detail → Export) | DONE (Approved) |
| 4 | SIA Tower Interior (Neural Core Atrium) | DONE (Approved) |
| 5 | Integration Test (Scenes 1/2/3 camera verification) | DONE (Passed) |
| **-> 6** | **Fitness Exterior — Major Forms (this session)** | **NOW** |
| 7 | Fitness Exterior — Detail + Polish + Export GLB | Next |
| 8 | Fitness Interior — Holographic Workout Arena | Queued |
| 9 | Yoga Exterior — Major Forms | Queued |
| 10 | Yoga Exterior — Detail + Polish + Export GLB | Queued |
| 11 | Yoga Interior — Meditation Dome | Queued |
| 12 | Finance Exterior — Major Forms | Queued |
| 13 | Finance Exterior — Detail + Polish + Export GLB | Queued |
| 14 | Finance Interior — Advisory Space | Queued |
| 15 | Phase 2 Integration Test — SIA + 3 Districts | Queued |

## SCENE 4 REFERENCE (What This Building Will Look Like in the Scroll Journey)

At 20% scroll (Scene 4), the camera approaches the Fitness District:

**Exterior**: Angular gym megastructure with green energy strips on every floor, exposed
steel framework, cantilevers creating an aggressive silhouette. An outdoor athletic track
wraps the perimeter with green light lanes. The entrance features two heavy angled beams
forming a triangular portal.

**Interior** (push-in): A cavernous workout arena with holographic performance tracking.
Synchronized weightlifting platforms, AI treadmill, boxing ring, energy pulse floors.
A massive analytics dashboard dominates the back wall.

**Text overlay**: "Your body tells a story every day. I read every chapter."

**Mood**: Active, energized, powerful — this is the aggressive counterpoint to Yoga's calm.
