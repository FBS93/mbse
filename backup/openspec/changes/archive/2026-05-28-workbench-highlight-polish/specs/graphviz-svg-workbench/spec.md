# Delta for graphviz-svg-workbench

## MODIFIED Requirements

### Requirement: In-Memory Runtime Bridge Contract

The system MUST expose one backend-owned runtime bridge for the active workbench server process. The minimal web contract MUST support: read current snapshot, `init/reset`, `send_event`, and `set_variable`. `send_event` MUST accept exactly one `event_id`. `set_variable` MUST accept exactly one `variable_id` plus one raw JSON `value`. Every successful mutation and every snapshot read MUST return the full updated snapshot. The live Python server/runtime in memory SHALL be the single source of truth for runtime state and viewer-facing metadata. For this slice, the snapshot view-model MAY add one optional exact SVG `last_transition_id`, and `active_path` MUST remain unchanged for observability.
(Previously: the contract allowed only the existing snapshot fields and did not define `last_transition_id`.)

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

The system MUST derive runtime highlight state in the backend from the current runtime snapshot and MUST return `active_ids` that match SVG element IDs by exact string equality. `active_ids` MUST represent only the current active leaf state, even when `active_path` includes parent compounds. The snapshot MAY include one optional `last_transition_id`, and when present it MUST identify the final exact SVG transition ID that led into the current leaf state. The frontend MUST apply only those returned exact IDs, MUST render state highlight and transition highlight as visually distinct treatments, MUST keep the state highlight subtle enough to preserve label legibility, and MUST NOT infer targets from labels, titles, text, or heuristics.
(Previously: `active_ids` reflected the active path broadly and no distinct transition highlight contract existed.)

#### Scenario: Leaf-only state highlight is applied by exact ID

- GIVEN the backend snapshot reports a compound parent and one active leaf in `active_path`
- WHEN the snapshot response is produced
- THEN `active_ids` contains only the exact SVG ID for the active leaf
- AND the viewer highlights only that returned state ID

#### Scenario: Final transition into the leaf is highlighted separately

- GIVEN entry into the current leaf required one or more transitions
- WHEN the snapshot response is produced
- THEN `last_transition_id` identifies only the final transition into that leaf when such an SVG ID exists
- AND the viewer applies a transition highlight that is visually distinct from the state highlight

### Requirement: Slice-1 Scope Boundary

This slice MUST remain a thin SVG workbench with minimal backend-owned runtime synchronization. It MAY include only snapshot read, `init/reset`, one event dispatch by `event_id`, one variable update by `variable_id`, backend-driven exact-ID highlight refresh, a persistent compact operator sidebar ordered as `Reset -> Events -> Variables`, independent sidebar scrolling, client-side wheel zoom inside the diagram viewport, and client-side drag-pan through viewport scrolling. For this highlight-polish slice, it MAY additionally narrow `active_ids` to the active leaf only, add one optional `last_transition_id`, and refine CSS/view-model behavior needed to distinguish state-versus-transition highlighting. It MUST NOT change internal SVG structure, exact SVG ID semantics, runtime execution semantics beyond that minimal view-model addition, transition history beyond the final transition into the active leaf, multi-step execution modeling, mobile redesign, new status surfaces, or transform-state/freeform canvas pan.
(Previously: backend contract changes and runtime-semantic expansion were broadly out of scope; this slice allows only the minimal highlight view-model delta.)

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
