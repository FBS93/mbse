# Proposal: SVG Render Activity Parity

## Intent

Close the gap between the executable HSM model and authored SVG text so reviewers can see lifecycle hooks, internal transitions, guards, and activities directly in render output without changing runtime or public SVG contracts.

## Scope

### In Scope
- Render state-body sections for `on_initial`, `on_entry`, and `on_exit` in authored order.
- Render `internal_transitions:` inside each owning state's body using compact `event/activity` lines.
- Render normal transition labels with guard and activity text using `event [guard]/activity` formatting.
- Render initial-transition activities on initial edges as compact activity-only labels.
- Keep changes inside render DTO shaping, DOT templating, and render-focused tests.

### Out of Scope
- Runtime/viewer activity highlighting; that is the planned next iteration.
- New public per-activity SVG IDs or highlight targets.
- API, bridge, validation, or runtime-semantics changes.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `hsm-json-graphviz-rendering`: extend prepared render and SVG text parity for executable activity metadata while preserving exact public SVG IDs.

## Approach

Adopt a small internal render-DTO expansion instead of piling more ad-hoc strings onto `body_lines` and edge `label`. Keep the public SVG contract unchanged, but shape state-body sections and edge-label parts explicitly before DOT rendering. Use exact section header `internal_transitions:`. Preserve authored order. Initial-edge activities render as `/activity` text; if multiple activities exist, join them deterministically in authored order.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/mbse/domain/models.py` | Modified | Add structured render-view fields for state sections and initial-edge labels. |
| `src/mbse/application/prepare_hsm_render.py` | Modified | Map executable model data into parity-focused render sections and edge labels. |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modified | Render richer state bodies and initial/normal edge labels cleanly. |
| `tests/unit/mbse/test_hsm_render_view.py` | Modified | Lock ordering and text formatting for hooks, guards, and activities. |
| `tests/integration/test_hsm_json_workbench.py` | Modified | Prove rendered output gains parity text without changing public IDs. |
| `openspec/specs/hsm-json-graphviz-rendering/spec.md` | Modified | Add normative render-parity requirements and scope boundary. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Label density hurts readability | Medium | Keep formatting compact and deterministic; avoid highlight scaffolding now. |
| Guard/activity notation becomes ambiguous | Medium | Lock one format in spec: `event [guard]/activity`. |
| Scope creeps into highlighting | Medium | Reject new public IDs and viewer/runtime work in this slice. |

## Rollback Plan

Revert render-preparation, DOT template, and render-test changes for this change set, restoring prior `on_entry`/`on_exit`-only output and existing public SVG IDs.

## Dependencies

- Existing exploration artifact at `openspec/changes/svg-render-activity-parity/exploration.md`.

## Success Criteria

- [ ] SVG/DOT output shows `on_initial`, `on_entry`, `on_exit`, `internal_transitions:`, guards, and authored activities for supported edges.
- [ ] Public `highlightable_ids` and authored SVG IDs remain unchanged except for added visible text.
- [ ] No runtime, viewer-highlighting, or API behavior changes are introduced.
