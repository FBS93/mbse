# Delta for hsm-json-graphviz-rendering

## MODIFIED Requirements

### Requirement: Deterministic Prepared Render Contract

From one valid HSM JSON v1 document, the system MUST produce one prepared Graphviz document with the same `document_id`, deterministic `dot_source`, and deterministic ordered `highlightable_ids`. State emission order MUST follow authored array order with depth-first traversal. Transition, initial-transition, variable, event, parameter, `on_entry`, and `on_exit` label emission MUST follow authored order. The rendered SVG MUST omit any top graph-level `Variables` or `Events` summary banner. Every highlightable rendered state, compound-state container, and transition MUST emit the exact authored JSON `id` as the public Graphviz/SVG `id` unchanged, with no renaming, prefixing, wrapper-owned replacement, or ambiguous alternate public identity.
(Previously: the contract required deterministic output and exact authored IDs, but did not forbid the top banner or spell out the exact-ID rule across every highlightable public SVG element.)

#### Scenario: Top summary banner is absent

- GIVEN a valid document with declared variables and events
- WHEN DOT and SVG are generated
- THEN the rendered SVG contains no top graph-level `Variables` or `Events` summary banner
- AND those declarations remain available only through their existing authored data and downstream consumers

#### Scenario: Every highlightable element keeps its authored ID exactly

- GIVEN authored IDs `state_idle`, `state_parent`, and `edge_start`
- WHEN DOT and SVG are generated
- THEN the public highlightable SVG elements use exactly `state_idle`, `state_parent`, and `edge_start`
- AND no renamed, prefixed, wrapped, or alternate public IDs replace them

### Requirement: Compound State Cluster Visual Contract

Compound states MUST render their public parent visual on the enclosing Graphviz cluster. The cluster MUST carry the exact authored compound-state `id` and the visible parent label. State visuals for both flat and compound states MUST present a clearer two-part structure: a title area above and an entry/exit body area below when entry/exit content exists. The system MUST NOT emit a second visible internal parent node for that same compound state. If Graphviz routing needs an internal endpoint for local initials or transitions, the system MAY emit one internal anchor, but that anchor MUST remain private and MUST NOT replace, duplicate, or expose a second public SVG identity for the authored compound state. This change MUST preserve the exact public SVG `id` contract for compound states and MUST NOT change runtime semantics, viewer-shell behavior, or the highlight contract.
(Previously: compound states rendered on the cluster with exact public IDs, but the requirement did not define the clearer title/body partition or restate the private-anchor-only boundary.)

#### Scenario: Compound parent keeps exact public ID with clearer partitioning

- GIVEN a compound state with authored `id` `state_parent`, label `Parent`, and entry/exit content
- WHEN the document is prepared and rendered to SVG
- THEN the enclosing cluster exposes the exact public SVG `id` `state_parent`
- AND the visible state renders with a distinct title area above its entry/exit body area

#### Scenario: Internal routing anchor stays private

- GIVEN a compound state with nested children and an internal routing anchor
- WHEN the document is rendered
- THEN no second public highlightable SVG identity represents that parent state
- AND the internal anchor does not rename or replace the public `state_parent` ID

## ADDED Requirements

### Requirement: Render-Only Scope Boundary For Slice C

This slice MUST stay inside JSON-to-DOT-to-SVG rendering only. It MAY remove the graph summary banner and refine state/compound-state visual partitioning. It MUST NOT change runtime behavior, runtime data contracts, viewer-shell UX, sidebar behavior, or the exact authored-ID contract beyond protecting it more explicitly in tests and render validation.

#### Scenario: Non-render work remains out of scope

- GIVEN the SVG render-improvement slice is implemented
- WHEN the change is evaluated
- THEN runtime execution and shell UI behavior remain unchanged
- AND any broader runtime or workbench UX change requires a separate spec change
