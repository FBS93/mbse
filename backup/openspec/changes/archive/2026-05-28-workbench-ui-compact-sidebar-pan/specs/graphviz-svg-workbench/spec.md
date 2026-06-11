# Delta for graphviz-svg-workbench

## MODIFIED Requirements

### Requirement: Persistent Operator Sidebar

The workbench UI MUST keep one sidebar visible beside the SVG pane at normal workbench widths. The sidebar MUST present `Reset` first, followed by `Events`, then `Variables`. The sidebar MUST NOT show `Status`, `Current state`, or `Current snapshot`. Sidebar controls MUST stay compact and expose only the minimum functional information needed to reset, send one event, and edit declared variables. The system MUST keep this as a frontend-only hierarchy and ergonomics simplification and MUST NOT alter runtime semantics.
(Previously: The sidebar order was `Reset`, `Variables`, `Events`, plus status/error feedback.)

#### Scenario: Compact reordered sidebar remains continuously available

- GIVEN the workbench session loads successfully
- WHEN the user inspects the page at a normal workbench width
- THEN the sidebar remains visible while the SVG pane is also visible
- AND only compact `Reset`, `Events`, and `Variables` sections are shown in that order

#### Scenario: Removed status section is not required UI

- GIVEN the workbench renders or refreshes after a runtime action
- WHEN the sidebar contract is evaluated
- THEN no visible `Status` section is required
- AND runtime behavior still uses the existing backend snapshot and mutation flow

### Requirement: Client-Side SVG View Controls

The workbench UI MUST keep mouse-wheel zoom inside the SVG viewport only, and wheel input over the sidebar MUST scroll only the sidebar vertically. The diagram viewport MUST support click-and-drag pan by moving viewport scroll offsets. Zoom and pan behavior MUST operate entirely in client-side view state and MUST NOT change SVG IDs, runtime state, or backend requests beyond the already existing workbench operations.
(Previously: Only wheel zoom inside the SVG viewport was required, with an optional client-side reset view action.)

#### Scenario: Sidebar wheel scroll stays isolated from diagram zoom

- GIVEN sidebar content exceeds the visible sidebar height
- WHEN the user uses the mouse wheel over the sidebar
- THEN only the sidebar scroll position changes vertically
- AND the diagram zoom level does not change

#### Scenario: Diagram wheel zoom stays isolated from sidebar scroll

- GIVEN the diagram is loaded in the workbench
- WHEN the user uses the mouse wheel inside the SVG viewport
- THEN the visible SVG viewport zoom changes accordingly
- AND the sidebar scroll position does not change because of that wheel input

#### Scenario: Drag pans the diagram viewport

- GIVEN the diagram viewport has scrollable overflow at the current zoom
- WHEN the user clicks and drags inside the SVG viewport
- THEN the viewport scroll position updates to pan the diagram
- AND no backend or runtime request is introduced for that interaction

### Requirement: Slice-1 Scope Boundary

This slice MUST remain a thin SVG workbench with minimal backend-owned runtime synchronization. It MAY include only snapshot read, `init/reset`, one event dispatch by `event_id`, one variable update by `variable_id`, backend-driven exact-ID highlight refresh, a persistent compact operator sidebar ordered as `Reset -> Events -> Variables`, independent sidebar scrolling, client-side wheel zoom inside the diagram viewport, and client-side drag-pan through viewport scrolling. It MUST NOT include session persistence, recovery from persisted runtime session files, dependence on `workbench-session.json`, event parameters, event queues, timers, history, async runtime behavior, multi-document workspaces, multi-user support, heuristic element discovery, runtime-semantic expansion, backend contract changes, mobile redesign, new status surfaces, or transform-state/freeform canvas pan.
(Previously: The slice allowed a simplified sidebar ordered `Reset`, `Variables`, `Events`, status/error feedback, and client-side wheel zoom only.)

#### Scenario: Compact navigation update stays frontend-only

- GIVEN a user opens the runtime-enabled workbench successfully
- WHEN they use reset, events, variables, sidebar scroll, wheel zoom, or drag-pan
- THEN behavior stays within existing frontend and runtime bridge contracts
- AND no backend or runtime semantic changes are introduced

#### Scenario: Large UI redesign remains out of scope

- GIVEN future UX ideas beyond this slice
- WHEN a change requires new status surfaces, mobile redesign, or transform-based freeform pan
- THEN that work is outside this delta
- AND it requires a separate spec change
