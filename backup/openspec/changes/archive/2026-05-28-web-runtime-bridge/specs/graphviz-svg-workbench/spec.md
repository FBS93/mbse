# Delta for graphviz-svg-workbench

## ADDED Requirements

### Requirement: In-Memory Runtime Bridge Contract

The system MUST expose one backend-owned runtime bridge for the active workbench server process. The minimal web contract MUST support: read current snapshot, `init/reset`, `send_event`, and `set_variable`. `send_event` MUST accept exactly one `event_id`. `set_variable` MUST accept exactly one `variable_id` plus one raw JSON `value`. Every successful mutation and every snapshot read MUST return the full updated snapshot. The live Python server/runtime in memory SHALL be the single source of truth for runtime state and viewer-facing metadata.

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

The system MUST derive runtime highlight state in the backend from the current runtime snapshot and MUST return `active_ids` that match SVG element IDs by exact string equality. The frontend MUST apply only those returned IDs and MUST NOT infer targets from labels, titles, text, or heuristics.

#### Scenario: Active path becomes exact SVG highlights

- GIVEN the backend snapshot reports active runtime states
- WHEN the snapshot response is produced
- THEN `active_ids` contains the exact matching SVG IDs for those states
- AND the viewer highlights only those exact IDs

## MODIFIED Requirements

### Requirement: Slice-1 Session Artifacts

The system MUST create one bounded workbench session from one prepared Graphviz input. The workbench MUST expose `diagram.svg` for rendering, and it MAY expose read-only artifact metadata for static loading. For the runtime bridge slice, the viewer-facing runtime snapshot and the metadata needed to drive minimal event/variable controls MUST come from the live Python process in memory. The system MUST NOT require `workbench-session.json` or any persisted session-state artifact as the runtime source of truth.
(Previously: The session exposed exactly the prepared source document, `diagram.svg`, and `workbench-session.json` as the minimal backend/frontend contract.)

#### Scenario: Session opens from bounded artifacts plus live runtime metadata

- GIVEN one prepared input was rendered successfully
- WHEN the workbench session is created
- THEN the frontend can load `diagram.svg`
- AND runtime snapshot data is served from the live backend process

### Requirement: Slice-1 Scope Boundary

This slice MUST remain a thin SVG workbench with minimal backend-owned runtime synchronization. It MAY include only snapshot read, `init/reset`, one event dispatch by `event_id`, one variable update by `variable_id`, and backend-driven exact-ID highlight refresh. It MUST NOT include session persistence, recovery from persisted runtime session files, dependence on `workbench-session.json`, event parameters, event queues, timers, history, async runtime behavior, multi-document workspaces, multi-user support, heuristic element discovery, or visual redesign/polish.
(Previously: Slice 1 was a read-only SVG inspection and highlight workbench with runtime execution and synchronization excluded.)

#### Scenario: Deferred runtime features stay out of this slice

- GIVEN a user opens the runtime-enabled workbench successfully
- WHEN they inspect the available actions
- THEN only the minimal runtime bridge operations are available
- AND richer runtime semantics or visual enhancements are absent
