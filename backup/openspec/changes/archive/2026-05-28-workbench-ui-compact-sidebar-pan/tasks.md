# Tasks: Compact Sidebar and Diagram Pan Controls

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 220-340 |
| 400-line budget risk | Medium |
| Chained PRs recommended | No |
| Suggested split | Single PR |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Medium

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Compact sidebar markup + density | PR 1 | Keep IDs/contracts unchanged |
| 2 | Diagram pan/scroll isolation + tests | PR 1 | Same slice; verify in one batch |

## Phase 1: Sidebar Foundation

- [x] 1.1 Update `src/mbse/web/static/index.html` to render sections in `Reset -> Events -> Variables` order and remove the visible `Status` section without changing existing form/select/container IDs.
- [x] 1.2 Tighten `src/mbse/web/static/viewer.css` sidebar sizing/spacing to a compact dense layout; keep the sidebar readable and set sidebar-owned vertical overflow.

## Phase 2: Diagram Interaction Wiring

- [x] 2.1 Extend `src/mbse/web/static/viewer.js` view state with drag-pan fields and keep wheel zoom bound only to `#svg-viewport`.
- [x] 2.2 Add viewport drag handlers in `src/mbse/web/static/viewer.js` that pan via `#svg-viewport.scrollLeft/scrollTop`; do not add backend calls or transform-based pan state.

## Phase 3: Harness Adjustment

- [x] 3.1 Extend `tests/support/viewer_browser_harness.py` snapshot/layout state with sidebar scroll and viewport scroll offsets only if required by the new assertions.
- [x] 3.2 Add minimal harness helpers for sidebar wheel and viewport drag simulation, keeping fetch counting and existing event/variable helpers unchanged.

## Phase 4: Verification Batch

- [x] 4.1 Update `tests/integration/test_mbse_workbench.py` server/static assertions for compact sidebar order, absence of `Status`, and unchanged runtime endpoints.
- [x] 4.2 Add/adjust browser-harness tests in `tests/integration/test_mbse_workbench.py` for spec scenarios: sidebar wheel changes only sidebar scroll, viewport wheel changes only zoom, and drag-pan changes viewport scroll with no extra requests.
- [x] 4.3 Run `pytest tests/integration/test_mbse_workbench.py` as the batch verification gate for this slice; avoid unrelated test or UI scope expansion.
