# hsm-json-graphviz-rendering Specification

## Purpose

Define HSM JSON v1 as the source-of-truth contract for deterministic `JSON -> Jinja2 DOT -> Graphviz SVG -> workbench` rendering, without changing the downstream exact-SVG-ID contract.

## Requirements

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

### Requirement: Global Identity And Exact References

`document_id`, every variable `id`, event `id`, state `id`, transition `id`, and initial-transition `id` MUST be non-empty and unique within the document. IDs MUST match `^[a-z][a-z0-9_]*$`. Event parameter names MUST be unique within their event. Labels MUST NOT participate in identity. `source_id`, `target_id`, and any state `initial.target_id` MUST reference defined state IDs by exact string equality. `event_id`, when present, MUST reference a defined event. Nesting MUST NOT create local scopes, path-derived IDs, or rewritten render IDs.

#### Scenario: Duplicate labels do not collide

- GIVEN two states share a `label` and have different `id` values
- WHEN the document is validated and rendered
- THEN identity remains based only on authored IDs
- AND rendered Graphviz IDs equal those authored IDs exactly

#### Scenario: Broken references fail validation

- GIVEN a transition references an unknown event or state, or any global ID is duplicated
- WHEN the document is validated
- THEN the system rejects the document before DOT generation

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

### Requirement: Private Render-Owned Text Fragment Targets

The prepared render metadata MUST include a private render-owned fragment-target contract for text-level highlighting. The contract SHALL map authored semantic refs to normalized private SVG fragment targets for transition event/activity text, `on_initial`, `on_entry`, `on_exit` section labels plus executed activity text, and internal-transition section/row text. It MUST preserve authored/public SVG `id` values and `highlightable_ids` exactly, MUST keep current shape/edge targets unchanged, and MUST NOT move runtime or viewer concerns into the diagram-definition layer.

#### Scenario: Lifecycle and transition text get private targets

- GIVEN a state body renders `on_initial`, `on_entry`, `on_exit` content and an external transition renders event/activity text
- WHEN SVG marker hints are normalized into prepared metadata
- THEN the metadata includes private targets for those labels and activity fragments
- AND the public/authored SVG IDs remain unchanged

#### Scenario: Internal-transition rows stay distinguishable

- GIVEN one state renders `internal_transitions:` with multiple internal transition rows
- WHEN prepared metadata is produced
- THEN the contract includes one section-label target plus row-scoped event/activity targets keyed by `internal_transition_id`
- AND no new public SVG IDs are introduced for those rows

#### Scenario: Missing unique fragment stays unmapped

- GIVEN normalization cannot identify one unique fragment for a text target
- WHEN the contract is emitted
- THEN that private target is omitted instead of retargeting a different fragment
- AND the renderer does not mint or expose a replacement public ID

### Requirement: Render-Only Scope Boundary For Activity Parity Slice

This slice MUST stay inside JSON-to-DOT-to-SVG rendering only. It MAY add visible parity text for lifecycle hooks, internal transitions, and normal-transition guards and activities. It MUST NOT change runtime behavior, runtime data contracts, validation rules, viewer-highlighting behavior, shell/UI behavior, or the public authored-ID contract. Future activity highlighting and any activity-level SVG targets MUST remain out of scope for this slice.

#### Scenario: Activity highlighting remains out of scope

- GIVEN the activity parity slice is implemented
- WHEN the rendered SVG is inspected for highlight targets
- THEN the visible parity text appears without new activity-level public IDs
- AND activity highlighting requires a separate spec change

### Requirement: Compound State Cluster Visual Contract

Compound states MUST render their public parent visual on the enclosing Graphviz cluster. The cluster MUST carry the exact authored compound-state `id` and the visible parent label. State visuals for both flat and compound states MUST present a two-part structure: a title area above and an entry/exit body area below. That lower partition MUST remain present even when entry/exit content is empty. The system MUST NOT emit a second visible internal parent node for that same compound state. If Graphviz routing needs an internal endpoint for local initials or transitions, the system MAY emit one internal anchor, but that anchor MUST remain private and MUST NOT replace, duplicate, or expose a second public SVG identity for the authored compound state. This change MUST preserve the exact public SVG `id` contract for compound states and MUST NOT change runtime semantics, viewer-shell behavior, or the highlight contract.

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

### Requirement: Render-Only Scope Boundary For Slice C

This slice MUST stay inside JSON-to-DOT-to-SVG rendering only. It MAY remove the graph summary banner and refine state/compound-state visual partitioning. It MUST NOT change runtime behavior, runtime data contracts, viewer-shell UX, sidebar behavior, or the exact authored-ID contract beyond protecting it more explicitly in tests and render validation.

#### Scenario: Non-render work remains out of scope

- GIVEN the SVG render-improvement slice is implemented
- WHEN the change is evaluated
- THEN runtime execution and shell UI behavior remain unchanged
- AND any broader runtime or workbench UX change requires a separate spec change

### Requirement: Explicit v1 Boundary

HSM JSON v1 MUST include declarative events, event parameters, machine variables, `on_entry`, `on_exit`, and initial transitions. This rendering capability MUST treat those fields as declarative model data for validation and deterministic rendering only. The system MUST NOT infer or execute runtime behavior inside this capability. History, orthogonal regions, guards, action execution semantics, event-payload binding semantics, multi-document composition, reverse parsing, editing workflows, and layout-tuning fields MUST remain out of scope here. Unsupported constructs MUST be rejected rather than inferred. The same validated JSON MAY be consumed by a separate runtime capability without expanding this rendering contract.

#### Scenario: Deferred complex semantics stay out of v1

- GIVEN a document attempts to encode history or orthogonal regions
- WHEN the document is validated
- THEN the system rejects the document as out of scope for HSM JSON v1

#### Scenario: Render pipeline stays non-executable

- GIVEN a document contains variables, initials, and `on_entry` or `on_exit` strings
- WHEN the document is validated and prepared for rendering
- THEN the capability preserves those fields as declarative data only
- AND no runtime execution semantics are introduced by rendering
