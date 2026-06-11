# Delta for hsm-json-graphviz-rendering

## MODIFIED Requirements

### Requirement: Canonical HSM JSON v1 Document

The system MUST define one JSON Schema-governed HSM document. The root object MUST contain `schema_version`, `document_id`, `variables`, `events`, `states`, and `transitions`, and MAY contain one root `initial`. `schema_version` MUST equal `hsm-v1`. `variables`, `events`, and `transitions` MAY be empty arrays. Each variable MUST contain `id`. Each event MUST contain `id` and MAY contain ordered `parameters`. Each state MUST contain `id` and MAY contain `label`, recursive `states`, ordered `on_initial`, ordered `on_entry`, ordered `on_exit`, and one `initial`. Each transition MUST contain `id`, `source_id`, and `target_id`, and MAY contain `event_id`. Additional properties MUST be rejected.

(Previously: states could declare `on_entry` and `on_exit`, but the canonical document did not require `on_initial` as the matching optional lifecycle hook.)

#### Scenario: Minimal FSM-form document is valid

- GIVEN a document with the required root fields, one top-level state, and empty `variables`, `events`, and `transitions`
- WHEN the document is validated against HSM JSON v1
- THEN the document is accepted as a valid flat-machine input

#### Scenario: Behavioral metadata is valid

- GIVEN an event declares ordered parameters and a state declares ordered `on_initial`, `on_entry`, and `on_exit`
- WHEN the document is validated
- THEN the document is accepted without requiring render-time execution semantics

### Requirement: Supported Hierarchy And Initials For v1

The root `states` array MUST define the top-level state set. A state MAY contain nested `states`, and nesting MAY repeat recursively to form a finite tree. A valid FSM input SHALL be the case where no state contains nested states. The root document MAY declare one root initial transition, and a compound state MAY declare one local initial transition, each with only `id` and `target_id`. A local initial target MUST be one of that state's direct children. Shared children, cyclic containment, multiple initials for the same container, and authored `initial.activities` MUST NOT be allowed.

(Previously: root and local initials were defined by `id` and `target_id`, but the requirement did not explicitly forbid executable `initial.activities`.)

#### Scenario: Hierarchical state with local initial is valid

- GIVEN a compound state contains child states and one `initial` targeting a direct child
- WHEN the document is validated
- THEN the hierarchy is accepted as valid HSM JSON v1

#### Scenario: Invalid or executable initial is rejected

- GIVEN a compound state's `initial` points outside its child set or declares `activities`
- WHEN the document is validated
- THEN the system rejects the document

### Requirement: Deterministic Prepared Render Contract

From one valid HSM JSON v1 document, the system MUST produce one prepared Graphviz document with the same `document_id`, deterministic `dot_source`, and deterministic ordered `highlightable_ids`. State emission order MUST follow authored array order with depth-first traversal. Transition, initial-transition, `on_initial`, `on_entry`, and `on_exit` label emission MUST follow authored order. State bodies MUST render `on_initial:`, `on_entry:`, and `on_exit:` as separate sections when present. Initial-transition edges MUST remain routing-only render elements: they MUST keep their authored IDs and visible source pseudostates, and MUST NOT render `initial_transition:` text or any activity list. The rendered SVG MUST omit any top graph-level `Variables` or `Events` summary banner. Prepared render metadata MAY include deterministic hierarchy fields plus private routing anchors, but private anchors MUST remain absent from `highlightable_ids` and invisible in the final SVG. Initial and compound routing MUST still reach the intended target without creating a stray public helper visual.

(Previously: prepared render output allowed distinct initial-transition activity text alongside state-owned `on_initial` sections.)

#### Scenario: Same input yields same prepared output

- GIVEN the same valid HSM JSON v1 document and template version
- WHEN render preparation runs multiple times
- THEN `document_id`, `dot_source`, and `highlightable_ids` are identical across runs
- AND any private routing helpers are created deterministically from the same authored structure

#### Scenario: Top summary banner is absent

- GIVEN a valid document with declared variables and events
- WHEN DOT and SVG are generated
- THEN the rendered SVG contains no top `Variables` or `Events` summary banner
- AND those declarations remain available only through authored data and downstream consumers

#### Scenario: Every highlightable element keeps its authored ID exactly

- GIVEN authored IDs `state_idle`, `state_parent`, `edge_start`, and `init_root`
- WHEN DOT and SVG are generated
- THEN the public highlightable SVG elements use exactly those authored IDs
- AND no helper, renamed, prefixed, wrapped, or alternate public IDs replace or duplicate them

#### Scenario: State-owned hooks render without competing initial text

- GIVEN a compound state authors `on_initial`, `on_entry`, and `on_exit`
- WHEN DOT and SVG are generated
- THEN those sections render in the state body in authored order
- AND no `initial_transition:` section or initial activity text appears

#### Scenario: Initial source pseudostates stay visible

- GIVEN a root initial or local initial is present in the authored model
- WHEN Graphviz renders the SVG for that initial transition
- THEN the source pseudostate at the start of the initial transition is visible as a black point
- AND private routing cleanup does not remove, hide, or replace that visible source marker

#### Scenario: Private target and compound routing anchors stay private

- GIVEN a render needs internal routing support for an initial target or compound-state endpoint
- WHEN the prepared render view and SVG are produced
- THEN private anchor records remain absent from `highlightable_ids` and from the public authored-ID set
- AND the final SVG exposes no stray visible target dot or helper ellipse as a public artifact

#### Scenario: Root and local initials route cleanly to compound targets

- GIVEN a root initial or local initial is present in the authored model
- WHEN Graphviz renders the SVG
- THEN the initial edge keeps its authored public ID and reaches the intended target
- AND the source dot stays visible while no stray helper point, destination dot, or helper ellipse appears
