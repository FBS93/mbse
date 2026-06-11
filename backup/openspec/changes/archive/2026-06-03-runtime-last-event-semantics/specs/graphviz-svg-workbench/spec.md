# Delta for graphviz-svg-workbench

## MODIFIED Requirements

### Requirement: In-Memory Runtime Bridge Contract

The system MUST expose one backend-owned runtime bridge for the active workbench server process. The minimal web contract MUST support snapshot read, `init/reset`, `send_event(event_id)`, and `set_variable(variable_id, value)`. Every successful mutation and every snapshot read MUST return the full updated snapshot. The live Python server/runtime in memory SHALL be the single source of truth. The viewer snapshot MUST preserve the runtime snapshot's last-event semantics: it MUST include the current `active_path` plus a `last_event` object describing the latest received event outcome. The bridge MUST serialize `last_event.event_id`, handled/unhandled status, handled `handler_kind` and handler ID, ordered `executed_activities`, and `transition_path_ids` only when transitions were actually taken. The bridge MUST NOT invent transition IDs for handled internal work, MUST NOT reinterpret semantic origins as SVG targets, and MUST NOT emit a scalar compatibility field for transition history.

(Previously: the bridge only had to expose `active_path` plus `last_transition_id` as a JSON array of exact SVG transition IDs.)

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
