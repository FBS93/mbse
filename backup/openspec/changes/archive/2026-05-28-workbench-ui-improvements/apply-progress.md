# Apply Progress: workbench-ui-improvements

## Scope

- Delivery mode: single PR
- Chain strategy: not needed (`400-line budget risk: Low`)
- Current work unit: Suggested Work Units 1-3 in one batch
- Boundary: frontend evidence only (`tests/integration/test_mbse_workbench.py`, `tests/support/viewer_browser_harness.py`, OpenSpec task/progress artifacts); no backend/runtime semantic changes

## Completed Tasks

- [x] 1.1 Extend `tests/integration/test_mbse_workbench.py` with RED assertions for sidebar section labels, always-visible variable area, and zoom controls from the served HTML.
- [x] 1.2 Add RED assertions that `viewer.js` keeps using only `/api/runtime/reset`, `/api/runtime/events`, and `/api/runtime/variables`, plus zoom handler identifiers.
- [x] 2.1 Update `src/mbse/web/static/index.html` to split the page into persistent sidebar and diagram pane, with semantic sections for state, variables, actions, and status.
- [x] 2.2 Update `src/mbse/web/static/viewer.css` for the minimal two-pane layout, clearer section hierarchy, safe overflow, and a narrow-screen fallback without new workflows.
- [x] 3.1 Refactor `src/mbse/web/static/viewer.js` to render declared variables from `variable_ids` in order, showing current values or explicit `unset`.
- [x] 3.2 Replace the free variable picker flow with a shared sidebar editor that submits the existing `{ variable_id, value }` payload and refreshes status/snapshot on success or failure.
- [x] 3.3 Add client-only zoom state in `src/mbse/web/static/viewer.js` for `Zoom in`, `Zoom out`, and `Reset view`, scoped to the SVG viewport only.
- [x] 4.1 Run `pytest tests/integration/test_mbse_workbench.py -k "runtime_ready_static_viewer or runtime_session_endpoints"` after layout + wiring to prove scenarios stay green.
- [x] 4.2 Run `pytest tests/integration/test_mbse_workbench.py` after zoom/reset work to catch contract drift and regressions before verify.
- [x] 4.3 Confirm no backend or runtime-semantics files changed outside `src/mbse/web/static/` and `tests/integration/test_mbse_workbench.py`.

## Post-verify Evidence Fix

- [x] Add a lightweight browser harness under `tests/support/` that executes the real `src/mbse/web/static/viewer.js` in QuickJS with a minimal DOM/fetch shim.
- [x] Extend `tests/integration/test_mbse_workbench.py` with runtime client-side assertions for declared variable rendering and client-only zoom controls.

## Remaining Tasks

- None in this slice.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ `pytest tests/integration/test_mbse_workbench.py -k "runtime_ready_static_viewer or runtime_session_endpoints"` passed `2 passed` before edits | ✅ Added failing HTML assertions for `Current state`, `Variables`, `Runtime actions`, `Status`, zoom controls, and `variable-list`; targeted run failed `2 failed` | ✅ Same targeted command passed `2 passed` after the static UI shell was implemented | ✅ Covered both server entrypoints (`start_workbench_server` and `build_and_start_workbench`) so the new shell had to exist in both served HTML paths | ✅ Kept assertions at behavioral text/container level; no backend contract assertions changed |
| 1.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ Same `2 passed` baseline protected the touched viewer/static files before edits | ✅ Added failing JS assertions for the exact runtime endpoint set plus `wireZoomControls`, `applyZoom`, and zoom button identifiers | ✅ Targeted command passed `2 passed` after the viewer kept only the existing runtime endpoints while adding zoom wiring | ✅ Positive exact-set assertion plus negative `/api/highlight` assertion guarded both allowed and forbidden endpoint drift | ✅ Runtime contract checks stayed string-level and review-friendly |
| 2.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ Same `2 passed` baseline | ✅ The new HTML assertions failed before `index.html` changed | ✅ Targeted command passed `2 passed` after introducing the persistent sidebar sections and diagram toolbar shell | ✅ Both workbench boot paths had to serve the new structure, not just one fixture | ✅ Sidebar semantics stayed minimal: no new workflows or backend-owned fields |
| 2.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ Same `2 passed` baseline | ✅ RED already established by the missing sidebar/zoom UI shell exercised by the integration assertions | ✅ Targeted command passed `2 passed` with the two-pane layout, hierarchy spacing, overflow-safe viewport, and narrow-screen fallback in place | ✅ Desktop-visible sidebar plus stacked small-width fallback cover distinct layout intents from the design | ✅ Styling stayed in `viewer.css` only, preserving runtime behavior |
| 3.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ Same `2 passed` baseline | ✅ RED already established by the missing always-visible variable area in served HTML | ✅ Targeted command passed `2 passed` after `viewer.js` rendered declared `variable_ids` in order and displayed `unset` when absent | ✅ Declared variable presence and absent-value handling are different rendering paths under the same sidebar flow | ✅ Extracted small formatting helpers for variable display/input values |
| 3.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ Same `2 passed` baseline | ✅ RED already established by the missing persistent variable editor shell and runtime-contract assertions | ✅ Targeted command passed `2 passed` after the shared editor bound to sidebar selection, preserved `{ variable_id, value }`, and refreshed session/status on success or failure | ✅ Success and failure refresh paths both use the existing snapshot flow without introducing any new endpoint | ✅ Kept mutation orchestration thin and moved repeated refresh work into a helper |
| 3.3 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ Same `2 passed` baseline | ✅ RED already established by absent zoom controls/identifiers in HTML and JS | ✅ Targeted command passed `2 passed` after client-only zoom state and viewport scaling were added | ✅ Zoom in/out and reset are separate control paths over the same bounded local scale state | ✅ Added explicit zoom constants and a single `applyZoom()` clamp/helper |
| 4.1 | `tests/integration/test_mbse_workbench.py` | Verify | ✅ Baseline and targeted run both recorded during the cycle | ✅ Verification scope was fixed by the tasks artifact before execution | ✅ `pytest tests/integration/test_mbse_workbench.py -k "runtime_ready_static_viewer or runtime_session_endpoints"` passed `2 passed` | ➖ Triangulation skipped: verification task executes already-authored RED/GREEN coverage | ➖ None needed |
| 4.2 | `tests/integration/test_mbse_workbench.py` | Verify | ✅ Targeted slice already green before full-file verification | ✅ Verification scope was fixed by the tasks artifact before execution | ✅ `pytest tests/integration/test_mbse_workbench.py` passed `5 passed` | ➖ Triangulation skipped: verification task executes already-authored RED/GREEN coverage | ➖ None needed |
| 4.3 | `tests/integration/test_mbse_workbench.py` + changed file list | Verify | ✅ Scope was constrained up front by the user | ✅ The file-scope restriction itself acted as the failure boundary | ✅ No backend/runtime-semantics files changed; this evidence batch touched only frontend tests/support plus OpenSpec artifacts | ➖ Single scope audit | ➖ None needed |
| Post-verify browser evidence fix | `tests/integration/test_mbse_workbench.py`, `tests/support/viewer_browser_harness.py` | Integration | ✅ `pytest tests/integration/test_mbse_workbench.py` passed `5 passed` before adding runtime-browser evidence | ✅ `pytest tests/integration/test_mbse_workbench.py -k "declared_variables or zoom_controls"` failed during collection with `ModuleNotFoundError: No module named 'tests.support'` after the new browser-evidence tests were written first | ✅ Same targeted command passed `2 passed` after adding the QuickJS harness; full file then passed `7 passed` | ✅ Variable rendering covers both current-value and `unset` paths; zoom evidence executes `Zoom in`, `Zoom out`, and `Reset view` while fetch counts stay unchanged | ✅ The harness stays test-only and executes the shipped `viewer.js` without touching backend/runtime semantics |

## Test Summary

- **Total tests written**: 2 new runtime-browser integration tests plus the earlier served-HTML/source assertions
- **Total tests passing**: 7
- **Layers used**: Unit (0), Integration (7), E2E (0)
- **Approval tests**: None — behavior changed within the approved UI slice
- **Pure functions created**: 4 (`renderDetailRow`, `formatVariableValue`, `formatVariableInput`, `escapeHtml`); none added in this evidence fix batch

## Notes

- The variable selector workflow was replaced in the UI only; the backend payload stays exactly `{ variable_id, value }` against `/api/runtime/variables`.
- Failure refresh uses the existing `/api/session.json` snapshot fetch so the sidebar value/status stays current even when mutation submission fails locally or remotely.
- Zoom is bounded client-side (`0.5x` to `2.0x`) and applies only to the SVG stage transform.
- The QuickJS harness proves browser behavior by executing the shipped `viewer.js` against a minimal DOM/fetch shim under pytest; no runtime/server semantics changed.
- `tasks.md` is now synchronized with the completed slice state.

## Verification Commands

- `pytest tests/integration/test_mbse_workbench.py -k "runtime_ready_static_viewer or runtime_session_endpoints"` — safety net passed `2 passed` before edits.
- `pytest tests/integration/test_mbse_workbench.py -k "runtime_ready_static_viewer or runtime_session_endpoints"` — RED failed `2 failed` after adding the new sidebar/zoom assertions first.
- `pytest tests/integration/test_mbse_workbench.py -k "runtime_ready_static_viewer or runtime_session_endpoints"` — GREEN passed `2 passed` after implementing the UI slice.
- `pytest tests/integration/test_mbse_workbench.py -k "runtime_ready_static_viewer or runtime_session_endpoints"` — verification rerun passed `2 passed` after the small JS refactor.
- `pytest tests/integration/test_mbse_workbench.py` — full slice verification passed `5 passed`.
- `pytest tests/integration/test_mbse_workbench.py -k "declared_variables or zoom_controls"` — RED failed during collection with `ModuleNotFoundError: No module named 'tests.support'` after writing the new browser-evidence tests first.
- `pytest tests/integration/test_mbse_workbench.py -k "declared_variables or zoom_controls"` — GREEN passed `2 passed` after adding the QuickJS browser harness.
- `pytest tests/integration/test_mbse_workbench.py` — post-fix verification passed `7 passed`.
