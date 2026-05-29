# Session 74 Report: Urban Exterior Polish Wave

Date: 2026-05-26
Status: Approved

## Summary

Session 74 completed Phase 8.6. It polished the approved Knowledgebase, Chat, and Career exterior GLBs to the Phase 8 finish bar, promoted all three v2 assets to their approved and app model paths, and preserved city-layout-v2 placement, origins, and baked energy route assumptions.

## Changes

- Added `assembly/drafts/build-session-74-urban-polish.py`.
- Added `assembly/drafts/cleanup-session-74-knowledgebase-root.py`.
- Added `prompts/session-74-knowledge-chat-career-urban-polish-wave.md`.
- Generated `assembly/audit/session-74-urban-polish.json` and `assembly/audit/session-74-urban-polish.md`.
- Promoted Knowledgebase v2 to `modules/04-knowledgebase/exterior/approved/knowledgebase-ext.glb` and the app public model path.
- Promoted Chat v2 to `modules/05-chat-communication/exterior/approved/chat-ext.glb` and the app public model path.
- Promoted Career v2 to `modules/08-career/exterior/approved/career-ext.glb` and the app public model path.
- Rendered module evidence screenshots and `assembly/screenshots/s74-exterior-finish-contact-sheet.png`.

## Results

| Module | Previous | Session 74 |
|--------|----------|------------|
| Knowledgebase | 7,532 tris, 357 objects, 357.0 KB | 15,204 tris, 7 objects, 102.0 KB |
| Chat & Communication | 18,580 tris, 192 objects, 300.0 KB | 20,052 tris, 7 objects, 158.1 KB |
| Career | 19,692 tris, 175 objects, 239.5 KB | 20,288 tris, 6 objects, 113.4 KB |

## QA

| Check | Result |
|-------|--------|
| Knowledgebase v2 import validation | PASS |
| Knowledgebase v2 material validation | PASS |
| Knowledgebase v2 camera/light export check | PASS |
| Knowledgebase v2 clean root check | PASS - one root named `knowledgebase-ext` |
| Knowledgebase v2 budget | PASS - 15,204 tris / 102.0 KB |
| Chat v2 import validation | PASS |
| Chat v2 material validation | PASS |
| Chat v2 camera/light export check | PASS |
| Chat v2 budget | PASS - 20,052 tris / 158.1 KB |
| Career v2 import validation | PASS |
| Career v2 material validation | PASS |
| Career v2 camera/light export check | PASS |
| Career v2 budget | PASS - 20,288 tris / 113.4 KB |
| `npm run build` | PASS - existing Vite large-chunk warning and Node deprecation warning only |
| Local asset HTTP checks | PASS - app route plus all three promoted GLBs returned HTTP 200 with expected content lengths |

## Artifacts

| Artifact | Path |
|----------|------|
| Build script | `assembly/drafts/build-session-74-urban-polish.py` |
| Cleanup script | `assembly/drafts/cleanup-session-74-knowledgebase-root.py` |
| Wave report | `assembly/audit/session-74-urban-polish.md` |
| Knowledgebase metrics | `modules/04-knowledgebase/exterior/drafts/session74-v2-metrics.json` |
| Knowledgebase QA import | `modules/04-knowledgebase/exterior/drafts/session74-qa-import.json` |
| Chat metrics | `modules/05-chat-communication/exterior/drafts/session74-v2-metrics.json` |
| Chat QA import | `modules/05-chat-communication/exterior/drafts/session74-qa-import.json` |
| Career metrics | `modules/08-career/exterior/drafts/session74-v2-metrics.json` |
| Career QA import | `modules/08-career/exterior/drafts/session74-qa-import.json` |
| Contact sheet | `assembly/screenshots/s74-exterior-finish-contact-sheet.png` |

## Next

Session 75 should polish Leaderboard, AI Analytics, and Nutrition so the remaining signature districts reach the same Phase 8 finish bar.
