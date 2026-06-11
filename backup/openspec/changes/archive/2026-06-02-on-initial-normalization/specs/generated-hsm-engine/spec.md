# Delta for generated-hsm-engine

## MODIFIED Requirements

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
