# Proposal: Render Hierarchy Colors And Empty Actions

## Intent

Deliver a small render-only visual polish slice: every state keeps a visible title/body partition even when entry/exit actions are empty, and states gain soft hierarchy colors derived deterministically from nesting depth.

## Scope

### In Scope
- Always render the lower entry/exit partition for flat and compound states, even when it has no lines.
- Add deterministic, depth-based soft colors for state-owned visuals, including compound states.
- Preserve exact public SVG IDs and private anchor behavior unchanged.

### Out of Scope
- Runtime, validation, or execution changes.
- Workbench shell/UI, highlight behavior, or non-render UX updates.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `hsm-json-graphviz-rendering`: refine render output so hierarchy depth drives visual coloring and empty action partitions remain visible without changing authored SVG IDs.

## Approach

Prepare minimal visual metadata during render-view construction, then keep the Jinja/DOT template thin. Color MUST come from a deterministic algorithm keyed by hierarchy depth, not state IDs or a short hardcoded palette. The template will always emit the same title/body table structure while keeping authored IDs on the same public node/cluster elements.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/mbse/application/prepare_hsm_render.py` | Modified | Add depth-based visual metadata preparation. |
| `src/mbse/domain/models.py` | Modified | Extend render-view state data minimally for visual fields. |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modified | Always render the partition and apply prepared colors. |
| `tests/unit/mbse/test_hsm_render_view.py` | Modified | Lock deterministic colors and always-present partition behavior. |
| `tests/integration/test_hsm_json_workbench.py` | Modified | Reconfirm exact public SVG IDs remain unchanged. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Compound cluster tint looks inconsistent in Graphviz | Med | Verify both label/body and cluster-owned visuals in focused render tests. |
| Visual change accidentally shifts public IDs | Low | Keep IDs on existing public elements and protect with integration assertions. |

## Rollback Plan

Revert render-view visual metadata and template changes, restoring prior state styling while keeping authored-ID tests intact.

## Dependencies

- Existing render pipeline and current Graphviz SVG contract.

## Success Criteria

- [ ] Empty entry/exit sections still render a visible lower partition for flat and compound states.
- [ ] State coloring varies deterministically by hierarchy depth, not by concrete state ID.
- [ ] Exact public SVG IDs remain byte-for-byte unchanged for states, compound states, and transitions.
