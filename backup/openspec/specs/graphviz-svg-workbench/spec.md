# graphviz-svg-workbench Specification

## Purpose

Define slice 1 as a local SVG workbench in `src/mbse` for inspecting one Graphviz-rendered diagram with backend-owned runtime synchronization and exact SVG ID highlighting.

## Requirements

### Requirement: Compact Restyle Stays Presentation-Only

The visual restyle MUST remain frontend-only and MUST NOT change runtime semantics, backend contracts, or action outcomes.

#### Scenario: Cosmetic changes do not alter runtime behavior

- GIVEN the compact restyle is present
- WHEN the operator uses existing sidebar actions
- THEN the same runtime and backend behaviors still occur

### Requirement: Slice-1 Session Artifacts

The system MUST create one bounded workbench session from one prepared Graphviz input. The workbench MUST expose `diagram.svg` for rendering, and it MAY expose read-only artifact metadata for static loading. For the runtime bridge slice, the viewer-facing runtime snapshot and the metadata needed to drive minimal event/variable controls MUST come from the live Python process in memory. The system MUST NOT require `workbench-session.json` or any persisted session-state artifact as the runtime source of truth.

#### Scenario: Session opens from bounded artifacts plus live runtime metadata

- GIVEN one prepared input was rendered successfully
- WHEN the workbench session is created
- THEN the frontend can load `diagram.svg`
- AND runtime snapshot data is served from the live backend process

### Requirement: SVG IDs Are The Only Visual Source Of Truth

The system MUST treat the exact SVG `id` attributes preserved by Graphviz as the only visual identity contract for highlightable elements. Declared highlightable IDs and returned `active_ids` MUST contain only IDs that exist in `diagram.svg`, and the system MUST NOT derive highlight targets from visible text, labels, titles, or heuristic SVG text parsing.

#### Scenario: Exact Graphviz IDs drive inspection

- GIVEN the runtime session declares `state_idle`
- WHEN the frontend resolves that ID in the loaded SVG
- THEN it targets the DOM element whose `id` is exactly `state_idle`

#### Scenario: Visible text is not a selector

- GIVEN an SVG label shows `Idle` but no highlightable ID equals `Idle`
- WHEN the user asks to highlight `Idle`
- THEN the system does not infer a target from visible text

### Requirement: In-Memory Runtime Bridge Contract

The system MUST expose one backend-owned runtime bridge for the active workbench server process. The minimal web contract MUST support snapshot read, `init/reset`, `send_event(event_id)`, and `set_variable(variable_id, value)`. Every successful mutation and every snapshot read MUST return the full updated snapshot. The live Python server/runtime in memory SHALL be the single source of truth. The viewer snapshot MUST preserve the runtime snapshot's last-event semantics: it MUST include the current `active_path` plus a `last_event` object describing the latest received event outcome. The bridge MUST serialize `last_event.event_id`, handled/unhandled status, handled `handler_kind` and handler ID, ordered `executed_activities`, and `transition_path_ids` only when transitions were actually taken. The bridge MUST NOT invent transition IDs for handled internal work, MUST NOT reinterpret semantic origins as SVG targets, and MUST NOT emit a scalar compatibility field for transition history.

#### Scenario: Viewer receives unhandled-event semantics

- GIVEN the runtime drops an event as unhandled
- WHEN the backend returns the updated snapshot
- THEN the payload still includes `last_event.event_id` with `handled=false`
- AND the viewer receives no implied transition path or executed activities

#### Scenario: Internal handling does not imply an external arrow

- GIVEN the runtime handles an event through an internal transition
- WHEN the backend serializes the snapshot for the viewer
- THEN `last_event.transition_path_ids` is empty while `last_event.executed_activities` remains ordered
- AND the payload still identifies the internal handler as the semantic source

#### Scenario: Ordered activity origins stay semantic-only

- GIVEN one handled event executes lifecycle and event-owned activities in order
- WHEN the bridge returns the viewer snapshot
- THEN each `executed_activities` item preserves runtime order with authored semantic origin metadata
- AND the payload contains no SVG ID, render fragment, or styling contract

#### Scenario: Reset returns a fresh backend snapshot

- GIVEN the workbench server has an in-memory runtime session
- WHEN the client requests `init/reset`
- THEN the backend reinitializes the runtime in memory
- AND the response returns the full updated snapshot

#### Scenario: Event and variable mutations round-trip through backend state

- GIVEN the client has one `event_id` or one `variable_id`
- WHEN it calls `send_event` or `set_variable`
- THEN the backend applies the mutation against the in-memory runtime only
- AND the response returns the full updated snapshot for re-render

### Requirement: Backend-Driven Exact-ID Highlight Sync

The system MUST derive shape highlight state in the backend and MUST return `active_ids` that match SVG element IDs by exact equality. `active_ids` MUST represent only the current active leaf state, even when `active_path` includes parent compounds. `last_transition_id` MUST be returned as the ordered latest-resolution path after filtering each member against `highlightable_ids` by exact equality. The backend MUST preserve surviving order, MUST drop unmatched members, and MUST NOT use labels, substrings, prefixes, or other partial-ID matching. The frontend MUST apply every returned transition ID and MUST preserve the current active-state and taken-edge shape/arrow highlighting behavior. The frontend MAY additionally highlight visible text only when session metadata provides private render-owned fragment targets and `last_event` provides matching semantic refs. Text emphasis MUST avoid heavier font weight and SHOULD use text-safe accent treatment such as underline and subtle background. For internal transitions, the viewer MUST highlight `internal_transitions:` plus only the matching internal-transition event/activity text for the latest handled row.

#### Scenario: Leaf-only state highlight is applied by exact ID

- GIVEN the backend snapshot reports a compound parent and one active leaf in `active_path`
- WHEN the snapshot response is produced
- THEN `active_ids` contains only the exact SVG ID for the active leaf
- AND the viewer highlights only that returned state ID with border emphasis and no fill intensification

#### Scenario: Mixed transition path is filtered member-by-member

- GIVEN the latest runtime resolution reports `["edge_enter", "edge_nested", "missing_edge"]` and only the first two are in `highlightable_ids`
- WHEN the snapshot response is produced
- THEN `last_transition_id` becomes `["edge_enter", "edge_nested"]` in that same order
- AND the viewer highlights both returned transitions without attempting a partial match for `missing_edge`

#### Scenario: Last-event semantics drive precise text emphasis

- GIVEN session metadata contains private targets for one transition label plus one state's `on_entry` label and executed activity text
- WHEN `last_event.transition_path_ids` and ordered `last_event.executed_activities` identify those semantic refs
- THEN the viewer highlights only the matching transition event/activity text and matching lifecycle label/activity fragments
- AND unrelated label text stays visually neutral

#### Scenario: Internal-transition highlighting stays row-specific

- GIVEN `last_event` reports a handled internal transition with no external transition path and the rendered state contains multiple internal-transition rows
- WHEN the viewer resolves private targets from the handled internal-transition semantic ref and executed activities
- THEN it highlights `internal_transitions:` and only that row's event/activity text
- AND no other internal-transition row or external edge receives highlight emphasis

### Requirement: Contract Robustness Validation

The system MUST reject a session as invalid when `diagram.svg` contains duplicate highlightable IDs, when backend-declared highlightable IDs reference an ID absent from the SVG, or when the SVG omits an authored Graphviz ID that the session declares highlightable. A valid session SHALL guarantee that every declared or returned highlight ID resolves to exactly one SVG element.

#### Scenario: Session creation fails on ID mismatch

- GIVEN the backend declares a highlightable ID missing from `diagram.svg`
- WHEN the session is validated
- THEN the system returns an actionable contract error
- AND the workbench does not start a misleading highlight session

### Requirement: Persistent Operator Sidebar

The workbench UI MUST keep one sidebar visible beside the SVG pane at normal workbench widths. The sidebar MUST present `Reset`, then `Events`, then `Variables`. The sidebar MUST NOT show `Status`, `Current state`, `Current snapshot`, or a separate title/intro block. `Reset runtime` and `Reset view` MUST appear together in one compact row while preserving their existing distinct behaviors. Sidebar controls MUST stay compact and SHOULD reduce unnecessary sidebar scrolling before true overflow occurs. The system MUST keep this as a frontend-only hierarchy simplification and MUST NOT alter runtime semantics.

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

#### Scenario: Intro block is removed without removing controls

- GIVEN the sidebar is rendered
- WHEN the operator looks above the control sections
- THEN no separate title or intro block is shown
- AND the existing controls remain available

#### Scenario: Reset actions stay grouped but distinct

- GIVEN the reset controls are visible
- WHEN the operator inspects that section
- THEN `Reset runtime` and `Reset view` appear together in one compact row
- AND each control keeps its own existing behavior

#### Scenario: Sidebar overflow appears only when needed

- GIVEN the compact sidebar controls fit within the visible height
- WHEN the operator opens the workbench at a normal desktop size
- THEN the sidebar does not require vertical scrolling
- AND independent sidebar overflow still appears if later content exceeds that height

### Requirement: Variables Stay Visible And Editable

The workbench UI MUST always render every declared `variable_id` as a live editable list entry with its current value from `snapshot.variables`, or an explicit unset state when no current value exists. The UI MUST allow editing each declared variable through the existing `set_variable(variable_id, value)` operation only. Successful and failed edits MUST refresh the visible value and status using the existing snapshot/mutation flow.

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

### Requirement: Scroll Ownership Remains Isolated Across Surfaces

The workbench UI MUST keep page scrolling disabled while the workbench is open. The sidebar MUST own vertical overflow only for sidebar content, and the diagram canvas MUST own overflow only when zoomed or panned diagram content exceeds the current viewport.

#### Scenario: Page scroll stays fixed while sidebar content overflows

- GIVEN the workbench page is open and sidebar content exceeds the visible sidebar height
- WHEN the user scrolls outside the diagram canvas
- THEN the document page position does not move
- AND only the sidebar scroll position changes

#### Scenario: Diagram scrollbars appear only for zoomed or panned overflow

- GIVEN the full diagram is fitted inside the current viewport
- WHEN the user has not zoomed or panned beyond the fitted bounds
- THEN the diagram canvas does not require scrollbars

### Requirement: Client-Side SVG View Controls

The workbench UI MUST keep mouse-wheel zoom inside the SVG viewport only, and wheel input over the sidebar MUST scroll only the sidebar vertically. The diagram viewport MUST support click-and-drag pan by moving viewport scroll offsets. During an active pan gesture, the viewport MUST NOT trigger browser text selection, text-underlining, or other selection side effects that interrupt drag ownership. Zoom and pan behavior MUST operate entirely in client-side view state and MUST NOT change SVG IDs, runtime state, or backend requests beyond the already existing workbench operations.

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

#### Scenario: Drag pans the diagram viewport without selection side effects

- GIVEN the diagram viewport has scrollable overflow at the current zoom
- WHEN the user clicks and drags inside the SVG viewport
- THEN the viewport scroll position updates to pan the diagram continuously
- AND no text selection or underline styling appears because of that drag

### Requirement: Events Use Simple Dispatch Controls

The workbench UI MUST present available events as one dropdown plus one `Send` action using the existing `send_event(event_id)` flow only.

#### Scenario: Event dispatch stays minimal

- GIVEN the session declares available events
- WHEN the user selects one event and activates `Send`
- THEN the UI sends exactly that `event_id` with no new parameters or backend fields

### Requirement: Compact One-Line Variable Rows

The workbench UI MUST render each declared `variable_id` as one compact row that keeps the variable name, editable value control, and submit action visible together without expanding into per-variable cards. The editable textbox MUST be the primary visible presentation of the current value from the existing snapshot flow. The row MUST still show an explicit inline unset state when no current value exists.

#### Scenario: Declared variables stay compact and editable

- GIVEN the session declares one or more `variable_ids`
- WHEN the sidebar renders or refreshes from a snapshot
- THEN each declared variable appears as one compact row
- AND the row still exposes the existing edit flow for that variable

#### Scenario: Unset variables do not expand into a larger layout

- GIVEN a declared variable has no current value
- WHEN the variable row is shown
- THEN the row stays on the same one-line compact layout
- AND the UI shows an explicit unset state

#### Scenario: Textbox shows the current value directly

- GIVEN a declared variable has a current value
- WHEN the row is rendered or refreshed
- THEN the editable textbox shows that value directly
- AND no separate current-value line is required

### Requirement: Resizable Sidebar And Split Layout

The workbench UI MUST provide a horizontal resizable split between the operator sidebar and the SVG viewport. Adjusting that split MUST remain a frontend-only layout action and MUST NOT change runtime state, backend requests, or the event/variable mutation contract.

#### Scenario: User resizes sidebar width

- GIVEN the workbench is open at a normal desktop width
- WHEN the user drags the sidebar-canvas splitter
- THEN the sidebar width and SVG viewport width both update in the same page session
- AND no runtime mutation is triggered by that resize

### Requirement: Runtime Reset And View Reset Stay Separate

The workbench UI MUST expose `Reset runtime` and `Reset view` as distinct actions. `Reset runtime` MUST use the existing runtime reset flow only. `Reset view` MUST restore only client-side diagram view state and MUST NOT call backend/runtime reset behavior.

#### Scenario: Reset runtime does not replace reset view

- GIVEN the user wants to reinitialize runtime state
- WHEN they activate `Reset runtime`
- THEN the existing runtime reset operation runs
- AND the diagram view action remains a separate control

#### Scenario: Reset view stays client-only

- GIVEN the user has changed zoom or pan locally
- WHEN they activate `Reset view`
- THEN the visible diagram view returns to its stored baseline
- AND no backend or runtime reset request is introduced

### Requirement: Fit-Based Initial View With Preserved Zoom And Pan

On initial diagram load, the workbench UI MUST start from a full-diagram fit baseline computed from the current viewport size so the complete rendered diagram is visible inside the viewport. `Reset view` MUST recompute and restore that full-diagram fit baseline from the current viewport size at the time of reset. After that baseline is established, existing client-side wheel zoom and drag-pan MUST continue to operate on top of it.

#### Scenario: Initial view fits the whole diagram in the current viewport

- GIVEN the SVG diagram has loaded successfully
- WHEN the first usable workbench view is presented
- THEN the complete diagram is fit within the current viewport
- AND no diagram region starts outside the visible baseline view

#### Scenario: Reset view refits after viewport size changes

- GIVEN the user changed the sidebar width or viewport size after initial load
- WHEN they activate `Reset view`
- THEN the visible diagram view is recomputed from the current viewport size
- AND the complete diagram becomes visible again within that viewport

#### Scenario: Zoom and pan remain available after fit

- GIVEN the diagram opened from the fit baseline
- WHEN the user zooms or pans the viewport
- THEN the existing client-side zoom and pan interactions still work
- AND those interactions remain layered on top of the fit-based starting view

### Requirement: Slice A Frontend Boundary

Slice A MUST stay frontend-only. It MAY add only compact one-line variable rows, a resizable sidebar/viewport split, separate `Reset runtime` and `Reset view` controls, and fit-based initial/reset view behavior. It MUST NOT change backend endpoints, runtime semantics, highlight behavior, internal SVG rendering, or later Slice B/C work.

#### Scenario: Backend and runtime remain unchanged

- GIVEN Slice A is implemented
- WHEN its behavior is evaluated
- THEN all runtime mutations still use the existing backend contract unchanged
- AND the change is limited to HTML/CSS/JS workbench UX behavior

### Requirement: Slice-1 Scope Boundary

This slice MUST remain a thin SVG workbench with minimal backend-owned runtime synchronization. It MAY include only snapshot read, `init/reset`, one event dispatch by `event_id`, one variable update by `variable_id`, backend-driven exact-ID highlight refresh, a persistent compact operator sidebar ordered as `Reset -> Events -> Variables`, independent sidebar scrolling, client-side wheel zoom inside the diagram viewport, and client-side drag-pan through viewport scrolling. It MAY additionally narrow `active_ids` to the active leaf only, add one optional `last_transition_id`, and refine CSS/view-model behavior needed to distinguish state-versus-transition highlighting. It MUST NOT include session persistence, recovery from persisted runtime session files, dependence on `workbench-session.json`, event parameters, event queues, timers, history, async runtime behavior, multi-document workspaces, multi-user support, heuristic element discovery, runtime-semantic expansion beyond that minimal highlight view-model addition, internal SVG structure changes, exact SVG ID semantic changes, mobile redesign, new status surfaces, or transform-state/freeform canvas pan.

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
