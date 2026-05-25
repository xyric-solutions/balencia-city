---
name: balencia-build
description: "Run the Balencia City build-loop workflow. Use when the user types /balencia-build, asks to build next, continue building Balencia, build a specific module, generate a build session prompt, or run looped structure, energy, assembly, or app work."
---

# Balencia Build

## Alias

Treat `/balencia-build` as the human-facing alias for this skill. `$balencia-build` may be invoked explicitly.

## State Read

1. Read `PROGRESS.md` and `BUILD-ORDER.md`.
2. Parse frontmatter fields: `current_module`, `current_phase`, `current_session`, `last_completed`, and `next_batch`.
3. If frontmatter is missing, scan the Structure Status table for the first module that is not complete.
4. Resolve arguments:
   - `next`: use `next_batch`.
   - `{NN}-{slug}`: target that module.
   - `loop max=N`: repeat after successful QA, stopping at `N` iterations.

## Workflow Selection

- Phases 1-4: use `$balencia-structure-team`.
- Phase 5: use `$balencia-energy-team`.
- Phase 6: use `$balencia-assembly-team`.
- Phase 7: use `$balencia-app-team`.
- For structure phases, map `exterior-major-forms`, `exterior-detail`, `interior`, and `integration` to the corresponding prompt template in `PROMPT-TEMPLATES.md`.
- Combined exterior may be used only when the target has no prior exterior sessions, fewer than 6 key architectural elements, and an exterior budget max of 15000 tris or less.

## Prompt Generation

1. Load `quick-context` plus only the needed `MASTER-CONTEXT.md` sections by anchor.
2. Read the module `SPEC.md` in full and the current `REVIEW.md` for previous sessions or fix instructions.
3. Extract variables from the SPEC, REVIEW, current session number, material slot table, and build order.
4. Interpolate the chosen template from `PROMPT-TEMPLATES.md`.
5. Keep the final session prompt around 150-200 lines and avoid inlining unrelated context.

## Execution Safety

- In plan mode, only produce a plan or build prompt. Do not mutate files.
- For live Blender work, verify available tools such as `execute_blender_code` or an approved Blender runner.
- Do not install Blender MCP automatically. If the needed Blender tool is unavailable, stop and state the setup required.
- Use named roles like `DESIGN-05` and `DESIGN-08` only when corresponding tools or agents are actually available; otherwise perform the role locally or prepare a handoff prompt.
- After QA failure, include fix instructions in the next prompt and retry at most 2 times for the same gate before escalating.

## State Updates

Update `PROGRESS.md` and the module `REVIEW.md` only after an executed build and QA result justify the change. Recalculate summary counters from the Structure Status table and approved artifacts instead of hand-editing stale numbers.
