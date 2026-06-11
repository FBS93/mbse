## Exploration: workbench-ui-compact-sidebar-pan

### Current State
The current workbench is already frontend-only for layout and interaction changes: `index.html` renders a sidebar with `Reset`, `Variables`, `Events`, and `Status`; `viewer.css` keeps a two-column layout with the diagram inside scrollable `#svg-viewport`; and `viewer.js` owns client-side wheel zoom by scaling `#svg-stage` while leaving runtime calls limited to reset, event dispatch, and variable updates. There is no diagram drag-pan behavior today, and the sidebar itself is not explicitly constrained to its own independent scroll container.

### Affected Areas
- `src/mbse/web/static/index.html` — reorder sections to `Reset -> Events -> Variables`, remove the empty `Status` block, and keep the sidebar shell minimal.
- `src/mbse/web/static/viewer.css` — make sidebar sections denser, give the sidebar its own vertical overflow behavior, and keep diagram overflow isolated to the diagram pane.
- `src/mbse/web/static/viewer.js` — preserve existing runtime endpoints, keep wheel zoom scoped to `#svg-viewport`, and add client-only drag-pan behavior.
- `tests/integration/test_mbse_workbench.py` — update markup assertions (`Status` removed, order changed) and add/adjust behavior coverage for sidebar-vs-diagram wheel separation plus drag-pan.
- `tests/support/viewer_browser_harness.py` — likely extend the harness with minimal scroll state and pointer/mouse event simulation because it currently supports wheel only.
- `openspec/specs/graphviz-svg-workbench/spec.md` — current main spec still requires `Variables` before `Events` and still mentions status/error feedback, so the requested UI iteration needs a spec delta before apply.

### Approaches
1. **Compact shell + drag-to-scroll viewport pan** — keep zoom as the existing `scale(...)` transform, make the sidebar independently scrollable with CSS, scope wheel behavior by target (`sidebar` scrolls naturally, `diagram` zooms), and implement diagram pan by updating `#svg-viewport.scrollLeft/scrollTop` during mouse drag.
   - Pros: Smallest safe slice, reuses existing scroll container, avoids introducing a second transform state, keeps backend/runtime fully untouched.
   - Cons: Pan only works when the zoomed/content area can actually scroll; tests need harness support for scroll offsets and drag events.
   - Effort: Low

2. **Compact shell + translated stage pan state** — add explicit pan coordinates to viewer state and combine `translate(...) scale(...)` on `#svg-stage`.
   - Pros: Pan works even when native overflow is limited; behavior can feel more canvas-like.
   - Cons: More moving parts, more risk of zoom/pan math bugs, and a larger harness/test surface for a frontend-only polish request.
   - Effort: Medium

### Recommendation
Use **Compact shell + drag-to-scroll viewport pan**. It is the narrowest path because the diagram already lives in a dedicated overflow container, wheel zoom is already isolated in `viewer.js`, and the requested sidebar cleanup is pure HTML/CSS. This keeps the runtime contract frozen and adds pan as viewport movement rather than as a new visual transform model.

### Risks
- The current main spec is not aligned with the new requested order/removal: it still requires `Reset`, `Variables`, `Events`, and status/error feedback, so proposal/spec work must update that contract first.
- The current browser harness has no notion of sidebar scroll, viewport scroll offsets, or drag lifecycle, so verification for pan/scroll separation will require a small but real harness extension.
- Drag-to-scroll pan depends on overflow; if a diagram fits fully inside the viewport at current zoom, dragging will have little or no visible effect unless later expanded to transform-based pan.

### Ready for Proposal
Yes — propose a frontend-only delta that updates the sidebar hierarchy to `Reset -> Events -> Variables`, removes the empty status section, requires independent sidebar scrolling, keeps wheel zoom confined to the diagram viewport, and adds client-side drag-pan using viewport scroll movement without backend changes.
