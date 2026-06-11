# Apply Progress: workbench-highlight-polish

## Batch Status

- Completed Batch A and Batch B.
- Completed closure batch: aligned tracking artifacts and replaced weak source-string highlight assertions with behavior-level browser-harness proof.
- Scope kept to backend/view-model plus viewer/browser polish only.
- No SVG structure changes.
- Slice C remains untouched.

## Completed Tasks

- [x] 1.1 Update `tests/unit/mbse/test_prepare_hsm_engine.py` and `tests/unit/mbse/test_generated_engine.py` to fail on missing `initial_transition_ids` metadata.
- [x] 1.2 Update `tests/unit/mbse/test_hsm_runtime.py` to fail until init/reset and event re-entry keep only the final transition into the active leaf.
- [x] 1.3 Update `tests/unit/mbse/test_web_runtime_bridge.py` to fail until snapshots emit leaf-only `active_ids` plus optional filtered `last_transition_id`.
- [x] 2.1 Modify `src/mbse/domain/models.py` to add optional `last_transition_id` and document `active_ids` as leaf-only.
- [x] 2.2 Modify `src/mbse/application/prepare_hsm_engine.py` and `src/mbse/infrastructure/generated_engine.py` to carry `initial_transition_ids` lookup metadata without touching SVG generation.
- [x] 2.3 Modify `src/mbse/application/hsm_runtime.py` to resolve the active leaf and remember only the final transition used to enter it.
- [x] 2.4 Modify `src/mbse/application/web_runtime_bridge.py` to serialize exact-ID leaf highlights and pass through `last_transition_id` only when it matches SVG IDs.
- [x] 2.5 Batch A verify: run `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_generated_engine.py tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_web_runtime_bridge.py`.
- [x] 3.1 Update `tests/support/viewer_browser_harness.py` and `tests/integration/test_mbse_workbench.py` to assert separate state/transition classes, subtler state emphasis, and no parent highlight expectation.
- [x] 3.2 Modify `src/mbse/web/static/viewer.js` to clear/apply separate classes for leaf states vs last transition using exact SVG IDs only.
- [x] 3.3 Modify `src/mbse/web/static/viewer.css` to soften active-state styling and add a distinct transition highlight without changing SVG structure.
- [x] 3.4 Batch B verify: run `pytest tests/integration/test_mbse_workbench.py`.
- [x] 4.1 Run `pytest` for the full suite and confirm no unrelated snapshot/UI regressions.
- [x] 4.2 Review changed files against `openspec/changes/workbench-highlight-polish/design.md` and stop if work drifts into SVG internals or Slice C concerns.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 / 2.2 | `tests/unit/mbse/test_prepare_hsm_engine.py`, `tests/unit/mbse/test_generated_engine.py` | Unit | ✅ 11/11 targeted baseline | ✅ Wrote failing metadata assertions first | ✅ 4/4 relevant tests passing | ✅ Engine view + generated wrapper/source cases | ✅ Added shared metadata formatting path |
| 1.2 / 2.3 | `tests/unit/mbse/test_hsm_runtime.py` | Unit | ✅ 11/11 targeted baseline | ✅ Wrote failing final-transition assertions first | ✅ 3/3 file tests passing | ✅ Covered init, parent-handled event, compound re-entry | ✅ Centralized active-path resolution + transition tracking |
| 1.3 / 2.4 | `tests/unit/mbse/test_web_runtime_bridge.py` | Unit | ✅ 11/11 targeted baseline | ✅ Wrote failing leaf-only/filtered snapshot assertions first | ✅ 4/4 file tests passing | ✅ Covered exact leaf-only ids, filtered transition id, reset/event cases | ✅ Simplified snapshot filtering logic |
| 3.1 / 3.2 / 3.3 | `tests/integration/test_mbse_workbench.py`, `tests/support/viewer_browser_harness.py` | Integration | ⚠️ 12/16 passing baseline in target file; 4 expected failures from outdated highlight contract | ✅ Updated browser/runtime assertions first for leaf-only state + final transition classes | ✅ 16/16 integration tests passing | ✅ Covered initial render, event update, repeated leaf re-entry, static JS/CSS contract | ✅ Extracted shared highlight-class helpers and kept exact-ID behavior |
| 4.1 / 4.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 58/58 full-suite baseline before closure polish | ✅ Replaced implementation-detail string/selector assertions with failing behavior-level highlight assertions first | ✅ 58/58 full suite passing | ✅ Coupled live session payload, served SVG, and harness-rendered highlight classes in the server integration path | ➖ No production refactor needed |

## Test Summary

- Total tests written: 20 assertion updates across 4 unit files plus integration/browser coverage for viewer highlight behavior
- Total tests passing: 58 full-suite tests, including 11 targeted unit tests and 16 integration tests covering viewer highlight behavior
- Layers used: Unit (11), Integration (16)
- Approval tests (refactoring): None — behavior changed per spec
- Pure functions created: 3 formatter/collector/highlight helpers

## Files Changed

- `src/mbse/domain/models.py` — added snapshot metadata fields and documented leaf-only `active_ids`
- `src/mbse/application/prepare_hsm_engine.py` — collected `initial_transition_ids`
- `src/mbse/infrastructure/generated_engine.py` — preserved initial/event transition lookup metadata in generated wrapper
- `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` — emitted transition lookup tables in generated source
- `src/mbse/application/hsm_runtime.py` — tracked final transition into resolved active leaf
- `src/mbse/application/web_runtime_bridge.py` — serialized leaf-only `active_ids` and filtered `last_transition_id`
- `tests/unit/mbse/test_prepare_hsm_engine.py` — asserted initial-transition metadata
- `tests/unit/mbse/test_generated_engine.py` — asserted generated source/wrapper metadata
- `tests/unit/mbse/test_hsm_runtime.py` — asserted final-transition semantics on init and re-entry
- `tests/unit/mbse/test_web_runtime_bridge.py` — asserted leaf-only/final-transition snapshot contract
- `src/mbse/web/static/viewer.js` — separated leaf-state vs transition highlight class application using exact SVG ids
- `src/mbse/web/static/viewer.css` — softened state highlight and added distinct transition highlight styling
- `tests/support/viewer_browser_harness.py` — exposed state/transition highlight ids for browser assertions
- `tests/integration/test_mbse_workbench.py` — asserted leaf-only snapshots plus distinct viewer highlight classes
- `openspec/changes/workbench-highlight-polish/tasks.md` — marked Batch A tasks complete
- `openspec/changes/workbench-highlight-polish/tasks.md` — marked Batch B tasks complete
- `openspec/changes/workbench-highlight-polish/tasks.md` — marked Phase 4 closure tasks complete

## Deviations from Design

None — Batches A/B match the design and stay out of SVG internals / Slice C.

## Remaining Tasks

- None.

## Workload / PR Boundary

- Mode: single PR
- Current work unit: Closure batch — artifact alignment plus minimal assertion hardening
- Boundary: `tasks.md`, `apply-progress.md`, and server/browser verification assertions only; no SVG structure or Slice C changes
- Estimated review budget impact: still within the planned single-PR review budget

## Status

14/14 tasks complete. Ready for archive.
