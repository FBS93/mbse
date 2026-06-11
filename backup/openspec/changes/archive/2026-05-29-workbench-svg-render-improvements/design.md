# Design: Workbench SVG Render Improvements

Short render-pipeline-only change: stop emitting the graph banner, replace flat string state labels with structured title/body label data, and render both leaf and compound states through Graphviz HTML-like table labels while preserving exact public SVG ids.

## Technical Approach

`prepare_hsm_render_view()` becomes the single place that shapes render-only visual data. It will stop producing `variables_block` / `events_block`, and will produce per-state `title_text` plus ordered `body_lines`. `hsm_v1.dot.j2` will consume that structure and emit HTML-like table labels for state nodes and cluster labels. Runtime loading, session building, SVG validation, and web UI stay unchanged.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Remove top banner | Delete `graph [label=...]` usage and stop preparing top-level summary blocks | Hide with CSS/UI, keep banner data but ignore in template | The banner is introduced only by the DOT template, so removal belongs in the render pipeline and avoids any shell/runtime coupling. |
| Clearer state boxes | Replace `annotation_block` string with structured render fields: `title_text`, `body_lines`, `has_children`-compatible label rendering | Keep one flattened string and parse it in Jinja; plain multiline labels | Structured fields keep logic in Python, not fragile template parsing, and support the same title/body contract for leaf and compound states. |
| Exact public IDs | Keep `state.id` as the only public `id` for leaf nodes and compound clusters; keep `__anchor` private for routing only | Prefix cluster ids, expose anchor ids, derive ids from labels | Existing validation and workbench highlighting already depend on exact authored ids. Any alternate public identity breaks the contract. |

## Data Flow

`HSM JSON` -> `prepare_hsm_render_view()` -> `HsmPreparedRenderView.state_nodes[*]` with structured visual fields -> `hsm_v1.dot.j2` -> DOT ids/labels -> Graphviz SVG -> existing exact-id validation.

Compound path stays:

- public cluster id = exact authored compound state id
- private routing endpoint = `{state.id}__anchor`
- `highlightable_ids` continues to list only authored ids and transition ids

## File Changes

| File | Action | Description |
|---|---|---|
| `src/mbse/application/prepare_hsm_render.py` | Modify | Remove `variables_block` / `events_block` population and build structured state visual fields from `label`, `on_entry`, and `on_exit`. Keep depth-first order and anchor routing unchanged. |
| `src/mbse/domain/models.py` | Modify | Replace render-view string fields with render-only title/body fields on `HsmPreparedRenderView` / `HsmRenderStateNode`. No runtime model changes. |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modify | Remove the graph banner and render leaf/compound labels as HTML-like tables. Keep `id="{{ state.id }}"` on public nodes/clusters and keep anchors unlabeled/private. |
| `tests/unit/mbse/test_hsm_render_view.py` | Modify | Update render-view and DOT assertions to lock banner removal, title/body shaping, and unchanged anchor routing/public ids. |
| `tests/integration/test_hsm_json_workbench.py` | Modify | Prove rendered output still exposes exact authored ids once, including compound states, after HTML-label changes. |

## Interfaces / Contracts

Planned render-view shape:

```python
@dataclass(frozen=True)
class HsmRenderStateNode:
  id: str
  title_text: str
  body_lines: tuple[str, ...]
  parent_id: str | None
  child_state_ids: tuple[str, ...]
  initial_connector_id: str | None
```

Contract rules:

- `highlightable_ids` remains authored-state ids + authored-edge ids only.
- Compound states keep public cluster `id == authored state.id` exactly.
- Any `__anchor` id remains internal and MUST NOT become a public highlight target.

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Unit | Render-view structure | Assert no top summary blocks, exact `title_text`/`body_lines`, and unchanged authored `highlightable_ids`. |
| Unit | DOT contract | Assert HTML-table labels are emitted, cluster public ids stay exact, and compound anchors still handle edge routing privately. |
| Integration | SVG/public-id contract | Build a session with fake Graphviz, then assert exact authored ids remain present/unique and `parent__anchor` stays absent from SVG. |

## Migration / Rollout

No migration required.

## Open Questions

- None.
