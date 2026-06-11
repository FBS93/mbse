# Proposal: Graphviz Compound State Visual Fix

## Intent

Fix compound-state rendering so the parent state reads as the container title, not as a child box, while keeping the existing JSON -> DOT -> SVG -> workbench runtime and exact authored SVG ids intact.

## Scope

### In Scope
- Move the public compound-state visual from an inner node to the enclosing Graphviz cluster.
- Introduce one internal non-public anchor per compound state so transitions and local initials still have a concrete DOT endpoint.
- Add tests that prove compound-state SVG ids remain exact and unique after the visual adjustment.

### Out of Scope
- Any runtime, validation, workbench, or Graphviz runner behavior change.
- Layout tuning beyond compound-state visuals, including flat states, transitions, or non-compound labels.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `hsm-json-graphviz-rendering`: refine compound-state rendering so the cluster carries the public state id/label and the visible parent box is no longer emitted.

## Approach

Update the DOT template so compound clusters emit the public authored state id and visible label on the cluster itself. Replace the current visible parent node with an internal anchor id used only for Graphviz edge routing. Adjust render preparation only for compound-state endpoints so authored ids stay unchanged in `highlightable_ids` and in the final SVG contract.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modified | Render compound parent as labeled cluster, not visible child node |
| `src/mbse/application/prepare_hsm_render.py` | Modified | Reroute compound-state edge endpoints to internal anchor ids |
| `src/mbse/domain/models.py` | Modified | Carry minimal anchor metadata in render view if needed |
| `tests/unit/mbse/test_hsm_render_view.py` | Modified | Lock DOT/anchor contract for compound states |
| `tests/integration/test_hsm_json_workbench.py` | Modified | Prove exact compound-state SVG ids still resolve once |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Duplicate or missing public SVG ids for compound states | Low | Assert one exact public id per compound state in unit and integration tests |
| Cluster label escaping drifts from current node label formatting | Low | Reuse existing label formatting rules in template assertions |

## Rollback Plan

Revert the template and render-preparation changes so compound states again render through the current visible parent node path, then rerun the existing render and workbench tests.

## Dependencies

- Existing `hsm-json-graphviz-rendering` spec and current Graphviz cluster `id` support.

## Success Criteria

- [ ] Compound states render with the parent title on the cluster and without a misleading visible parent child box.
- [ ] The JSON -> DOT -> SVG -> workbench pipeline behavior is unchanged outside compound-state visuals.
- [ ] Each compound state still exposes exactly one public SVG id equal to the authored state id.
