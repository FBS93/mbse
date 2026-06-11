## Exploration: graphviz-compound-state-visual-fix

### Current State
Compound states are rendered in `src/mbse/infrastructure/templates/hsm_v1.dot.j2` as a cluster with `label=""` plus a normal boxed node using the same public state id inside that cluster. The rendered SVG therefore shows the parent state as just another child box, while the enclosing cluster has no title. `prepare_hsm_render_view()` currently emits edges directly to/from the public state id, so the template needs that node to exist today.

### Affected Areas
- `src/mbse/infrastructure/templates/hsm_v1.dot.j2` — current compound-state markup causes the visual problem.
- `src/mbse/application/prepare_hsm_render.py` — edge endpoints for compound states are prepared here and would need minimal rerouting if the visible parent box is removed.
- `src/mbse/domain/models.py` — render-view fields may need one small addition for an internal anchor id.
- `tests/unit/mbse/test_hsm_render_view.py` — should assert the new compound-state DOT contract.
- `tests/integration/test_hsm_json_workbench.py` — should protect SVG id stability for compound states after the visual fix.

### Approaches
1. **Label the cluster, keep the parent node box** — set the cluster label from the parent state label/annotation and leave the current boxed parent node inside it.
   - Pros: Tiny template-only change.
   - Cons: The misleading “parent as child” box remains, so it does not fully solve the reported issue.
   - Effort: Low

2. **Promote the parent to the cluster and route edges through an internal anchor** — give the cluster the public state `id` and visual label, replace the inner parent box with a non-public internal anchor node, and have prepared edges target that anchor for compound states.
   - Pros: Fixes both observed problems; preserves public authored ids for highlightability; stays within the existing DOT/Graphviz pipeline.
   - Cons: Slightly broader than template-only because edge endpoints must be rerouted for compound states.
   - Effort: Low

### Recommendation
Choose **Promote the parent to the cluster and route edges through an internal anchor**.

Smallest safe shape:
- in the DOT template, set compound clusters to `id="{{ state.id }}"` and `label="{{ state.label ... }}"` instead of `label=""`;
- stop rendering the parent as a visible boxed child;
- add one internal anchor node (for example `{{ state.id }}__anchor`) inside each compound cluster so transitions and initial edges still have a concrete Graphviz endpoint;
- in render preparation, reroute any edge whose source or target is a compound state from the public state id to that internal anchor id;
- keep `highlightable_ids` unchanged, with the public compound-state id now authored on the cluster itself.

This is the smallest change that actually fixes the mental model instead of merely decorating the broken one.

### Risks
- The authored-id contract must keep exactly one public `id` per compound state; otherwise the prepared-document validator or SVG highlight behavior can drift.
- Cluster-level highlighting may behave slightly differently in the workbench than node-level highlighting, so one integration assertion should confirm the compound-state SVG id still renders.
- If multiline annotations are moved into cluster labels, DOT escaping must stay consistent with the current node-label formatting.

### Ready for Proposal
Yes — the proposal can stay tightly scoped to a render-view plus DOT-template adjustment, with no workbench or Graphviz runner changes.
