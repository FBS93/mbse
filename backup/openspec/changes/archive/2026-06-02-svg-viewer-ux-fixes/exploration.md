## Exploration: svg-viewer-ux-fixes

### Current State
The viewer loads the SVG into `#svg-root`, computes one fit baseline during `loadSession()`, and applies zoom by setting `transform: scale(...)` on `#svg-stage`. Panning is implemented with viewport `mousedown/mousemove/mouseup` handlers that directly mutate `scrollLeft/scrollTop`. The sidebar and diagram live in one grid layout, with sidebar scrolling enabled by CSS and viewport scrolling delegated to `overflow: auto`.

Three implementation details explain the reported UX issues. First, pan drag does not suppress browser text selection and does not keep pointer ownership once the pointer leaves the viewport, so SVG labels can be selected/underlined and drag can feel sticky. Second, fit/reset is constrained by `MIN_ZOOM = 0.5`, so larger diagrams cannot scale below 50% even when needed to fit the full viewport. Third, zoom is purely visual (`transform: scale`) while the scroll container still measures the stage at its unscaled layout size, so canvas scrollbars can appear even when the fitted diagram is visually inside the viewport. Reset also reuses a baseline captured only once, so it can become stale after splitter resize.

### Affected Areas
- `src/mbse/web/static/viewer.js` — current zoom, fit-baseline, reset-view, panning, and splitter behavior all live here.
- `src/mbse/web/static/viewer.css` — viewport overflow, selection behavior, and panel scroll isolation are controlled here.
- `src/mbse/web/static/index.html` — likely unchanged structurally, but it defines the viewport/sidebar split used by the fix.
- `tests/integration/test_mbse_workbench.py` — existing viewer interaction coverage should be extended for fit/reset and scrollbar-related regressions.
- `tests/support/viewer_browser_harness.py` — harness will likely need small extensions to observe recomputed baselines and drag-suppression behavior safely.

### Approaches
1. **Targeted viewport behavior correction** — Keep the current DOM structure, but fix drag ownership/selection suppression, allow fit below 0.5, recompute fit on reset and resize, and make the scaled stage report layout dimensions that match the current zoom.
   - Pros: Smallest safe slice; stays frontend-only; aligns with current spec boundaries; likely fits one reviewable PR.
   - Cons: Still builds on the current scroll-container model; requires careful stage sizing so scrollbars match zoom.
   - Effort: Medium

2. **Pan/zoom architecture rewrite** — Replace scroll-based pan with transform-based translate/scale and rework the viewport interaction model more broadly.
   - Pros: Cleaner long-term canvas model; more flexibility for future gestures.
   - Cons: Much larger change; higher regression risk; exceeds the stated “UX correction, not redesign” scope.
   - Effort: High

### Recommendation
Use **Targeted viewport behavior correction**. The smallest safe implementation is to keep scroll-based pan, but harden it: suppress selection while dragging, retain drag continuity with pointer capture or equivalent document-level ownership, remove the hard 0.5 floor from fit/reset by separating interactive min zoom from fit zoom, recompute the fit baseline on reset and after layout width changes, and make the stage/root dimensions follow the zoomed SVG size so viewport scrollbars appear only when the zoomed content exceeds the viewport.

Forecast: small frontend-only change, likely ~120-220 changed lines across JS/CSS/tests. Decision needed before apply: No. Chained PRs recommended: No. 400-line budget risk: Low.

### Risks
- Scrollbar correctness depends on matching visual zoom to layout size; a partial fix could make pan math or centering inconsistent.
- Pointer-capture/document-level drag handling must not break existing test harness assumptions or sidebar/splitter interactions.

### Ready for Proposal
Yes — propose a frontend-only UX correction scoped to `viewer.js`, `viewer.css`, and viewer interaction tests, with explicit non-goals of backend/runtime changes and no pan/zoom redesign.
