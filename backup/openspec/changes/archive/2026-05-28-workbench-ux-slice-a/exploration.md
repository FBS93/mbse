## Exploration: workbench-ux-slice-a

### Current State
The current workbench already keeps this area frontend-only. `index.html` exposes a fixed two-pane shell with `Reset`, `Events`, and `Variables`. `viewer.js` renders one form per variable, applies wheel zoom by scaling `#svg-stage`, and pans by mutating `#svg-viewport.scrollLeft/scrollTop`. There is no resize handle between sidebar and canvas, no separate `Reset view` control, and no fit-to-diagram initialization step: startup always calls `applyZoom(1)`.

### Affected Areas
- `src/mbse/web/static/index.html` — add the smallest possible splitter handle and separate `Reset runtime` / `Reset view` controls without changing runtime form IDs.
- `src/mbse/web/static/viewer.css` — replace the fixed sidebar column with a resizable-width layout contract and tighten variable rows to a true one-line presentation.
- `src/mbse/web/static/viewer.js` — introduce local view state for sidebar width and “base fit” initialization, while keeping runtime POSTs unchanged.
- `tests/integration/test_mbse_workbench.py` — update static assertions and add coverage for reset-view behavior staying client-side.
- `tests/support/viewer_browser_harness.py` — extend the harness only enough to observe fit/reset-view state and, if implemented, splitter drag state.
- `openspec/specs/graphviz-svg-workbench/spec.md` — the current main spec does not yet require resizable split, initial fit-to-diagram, or distinct reset-view control, so a delta spec is needed before apply.

### Approaches
1. **Native scroll viewport + computed fit baseline** — keep the existing `scale(...)` plus native scroll pan model, compute a fit scale after SVG load from viewport-vs-SVG dimensions, and define `Reset view` as “restore fit scale and scroll origin derived from that baseline”.
   - Pros: Smallest safe delta, preserves current pan model, no backend/runtime drift, fits the repo’s existing viewer architecture.
   - Cons: Needs small DOM measurement logic and harness support for SVG/viewport sizing; fit centering can be brittle if implemented with ad-hoc numbers.
   - Effort: Low

2. **New transform camera model** — replace the current scroll-pan behavior with explicit zoom/pan coordinates and make fit/reset operate on that camera state.
   - Pros: Cleaner long-term canvas model and easier future polish for navigation.
   - Cons: Larger rewrite, conflicts with the explicit “smallest and safest” goal, higher regression risk against already-verified pan behavior.
   - Effort: Medium

### Recommendation
Use **Native scroll viewport + computed fit baseline**. Keep runtime semantics frozen and treat Slice A as a thin extension of the current static viewer: compact the existing variable row markup into one visual line, add one frontend-only splitter between sidebar and diagram, and add a dedicated `Reset view` action that restores a stored fit baseline computed once from the loaded SVG. Then wheel zoom and drag-pan continue operating on top of that baseline exactly as they do today.

For the resizable split, the safest implementation path is a CSS custom property such as `--sidebar-width` owned by the layout container plus pointer/mouse drag on a narrow splitter element. That keeps the change local to static assets and avoids introducing any backend or persistence concerns.

### Risks
- The current main spec only guarantees compact sidebar + wheel zoom + drag-pan; resizable split, fit-on-load, and `Reset view` need an explicit delta before implementation.
- The present pan model depends on native overflow. Fit logic must guarantee useful overflow after user zooms, or pan can feel inert when the diagram fully fits.
- The browser harness is intentionally lightweight and does not currently model real SVG geometry, so test support for fit calculations is the main hidden cost in this slice.

### Ready for Proposal
Yes — propose a frontend-only delta limited to: one-line variable rows, resizable sidebar/canvas split, separate runtime/view reset controls, and initial fit-to-diagram view state with existing zoom/pan preserved above that baseline.
