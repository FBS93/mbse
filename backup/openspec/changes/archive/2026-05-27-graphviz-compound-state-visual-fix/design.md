# Design: Graphviz Compound State Visual Fix

## Technical Approach

Keep the existing `HSM JSON -> prepared render view -> Jinja DOT -> SVG -> workbench` pipeline, but change the compound-state visual contract in one place: the public parent identity moves from the inner node to the enclosing cluster. Edge routing stays valid by using one private internal anchor for compound states only.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Public compound visual | Put `id="{state.id}"` and the visible parent label on the cluster | Keep the current inner parent node; add cluster label only | The fix is visual, so the visible parent must be the container itself. Keeping the inner box preserves the wrong mental model. |
| Internal routing endpoint | Use one private anchor node per compound state: `{state.id}__anchor` | No anchor; reuse child init point; keep edges on public id | Graphviz still needs a concrete node endpoint for transitions and local initials once the visible parent box disappears. |
| Public ID ownership | Keep the authored public ID in `HsmRenderStateNode.id` and `highlightable_ids`; only the DOT template changes where it is emitted | Introduce a second public field or rewrite highlight IDs | The authored ID contract already works. The safe change is to move its SVG owner from node to cluster, not to redefine identity. |
| Parent label/annotation preservation | Reuse the current label composition (`label + optional annotation_block`) on the cluster label | Drop annotations for compound parents; invent a new formatting path | This preserves current text semantics and minimizes drift in escaping/line-break behavior. |

## Data Flow

```text
HsmState.id="parent"
  -> prepare_hsm_render_view()
     - public state id stays "parent"
     - private anchor id becomes "parent__anchor" for compound endpoints only
  -> hsm_v1.dot.j2
     - cluster gets id="parent"
     - anchor node stays internal
  -> SVG/workbench
     - exactly one public SVG id resolves for "parent"
```

Routing rule: if an initial edge or transition source/target references a compound state, prepare that endpoint as `{state.id}__anchor`; flat states remain unchanged.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modify | Emit compound parent label/id on the cluster, remove the visible parent node, add one internal anchor node inside the cluster. |
| `src/mbse/application/prepare_hsm_render.py` | Modify | Reroute compound-state edge endpoints to the private anchor naming convention while keeping `highlightable_ids` on authored public IDs. |
| `src/mbse/domain/models.py` | No change expected | Current render-view shape is enough; the anchor can stay a derived convention, not public model data. |
| `tests/unit/mbse/test_hsm_render_view.py` | Modify | Assert cluster-vs-anchor DOT contract and unchanged public highlightable IDs. |
| `tests/integration/test_hsm_json_workbench.py` | Modify | Assert a compound state still resolves exactly one public SVG id equal to the authored id. |

## Interfaces / Contracts

No public API change.

Private convention introduced during preparation/template rendering:

```text
compound public id: state.id
compound internal anchor: f"{state.id}__anchor"
```

Contract rules:
- `highlightable_ids` MUST keep only authored public IDs.
- Internal anchor IDs MUST NOT be added to `highlightable_ids`.
- Flat-state DOT and edge endpoints MUST remain unchanged.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Compound DOT contract | In `test_hsm_render_view.py`, assert the cluster carries `id="parent"`, the visible inner parent box is absent, the private anchor exists, and compound transition/local-initial endpoints target the anchor. |
| Unit | Public identity stability | In the same test, assert `highlightable_ids` still list `parent`, not `parent__anchor`. |
| Integration | SVG/workbench contract | In `test_hsm_json_workbench.py`, add a compound-state fixture and assert `prepared-document.json` keeps the authored public IDs while `diagram.svg` resolves exactly one `id="parent"`. |

## Migration / Rollout

No migration required.

## Open Questions

- [ ] None blocking. The implementation should verify Graphviz emits the cluster `id` as expected with the current runner/test double.
