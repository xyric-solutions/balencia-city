# Balencia City v3 — Quality Rubric

Every asset must pass all applicable gates before moving to the next module. Exterior approvals require Gates 1-6 and 8; interior approvals require Gates 3-5 and 7; integration work must preserve the relevant exterior, interior, and energy checks.

## Gate 1: Silhouette Clarity [CRITICAL]
- [ ] Identifiable as its building type at 200px viewport height
- [ ] Unique outline among all 12 structures — no two silhouettes similar
- [ ] SIA Tower is unmistakably tallest from any angle
- [ ] Building has clear roofline/crown that differentiates it
- Test: Show silhouette with no label — viewer identifies function in 3 seconds

## Gate 2: Architectural Scale
- [ ] Reads as 20-40 floor megastructure (NOT a 3-story building)
- [ ] SIA Tower reads as 100+ floors (at least 2.5x tallest district)
- [ ] Floor plates or indicators visible on facade (bands, ledges, window grids)
- [ ] No building reads as "suburban" — all metropolitan scale
- [ ] 3+ distinct sub-elements visible (base, body, crown/roof)
- [ ] Complex multi-part structures have articulated primary volumes before detail approval — simple cuboid blockouts, flat slab bridges, or placeholder facade panels are not sufficient even when silhouette/scale pass

## Gate 3: Material System Compliance
- [ ] Materials use the 7-slot naming convention
- [ ] Surface area distribution within spec ranges (base 50-55%, etc.)
- [ ] Energy and holo slots present ONLY where specified in SPEC
- [ ] All material names match the runtime regex patterns
- [ ] No unnamed materials, no materials outside the 7-slot set

## Gate 4: Dark-First Test
- [ ] With all emissive at 0, structure reads as recognizable architectural form
- [ ] No surface appears bright or saturated when inactive
- [ ] District accent color appears ONLY on accent, emissive, energy, holo — never on base or detail
- [ ] Overall tone matches the Ink-900 (#0A0A0F) environment

## Gate 5: Technical Budget
- [ ] Triangle count within SPEC budget
- [ ] File size within SPEC budget (after Draco level 6)
- [ ] Origin at bottom-center, Y=0
- [ ] All transforms applied
- [ ] No cameras or lights in export (empties only for markers)
- [ ] GLB opens cleanly in Three.js GLTFLoader
- [ ] Triangle count represents real architectural articulation, not padding; unusually low utilization requires a documented design-intent exception or a geometry reinforcement pass

## Gate 6: Cohesion Check (after 2+ structures approved)
- [ ] Place alongside all previously approved structures at orbital positions
- [ ] Consistent material darkness with neighbors
- [ ] Consistent detail density (no building significantly flatter or busier)
- [ ] Scale relationships correct within the city
- [ ] All structures feel like they belong to the same civilization

## Gate 7: Interior-Specific
- [ ] Clear focal point (the center attention piece)
- [ ] Light empties sensibly placed at logical light source positions
- [ ] camera_target empty at room's focal point
- [ ] 4-8 props present, each identifiable
- [ ] Complete room shell (floor, walls, ceiling — one open/windowed wall)
- [ ] Interior materials use same 7-slot system as exterior

## Gate 8: Architectural Completion
- [ ] Exterior has a finished facade envelope: solid skin, glazing, panels, or layered surfaces behind any exposed frame or exoskeleton
- [ ] Base/plinth reads complete with visible entrance logic, threshold depth, civic edge, or district-specific ground connection
- [ ] Roof/crown reads resolved with parapets, cap, equipment, beacon, canopy, or district-specific terminal detail
- [ ] Floor/deck rhythm is believable from the app hero camera through mullions, bands, ledges, windows, terraces, or equivalent scale cues
- [ ] Exoskeletons, lattice, rails, and energy frames read as intentional finished architecture, not construction scaffolding or a temporary wireframe shell
- [ ] Primary app hero-camera view does not read as "under construction," "unfinished facade," "bare frame," or "placeholder shell"
- [ ] Detail improves real architectural articulation and preserves silhouette, origin, energy endpoints, and the 7-slot material system

## Energy Integration Check (after pipeline session)
- [ ] Pipeline connects cleanly from SIA crown to district
- [ ] Pipeline follows arced path (not straight line)
- [ ] Energy delivery style matches SPEC (hard/mist/thread/special)
- [ ] Ground veins radiate from pipeline endpoint
- [ ] Pipeline material named "energy" for runtime override

## Approval Workflow
1. Run full checklist above
2. ALL items pass → move GLB to `approved/`, update REVIEW.md with APPROVED + date
3. ANY item fails → note failures, return to modeling for targeted fixes
4. After fix → re-run FULL rubric (not just fixed items)
