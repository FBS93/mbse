# Delta for hsm-json-graphviz-rendering

## MODIFIED Requirements

### Requirement: Deterministic Prepared Render Contract

From one valid HSM JSON v1 document, the system MUST produce one prepared Graphviz document with the same `document_id`, deterministic `dot_source`, and deterministic ordered `highlightable_ids`. State emission order MUST follow authored array order with depth-first traversal. Transition, initial-transition, variable, event, parameter, `on_entry`, and `on_exit` label emission MUST follow authored order. The rendered SVG MUST omit any top graph-level `Variables` or `Events` summary banner. Prepared render metadata MAY include deterministic hierarchy visual fields, but every highlightable rendered state, compound-state container, and transition MUST emit the exact authored JSON `id` as the public Graphviz/SVG `id` unchanged, with no renaming, prefixing, wrapper-owned replacement, or ambiguous alternate public identity.
(Previously: the contract required deterministic output and exact authored IDs, but did not explicitly allow derived hierarchy visual metadata while preserving those IDs unchanged.)

#### Scenario: Same input yields same prepared output

- GIVEN the same valid HSM JSON v1 document and template version
- WHEN render preparation runs multiple times
- THEN `document_id`, `dot_source`, and `highlightable_ids` are identical across runs

#### Scenario: Top summary banner is absent

- GIVEN a valid document with declared variables and events
- WHEN DOT and SVG are generated
- THEN the rendered SVG contains no top graph-level `Variables` or `Events` summary banner
- AND those declarations remain available only through their existing authored data and downstream consumers

#### Scenario: Every highlightable element keeps its authored ID exactly

- GIVEN authored IDs `state_idle`, `state_parent`, and `edge_start`
- WHEN DOT and SVG are generated with hierarchy visuals enabled
- THEN the public highlightable SVG elements use exactly `state_idle`, `state_parent`, and `edge_start`
- AND no renamed, prefixed, wrapped, or alternate public IDs replace them

### Requirement: Compound State Cluster Visual Contract

Compound states MUST render their public parent visual on the enclosing Graphviz cluster. The cluster MUST carry the exact authored compound-state `id` and the visible parent label. State visuals for both flat and compound states MUST present a two-part structure: a title area above and an entry/exit body area below. That lower partition MUST remain present even when entry/exit content is empty. The system MUST NOT emit a second visible internal parent node for that same compound state. If Graphviz routing needs an internal endpoint for local initials or transitions, the system MAY emit one internal anchor, but that anchor MUST remain private and MUST NOT replace, duplicate, or expose a second public SVG identity for the authored compound state. This change MUST preserve the exact public SVG `id` contract for compound states and MUST NOT change runtime semantics, viewer-shell behavior, or the highlight contract.
(Previously: the requirement described clearer partitioning only when entry/exit content existed, without requiring the lower partition to remain visible when empty.)

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

#### Scenario: Empty action partition still renders

- GIVEN a flat or compound state with no `on_entry` and no `on_exit` lines
- WHEN the document is rendered
- THEN the visible state still includes the lower body partition
- AND the public authored SVG ID remains unchanged

## ADDED Requirements

### Requirement: Hierarchy-Derived State Colors

The renderer MUST apply a soft background color to states and compound states based on hierarchy depth. Level 0 MUST start from one configured RGB base color. Deeper levels MUST derive their colors from that base by one simple deterministic algorithm, and MUST NOT depend on a hardcoded per-level palette or on authored state IDs.

#### Scenario: Same depth shares the same tint

- GIVEN two states at the same hierarchy depth
- WHEN the document is rendered
- THEN both states receive the same derived background color
- AND that color is determined only from the shared depth and base RGB color

#### Scenario: Deeper depth derives a new tint deterministically

- GIVEN a top-level state and a nested child state
- WHEN the document is rendered
- THEN the child receives a different soft background color from the parent
- AND the child color is derived from the same base RGB color by the deterministic depth algorithm

### Requirement: Render-Only Scope Boundary For Hierarchy Visual Slice

This slice MUST stay inside JSON-to-DOT-to-SVG rendering only. It MAY add hierarchy-derived state colors and always-visible empty action partitions. It MUST NOT change runtime behavior, runtime data contracts, validation rules, workbench shell/UI behavior, or highlight semantics.

#### Scenario: Non-render work remains out of scope

- GIVEN the hierarchy visual slice is implemented
- WHEN the change is evaluated
- THEN runtime execution and viewer behavior remain unchanged
- AND any broader runtime or UX change requires a separate spec change
