# Session 25: Leaderboard & Competition -- Exterior Major Forms

## Quick Context

- Project: Balencia City v3, an interactive cinematic 3D city, not a website.
- Aesthetic: Blade Runner 2049 warmth, Apple spatial computing, UE5 archviz.
- Scene tone: dark premium night, ink-blue sky `#0A0A0F`, warm amber fog.
- Brand balance: burnt orange energy, forest green success accents, royal purple AI accents.
- Material system: slot names must be exactly `base`, `accent`, `glass`, `detail`, `emissive`, `energy`; no `holo` for this module.
- SIA Tower remains the 40u / 100+ floor scale anchor. This district must stay clearly shorter.
- Current module: #06 Leaderboard & Competition.
- Current phase: Phase 3, Step 3.3, exterior major forms.
- Current session: 25.

## Session Scope

- District color: Bright Coral `#FB7185`, with orange/gold energy accents through approved slots only.
- Floors: 8 arena decks, wide and short rather than tower-like.
- Exterior budget: 12K-18K tris.
- Major-form target: stay under 60% of max budget, below 10,800 tris.
- This session builds silhouette geometry only.
- Next session adds facade detail, polish, decimation, export, and full exterior QA.

## Architectural Identity

The Leaderboard district is a futuristic open-top colosseum. It is circular in plan,
rising through stepped tiers with a visible bowl inside. The building must read as
the only arena in Balencia City: wide footprint, low crown, exposed top, and four
victory pillars at the cardinal points.

Its silhouette must not be confused with any prior module:

- SIA Tower is a single central spire.
- Fitness is an angular gym megastructure.
- Yoga is floating organic domes.
- Finance is crystalline and faceted.
- Knowledgebase is a library cathedral.
- Chat is a connected multi-tower signal hub.
- Leaderboard must read as an arena colosseum from 200px height.

## Required Major Forms

Build these primary forms now:

1. Circular colosseum main structure with 8 rising tier bands.
2. Visible tiered seating bowl inside the open roof.
3. Open roof with no ceiling and a thick structural rim ring.
4. Oversized grand entrance archway on the primary face.
5. Four victory pillars at the cardinal points.
6. Coral/orange energy beacons at the victory pillar tops.
7. Curved leaderboard display wrapping roughly 90 degrees of the exterior wall.
8. Raised competitor walkway leading to the grand entrance.
9. Energy lightning entry point at the open apex.
10. A top rim ring that makes the open roof unmistakable.

## Proportion Guidance

- Use a large footprint, roughly 18u across including rim and pillar bases.
- Main arena rim height should be roughly 6.5u.
- Victory beacons may rise to roughly 9u-10u for skyline readability.
- The building should feel like a metropolitan stadium, not a small sports field.
- SIA remains more than 2.5x taller than the tallest Leaderboard element.
- The open top is the defining feature; keep the center void readable.

## Material Assignment

| Surface | Slot | Notes |
| --- | --- | --- |
| Colosseum main walls | `base` | Dark structural material |
| Tiered seating surfaces | `detail` | Slightly lighter internal ring geometry |
| Facade gaps between tiers | `glass` | Dark tinted openings |
| Grand entrance archway frame | `accent` | Faint coral edge emission |
| Victory pillars | `detail` | Tall narrow structural metal |
| Energy beacons at pillar tops | `emissive` and `energy` | Coral/orange glow using approved slots |
| Leaderboard display panel | `emissive` | Curved screen surface |
| Competitor walkway surface | `base` and `accent` | Dark raised path with coral edges |
| Structural rim ring at top | `detail` | Thick torus defining roof edge |
| Energy lightning entry zone | `energy` | Orange strike/socket at center |

## Workflow

1. Save any currently dirty Blender scene before clearing.
2. Clear the scene with factory settings.
3. Run `shared/lighting-rig.py`.
4. Run `shared/material-library.py` with `#FB7185`, `include_energy=True`, `include_holo=False`.
5. Verify 3 lights, 1 camera, and 6 material slots.
6. Build the arena shell before any secondary forms.
7. Build the inner stepped seating bowl.
8. Add the top structural rim ring.
9. Add the entrance arch and raised walkway on the front face.
10. Add the 4 cardinal victory pillars and beacons.
11. Add the curved leaderboard display panel.
12. Add only a major-form lightning receiver, not the final pipeline.
13. Capture front, three-quarter, and distance screenshots.
14. Save the `.blend` in `modules/06-leaderboard-competition/exterior/drafts/`.
15. Record object metrics and screenshots in `REVIEW.md`.

## Gate 1 Self-Check

- At thumbnail size, the model must read as a circular open arena.
- The four victory pillars should create a cross-pattern from above and a beacon skyline from the side.
- The thick top rim and center void must be obvious.
- The curved leaderboard panel should reinforce competition rather than read like a normal screen facade.
- The silhouette must be distinct from the Chat cluster and the upcoming Career tower cluster.

## Gate 2 Self-Check

- The arena must feel civic and metropolitan in footprint.
- Eight deck bands must read as floor/seat tiers.
- The structure needs at least base, bowl/body, rim/crown, entrance, and pillar/beacon sub-elements.
- The tallest beacon should remain far below the SIA Tower.
- Avoid a suburban stadium feel by using large massing, strong rim thickness, and monumental entrance scale.

## Do Not Build Yet

- No final GLB export.
- No detailed facade trim, dense row markers, score text, or small railing details.
- No interior competition floor props.
- No final SIA-to-Leaderboard energy pipeline.
- No decorative confetti or celebration particles.
- No downloading external models.

## Expected Output

- `exterior/drafts/build-session-25.py`
- `exterior/drafts/leaderboard-competition-s25-major-forms.blend`
- `exterior/drafts/session25-metrics.json`
- `screenshots/s25_front_elevation.png`
- `screenshots/s25_three_quarter.png`
- `screenshots/s25_distance_view.png`
- Updated `REVIEW.md` with build and QA entries.
- Updated `PROGRESS.md` only after Gates 1-2 pass.
