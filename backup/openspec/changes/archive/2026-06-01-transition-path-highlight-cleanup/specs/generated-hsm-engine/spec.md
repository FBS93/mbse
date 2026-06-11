# Delta for generated-hsm-engine

## MODIFIED Requirements

### Requirement: Stable Runtime API

The system MUST expose only `init`, `set_variable`, `get_variable`, `send_event`, `set_state`, `get_state`, and `get_snapshot` as the public runtime surface. `init` MUST resolve the initial active leaf path. `set_variable` MUST store one variable value by ID. `get_variable` MUST return the stored value for one variable ID. `send_event` MUST dispatch one event by ID against the current active state path. `set_state` MUST force the active leaf state for controlled test or inspection use. `get_state` MUST return the current active leaf state ID. `get_snapshot` MUST return a deterministic inspection view containing at least the current leaf state ID, active ancestry path, runtime variable values, and `last_transition_id` as the ordered latest-resolution transition path. `last_transition_id` MUST be a tuple of transition IDs in runtime memory, MUST serialize as a JSON array for bridge consumers, MUST include nested initial transitions taken during the same `init()` or `send_event()` resolution, and MUST be empty after `set_state()` or when no transition was taken in the latest snapshot.
(Previously: `get_snapshot` required deterministic state/path/variable inspection data but did not define `last_transition_id` as a full ordered path contract.)

#### Scenario: Initialization produces an inspectable state

- GIVEN a valid generated machine and a handwritten runtime instance
- WHEN `init()` is called
- THEN the runtime resolves one active leaf state deterministically
- AND `get_state()` and `get_snapshot()` report that same leaf state

#### Scenario: Variable access is explicit

- GIVEN an initialized runtime
- WHEN `set_variable("speed", 3)` and then `get_variable("speed")` are called
- THEN the returned value is `3`

#### Scenario: Initial resolution reports the full ordered path

- GIVEN root initialization enters an explicit initial transition and one nested local initial before reaching the leaf
- WHEN `init()` completes and `get_snapshot()` is read
- THEN `last_transition_id` equals those transition IDs in execution order
- AND the value is not reduced to only the final transition ID

#### Scenario: Forced state clears latest transition history

- GIVEN the runtime previously reported a non-empty `last_transition_id`
- WHEN `set_state("S2111")` is called and `get_snapshot()` is read
- THEN `last_transition_id` is empty
- AND no scalar compatibility value is returned
