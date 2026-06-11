# generated-hsm-engine Specification

## Purpose

Define the first executable HSM runtime slice generated from validated HSM JSON v1 behind a stable handwritten API.

## Requirements

### Requirement: Stable Runtime API

The system MUST expose only `init`, `set_variable`, `get_variable`, `send_event`, `set_state`, `get_state`, and `get_snapshot` as the public runtime surface. `init` MUST resolve the initial active leaf path. `set_variable` MUST store one variable value by ID. `get_variable` MUST return the stored value for one variable ID. `send_event` MUST dispatch one event by ID against the current active state path. `set_state` MUST force the active leaf state for controlled test or inspection use. `get_state` MUST return the current active leaf state ID. `get_snapshot` MUST return a deterministic inspection view containing at least the current leaf state ID, active ancestry path, and runtime variable values.

#### Scenario: Initialization produces an inspectable state

- GIVEN a valid generated machine and a handwritten runtime instance
- WHEN `init()` is called
- THEN the runtime resolves one active leaf state deterministically
- AND `get_state()` and `get_snapshot()` report that same leaf state

#### Scenario: Variable access is explicit

- GIVEN an initialized runtime
- WHEN `set_variable("speed", 3)` and then `get_variable("speed")` are called
- THEN the returned value is `3`

### Requirement: Minimal Hierarchical Execution Semantics

The system MUST support exactly one active leaf path at a time. `init` MUST resolve the root initial and each nested local initial until a leaf state is active. `send_event` MUST first offer the event to the current leaf state and then continue outward through parents until one state handles the event or the event is dropped. When a transition is taken, the runtime MUST update the active leaf path deterministically to the transition target plus any required nested initials.

#### Scenario: Parent fallback handles an event

- GIVEN the active leaf does not handle event `ev_stop` and its parent does
- WHEN `send_event("ev_stop")` is called
- THEN the parent-level transition or handling is applied
- AND the resulting active leaf path is updated deterministically

#### Scenario: Unhandled event is inert

- GIVEN no state on the active path handles event `ev_ping`
- WHEN `send_event("ev_ping")` is called
- THEN the event is dropped without changing state or variables

### Requirement: Generated Engine And Handwritten Runtime Stay Separated

The generated engine MUST remain an internal dependency, not a public API. The handwritten runtime layer MUST own machine context, public operations, and inspection hooks. The generated engine MUST provide one internal state-handler function per authored state and the runtime MUST dispatch events to the handler of the current state with machine context. `set_state` MUST NOT be required for normal business flow.

#### Scenario: Public callers do not depend on generated internals

- GIVEN a consumer uses the runtime API
- WHEN the generated engine structure changes without changing public semantics
- THEN the consumer contract remains the handwritten API only

### Requirement: Explicit v1 Exclusions And Safety

The system MUST NOT execute authored `on_entry` or `on_exit` strings in v1. The system MUST NOT add guards, transition-action execution, timers, history, orthogonal regions, event queues, async dispatch, or string evaluation semantics in this capability. Generated behavior MUST be deterministic for the same machine structure, starting variables, forced state, and event sequence.

#### Scenario: Action strings remain inert metadata

- GIVEN a state declares ordered `on_entry` and `on_exit` strings
- WHEN `init()` or `send_event()` runs
- THEN those strings are not evaluated or executed

#### Scenario: Deterministic replay stays stable

- GIVEN two runtime instances with the same generated machine and same inputs
- WHEN they receive the same initialization, variable updates, and event sequence
- THEN they produce the same state and snapshot results
