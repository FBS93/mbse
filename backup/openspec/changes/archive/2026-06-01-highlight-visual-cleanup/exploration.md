## Exploration: highlight-visual-cleanup

### Current State
`viewer.js` applies `is-active-state` and `is-active-transition` directly to the exact SVG element resolved by ID. In real Graphviz output, those IDs sit on wrapper `<g>` elements, not on isolated border-only shapes: a state group contains multiple `polygon`/`text` children, a compound-state cluster contains multiple `polygon`/`text` children, and a transition group contains the edge `path`, arrowhead `polygon`, and event-label `text`. `viewer.css` currently styles the whole highlighted group with broad stroke rules, so the highlight surface is too coarse for the new goal of emphasizing contours/arrows/background while keeping text visually neutral.

### Affected Areas
- `src/mbse/web/static/viewer.js` — current highlight application stays group-oriented by exact SVG ID.
- `src/mbse/web/static/viewer.css` — current state/transition highlight rules are too broad for text exclusion.
- `src/mbse/infrastructure/templates/hsm_v1.dot.j2` — explains the state/compound-state SVG structure Graphviz emits from HTML-like labels.
- `tests/support/viewer_browser_harness.py` — current harness only records which IDs received highlight classes, not descendant-shape targeting.
- `tests/integration/test_mbse_workbench.py` — browser-facing workbench coverage will need assertions for the refined visual contract.

### Approaches
1. **CSS-only descendant targeting on existing highlight groups** — keep JS as-is, but change CSS so state highlights target only descendant shapes/background polygons and transition highlights target only edge path/arrow polygons, explicitly excluding `text`.
   - Pros: Smallest code delta; preserves exact-ID contract; no backend or SVG-generation change; fits the requested light iteration.
   - Cons: Relies on current Graphviz child-shape patterns (`polygon`, `path`, `ellipse`, `text`) and may need careful selectors for compound-state clusters vs leaf nodes.
   - Effort: Low

2. **JS-assisted structural tagging** — after resolving a highlighted SVG group by exact ID, walk its descendants and add finer-grained classes to shape nodes vs text nodes.
   - Pros: More explicit control over contours, arrowheads, fills, and labels; less CSS guesswork about Graphviz child ordering.
   - Cons: More moving parts in `viewer.js`; more harness/test updates; unnecessary complexity for a purely visual polish if current SVG structure is already stable enough.
   - Effort: Medium

### Recommendation
Use **CSS-only descendant targeting on existing highlight groups**. Keep `viewer.js` exact-ID behavior unchanged, and refine `viewer.css` so active states style only non-text descendants (contours plus a mild same-hue fill-intensity bump) while active transitions style only the edge path and arrowhead, not the event-label text. This is the minimal clean approach because the runtime/view-model contract already gives the correct authored IDs, and the real SVG structure is predictable enough to exclude text without introducing new DOM mutation logic.

### Risks
- Graphviz emits compound states and leaf states with different polygon stacks, so selectors must be validated against both structures.
- A too-broad state selector could accidentally emphasize internal divider polygons, not just the outer contour/background.
- Current browser-harness tests prove highlight IDs, not descendant visual targeting, so coverage must expand before implementation.

### Ready for Proposal
Yes — propose a frontend-only change that preserves exact-ID highlighting, excludes all state/event label text from highlight styling, and tightens visuals through descendant shape selectors rather than new runtime or SVG-generation behavior.
