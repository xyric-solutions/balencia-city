# Balencia City v3 — Session 3: SIA Tower Exterior (Polish, Holo Mark, Export)

## CONTEXT

You are completing the EXTERIOR of the SIA Life Coach Tower, the hero structure of Balencia
City v3. Sessions 1-2 established all major geometry: the base platform, tapered glass body,
crystalline crown, antenna spire, bronze exoskeleton lattice, 10 energy rings, crown junction
ring with 11 hardpoints, entrance archway, and ground-level energy veins. Combined: 6,898 tris.

Session 3 is the FINAL exterior session. You will:
1. Add the holographic SIA mark floating above the entrance
2. Add the crown beacon geometry (vertical light column above the crown)
3. Run a visual polish pass on all existing geometry
4. Run the full Quality Rubric (Gates 1-5) and fix any failures
5. Export the approved GLB via the export pipeline

After Session 3, the SIA Tower exterior is DONE and moves to the `approved/` folder.
Do NOT modify the fundamental proportions of Session 1 geometry (base, body, crown, spire).

## READ THESE FILES FIRST

Before doing anything, read all four of these files completely:
1. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/MASTER-CONTEXT.md`
2. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/SPEC.md`
3. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/export-pipeline.py`
4. `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/QUALITY-RUBRIC.md`

## LOAD SESSION 2 FILE

Open the Session 2 .blend file before building anything:
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/exterior/drafts/sia-tower-session02-architectural-detail.blend`

Verify these 10 objects exist from Sessions 1 and 2:

**Session 1 objects (DO NOT modify geometry):**
- `SIA_Base_Platform` (base material, 36 tris)
- `SIA_Tower_Glass` (glass material, 876 tris)
- `SIA_Tower_Ledges` (base material, 480 tris)
- `SIA_Crown` (glass material, 58 tris)
- `SIA_Spire` (detail material, 28 tris)

**Session 2 objects:**
- `SIA_Exoskeleton` (accent material, 1,488 tris)
- `SIA_Energy_Rings` (energy material, 1,280 tris)
- `SIA_Junction_Ring` (detail material, 516 tris)
- `SIA_Entrance_Arch` (base material, 96 tris)
- `SIA_Ground_Veins` (energy material, 2,040 tris)

**Total entering Session 3: 6,898 tris**

If the lighting rig or materials are missing, re-run them:
- Lighting: `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/lighting-rig.py`
- Materials: `/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared/material-library.py`
  Call: `create_materials("#FF5E00", include_energy=True, include_holo=True)`

## AESTHETIC IDENTITY (same as Sessions 1-2)

- Inspiration: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz
- NOT: Lego proportions, neon overload, photorealism, daytime, cartoon
- Night scene, ink-blue sky (#0A0A0F), warm amber fog
- Dark sophistication: base surfaces are #1E1E28, never pure black #000000
- The tower is a dark glass monolith with a warm bronze framework — premium, not garish

## SESSION 1-2 GEOMETRY REFERENCE

These are the locked dimensions from previous sessions. Use for positioning:

| Element | Dimensions | Z Range |
|---------|-----------|---------|
| Base Platform (3 steps) | 18x18 → 14x14 → 10x10 | 0 → 4 |
| Tower Body (tapered) | 7x7 bottom → 5x5 top | 4 → 44 |
| Crystalline Crown (6-sided) | ~8 wide at bulge | 44 → 50.5 |
| Antenna/Spire | 0.36 diameter | 50.5 → 56.5 |
| Exoskeleton | Offset 0.20 from glass | 4 → 44 |
| Energy Rings | Offset 0.40 from glass | Z = 8,12,16,20,24,28,32,36,40,44 |
| Junction Ring | Major radius 3.5, minor 0.40 | Z = 44 |
| Entrance Archway | 4 units wide, -Y face | 4 → 6 |
| Ground Veins | 10 radial, radius 13 | Z = 0.05 |

Tower body half-widths: bottom hw=3.5, top hw=2.5 (linear interpolation).
`hw(z) = 3.5 - (z - 4) * (1.0 / 40.0)` for z in [4, 44]

## WHAT TO BUILD (THIS SESSION)

Build these 2 new elements, then polish and export:

### 1. Holographic SIA Mark (Floating Logo Above Entrance)

A floating geometric logo hovering above the entrance archway. This is the tower's brand
signature — visible from approach angles, semi-transparent, glowing warm orange.

**Geometry**: A simplified geometric "SIA" logo. Since this is low-poly, create it as an
abstract geometric emblem rather than literal text:
- **Option A (Recommended)**: A hexagonal ring with an inner triangle — the SIA "eye" motif.
  Hexagon outer ring (6 sides, flat, facing -Y) with an equilateral triangle inside.
- **Option B**: Three overlapping geometric planes arranged as an abstract "S-I-A" monogram.

Choose whichever reads better as a distinctive brand mark at small viewport sizes.

**Dimensions & Position**:
- Height: ~2 units tall (represents ~10 meters at city scale)
- Width: ~2 units wide
- Position: centered on the -Y face, directly above the entrance archway
  - X = 0 (centered)
  - Y = -(hw_at_z(7) + 0.5) ≈ -4.0 (floating just in front of the facade)
  - Z = 7.5 (center of the mark, ~1.5 units above the archway top at Z=6)
  - So the mark spans roughly Z=6.5 to Z=8.5
- Oriented to face -Y (toward the approaching viewer)
- Flat geometry — no depth needed (it's a hologram, not a physical object)

**Material**: `holo` — semi-transparent (alpha 0.40), orange glow, emission 0.15
**Object name**: `SIA_Holo_Mark`
**Triangle budget**: 50-150 tris (simple flat geometry)

### 2. Crown Beacon (Vertical Light Column)

A vertical beam of light geometry rising from the crystalline crown upward. This is the
tower's long-range identifier — visible from across the entire city. In the final R3F app
this will be a volumetric shader, but we need placeholder geometry for the GLB.

**Geometry**: A tall, thin, tapered cylinder (or 6-sided prism to match the crown's hexagonal
shape) rising from the crown tip upward.

**Dimensions & Position**:
- Base: at the top of the crown, Z = 50.5 (where the spire begins)
  - OR at the crown's widest point Z ≈ 48, wrapping slightly around the crown top
- Top: Z = 62-65 (extending 12-15 units above the crown, well past the spire tip at 56.5)
- Base radius: ~1.0-1.5 units (wider than the spire, enclosing it in glow)
- Top radius: ~0.3-0.5 units (tapered to a soft point)
- Segments: 6-8 sides (match the hexagonal crown)

**Material**: `emissive` — full burnt orange emission, strength 0.06+
**Object name**: `SIA_Crown_Beacon`
**Triangle budget**: 50-150 tris

**Important**: The beacon is AROUND the spire, not replacing it. The spire (SIA_Spire) stays
intact inside the beacon column. The beacon is a semi-transparent glow volume.

## WORKFLOW

Follow this exact sequence. Do not skip steps.

### Step 1: Load Session 2 File
- Open the .blend from Session 2
- Verify all 10 existing objects are present with correct materials
- Verify lighting and materials are loaded — re-run scripts if needed
- Take a verification screenshot to confirm starting state

### Step 2: Build the Holographic SIA Mark
- Create flat geometric emblem (hexagonal ring + inner triangle, or chosen motif)
- Position it floating above the entrance archway on the -Y face
- Orient it facing -Y (toward the viewer's approach direction)
- Assign `holo` material (semi-transparent, alpha 0.40, orange emission)
- Object name: `SIA_Holo_Mark`

### Step 3: Build the Crown Beacon
- Create a tapered hexagonal prism (6-sided) rising from Z=50.5 upward to Z=63
- Base radius ~1.2, top radius ~0.4
- This wraps AROUND the existing spire — do NOT delete the spire
- Assign `emissive` material (burnt orange, emission strength 0.06)
- Object name: `SIA_Crown_Beacon`

### --- CHECKPOINT 1 ---
**Take viewport screenshot (3/4 angle).**
Is the holo mark visible floating above the entrance? Does the beacon extend visibly
above the crown? Do both new elements use the correct warm orange glow?

### Step 4: Visual Polish Pass

Review the ENTIRE tower from multiple angles. This is the final polish before export.
Take screenshots from at least 4 angles and evaluate each critically:

**4a. Distance silhouette test (from far away, ~100 units)**
- Is the tower immediately identifiable as "the SIA Tower"?
- Does the crown beacon make it unmistakably the tallest structure?
- Can you see the exoskeleton lattice at distance, or does it merge into noise?
- Adjust: If the beacon is too short or thin, increase its height/radius.

**4b. Mid-range evaluation (from ~40-50 units)**
- Are the energy rings visible as distinct horizontal bands?
- Does the exoskeleton create a clear diamond pattern?
- Is the junction ring visible as a distinct structural element at the crown base?
- Is the holo mark readable as a floating emblem?
- Adjust: If any element is invisible at this range, increase its scale slightly.

**4c. Close-up entrance approach (from ~15 units, looking at -Y face, Z~8)**
- Is the entrance archway clearly a doorway?
- Is the holo mark floating above it convincingly?
- Do the ground veins radiate outward from the base convincingly?
- Adjust: If the archway is too shallow, increase pillar depth or width.

**4d. Ground-up dramatic (from base, looking straight up)**
- Does the exoskeleton lattice create a dramatic converging pattern?
- Are the energy rings visible as rhythmic horizontal bands?
- Does the beacon glow visibly at the top?
- This is the hero angle — it should feel awe-inspiring.

For each angle, note what works and what needs adjustment. Make small targeted fixes.
Do NOT rebuild entire elements — nudge sizes, positions, or material values only.

### --- CHECKPOINT 2 ---
**Take 4 viewport screenshots (distance, mid-range, entrance, ground-up).**
Document any adjustments made during the polish pass.

### Step 5: Quality Gate Verification

Run through each gate methodically. For each gate, state PASS or FAIL with evidence.

**Gate 1 — Silhouette Clarity**
- [ ] Identifiable as SIA Tower at 200px viewport height
- [ ] Unique outline (no other structure has vertical beacon + exoskeleton + energy rings)
- [ ] Clear crown/roofline that differentiates it
- Test: Take a screenshot from far away. Could someone identify this as "the main tower"
  without labels, in 3 seconds? If not, what's missing?

**Gate 2 — Architectural Scale**
- [ ] Reads as 100+ floor megastructure (2.5x taller than any future district)
- [ ] Floor plates visible on facade (the ledges + exoskeleton create this)
- [ ] 3+ distinct sub-elements visible (base platform, tower body, exoskeleton,
      energy rings, crown, beacon — should have 5+ easily)

**Gate 3 — Material System Compliance**
- [ ] All materials use the 7-slot naming convention
- [ ] No unnamed materials, no materials outside the set
- [ ] Verify each object → material mapping matches the SPEC:
  - SIA_Base_Platform → base
  - SIA_Tower_Glass → glass
  - SIA_Tower_Ledges → base
  - SIA_Crown → glass
  - SIA_Spire → detail
  - SIA_Exoskeleton → accent
  - SIA_Energy_Rings → energy
  - SIA_Junction_Ring → detail
  - SIA_Entrance_Arch → base
  - SIA_Ground_Veins → energy
  - SIA_Holo_Mark → holo
  - SIA_Crown_Beacon → emissive

**Gate 4 — Dark-First Test**
- [ ] Temporarily set ALL emission strengths to 0 in materials
- [ ] Take a screenshot — tower should still read as a recognizable architectural form
- [ ] No surface appears bright or saturated when inactive
- [ ] Restore emission strengths after the test

**Gate 5 — Technical Budget**
- [ ] Triangle count within 20K-30K exterior spec (we're at ~7K, well within range)
- [ ] Verify origin is at bottom-center
- [ ] All transforms applied
- [ ] No cameras or lights will be included in GLB export

### --- CHECKPOINT 3 ---
**Report gate results: PASS/FAIL for each gate.**
If any gate FAILS, fix the issue before proceeding. After fixing, re-run ALL gates.

### Step 6: Pre-Export Preparation

Prepare the scene for GLB export. Do these in order:

1. **Apply all transforms**: `Ctrl+A` → Location, Rotation, Scale on every mesh object
2. **Verify origin**: All objects should have origin at the scene center / bottom-center
3. **Clean up**: Remove any stray vertices, empty mesh objects, or leftover construction geometry
4. **Material audit**: Run `verify_materials()` from export-pipeline.py — all materials
   must be in the 7-slot set: {base, accent, glass, detail, emissive, energy, holo}

### Step 7: GLB Export

Use the export pipeline from `shared/export-pipeline.py`:

```python
import sys
sys.path.insert(0, "/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/shared")
import export_pipeline

export_pipeline.export_glb(
    output_path="/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/exterior/approved/sia-tower-ext.glb",
    root_name="sia-tower-ext",
    max_tris=25000,
    max_size_kb=500,
)
```

**IMPORTANT**: The export pipeline will:
- Apply transforms
- Decimate per-object if over budget (we should be well under 25K)
- Set origins to bottom-center
- Remove cameras and lights from the export
- Parent everything under a root empty
- Verify 7-slot materials
- Export as Draco-compressed GLB (level 6, Y-up)

After export, verify:
- [ ] GLB file exists in `approved/` folder
- [ ] File size is under 500 KB
- [ ] Triangle count is reported as under 25,000
- [ ] No warnings from material verification

### --- CHECKPOINT 4 ---
**Report: GLB file path, triangle count, file size in KB.**

### Step 8: Final Screenshots

Save final screenshots with the polished, export-ready tower:

Set viewport to Material Preview mode for all screenshots.

1. **Full tower, 3/4 angle** (the standard beauty shot)
   - Camera at distance ~55, elevation ~70°, rotation ~35°
   - Save to: `modules/00-sia-tower/screenshots/session03-final-3quarter.png`

2. **Distance silhouette** (from ~100 units away, tower as small figure)
   - Save to: `modules/00-sia-tower/screenshots/session03-final-distance.png`

3. **Entrance approach** (from ~15 units, looking at -Y face at Z~8)
   - Shows holo mark, archway, ground veins
   - Save to: `modules/00-sia-tower/screenshots/session03-final-entrance.png`

4. **Ground-up dramatic** (from base looking up)
   - The hero shot — lattice converging upward, rings, beacon at top
   - Save to: `modules/00-sia-tower/screenshots/session03-final-ground-up.png`

### Step 9: Save Final .blend

Save the Blender file (WITH lighting and materials, before the export pipeline strips them):
`/Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/00-sia-tower/exterior/drafts/sia-tower-session03-polish-export.blend`

## QUALITY GATES (Session 3 — Final Exterior)

Before ending this session, verify ALL of these:

- [ ] **Gate 1 — Silhouette**: Tower identifiable at 200px. Crown beacon extends above all
      other geometry. Unique outline among future city structures.
- [ ] **Gate 2 — Scale**: Reads as 100+ floor megastructure. 5+ distinct sub-elements
      visible. Floor-plate rhythm visible on facade.
- [ ] **Gate 3 — Materials**: All 12 objects have correct materials from the 7-slot set.
      No default gray. No unnamed materials. Mapping matches SPEC exactly.
- [ ] **Gate 4 — Dark-First**: With emissions at 0, tower reads as architectural form.
      No bright surfaces when inactive.
- [ ] **Gate 5 — Technical**: Triangle count under 25K. GLB under 500 KB. Origin at
      bottom-center. Transforms applied. No cameras/lights exported.
- [ ] **Gate 6 — Holo Mark**: Floating emblem visible above entrance. Uses `holo`
      material. Semi-transparent and glowing, not solid.
- [ ] **Gate 7 — Crown Beacon**: Vertical light column extends above crown and spire.
      Uses `emissive` material. Tapered. Visible from distance.
- [ ] **Gate 8 — Export**: GLB exists in `approved/` folder. Export pipeline completed
      without errors. File opens cleanly (no import warnings expected).

## NEW OBJECTS SUMMARY (Session 3 additions)

| Object | Material | Estimated Tris | Purpose |
|--------|----------|---------------|---------|
| `SIA_Holo_Mark` | `holo` | 50-150 | Floating brand emblem above entrance |
| `SIA_Crown_Beacon` | `emissive` | 50-150 | Vertical light column above crown |

**Estimated Session 3 addition**: 100-300 tris
**Combined total (Sessions 1+2+3)**: ~7,000-7,200 tris
**Export budget**: 25,000 tris (no decimation needed)

## COMPLETE OBJECT INVENTORY (After Session 3)

After Session 3, these 12 objects should exist:

| # | Object | Material | Session | Tris |
|---|--------|----------|---------|------|
| 1 | `SIA_Base_Platform` | `base` | 1 | 36 |
| 2 | `SIA_Tower_Glass` | `glass` | 1 | 876 |
| 3 | `SIA_Tower_Ledges` | `base` | 1 | 480 |
| 4 | `SIA_Crown` | `glass` | 1 | 58 |
| 5 | `SIA_Spire` | `detail` | 1 | 28 |
| 6 | `SIA_Exoskeleton` | `accent` | 2 | 1,488 |
| 7 | `SIA_Energy_Rings` | `energy` | 2 | 1,280 |
| 8 | `SIA_Junction_Ring` | `detail` | 2 | 516 |
| 9 | `SIA_Entrance_Arch` | `base` | 2 | 96 |
| 10 | `SIA_Ground_Veins` | `energy` | 2 | 2,040 |
| 11 | `SIA_Holo_Mark` | `holo` | 3 | ~100 |
| 12 | `SIA_Crown_Beacon` | `emissive` | 3 | ~100 |

## WHAT TO SAVE

1. **Blend file** (with lighting/materials, pre-export):
   `modules/00-sia-tower/exterior/drafts/sia-tower-session03-polish-export.blend`

2. **Exported GLB** (production-ready, Draco-compressed):
   `modules/00-sia-tower/exterior/approved/sia-tower-ext.glb`

3. **Final screenshots**:
   - `modules/00-sia-tower/screenshots/session03-final-3quarter.png`
   - `modules/00-sia-tower/screenshots/session03-final-distance.png`
   - `modules/00-sia-tower/screenshots/session03-final-entrance.png`
   - `modules/00-sia-tower/screenshots/session03-final-ground-up.png`

## WHAT NOT TO DO

These belong in other sessions. Do NOT attempt them now:

- No interior modeling (Session 4 — Neural Core Atrium)
- No energy pipeline tubes to districts (separate Energy Pipeline Sessions)
- No particle systems or animation (runtime R3F only)
- No modifying Session 1 fundamental proportions (base platform shape, tower taper, crown form)
- No increasing triangle count above 25K (we're well under — no need to add complexity)
- No adding district buildings or city context (Assembly Phase)
- No R3F/Three.js integration (Phase 7)
- Do NOT join all objects into one mesh — keep them separate for per-object material assignment

## AFTER SESSION 3

When this session is complete:
1. The GLB at `approved/sia-tower-ext.glb` is the production exterior asset
2. Update `REVIEW.md` — check off Gates 1-5, set Exterior Approved with today's date
3. Update `PROGRESS.md` — mark SIA Tower exterior as APPROVED
4. Session 4 (Interior — Neural Core Atrium) can now begin
5. Phase 2 (First 3 districts) can also begin, since the hero structure is established

## SESSION ROADMAP (For Reference)

| Session | Focus | Status |
|---------|-------|--------|
| 1 | Exterior — Major Forms | DONE |
| 2 | Exterior — Architectural Detail | DONE |
| **-> 3** | **Exterior — Polish, Holo Mark, Export GLB** | **NOW** |
| 4 | Interior — Neural Core Atrium | Next |
| 5 | Integration Test — Scene 1/2/3 camera verification | Queued |
