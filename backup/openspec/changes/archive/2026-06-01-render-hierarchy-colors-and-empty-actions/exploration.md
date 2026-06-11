## Exploration: render-hierarchy-colors-and-empty-actions

### Current State
The render pipeline is already isolated in `prepare_hsm_render_view() -> render_hsm_dot() -> Graphviz SVG`, which matches the requested scope boundary. Today `prepare_hsm_render_view()` preserves authored IDs, depth-first ordering, and private `__anchor` routing for compound states, while `hsm_v1.dot.j2` renders flat states as boxed nodes and compound states as cluster labels. Two gaps matter for this slice: the title/body partition disappears when `body_lines` is empty because the template omits the second table row, and there is no state-owned background color logic at all for leaf states, compound clusters, or hierarchy depth.

### Affected Areas
- `src/mbse/application/prepare_hsm_render.py` — best place to add deterministic per-state visual metadata while keeping authored IDs, ordering, and anchor routing unchanged.
- `src/mbse/domain/models.py` — `HsmRenderStateNode` likely needs a minimal visual-data extension such as depth and/or derived color fields.
- `src/mbse/infrastructure/templates/hsm_v1.dot.j2` — currently suppresses the body row when empty and owns the node/cluster label markup where color and always-present partitioning would be applied.
- `tests/unit/mbse/test_hsm_render_view.py` — should protect the new always-present partition and deterministic depth/color preparation without touching runtime behavior.
- `tests/integration/test_hsm_json_workbench.py` — should keep proving exact public SVG IDs remain unchanged while render output gains hierarchy coloring.

### Approaches
1. **Template-only depth styling** — keep render-view shape mostly as-is and compute depth colors directly inside the recursive Jinja template.
   - Pros: Very small Python diff; stays inside render output.
   - Cons: Jinja arithmetic/palette logic gets brittle fast, is harder to unit-test, and mixes render policy with markup.
   - Effort: Low

2. **Prepared visual metadata + thin template** — extend render-state view data with depth and deterministic derived colors, then let the template only render those prepared values while always emitting the title/body table structure.
   - Pros: Still render-only; deterministic algorithm is easy to test; keeps IDs and routing untouched; scales to unlimited depth without a hardcoded palette.
   - Cons: Slightly broader diff because model/test fixtures must evolve with the render view.
   - Effort: Low/Medium

### Recommendation
Use **Prepared visual metadata + thin template**.

Smallest safe slice:
- keep `highlightable_ids`, state ordering, authored public IDs, and private `{state.id}__anchor` routing exactly as they are;
- add hierarchy depth to each prepared state node and derive soft colors algorithmically from that depth using a deterministic formula instead of a fixed palette;
- render both flat states and compound clusters with the same HTML-table structure, but always keep the lower entry/exit partition present even when `body_lines` is empty;
- apply the derived colors to the whole state-owned visual surface so compound clusters and empty compounds are tinted too, without touching runtime or viewer code.

This keeps the change centered in the render pipeline and preserves the exact SVG ID contract because the public IDs continue to live on the same node/cluster elements.

### Risks
- Graphviz cluster coloring can be trickier than node coloring; if the implementation colors only the HTML label table and not the cluster boundary/background, empty compounds may still look unowned.
- Existing tests currently assert body-row omission for empty states implicitly through exact DOT fragments; those assertions will need focused updates.
- Any attempt to derive color from authored IDs instead of hierarchy depth would conflict with the requested per-level variation and could make sibling states at the same level visually inconsistent.

### Ready for Proposal
Yes — propose a render-only slice that adds deterministic depth-based state coloring and an always-visible title/body partition, explicitly preserving authored SVG IDs, private anchors, runtime behavior, and workbench contracts.
