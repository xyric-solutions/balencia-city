# Session 76: Final Phase 8 City QA, Contact Sheets, Performance Review

## Session Scope

- **Phase**: 8.8 City Spread And Exterior Finish
- **Focus**: Close Phase 8 with final city QA evidence after all exterior polish waves
- **Inputs**: Current approved structure exteriors, current approved interiors for verification metrics, current approved energy GLBs, `shared/city-layout-v2.json`, and the Vite/R3F app
- **Do not modify**: Approved GLB geometry, city-layout-v2 positions, scroll camera data, approved interiors, or baked energy endpoints

## Context

Sessions 69-70 spread the city into layout v2 and rebaked the assembly/energy system. Sessions 71-75 then polished all 12 approved exteriors to the Phase 8 finish bar:

- Session 71: SIA Tower pilot polish
- Session 72: Fitness and Finance polish
- Session 73: Yoga, Recovery, and Relationships organic polish
- Session 74: Knowledgebase, Chat, and Career urban polish
- Session 75: Leaderboard, AI Analytics, and Nutrition signature polish

Session 76 is not a modeling pass. It is the evidence and closure pass that verifies the full city now reads as a finished, spacious, premium 3D environment across assembly evidence and app runtime checks.

## Build Requirements

1. Audit all 12 current approved exterior GLBs.
2. Audit all 12 current approved interior GLBs for hidden/on-demand verification metrics.
3. Audit all 7 approved energy GLBs.
4. Confirm every imported material root is in the approved 7-slot set: `base`, `accent`, `glass`, `detail`, `emissive`, `energy`, `holo`.
5. Confirm all structure placements match `shared/city-layout-v2.json`.
6. Confirm minimum district-center spacing remains at or above 36u.
7. Confirm SIA Tower remains visually dominant over all districts.
8. Confirm active city triangles remain under the 250K Phase 8 cap.
9. Render a refreshed 12-structure exterior contact sheet.
10. Render refreshed city overview evidence from citywide, top-down, four skyline, and energy climax views.
11. Build a city overview contact sheet from the refreshed overview renders.
12. Render required scroll verification frames for the final app-facing views: Scenes 1, 4, 6, 11, 15, 16, and 17.
13. Write `assembly/audit/session-76-final-phase-8-city-qa.json`.
14. Write `assembly/audit/session-76-final-phase-8-city-qa.md`.
15. Write `assembly/performance-reports/session-76-performance.json`.
16. Run `npm run build` in `apps/balencia`.
17. Run local app/model HTTP checks.
18. Run browser smoke across target scenes with canvas, label/overlay, and console checks where the browser is available.

## QA Gates

| Gate | Pass Criteria |
|------|---------------|
| Asset presence | 12 exteriors, 12 interiors, and 7 energy assets exist and import cleanly |
| Material roots | No material roots outside the approved 7-slot set |
| Layout spread | Minimum district-center spacing is at least 36u |
| Active budget | Current exteriors + approved energy + city context remain below 250K tris |
| Source budget | Active exterior + energy source GLBs remain below 5 MB |
| SIA dominance | SIA Tower height remains at least 2x the tallest district |
| Evidence | Exterior sheet, city overview sheet, overview stills, and scroll frames are nonblank |
| App build | TypeScript and Vite build pass |
| Runtime smoke | Required target scenes load with a nonblank WebGL canvas and no warning/error console logs |

## Expected Outputs

- `assembly/drafts/build-session-76-final-phase-8-city-qa.py`
- `assembly/audit/session-76-final-phase-8-city-qa.json`
- `assembly/audit/session-76-final-phase-8-city-qa.md`
- `assembly/performance-reports/session-76-performance.json`
- `assembly/screenshots/s76-exterior-finish-contact-sheet.png`
- `assembly/screenshots/s76-city-overview-contact-sheet.png`
- `assembly/screenshots/s76-overview-*.png`
- `assembly/scroll-verification/session-76/scene-*.png`
- `apps/balencia/SESSION-76-REPORT.md`

## Acceptance Criteria

- Session 76 report is approved or clearly labels any residual risk.
- Phase 8 backlog is updated to mark final city QA complete only if all required gates pass.
- `PROGRESS.md` frontmatter advances to Session 76 only after executed QA passes.
- `BUILD-ORDER.md` marks Phase 8.8 complete only after executed QA passes.
- No approved GLB geometry is changed during the QA pass.
