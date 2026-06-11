# Proposal: Workbench UX Slice A

## Intent

Deliver a smaller, clearer workbench UX for the current frontend without changing runtime behavior: make variables truly one-line compact, add a resizable split between sidebar and diagram, separate `Reset runtime` from `Reset view`, and open on a full-diagram fit.

## Scope

### In Scope
- Compact variable rows to a single visual line per declared variable.
- Add a frontend-only resizable split between the sidebar and SVG viewport.
- Replace the single reset action with distinct `Reset runtime` and `Reset view` controls.
- Initialize the diagram view from a computed full-diagram fit and let `Reset view` restore that fit baseline.

### Out of Scope
- Any backend, runtime bridge, highlight, or SVG rendering pipeline change.
- Slice B and Slice C work, including highlight polish, internal SVG render changes, or runtime semantic changes.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `graphviz-svg-workbench`: refine the frontend UX contract for variable compactness, resizable split layout, separate runtime/view reset actions, and fit-based initial/reset view behavior.

## Approach

Use the existing static workbench architecture. Keep runtime mutations on the current endpoints, add local client view state for sidebar width and fit baseline, and preserve the native scroll + wheel zoom + drag-pan model. Treat this as a bounded HTML/CSS/JS delta only.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/specs/graphviz-svg-workbench/spec.md` | Modified | Add Slice A UX delta requirements |
| `src/mbse/web/static/index.html` | Modified | Splitter and separate reset controls |
| `src/mbse/web/static/viewer.css` | Modified | Compact one-line rows and resizable layout |
| `src/mbse/web/static/viewer.js` | Modified | Fit baseline, reset-view behavior, sidebar width state |
| `tests/integration/test_mbse_workbench.py` | Modified | Cover fit/reset-view and frontend-only UX contract |
| `tests/support/viewer_browser_harness.py` | Modified | Expose fit/reset-view and splitter behavior for tests |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Fit math behaves differently across SVG sizes | Med | Base fit on measured viewport/SVG bounds and test representative diagrams |
| Splitter adds flaky browser-test interactions | Med | Keep handle narrow, state local, and harness support minimal |
| Compact rows reduce readability | Low | Keep labels visible and avoid hiding current values |

## Rollback Plan

Revert the static frontend and spec delta for this slice; no backend migration, data migration, or runtime rollback is needed.

## Dependencies

- Existing `graphviz-svg-workbench` capability and the completed exploration for `workbench-ux-slice-a`.

## Success Criteria

- [ ] Slice A is specified as a frontend-only UX change.
- [ ] Variables are required to render in a denser one-line format.
- [ ] The sidebar/diagram split is resizable without changing runtime semantics.
- [ ] The initial diagram view and `Reset view` both restore a full-diagram fit baseline.
