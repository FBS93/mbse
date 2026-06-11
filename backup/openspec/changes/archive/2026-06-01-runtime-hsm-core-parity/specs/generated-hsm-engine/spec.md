# Delta for generated-hsm-engine

## MODIFIED Requirements

### Requirement: Minimal Hierarchical Execution Semantics

The system MUST support exactly one active leaf path at a time. `init` MUST behave as the runtime start operation: begin from the root initial transition and repeatedly follow nested local initials until the final active leaf is reached. `send_event` MUST first offer the event to the current leaf state and then continue outward through parents until one state handles the event or the event is dropped. When a transition is taken, the state that returned the transition MUST be treated as the transition source. The runtime MUST compute the exit path from the active leaf up to but excluding the lowest common ancestor of source and explicit target, MUST compute the entry path from that ancestor down to the explicit target, and MUST then follow any nested initials required below the target. Self, ancestor-target, descendant-target, and cross-branch transitions MUST produce the same final active leaf as the C reference behavior.
(Previously: The runtime only had to bubble events and deterministically rebuild the target leaf path after a taken transition.)

#### Scenario: Start follows the full initial chain

- GIVEN the reference topology whose root initial descends through `S1 → S11 → S111 → S1111`
- WHEN `init()` is called
- THEN the active leaf is `S11111`
- AND no intermediate compound state remains active as the final leaf

#### Scenario: Ancestor dispatch source can take a transition

- GIVEN the active leaf is `S11111` and only `S1` handles `TRANSITION`
- WHEN `send_event("TRANSITION")` is called
- THEN the runtime escalates to `S1`, uses `S1` as the transition source, and ends in `S2111`

#### Scenario: Same-branch transition trims at the local ancestor

- GIVEN the active leaf is `S2111`
- WHEN `send_event("TRANSITION")` takes the explicit target `S2112`
- THEN the runtime exits only the source leaf, reuses common ancestry under `S211`, and ends in `S2112`

#### Scenario: Ancestor target stops at that ancestor

- GIVEN the active leaf is `S2112`
- WHEN `send_event("TRANSITION")` takes the explicit target `S2`
- THEN the runtime trims entry at the `S2` ancestor and ends in `S2`

#### Scenario: Cross-branch target performs nested initial descent

- GIVEN the active leaf is `S311`
- WHEN `send_event("TRANSITION")` takes the explicit target `S4`
- THEN the runtime exits up to the branch LCA, enters `S4`, follows `S4`'s local initial, and ends in `S41`

#### Scenario: Self transition re-enters the active leaf

- GIVEN the active leaf is `S41` and the handled transition explicitly targets `S41`
- WHEN `send_event("TRANSITION")` is called
- THEN the runtime treats it as a self transition and the active leaf remains `S41`

#### Scenario: Unhandled event is inert

- GIVEN no state on the active path handles event `ev_ping`
- WHEN `send_event("ev_ping")` is called
- THEN the event is dropped without changing state or variables

### Requirement: Explicit v1 Exclusions And Safety

The system MUST NOT execute authored `on_entry` or `on_exit` strings in v1. The system MUST NOT add guards, transition-action execution, timers, history, orthogonal regions, event queues, async dispatch, or string evaluation semantics in this capability. This runtime-parity slice MUST NOT require AO/pub-sub, scheduler behavior, reserved event objects, fixed-depth buffers, static-memory rules, or other embedded transport mechanics irrelevant to the Python host runtime. Generated behavior MUST be deterministic for the same machine structure, starting variables, forced state, and event sequence.
(Previously: The exclusions covered generic v1 omissions, but did not explicitly exclude AO/scheduler/static-memory mechanics from the parity slice.)

#### Scenario: Action strings remain inert metadata

- GIVEN a state declares ordered `on_entry` and `on_exit` strings
- WHEN `init()` or `send_event()` runs
- THEN those strings are not evaluated or executed

#### Scenario: Embedded mechanics stay out of scope

- GIVEN parity tests cover only Python-visible state-path outcomes
- WHEN runtime behavior matches the reference without AO queues or static buffers
- THEN the capability is compliant without implementing embedded transport mechanics
