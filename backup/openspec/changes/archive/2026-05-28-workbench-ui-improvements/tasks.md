# Tasks: Workbench UI Improvements

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 220-340 |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR with 3 small work units |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Sidebar shell + hierarchy | PR 1 | `index.html` + `viewer.css`, no JS behavior drift |
| 2 | Variable visibility/edit flow | PR 1 | `viewer.js` + tests, preserve `set_variable` contract |
| 3 | SVG zoom + verification batches | PR 1 | `viewer.js` + tests, client-only state |

## Phase 1: Test Guards

- [x] 1.1 Extend `tests/integration/test_mbse_workbench.py` with RED assertions for sidebar section labels, always-visible variable area, and zoom controls from the served HTML.
- [x] 1.2 Add RED assertions that `viewer.js` keeps using only `/api/runtime/reset`, `/api/runtime/events`, and `/api/runtime/variables`, plus zoom handler identifiers.

## Phase 2: Layout Foundation

- [x] 2.1 Update `src/mbse/web/static/index.html` to split the page into persistent sidebar and diagram pane, with semantic sections for state, variables, actions, and status.
- [x] 2.2 Update `src/mbse/web/static/viewer.css` for the minimal two-pane layout, clearer section hierarchy, safe overflow, and a narrow-screen fallback without new workflows.

## Phase 3: Runtime UI Wiring

- [x] 3.1 Refactor `src/mbse/web/static/viewer.js` to render declared variables from `variable_ids` in order, showing current values or explicit `unset`.
- [x] 3.2 Replace the free variable picker flow with a shared sidebar editor that submits the existing `{ variable_id, value }` payload and refreshes status/snapshot on success or failure.
- [x] 3.3 Add client-only zoom state in `src/mbse/web/static/viewer.js` for `Zoom in`, `Zoom out`, and `Reset view`, scoped to the SVG viewport only.

## Phase 4: Batch Verification

- [x] 4.1 Run `pytest tests/integration/test_mbse_workbench.py -k "runtime_ready_static_viewer or runtime_session_endpoints"` after layout + wiring to prove scenarios stay green.
- [x] 4.2 Run `pytest tests/integration/test_mbse_workbench.py` after zoom/reset work to catch contract drift and regressions before verify.
- [x] 4.3 Confirm no backend or runtime-semantics files changed outside `src/mbse/web/static/` and `tests/integration/test_mbse_workbench.py`.
