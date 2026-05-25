# Balencia City v3 — Session 2: SIA Tower Exterior (Architectural Detail)

## CONTEXT

You are continuing work on the SIA Life Coach Tower, the hero structure of Balencia City v3.
Session 1 established the primary silhouette geometry — base platform, tapered tower body,
crystalline crown, and antenna spire. The proportions are locked. Session 1 used ~1,478 tris.

Session 2 adds the elements that give the tower its signature identity: the bronze exoskeleton
lattice, the pulsing energy rings, the entrance archway, the crown junction ring, and the
ground-level energy veins. These are what separate "tall glass box" from "SIA Tower."

This is Session 2 of 5 for the SIA Tower. We are adding architectural detail to the existing
major forms. Do NOT modify the Session 1 geometry — only add to it.

## READ THESE FILES FIRST

Before doing anything, read all three of these files completely:
1. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/MASTER-CONTEXT.md`
2. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/SPEC.md`
3. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/energy-pipeline-utils.py`

## LOAD SESSION 1 FILE

Open the Session 1 .blend file before building anything:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/exterior/drafts/sia-tower-session01-major-forms.blend`

Verify these 5 objects exist from Session 1:
- `SIA_Base_Platform` (base material, 36 tris)
- `SIA_Tower_Glass` (glass material, 876 tris)
- `SIA_Tower_Ledges` (base material, 480 tris)
- `SIA_Crown` (glass material, 58 tris)
- `SIA_Spire` (detail material, 28 tris)

If the lighting rig or materials are missing, re-run them:
- Lighting: `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/lighting-rig.py`
- Materials: `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/material-library.py`
  Call: `create_materials("#FF5E00", include_energy=True, include_holo=True)`

## AESTHETIC IDENTITY (same as Session 1)

- Inspiration: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz
- NOT: Lego proportions, neon overload, photorealism, daytime, cartoon
- Night scene, ink-blue sky (#0A0A0F), warm amber fog
- Dark sophistication: base surfaces are #1E1E28, never pure black #000000
- The tower is a dark glass monolith with a warm bronze framework — premium, not garish

## SESSION 1 GEOMETRY REFERENCE

These are the dimensions from the locked Session 1 forms. Use these for positioning:

| Element | Dimensions | Z Range |
|---------|-----------|---------|
| Base Platform (3 steps) | 18x18 → 14x14 → 10x10 | 0 → 4 |
| Tower Body (tapered) | 7x7 bottom → 5x5 top | 4 → 44 |
| Crystalline Crown (6-sided) | ~8 wide at bulge | 44 → 50.5 |
| Antenna/Spire | 0.36 diameter | 50.5 → 56.5 |

Tower body half-widths: bottom hw=3.5, top hw=2.5 (linear interpolation).

## WHAT TO BUILD (THIS SESSION ONLY)

Build these 5 elements, adding them to the existing geometry:

### 1. Bronze Geometric Exoskeleton Framework
This is the tower's signature visual element — a lattice of structural members on all 4 facades.

- **Diagonal members**: X-pattern / diamond lattice across each facade
  - Run from one floor-plate ledge to the next, crossing in the middle
  - Creates diamond/rhombus shapes across each face
  - Thin beams (~0.08-0.12 units wide)
  - Should span the full tower height (Z=4 to Z=44)
- **Horizontal members**: Structural bands at each floor-plate level
  - Align with the existing ledge positions from Session 1
  - Slightly thinner than the diagonals
- The exoskeleton sits OUTSIDE the glass body (offset 0.15-0.25 units from glass surface)
- Material slot: `accent` (warm metallic with faint orange emission)
- This is the most complex element — take time to get the pattern right
- The lattice must follow the tower's taper (wider at bottom, narrower at top)

### 2. Orange Energy Rings (10 total)
- Horizontal glowing rings encircling the tower at each 10-floor mark
- Position: at the same Z-heights as the Session 1 ledges
- Should sit OUTSIDE the exoskeleton (further out than the bronze framework)
- Thin torus geometry or flat ring bands (~0.06 units thick, 0.08 units deep)
- The rings should intensify toward the crown (optional: slightly larger radius near top)
- Material slot: `energy` (#FF5E00, emission strength 0.10)

### 3. Crown Junction Ring
- Thick structural torus sitting between the tower body top (Z=44) and the crown base
- This is where the 11 energy pipelines will eventually depart from
- Position: Z=43.5 to Z=44.5 (straddling the tower-crown boundary)
- Radius: slightly wider than the tower body at its top (~3.5 units from center)
- 11 evenly-spaced hardpoint markers (small cubes or nubs on the ring's outer edge)
  - These mark where pipelines will connect in a later phase
  - Material: `detail` for the hardpoints
- Ring material: `detail` (structural dark metal, non-emissive)

### 4. 5-Story Entrance Archway
- Located on ONE face of the tower (the -Y face, facing the viewer's approach)
- 5 stories tall: Z=4 to Z=6 (the bottom portion of the tower body)
- Width: about 60% of the face width at that height (~4 units wide)
- Deep angular recess cut into the base of the tower
- Framed by angular support structures on both sides
- The archway is a negative space (recessed area) with framing geometry
- Material: `base` for the archway structure (dark, heavy framing)
- Do NOT add volumetric light (that's runtime) — just the structural geometry

### 5. Ground-Level Energy Veins
- 8-12 flat tubes radiating outward from the base platform like roots
- Use the `create_ground_veins()` pattern from `shared/energy-pipeline-utils.py`
  - Center: (0, 0, 0.05)
  - Radius: 12-15 units (extending well beyond the base platform)
  - Vein count: 10 (one per district + one extra)
- Very thin geometry (bevel_depth ~0.04-0.06) hugging the ground plane
- Material slot: `energy` (#FF5E00)

## WORKFLOW

Follow this exact sequence. Do not skip steps.

### Step 1: Load Session 1 File
- Open the .blend from Session 1
- Verify all 5 existing objects are present
- Verify lighting and materials are loaded (re-run scripts if needed)
- Take a verification screenshot to confirm starting state

### Step 2: Build the Exoskeleton Framework
This is the most complex and important element of Session 2.

**Approach**: For each facade, create diagonal beam geometry that forms a diamond/X pattern
between floor-plate levels. The beams should be thin rectangular prisms or beveled edges.

**Pattern per facade panel (between two floor levels)**:
```
    ╲    ╱
     ╲  ╱
      ╲╱     (diamond shape formed by two diagonals)
      ╱╲
     ╱  ╲
    ╱    ╲
```

- Work facade by facade (4 total)
- At each level between floor plates, create two crossing diagonal beams
- The diagonals should span from corner-to-corner of each diamond cell
- Add horizontal connecting beams at each floor-plate Z-height
- Join all exoskeleton geometry into a single object: `SIA_Exoskeleton`
- Material: `accent`

**Triangle budget for exoskeleton**: Aim for 3,000-5,000 tris. This is the most geometry-heavy
element. Use thin rectangular cross-sections (4-6 sided) for each beam, not round tubes.

### Step 3: Add Energy Rings
- Create 10 torus rings at each floor-plate Z-height
- Each ring encircles the tower just outside the exoskeleton
- Use `bpy.ops.mesh.primitive_torus_add()` with low segment counts to stay efficient
  - Major segments: 16-20
  - Minor segments: 4-6
  - Minor radius: 0.04-0.06
- Scale major radius to match the tower width + exoskeleton offset at each Z-height
- Join all rings into: `SIA_Energy_Rings`
- Material: `energy`

### Step 4: Build the Crown Junction Ring
- Create a thick torus at Z=44 (tower body / crown boundary)
- Major radius: ~3.5 (slightly wider than tower top)
- Minor radius: 0.3-0.5 (thick and structural)
- Add 11 small cube hardpoints equally spaced around the outer edge
- These cubes are attachment points for future energy pipelines
- Join into: `SIA_Junction_Ring`
- Material: `detail`

### Step 5: Build the Entrance Archway
- On the -Y face of the tower, create an angular archway frame
- Two vertical support pillars on each side
- An angular arch spanning the top
- Optional: slight depth/recess to suggest the entrance opens inward
- Position: centered on the -Y face, Z=4 to Z=6, width ~4 units
- Object: `SIA_Entrance_Arch`
- Material: `base`

### Step 6: Add Ground-Level Energy Veins
- Create 10 radial veins from center outward
- Each vein is a flat tube at Z=0.05 (just above ground)
- Radius: 12-15 units outward from center
- Bevel depth: 0.04-0.06
- Join all into: `SIA_Ground_Veins`
- Material: `energy`

### --- CHECKPOINT 1 ---
**Take viewport screenshot (3/4 angle).**
Does the exoskeleton create a visible lattice pattern on the facades? Are the energy rings
visible as horizontal glowing bands? Is the junction ring distinct at the crown base?

### Step 7: Silhouette Re-evaluation
- Take screenshots from: front view, 3/4 angle, distance view
- The exoskeleton should ADD to the silhouette complexity without overwhelming the form
- Energy rings should create rhythmic horizontal punctuation
- The entrance archway should be visible at ground level
- Ground veins should radiate outward visibly from the base

### --- CHECKPOINT 2 ---
**Take viewport screenshots (front + 3/4 + distance).**

### Step 8: Detail Adjustment (ITERATE)

Look at the screenshots critically:

1. **Does the exoskeleton read as a structured lattice, or just noise?**
   → If noisy, reduce beam density or increase beam thickness
   → If invisible, the beams are too thin or too close to the glass surface

2. **Are the energy rings visible but not overwhelming?**
   → They should be subtle glowing bands, not thick neon tubes
   → If invisible, increase minor radius slightly

3. **Does the junction ring look like a major structural element?**
   → It should feel heavy and industrial at the crown base
   → If it disappears into the crown, make it thicker or wider

4. **Is the entrance archway visible from distance?**
   → It should be readable as a doorway from the 3/4 angle
   → If invisible, increase its depth or add more prominent framing

5. **Do the ground veins spread convincingly?**
   → They should look like energy roots growing from the base
   → If they look like random lines, adjust spacing or add slight curves

### --- CHECKPOINT 3 ---
**Take viewport screenshot from ground-level looking up.**
The exoskeleton lattice should be dramatic from below. Energy rings should create
horizontal bands of light across the facade. This is the Scene 2 money shot.

## QUALITY GATES (Session 2 Additions)

Before ending this session, verify ALL of these:

- [ ] **Gate 1 — Exoskeleton**: Diamond/lattice pattern visible on all 4 facades.
      Framework follows the tower's taper. Beams are consistent thickness.
- [ ] **Gate 2 — Energy Rings**: 10 rings visible at regular intervals. All use `energy`
      material. Rings encircle the full tower (not partial).
- [ ] **Gate 3 — Junction Ring**: Thick structural ring at crown base. 11 hardpoint
      markers evenly distributed. Uses `detail` material.
- [ ] **Gate 4 — Entrance**: Archway visible on -Y face. Angular framing geometry present.
      Reads as an entrance from distance.
- [ ] **Gate 5 — Veins**: 10 radial energy veins from base. Extend beyond platform edge.
      Use `energy` material.
- [ ] **Gate 6 — Materials**: ALL new objects assigned materials from 7-slot set. No
      default gray materials. Session 1 objects untouched.
- [ ] **Gate 7 — Dark-First**: New additions don't make the tower feel bright or garish.
      Accent material has warm glow, not neon blaze. Energy rings are subtle.
- [ ] **Triangle Budget**: Total scene (Session 1 + Session 2) under 18,000 tris.
      Exoskeleton should be the most expensive element (~3,000-5,000 tris).

## WHAT TO SAVE

Save the Blender file to:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/exterior/drafts/sia-tower-session02-architectural-detail.blend`

Take final viewport screenshots and save to:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/screenshots/`
- `session02-front.png`
- `session02-3quarter.png`
- `session02-ground-up.png`

Do NOT export GLB yet — that happens in Session 3 after polish and decimation.

## WHAT NOT TO DO

These belong in later sessions. Do NOT attempt them now:

- ❌ Holographic SIA mark above entrance (Session 3)
- ❌ Crown beacon light shaft / vertical beam (Session 3)
- ❌ Decimation or polygon optimization (Session 3)
- ❌ GLB export (Session 3)
- ❌ Interior modeling (Session 4)
- ❌ Modifying Session 1 geometry (base, body, crown, spire are locked)
- ❌ Creating actual pipeline tubes to districts (that's a separate Energy Pipeline Session)
- ❌ Adding particle systems or animation (runtime only)
- ❌ Overly detailed exoskeleton with hundreds of micro-beams (keep it readable at distance)

## NEW OBJECTS SUMMARY

After Session 2, these NEW objects should exist alongside the Session 1 objects:

| Object | Material | Estimated Tris | Purpose |
|--------|----------|---------------|---------|
| `SIA_Exoskeleton` | `accent` | 3,000-5,000 | Bronze lattice framework |
| `SIA_Energy_Rings` | `energy` | 800-1,500 | 10 horizontal glow bands |
| `SIA_Junction_Ring` | `detail` | 300-500 | Crown pipeline hub + 11 hardpoints |
| `SIA_Entrance_Arch` | `base` | 200-400 | Ground-level entrance frame |
| `SIA_Ground_Veins` | `energy` | 500-1,000 | 10 radial energy roots |

**Estimated Session 2 total**: 5,000-8,400 tris
**Combined with Session 1** (~1,478): 6,500-10,000 tris
**Budget cap**: 18,000 tris

## SESSION END CRITERIA

This session is DONE when:
1. You have 3+ viewport screenshots showing the detailed tower from different angles
2. The exoskeleton lattice is the dominant new visual feature — visible and structured
3. Energy rings create rhythmic horizontal bands at regular intervals
4. The junction ring is a clear structural element at the crown base with 11 hardpoints
5. The entrance archway is readable as a ground-level doorway
6. Ground veins radiate outward like energy roots
7. All 8 quality gates above are checked
8. The .blend file is saved to the drafts folder
9. You can clearly describe what Session 3 will add (holo mark, beacon, polish, decimate, export)

## SESSION ROADMAP (For Reference)

| Session | Focus | Status |
|---------|-------|--------|
| 1 | Exterior — Major Forms | DONE |
| **→ 2** | **Exterior — Architectural Detail (this session)** | **NOW** |
| 3 | Exterior — Polish, Holo Mark, Decimate, Export GLB | Next |
| 4 | Interior — Neural Core Atrium | Queued |
| 5 | Integration Test — Scene 1/2/3 camera verification | Queued |
