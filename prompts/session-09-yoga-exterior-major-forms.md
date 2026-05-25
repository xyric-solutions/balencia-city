# Balencia City v3 — Session 9: Yoga & Wellbeing Exterior (Major Forms)

## CONTEXT

You are building the SECOND district of Balencia City v3 — the Yoga & Wellbeing Floating
Sanctuary. This is the most architecturally unique structure in the entire city: it is the
ONLY building that does not sit on solid ground. It floats above a reflecting lake on
organic support pillars.

The Fitness District (Module 01) is fully approved — exterior and interior. The Yoga district
establishes the opposite end of the aesthetic spectrum:
- Fitness = Angular (aggressive, cantilevers, exposed steel)
- **Yoga = Organic (flowing curves, glass domes, floating platform over water)**
- Finance = Crystalline (faceted, precise, sharp) — coming in Session 12

This is Session 9 of the project. We are ONLY building the primary silhouette geometry —
the floating platform, support pillars, glass domes, and reflecting lake. No fine
bioluminescent vegetation detail, no walkway railings, no hanging garden vines. Quality
over speed.

## READ THESE FILES FIRST

Before doing anything, read all three of these files completely:
1. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/MASTER-CONTEXT.md`
2. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/02-yoga-wellbeing/SPEC.md`
3. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/QUALITY-RUBRIC.md`

## AESTHETIC IDENTITY (same as all sessions)

- Inspiration: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz
- NOT: Lego proportions, neon overload, photorealism, daytime, cartoon
- Night scene, ink-blue sky (#0A0A0F), warm amber fog
- Dark sophistication: base surfaces are #1E1E28, never pure black #000000
- Yoga district color: Sage `#6EE7B7` — used ONLY on emissive/holo/accent slots

## CRITICAL DIFFERENCE FROM FITNESS

The Yoga Sanctuary is the visual antithesis of Fitness:

| Aspect | Fitness | Yoga |
|--------|---------|------|
| Geometry | Sharp angles, straight lines, cantilevers | Flowing curves, organic forms, domes |
| Grounding | Planted firmly on stepped foundation | Floating above a reflecting lake |
| Profile | Vertical tower (12-13 units tall) | Horizontal spread (low-rise, ~5 floors) |
| Aggression | Clenched fist — tension, compression | Open palm — expansion, breath, calm |
| Materials | 6-slot (no holo) | 7-slot (includes holo for bioluminescence) |
| Energy delivery | Hard pipeline from SIA | Warm mist — soft particle cloud, no tube |
| Silhouette | Angular blocks jutting at 3 heights | Cluster of bubbles resting on a mirror |

Every design decision should reinforce this contrast. If something looks angular or
aggressive, it's wrong for this building.

## SCALE REFERENCE — SIA TOWER DIMENSIONS

The SIA Tower is the scale anchor. Everything is measured against it:

| Element | Value |
|---------|-------|
| SIA Tower total height | ~40 units (beacon tip) |
| SIA Tower floors | 100+ |
| SIA Tower body base | ~7x7 units |
| Tallest district allowed | ~16 units (SIA must be 2.5x taller) |

The Yoga Sanctuary is LOW-RISE — only ~5 floors of interior space, spread
horizontally rather than vertically. The tallest dome apex should reach approximately
**5-7 units** above the water surface. The floating platform sits at approximately
Z=2-3 (elevated above the lake). Total structure height from lake surface to dome
apex: ~5-7 units.

**Horizontal spread is the defining dimension**: the platform + walkways span
approximately **16-20 units** across. This building is WIDE, not tall.

**Floor plate reference**: N/A — this isn't a stacked-floor tower. The domes are
open-volume spaces (double/triple height interiors).

## WHAT TO BUILD (THIS SESSION ONLY)

This session focuses ONLY on the primary massing and silhouette. No bioluminescent
vegetation patches, no hanging garden vines, no detailed walkway railings, no interior
modeling. Those come in Session 10.

Build these 5 elements:

### 1. Reflecting Lake Surface
- A large flat plane at Z=0 representing the calm water surface
- Approximately 24x24 units — extends well beyond the building footprint
- Perfectly flat, still water (this is a meditation lake, not an ocean)
- The lake is what makes this district unique — it should be prominent
- Material slot: `glass` (mirror-like reflectivity, dark tint)

### 2. Main Floating Platform
- A large organic curved disc/slab floating above the lake
- Bottom of platform at approximately Z=2.5, top surface at Z=3.0 (0.5 units thick)
- Footprint: ~14x14 units, BUT with organic curved edges — NOT a perfect circle or square
- Think of a large lily pad or organic blob shape — smooth, no sharp corners
- The underside should be smooth and visible from certain angles (this building floats)
- Use a subdivided circle or hand-placed vertices to create an irregular organic outline
- Material slot: `base` (structural surfaces)

### 3. Support Pillars (4-6)
- Tapered organic columns rising from the lake surface (Z=0) to the platform underside (Z=2.5)
- Smooth taper — wider at the base, narrowing toward the platform like tree trunks
- 4-6 pillars arranged in an organic (non-grid) pattern beneath the platform
- They should feel structural but natural — not mechanical
- Each pillar: base diameter ~1.0 units, top diameter ~0.5 units, height ~2.5 units
- Material slot: `detail`

### 4. Glass Domes (2-3)
- 2-3 domes of varying sizes sitting on top of the floating platform
- **Primary dome**: ~12 units diameter, apex at ~Z=8-9 (the main yoga space)
- **Secondary dome**: ~8 units diameter, apex at ~Z=6-7 (meditation area)
- **Optional tertiary dome**: ~5 units diameter, apex at ~Z=5 (healing chamber)
- Domes are smooth hemisphere or slightly elongated egg shapes
- Partial transparency — these are glass structures showing interior spaces
- Position domes in an organic cluster (not perfectly centered or symmetrical)
- Material slot: `glass` (sage-tinted, alpha 0.86)

### 5. Meditation Garden Platforms (2-3)
- Smaller floating discs at varying heights around the main platform
- Each disc: 3-5 units diameter, ~0.3 units thick
- Connected conceptually to the main platform (walkways added in Session 10)
- Heights: Z=2.0, Z=3.5, Z=4.0 (staggered, organic arrangement)
- These are the open-air terrace/garden areas
- Material slot: `base`

## DIMENSIONS GUIDE

| Element | Approximate Size |
|---------|-----------------|
| Lake surface | ~24x24 units, Z=0 |
| Main platform bottom | Z=2.5 |
| Main platform top | Z=3.0 (0.5 units thick) |
| Main platform footprint | ~14x14 units (organic outline) |
| Support pillars | Z=0 to Z=2.5, ~1.0 base diameter |
| Primary dome apex | Z=8-9 (tallest point of structure) |
| Secondary dome apex | Z=6-7 |
| Tertiary dome apex | Z=5 (if included) |
| Garden platforms | 3-5 units diameter, various heights |
| Total horizontal spread | ~16-20 units |
| Total height (lake to dome apex) | ~8-9 units |

**Important**: These are guides, not rigid constraints. The structure should FEEL right —
like a floating organic sanctuary hovering above calm water with glass domes catching
the city light. If the proportions need to change to achieve the right visual, change them.
The silhouette matters more than the numbers.

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
   Call: `create_materials("#6EE7B7", include_energy=True, include_holo=True)`
   (Yoga USES the holo slot — for bioluminescent vegetation in Session 10)
4. Verify: scene should have 3 lights and 7 materials (base, accent, glass, detail, emissive, energy, holo)

### Step 2: Build the Reflecting Lake Surface
- Create a large flat plane at Z=0 (~24x24 units)
- Assign material: `glass`
- This plane defines the ground plane for the entire composition
- It should extend well beyond the building footprint in all directions

### Step 3: Build the Main Floating Platform
- Create an organic-shaped disc floating above the lake
- Bottom at Z=2.5, top at Z=3.0 (~0.5 units thick)
- Start with a circle, then deform vertices to create an organic, irregular edge
- NOT a perfect circle — think lily pad, organic blob
- Smooth the surface (shade smooth)
- Assign material: `base`

**The critical question**: does this platform feel like it's floating? There must be
visible space between the lake surface and the platform underside. The gap (Z=0 to Z=2.5)
is essential — it's what makes this building unique in the city.

### Step 4: Build the Support Pillars
- Create 4-6 tapered cylinders rising from Z=0 to Z=2.5
- Each pillar wider at the base, narrower at the top (tree trunk taper)
- Arrange in a natural, non-grid pattern beneath the platform
- These are the only elements touching both the water and the platform
- Shade smooth — no hard edges
- Assign material: `detail`

### Step 5: Build the Glass Domes
- Create 2-3 hemisphere/dome shapes sitting on top of the platform
- Primary dome: largest, centered or slightly offset on the platform
- Secondary dome: smaller, overlapping with the primary dome's edge or nearby
- Optional tertiary dome: smallest, furthest offset
- Domes rise from the platform surface (Z=3.0) to their respective apex heights
- Shade smooth — these should be perfectly smooth curves
- Assign material: `glass`

**Critical**: The domes are the PRIMARY silhouette element. From any angle, the cluster
of rounded domes over a flat reflecting surface should be instantly readable.

### Step 6: Build the Meditation Garden Platforms
- Create 2-3 smaller floating discs around the main platform
- Varying heights (Z=2.0, Z=3.5, Z=4.0) — staggered, organic arrangement
- Smaller than the main platform (3-5 units each)
- Similar organic edge shape as the main platform (not perfect circles)
- These hover independently — they have no visible support (or 1 thin pillar each)
- Assign material: `base`

### --- CHECKPOINT 1 ---
**Take viewport screenshot (front view / side elevation).**
Does the structure read as a floating sanctuary over water? Key checks:
- Is the gap between lake and platform clearly visible?
- Do the domes create a distinctive rounded silhouette?
- Does it look NOTHING like Fitness (angular) or a conventional tower?

### Step 7: Silhouette Evaluation
- Take a screenshot from 3/4 angle (showing domes + platform + lake reflection)
- Take a screenshot from a distance (should be identifiable even when small)
- Evaluate: at 200px viewport height, can you tell this is a DIFFERENT building from
  SIA Tower AND from Fitness? Is the silhouette unique?
- Check: is there a clear composition of lake → gap → platform → domes?
- Check: does the organic curve language read consistently across all elements?

### --- CHECKPOINT 2 ---
**Take viewport screenshots (3/4 view AND distance view).**

### Step 8: Proportion Adjustment (ITERATE — THIS IS THE MOST IMPORTANT STEP)

Look at the screenshots critically and ask:

1. **Does it float?**
   - The gap between water and platform is the signature feature
   - If the gap is too small, the floating effect is lost — raise the platform
   - If the gap is too large, it looks disconnected — lower the platform
   - The support pillars should bridge the gap visually without filling it

2. **Do the domes dominate the silhouette?**
   - The domes should be the largest visual element — they ARE the building
   - If the platform is more prominent than the domes, the domes are too small
   - If the domes look like bumps on a platform, increase their size
   - The primary dome should clearly be the "main" dome (largest, tallest)

3. **Does it feel organic and calm?**
   - If any edge looks sharp or angular, smooth it
   - If the arrangement feels grid-like or symmetrical, offset elements
   - The building should feel like it grew naturally, not like it was engineered

4. **Is the lake surface readable?**
   - The lake must be clearly visible around and beneath the structure
   - If the building fills all the lake space, the lake needs to be larger
   - The mirror/reflection effect of the lake adds visual presence

5. **Is the silhouette DIFFERENT from all other buildings?**
   - SIA = vertical needle with symmetric crown
   - Fitness = stocky fist with asymmetric cantilevers at 3 heights
   - Yoga = cluster of bubbles on a mirror — horizontal, organic, low
   - If it could be mistaken for either, something is wrong

Make adjustments and take another screenshot. **Repeat until the proportions feel right.**
Do NOT proceed until the silhouette is distinctive.

### --- CHECKPOINT 3 ---
**Take viewport screenshot from low angle across the lake surface.**
This mimics the approach view from Scene 5 — the camera approaches across the water.
The reflection on the lake, the visible underside of the platform, and the dome
silhouettes against the night sky should create a serene, otherworldly image.

### Step 9: Scale Comparison (Optional but Recommended)

Import the approved SIA Tower exterior and Fitness exterior for comparison:
- SIA Tower: `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/exterior/approved/sia-tower-ext.glb`
- Fitness: `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/01-fitness/exterior/approved/fitness-ext.glb`

Place them offset: SIA at (30, 0, 0), Fitness at (-30, 0, 0), Yoga at origin.
Take a viewport screenshot showing all three.

**Check**:
- SIA Tower should be clearly ~5-6x taller than Yoga
- Fitness should be clearly ~2x taller than Yoga, but Yoga should be wider
- All three should feel like they belong to the same dark premium city
- Material darkness should be consistent across all three
- Each building has a completely distinct silhouette language:
  - SIA = vertical needle
  - Fitness = angular fist
  - Yoga = organic bubbles on water
- The variety proves the city's architectural range

After comparison, delete the SIA and Fitness imports (do not save them into the Yoga .blend).

### --- CHECKPOINT 4 ---
**Show the three-building comparison.**

## QUALITY GATES (Session 9 — Major Forms Only)

Before ending this session, verify ALL of these:

- [ ] **Gate 1 — Silhouette**: Building is identifiable as a unique organic floating
      structure at 200px height. Dome cluster and hovering platform create a silhouette
      impossible to confuse with SIA Tower, Fitness, or any rectangular building.
- [ ] **Gate 2 — Scale**: Reads as a low-rise sanctuary spread horizontally over water.
      The floating gap is clearly visible. Multiple dome sizes create visual hierarchy.
      Has 5+ distinct sub-elements (lake, pillars, platform, domes, garden platforms).
- [ ] **Gate 3 — Materials**: Every object has a material from the 7-slot set. No unnamed
      or default gray materials remaining. `holo` material exists but is not yet assigned
      to geometry (that's Session 10).
- [ ] **Gate 4 — Dark-First**: The building reads as a dark, premium form. No surfaces are
      bright or saturated. Sage (#6EE7B7) appears ONLY on emissive-assigned slots (if any
      at this stage). Building looks at home in the ink-blue night cityscape. The glass
      domes and lake surface should be dark and reflective, not bright.
- [ ] **Triangle Budget**: Under 10,000 tris at this stage (leaving budget for Session 10
      detail: bioluminescent vegetation, walkway railings, hanging gardens, dome apex
      energy receptor, planter walls).

## WHAT TO SAVE

Save the Blender file to:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/02-yoga-wellbeing/exterior/drafts/yoga-session09.blend`

Take final viewport screenshots and save to:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/02-yoga-wellbeing/screenshots/`

Recommended screenshots:
- `session09-elevation.png` — side elevation showing floating gap
- `session09-3quarter.png` — 3/4 angle showing dome cluster
- `session09-lake-approach.png` — low angle across lake surface
- `session09-comparison.png` — three-building comparison (if done)

Do NOT export GLB yet — that happens in Session 10 after all detail is added.

## WHAT NOT TO DO

These belong in later sessions. Do NOT attempt them now:

- No bioluminescent vegetation patches on dome bases/platform edges (Session 10)
- No hanging garden vines or trailing geometry at platform edges (Session 10)
- No detailed walkway railings or walkway geometry between platforms (Session 10)
- No planter wall detail on terraces (Session 10)
- No dome apex energy mist receptor detail (Session 10)
- No accent material edge glow on walkway railings (Session 10)
- No fine dome surface subdivisions beyond what's needed for smooth shading (Session 10)
- No decimation or GLB export (Session 10)
- No interior modeling (Session 11)
- No energy mist pipeline from SIA Tower (Phase 5)
- No searching for or downloading reference 3D models (build from scratch)
- No trying to make it perfect on the first attempt — iterate on proportions instead

## SESSION END CRITERIA

This session is DONE when:
1. You have 3+ viewport screenshots showing the structure from different angles
2. The silhouette is distinctive — organic, floating, clearly not SIA Tower or Fitness
3. The dome cluster + floating platform + reflecting lake reads at every angle
4. All 5 quality gates above are checked
5. The .blend file is saved to the drafts folder
6. You can clearly describe what Session 10 will add (bioluminescent vegetation patches,
   walkway geometry + railings, hanging garden vines, planter wall detail, dome apex
   energy receptor, accent edge glow, polish, decimation, GLB export)

## SESSION ROADMAP (For Reference)

| Session | Focus | Status |
|---------|-------|--------|
| 1-3 | SIA Tower Exterior (Forms → Detail → Export) | DONE (Approved) |
| 4 | SIA Tower Interior (Neural Core Atrium) | DONE (Approved) |
| 5 | Integration Test (Scenes 1/2/3 camera verification) | DONE (Passed) |
| 6 | Fitness Exterior — Major Forms | DONE (Approved) |
| 7 | Fitness Exterior — Detail + Polish + Export GLB | DONE (Approved) |
| 8 | Fitness Interior — Holographic Workout Arena | DONE (Approved) |
| **→ 9** | **Yoga Exterior — Major Forms (this session)** | **NOW** |
| 10 | Yoga Exterior — Detail + Polish + Export GLB | Next |
| 11 | Yoga Interior — Meditation Dome | Queued |
| 12 | Finance Exterior — Major Forms | Queued |
| 13 | Finance Exterior — Detail + Polish + Export GLB | Queued |
| 14 | Finance Interior — Advisory Space | Queued |
| 15 | Phase 2 Integration Test — SIA + 3 Districts | Queued |

## SCENE 5 REFERENCE (What This Building Will Look Like in the Scroll Journey)

At 25% scroll (Scene 5), the camera approaches the Yoga Sanctuary across the water:

**Exterior**: The Floating Sanctuary hovers above a calm reflecting lake — the only
structure not built on solid ground. Organic curved platform supported by smooth tapered
pillars rising from the water. Multiple glass domes of varying sizes cap different
sections, their surfaces partially transparent. Bioluminescent vegetation patches glow
with a soft sage pulse on a breathing cycle. Hanging gardens trail from platform edges.
Gentle floating walkways connect sections with thin curved paths arcing over the water.

**Interior** (push-in): A single open space under the largest dome with a translucent
ceiling filtering soft sage-tinted light. 12 yoga mat positions arranged in a circle with
breathing energy rings expanding outward on a 4-second cycle. Meditation gardens at the
edges with still water pools and floating amber lanterns. Mindfulness pod chambers along
one wall. Healing gathering sub-dome projecting mood landscapes.

**Text overlay**: "I understand that strength begins in stillness."

**Mood**: Serene, expansive, contemplative — the calm counterpoint to Fitness's raw power.
