# Design: Init Transition Rendering Cleanup

## Technical Approach

Stop treating every helper node the same. `prepare_hsm_render_view()` will model two semantic endpoint classes: visible initial-source markers for root/local initials, and private routing anchors for compound targets. The DOT template will render initial-source markers as visible black points, keep compound anchors invisible, and continue assigning authored public SVG IDs only to states/clusters and edge records.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Public/private ID boundary | Authored IDs remain public only on state nodes, compound clusters, and transition/initial edge `id` attributes; helper IDs stay internal DOT names only | Put public IDs on helper nodes; keep suffix-based implicit behavior | This preserves the exact authored-ID contract and avoids ambiguous duplicate SVG ids. |
| Endpoint semantics model | Extend helper metadata with semantic kind plus render visibility so `root_initial_source` and `local_initial_source` are visible markers, while `compound_anchor` stays private/invisible | One generic helper type with one style rule; separate ad hoc fields per case | The bug came from flattening different semantics into one invisible-helper rule. The model must encode meaning, not just existence. |
| Visibility policy | Render visible initial-source helpers as black `shape=point` nodes without public `id=` attributes; render private target anchors with invisible point styling | Make all helpers invisible; make all helpers visible | Root/local initial sources are part of the authored visual language, but target anchors are only routing scaffolding. |
| Validation guard | Keep leak checks focused on private helper kinds only and continue verifying `highlightable_ids` against authored DOT ids | Ban every helper-like token everywhere | Visible source markers may exist in DOT, but only private anchors must be forbidden from the public/highlightable contract. |

## Data Flow

```text
HsmDocument
  -> prepare_hsm_render_view()
     - flatten public state nodes
     - resolve edge endpoints
     - register semantic endpoints:
         * visible initial-source marker
         * private compound anchor
  -> render_hsm_dot()
     - emit public states/clusters with authored ids
     - emit visible source markers as black points
     - emit private anchors invisibly in correct scope
     - connect edges to resolved endpoint ids
  -> Graphviz SVG
     - authored ids remain exact and unique
     - initial source dots stay visible
     - target anchors do not appear visually
```

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `src/mbse/domain/models.py` | Modify | Extend `HsmRenderRoutingHelper` with explicit semantics/visibility (or equivalent enum-like field) so source markers and private anchors are distinguishable in prepared data. |
| `src/mbse/application/prepare_hsm_render.py` | Modify | Update `_RoutingHelperRegistry` and endpoint routing so root/local initial sources register visible marker helpers, while compound targets register invisible private anchors; keep ordering deterministic. |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modify | Branch helper emission by semantic visibility: visible black points for initial sources, invisible points for compound anchors, both scoped correctly. |
| `src/mbse/domain/validation.py` | Modify | Keep `highlightable_ids` and authored-id extraction strict, but only treat private helper ids as leaks; do not require visible source markers to be public ids. |
| `tests/unit/mbse/test_hsm_render_view.py` | Modify | Assert helper metadata distinguishes visible source markers from private anchors, root/local initial edges start from visible-source helpers, compound targets still route to private anchors, and `highlightable_ids` stay authored-only. |
| `tests/integration/test_hsm_json_workbench.py` | Modify | Update fake-Graphviz visibility contract so visible initial-source markers may render while private anchors may not; add/adjust real-`dot` regression to prove initial source dots remain visible and stray target dots/helper ellipses disappear. |

## Interfaces / Contracts

```python
@dataclass(frozen=True)
class HsmRenderRoutingHelper:
  id: str
  kind: str  # root_initial_source | local_initial_source | compound_anchor
  parent_id: str | None
  owner_id: str | None
  visibility: str  # visible_source | private_anchor
```

Contract rules:
- `highlightable_ids` remain authored state/transition/initial ids only.
- Visible source markers are render-only helpers: they may appear visually, but never as public/authored SVG ids.
- Private compound anchors stay absent from `highlightable_ids`, absent from authored/public IDs, and invisible in final SVG.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Semantic helper registration | Assert helper tuples now encode `visible_source` for root/local initials and `private_anchor` for compound targets, in deterministic order. |
| Unit | DOT emission rules | Assert source-marker helpers render as visible `shape=point` nodes, while compound anchors still render with invisible styling and no public `id=` attribute. |
| Integration | Public ID and visual cleanup | Use fake Graphviz to assert authored ids remain exact/unique and private anchors never surface as SVG ids. |
| Integration | Real Graphviz regression | Run `dot` when available and assert visible black points remain for root/local initial sources, while helper titles, stray destination dots, and helper ellipses at target sites are absent. |

## Migration / Rollout

No migration required. This is a render-only contract correction.

## Open Questions

- [ ] None.
