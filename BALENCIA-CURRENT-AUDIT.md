# Balencia Current-State Audit Report

Date: 2026-05-26  
Scope: current approved Balencia City v3 assets, layout-v2 app integration, labels, hover/click metadata, camera readability, interior reveals, and 17-scene scroll flow.  
Mode: audit only. No bugs were fixed and no app/model/progress files were changed.

## Executive Summary

Balencia City is asset-complete but not final-experience-complete. The GLB library and Phase 8 assembly are strong: all 12 exteriors, all 12 interiors, 11 / 11 pipelines, cross-district connections, AI pulse, and final city QA are recorded as approved. The current risk is the React Three Fiber app layer that stitches those assets into a user-facing journey.

Overall current-state grade: **6.4 / 10**

- Asset/model library quality: **8.2 / 10**. The v2 exterior polish waves materially improved finish, density, and city cohesion.
- App interaction quality: **4.6 / 10**. Only 5 of 12 structures have hover/click targets, and those targets remain mounted in scenes where they are irrelevant or offscreen.
- Camera/scroll journey quality: **5.8 / 10**. Scene sequencing exists, but interior reveals often read as close exterior views or abstract fragments rather than smooth, intentional entries.
- Label/text placement quality: **5.9 / 10**. Text content is mostly correct, but label placement is hard-coded in screen space and can drift away from actual structures.

Current handoff verdict: **Not final-demo ready.** The city is approved as an asset assembly, but the app needs a focused interaction, label, and camera pass before a user review should treat it as polished.

## Evidence Reviewed

- Project status and build history: `PROGRESS.md`
- Formal build rubric: `QUALITY-RUBRIC.md`
- Intended 17-scene journey: `SCROLL-JOURNEY.md`
- Final Phase 8 QA: `assembly/audit/session-76-final-phase-8-city-qa.md`
- Final app QA report: `apps/balencia/SESSION-76-REPORT.md`
- Runtime metadata and label source: `apps/balencia/src/lib/district-metadata.ts`
- Camera and scene source: `apps/balencia/src/lib/scroll-scenes.ts`
- Interaction layer source: `apps/balencia/src/components/scenes/BuildingInteractionLayer.tsx`
- Label rendering source: `apps/balencia/src/components/scenes/CityContext.tsx`
- Existing visual artifacts under `assembly/screenshots/`, `assembly/scroll-verification/`, and `output/playwright/`
- User-provided screenshots showing overview label drift, Knowledgebase/Finance hover mismatch, SIA interior readability failure, and Fitness close-up framing
- Live app DOM survey at `http://localhost:3006/`

Browser screenshot limitation: in-app screenshot capture failed during this audit with `Page.captureScreenshot` timeout. This matches prior session notes. The live browser survey still succeeded for DOM, scene state, hit areas, product overlay state, and console warnings/errors.

Live browser console result: **0 warnings/errors** during the audit survey.

## Top Blockers

| Priority | Finding | Impact | Recommendation |
|---|---|---|---|
| P0 | Only 5 / 12 structures are interactive: SIA, Fitness, Finance, Relationships, Career. | Most buildings do not show hover information, matching the user's report. | Add interaction targets and preview metadata for all structures, or intentionally disable hover globally until coverage is complete. |
| P0 | Interaction targets are not scene-gated. | Users can hover or click invisible/unrelated hit areas and see the wrong district panel. This plausibly explains Knowledgebase showing finance-related content. | Gate targets by active scene/visibility and align each hit area to the visible model and label. |
| P0 | SIA Tower interior does not read as an interior. | Scene 3 says "Inside SIA tower" but visually reads as a close, abstract, poorly framed core object. | Rebuild Scene 3 camera path and lighting around a clear entrance, atrium, city model, walls, and readable focal hierarchy. |
| P1 | Overview labels are hard-coded screen percentages. | Labels can look detached from actual structures after viewport/camera/layout changes. | Derive labels from projected 3D anchors or maintain a camera-specific label QA pass with stronger tethering. |
| P1 | Exterior-to-interior flow is not convincingly smooth. | Scroll often moves close to a building but does not make the user feel they entered it. | Audit each scene at start, midpoint, and interior threshold; tune camera, clipping, active interior mounting, and lighting. |
| P1 | Current evidence pipeline cannot reliably capture live app screenshots. | Visual QA depends too much on manual screenshots and DOM checks. | Add a stable screenshot path or fallback browser harness before final QA. |

## Scoring Rubric

Each structure is scored out of 10:

| Category | Max |
|---|---:|
| Model craft/spec compliance | 2.0 |
| Placement/scale/city integration | 1.5 |
| Label and text accuracy | 1.5 |
| Hover/click metadata | 1.5 |
| Camera/interior readability | 2.0 |
| Narrative/flow contribution | 1.5 |

Priority meanings:

- **P0 blocker**: must be fixed before a serious demo or review.
- **P1 high-impact**: should be grouped into near-term repair sessions.
- **P2 polish**: good candidate after blockers are resolved.
- **P3 optional**: acceptable as-is unless time allows.

## Structure Ranking

| Rank | Structure | Score | Priority | Main Reason |
|---:|---|---:|---|---|
| 1 | Career towers | 7.9 | P1 | Strong v2 model, interactive, and readable camera; still affected by global label/target issues. |
| 2 | Finance bank | 7.8 | P1 | Strong model and interactive preview, but stale hit areas can create cross-district hover confusion. |
| 3 | Fitness complex | 7.5 | P1 | Strong v2 model and interaction, but app camera can get too close and flatten the district read. |
| 4 | Relationships garden | 7.2 | P1 | Good model and interaction, but label/board elevation and camera flow need tuning. |
| 5 | SIA Tower | 6.9 | P0 | Asset is central and approved, but Scene 3 interior is a major experience blocker. |
| 6 | AI analytics | 6.2 | P1 | Strong model and scene concept, but no hover target and interior proof is weak in current app. |
| 7 | Leaderboard / Competition | 6.2 | P1 | Strong arena model, but no hover target and active scene still carries unrelated targets. |
| 8 | Yoga sanctuary | 6.1 | P1 | Strong organic model, but no hover target and app scene can expose unrelated hit areas. |
| 9 | Nutrition farm | 6.1 | P1 | Strong model, but no hover target and interior transition needs visual confirmation. |
| 10 | Chat hub | 5.9 | P1 | Good approved model, but no hover target despite being used for product scene context. |
| 11 | Recovery and sleep | 5.9 | P1 | Good approved model, but no hover target and faint/ethereal scene needs stronger readable framing. |
| 12 | Knowledgebase library | 5.7 | P0 | No hover target, user-observed metadata mismatch, and label/interaction alignment is the clearest bug report. |

## Per-Structure Audit

### 00 - SIA Tower

Score: **6.9 / 10**  
Priority: **P0 blocker**

| Category | Score |
|---|---:|
| Model craft/spec compliance | 1.55 / 2.0 |
| Placement/scale/city integration | 1.30 / 1.5 |
| Label and text accuracy | 1.05 / 1.5 |
| Hover/click metadata | 1.25 / 1.5 |
| Camera/interior readability | 0.70 / 2.0 |
| Narrative/flow contribution | 1.05 / 1.5 |

Issues:

- Scene 3 is the biggest current experience failure. It enters the `interior` state and mounts the SIA interior, but the image reads as a close abstract core, not as a tower interior or neural atrium.
- The intended journey says Scene 3 should push through the entrance and rise through the atrium; the current view does not communicate entrance, walls, platforms, city model, or spatial scale clearly enough.
- In Scene 3, active label boards are intentionally hidden, so there is no visual label reinforcement while the camera is already confusing.
- The SIA hit area becomes very large in Scene 3, which can make the interaction feel like an invisible overlay rather than a precise building target.
- SIA still has a documented Phase 8 density exception versus later polished districts. It remains approved, but it should not be treated as the strongest model craft example.

Recommendations:

- First repair session should focus on Scene 3 only: rebuild the camera path, lighting, target, and interior composition until it unmistakably reads as "inside SIA Tower."
- Add a labeled/focal interior cue for Scene 3, even if overview labels remain hidden.
- Verify SIA interior at three scroll positions: scene start, interior midpoint, and transition out.

### 01 - Fitness Complex

Score: **7.5 / 10**  
Priority: **P1 high-impact**

| Category | Score |
|---|---:|
| Model craft/spec compliance | 1.75 / 2.0 |
| Placement/scale/city integration | 1.20 / 1.5 |
| Label and text accuracy | 1.10 / 1.5 |
| Hover/click metadata | 1.20 / 1.5 |
| Camera/interior readability | 1.10 / 2.0 |
| Narrative/flow contribution | 1.15 / 1.5 |

Issues:

- The v2 exterior is substantially improved and reads as a strong green athletic structure in the asset evidence.
- User screenshot of Scene 4 shows the live app camera pressed very close into the facade, with horizontal green bars dominating the entire frame. This reduces the sense of approach and district scale.
- Fitness is interactive, but other unrelated targets remain present in the scene. The live survey showed all five app targets in viewport during Scene 4.
- Interior transition is configured in source, but the current review did not produce reliable live screenshots to prove the interior read at the threshold.

Recommendations:

- Tune Scene 4 start and interior threshold framing so the exterior reads first, then the camera enters intentionally.
- Gate non-Fitness interaction targets while Fitness is the active district, or make them visibly and spatially meaningful.
- Add a QA shot for the actual interior threshold, not only the exterior establishing view.

### 02 - Yoga Sanctuary

Score: **6.1 / 10**  
Priority: **P1 high-impact**

| Category | Score |
|---|---:|
| Model craft/spec compliance | 1.70 / 2.0 |
| Placement/scale/city integration | 1.25 / 1.5 |
| Label and text accuracy | 1.00 / 1.5 |
| Hover/click metadata | 0.00 / 1.5 |
| Camera/interior readability | 1.05 / 2.0 |
| Narrative/flow contribution | 1.05 / 1.5 |

Issues:

- Model quality is solid after prior geometry and organic polish passes.
- Yoga has preview metadata in `DISTRICT_PROFILES`, but `interactionTarget` is false, so it does not expose hover/click information in the app.
- Live Scene 5 survey showed Yoga's active board, but no Yoga hit area. Finance and Relationships hit areas were in viewport instead, creating wrong-hover risk.
- Overview label is hand-placed and not projected from the actual dome/sanctuary geometry.

Recommendations:

- Add Yoga to the interaction target set with a hit area aligned to the visible sanctuary.
- Verify warm-mist delivery remains readable without overpowering the calm scene.
- Capture a midpoint view that proves the transition into the yoga dome, not just the exterior.

### 03 - Finance Bank

Score: **7.8 / 10**  
Priority: **P1 high-impact**

| Category | Score |
|---|---:|
| Model craft/spec compliance | 1.85 / 2.0 |
| Placement/scale/city integration | 1.25 / 1.5 |
| Label and text accuracy | 1.10 / 1.5 |
| Hover/click metadata | 1.10 / 1.5 |
| Camera/interior readability | 1.25 / 2.0 |
| Narrative/flow contribution | 1.20 / 1.5 |

Issues:

- Finance v2 is one of the stronger model updates: the crystalline gold tower has clear identity and strong detail density.
- Finance is interactive and has preview metadata, but the target remains active outside the Finance scene.
- The user-observed Knowledgebase/Finance hover mismatch is plausible because Finance is one of the only interactive targets while Knowledgebase is not.
- During several non-Finance scenes, Finance hit areas were either in viewport or mounted offscreen. This makes it too easy for Finance metadata to leak into unrelated areas.

Recommendations:

- Keep the Finance preview content, but make its hit area scene-aware.
- Add a regression test: hovering Knowledgebase should never show Finance text.
- Confirm Finance interior threshold with a live visual capture once screenshot tooling is stable.

### 04 - Knowledgebase Library

Score: **5.7 / 10**  
Priority: **P0 blocker**

| Category | Score |
|---|---:|
| Model craft/spec compliance | 1.65 / 2.0 |
| Placement/scale/city integration | 1.15 / 1.5 |
| Label and text accuracy | 0.85 / 1.5 |
| Hover/click metadata | 0.00 / 1.5 |
| Camera/interior readability | 0.95 / 2.0 |
| Narrative/flow contribution | 1.05 / 1.5 |

Issues:

- The model is approved and had a Phase 8 material-slot repair in Session 76, but its app experience is currently one of the weakest.
- Knowledgebase has preview metadata but `interactionTarget` is false. It cannot directly show its own hover/click panel.
- The user reports clicking or hovering Knowledgebase and seeing finance-related information. The app source supports this failure mode: Finance is interactive, Knowledgebase is not, and stale targets remain mounted across scenes.
- Scene 7 shows an active Knowledgebase board, but the live survey found only Relationships and Career hit areas in viewport; SIA/Fitness/Finance targets remained mounted offscreen.
- Overview label placement is hard-coded and can visually detach from the actual model.

Recommendations:

- Treat Knowledgebase hover/click repair as P0 with SIA interior.
- Add Knowledgebase to the interaction target set and align its hit area to the model/crown/base.
- Add explicit QA: hover/click Knowledgebase in overview and Scene 7 must show `Learning queue tuned` and never Finance copy.
- Recheck Knowledgebase label position in Scene 1, Scene 7, Scene 15, and Scene 17.

### 05 - Chat Hub

Score: **5.9 / 10**  
Priority: **P1 high-impact**

| Category | Score |
|---|---:|
| Model craft/spec compliance | 1.75 / 2.0 |
| Placement/scale/city integration | 1.15 / 1.5 |
| Label and text accuracy | 0.95 / 1.5 |
| Hover/click metadata | 0.00 / 1.5 |
| Camera/interior readability | 0.95 / 2.0 |
| Narrative/flow contribution | 1.05 / 1.5 |

Issues:

- The approved model recovered from early blockout status and now has a strong signal-tower identity.
- Chat has preview metadata but no interaction target.
- Scene 8 shows the Chat active board, but live survey found SIA, Relationships, and Career hit areas in viewport instead of a Chat target.
- Scene 16 uses Chat as the active district for the product-reality corridor, yet the automatic board is hidden and Chat itself is not directly interactive.

Recommendations:

- Add Chat interaction support and make sure it does not interfere with the product phone overlay in Scene 16.
- Verify Scene 8 exterior sweep and interior nexus push at multiple scroll positions.
- Clarify whether Scene 16 should remain "chat district" internally or use a neutral product/street context to avoid confusing metadata.

### 06 - Leaderboard / Competition Arena

Score: **6.2 / 10**  
Priority: **P1 high-impact**

| Category | Score |
|---|---:|
| Model craft/spec compliance | 1.80 / 2.0 |
| Placement/scale/city integration | 1.20 / 1.5 |
| Label and text accuracy | 0.95 / 1.5 |
| Hover/click metadata | 0.00 / 1.5 |
| Camera/interior readability | 1.05 / 2.0 |
| Narrative/flow contribution | 1.15 / 1.5 |

Issues:

- The arena model has strong silhouette and lightning identity.
- Leaderboard has preview metadata but no interaction target.
- Live Scene 9 survey showed the Leaderboard board, but Fitness and Relationships hit areas were in viewport instead.
- The label says "Competition arena" while scene/metadata naming mixes "Leaderboard", "Competition", and "Competition arena"; this is understandable but should be standardized before final copy QA.

Recommendations:

- Add an interaction target to the arena bowl/apex region.
- Standardize naming across label, overlay, preview, and nav: decide between "Competition arena" and "Leaderboard and competition."
- Confirm lightning entry remains visible in both exterior and interior push.

### 07 - Relationships Garden

Score: **7.2 / 10**  
Priority: **P1 high-impact**

| Category | Score |
|---|---:|
| Model craft/spec compliance | 1.75 / 2.0 |
| Placement/scale/city integration | 1.20 / 1.5 |
| Label and text accuracy | 0.95 / 1.5 |
| Hover/click metadata | 1.05 / 1.5 |
| Camera/interior readability | 1.05 / 2.0 |
| Narrative/flow contribution | 1.15 / 1.5 |

Issues:

- The garden/pavilion model reads well in the approved asset evidence.
- Relationships is interactive and can show its own preview.
- The profile uses unusually high `labelLift` and board direction tuning; labels may feel detached depending on camera.
- In several non-Relationships scenes, the Relationships hit area appears in viewport and can become an unrelated target.

Recommendations:

- Keep Relationships interaction but gate it to relevant overview and focus contexts.
- Re-evaluate board/label height so it feels attached to the low garden form.
- Confirm Scene 10 interior garden push is visually distinct from an exterior close-up.

### 08 - Career Towers

Score: **7.9 / 10**  
Priority: **P1 high-impact**

| Category | Score |
|---|---:|
| Model craft/spec compliance | 1.85 / 2.0 |
| Placement/scale/city integration | 1.25 / 1.5 |
| Label and text accuracy | 1.15 / 1.5 |
| Hover/click metadata | 1.15 / 1.5 |
| Camera/interior readability | 1.25 / 2.0 |
| Narrative/flow contribution | 1.25 / 1.5 |

Issues:

- Career is one of the strongest combined model/app structures right now.
- It has an interaction target, strong model identity, and a readable district concept.
- Career target still remains mounted across unrelated scenes. In the live survey it appeared offscreen or in viewport in many non-Career scenes.
- Scene 11 should still be checked at the interior threshold to prove the command hub appears clearly.

Recommendations:

- Use Career as a reference for the quality level other interactive districts should reach.
- Gate Career interaction outside overview/Scene 11.
- Reuse its preview-panel pattern for the seven non-interactive districts.

### 09 - Recovery and Sleep

Score: **5.9 / 10**  
Priority: **P1 high-impact**

| Category | Score |
|---|---:|
| Model craft/spec compliance | 1.75 / 2.0 |
| Placement/scale/city integration | 1.15 / 1.5 |
| Label and text accuracy | 0.95 / 1.5 |
| Hover/click metadata | 0.00 / 1.5 |
| Camera/interior readability | 0.95 / 2.0 |
| Narrative/flow contribution | 1.05 / 1.5 |

Issues:

- Recovery is approved and has a distinct low, ethereal silhouette.
- It has no hover/click target despite having preview metadata.
- Scene 12 live survey showed only a Fitness hit area in viewport and the remaining five app targets mounted offscreen. Recovery itself was not interactive.
- The faint-thread concept can be visually subtle, so camera and label support need to work harder than they do for larger tower districts.

Recommendations:

- Add Recovery interaction with a larger but accurately anchored target around the cloud/lake form.
- Verify the faint thread and interior recovery chamber are readable without making the scene visually noisy.
- Add a dedicated Scene 12 midpoint screenshot once capture tooling is repaired.

### 10 - AI Analytics

Score: **6.2 / 10**  
Priority: **P1 high-impact**

| Category | Score |
|---|---:|
| Model craft/spec compliance | 1.80 / 2.0 |
| Placement/scale/city integration | 1.20 / 1.5 |
| Label and text accuracy | 0.95 / 1.5 |
| Hover/click metadata | 0.00 / 1.5 |
| Camera/interior readability | 1.05 / 2.0 |
| Narrative/flow contribution | 1.15 / 1.5 |

Issues:

- The data cathedral model is strong and has clear teal identity.
- Analytics has preview metadata but no interaction target.
- Scene 13 live survey showed SIA, Fitness, and Finance hit areas in viewport instead of Analytics.
- The scene concept is important narratively, but without direct interaction and stronger interior proof it currently feels less discoverable than Finance/Career.

Recommendations:

- Add Analytics interaction target around the cathedral body/spire.
- Verify the Data Sanctum interior push reads as "where SIA thinks", not just an exterior fly-by.
- Give Analytics a clear label/preview treatment because it is conceptually central to the product story.

### 11 - Nutrition Farm

Score: **6.1 / 10**  
Priority: **P1 high-impact**

| Category | Score |
|---|---:|
| Model craft/spec compliance | 1.80 / 2.0 |
| Placement/scale/city integration | 1.20 / 1.5 |
| Label and text accuracy | 0.95 / 1.5 |
| Hover/click metadata | 0.00 / 1.5 |
| Camera/interior readability | 1.00 / 2.0 |
| Narrative/flow contribution | 1.10 / 1.5 |

Issues:

- The v2 model has strong vertical farm identity and restored green plant accents.
- Nutrition has preview metadata but no interaction target.
- Scene 14 live survey showed Fitness and Finance hit areas in viewport, not Nutrition.
- The Nutrition scene comes late in the journey and has only 14 seconds in the canonical plan, so weak interaction/camera clarity is especially costly.

Recommendations:

- Add Nutrition interaction target to the farm tiers or market base.
- Verify the interior Nourishment Hall push, especially because the integration review documents a cinematic cutaway exception.
- Consider slightly stronger label/camera support due to its short scene duration.

## 17-Scene App Journey Audit

| Scene | Expected Role | Live / Source Observation | Grade | Priority |
|---:|---|---|---:|---|
| 1 | Full city aerial hero | 12 labels render; only 5 structures interactive. Labels are hard-coded screen positions and can feel detached. | 6.5 | P1 |
| 2 | SIA exterior reveal | SIA board appears; unrelated targets remain mounted offscreen. | 6.8 | P1 |
| 3 | Inside SIA Tower | Interior state active, but no board labels and user/current evidence shows abstract close-up rather than a clear interior. | 3.0 | P0 |
| 4 | Fitness exterior -> interior | Fitness board and target exist; all 5 targets in viewport; user screenshot shows over-close facade framing. | 6.4 | P1 |
| 5 | Yoga exterior -> interior | Yoga board appears but Yoga is not interactive; Finance/Relationships targets are in viewport. | 5.0 | P1 |
| 6 | Finance exterior -> interior | Finance board/target work, but unrelated SIA/Relationships/Career targets are also in viewport. | 6.8 | P1 |
| 7 | Knowledgebase exterior -> interior | Knowledgebase board appears but no Knowledgebase target; user reports wrong Finance hover. | 4.2 | P0 |
| 8 | Chat exterior -> interior | Chat board appears but no Chat target; unrelated targets remain present. | 5.0 | P1 |
| 9 | Leaderboard exterior -> interior | Leaderboard board appears but no Leaderboard target; unrelated targets in viewport. | 5.2 | P1 |
| 10 | Relationships exterior -> interior | Relationships board/target work, but other targets remain mounted. | 6.4 | P1 |
| 11 | Career exterior -> interior | Career board/target work; still affected by global target leakage. | 7.0 | P1 |
| 12 | Recovery exterior -> interior | Recovery board appears but no Recovery target; only Fitness target in viewport. | 5.0 | P1 |
| 13 | AI Analytics exterior -> interior | Analytics board appears but no Analytics target; SIA/Fitness/Finance targets in viewport. | 5.4 | P1 |
| 14 | Nutrition exterior -> interior | Nutrition board appears but no Nutrition target; Fitness/Finance targets in viewport. | 5.2 | P1 |
| 15 | Cross-pillar revelation | 12 labels render; only 5 structures interactive. Strong city read, weak full-system interaction. | 6.6 | P1 |
| 16 | Product reality | Product overlay visible; active board hidden; all five interaction targets mounted offscreen. | 6.2 | P2 |
| 17 | Closing | 12 labels render; only 5 structures interactive. Good city closure but no final brand-frame polish verified. | 6.4 | P2 |

## Runtime Interaction Survey

Live DOM survey at 1280 x 720:

| Scene Group | Label/Board State | Interaction State |
|---|---|---|
| Scenes 1, 15, 17 | 12 overview labels | Only SIA, Fitness, Finance, Relationships, Career are interactive. |
| Scene 3 | 0 labels, 0 boards | SIA target in viewport; the other four app targets mounted offscreen. |
| Scenes 4, 6, 10, 11 | Active board for target district | Active district is interactive, but unrelated interactive targets remain mounted. |
| Scenes 5, 7, 8, 9, 12, 13, 14 | Active board for target district | Active district is not interactive; unrelated targets appear in viewport or remain mounted offscreen. |
| Scene 16 | Product overlay visible, no board | Five interaction targets remain mounted offscreen. |

This is the clearest systemic issue in the app: label boards and interaction targets are separate systems. A district can have the correct visible board while the actual hover/click target belongs to another district or does not exist.

## Text And Label Placement Findings

- Overview labels are not projected from model anchors. They use hard-coded `left` and `top` percentages for Scenes 1, 15, and 17.
- Active district boards use 3D `Html` anchors, but their offsets and heights are individually tuned and not always visually attached to the structure.
- Mobile overview labels use a dock instead of spatial labels. This is safer for overlap but weakens the spatial city read.
- Scene 3 and Scene 16 intentionally hide active boards. This is sensible for visual cleanliness, but Scene 3 currently needs more orientation, not less.
- Some label names differ from scene names: "Finance bank" vs "Finance district", "Competition arena" vs "Leaderboard and competition", "Chat hub" vs "Chat and communication." These are not fatal, but final copy QA should standardize them.

## Camera And Interior Findings

- Every district scene from 4 through 14 has an `interiorCamera` and `interiorStart` configured in source.
- The live jump buttons land near the beginning of each scene, so they do not prove interior readability.
- Browser screenshot capture currently fails, preventing reliable live verification of every interior threshold.
- User screenshot evidence shows the current SIA interior and Fitness close-up are not visually smooth or informative enough.
- Assembly scroll-verification images prove nonblank model/city frames, but they do not fully prove the production app's user-facing scroll entry experience.

Recommended camera QA for the next pass:

- For each scene, capture and grade: scene start, pre-interior approach, interior threshold, interior midpoint, and exit transition.
- Require that the first two seconds of each district identify the exterior, and the interior midpoint identify a room/focal object.
- Add a specific "inside/not inside" verdict for every interior scene.

## Recommended Repair Sessions

### Session A - P0 Interaction Coverage And Target Gating

Goal: fix wrong-hover and missing-hover issues.

- Add interaction targets for Yoga, Knowledgebase, Chat, Leaderboard, Recovery, Analytics, and Nutrition.
- Gate targets so only overview-relevant or active-scene-relevant targets can be hovered.
- Align hit areas to actual projected model anchors.
- Add QA cases for each structure: hover/click shows the correct label, status, insight, and signal.
- Specific acceptance test: Knowledgebase hover/click never shows Finance copy.

### Session B - P0 SIA Interior Camera Rewrite

Goal: make Scene 3 unmistakably read as "Inside SIA Tower."

- Rework camera position, target, FOV, and easing around a clear atrium path.
- Add or emphasize visible interior anchors: city model, neural core, walls/platforms, crown light, and data screens.
- Add a temporary or permanent orientation label/focal cue.
- Verify against the user complaint: scrolling should feel like entering, not only zooming close.

### Session C - P1 Label Placement System

Goal: make labels feel attached and accurate.

- Replace or supplement screen-percentage labels with projected 3D anchors where possible.
- Keep mobile dock only if projected labels fail mobile readability.
- Add per-scene label collision and label-to-model-distance checks.
- Standardize structure names across labels, overlays, nav titles, and preview panels.

### Session D - P1 Interior Reveal Pass For Scenes 4-14

Goal: make every exterior-to-interior scene smooth and legible.

- Audit all district scenes at interior threshold and midpoint.
- Tune camera paths, target heights, and active interior mounting thresholds.
- Make each district interior focal object visible within one second after entry.
- Mark any district that should remain exterior-only and update copy accordingly.

### Session E - P1 Flow And Pacing Pass

Goal: make the full scroll journey feel designed from beginning to end.

- Review 0-100% scroll as one continuous story, not isolated scene jumps.
- Smooth transitions between SIA -> Fitness, Analytics -> Nutrition, Climax -> Product, and Product -> Closing.
- Ensure overlay copy changes support the camera rather than distracting from visual confusion.

### Session F - P1/P2 QA Harness Repair

Goal: restore reliable visual evidence.

- Add a screenshot capture fallback for the heavy WebGL scene.
- Record DOM state, canvas nonblank check, console warnings/errors, and visual screenshot per key scene.
- Save final evidence under a new audit/session folder so later work can compare before/after.

## Final Recommendations

1. Do not start by rebuilding models. The approved v2 models are mostly strong enough; the biggest user-visible failures are app interaction, label anchoring, and camera flow.
2. Fix hover/click coverage before label polish. Wrong metadata is more damaging than a merely imperfect label position.
3. Treat SIA Scene 3 as its own P0 session. It is the narrative heart of the product and currently undercuts the entire journey.
4. After interaction and SIA interior are fixed, run a full 17-scene visual QA pass with screenshots and midpoint interior checks.
5. Keep this audit as the issue backlog seed. Future sessions should close items here rather than relying only on previous "approved" phase status.

