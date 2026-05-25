# Balencia City v3 — Session 1: SIA Tower Exterior (Major Forms)

## CONTEXT

You are building the hero structure of Balencia City v3, a premium cinematic 3D city.
The SIA Life Coach Tower is a 100+ floor dark glass monolith at the absolute center of
the city. It is the tallest structure by 2.5x and appears in the first 3 scenes of a
17-scene scroll experience. Every energy pipeline in the city originates from its crown.

If this tower is not excellent, nothing else matters.

This is Session 1 of 5 for the SIA Tower. We are ONLY building the primary silhouette
geometry — the proportions and major forms. No fine detail, no export. Quality over speed.

## READ THESE FILES FIRST

Before doing anything, read both of these files completely:
1. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/MASTER-CONTEXT.md`
2. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/SPEC.md`

## AESTHETIC IDENTITY

- Inspiration: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz
- NOT: Lego proportions, neon overload, photorealism, daytime, cartoon
- Night scene, ink-blue sky (#0A0A0F), warm amber fog
- Dark sophistication: base surfaces are #1E1E28, never pure black #000000
- The tower is a dark glass monolith with a warm bronze framework — premium, not garish

## WHAT TO BUILD (THIS SESSION ONLY)

This session focuses ONLY on the primary silhouette geometry. No fine detail, no energy
rings, no entrance archway, no holo elements. Those come in later sessions.

Build these 4 elements:

### 1. Angular Base Platform
- Wide footprint, stepped geometry (2-3 levels rising up)
- Darker and heavier than the tower body
- Gives the tower a grounded, monumental foundation
- Material slot: `base`

### 2. Main Tower Body
- Tapered rectangular column rising from the base
- Must read as 100+ floors — add horizontal bands/ledges at regular intervals
  (every ~10 floors = minimum 10 bands). These are rough floor-plate indicators, not final detail
- Add vertical panel divisions on each facade to suggest window columns
- The tower MUST taper: base footprint wider than the top
- Material slots: `glass` (panels), `base` (structural frame edges)

### 3. Crystalline Crown
- Faceted, angular glass geometry at the tower apex
- This is where the energy beacon will go (don't build the beacon yet)
- Geometric, angular facets — NOT smooth or rounded
- Should look like a geometric jewel sitting on top of the column
- Material slot: `glass` (brighter treatment than body glass)

### 4. Antenna / Spire
- Thin vertical element rising above the crown
- Adds height emphasis and breaks the roofline
- Simple geometry (tapered cylinder or cone)
- Material slot: `detail`

## WORKFLOW

Follow this exact sequence. Do not skip steps. Take viewport screenshots at the
marked checkpoints.

### Step 1: Prepare the Scene
- Clear the Blender scene completely (remove default cube, camera, light)
- Read and execute the lighting rig script:
  `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/lighting-rig.py`
- Read and execute the material library script:
  `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/material-library.py`
  Call: `create_materials("#FF5E00", include_energy=True, include_holo=True)`
- Verify: scene should have 3 lights and 7 materials ready

### Step 2: Build the Base Platform
- Create the angular, stepped base platform
- Wide footprint (noticeably wider than the tower body)
- 2-3 stepped levels rising up to where the tower body begins
- Assign material: `base`
- This should feel monumental — a proper foundation for a 100+ floor tower

### Step 3: Build the Tower Body
- Create the tapered rectangular column rising from the base
- Add horizontal bands or ledges at regular intervals (10+ bands for floor-plate reads)
- Add vertical panel divisions on each facade to suggest window columns
- The tower must taper: wider at bottom, narrower at top
- Assign materials: `glass` for window panels, `base` for structural frame edges
- This is the largest element — take time to get the proportions right

### Step 4: Build the Crystalline Crown
- Create faceted, angular glass geometry at the top of the tower
- Multiple angular facets, geometric and sharp — not smooth
- Should visually "cap" the tower with a distinct geometric element
- Assign material: `glass`

### Step 5: Add the Antenna / Spire
- Thin vertical element rising above the crown
- Simple geometry — tapered cylinder or cone
- Assign material: `detail`

### --- CHECKPOINT 1 ---
**Take viewport screenshot (front view).**
Does the tower read as a 100+ floor megastructure? Is there a clear visual hierarchy
from base → body → crown → spire?

### Step 6: Silhouette Evaluation
- Take a screenshot from 3/4 angle (showing two facades)
- Take a screenshot from a distance (the tower should be identifiable even when small)
- Evaluate: at 200px viewport height, can you tell this is a unique tower?
- Check: is there a clear base / body / crown / spire hierarchy?

### --- CHECKPOINT 2 ---
**Take viewport screenshots (3/4 view AND distance view).**

### Step 7: Proportion Adjustment (ITERATE — THIS IS THE MOST IMPORTANT STEP)

Look at the screenshots critically and ask:

1. **Does it look like a 100+ floor building, or a 10-story office?**
   → If too short/stubby, increase the body height significantly

2. **Is the base platform proportional?** Too big? Too small?
   → Adjust until the tower feels grounded but not squatting

3. **Does the crown read as a special geometric element?**
   → If it disappears into the body, make it more distinct (larger, more angular)

4. **Is the taper visible?** The body should NOT be a uniform rectangle
   → Adjust the taper until the tower looks like it reaches upward

5. **Does it feel monumental?** Would this dominate a city skyline?
   → Scale up if it feels like a building you'd walk past without noticing

Make adjustments and take another screenshot. **Repeat until the proportions feel right.**
Do NOT proceed until you are satisfied with the silhouette.

### --- CHECKPOINT 3 ---
**Take viewport screenshot from ground-level looking up.**
This mimics Scene 2 of the scroll journey. The tower should dominate the frame
and feel powerful from below.

## QUALITY GATES

Before ending this session, verify ALL of these:

- [ ] **Gate 1 — Silhouette**: Tower is identifiable at 200px height. Has unique roofline
      (crown + spire). No other building would look like this.
- [ ] **Gate 2 — Scale**: Reads as 100+ floor megastructure. Floor indicators visible on
      facade. Has 4 distinct sub-elements (base, body, crown, spire).
- [ ] **Gate 3 — Materials**: Every object has a material from the 7-slot set. No unnamed
      or default gray materials remaining.
- [ ] **Gate 4 — Dark-First**: The tower reads as a dark, premium form. No surfaces are
      inappropriately bright. It looks like it belongs in a night cityscape.
- [ ] **Triangle Budget**: Under 12,000 tris at this stage (leaving budget for Session 2
      architectural detail). Check with `get_scene_info`.

## WHAT TO SAVE

Save the Blender file to:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/exterior/drafts/`

Take a final viewport screenshot and save to:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/screenshots/`

Do NOT export GLB yet — that happens in Session 3 after all detail is added.

## WHAT NOT TO DO

These belong in later sessions. Do NOT attempt them now:

- ❌ Bronze exoskeleton framework (Session 2)
- ❌ Energy rings every 10 floors (Session 2)
- ❌ 5-story entrance archway (Session 2)
- ❌ Crown junction ring with 11 hardpoints (Session 2)
- ❌ Ground-level energy veins (Session 2)
- ❌ Holographic SIA mark (Session 3)
- ❌ Crown beacon light shaft (Session 3)
- ❌ Decimation or GLB export (Session 3)
- ❌ Interior modeling (Session 4)
- ❌ Searching for or downloading reference models (not needed for major forms)
- ❌ Trying to make it perfect on the first attempt — iterate on proportions instead

## SESSION END CRITERIA

This session is DONE when:
1. ✅ You have 3+ viewport screenshots showing the tower from different angles
2. ✅ The silhouette is distinctive and reads as a massive 100+ floor tower
3. ✅ All 5 quality gates above are checked
4. ✅ The .blend file is saved to the drafts folder
5. ✅ You can clearly describe what Session 2 will add (exoskeleton, energy rings,
   entrance archway, junction ring, ground veins)

## SESSION ROADMAP (For Reference)

| Session | Focus | Status |
|---------|-------|--------|
| **→ 1** | **Exterior — Major Forms (this session)** | **NOW** |
| 2 | Exterior — Architectural Detail (exoskeleton, rings, archway, veins) | Next |
| 3 | Exterior — Polish, Holo Mark, Decimate, Export GLB | Queued |
| 4 | Interior — Neural Core Atrium | Queued |
| 5 | Integration Test — Scene 1/2/3 camera verification | Queued |
