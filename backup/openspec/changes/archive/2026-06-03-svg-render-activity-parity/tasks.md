# Tasks: SVG Render Activity Parity

## Review Workload Forecast

| Field | Value |
|---|---|
| Estimated changed lines | 180-260 |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR |
| Delivery strategy | ask-always |
| Chain strategy | pending |

Decision needed before apply: Yes
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|---|---|---|---|
| 1 | Keep render parity to state hooks, internal rows, normal labels, and SVG ID contract | Single PR | Fits one review slice; no highlighting follow-up in this change |

## Phase 1: RED Unit Coverage

- [x] 1.1 In `tests/unit/mbse/test_hsm_render_view.py`, add failing assertions for ordered `on_initial:`, `on_entry:`, `on_exit:`, then `internal_transitions:` sections on compound states.
- [x] 1.2 In `tests/unit/mbse/test_hsm_render_view.py`, add failing assertions for normal labels covering event-only, event+guard, event+activities, and `event [guard]/activity` omission rules.
- [x] 1.3 In `tests/unit/mbse/test_hsm_render_view.py`, add failing assertions that initial edges stay unlabeled, keep authored IDs, and never expose authored `initial.activities` text.

## Phase 2: GREEN Render Preparation

- [x] 2.1 In `src/mbse/application/prepare_hsm_render.py`, finalize ordered `body_sections` shaping for lifecycle hooks and state-owned internal transitions using authored order.
- [x] 2.2 In `src/mbse/application/prepare_hsm_render.py`, keep normal transition labels omission-safe as `event [guard]/activity` and keep all initial edges routing-only with empty visible labels.
- [x] 2.3 In `src/mbse/infrastructure/templates/hsm_v1.dot.j2`, render prepared state sections and keep initial edges `label=""` while normal transitions render prepared labels only.

## Phase 3: Integration and Contract Checks

- [x] 3.1 In `tests/integration/test_hsm_json_workbench.py`, add failing coverage proving DOT/SVG show lifecycle hooks, internal rows, and normal guard/activity text.
- [x] 3.2 In `tests/integration/test_hsm_json_workbench.py`, assert `highlightable_ids` and public SVG `id="..."` values stay limited to authored states and authored transition IDs, with helpers private.
- [x] 3.3 In `tests/integration/test_hsm_json_workbench.py`, assert root and local initial source dots stay visible while no initial-edge activity label or helper artifact appears.

## Phase 4: Verification

- [x] 4.1 Run `pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` and reach GREEN.
- [x] 4.2 Run `pytest` to confirm the slice remains render-only and does not pull in highlighting or runtime behavior changes.
