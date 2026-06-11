# Proposal: Workbench UI Improvements

## Intent

Deliver a SMALL frontend-only UI slice that makes the workbench easier to operate: the sidebar stays visible, current variable values stay visible, variables can be edited in place, and the diagram gains basic zoom controls. This improves day-to-day usability WITHOUT changing runtime semantics or the backend contract.

## Scope

### In Scope
- Keep a persistent sidebar visible alongside the diagram at normal workbench widths.
- Show every declared `variable_id` with its current value or explicit unset state.
- Allow editing variables from that sidebar through the existing `set_variable` operation.
- Improve hierarchy/readability of state, variables, runtime actions, and status/error areas.
- Add client-side `Zoom in`, `Zoom out`, and `Reset view` controls for the SVG pane.

### Out of Scope
- Event parameters, event queues, timers, history, or any runtime-semantic expansion.
- Backend/runtime contract changes, new metadata fields, or visual redesign beyond controlled UI polish.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `graphviz-svg-workbench`: widen the current thin viewer boundary to include persistent UI visibility, sidebar-based variable editing, and client-side SVG zoom while preserving the existing backend/runtime contract.

## Approach

Reuse the current static HTML/CSS/JS viewer and derive the richer UI entirely from existing `variable_ids`, `event_ids`, `snapshot.variables`, and `active_ids`. Keep the backend as-is: variable edits still round-trip through `set_variable`, snapshot reads still drive refresh, and zoom state lives only in the client diagram container.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/specs/graphviz-svg-workbench/spec.md` | Modified | Add the UI slice requirements and preserve contract boundaries |
| `src/mbse/web/static/index.html` | Modified | Persistent sidebar structure and clearer sections |
| `src/mbse/web/static/viewer.css` | Modified | Layout, hierarchy, and scroll/zoom presentation |
| `src/mbse/web/static/viewer.js` | Modified | Variable panel rendering/editing and SVG zoom controls |
| `tests/integration/test_mbse_workbench.py` | Modified | Assert the new frontend behavior without API drift |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Sidebar/zoom CSS introduces cramped or clipped layouts | Med | Keep scope to stable two-pane layout with explicit overflow behavior |
| Variable panel lacks friendly labels | Med | Show stable IDs and values only; defer richer metadata |
| UI scope drifts into runtime semantics | Low | Freeze event params and backend changes out of scope in spec |

## Rollback Plan

Revert the static viewer markup, styles, and client-side controls to the current thin viewer while leaving backend/runtime endpoints unchanged.

## Dependencies

- Existing runtime session payload and current `set_variable` / snapshot endpoints.

## Success Criteria

- [ ] The workbench shows a persistent sidebar with clearly separated state, variables, actions, and status sections.
- [ ] Every declared variable is always visible with its latest value and can be edited through the existing runtime mutation flow.
- [ ] The diagram pane supports zoom in, zoom out, and reset view without any backend/runtime contract change.
