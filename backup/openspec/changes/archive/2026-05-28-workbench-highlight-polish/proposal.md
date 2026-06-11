# Proposal: Workbench Highlight Polish Slice B

## Intent

Improve workbench highlight readability without changing SVG structure or broad runtime semantics: make the active-state highlight calmer, show the transition that led to the current state, and avoid dual parent+child highlighting by treating only the active leaf as highlighted.

## Scope

### In Scope
- Soften the visual treatment of the active state highlight.
- Add a distinct visual treatment for the exact transition that most recently led to the current leaf state.
- Narrow backend/view-model output so `active_ids` is leaf-only and snapshot data MAY include one optional `last_transition_id`.
- Preserve exact SVG-ID targeting as the only highlight contract.

### Out of Scope
- Any internal SVG render/DOM structure work (Slice C).
- Broad runtime semantic changes, transition history, or multi-step execution modeling.
- Any change that relaxes or renames exact SVG IDs.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `graphviz-svg-workbench`: refine highlight behavior so the viewer applies lighter state styling, highlights one optional last transition by exact SVG ID, and limits active state highlighting to the current leaf.

## Approach

Keep the current backend-owned highlight model. Update the snapshot contract minimally: `active_path` stays unchanged for observability, `active_ids` becomes the single active leaf ID list, and `last_transition_id` becomes an optional exact SVG ID. The frontend keeps exact-ID lookup, splits state-vs-transition CSS classes, and does not infer targets from labels or SVG text.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/specs/graphviz-svg-workbench/spec.md` | Modified | Add Slice B highlight UX and boundary requirements |
| `src/mbse/application/web_runtime_bridge.py` | Modified | Emit leaf-only `active_ids` and optional `last_transition_id` |
| `src/mbse/domain/models.py` | Modified | Extend viewer snapshot shape minimally |
| `src/mbse/web/static/viewer.js` | Modified | Apply separate state/transition highlight classes |
| `src/mbse/web/static/viewer.css` | Modified | Tone down active styling and add transition styling |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Initial nested entry chooses the wrong transition to highlight | Med | Specify `last_transition_id` as the final transition into the current leaf |
| Existing tests assume broader `active_ids` semantics | Med | Update spec/tests together around leaf-only behavior |

## Rollback Plan

Revert the Slice B spec and the small snapshot/frontend highlight delta; no SVG migration or runtime data migration is required.

## Dependencies

- Existing `graphviz-svg-workbench` capability.
- `openspec/changes/workbench-highlight-polish/exploration.md`.

## Success Criteria

- [ ] The spec defines a calmer active-state highlight outcome.
- [ ] The spec requires highlighting the exact last transition into the active leaf state.
- [ ] The spec limits active state highlighting to the leaf state only.
- [ ] Slice B stays out of SVG structural work and deep runtime changes.
