# Proposal: SVG Activity Text Highlighting

## Intent

Add viewer text highlighting for the latest executed event/activity context without changing runtime semantics or exposing new public SVG IDs.

## Scope

### In Scope
- Add a private render-owned fragment-target contract for lifecycle, transition, and internal-transition text.
- Highlight text for `last_event` event/activity semantics, including `on_initial`, `on_entry`, `on_exit`, transition labels, and internal-transition sections/rows.
- Preserve current active-state and taken-edge shape highlighting.

### Out of Scope
- Runtime semantic changes or new runtime payload fields.
- New authored/public SVG IDs, diagram-definition changes, or heavier font-weight styling.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `graphviz-svg-workbench`: extend the viewer/session contract to consume private render fragment targets for text-safe highlighting while preserving existing shape/edge behavior.
- `hsm-json-graphviz-rendering`: extend prepared render/session metadata with private fragment-target mapping while keeping public authored SVG IDs unchanged.

## Approach

Render will embed private marker hints in Graphviz label output, then normalize rendered SVG into a stable private fragment-target map carried in session/app metadata. The viewer will combine those render targets with existing `last_event` semantics to highlight only the relevant text fragments. Text emphasis will use a thin underline plus subtle warm background/accent, not bolder weight.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/mbse/application/prepare_hsm_render.py` | Modified | Derive semantic-to-fragment marker metadata. |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modified | Emit private marker hints in label markup. |
| `src/mbse/application/build_session.py` | Modified | Normalize SVG hints into viewer-consumable targets. |
| `src/mbse/infrastructure/svg_contract.py` | Modified | Parse/validate private fragment targets. |
| `src/mbse/domain/models.py` | Modified | Carry render-owned fragment-target contract. |
| `src/mbse/web/static/viewer.js`, `viewer.css` | Modified | Apply text-safe fragment highlighting. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Graphviz wrappers are unstable | Med | Normalize marker hints after render into a private contract. |
| Review size nears 400 lines | Med | Keep scope to render/session/viewer text targeting only. |
| Dense labels lose legibility | Low | Avoid font-weight changes; verify with browser coverage. |

## Rollback Plan

Remove fragment-target metadata generation/normalization and viewer text classes, reverting to the existing shape/edge-only highlight behavior.

## Dependencies

- Archived `runtime-last-event-semantics` contract for `last_event`, `executed_activities`, and `transition_path_ids`.

## Success Criteria

- [ ] Public/authored SVG IDs and existing shape/edge highlights remain unchanged.
- [ ] Viewer highlights the correct lifecycle, transition, and internal-transition text fragments from `last_event` semantics.
- [ ] Text emphasis stays legible without heavier font weight.
