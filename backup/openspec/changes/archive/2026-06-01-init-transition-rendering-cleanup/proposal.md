# Proposal: Init Transition Rendering Cleanup

## Intent

Clean up init-transition rendering so private routing helpers stay internal, real Graphviz output has no stray helper visuals, and authored SVG IDs remain exact, unique, and unambiguous.

## Scope

### In Scope
- Formalize a private routing layer for root init sources, local init sources, and compound target anchors in the prepared render model.
- Render private routing helpers invisibly so Graphviz can route edges without exposing phantom ellipses or the remaining stray destination point on the initial transition target.
- Strengthen render validation/tests around exact public IDs, helper privacy, and real-SVG visual cleanliness.

### Out of Scope
- Runtime semantics, workbench UX, or highlight behavior changes.
- New Graphviz layout features beyond fixing init/helper routing cleanup.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `hsm-json-graphviz-rendering`: make private routing helpers explicit, preserve exact public IDs, and require visually clean init/compound routing output.

## Approach

Adopt the explored explicit private-routing model: separate public renderables from private helper nodes in prepared render data, create helpers only on demand, and update DOT emission so helper nodes participate in routing but do not render as visible points/ellipses. Keep the current authored-ID contract unchanged and prove the cleanup with at least one real-Graphviz regression.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/mbse/domain/models.py` | Modified | Add explicit private-routing helper representation. |
| `src/mbse/application/prepare_hsm_render.py` | Modified | Centralize helper creation and edge endpoint routing. |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modified | Emit invisible helper routing nodes only when needed. |
| `src/mbse/domain/validation.py` | Modified | Protect exact public/highlightable ID contract. |
| `tests/unit/mbse/test_hsm_render_view.py` | Modified | Cover public-vs-private render model behavior. |
| `tests/integration/test_hsm_json_workbench.py` | Modified | Assert real SVG has no stray init destination point/helper visuals. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Invisible helpers alter Graphviz layout unexpectedly | Med | Keep helpers on-demand and add real-Graphviz regression coverage. |
| Refactor leaks private IDs into public contract | Low | Validate highlightable/public IDs against authored IDs only. |

## Rollback Plan

Revert the prepared-render model/template cleanup and restore current helper emission, keeping the already-fixed compound init endpoint routing if rollback is partial.

## Dependencies

- Graphviz `dot` availability for one real-SVG regression.

## Success Criteria

- [ ] Initial-transition rendering shows no stray destination point or helper ellipse in real SVG output.
- [ ] Public/highlightable SVG IDs remain authored, exact, unique, and unambiguous.
- [ ] Compound/init routing remains correct for root and local initials targeting compound states.
