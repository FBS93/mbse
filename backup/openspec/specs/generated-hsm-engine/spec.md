# generated-hsm-engine Specification

## Purpose

Define the first executable HSM runtime slice generated from validated HSM JSON v1 behind a stable handwritten API.

## Requirements

### Requirement: Stable Runtime API

The system MUST expose only `init`, `set_variable`, `get_variable`, `send_event`, `set_state`, `get_state`, and `get_snapshot` as the public runtime surface. `init` MUST resolve the initial active leaf path. `set_variable` MUST store one variable value by ID. `get_variable` MUST return the stored value for one variable ID. `send_event` MUST dispatch one event by ID against the current active state path. `set_state` MUST force the active leaf state for controlled test or inspection use. `get_state` MUST return the current active leaf state ID. `get_snapshot` MUST return a deterministic inspection view containing at least the current leaf state ID, active ancestry path, runtime variable values, and `last_event`, where `last_event` describes the latest received event outcome rather than only the resulting active state. `last_event` MUST include the received `event_id`, whether it was handled, the matched handler kind and handler ID when handled, `transition_path_ids` only for transitions actually taken in that same resolution, and ordered `executed_activities`. Each `executed_activities` item MUST preserve execution order and MUST include the authored `activity_id` plus semantic origin metadata `{owner_kind, owner_id}` sufficient to identify which state lifecycle slot or event handler produced it, without including render-target or SVG-specific fields. `transition_path_ids` MUST serialize as a JSON array for bridge consumers, MUST preserve execution order including nested initial transitions caused by a taken external transition, and MUST be empty for unhandled events, handled internal transitions, `set_state()`, or any handled event that takes no transition.

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

The system MUST support exactly one active leaf path at a time. `init` MUST begin from root initial routing and follow nested local initials until the final leaf is reached. Root and local `initial` objects MUST provide routing only and MUST NOT execute activities. When a compound state becomes active during `init` or nested initial descent, that state's optional `on_initial` MAY run only after activation and before the next local initial routing step. `send_event` MUST keep the same bubbling, guard, transition-order, exit, event-activity, entry, and nested-initial semantics already defined here.

(Previously: initial resolution followed root and local initials but the capability did not forbid distinct executable behavior authored on initial objects.)

#### Scenario: Start follows the full initial chain

- GIVEN root initialization enters nested compound states
- WHEN `init()` is called
- THEN each state's `on_initial` runs only after that state becomes active
- AND no root or local `initial` object executes its own activities

#### Scenario: Guard-false handling bubbles outward

- GIVEN the leaf state matches an event but its guard evaluates false
- WHEN `send_event()` is called
- THEN that candidate is treated as unhandled
- AND dispatch continues toward ancestors until a handler succeeds or the event is dropped

#### Scenario: Handled event without transition still runs activities

- GIVEN a state handles an event with ordered event-associated activities and no taken transition
- WHEN `send_event()` is called
- THEN those activities run in declaration order
- AND the active leaf state does not change

#### Scenario: Self transition re-enters the source state

- GIVEN the active leaf handles an event with an explicit target equal to itself
- WHEN the transition is taken
- THEN `on_exit` runs before event-associated activities and `on_entry` runs after them
- AND the active leaf remains that same state after re-entry

#### Scenario: Ancestor and descendant paths preserve `example_hsm` ordering

- GIVEN a handled event targets either an ancestor or a descendant of the handling source
- WHEN the transition is taken
- THEN ancestor targets do not re-enter the target ancestor and descendant targets do not exit the ancestor source
- AND any newly active compound target continues through its nested `on_initial` resolution before the final leaf is reported

### Requirement: Executable Behavior Model Contract

The system MUST use the term `activity`. Each state MAY define optional lifecycle-slot activities named `on_initial`, `on_entry`, and `on_exit`. `on_initial` MUST be the only executable initial hook and MUST describe the ordered activities of that owning state's local initial behavior. The root document `initial` object and any state `initial` object MUST contain only `id` and `target_id` and MUST NOT declare `activities` or any other executable field. Event handling MUST distinguish `internal transition` definitions from normal `transition` definitions. An `internal transition` MUST declare `source_id`, `event_id`, and ordered `activities`, and MUST NOT declare a target or guard. A normal `transition` MUST declare `source_id`, `event_id`, explicit `target_id`, ordered `activities`, and MAY declare a `guard`. Activities and guards MUST be declared as schema-valid callable references, and inline code strings MUST be rejected.

(Previously: `on_initial` was state-owned, but initial objects could still carry distinct executable activities.)

#### Scenario: State lifecycle slots are declared distinctly

- GIVEN a compound state definition
- WHEN it declares `on_initial`, `on_entry`, and `on_exit`
- THEN the schema accepts all three as separate lifecycle slots
- AND `on_initial` is the only executable hook for initial behavior

#### Scenario: Initial objects stay structural only

- GIVEN a root or local `initial` object
- WHEN it is authored in HSM JSON v1
- THEN only `id` and `target_id` are accepted
- AND authored `initial.activities` is rejected

#### Scenario: Event handling declares activities and guard

- GIVEN an event handler definition for a state
- WHEN it includes ordered `activities` and an optional `guard`
- THEN the schema accepts the declaration
- AND the order of `activities` is preserved

#### Scenario: Internal transitions are authored without a target

- GIVEN a state handles an event internally
- WHEN the author declares an `internal transition`
- THEN the schema accepts ordered `activities` with `source_id` and `event_id`
- AND the schema rejects `target_id` or `guard` on that internal transition

### Requirement: Generated Engine And Handwritten Runtime Stay Separated

The generated engine MUST remain an internal dependency, not a public API. The handwritten runtime layer MUST own machine context, public operations, and inspection hooks. The generated engine MUST provide one internal state-handler function per authored state and the runtime MUST dispatch events to the handler of the current state with machine context. `set_state` MUST NOT be required for normal business flow.

#### Scenario: Public callers do not depend on generated internals

- GIVEN a consumer uses the runtime API
- WHEN the generated engine structure changes without changing public semantics
- THEN the consumer contract remains the handwritten API only

### Requirement: Explicit v1 Exclusions And Safety

The system MUST execute authored `on_initial`, `on_entry`, `on_exit`, and event-associated activities only through validated callable references. The system MUST NOT execute inline code strings. Guards MUST be evaluated only as part of event handling / transition selection and SHOULD be side-effect free. This capability MUST NOT add timers, history, orthogonal regions, event queues, async dispatch, AO/pub-sub transport, or fixed-buffer embedded runtime mechanics. Generated behavior MUST remain deterministic for the same machine structure, callable set, starting variables, forced state, and event sequence.

(Previously: All authored `on_entry`/`on_exit` strings, guards, and transition-action execution were excluded and had to remain inert.)

#### Scenario: Inline executable strings are rejected

- GIVEN lifecycle or event behavior is authored as a raw code string
- WHEN the document is validated or prepared for runtime use
- THEN the document is rejected
- AND no runtime executes that string

#### Scenario: Embedded mechanics stay out of scope

- GIVEN parity tests cover Python-visible ordering and state outcomes
- WHEN runtime behavior matches `example_hsm` without embedded transport features
- THEN the capability is compliant without implementing embedded transport mechanics

#### Scenario: Deterministic replay stays stable

- GIVEN two runtime instances with the same model, callables, and inputs
- WHEN they receive the same initialization and event sequence
- THEN they produce the same activity order, state, and snapshot results
