# Tasks: Init Transition Rendering Cleanup

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 220-320 |
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
| 1 | Visible source-dot restoration + private-anchor cleanup | Single PR | Keep RED/GREEN/refactor and ID-contract tests together |

## Phase 1: RED - Correction Regressions

- [x] 1.1 In `tests/unit/mbse/test_hsm_render_view.py`, add failing assertions that `routing_helpers` distinguish `root_initial_source`, `local_initial_source`, and `compound_anchor`, with deterministic order and authored-only `highlightable_ids`.
- [x] 1.2 In `tests/integration/test_hsm_json_workbench.py`, add a fake-Graphviz failing contract that visible initial-source dots render, private anchors never surface as public SVG IDs, and authored IDs remain exact and unique.
- [x] 1.3 In `tests/integration/test_hsm_json_workbench.py`, add/refresh a real-`dot` regression (skip only when `dot` is unavailable) proving visible source dots stay present while stray target dots/helper ellipses disappear.

## Phase 2: GREEN - Render Model + Routing

- [x] 2.1 In `src/mbse/domain/models.py`, extend `HsmRenderRoutingHelper` metadata so helper kind and visibility explicitly separate visible source markers from private anchors.
- [x] 2.2 In `src/mbse/application/prepare_hsm_render.py`, register root/local initial sources as visible helpers and compound targets as private anchors, keeping endpoint ownership and ordering deterministic.

## Phase 3: GREEN - DOT + Validation Contract

- [x] 3.1 In `src/mbse/infrastructure/templates/hsm_v1.dot.j2`, render visible initial-source helpers as black `shape=point` nodes without public `id=` attributes and keep compound anchors invisible in the correct scope.
- [x] 3.2 In `src/mbse/domain/validation.py`, enforce that only private helper kinds are leak-checked while public SVG IDs for states, clusters, transitions, and initial transitions stay exact, unique, and unambiguous.

## Phase 4: REFACTOR + Verification

- [x] 4.1 Refactor shared helper fixtures/assertions in `tests/unit/mbse/test_hsm_render_view.py` and `tests/integration/test_hsm_json_workbench.py` so source-marker and private-anchor expectations stay readable.
- [x] 4.2 Run `pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` and confirm root/local visible source dots return, private anchors stay invisible, and authored public IDs remain stable.
