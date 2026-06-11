# Design: SVG Activity Text Highlighting

## Technical Approach

Keep runtime semantics unchanged and make render own text targeting. DOT emission will add private marker tokens around authored lifecycle, transition, and internal-transition text fragments. After Graphviz renders SVG, a normalization pass will strip those tokens, split the affected `<text>/<tspan>` content into exact private fragment IDs, and return a viewer-only target map. The bridge will expose that static target map beside the existing `last_event` snapshot so the viewer can combine semantic refs with exact fragment IDs without scraping arbitrary label text.

## Architecture Decisions

| Decision | Options | Choice | Rationale |
|---|---|---|---|
| Fragment ownership | Viewer guesses text nodes; diagram definition carries IDs; render emits private markers | Render emits private semantic markers and normalizes them post-render | Preserves layer boundaries and avoids heuristic DOM lookup. |
| Private target shape | One flat string-key map; nested typed maps; public SVG IDs | Nested typed maps keyed by semantic origin, resolved to private fragment IDs | Keeps bridge/viewer mapping explicit for `transition_path_ids`, lifecycle slots, and internal rows. |
| Unstable wrapper handling | Retarget nearest text; synthesize fallback public IDs; omit unmappable targets | Omit only the unstable target | Safer than highlighting the wrong row/text and keeps public IDs unchanged. |
| Text emphasis | Heavier font; injected background rects; underline + subtle accent | Underline + subtle accent class on exact text fragments | Preserves legibility in dense Graphviz labels. |

## Data Flow

```text
prepare_hsm_render_view
  -> build semantic marker plan for lifecycle / transition / internal text
  -> template emits marker-delimited label text
  -> Graphviz renders normal SVG
  -> svg_contract normalizes marker-delimited text into private fragment IDs
  -> WorkbenchAppState stores fragment target map
  -> Runtime bridge copies static map into session JSON
  -> viewer resolves last_event semantics to exact fragment IDs and applies text class
```

Mapping rules:
- `last_event.transition_path_ids` -> transition label targets for each taken transition ID.
- `last_event.executed_activities` with `owner_kind in {state_on_initial,state_on_entry,state_on_exit}` -> matching lifecycle activity targets, plus the owning section label (`on_initial:`, `on_entry:`, `on_exit:`).
- `owner_kind == "transition"` -> matching transition activity targets.
- `handler_kind == "internal_transition"` + `handler_id` -> `internal_transitions:` section target and only that row's event/activity targets; no external edge text is highlighted.

## File Changes

| File | Action | Description |
|---|---|---|
| `src/mbse/domain/models.py` | Modify | Add private text-target DTOs on render/app/viewer models. |
| `src/mbse/application/prepare_hsm_render.py` | Modify | Build semantic marker refs for lifecycle sections, transition labels/activities, and internal-transition rows. |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modify | Emit marker-delimited label fragments without changing public authored IDs. |
| `src/mbse/infrastructure/svg_contract.py` | Modify | Normalize marker-delimited SVG text, mint reserved private fragment IDs, strip markers, and omit ambiguous targets. |
| `src/mbse/application/build_session.py` | Modify | Run normalization after Graphviz render and store fragment targets in `WorkbenchAppState`. |
| `src/mbse/application/web_runtime_bridge.py` | Modify | Expose static fragment targets in session JSON while preserving current active/edge behavior. |
| `src/mbse/web/static/viewer.js` / `viewer.css` | Modify | Resolve semantic refs to exact fragment IDs and apply text-safe emphasis. |
| `tests/unit/mbse/test_svg_contract.py` | Modify | Cover marker normalization, ID minting, and omission-on-ambiguity. |
| `tests/unit/mbse/test_hsm_render_view.py` | Modify | Lock render marker generation for lifecycle/transition/internal rows. |
| `tests/unit/mbse/test_web_runtime_bridge.py` | Modify | Lock session contract shape for private text targets. |
| `tests/integration/test_hsm_json_workbench.py` / `test_mbse_session_build.py` / `test_mbse_workbench.py` | Modify | Cover end-to-end targeting, internal-transition-only text highlighting, and preserved shape/edge highlights. |

## Interfaces / Contracts

```python
@dataclass(frozen=True)
class RuntimeViewerTextTargets:
  lifecycle_section_ids: dict[str, dict[str, tuple[str, ...]]]
  lifecycle_activity_ids: dict[str, dict[str, dict[str, tuple[str, ...]]]]
  transition_label_ids: dict[str, tuple[str, ...]]
  transition_activity_ids: dict[str, dict[str, tuple[str, ...]]]
  internal_transition_section_ids: dict[str, tuple[str, ...]]
  internal_transition_event_ids: dict[str, tuple[str, ...]]
  internal_transition_activity_ids: dict[str, dict[str, tuple[str, ...]]]
```

All private fragment IDs use a reserved prefix (for example `__mbse_text_fragment__...`), MUST stay out of `highlightable_ids`, and are valid only for the rendered SVG instance created in that session.

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Unit | Marker plan generation | Assert lifecycle, transition, and row-scoped internal refs are emitted in authored order. |
| Unit | SVG normalization | Feed marker-bearing SVG text, assert markers are stripped, private IDs are minted deterministically, and ambiguous/missing fragments are omitted. |
| Integration | Session build | Assert public IDs remain exact, shape/edge targets remain unchanged, and app/session metadata carries only private text targets. |
| Integration | Viewer behavior | Assert transition label highlighting, lifecycle section+activity highlighting, and internal-transition-only row highlighting while unrelated text stays neutral. |

## Migration / Rollout

No migration required. Review budget risk is **Medium** because the slice spans render, normalization, viewer, and tests; keep the contract minimal and avoid expanding generic prepared-document semantics.

## Open Questions

- [ ] None blocking; if real Graphviz collapses specific markers unpredictably, omit that target and lock the unsupported shape in tests.
