# Design: Workbench UX Slice A

## Technical Approach

Implement Slice A as a static viewer delta only: keep the current HTML/CSS/JS shell, preserve the existing runtime POST endpoints, and add local-only layout/view state for splitter width and diagram fit baseline.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Split layout | CSS grid with `grid-template-columns: var(--sidebar-width) 0.5rem minmax(0, 1fr)` and a dedicated splitter element between sidebar and diagram | Replacing layout with flexbox; overlay drag handle inside sidebar | Grid keeps the current two-pane structure, makes the handle explicit, and limits the change to static assets. |
| Variable rows | Keep one `<form class="variable-row">` per variable, but render one visual row with name, current value/unset, input, and submit button in a single grid line | Rebuilding as cards; merging all variables into one form | Reuses the existing submit contract per variable and narrows the change to presentation. |
| View reset model | Add client-only `Reset view` that restores a stored fit baseline `{zoomScale, scrollLeft, scrollTop}`; keep `Reset runtime` mapped only to `/api/runtime/reset` | Reusing runtime reset for both; introducing persistent view state | Cleanly separates runtime from viewport behavior and matches Slice A scope. |
| Fit baseline | Compute once after SVG injection from viewport size and SVG bounding box / viewBox dimensions, clamp into existing zoom limits, center via scroll offsets | Fixed zoom `1`; full camera rewrite | Smallest safe extension of the current scale + native-scroll model. |

## Data Flow

`loadSession()` → fetch session + SVG → inject SVG → measure viewport/SVG → compute fit baseline → `applyViewBaseline()` → wire wheel zoom, drag pan, reset-runtime, reset-view → runtime actions still call existing endpoints and only rerender snapshot/highlights.

## File Changes

| File | Action | Description |
|---|---|---|
| `openspec/changes/workbench-ux-slice-a/design.md` | Create | Slice A technical design artifact |
| `src/mbse/web/static/index.html` | Modify | Insert splitter element, add `Reset view` button next to `Reset runtime`, keep existing form IDs/endpoints |
| `src/mbse/web/static/viewer.css` | Modify | Convert fixed 2-column layout to explicit splitter grid; style one-line variable rows and drag handle |
| `src/mbse/web/static/viewer.js` | Modify | Add sidebar width state, splitter drag wiring, fit-baseline calculation, and client-only reset-view behavior |
| `tests/support/viewer_browser_harness.py` | Modify | Expose splitter drag and fit/reset-view state without adding backend behavior |
| `tests/integration/test_mbse_workbench.py` | Modify | Assert `Reset view` presence, client-only reset behavior, initial fit baseline, and unchanged runtime contract |

## Interfaces / Contracts

```js
viewerState = {
  zoomScale,
  isDragging,
  dragStartX,
  dragStartY,
  dragStartScrollLeft,
  dragStartScrollTop,
  sidebarWidthPx,
  fitBaseline: { zoomScale, scrollLeft, scrollTop }
}
```

- `Reset runtime`: unchanged `POST /api/runtime/reset`
- `Reset view`: no fetch; restore `fitBaseline`
- Variable submit/event submit payloads: unchanged

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Integration | Static shell includes splitter and separate reset controls | Existing server HTML assertions |
| Harness | Variable rows remain one-form-per-variable but render as one-line rows; `Reset view` performs no fetch | Extend QuickJS harness snapshot/assertions |
| Harness | Initial load computes fit baseline; wheel zoom/drag pan still work after fit | Simulate viewport geometry and verify transform/scroll restoration |

## Migration / Rollout

No migration required.

## Open Questions

- [ ] None blocking; Slice A stays limited to static viewer assets plus test support.
