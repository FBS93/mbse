# Design: Render Hierarchy Colors And Empty Actions

## Technical Approach

Keep this slice inside render preparation plus the DOT template. Python prepares deterministic visual fields per state from hierarchy depth, and Jinja only renders them. Public authored IDs stay on the same visible leaf node or compound cluster as today; private routing anchors remain unnamed in the public SVG contract.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Depth color algorithm | Fix base RGB at `(220, 232, 242)` / `#DCE8F2`, keep depth `0` as-is, then derive deeper fills by converting the base color to HLS, rotating hue by `-0.60` per depth, increasing lightness by `0.004` per depth up to `0.94`, capping saturation at `0.30`, and converting back to RGB with integer rounding | Channel-wise tint-to-white; hardcoded palette; hash by state id | Deterministic, still rooted in one base color, creates more visible parent/child separation than same-hue tinting, and remains cheap to compute/test. |
| Empty partition rendering | Always emit the body row; when `body_lines` is empty, render one non-breaking-space placeholder | Omit the row; special-case only compound states | Keeps the title/body split visible for every state with one template rule. |
| Color application surface | Prepare color once per `HsmRenderStateNode`; apply it to leaf nodes and compound cluster labels from the same field | Separate color logic in template; color only leaves | Keeps rendering thin and guarantees compound and leaf states follow the same depth contract. |
| Public vs private IDs | Keep `id="{authored_id}"` only on the current public leaf node or cluster; continue routing compound edges through `__anchor`/`__init` names without public `id` attributes | Move public id to anchor; add wrapper ids | Preserves exact SVG IDs and avoids leaking private routing helpers into highlightable/public identity. |

## Data Flow

```text
HsmDocument
  -> prepare_hsm_render_view()
     computes depth, body placeholder contract, fill_rgb from #DCE8F2 via deterministic HLS rotation
  -> render_hsm_dot()
     applies color + always-on body row
  -> Graphviz/SVG
     preserves authored public ids only
```

Depth rule: top-level states are depth `0`; each nested child adds `1`.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `src/mbse/application/prepare_hsm_render.py` | Modify | Thread `depth` through flattening, compute deterministic HLS-derived fill colors from the base RGB, and expose an always-rendered body contract. |
| `src/mbse/domain/models.py` | Modify | Extend `HsmRenderStateNode` with minimal render-only visual fields (`depth`, `fill_rgb`, optional `has_body_content`). |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modify | Always emit the second row, render placeholder when empty, and apply prepared color to leaf/compound visuals. |
| `tests/unit/mbse/test_hsm_render_view.py` | Modify | Lock depth-to-color determinism, empty body behavior, and unchanged anchor/public ID routing. |
| `tests/integration/test_hsm_json_workbench.py` | Modify | Assert rendered DOT/SVG keep exact public ids while compound anchors stay private. |

## Interfaces / Contracts

```python
@dataclass(frozen=True)
class HsmRenderStateNode:
  id: str
  title_text: str
  body_lines: tuple[str, ...]
  parent_id: str | None
  child_state_ids: tuple[str, ...]
  initial_connector_id: str | None
  depth: int
  fill_rgb: str            # example: "#DCE8F2"
  has_body_content: bool
```

Template contract:
- `fill_rgb` is reused for leaf nodes and compound cluster labels.
- Empty bodies render one placeholder line, but `body_lines` stays semantically empty in Python.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Deterministic depth colors | Assert depth 0/1/2 produce stable expected hex values from the base RGB through the HLS derivation and same-depth siblings match. |
| Unit | Visible empty partition | Assert states with no `on_entry`/`on_exit` still render the second table row in DOT for flat and compound states. |
| Integration | Exact ID contract | Re-assert authored public ids are unchanged and private `__anchor` ids never appear as public SVG ids. |

## Migration / Rollout

No migration required. Render-only change; runtime and viewer contracts stay unchanged.

## Open Questions

- [ ] None.
