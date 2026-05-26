# Session 70 Report: Assembly And Energy Layout v2 Rebase

Date: 2026-05-26
Status: Approved

## Summary

Session 70 completed the Phase 8.2 layout rebase. The Blender assembly and all baked endpoint energy GLBs now read from `shared/city-layout-v2.json`, so the approved energy assets match the wider spread city instead of the tighter Session 56 layout.

## Changes

- Added `assembly/drafts/build-session-70-layout-v2-rebase.py`.
- Rebuilt the approved hard pipelines, warm mist, faint thread, Knowledgebase waterfall, Leaderboard lightning, cross-district gold, and AI pulse GLBs from the layout-v2 district positions.
- Rebuilt `assembly/drafts/full-city-assembly.blend` with all 12 approved exteriors, hidden interiors, layout-v2 city context, and the rebaked approved energy assets.
- Rendered Session 70 assembly evidence: 7 overview screenshots and 17 scroll-verification screenshots under `assembly/scroll-verification/session-70/`.
- Restored baked energy rendering in the R3F app via `Approved_Energy_Layout_V2_Rebake` and preloaded energy GLB paths separately from structure exteriors.
- Bumped the app asset manifest session to 70 and synced the rebuilt GLBs into `apps/balencia/public/models/energy/`.

## QA

| Check | Result |
|-------|--------|
| Energy rebake report | APPROVED |
| Assembly report | APPROVED |
| Minimum district spacing | PASS - 36.4005u |
| Active city tris | PASS - 176,183 / 250,000 |
| Active source GLB bytes | PASS - 2,317,040 / 5,242,880 |
| SIA dominance | PASS - 2.1841x |
| Overview screenshots | PASS - 7 / 7 nonzero |
| Scroll verification screenshots | PASS - 17 / 17 nonzero |
| `npm run build` | PASS |
| Browser smoke | PASS - canvas present, Scene 15 copy reached, no warning/error logs |

Known notes: Vite still reports the existing large client chunk warning, Node still emits the existing `module.register()` deprecation warning, and in-app browser screenshot capture timed out again. Blender screenshot evidence completed successfully.

## Artifacts

| Artifact | Path |
|----------|------|
| Energy report | `energy-system/pipelines/drafts/energy-layout-v2-session70-report.json` |
| Assembly report | `assembly/drafts/full-city-assembly-session70-report.json` |
| Performance report | `assembly/performance-reports/session-70-performance.json` |
| Assembly blend | `assembly/drafts/full-city-assembly.blend` |
| Overview screenshots | `assembly/screenshots/s70-*.png` |
| Scroll screenshots | `assembly/scroll-verification/session-70/` |

## Next

Session 71 should start the exterior finish audit and SIA pilot polish pass.
