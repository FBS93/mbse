# Delta for hsm-json-graphviz-rendering

## MODIFIED Requirements

### Requirement: Deterministic Prepared Render Contract

From one valid HSM JSON v1 document, the system MUST produce one prepared Graphviz document with the same `document_id`, deterministic `dot_source`, and deterministic ordered `highlightable_ids`. State emission order MUST follow authored array order with depth-first traversal. Transition, initial-transition, `on_initial`, `on_entry`, `on_exit`, internal-transition, guard, and activity text MUST preserve authored order. State bodies MUST render `on_initial:`, `on_entry:`, and `on_exit:` as separate sections when present, and MUST render `internal_transitions:` when the state owns internal transitions. Internal-transition lines MUST use compact `event/activity` text, omitting `/activity` when no activities exist. Normal transition labels MUST use `event [guard]/activity`, omitting missing parts without leaving placeholder punctuation. Initial-transition edges MUST remain routing-only render elements: they MUST keep their authored IDs and visible source pseudostates, and MUST NOT render `initial_transition:` text or any activity list. The rendered SVG MUST omit any top graph-level `Variables` or `Events` summary banner. Prepared render metadata MAY include deterministic hierarchy fields plus private routing anchors, but private anchors MUST remain absent from `highlightable_ids` and invisible in the final SVG. Initial and compound routing MUST still reach the intended target without creating a stray public helper visual.

(Previously: the contract required initial-edge activity labels; after `on-initial-normalization`, parity is limited to state-body hooks, internal transitions, and normal transition guard/activity text while initials stay routing-only.)

#### Scenario: Same input yields same prepared output

- GIVEN the same valid HSM JSON v1 document and template version
- WHEN render preparation runs multiple times
- THEN `document_id`, `dot_source`, and `highlightable_ids` are identical across runs
- AND any private routing helpers are created deterministically from the same authored structure

#### Scenario: Top summary banner is absent

- GIVEN a valid document with declared variables and events
- WHEN DOT and SVG are generated
- THEN the rendered SVG contains no top graph-level `Variables` or `Events` summary banner
- AND those declarations remain available only through their existing authored data and downstream consumers

#### Scenario: Every highlightable element keeps its authored ID exactly

- GIVEN authored IDs `state_idle`, `state_parent`, `edge_start`, and `init_root`
- WHEN DOT and SVG are generated
- THEN the public highlightable SVG elements use exactly `state_idle`, `state_parent`, `edge_start`, and `init_root`
- AND no helper, renamed, prefixed, wrapped, or alternate public IDs replace or duplicate them

#### Scenario: State body shows lifecycle hooks and internal transitions

- GIVEN a compound state authors `on_initial`, `on_entry`, `on_exit`, and internal transitions
- WHEN DOT and SVG are generated
- THEN those sections render in the state body in authored order
- AND `internal_transitions:` shows compact `event/activity` rows without new public IDs

#### Scenario: Normal transition label shows guard and activity text

- GIVEN a transition authors an event, a guard, and activities
- WHEN DOT and SVG are generated
- THEN the visible edge label uses `event [guard]/activity`
- AND missing guard or activity text does not leave placeholder punctuation

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

- GIVEN a root initial and a compound state's local initial each target a compound-state endpoint that requires helper routing
- WHEN Graphviz renders the SVG
- THEN each initial transition reaches the intended compound target without changing any authored public SVG ID
- AND the initial source dots remain visible while no initial-edge activity label or helper public artifact appears

## ADDED Requirements

### Requirement: Render-Only Scope Boundary For Activity Parity Slice

This slice MUST stay inside JSON-to-DOT-to-SVG rendering only. It MAY add visible parity text for lifecycle hooks, internal transitions, and normal-transition guards and activities. It MUST NOT change runtime behavior, runtime data contracts, validation rules, viewer-highlighting behavior, shell/UI behavior, or the public authored-ID contract. Future activity highlighting and any activity-level SVG targets MUST remain out of scope for this slice.

#### Scenario: Activity highlighting remains out of scope

- GIVEN the activity parity slice is implemented
- WHEN the rendered SVG is inspected for highlight targets
- THEN the visible parity text appears without new activity-level public IDs
- AND activity highlighting requires a separate spec change
