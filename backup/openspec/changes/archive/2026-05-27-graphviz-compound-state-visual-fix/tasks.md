# Tasks: Graphviz Compound State Visual Fix

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | ~120-220 |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR |
| Delivery strategy | ask-always |
| Chain strategy | pending |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Complete compound-state visual fix plus test coverage | PR 1 | Single reviewable change |

## Phase 1: Render Contract

- [x] 1.1 Update `src/mbse/infrastructure/templates/hsm_v1.dot.j2` so compound states emit the public authored id and visible label on the cluster, not on an inner visible parent node.
- [x] 1.2 Keep one private `__anchor` node inside each compound cluster for transition and local-initial routing.

## Phase 2: Render Preparation

- [x] 2.1 Update `src/mbse/application/prepare_hsm_render.py` to route compound-state initial and transition endpoints to `{state.id}__anchor` only.
- [x] 2.2 Preserve authored public ids in `highlightable_ids` and leave flat-state behavior unchanged.

## Phase 3: Verification Coverage

- [x] 3.1 Extend `tests/unit/mbse/test_hsm_render_view.py` to assert cluster-owned public ids, no duplicate visible parent box, and anchor-based routing.
- [x] 3.2 Extend `tests/integration/test_hsm_json_workbench.py` to assert the workbench/SVG contract still resolves exactly one public compound-state id.

## Phase 4: Verify

- [x] 4.1 Run targeted pytest for the compound-state render/workbench coverage.
- [x] 4.2 Run the full `pytest` suite to confirm non-compound behavior remains unchanged.
