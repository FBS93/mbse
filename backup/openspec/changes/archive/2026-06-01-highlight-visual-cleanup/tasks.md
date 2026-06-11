# Tasks: Highlight Visual Cleanup

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 120-220 |
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
| 1 | CSS descendant targeting plus browser-harness and integration checks | PR 1 | Single frontend slice; tests and asset assertions together |

## Phase 1: RED - Browser-facing coverage

- [x] 1.1 In `tests/integration/test_mbse_workbench.py`, add CSS asset assertions for `.is-active-state > ...` and `.is-active-transition > path/polygon`, and assert no broad group-level highlight rule remains.
- [x] 1.2 In `tests/support/viewer_browser_harness.py`, extend `__snapshot()` to expose highlighted group child-tag summaries so tests can detect text descendants separately from shape descendants.
- [x] 1.3 In `tests/integration/test_mbse_workbench.py`, add failing harness scenarios for a leaf state, a compound state, and a transition group proving labels stay neutral while only intended shapes are highlight targets.

## Phase 2: GREEN - Frontend styling

- [x] 2.1 Update `src/mbse/web/static/viewer.css` to replace broad `.is-active-state` group styling with narrow direct-child selectors for state contour/background shapes only; leave `text` untouched.
- [x] 2.2 Update `src/mbse/web/static/viewer.css` to style `.is-active-transition > path` and `.is-active-transition > polygon` only, preserving distinct transition emphasis without touching event-label text.
- [x] 2.3 Validate the chosen state selectors against both leaf and compound Graphviz SVG fixtures used in the harness tests; narrow any selector that catches divider or nested-label shapes.

## Phase 3: REFACTOR - Harness clarity

- [x] 3.1 Refine `tests/support/viewer_browser_harness.py` helper naming/shape-summary structure so descendant-target assertions stay readable and stable for future viewer CSS changes.

## Phase 4: Verification

- [x] 4.1 Run `pytest tests/integration/test_mbse_workbench.py -k highlight` or the smallest equivalent focused selection covering the new highlight scenarios.
- [x] 4.2 Run `pytest tests/integration/test_mbse_workbench.py` to confirm the frontend-only cleanup preserves existing exact-ID highlight behavior.
