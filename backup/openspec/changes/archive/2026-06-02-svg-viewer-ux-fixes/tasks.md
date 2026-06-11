# Tasks: SVG Viewer UX Fixes

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 320-470 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1: viewer/harness foundation → PR 2: integration regression coverage |
| Delivery strategy | ask-always |
| Chain strategy | pending |

Decision needed before apply: Yes
Chained PRs recommended: Yes
Chain strategy: pending
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Pan lifecycle, fit baseline, stage sizing hooks | PR 1 | Base slice in `viewer.js`, `viewer.css`, `index.html`, harness helpers |
| 2 | Spec regression coverage for scroll ownership and reset/refit | PR 2 | Depends on PR 1; keep pytest assertions focused |

## Phase 1: Test Harness Foundation

- [x] 1.1 In `tests/support/viewer_browser_harness.py`, add RED helpers/snapshots for document-level drag listeners, pan-active state, stage size, and selection suppression signals.
- [x] 1.2 In `tests/support/viewer_browser_harness.py`, add RED interaction helpers for drag ending on `document`, viewport resize/sidebar-width refit checks, and overflow ownership snapshots.

## Phase 2: Frontend Interaction Fixes

- [x] 2.1 In `src/mbse/web/static/viewer.js`, move viewport pan to a document-scoped gesture lifecycle with explicit pan state, drag start/end cleanup, and selection guard toggles.
- [x] 2.2 In `src/mbse/web/static/viewer.js`, split fit-baseline math from interactive zoom clamping so first load and `Reset view` recompute from live viewport geometry.
- [x] 2.3 In `src/mbse/web/static/viewer.js`, update stage sizing and sidebar-resize/reset wiring so overflow reflects effective zoom and fitted views stay centered.
- [x] 2.4 In `src/mbse/web/static/viewer.css` and `src/mbse/web/static/index.html`, lock page scroll, keep sidebar overflow local, and add the minimal hooks/classes needed for pan-active cursor and selection behavior.

## Phase 3: Integration Regression Coverage

- [x] 3.1 In `tests/integration/test_mbse_workbench.py`, add RED/GREEN cases for sidebar wheel isolation and viewport wheel zoom isolation from sidebar/page scroll.
- [x] 3.2 In `tests/integration/test_mbse_workbench.py`, add RED/GREEN cases for drag continuity when the pointer leaves `#svg-viewport` and for no selection side effects during pan.
- [x] 3.3 In `tests/integration/test_mbse_workbench.py`, add RED/GREEN cases for full-diagram fit on initial load plus `Reset view` recomputation after viewport or splitter size changes.

## Phase 4: Verification and Cleanup

- [x] 4.1 Run `pytest tests/integration/test_mbse_workbench.py` and confirm the spec scenarios pass without extra runtime fetches beyond existing workbench operations.
- [x] 4.2 Refactor touched frontend/test code for readability only after GREEN, keeping file scope frontend-only and avoiding pan/zoom model rewrites.
