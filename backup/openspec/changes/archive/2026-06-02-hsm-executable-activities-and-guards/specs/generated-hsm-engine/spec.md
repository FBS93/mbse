# Delta for generated-hsm-engine

## ADDED Requirements

### Requirement: Executable Behavior Model Contract

The system MUST use the term `activity`. Each state MAY define optional reserved lifecycle-slot activities named `on_initial`, `on_entry`, and `on_exit`. `on_initial` MUST describe the ordered activities of that state's local initial behavior and MUST remain distinct from normal event-associated activities. Event handling declarations MUST distinguish first-class `internal transition` definitions from normal `transition` definitions. An `internal transition` MUST declare `source_id`, `event_id`, and ordered `activities`, and MUST NOT declare a target or guard because it does not change state. A normal `transition` MUST declare `source_id`, `event_id`, explicit `target_id`, ordered `activities`, and MAY declare a `guard`. Activities and guards MUST be declared as schema-valid callable references, and inline code strings MUST be rejected.

#### Scenario: State lifecycle slots are declared distinctly

- GIVEN a compound state definition
- WHEN it declares `on_initial`, `on_entry`, and `on_exit`
- THEN the schema accepts all three as separate lifecycle slots
- AND `on_initial` is not modeled as a normal event activity list

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

## MODIFIED Requirements

### Requirement: Minimal Hierarchical Execution Semantics

The system MUST support exactly one active leaf path at a time. `init` MUST behave as the runtime start operation: begin from the root initial behavior and repeatedly follow nested local initials until the final active leaf is reached. `send_event` MUST first offer the event to the current leaf state and then continue outward through parents until one state handles the event or the event is dropped. When a state authors matching candidates across both `internal_transitions` and `transitions`, evaluation order MUST follow the document's authored collection order between those two collections while preserving declaration order inside each collection. Guards MUST participate in event handling and transition selection; when a matching candidate's guard evaluates false, that candidate MUST be treated as unhandled and bubbling MUST continue. The state that handles the event MUST be treated as the handling source. If handling selects a transition, the runtime MUST execute, in order: required exits from the current leaf toward the source/LCA, event-associated activities for the handled event, entry toward the explicit target, and repeated local initial resolution for each newly active compound state. If handling does not transition, the event-associated activities MUST still run and the active state MUST remain unchanged. Self, ancestor-target, descendant-target, and nested-initial behavior MUST match `example_hsm` in observable ordering and final active leaf semantics.

(Previously: Event dispatch bubbled structurally and only transition selection changed active state; guards and executable activities were out of scope.)

#### Scenario: Start follows the full initial chain

- GIVEN root initialization enters nested compound states
- WHEN `init()` is called
- THEN each state's `on_initial` runs only after that state becomes active
- AND the final active leaf is the last nested initial target

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
- THEN the capability remains compliant

#### Scenario: Deterministic replay stays stable

- GIVEN two runtime instances with the same model, callables, and inputs
- WHEN they receive the same initialization and event sequence
- THEN they produce the same activity order, state, and snapshot results
