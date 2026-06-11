# Delta for graphviz-svg-workbench

## MODIFIED Requirements

### Requirement: In-Memory Runtime Bridge Contract

The system MUST expose one backend-owned runtime bridge for the active workbench server process. The minimal web contract MUST support snapshot read, `init/reset`, `send_event(event_id)`, and `set_variable(variable_id, value)`. Every successful mutation and every snapshot read MUST return the full updated snapshot. The live Python server/runtime in memory SHALL be the single source of truth. The snapshot MUST expose `last_transition_id` as a JSON array of exact SVG transition IDs in latest-resolution order, and `active_path` MUST remain unchanged. The bridge MUST NOT emit a scalar `last_transition_id`, fallback field, or compatibility format.
(Previously: the snapshot view-model could add one optional scalar `last_transition_id`.)

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

#### Scenario: Snapshot serializes the full transition path

- GIVEN one runtime resolution executes multiple authored transitions before the new leaf becomes active
- WHEN the backend returns the updated snapshot
- THEN `last_transition_id` is a JSON array preserving that exact execution order
- AND the payload contains no scalar compatibility value

### Requirement: Backend-Driven Exact-ID Highlight Sync

The system MUST derive highlight state in the backend and MUST return `active_ids` that match SVG element IDs by exact equality. `active_ids` MUST represent only the current active leaf state, even when `active_path` includes parent compounds. `last_transition_id` MUST be returned as the ordered latest-resolution path after filtering each member against `highlightable_ids` by exact equality. The backend MUST preserve surviving order, MUST drop unmatched members, and MUST NOT use labels, substrings, prefixes, or other partial-ID matching. The frontend MUST apply every returned transition ID, MUST keep labels visually neutral, MUST emphasize active states through border/contour treatment only with no fill intensification, and MUST emphasize active transitions only on the edge line and arrowhead.
(Previously: `last_transition_id` identified only the final transition, active states also intensified fill, and path-member filtering was undefined.)

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

#### Scenario: Highlight styling excludes labels and targets only intended shapes

- GIVEN the active state or transition SVG group also contains visible text labels
- WHEN the frontend applies highlight styling for the returned exact IDs
- THEN text descendants keep their normal visual treatment
- AND only state borders or transition edge/arrowhead shapes receive highlight emphasis
