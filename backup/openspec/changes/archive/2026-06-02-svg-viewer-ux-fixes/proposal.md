# Proposal: SVG Viewer UX Fixes

## Intent

Correct three viewer UX regressions in the existing frontend-only SVG workbench: drag pan should feel continuous without browser text selection, first load and `Reset view` should fit the full diagram, and scrolling should stay isolated between page, sidebar, and diagram canvas.

## Scope

### In Scope
- Suppress text selection and preserve drag ownership while panning the SVG viewport.
- Recompute fit-based initial view and `Reset view` from current viewport/layout size so the full SVG is visible, even for large diagrams.
- Align overflow behavior so the page does not scroll, the sidebar scrolls only on overflow, and the diagram viewport scrolls only when zoomed content exceeds its bounds.

### Out of Scope
- Any backend, runtime bridge, session, or Graphviz rendering change.
- A full pan/zoom model redesign such as transform-based freeform canvas navigation.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `graphviz-svg-workbench`: refine the client-side SVG view-controls contract for drag pan, fit/reset behavior, and scrollbar isolation.

## Approach

Keep the current scroll-based viewport model. Harden drag handling in `viewer.js`, separate fit-baseline math from the interactive minimum zoom, recompute the baseline on load/reset/layout-width changes, and make the scaled stage dimensions track effective zoom so overflow reflects visible content size. Use CSS to lock page scrolling and keep sidebar/canvas overflow independent.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/specs/graphviz-svg-workbench/spec.md` | Modified | Add UX-correction delta requirements |
| `src/mbse/web/static/viewer.js` | Modified | Pan ownership, fit/reset recomputation, zoom/layout sizing |
| `src/mbse/web/static/viewer.css` | Modified | Page/sidebar/canvas overflow isolation and selection rules |
| `src/mbse/web/static/index.html` | Modified | No structural redesign expected; keep current split layout contract |
| `tests/integration/test_mbse_workbench.py` | Modified | Cover fit/reset and scroll isolation regressions |
| `tests/support/viewer_browser_harness.py` | Modified | Expose safe assertions for drag and overflow behavior |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Layout sizing and visual zoom diverge again | Med | Test fitted, default, and zoomed overflow states explicitly |
| Drag handling interferes with splitter/sidebar behavior | Low | Scope handlers to viewport pan lifecycle only |

## Rollback Plan

Revert the frontend JS/CSS/HTML delta and matching spec/test updates; no data migration or backend rollback is required.

## Dependencies

- `openspec/changes/svg-viewer-ux-fixes/exploration.md`
- Existing `graphviz-svg-workbench` capability

## Success Criteria

- [ ] Initial load and `Reset view` both fit the full SVG within the current viewport.
- [ ] Drag pan does not trigger text selection and remains continuous through normal pointer movement.
- [ ] The document body stays fixed, sidebar scroll is independent, and diagram scrollbars appear only when zoomed content exceeds the viewport.
