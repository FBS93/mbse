# Proposal: MBSE 1 Graphical Workbench

## Intent

Deliver a SMALL slice-1 GUI in `src/mbse_1` that renders one diagram to SVG through Graphviz and lets the user inspect that SVG with selective highlight. This creates the reusable SVG boundary needed for future JSON-model adapters without turning the product into a text-diagram editor.

## Scope

### In Scope
- Add a new isolated package in `src/mbse_1`; leave `src/mbse` unchanged.
- Support one controlled loop: load a prepared diagram input, render to SVG via Graphviz, open a local workbench page, and inspect/highlight SVG elements by stable IDs.
- Define the slice-1 artifact/session contract for rendered SVG plus preserved element IDs and basic metadata needed for future bindings.

### Out of Scope
- JSON-model execution adapters, HSM runtime sync, hierarchy semantics, or advanced state-machine UX.
- Text-diagram authoring/editing, generic PlantUML GUI behavior, file watching, multi-document workspaces, or live editing loops.
- Rich overlays, drag/drop, animation, or generalized diagram tooling beyond selective SVG inspection.

## Capabilities

### New Capabilities
- `graphviz-svg-workbench`: Local workbench that renders one bounded input to SVG with preserved IDs and supports read-only SVG inspection/highlight in `src/mbse_1`.

### Modified Capabilities
- None.

## Approach

Use Graphviz as the slice-1 renderer because it best satisfies the confirmed contract: explicit IDs survive into SVG. Build a Python-first local web surface in `src/mbse_1` with minimal JS, focused on SVG display, element selection, and metadata inspection. Keep the renderer boundary external and diagram-type-agnostic so future JSON adapters can produce Graphviz inputs plus stable IDs without coupling the new GUI to HSM internals.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/changes/mbse-1-graphical-workbench/proposal.md` | New | Slice-1 proposal contract |
| `openspec/specs/graphviz-svg-workbench/spec.md` | New | Future source-of-truth spec for the new capability |
| `src/mbse_1/` | New | New isolated package for renderer/workbench boundaries |
| `tests/` | Modified | Slice-1 tests for renderer contract and SVG inspection behavior |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Scope drifts into editor/runtime features | Med | Freeze slice-1 to render + inspect + highlight only |
| Graphviz IDs vary if contract is vague | Med | Specify explicit ID preservation and verify with tests |
| GUI copies old HSM viewer assumptions | Med | Keep all new code in `src/mbse_1` behind new generic contracts |

## Rollback Plan

Remove `src/mbse_1` and the new capability artifacts; no rollback changes are required in `src/mbse` because slice 1 does not modify existing packages.

## Dependencies

- Graphviz available through a supported local execution path for SVG rendering.

## Success Criteria

- [ ] A user can run the slice-1 workbench against one prepared input and see rendered SVG in a local page.
- [ ] SVG element selection/highlight works through preserved stable IDs rather than text heuristics.
- [ ] The new workbench lives entirely under `src/mbse_1` and does not change `src/mbse` behavior.
