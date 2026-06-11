# Design: Compact Sidebar and Diagram Pan Controls

## Technical Approach

Keep the change frontend-only inside the existing static workbench. Rework sidebar markup/CSS for denser operator controls, preserve wheel zoom on `#svg-viewport`, and add drag-pan by updating viewport scroll offsets instead of introducing transform-pan state or backend calls.

## Architecture Decisions

| Decision | Options | Choice | Rationale |
|---|---|---|---|
| Sidebar structure | Keep current order/status vs reorder/remove | `Reset -> Events -> Variables`, remove `Status` block | Matches delta spec and reduces vertical waste without touching runtime data flow. |
| Compactness model | New components vs tighten existing forms | Keep existing forms, shrink spacing/labels/buttons | Smallest safe slice; no new rendering model. |
| Sidebar scroll | Whole page scroll vs sidebar-owned scroll | Sidebar owns `overflow-y: auto` inside fixed-height layout | Isolates operator scrolling from diagram interaction. |
| Diagram pan | Transform translate state vs native scroll pan | Drag updates `#svg-viewport.scrollLeft/scrollTop` | Reuses existing overflow container and avoids zoom/pan math drift. |

## Data Flow

`/api/session.json` and existing runtime POSTs stay unchanged.

```text
session payload -> renderSession()
  -> renderSelectOptions(#event-select)
  -> renderVariableList(#variable-list)

sidebar wheel -> browser native sidebar scroll only
viewport wheel -> applyZoom() -> #svg-stage transform = scale(...)
viewport drag -> mouse delta -> #svg-viewport scrollLeft/scrollTop
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `openspec/changes/workbench-ui-compact-sidebar-pan/design.md` | Create | Technical design for this slice. |
| `src/mbse/web/static/index.html` | Modify | Reorder sections to Reset/Events/Variables, remove `Status`, keep same runtime form IDs. |
| `src/mbse/web/static/viewer.css` | Modify | Make sidebar column narrower and denser; add independent sidebar scrolling; keep diagram viewport overflow isolated. |
| `src/mbse/web/static/viewer.js` | Modify | Keep existing runtime endpoints; add local drag-pan handlers on `#svg-viewport`; remove status writes from visible UI dependency. |
| `tests/integration/test_mbse_workbench.py` | Modify | Assert new sidebar order/removal and client-only pan/scroll behavior. |
| `tests/support/viewer_browser_harness.py` | Modify | Add minimal sidebar scroll state plus viewport drag event simulation. |

## Interfaces / Contracts

No backend or runtime contract changes.

Local viewer state grows only as client view state:

```js
viewerState = {
  zoomScale,
  isDragging,
  dragStartX,
  dragStartY,
  dragStartScrollLeft,
  dragStartScrollTop,
};
```

Layout contract:
- Sidebar column: `minmax(15rem, 18rem)`
- Section order: `Reset`, `Events`, `Variables`
- `Status` markup removed
- Sidebar owns vertical overflow; diagram keeps its own overflow in `#svg-viewport`

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Integration | HTML no longer exposes `Status`; `Events` appears before `Variables` | Update existing server/browser assertions. |
| Integration | Sidebar wheel/scroll does not change zoom | Extend harness snapshot with sidebar scroll + zoom transform. |
| Integration | Viewport wheel still zooms without extra fetches | Reuse current wheel test with unchanged fetch assertions. |
| Integration | Drag-pan updates viewport scroll without runtime requests | Add harness drag helper and assert scroll offsets changed while fetch counts stay flat. |

## Migration / Rollout

No migration required.

## Open Questions

- [ ] Drag-pan is intentionally native-overflow based, so fully fitting diagrams may show little movement until zoom creates overflow.
- [ ] Pan release is kept scoped to viewport mouse events (`mousedown/mousemove/mouseup/mouseleave`) to keep the harness small; broader pointer-capture behavior is out of scope for this slice.
