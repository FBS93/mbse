# Apply Progress: Compact Sidebar and Diagram Pan Controls

## Implementation Progress

**Change**: `workbench-ui-compact-sidebar-pan`
**Mode**: Strict TDD
**Workload**: single PR

### Completed Tasks
- [x] 1.1 Update `src/mbse/web/static/index.html` to render sections in `Reset -> Events -> Variables` order and remove the visible `Status` section without changing existing form/select/container IDs.
- [x] 1.2 Tighten `src/mbse/web/static/viewer.css` sidebar sizing/spacing to a compact dense layout; keep the sidebar readable and set sidebar-owned vertical overflow.
- [x] 2.1 Extend `src/mbse/web/static/viewer.js` view state with drag-pan fields and keep wheel zoom bound only to `#svg-viewport`.
- [x] 2.2 Add viewport drag handlers in `src/mbse/web/static/viewer.js` that pan via `#svg-viewport.scrollLeft/scrollTop`; do not add backend calls or transform-based pan state.
- [x] 3.1 Extend `tests/support/viewer_browser_harness.py` snapshot/layout state with sidebar scroll and viewport scroll offsets only if required by the new assertions.
- [x] 3.2 Add minimal harness helpers for sidebar wheel and viewport drag simulation, keeping fetch counting and existing event/variable helpers unchanged.
- [x] 4.1 Update `tests/integration/test_mbse_workbench.py` server/static assertions for compact sidebar order, absence of `Status`, and unchanged runtime endpoints.
- [x] 4.2 Add/adjust browser-harness tests in `tests/integration/test_mbse_workbench.py` for spec scenarios: sidebar wheel changes only sidebar scroll, viewport wheel changes only zoom, and drag-pan changes viewport scroll with no extra requests.
- [x] 4.3 Run `pytest tests/integration/test_mbse_workbench.py` as the batch verification gate for this slice; avoid unrelated test or UI scope expansion.

### Files Changed
| File | Action | What Was Done |
|------|--------|---------------|
| `src/mbse/web/static/index.html` | Modified | Reordered the visible sidebar sections to Reset → Events → Variables and fully removed the leftover hidden `#runtime-status` node |
| `src/mbse/web/static/viewer.css` | Modified | Tightened the sidebar layout, narrowed the column, gave the sidebar its own vertical scroll, and removed the obsolete `#runtime-status` selector |
| `src/mbse/web/static/viewer.js` | Modified | Added client-only drag-pan state, kept wheel zoom scoped to `#svg-viewport`, and removed obsolete runtime-status writes |
| `tests/support/viewer_browser_harness.py` | Modified | Added sidebar/viewport scroll snapshot fields plus minimal wheel-sidebar and drag-viewport simulation helpers, then removed unused runtime-status harness nodes |
| `tests/integration/test_mbse_workbench.py` | Modified | Drove sidebar order, full runtime-status removal from served HTML/CSS/JS, wheel isolation, and drag-pan behavior through integration assertions |
| `openspec/changes/workbench-ui-compact-sidebar-pan/tasks.md` | Modified | Marked apply tasks complete |
| `openspec/changes/workbench-ui-compact-sidebar-pan/apply-progress.md` | Created | Recorded cumulative apply progress and TDD evidence |

### TDD Cycle Evidence
| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 10/10 | ✅ Written | ✅ `-k 'serves_runtime_session_endpoints_and_svg or serves_runtime_ready_static_viewer or wheel or drag_pan'` passed after changes | ✅ Order asserted in 2 HTML scenarios | ✅ Minimal markup reorder only |
| 1.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 10/10 | ✅ Written | ✅ Same targeted run passed | ✅ Sidebar wheel isolation + compact layout contract covered across HTML and harness scenarios | ✅ Dense CSS only, no contract changes |
| 2.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 10/10 | ✅ Written | ✅ Same targeted run passed | ✅ Wheel zoom and drag-pan cover distinct viewport state paths | ✅ Reused existing zoom state |
| 2.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 10/10 | ✅ Written | ✅ Same targeted run passed | ✅ Drag-pan movement plus zero-request assertion cover behavior and contract boundary | ✅ Native scroll-based pan only |
| 3.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 10/10 | ✅ Written | ✅ Same targeted run passed | ✅ Sidebar and viewport scroll offsets asserted independently | ✅ Snapshot grew only with required fields |
| 3.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 10/10 | ✅ Written | ✅ Same targeted run passed | ✅ Separate sidebar wheel and viewport drag helpers prove different input paths | ✅ Helper surface kept minimal |
| 4.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 10/10 | ✅ Written | ✅ `-k 'serves_runtime_session_endpoints_and_svg or serves_runtime_ready_static_viewer'` passed after the follow-up fix | ✅ Server HTML + static asset assertions now cover the absence of hidden `runtime-status` plumbing in HTML/CSS/JS across two boot paths | ✅ Clean |
| 4.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 10/10 | ✅ Written | ✅ Same targeted run passed | ✅ Sidebar wheel, viewport wheel, and drag-pan each have dedicated assertions | ✅ Clean |
| 4.3 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 10/10 | ✅ Written | ✅ `pytest tests/integration/test_mbse_workbench.py` passed | ✅ Targeted RED/GREEN run plus full file verification | ➖ None needed |

### Test Summary
- **Baseline**: `pytest tests/integration/test_mbse_workbench.py` → 10 passed
- **RED**: `pytest tests/integration/test_mbse_workbench.py -k 'serves_runtime_session_endpoints_and_svg or serves_runtime_ready_static_viewer or wheel or drag_pan'` → 5 failed, 1 passed, 7 deselected
- **GREEN**: `pytest tests/integration/test_mbse_workbench.py -k 'serves_runtime_session_endpoints_and_svg or serves_runtime_ready_static_viewer'` → 2 passed, 11 deselected
- **Verification**: `pytest tests/integration/test_mbse_workbench.py` → 13 passed
- **Total tests written**: 3 new integration scenarios plus tightened assertions in 2 existing server/static tests
- **Total tests passing**: 13
- **Layers used**: Integration (13)
- **Approval tests**: None — behavior changed by spec, not by refactor-only work
- **Pure functions created**: 0

### Deviations from Design
None — implementation matches design.

### Issues Found
None.

### Remaining Tasks
- [ ] None.

### Workload / PR Boundary
- Mode: single PR
- Current work unit: full slice
- Boundary: limited to `src/mbse/web/static/*`, `tests/integration/test_mbse_workbench.py`, and `tests/support/viewer_browser_harness.py`
- Estimated review budget impact: stayed within the forecasted frontend-only batch

### Status
9/9 tasks complete. Ready for archive.
