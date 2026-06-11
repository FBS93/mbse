# Tasks: Workbench UX Slice A

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 320-430 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 layout/controls → PR 2 fit/reset-view |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: Yes
Chained PRs recommended: Yes
Chain strategy: pending
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Compact rows + split shell + reset buttons | PR 1 | `index.html` + `viewer.css` + light harness/test updates |
| 2 | Splitter drag + fit baseline + reset view | PR 2 | `viewer.js` + harness/test extensions; base on PR 1 |

## Phase 1: Shell And Layout

- [x] 1.1 Update `src/mbse/web/static/index.html` to add a splitter element and separate `Reset runtime` / `Reset view` controls without changing existing runtime form IDs or endpoints.
- [x] 1.2 Update `src/mbse/web/static/viewer.css` so `.layout` uses a resizable horizontal split and each `.variable-row` renders as one compact line with name, value/unset, input, and submit visible together.

## Phase 2: Client View Behavior

- [x] 2.1 Extend `src/mbse/web/static/viewer.js` state with `sidebarWidthPx` and `fitBaseline`, keeping one line per variable declaration in the source.
- [x] 2.2 Add splitter drag wiring in `viewer.js` so sidebar width changes stay local to the page session and trigger no runtime/backend fetches.
- [x] 2.3 Compute an initial full-diagram fit after SVG injection, clamp to existing zoom limits, apply it before first render settles, and preserve wheel zoom + drag pan behavior.
- [x] 2.4 Add client-only `Reset view` behavior in `viewer.js` that restores the stored fit baseline while `Reset runtime` remains mapped only to `/api/runtime/reset`.

## Phase 3: Harness Extension

- [x] 3.1 Extend `tests/support/viewer_browser_harness.py` snapshot data so tests can observe reset-view fetch counts, sidebar width changes, fit baseline, and viewport scroll/zoom restoration.
- [x] 3.2 Add harness actions for dragging the splitter and invoking `Reset view`, keeping support limited to Slice A frontend assertions only.

## Phase 4: Verification By Batch

- [x] 4.1 Batch 1 verification: update `tests/integration/test_mbse_workbench.py` HTML/harness checks for separate reset controls, compact variable rows, and unchanged runtime endpoints/contracts.
- [x] 4.2 Batch 2 verification: add harness coverage for splitter resize staying client-only, initial fit baseline, `Reset view` restoring fit, and wheel zoom/drag pan still working after fit.
- [x] 4.3 Run `pytest tests/integration/test_mbse_workbench.py -k "viewer or workbench"` after each batch; if either batch grows beyond review scope, stop before Slice B/C behavior.
