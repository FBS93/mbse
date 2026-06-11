# Tasks: Workbench Highlight Polish Slice B

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 220-340 |
| 400-line budget risk | Medium |
| Chained PRs recommended | No |
| Suggested split | Single PR, applied in 2 internal batches |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Medium

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Lock backend leaf-only + last-transition contract | PR 1 | Batch A; no SVG structure changes |
| 2 | Apply viewer polish and integration assertions | PR 1 | Batch B; stays out of Slice C |

## Phase 1: Contract RED

- [x] 1.1 Update `tests/unit/mbse/test_prepare_hsm_engine.py` and `tests/unit/mbse/test_generated_engine.py` to fail on missing `initial_transition_ids` metadata.
- [x] 1.2 Update `tests/unit/mbse/test_hsm_runtime.py` to fail until init/reset and event re-entry keep only the final transition into the active leaf.
- [x] 1.3 Update `tests/unit/mbse/test_web_runtime_bridge.py` to fail until snapshots emit leaf-only `active_ids` plus optional filtered `last_transition_id`.

## Phase 2: Backend GREEN

- [x] 2.1 Modify `src/mbse/domain/models.py` to add optional `last_transition_id` and document `active_ids` as leaf-only.
- [x] 2.2 Modify `src/mbse/application/prepare_hsm_engine.py` and `src/mbse/infrastructure/generated_engine.py` to carry `initial_transition_ids` lookup metadata without touching SVG generation.
- [x] 2.3 Modify `src/mbse/application/hsm_runtime.py` to resolve the active leaf and remember only the final transition used to enter it.
- [x] 2.4 Modify `src/mbse/application/web_runtime_bridge.py` to serialize exact-ID leaf highlights and pass through `last_transition_id` only when it matches SVG IDs.
- [x] 2.5 Batch A verify: run `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_generated_engine.py tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_web_runtime_bridge.py`.

## Phase 3: Viewer RED/GREEN

- [x] 3.1 Update `tests/support/viewer_browser_harness.py` and `tests/integration/test_mbse_workbench.py` to assert separate state/transition classes, subtler state emphasis, and no parent highlight expectation.
- [x] 3.2 Modify `src/mbse/web/static/viewer.js` to clear/apply separate classes for leaf states vs last transition using exact SVG IDs only.
- [x] 3.3 Modify `src/mbse/web/static/viewer.css` to soften active-state styling and add a distinct transition highlight without changing SVG structure.
- [x] 3.4 Batch B verify: run `pytest tests/integration/test_mbse_workbench.py`.

## Phase 4: Full Verification / Scope Guard

- [x] 4.1 Run `pytest` for the full suite and confirm no unrelated snapshot/UI regressions.
- [x] 4.2 Review changed files against `openspec/changes/workbench-highlight-polish/design.md` and stop if work drifts into SVG internals or Slice C concerns.
