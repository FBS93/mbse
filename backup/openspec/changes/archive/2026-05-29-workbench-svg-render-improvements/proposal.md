# Proposal: Workbench SVG Render Improvements

## Intent

Improve Slice C readability by removing duplicated `Variables` / `Events` text from the rendered SVG and by giving states a clearer two-part visual structure, while keeping runtime behavior, viewer-shell behavior, and exact authored SVG ids unchanged.

## Scope

### In Scope
- Remove the top graph-level `Variables` / `Events` summary from SVG output.
- Render state visuals with a clear upper title area and lower entry/exit area for both flat and compound states.
- Preserve the exact authored public SVG ids used by the workbench highlight contract.

### Out of Scope
- Any runtime-semantic change, including event/variable execution behavior.
- Viewer-shell or sidebar UX work beyond the minimum template/render changes needed to support the SVG output.
- Slice A and Slice B work, including layout, controls, or runtime bridge changes.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `hsm-json-graphviz-rendering`: refine the DOT/SVG visual contract so graph-level variable/event summaries are omitted and state labels render as structured title/body compartments without changing authored ids.

## Approach

Keep this slice inside the render pipeline only: `prepare_hsm_render.py` reshapes state visual fields, and `hsm_v1.dot.j2` renders them through Graphviz HTML-like table labels. Compound states continue to expose the exact public cluster id, and any existing internal anchor usage remains private.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/mbse/application/prepare_hsm_render.py` | Modified | Stop feeding top summary blocks and prepare structured state visual fields |
| `src/mbse/domain/models.py` | Modified | Carry render-only title/body state label data |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modified | Remove graph summary label and render partitioned state labels |
| `tests/unit/mbse/test_hsm_render_view.py` | Modified | Lock render-view and DOT contract changes |
| `tests/integration/test_hsm_json_workbench.py` | Modified | Prove SVG ids remain exact and unique after render changes |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| HTML-like labels change SVG structure unexpectedly | Medium | Update focused DOT/SVG assertions only where the render contract changes |
| Compound-state ids drift from the public cluster id contract | Low | Keep exact-id validation in integration coverage |

## Rollback Plan

Revert the render-view and DOT-template changes so the graph returns to the current plain-label output, then rerun unit and integration render/workbench tests.

## Dependencies

- Existing `hsm-json-graphviz-rendering` exact-id and compound-cluster contract.

## Success Criteria

- [ ] The rendered SVG no longer shows the top `Variables` / `Events` summary.
- [ ] Flat and compound states render with title above and entry/exit content below.
- [ ] Runtime behavior and viewer-shell behavior remain unchanged.
- [ ] Public SVG ids remain exact, unique, and highlight-compatible.
