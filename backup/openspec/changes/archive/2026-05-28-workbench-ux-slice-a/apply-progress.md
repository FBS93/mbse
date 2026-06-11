# Apply Progress: workbench-ux-slice-a

## Scope

- Delivery mode: chained PR slice
- Chain strategy: stacked-to-main
- Current work unit: 2 — splitter drag + fit baseline + reset view
- Boundary: frontend-only viewer behavior plus harness verification for fit/reset/splitter interactions; no backend/runtime behavior changes and no Slice B/C work

## Completed Tasks

- [x] 1.1 Update `src/mbse/web/static/index.html` to add a splitter element and separate `Reset runtime` / `Reset view` controls without changing existing runtime form IDs or endpoints.
- [x] 1.2 Update `src/mbse/web/static/viewer.css` so `.layout` uses a resizable horizontal split and each `.variable-row` renders as one compact line with name, value/unset, input, and submit visible together.
- [x] 2.1 Extend `src/mbse/web/static/viewer.js` state with `sidebarWidthPx` and `fitBaseline`, keeping one line per variable declaration in the source.
- [x] 2.2 Add splitter drag wiring in `viewer.js` so sidebar width changes stay local to the page session and trigger no runtime/backend fetches.
- [x] 2.3 Compute an initial full-diagram fit after SVG injection, clamp to existing zoom limits, apply it before first render settles, and preserve wheel zoom + drag pan behavior.
- [x] 2.4 Add client-only `Reset view` behavior in `viewer.js` that restores the stored fit baseline while `Reset runtime` remains mapped only to `/api/runtime/reset`.
- [x] 3.1 Extend `tests/support/viewer_browser_harness.py` snapshot data so tests can observe reset-view fetch counts, sidebar width changes, fit baseline, and viewport scroll/zoom restoration.
- [x] 3.2 Add harness actions for dragging the splitter and invoking `Reset view`, keeping support limited to Slice A frontend assertions only.
- [x] 4.1 Batch 1 verification: update `tests/integration/test_mbse_workbench.py` HTML/harness checks for separate reset controls, compact variable rows, and unchanged runtime endpoints/contracts.
- [x] 4.2 Batch 2 verification: add harness coverage for splitter resize staying client-only, initial fit baseline, `Reset view` restoring fit, and wheel zoom/drag pan still working after fit.
- [x] 4.3 Run `pytest tests/integration/test_mbse_workbench.py -k "viewer or workbench"` after each batch; if either batch grows beyond review scope, stop before Slice B/C behavior.

## Remaining Tasks

- None.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ `pytest tests/integration/test_mbse_workbench.py -k "viewer or workbench"` passed `13 passed` before edits | ✅ Added failing served-HTML assertions for `Reset view`, splitter markup, and explicit reset button ids; targeted run failed `2 failed` | ✅ `pytest tests/integration/test_mbse_workbench.py -k "serves_runtime_session_endpoints_and_svg or serves_runtime_ready_static_viewer"` passed `3 passed, 10 deselected` after the shell update | ✅ Verified both server entrypoints so the split shell exists in both boot paths | ✅ Kept runtime endpoint/form contracts unchanged while adding only static controls |
| 1.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ Same `13 passed` baseline protected the touched frontend files | ✅ Added a failing harness assertion for compact variable rows; targeted run failed with `KeyError: 'compact_variable_rows'` before implementation | ✅ Same targeted command passed after compact-row markup/CSS landed | ✅ Covered both populated and unset variable states in the same compact-row assertion path | ✅ Added a minimal `.variable-row-main` wrapper so CSS could drive the one-line layout without changing mutation contracts |
| 2.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ `pytest tests/integration/test_mbse_workbench.py -k "viewer or workbench"` passed `13 passed` before batch-2 edits | ✅ Added fit-baseline tests first; targeted run failed with `TypeError: ViewerBrowserHarness.__init__() got an unexpected keyword argument 'viewport_size'` | ✅ `pytest tests/integration/test_mbse_workbench.py -k "initial_fit or reset_view_restores_fit or splitter_drag_changes_sidebar_width or runtime_ready_static_viewer"` passed `4 passed, 12 deselected` after adding state + harness support | ✅ Covered both min-clamped (`0.5`) and max-clamped (`2`) fit baselines across initial-fit and reset-view scenarios | ✅ Extracted `computeFitBaseline`, `measureSvgSize`, and `applyViewBaseline` helpers to keep the state additions minimal and readable |
| 2.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ Same `13 passed` baseline protected the touched viewer and harness files | ✅ Added splitter-resize coverage first; targeted run failed with `AttributeError: 'ViewerBrowserHarness' object has no attribute 'drag_splitter'` | ✅ Same targeted command passed after local drag wiring landed | ✅ Asserted both the default `288px` width and the dragged `360px` width while verifying fetch counts stayed unchanged | ✅ Used document-level listeners so the splitter behavior stays frontend-local and easy to reset |
| 2.3 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ Same `13 passed` safety net | ✅ Initial-fit assertions failed before implementation because the harness exposed no fit baseline and the viewer still opened at `scale(1)` | ✅ Same targeted command passed once fit was computed immediately after SVG injection | ✅ Exercised fit on both larger-than-viewport and smaller-than-viewport SVG viewBoxes to force real clamp logic | ✅ Centralized zoom clamping through `clampZoom()` instead of duplicating bounds checks |
| 2.4 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ Same `13 passed` safety net | ✅ Updated static-viewer coverage to require `reset-view-button` wiring and added failing reset-view assertions before implementation | ✅ Same targeted command passed after wiring the client-only button to restore the stored baseline | ✅ Verified `Reset view` restores zoom + scroll while `/api/runtime/reset` fetch count remains `0` | ✅ Reused the stored baseline object so reset-view stays separate from runtime actions |
| 3.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ Same `13 passed` safety net | ✅ New assertions failed until the harness surfaced `fit_baseline`, `sidebar_width_px`, and the existing fetch counters together | ✅ Same targeted command passed after snapshot extensions | ✅ Snapshot now exposes both geometry state and no-fetch evidence for resize/reset behaviors | ✅ Kept the harness additions scoped to frontend-only observability |
| 3.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ Same `13 passed` safety net | ✅ New tests failed until harness actions existed for splitter drag and reset-view click flows | ✅ Same targeted command passed after adding the synthetic interactions | ✅ Covered both button-click and drag flows in the same frontend-only harness layer | ✅ Added only the minimal synthetic events needed for Slice A |
| 4.1 | `tests/integration/test_mbse_workbench.py` | Verify | ✅ Targeted slice was green before final verification | ✅ Verification scope was fixed by the tasks artifact before execution | ✅ `pytest tests/integration/test_mbse_workbench.py -k "viewer or workbench"` passed `13 passed` | ➖ Triangulation skipped: verification task executes already-authored RED/GREEN coverage | ➖ None needed |
| 4.2 | `tests/integration/test_mbse_workbench.py` | Verify | ✅ Batch-2 targeted behavior tests were green before full verification | ✅ Verification scope was fixed by the tasks artifact before execution | ✅ `pytest tests/integration/test_mbse_workbench.py -k "viewer or workbench"` passed `16 passed` | ➖ Triangulation skipped: verification task executes already-authored RED/GREEN coverage | ➖ None needed |
| 4.3 | `tests/integration/test_mbse_workbench.py` | Verify | ✅ Batch 1 and batch 2 both used the required command boundary | ✅ The task itself is the command requirement, so RED was defined by running the mandated scope after each batch | ✅ `pytest tests/integration/test_mbse_workbench.py -k "viewer or workbench"` passed `16 passed` at the end of batch 2 | ➖ Triangulation skipped: command-only verification task | ➖ None needed |

## Test Summary

- **Total tests written**: 7 assertion groups across served HTML/CSS, fit-baseline behavior, reset-view restoration, splitter resize, and QuickJS harness rendering
- **Total tests passing**: 16
- **Layers used**: Unit (0), Integration (16), E2E (0)
- **Approval tests**: None — this batch changed approved frontend behavior
- **Pure functions created**: 0

## Files Changed

- `src/mbse/web/static/index.html` — added splitter shell and separate reset controls
- `src/mbse/web/static/viewer.css` — added split-grid layout and compact variable-row styling
- `src/mbse/web/static/viewer.js` — added sidebar width state, fit-baseline computation, splitter drag wiring, and client-only reset-view restoration
- `tests/support/viewer_browser_harness.py` — exposed viewport geometry, fit-baseline snapshots, splitter drag, and reset-view interactions for QuickJS tests
- `tests/integration/test_mbse_workbench.py` — added batch-1 and batch-2 RED/GREEN assertions
- `openspec/changes/workbench-ux-slice-a/tasks.md` — marked all Slice A work-unit tasks complete

## Verification Commands

- `pytest tests/integration/test_mbse_workbench.py -k "viewer or workbench"` — safety net passed `13 passed` before edits.
- `pytest tests/integration/test_mbse_workbench.py -k "serves_runtime_session_endpoints_and_svg or serves_runtime_ready_static_viewer"` — RED failed `2 failed` after adding served-HTML assertions first.
- `pytest tests/integration/test_mbse_workbench.py -k "renders_declared_variables_with_current_value_or_unset"` — RED failed with `KeyError: 'compact_variable_rows'` after adding compact-row evidence first.
- `pytest tests/integration/test_mbse_workbench.py -k "serves_runtime_session_endpoints_and_svg or serves_runtime_ready_static_viewer or renders_declared_variables_with_current_value_or_unset"` — GREEN passed `3 passed`.
- `pytest tests/integration/test_mbse_workbench.py -k "viewer or workbench"` — batch verification passed `13 passed`.
- `pytest tests/integration/test_mbse_workbench.py -k "initial_fit or reset_view_restores_fit or splitter_drag_changes_sidebar_width"` — RED failed `3 failed` after adding batch-2 tests first (`viewport_size` and `drag_splitter` missing).
- `pytest tests/integration/test_mbse_workbench.py -k "initial_fit or reset_view_restores_fit or splitter_drag_changes_sidebar_width or runtime_ready_static_viewer"` — GREEN passed `4 passed, 12 deselected` after viewer/harness implementation.
- `pytest tests/integration/test_mbse_workbench.py -k "viewer or workbench"` — final batch verification passed `16 passed`.
