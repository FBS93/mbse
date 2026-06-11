# hsm-json-graphviz-rendering Specification

## Purpose

Define HSM JSON v1 as the source-of-truth contract for deterministic `JSON -> Jinja2 DOT -> Graphviz SVG -> workbench` rendering, without changing the downstream exact-SVG-ID contract.

## Requirements

### Requirement: Canonical HSM JSON v1 Document

The system MUST define one JSON Schema-governed HSM document. The root object MUST contain `schema_version`, `document_id`, `variables`, `events`, `states`, and `transitions`, and MAY contain one root `initial`. `schema_version` MUST equal `hsm-v1`. `variables`, `events`, and `transitions` MAY be empty arrays. Each variable MUST contain `id`. Each event MUST contain `id` and MAY contain ordered `parameters`. Each state MUST contain `id` and MAY contain `label`, recursive `states`, ordered `on_entry`, ordered `on_exit`, and one `initial`. Each transition MUST contain `id`, `source_id`, and `target_id`, and MAY contain `event_id`. Additional properties MUST be rejected.

#### Scenario: Minimal FSM-form document is valid

- GIVEN a document with the required root fields, one top-level state, and empty `variables`, `events`, and `transitions`
- WHEN the document is validated against HSM JSON v1
- THEN the document is accepted as a valid flat-machine input

#### Scenario: Behavioral metadata is valid

- GIVEN an event declares ordered parameters and a state declares ordered `on_entry` and `on_exit`
- WHEN the document is validated
- THEN the document is accepted without requiring runtime semantics

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

The root `states` array MUST define the top-level state set. A state MAY contain nested `states`, and nesting MAY repeat recursively to form a finite tree. A valid FSM input SHALL be the case where no state contains nested states. The root document MAY declare one root initial transition, and a compound state MAY declare one local initial transition, each with `id` and `target_id`. A local initial target MUST be one of that state's direct children. Shared children, cyclic containment, and multiple initials for the same container MUST NOT be allowed.

#### Scenario: Hierarchical state with local initial is valid

- GIVEN a compound state contains child states and one `initial` targeting a direct child
- WHEN the document is validated
- THEN the hierarchy is accepted as valid HSM JSON v1

#### Scenario: Invalid initial target is rejected

- GIVEN a compound state's `initial.target_id` points outside its child set
- WHEN the document is validated
- THEN the system rejects the document

### Requirement: Deterministic Prepared Render Contract

From one valid HSM JSON v1 document, the system MUST produce one prepared Graphviz document with the same `document_id`, deterministic `dot_source`, and deterministic ordered `highlightable_ids`. State emission order MUST follow authored array order with depth-first traversal. Transition, initial-transition, variable, event, parameter, `on_entry`, and `on_exit` label emission MUST follow authored order. Every rendered state edge or node that participates in workbench highlighting MUST emit the exact authored ID as the Graphviz `id` attribute unchanged.

#### Scenario: Same input yields same prepared output

- GIVEN the same valid HSM JSON v1 document and template version
- WHEN render preparation runs multiple times
- THEN `document_id`, `dot_source`, and `highlightable_ids` are identical across runs

#### Scenario: Workbench IDs remain stable

- GIVEN a state or transition is authored with ID `state_idle` or `edge_start`
- WHEN DOT and SVG are generated
- THEN the downstream workbench still resolves that exact SVG ID

### Requirement: Explicit v1 Boundary

HSM JSON v1 MUST include declarative events, event parameters, machine variables, `on_entry`, `on_exit`, and initial transitions, but MUST NOT include history, orthogonal regions, guards, action execution semantics, event-payload binding semantics, multi-document composition, reverse parsing, runtime execution, editing workflows, or layout-tuning fields. Unsupported constructs MUST be rejected rather than inferred.

#### Scenario: Deferred complex semantics stay out of v1

- GIVEN a document attempts to encode history or orthogonal regions
- WHEN the document is validated
- THEN the system rejects the document as out of scope for HSM JSON v1
