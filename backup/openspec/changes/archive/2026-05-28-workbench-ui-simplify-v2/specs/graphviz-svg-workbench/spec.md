# Delta for graphviz-svg-workbench

## ADDED Requirements

### Requirement: Events Use Simple Dispatch Controls

The workbench UI MUST present available events as one dropdown plus one `Send` action using the existing `send_event(event_id)` flow only.

#### Scenario: Event dispatch stays minimal

- GIVEN the session declares available events
- WHEN the user selects one event and activates `Send`
- THEN the UI sends exactly that `event_id` with no new parameters or backend fields

## MODIFIED Requirements

### Requirement: Persistent Operator Sidebar

The workbench UI MUST keep one sidebar visible beside the SVG pane at normal workbench widths. The sidebar MUST present `Reset` first, followed by `Variables`, `Events`, and status/error feedback. The UI MUST NOT show `Current state` or `Current snapshot`. The system MUST keep this as a frontend-only hierarchy simplification and MUST NOT alter runtime semantics.
(Previously: The sidebar required separate current state, variables, runtime actions, and status/error sections.)

#### Scenario: Simplified sidebar remains continuously available

- GIVEN the workbench session loads successfully
- WHEN the user inspects the page at a normal workbench width
- THEN the sidebar remains visible while the SVG pane is also visible
- AND only reset, variables, events, and status/error sections are shown

### Requirement: Variables Stay Visible And Editable

The workbench UI MUST always render every declared `variable_id` as a live editable list entry with its current value from `snapshot.variables`, or an explicit unset state when no current value exists. The UI MUST allow editing each declared variable through the existing `set_variable(variable_id, value)` operation only. Successful and failed edits MUST refresh the visible value and status using the existing snapshot/mutation flow.
(Previously: Variables had to stay visible and editable, but the spec did not require a list-style live editor presentation.)

#### Scenario: Declared variables are always shown

- GIVEN the session declares one or more `variable_ids`
- WHEN the sidebar renders or refreshes from a snapshot
- THEN every declared `variable_id` is visible as an editable list entry
- AND each entry shows its current value or an explicit unset state

#### Scenario: Variable edit uses the existing mutation contract

- GIVEN the user edits one visible variable value
- WHEN the UI submits the change
- THEN the request uses the existing `set_variable(variable_id, value)` flow
- AND the refreshed sidebar reflects the returned snapshot without adding new backend fields

### Requirement: Client-Side SVG View Controls

The workbench UI MUST support mouse-wheel zoom inside the SVG viewport and MAY keep an internal client-side reset-to-default view action. Zoom behavior MUST operate entirely in client-side view state and MUST NOT change SVG IDs, runtime state, or backend requests beyond the already existing workbench operations.
(Previously: The UI had to provide `Zoom in`, `Zoom out`, and `Reset view` controls.)

#### Scenario: Wheel zoom adjusts only the local diagram viewport

- GIVEN the diagram is loaded in the workbench
- WHEN the user uses the mouse wheel inside the SVG viewport
- THEN the visible SVG viewport zoom changes accordingly
- AND runtime semantics and backend contract remain unchanged

### Requirement: Slice-1 Scope Boundary

This slice MUST remain a thin SVG workbench with minimal backend-owned runtime synchronization. It MAY include only snapshot read, `init/reset`, one event dispatch by `event_id`, one variable update by `variable_id`, backend-driven exact-ID highlight refresh, a persistent simplified operator sidebar, live editable variable values, dropdown-based event dispatch, and client-side wheel zoom inside the diagram viewport. It MUST NOT include session persistence, recovery from persisted runtime session files, dependence on `workbench-session.json`, event parameters, event queues, timers, history, async runtime behavior, multi-document workspaces, multi-user support, heuristic element discovery, runtime-semantic expansion, or backend contract changes.
(Previously: The slice allowed a broader sidebar shape with current-state visibility and button-based zoom in/out/reset controls.)

#### Scenario: Simplification remains frontend-only

- GIVEN a user opens the runtime-enabled workbench successfully
- WHEN they use reset, variables, events, or wheel zoom
- THEN the behavior stays within existing frontend and runtime bridge contracts
- AND no backend or runtime semantic changes are introduced
