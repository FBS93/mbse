## Exploration: workbench-svg-render-improvements

### Current State
The rendered SVG still gets the top `Variables` / `Events` summary from the DOT graph label in `src/mbse/infrastructure/templates/hsm_v1.dot.j2`, backed by `view.variables_block` and `view.events_block` from `prepare_hsm_render_view()`. State visuals also still collapse the state name plus any `on_entry` / `on_exit` text into one plain Graphviz label string: flat states render one boxed node label, and compound states render one cluster label. That means Slice C is a render-pipeline problem only today: the viewer shell, runtime bridge, and runtime semantics do not participate in this visual structure.

### Affected Areas
- `src/mbse/application/prepare_hsm_render.py` — currently builds `variables_block`, `events_block`, and one flattened `annotation_block` string per state.
- `src/mbse/domain/models.py` — `HsmPreparedRenderView` / `HsmRenderStateNode` likely need a smaller visual-data reshape if entry/exit must render in a dedicated lower compartment instead of one concatenated label blob.
- `src/mbse/infrastructure/templates/hsm_v1.dot.j2` — owns the top graph label and the actual state/cluster label markup that Graphviz turns into SVG.
- `tests/unit/mbse/test_hsm_render_view.py` — protects prepared render-view fields and DOT output expectations.
- `tests/integration/test_hsm_json_workbench.py` — protects rendered SVG/public-id stability for compound states and label output.

### Approaches
1. **Template-only removal + plain multiline labels** — drop the top graph label and keep state labels as plain escaped strings with better line breaks.
   - Pros: Smallest diff on paper.
   - Cons: Does not create a real upper/lower partition for state name vs entry/exit; readability gain is weak and brittle.
   - Effort: Low

2. **Small render-view reshape + HTML-table state labels** — stop emitting top-level variables/events blocks, keep runtime/viewer contracts unchanged, and render states with Graphviz HTML-like table labels so the title row and entry/exit row are separate compartments.
   - Pros: Still isolated to the render pipeline; actually matches the Slice C goal; works for both node labels and cluster labels without changing authored public IDs.
   - Cons: Needs a targeted model/test update because the current single `annotation_block` string is too coarse for clean compartment rendering.
   - Effort: Low/Medium

### Recommendation
Use **Small render-view reshape + HTML-table state labels**.

Smallest safe path:
- remove `view.variables_block` / `view.events_block` from the DOT output so the SVG no longer duplicates sidebar information;
- replace the current flattened state annotation payload with structured visual fields derived from existing inert metadata (`label`, `on_entry`, `on_exit` only);
- render flat states as HTML-table labels with one clear title row and one lower row for entry/exit lines;
- render compound states with the same title/body split on the cluster label, while keeping the existing private anchor convention for routing and keeping public authored IDs unchanged.

That keeps Slice C fully inside `prepare_hsm_render -> DOT template -> SVG`, with no viewer-shell or runtime-semantic drift.

### Risks
- The current tests assert exact plain-string label fragments such as `Variables:\l...` and `on_entry:\l...`; they will need focused updates, not broad rewrites.
- If the implementation tries to preserve the old single `annotation_block` string and parse it back inside the template, the label contract will become fragile fast.
- Compound-state HTML labels must preserve the existing exact public SVG id ownership on the cluster; otherwise the rendered-contract validation and highlight behavior can regress.

### Ready for Proposal
Yes — propose a render-only Slice C that removes duplicated top summary labels and introduces structured title/body state labels, explicitly keeping runtime semantics, highlight semantics, sidebar structure, and authored SVG IDs unchanged.
