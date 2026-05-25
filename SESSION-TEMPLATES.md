# Balencia City v3 — Session Templates

Copy-paste the relevant prompt at the start of each session.

---

## Session Type 1: Exterior Session

**Before starting**: Read MASTER-CONTEXT.md + module SPEC.md

```
I'm building the EXTERIOR of Balencia City v3 module [NN]-[name].

Read the full context:
- /Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/MASTER-CONTEXT.md
- /Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/[NN]-[name]/SPEC.md

Steps:
1. Clear Blender scene
2. Run shared/lighting-rig.py
3. Run shared/material-library.py with color [HEX]
4. Build major forms (walls, roof, foundation) → viewport screenshot
5. Add architectural detail (windows, facade elements, crown) → screenshot
6. Add props and dressing → screenshot
7. Assign materials (7-slot: base, accent, glass, detail, emissive, [energy], [holo])
8. Verify material names match spec
9. Export GLB via shared/export-pipeline.py with max_tris=[BUDGET]
10. Save to modules/[NN]-[name]/exterior/drafts/[name]-ext-draft-[N].glb

After export, run the Quality Rubric (Gates 1-5).
```

---

## Session Type 2: Interior Session

**Before starting**: Exterior must be APPROVED. Read SPEC.md interior section.

```
I'm building the INTERIOR of Balencia City v3 module [NN]-[name].

Read the full context:
- /Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/MASTER-CONTEXT.md
- /Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/[NN]-[name]/SPEC.md (interior section)

Steps:
1. Clear Blender scene
2. Run shared/lighting-rig.py
3. Run shared/material-library.py with color [HEX]
4. Build room shell (floor, walls, ceiling — one open/windowed wall)
5. Add focal point element → screenshot
6. Add 4-8 supporting props → screenshot
7. Place light empties: light_0, light_1, light_2
8. Place camera_target empty at focal point
9. Assign materials (7-slot)
10. Export GLB via shared/export-pipeline.py with max_tris=[INTERIOR BUDGET]
11. Save to modules/[NN]-[name]/interior/drafts/[name]-int-draft-[N].glb

After export, run Quality Rubric (Gates 3-5, 7).
```

---

## Session Type 3: Energy Pipeline Session

**Before starting**: Both SIA Tower and target district must be APPROVED.

```
I'm building the ENERGY PIPELINE from SIA Tower to [NN]-[name].

Read:
- /Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/MASTER-CONTEXT.md (Section 7)
- /Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/energy-system/SPEC.md
- /Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/modules/[NN]-[name]/SPEC.md (energy delivery style)

Steps:
1. Import approved SIA Tower and target district GLBs for position reference
2. Create pipeline geometry using shared/energy-pipeline-utils.py
3. Style: [Hard pipeline / Warm mist / Faint thread / Special]
4. Apply energy material (always Burnt Orange #FF5E00)
5. Add ground-level energy veins at district endpoint
6. For special styles: add particle emitter geometry
7. Export to energy-system/pipelines/drafts/pipeline-[name]-draft-[N].glb

Run Energy Integration Check from Quality Rubric.
```

---

## Session Type 4: Cross-Connection Session

**Before starting**: All connected districts must be APPROVED.

```
I'm building CROSS-DISTRICT CONNECTIONS for Balencia City v3.

Read:
- /Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/energy-system/cross-connections/SPEC.md

Steps:
1. Import all approved district GLBs for position reference
2. Create thin gold line geometry between specified district pairs
3. Add midpoint anchor geometry (for insight card placement)
4. Apply gold #F59E0B emissive material
5. Export to energy-system/cross-connections/approved/

Connection pairs: [list from SPEC]
```

---

## Session Type 5: Integration Session

**Before starting**: New structure and all previously approved structures available.

```
I'm running an INTEGRATION CHECK for newly approved [NN]-[name].

Steps:
1. Import ALL approved structures into Blender at orbital positions
2. Run shared/lighting-rig.py
3. Take screenshot from overview camera position
4. Take screenshot from SIA Tower perspective (looking out)
5. Verify:
   - Scale consistency across all structures
   - Material darkness consistency
   - Detail density consistency
   - No building brighter or flatter than neighbors
   - SIA Tower remains unmistakably tallest
6. Note any cohesion issues
7. Save screenshots to assembly/screenshots/

Run Quality Rubric Gate 6 (Cohesion Check).
```

---

## Session Type 6: Scroll Verification Session

**Before starting**: Phase 6 assembly must be complete.

```
I'm running SCROLL VERIFICATION for all 17 scenes.

Read:
- /Users/hamza/Xyric Wiki/PLAYGROUND/balencia-city-v3/SCROLL-JOURNEY.md

Steps:
1. Load full assembled city in Blender
2. For each of 17 scenes:
   a. Position camera at specified location/angle
   b. Take viewport screenshot
   c. Verify: correct structures visible, emotional tone, framing
   d. Verify: energy pipelines visible where specified
   e. Note any obstructed views or empty voids
3. Save screenshots to assembly/scroll-verification/scene-[NN].png
4. Document scene-specific adjustments needed
```
