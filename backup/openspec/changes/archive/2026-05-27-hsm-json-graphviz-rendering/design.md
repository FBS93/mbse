# Design: HSM JSON Graphviz Rendering

## Technical Approach

Keep one narrow adapter inside `src/mbse`: validate one HSM JSON v1 document, prepare one deterministic render view, render DOT through one Jinja2 template, then hand the existing `PreparedGraphvizDocument` flow to Graphviz/SVG/workbench unchanged. The JSON document remains the source of truth; preparation is limited to validation, flattening authored order, and packaging values the template should not recompute.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Canonical JSON shape | Flat root with global `variables`, `events`, `states`, `transitions`, plus optional root/state `initial` objects | Nested runtime model; per-state local transition arrays | Matches the spec directly, keeps cross-references simple, and avoids inventing runtime semantics. |
| Identity contract | Authored IDs are global, immutable, and reused as Graphviz `id` values for highlightable state/transition elements | Path-derived IDs; generated SVG IDs | The workbench already depends on exact SVG IDs, so rewritten IDs would break determinism. |
| Template boundary | Jinja2 receives a prepared render view with ordered `state_nodes`, `initial_edges`, `transition_edges`, and display strings | Raw JSON direct to template; richer compiler layer | Raw JSON would push traversal/lookup logic into Jinja2; a compiler would overreach this slice. |
| Scope boundary | Render-only metadata for `events`, parameters, variables, `on_entry`, `on_exit`, initials | Runtime execution, guards, action semantics | Keeps v1 understandable and aligned with the corrected spec. |

## Data Flow

```text
hsm.json
  -> domain.load_hsm_document()
  -> domain.validate_hsm_document()
  -> application.prepare_hsm_render_view()
  -> infrastructure.dot_template.render(view)
  -> PreparedGraphvizDocument(document_id, dot_source, highlightable_ids)
  -> existing build_workbench_session() flow
```

Deterministic traversal rule: top-level `states` in authored order, then recursive depth-first children in authored order. Root `initial`, then each compound state's `initial`, then root `transitions`, all in authored order.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `src/mbse/domain/models.py` | Modify | Add HSM v1 document/value types plus a prepared render-view type. |
| `src/mbse/domain/validation.py` | Modify | Add HSM schema/semantic validation for IDs, references, hierarchy, and unsupported constructs. |
| `src/mbse/application/build_session.py` | Modify | Accept HSM JSON input via a new preparation path that still produces `PreparedGraphvizDocument`. |
| `src/mbse/application/prepare_hsm_render.py` | Create | Build the deterministic render view and `highlightable_ids`. |
| `src/mbse/infrastructure/dot_template.py` | Create | Jinja2 environment plus DOT rendering entry point. |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Create | Single deterministic DOT template. |
| `pyproject.toml` | Modify | Add narrow Jinja2 dependency/config if the repo chooses to declare runtime deps here. |
| `tests/unit/mbse/test_hsm_validation.py` | Create | Schema and semantic validation coverage. |
| `tests/unit/mbse/test_hsm_render_view.py` | Create | Deterministic ordering and highlightable ID coverage. |
| `tests/integration/test_hsm_json_workbench.py` | Create | HSM JSON -> DOT -> SVG -> workbench contract coverage. |

## Interfaces / Contracts

```json
{
  "schema_version": "hsm-v1",
  "document_id": "door_machine",
  "variables": [{"id": "count", "label": "count"}],
  "events": [
    {"id": "open_evt", "parameters": [{"name": "source"}]}
  ],
  "states": [
    {
      "id": "closed",
      "label": "Closed",
      "on_entry": ["count = count + 1"],
      "on_exit": [],
      "states": [],
      "initial": null
    }
  ],
  "initial": {"id": "machine_init", "target_id": "closed"},
  "transitions": [
    {
      "id": "closed_to_open",
      "source_id": "closed",
      "target_id": "open",
      "event_id": "open_evt"
    }
  ]
}
```

Preparation rules:
- Pass through unchanged: `document_id`, all authored IDs, labels/snippets, variable/event/parameter order, transition order.
- Prepare once in Python: flattened ordered state list; parent/child relationships; initial-edge list; resolved transition endpoints; display strings such as `open_evt(source)` and state annotation blocks for variables/`on_entry`/`on_exit`.
- `highlightable_ids` contains only state IDs and transition/initial IDs, in render order.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | HSM validation | Reject duplicate IDs, bad references, invalid local initials, unsupported fields, and non-deterministic identity patterns. |
| Unit | Render preparation | Assert exact traversal order, stable display-string assembly, and stable `highlightable_ids`. |
| Integration | Full pipeline | Render the same HSM JSON twice and assert identical `dot_source`, identical `highlightable_ids`, and surviving SVG IDs. |

## Migration / Rollout

No migration required. This slice adds an upstream input path while preserving the current prepared-document and workbench contracts.

## Open Questions

- [ ] Whether variable objects should allow only `id` in v1 or also optional display-only fields such as `label`/`initial_value`; implementation should stay at the minimum the spec finally blesses.
