## Exploration: hsm-json-graphviz-rendering

### Current State
`src/mbse` already implements the downstream half of the pipeline: it accepts one prepared Graphviz document (`document_id`, `dot_source`, `highlightable_ids`), renders SVG with Graphviz, validates exact SVG IDs, writes `diagram.svg` plus `workbench-session.json`, and serves a read-only workbench. The active spec in `openspec/specs/graphviz-svg-workbench/spec.md` intentionally stops at the prepared-Graphviz boundary and treats exact SVG IDs as the only visual contract.

That means slice 2 does NOT need a new viewer or runtime. The smallest safe addition is an upstream adapter that takes product-owned HSM JSON, validates it, emits deterministic DOT, derives the exact `highlightable_ids`, and then hands the existing prepared-document/workbench flow the same contract it already understands.

### Affected Areas
- `src/mbse/domain/models.py` — current prepared-document contract is the target output boundary for the new JSON-to-DOT adapter.
- `src/mbse/domain/validation.py` — shows current validation is Graphviz-document oriented; slice 2 needs separate HSM-JSON validation before DOT emission.
- `src/mbse/application/build_session.py` — existing orchestration can likely be reused after producing the same prepared Graphviz document shape.
- `src/mbse/infrastructure/graphviz_runner.py` — remains the renderer boundary; no new rendering backend is needed.
- `src/mbse/infrastructure/session_store.py` — persists the already-correct workbench artifacts; should stay downstream of the new adapter.
- `src/mbse/web/server.py` — proves the workbench only depends on `diagram.svg` and `workbench-session.json`, so reuse is straightforward.
- `openspec/specs/graphviz-svg-workbench/spec.md` — current source of truth for the downstream SVG/workbench contract that slice 2 must preserve.
- `prepared-document.json` — concrete example of the exact contract the new slice should continue producing.

### Approaches
1. **Direct HSM JSON -> Jinja2 DOT -> existing prepared-document contract** — validate the JSON shape, compute stable IDs, render DOT through one Jinja2 template, then feed the result into the current workbench pipeline.
   - Pros: Smallest change set; keeps JSON as source of truth; reuses current Graphviz/SVG/workbench path unchanged; easy to verify with fixture-driven tests.
   - Cons: Template can become messy if hierarchy lowering rules grow; needs a disciplined JSON schema and ID convention up front.
   - Effort: Low

2. **Normalized Python HSM model -> compiler -> DOT** — first map JSON into a richer in-memory model, then compile DOT from that model.
   - Pros: Better if hierarchy semantics, reuse, or multiple render targets expand soon.
   - Cons: More abstraction than the current goal needs; higher risk of inventing architecture before proving the simple path.
   - Effort: Medium

3. **Direct Python string builder without templates** — build DOT procedurally from JSON.
   - Pros: No new dependency.
   - Cons: Harder to read, review, and keep visually consistent; pushes formatting concerns into Python logic.
   - Effort: Low/Medium

### Recommendation
Choose **Direct HSM JSON -> Jinja2 DOT -> existing prepared-document contract**.

For this slice, the right move is the SMALLEST adapter, not a compiler framework. Add a product-owned HSM JSON document and schema, keep validation focused on structure plus deterministic ID rules, and render DOT from one controlled Jinja2 template. The adapter should output the same `PreparedGraphvizDocument` shape the repo already uses today, so `build_workbench_session()` and the read-only workbench remain effectively unchanged.

Recommended boundary for proposal/spec:
- input: one HSM JSON file with hierarchy, transitions, and optional labels/metadata;
- validation: JSON schema + a thin semantic pass for duplicate names, missing targets, and unsupported hierarchy cases;
- rendering: one Jinja2 DOT template plus minimal Python preprocessing only for values the template should not infer repeatedly (for example stable node/edge IDs and flattened iteration order);
- output: `document_id`, generated `dot_source`, and generated `highlightable_ids` for the existing slice-1 session builder;
- out of scope: runtime execution, sync, editing, bidirectional parsing, or a generalized HSM compiler layer.

### Risks
- Jinja2 is not currently declared in project dependencies, so the change must introduce it deliberately and keep its use narrow.
- If the JSON format leaves IDs or naming ambiguous, the SVG-ID contract will become unstable and break reproducible highlighting.
- Hierarchical states can tempt complex template logic; if flattening/ordering rules are not defined early, the “simple template” can rot fast.
- The current DOT authored-ID check is regex-based; slice 2 should avoid leaning on fragile DOT parsing assumptions beyond the controlled emitted template.

### Ready for Proposal
Yes — propose `hsm-json-graphviz-rendering` as an upstream adapter slice that defines one custom HSM JSON format, validates it, renders deterministic DOT via Jinja2, and reuses the existing Graphviz SVG workbench contract without introducing runtime behavior yet.
