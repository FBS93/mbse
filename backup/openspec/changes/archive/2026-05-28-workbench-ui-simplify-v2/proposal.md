# Proposal: Workbench UI Simplify v2

## Intent

Deliver a SMALL frontend-only cleanup of the existing workbench so the operator panel is faster to scan and the diagram zoom feels direct. The outcome is a simpler sidebar and wheel-based diagram zoom, with NO backend or runtime-semantic change.

## Scope

### In Scope
- Move `Reset` to the top of the sidebar.
- Remove `Current state` and `Current snapshot` sections.
- Keep `Variables` as a live editable list using existing snapshot + `set_variable` flow.
- Keep `Events` as a dropdown plus `Send` button using the existing event flow.
- Replace button-led zoom interaction with mouse-wheel zoom inside the diagram viewport.

### Out of Scope
- Backend, runtime, API, payload, or state-machine semantic changes.
- New metadata, event parameters, history, timers, persistence, or broader visual redesign.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `graphviz-svg-workbench`: simplify the operator panel contract and change diagram zoom interaction to wheel-based client behavior while preserving the existing runtime bridge.

## Approach

Update only the static viewer assets and the workbench spec delta. Reuse the current session payload, variable mutation contract, event dispatch contract, and client zoom state/clamping logic; only the UI structure and interaction model change.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/specs/graphviz-svg-workbench/spec.md` | Modified | Define simplified panel behavior and wheel zoom |
| `src/mbse/web/static/index.html` | Modified | Remove obsolete sections and move reset control |
| `src/mbse/web/static/viewer.js` | Modified | Keep existing runtime calls, adapt variable/event wiring, bind wheel zoom |
| `src/mbse/web/static/viewer.css` | Modified | Tighten layout after panel simplification |
| `tests/integration/test_mbse_workbench.py` | Modified | Assert frontend-only UX changes without contract drift |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Wheel zoom conflicts with normal scrolling | Med | Scope wheel handling to the diagram viewport and preserve bounded zoom |
| Variable list simplification accidentally changes mutation behavior | Low | Keep exact `set_variable(variable_id, value)` flow and snapshot refresh |

## Rollback Plan

Restore the prior viewer markup and zoom controls, leaving backend/runtime code untouched.

## Dependencies

- Existing `session.json`, `send_event`, `set_variable`, and reset flows.

## Success Criteria

- [ ] The sidebar shows `Reset` first, then `Variables`, `Events`, and status/error feedback only.
- [ ] Variables remain always visible, editable, and live-updated from the existing snapshot/mutation flow.
- [ ] Events remain a dropdown plus `Send` button with no runtime contract change.
- [ ] Users can zoom the diagram with the mouse wheel inside the viewport, without backend interaction changes.
