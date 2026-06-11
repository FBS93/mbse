# Proposal: Compact Sidebar and Diagram Pan Controls

## Intent

Deliver a tighter workbench UX that keeps the operator sidebar useful without constant scrolling: reorder it to `Reset -> Events -> Variables`, remove the `Status` section, and add clearer diagram interaction boundaries while keeping runtime behavior unchanged.

## Scope

### In Scope
- Reorder sidebar sections to `Reset`, `Events`, `Variables`.
- Remove visible `Status` UI and make sidebar sections denser, smaller, and self-contained.
- Require independent sidebar vertical scrolling, wheel zoom only in the diagram, and drag-pan in the SVG viewport.

### Out of Scope
- Backend, runtime bridge, snapshot shape, mutation semantics, or highlight logic changes.
- New status surfaces, mobile redesign, or transform-based freeform canvas pan.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `graphviz-svg-workbench`: tighten sidebar hierarchy and compactness requirements, remove status from the required UI contract, and define independent sidebar scroll plus diagram pan/zoom behavior.

## Approach

Use a frontend-only HTML/CSS/JS update. Keep wheel zoom on `#svg-viewport`, let sidebar wheel input scroll only the sidebar container, and implement drag-pan by moving `#svg-viewport` scroll offsets instead of adding new runtime or transform state.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/specs/graphviz-svg-workbench/spec.md` | Modified | Add spec delta source for compact sidebar and interaction boundaries |
| `src/mbse/web/static/index.html` | Modified | Reorder/remove sidebar sections |
| `src/mbse/web/static/viewer.css` | Modified | Increase sidebar density and isolate sidebar scroll |
| `src/mbse/web/static/viewer.js` | Modified | Preserve zoom and add client-side drag-pan |
| `tests/integration/test_mbse_workbench.py` | Modified | Verify new ordering and interaction boundaries |
| `tests/support/viewer_browser_harness.py` | Modified | Model sidebar scroll and drag-pan events |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Compact UI hurts readability | Med | Keep labels explicit and test with current variable/event content |
| Drag-pan feels inactive on fully fitting diagrams | Med | Document native-overflow limitation and keep zoom available |
| Harness gaps slow verification | Med | Extend only the minimal scroll/pointer behavior needed |

## Rollback Plan

Revert the frontend markup/CSS/JS slice and restore the prior sidebar order plus status block; no data or runtime migration is needed.

## Dependencies

- Existing `graphviz-svg-workbench` spec and current static workbench frontend.

## Success Criteria

- [ ] Proposal/spec work clearly defines a frontend-only UX outcome centered on sidebar compactness.
- [ ] The sidebar contract requires `Reset -> Events -> Variables` and no `Status` section.
- [ ] Wheel input over the sidebar scrolls only that panel, while wheel over the diagram zooms.
- [ ] Diagram drag updates viewport pan without backend or runtime contract changes.
