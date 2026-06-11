# Tasks: Workbench UI Simplify v2

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 220-340 |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | Single PR, 3 reviewable batches |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Simplify sidebar markup and CSS | PR 1 | Keep runtime contract untouched |
| 2 | Swap shared variable editor + zoom buttons for inline edit + wheel zoom | PR 1 | JS-only behavior slice |
| 3 | Update integration coverage and extend browser harness only if current hooks are insufficient | PR 1 | Verification batch before merge |

## Phase 1: Sidebar Shell

- [x] 1.1 Update `src/mbse/web/static/index.html` to remove `Current state` and `Current snapshot`, move `#reset-form` above variables, keep only `Variables`, `Events`, and `Status` sections.
- [x] 1.2 Trim `src/mbse/web/static/viewer.css` to match the smaller sidebar and delete toolbar/shared-editor styling that the new markup no longer uses.
- [x] 1.3 Batch verify markup with targeted assertions in `tests/integration/test_mbse_workbench.py` for kept headings/buttons and forbidden removed labels.

## Phase 2: Inline Variable + Event Flow

- [x] 2.1 Refactor `src/mbse/web/static/viewer.js` so `renderVariableList()` outputs one compact editable row per declared variable using the existing `{ variable_id, value }` POST contract.
- [x] 2.2 Remove selected-variable state and the shared `#variable-form` wiring from `src/mbse/web/static/viewer.js`, preserving refresh-on-success/failure and explicit `unset` rendering.
- [x] 2.3 Keep `#event-form` as dropdown + send in `src/mbse/web/static/viewer.js`; only tighten enable/disable behavior if needed, with no payload or endpoint changes.
- [x] 2.4 Batch verify browser-side variable rendering/editability scenarios in `tests/integration/test_mbse_workbench.py` against the delta-spec requirements.

## Phase 3: Viewport Zoom

- [x] 3.1 Remove zoom toolbar markup from `src/mbse/web/static/index.html` and related CSS from `src/mbse/web/static/viewer.css`, keeping `#svg-viewport` and `#svg-stage` intact.
- [x] 3.2 Replace button-based zoom wiring in `src/mbse/web/static/viewer.js` with wheel handling scoped to `#svg-viewport`, reusing existing clamp constants and client-only `applyZoom()` state.
- [x] 3.3 Batch verify zoom in `tests/integration/test_mbse_workbench.py` by asserting wheel-driven `scale(...)` updates and zero extra runtime fetches.

## Phase 4: Harness + Final Guardrails

- [x] 4.1 Update `tests/support/viewer_browser_harness.py` only as needed to support per-row variable forms/submits and wheel events; avoid simulating unrelated browser features.
- [x] 4.2 Re-run and align all affected workbench integration scenarios in `tests/integration/test_mbse_workbench.py` so the slice stays frontend-only and spec-bounded.
- [x] 4.3 Confirm no backend/runtime files change outside `src/mbse/web/static/*` and the two test files before handing off to `sdd-apply`.
