# Delta for graphviz-svg-workbench

## ADDED Requirements

### Requirement: Persistent Operator Sidebar

The workbench UI MUST keep one sidebar visible beside the SVG pane at normal workbench widths. The sidebar MUST present separate sections for current state, variables, runtime actions, and status/error feedback. The system MUST keep this as a minimal hierarchy improvement only and MUST NOT alter runtime semantics.

#### Scenario: Sidebar remains continuously available

- GIVEN the workbench session loads successfully
- WHEN the user inspects the page at a normal workbench width
- THEN the sidebar remains visible while the SVG pane is also visible
- AND state, variables, actions, and status appear as distinct sections

### Requirement: Variables Stay Visible And Editable

The workbench UI MUST always render every declared `variable_id` together with its current value from `snapshot.variables`, or an explicit unset state when no current value exists. The UI MUST allow editing each declared variable through the existing `set_variable` operation only. Successful and failed edits MUST refresh the visible value and status using the existing snapshot/mutation flow.

#### Scenario: Declared variables are always shown

- GIVEN the session declares one or more `variable_ids`
- WHEN the sidebar renders or refreshes from a snapshot
- THEN every declared `variable_id` is visible
- AND each entry shows its current value or an explicit unset state

#### Scenario: Variable edit uses the existing mutation contract

- GIVEN the user edits one visible variable value
- WHEN the UI submits the change
- THEN the request uses the existing `set_variable(variable_id, value)` flow
- AND the refreshed sidebar reflects the returned snapshot without adding new backend fields

### Requirement: Client-Side SVG View Controls

The workbench UI MUST provide `Zoom in`, `Zoom out`, and `Reset view` controls for the SVG pane. These controls MUST operate entirely in client-side view state and MUST NOT change SVG IDs, runtime state, or backend requests beyond the already existing workbench operations.

#### Scenario: View controls adjust only the local diagram viewport

- GIVEN the diagram is loaded in the workbench
- WHEN the user activates zoom or reset controls
- THEN the visible SVG viewport changes accordingly
- AND runtime semantics and backend contract remain unchanged

## MODIFIED Requirements

### Requirement: Slice-1 Scope Boundary

This slice MUST remain a thin SVG workbench with minimal backend-owned runtime synchronization. It MAY include only snapshot read, `init/reset`, one event dispatch by `event_id`, one variable update by `variable_id`, backend-driven exact-ID highlight refresh, a persistent operator sidebar, always-visible current variable values, minimal visual hierarchy improvements inside the existing workbench layout, and client-side SVG zoom in/out/reset controls. It MUST NOT include session persistence, recovery from persisted runtime session files, dependence on `workbench-session.json`, event parameters, event queues, timers, history, async runtime behavior, multi-document workspaces, multi-user support, heuristic element discovery, runtime-semantic expansion, or backend contract changes.
(Previously: visual enhancements were excluded; this change allows a narrow UI-only usability slice without changing semantics or contracts.)

#### Scenario: Deferred runtime features stay out of this slice

- GIVEN a user opens the runtime-enabled workbench successfully
- WHEN they inspect the available actions
- THEN only the minimal runtime bridge operations and UI-only visibility controls are available
- AND richer runtime semantics or backend contract expansions are absent

#### Scenario: Event parameters remain out of scope

- GIVEN the workbench exposes event dispatch actions
- WHEN the user triggers an event from this slice
- THEN the UI does not request event parameters
- AND event dispatch still uses exactly one `event_id`
