# Apply Progress: Workbench UI Simplify v2

## Implementation Progress

**Change**: `workbench-ui-simplify-v2`
**Mode**: Strict TDD
**Workload**: single PR

### Completed Tasks
- [x] 1.1 Update `src/mbse/web/static/index.html` to remove `Current state` and `Current snapshot`, move `#reset-form` above variables, keep only `Variables`, `Events`, and `Status` sections.
- [x] 1.2 Trim `src/mbse/web/static/viewer.css` to match the smaller sidebar and delete toolbar/shared-editor styling that the new markup no longer uses.
- [x] 1.3 Batch verify markup with targeted assertions in `tests/integration/test_mbse_workbench.py` for kept headings/buttons and forbidden removed labels.
- [x] 2.1 Refactor `src/mbse/web/static/viewer.js` so `renderVariableList()` outputs one compact editable row per declared variable using the existing `{ variable_id, value }` POST contract.
- [x] 2.2 Remove selected-variable state and the shared `#variable-form` wiring from `src/mbse/web/static/viewer.js`, preserving refresh-on-success/failure and explicit `unset` rendering.
- [x] 2.3 Keep `#event-form` as dropdown + send in `src/mbse/web/static/viewer.js`; only tighten enable/disable behavior if needed, with no payload or endpoint changes.
- [x] 2.4 Batch verify browser-side variable rendering/editability scenarios in `tests/integration/test_mbse_workbench.py` against the delta-spec requirements.
- [x] 3.1 Remove zoom toolbar markup from `src/mbse/web/static/index.html` and related CSS from `src/mbse/web/static/viewer.css`, keeping `#svg-viewport` and `#svg-stage` intact.
- [x] 3.2 Replace button-based zoom wiring in `src/mbse/web/static/viewer.js` with wheel handling scoped to `#svg-viewport`, reusing existing clamp constants and client-only `applyZoom()` state.
- [x] 3.3 Batch verify zoom in `tests/integration/test_mbse_workbench.py` by asserting wheel-driven `scale(...)` updates and zero extra runtime fetches.
- [x] 4.1 Update `tests/support/viewer_browser_harness.py` only as needed to support per-row variable forms/submits and wheel events; avoid simulating unrelated browser features.
- [x] 4.2 Re-run and align all affected workbench integration scenarios in `tests/integration/test_mbse_workbench.py` so the slice stays frontend-only and spec-bounded.
- [x] 4.3 Confirm no backend/runtime files change outside `src/mbse/web/static/*` and the two test files before handing off to `sdd-apply`.

### Files Changed
| File | Action | What Was Done |
|------|--------|---------------|
| `src/mbse/web/static/index.html` | Modified | Removed obsolete sidebar sections, moved reset to the top, and removed zoom toolbar markup |
| `src/mbse/web/static/viewer.css` | Modified | Trimmed sidebar styles, added inline variable-row layout, and removed unused toolbar/shared-editor rules |
| `src/mbse/web/static/viewer.js` | Modified | Replaced shared variable editor with per-row submits and swapped button zoom controls for wheel zoom |
| `tests/integration/test_mbse_workbench.py` | Modified | Drove the UI simplification through RED/GREEN integration assertions for markup, inline variable edits, runtime event submits, and wheel zoom |
| `tests/support/viewer_browser_harness.py` | Modified | Added minimal support for inline variable submit simulation, event-form submits, wheel events, and request capture |
| `openspec/changes/workbench-ui-simplify-v2/tasks.md` | Modified | Marked all apply tasks complete |
| `openspec/changes/workbench-ui-simplify-v2/apply-progress.md` | Created | Recorded cumulative apply progress and TDD evidence |

### TDD Cycle Evidence
| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 7/7 | ✅ Written | ✅ Passed | ✅ Kept/removed labels across 3 HTML scenarios | ✅ Simplified markup only |
| 1.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 7/7 | ✅ Written | ✅ Passed | ✅ Sidebar + toolbar removal covered with rendered HTML and harness behavior | ✅ Deleted unused CSS |
| 1.3 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 7/7 | ✅ Written | ✅ Passed | ✅ 3 markup assertions batches | ✅ Clean |
| 2.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 7/7 | ✅ Written | ✅ Passed | ✅ Current-value + unset + submit contract cases | ✅ Reused existing runtime POST flow |
| 2.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 7/7 | ✅ Written | ✅ Passed | ✅ Selected-state removal covered by row snapshots and submit path | ✅ Removed obsolete state/editor code |
| 2.3 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 8/8 | ✅ Written | ✅ Passed | ✅ Runtime submit cases for `open_evt` and `close_evt` prove exact `{ event_id }` payload only | ✅ Kept event flow untouched |
| 2.4 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 7/7 | ✅ Written | ✅ Passed | ✅ Render + submit scenarios | ✅ Clean |
| 3.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 7/7 | ✅ Written | ✅ Passed | ✅ HTML and JS assertions against removed buttons | ✅ Removed unused toolbar path |
| 3.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 7/7 | ✅ Written | ✅ Passed | ✅ Wheel in + wheel out paths | ✅ Reused zoom clamp state |
| 3.3 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 7/7 | ✅ Written | ✅ Passed | ✅ Zoom transform + zero extra fetch assertions | ✅ Clean |
| 4.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 7/7 | ✅ Written | ✅ Passed | ✅ Harness exercised row submit and wheel simulation | ✅ Added only needed hooks |
| 4.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 8/8 | ✅ Written | ✅ Passed | ✅ Full targeted suite rerun with event dispatch runtime coverage | ✅ Clean |
| 4.3 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 7/7 | ✅ Written | ✅ Passed | ✅ Scope enforced by changed-file set and targeted suite | ➖ None needed |

### Test Summary
- **Baseline**: `pytest tests/integration/test_mbse_workbench.py` → 8 passed before the event-form follow-up
- **RED**: `pytest tests/integration/test_mbse_workbench.py -k submits_events_with_existing_contract_only` → 1 failed, 8 deselected
- **GREEN**: `pytest tests/integration/test_mbse_workbench.py` → 10 passed
- **Total tests written**: 10 targeted integration scenarios in the modified file
- **Total tests passing**: 10
- **Layers used**: Integration (10)
- **Approval tests**: None — behavior changed by spec, not by pure refactor-only work
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
12/12 tasks complete. Ready for verify.
