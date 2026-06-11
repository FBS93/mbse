# Tasks: Transition Path Highlight Cleanup

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 260-360 |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Ship the breaking path-array contract end-to-end | PR 1 | One cohesive slice across runtime, bridge, viewer, and tests |

## Phase 1: Contract RED

- [x] 1.1 Update `tests/unit/mbse/test_hsm_runtime.py` to expect ordered tuple paths for `init()`, event+initial chains, self-transition, and `set_state()` clearing to `()`.
- [x] 1.2 Update `tests/unit/mbse/test_web_runtime_bridge.py` so bridge snapshots keep tuple order, drop unknown IDs member-by-member, and never emit scalar fallback.
- [x] 1.3 Update `tests/integration/test_generated_hsm_engine.py` and `tests/integration/test_mbse_workbench.py` fixtures/assertions to require JSON arrays, multi-edge highlight cases, and border-only active-state behavior.

## Phase 2: Runtime and Bridge GREEN

- [x] 2.1 Change `src/mbse/domain/models.py` dataclasses so runtime and viewer `last_transition_id` are `tuple[str, ...]` with empty-tuple defaults.
- [x] 2.2 Refactor `src/mbse/application/hsm_runtime.py` so `_descend_initials()` and `_execute_transition()` accumulate the full ordered executed path, `send_event()` preserves the prior tuple on rejected events, and `set_state()` resets to `()`.
- [x] 2.3 Update `src/mbse/application/web_runtime_bridge.py` to filter each transition ID by exact membership in `highlightable_ids`, preserve surviving order, and serialize only arrays.

## Phase 3: Viewer GREEN

- [x] 3.1 Update `src/mbse/web/static/viewer.js` to treat `snapshot.last_transition_id` as an array and apply `is-active-transition` to every returned exact ID.
- [x] 3.2 Update `src/mbse/web/static/viewer.css` so `.is-active-state` affects borders/contours only, while `.is-active-transition` still targets just edge lines and arrowheads, not labels.

## Phase 4: Refactor and Verify

- [x] 4.1 Reconcile any workbench helpers touched by the new contract in `tests/support/viewer_browser_harness.py` or `tests/integration/test_hsm_json_workbench.py` only if Phase 1 failures prove they still assume scalars.
- [x] 4.2 Run `pytest tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_web_runtime_bridge.py tests/integration/test_generated_hsm_engine.py tests/integration/test_mbse_workbench.py` and finish with a full `pytest` pass before handoff.
