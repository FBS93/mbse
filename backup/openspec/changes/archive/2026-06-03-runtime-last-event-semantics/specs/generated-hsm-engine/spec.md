# Delta for generated-hsm-engine

## MODIFIED Requirements

### Requirement: Stable Runtime API

The system MUST expose only `init`, `set_variable`, `get_variable`, `send_event`, `set_state`, `get_state`, and `get_snapshot` as the public runtime surface. `init` MUST resolve the initial active leaf path. `set_variable` MUST store one variable value by ID. `get_variable` MUST return the stored value for one variable ID. `send_event` MUST dispatch one event by ID against the current active state path. `set_state` MUST force the active leaf state for controlled test or inspection use. `get_state` MUST return the current active leaf state ID. `get_snapshot` MUST return a deterministic inspection view containing at least the current leaf state ID, active ancestry path, runtime variable values, and `last_event`, where `last_event` describes the latest received event outcome rather than only the resulting active state. `last_event` MUST include the received `event_id`, whether it was handled, the matched handler kind and handler ID when handled, `transition_path_ids` only for transitions actually taken in that same resolution, and ordered `executed_activities`. Each `executed_activities` item MUST preserve execution order and MUST include the authored `activity_id` plus semantic origin metadata `{owner_kind, owner_id}` sufficient to identify which state lifecycle slot or event handler produced it, without including render-target or SVG-specific fields. `transition_path_ids` MUST serialize as a JSON array for bridge consumers, MUST preserve execution order including nested initial transitions caused by a taken external transition, and MUST be empty for unhandled events, handled internal transitions, `set_state()`, or any handled event that takes no transition.

(Previously: `get_snapshot` only had to expose current state, variables, and `last_transition_id` as the latest resolution path.)

#### Scenario: Unhandled event is reported without implied execution

- GIVEN an initialized runtime and no handler accepts `event_id="tick"`
- WHEN `send_event("tick")` completes and `get_snapshot()` is read
- THEN `last_event.event_id` is `tick` and `last_event.handled` is `false`
- AND `last_event.transition_path_ids` and `last_event.executed_activities` are both empty

#### Scenario: Internal handling keeps state but reports execution

- GIVEN the active state handles `event_id="pulse"` with an internal transition
- WHEN `send_event("pulse")` completes
- THEN the active leaf state is unchanged and `last_event.handled` is `true`
- AND `last_event.handler_kind` is `internal_transition`, `transition_path_ids` is empty, and `executed_activities` stays ordered

#### Scenario: External transition reports only transitions actually taken

- GIVEN a handled event takes one authored transition and then nested initial routing
- WHEN `send_event()` completes
- THEN `last_event.handler_kind` is `transition`
- AND `last_event.transition_path_ids` lists exactly the taken transition IDs in execution order
