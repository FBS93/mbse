# Delta for hsm-json-graphviz-rendering

## MODIFIED Requirements

### Requirement: Deterministic Prepared Render Contract

From one valid HSM JSON v1 document, the system MUST produce one prepared Graphviz document with the same `document_id`, deterministic `dot_source`, and deterministic ordered `highlightable_ids`. State emission order MUST follow authored array order with depth-first traversal. Transition, initial-transition, variable, event, parameter, `on_entry`, and `on_exit` label emission MUST follow authored order. The rendered SVG MUST omit any top graph-level `Variables` or `Events` summary banner. Prepared render metadata MAY include deterministic hierarchy visual fields plus internal routing anchors for initial and compound routing, but only non-public target/compound anchors MAY remain private. The visible source pseudostate at the start of every root or local initial transition MUST remain rendered as a visible black point and MUST NOT be suppressed, replaced, or made ambiguous by private routing cleanup. Every highlightable rendered state, compound-state container, transition, and initial-transition MUST emit the exact authored JSON `id` as the one public Graphviz/SVG `id`, unchanged, unique, and unambiguous. Private target/compound anchors MUST stay internal-only, absent from `highlightable_ids`, and invisible in the final Graphviz SVG. Initial and compound routing MUST still reach the intended target without producing a stray visible destination dot or helper ellipse.
(Previously: The requirement made private helpers explicit, but it did not distinguish visible initial source pseudostates from invisible private target/compound anchors.)

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
- AND the initial source dots remain visible while no stray visible helper point, destination dot, or helper ellipse appears at the target site
