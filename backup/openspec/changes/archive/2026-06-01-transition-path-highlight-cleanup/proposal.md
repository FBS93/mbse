# Proposal: Transition Path Highlight Cleanup

## Intent

Make the runtime/viewer highlight contract reflect the full latest resolution path instead of only the final edge. This is a deliberate breaking change: `last_transition_id` stops being `str | null` and becomes `tuple[str, ...]` / JSON array with no compatibility layer.

## Scope

### In Scope
- Redefine `last_transition_id` as the ordered IDs executed during the latest `init` or `send_event` resolution, including nested initials.
- Update runtime, bridge, viewer, and tests end-to-end to use the new tuple/array contract with no fallback behavior.
- Change active-state styling to border-only emphasis while keeping transition highlight on edge/arrowhead only.

### Out of Scope
- New snapshot attributes such as `transition_highlight_ids`.
- Backward compatibility adapters, dual-format payloads, or unrelated workbench UX changes.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `generated-hsm-engine`: snapshot/runtime inspection contract now reports the full ordered latest-resolution transition path instead of only the final transition.
- `graphviz-svg-workbench`: viewer/runtime bridge contract now consumes `last_transition_id` as multiple exact SVG IDs, and active-state highlight becomes contour-only.

## Approach

Build the tuple in the runtime as the single source of truth: `init()` and taken event transitions collect the explicit transition plus any nested initials that finish the resolution; `set_state()` and empty snapshots return `()`. The backend filters that tuple member-by-member against `highlightable_ids`, and the frontend highlights each returned transition ID while removing active-state fill intensification.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/mbse/application/hsm_runtime.py` | Modified | Build ordered transition tuples per resolution |
| `src/mbse/domain/models.py` | Modified | Change snapshot type from scalar/optional to tuple |
| `src/mbse/application/web_runtime_bridge.py` | Modified | Filter and serialize multiple transition IDs |
| `src/mbse/web/static/viewer.js` | Modified | Apply transition highlight to each returned ID |
| `src/mbse/web/static/viewer.css` | Modified | Remove active-state fill intensification |
| `tests/unit/**`, `tests/integration/**` | Modified | Update contract assertions end-to-end |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Missed scalar assumption breaks viewer/tests | Med | Update all known consumers in one iteration and verify integration coverage |
| Missing SVG IDs in a returned path create partial highlights | Low | Keep per-ID backend filtering and lock behavior in tests |

## Rollback Plan

Revert the proposal and implementation together, restoring scalar `last_transition_id` semantics and the prior active-state fill styling.

## Dependencies

- Existing `generated-hsm-engine` and `graphviz-svg-workbench` specs must be updated in the next phase.

## Success Criteria

- [ ] Specs explicitly state that `last_transition_id` is an ordered tuple/JSON array for the latest resolution and that this is a breaking contract change.
- [ ] Runtime, bridge, viewer, and tests work end-to-end with no scalar compatibility path.
- [ ] Active states render with border-only emphasis, while executed transitions in the latest resolution can all highlight together.
