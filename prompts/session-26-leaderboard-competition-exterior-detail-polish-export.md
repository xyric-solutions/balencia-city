# Session 26: Leaderboard & Competition -- Exterior Detail, Polish & Export

## Quick Context

- Project: Balencia City v3 -- interactive cinematic 3D city, not a website.
- Aesthetic: Blade Runner 2049 warmth + Apple spatial computing + UE5 archviz.
- Avoid: Lego proportions, neon overload, photorealism, daytime, cartoon, suburban scale.
- Sky: Ink-blue `#0A0A0F`; surfaces `#1E1E28`; fog warm amber.
- Brand mix: burnt orange `#FF5E00`, forest green `#34A853`, royal purple `#7F24FF`.
- SIA Tower is the 100+ floor center landmark; every district remains much shorter.
- Materials use the 7-slot runtime override system: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
- Export GLB with Draco level 6, Y-up, no cameras/lights, origin bottom-center.

## Session Scope

- Module: #06 Leaderboard & Competition -- Arena Colosseum.
- Position: Phase 3, Step 3.3.
- District color: Bright Coral `#FB7185` with orange and gold accents.
- Focus: Exterior detail, polish, dark-first proof, cohesion proof, and GLB export.
- Final exterior budget: 12K-18K triangles.
- Previous session tris: 10,720.
- Remaining budget: 7,280 triangles.
- Energy slot: yes.
- Holo slot: no.

## Previous Session State

- Blend file: `modules/06-leaderboard-competition/exterior/drafts/leaderboard-competition-s25-major-forms.blend`.
- Session 25 built the open-top arena colosseum major forms.
- Retained elements: 8-tier circular arena shell, visible seating bowl, thick open roof rim, grand arch, competitor walkway, four victory pillar beacon assemblies, curved leaderboard screen, and apex lightning receiver marker.
- Session 25 passed Gates 1-2.
- QA fix instructions: none.

## Architectural Identity

The building must read as a futuristic competition colosseum: wide, circular, open to the sky, visibly tiered, and civic in scale.

The open roof is the silhouette signature. The thick rim and exposed seating bowl must remain readable after detail is added.

The arena is the only circular open-top building in the city. It must not drift toward a generic stadium, tower, or dashboard object.

## Material Rules

- `base`: dark structural arena walls and major civic surfaces.
- `detail`: seating surfaces, pillar shafts, rim hardware, braces, collars.
- `glass`: dark facade gaps and shadowed openings.
- `accent`: inactive coral/gold trims, arch frame edges, walkway linework.
- `emissive`: beacon flame forms and leaderboard display elements.
- `energy`: apex lightning receiver, energy traces, and orange conduit details.
- `holo`: do not use for this module.

All mesh materials must resolve to the approved slot names. No unnamed or ad hoc materials are allowed.

## Detail Elements To Add

- Refined facade rhythm around the arena exterior.
- Segmented wall panels, floor index ticks, dark glass slit breaks, and vertical pilaster rhythm.
- Visible seating row breaks inside the bowl.
- Radial aisle lines and section breaks so the seating reads at distance.
- Rim engineering: underside trusses, bolt blocks, segmented coral rim lip.
- Apex receiver polish: collar rings, splayed rods, micro strike spire.
- Entry portal polish: inner energy trace, keystone, buttress blocks, turnstile hardware.
- Competitor walkway articulation: chevrons, lane ticks, ceremonial approach language.
- Leaderboard screen detail: frame arcs, scanline, rank glyphs, score ticks.
- Victory pillar hardware: collars, diagonal braces, beacon cage rods, heat fins.

## Build Workflow

1. Load the Session 25 blend file.
2. Remove old screenshot cameras/lights and run `shared/lighting-rig.py`.
3. Reuse or create the Balencia materials with `#FB7185`, `include_energy=True`, `include_holo=False`.
4. Normalize all mesh material slots to approved names.
5. Add facade rhythm details first, preserving the main arena silhouette.
6. Add seating and aisle articulation inside the bowl.
7. Add rim and apex receiver engineering.
8. Add entry portal and walkway detail.
9. Add leaderboard display glyph geometry.
10. Add victory pillar detail.
11. Keep final triangles within 12K-18K.
12. Capture front, three-quarter, distance, and dark-first screenshots.
13. Export a Draco-compressed draft GLB.
14. Promote the exported GLB to `exterior/approved/leaderboard-ext.glb` only after QA import checks pass.
15. Import the six previously approved exteriors and this approved arena GLB for a Gate 6 cohesion screenshot.

## Polish Checklist

- All objects have materials assigned.
- Material names match runtime slot names exactly.
- No default gray material remains.
- No `holo` material is used.
- Energy appears only at the apex receiver and energy trace accents.
- District coral appears only through `accent`, `emissive`, or energy-adjacent geometry.
- Open roof, seating bowl, grand entry arch, four beacons, and curved leaderboard remain readable.
- Detail does not distort the wide colosseum silhouette.
- Geometry is visually connected unless intentionally hovering.
- No cameras or lights are embedded in exported GLB.
- Mesh transforms are applied in export.
- Export origin is bottom-center.

## QA Gates

Gate 1: Silhouette remains a circular open-top arena with thick rim, beacon pillars, leaderboard display, and apex receiver.

Gate 2: Architectural scale remains civic/metropolitan: 8 tier bands, monumental arch, floor/tier indicators, and 3+ sub-elements.

Gate 3: Material compliance passes with only approved slots and no `holo`.

Gate 4: Dark-first test passes with emissions disabled.

Gate 5: Technical budget passes: 12K-18K tris, 100-350 KB GLB, origin bottom-center, no cameras/lights, clean GLB import.

Gate 6: Cohesion passes beside SIA, Fitness, Yoga, Finance, Knowledgebase, and Chat.

## Output Files

- Build script: `modules/06-leaderboard-competition/exterior/drafts/build-session-26.py`.
- Metrics: `modules/06-leaderboard-competition/exterior/drafts/session26-metrics.json`.
- QA import report: `modules/06-leaderboard-competition/exterior/drafts/session26-qa-import.json`.
- Blend: `modules/06-leaderboard-competition/exterior/drafts/leaderboard-competition-s26-detail-export.blend`.
- Draft GLB: `modules/06-leaderboard-competition/exterior/drafts/leaderboard-ext-draft-s26.glb`.
- Approved GLB: `modules/06-leaderboard-competition/exterior/approved/leaderboard-ext.glb`.
- Screenshots:
  - `screenshots/s26_front_elevation.png`
  - `screenshots/s26_three_quarter.png`
  - `screenshots/s26_distance_view.png`
  - `screenshots/s26_dark_first.png`
  - `screenshots/s26_cohesion_all7.png`

## Post-Session Review Update

Append Session 26 to `modules/06-leaderboard-competition/REVIEW.md`.

Record:

- Object/category metrics.
- Final triangle count and GLB size.
- Material slot usage.
- Blend, draft GLB, approved GLB, metrics, and QA report paths.
- Screenshots captured.
- Detail elements added.
- Any QA exceptions.

If all gates pass, mark:

- Exterior Status: Session 26 Complete -- QA APPROVED.
- Exterior Approved: yes, dated 2026-05-24.

Then update `PROGRESS.md` to advance to Session 27 interior.
