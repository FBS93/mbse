# Delta for hsm-json-graphviz-rendering

## MODIFIED Requirements

### Requirement: Explicit v1 Boundary

HSM JSON v1 MUST include declarative events, event parameters, machine variables, `on_entry`, `on_exit`, and initial transitions. This rendering capability MUST treat those fields as declarative model data for validation and deterministic rendering only. The system MUST NOT infer or execute runtime behavior inside this capability. History, orthogonal regions, guards, action execution semantics, event-payload binding semantics, multi-document composition, reverse parsing, editing workflows, and layout-tuning fields MUST remain out of scope here. Unsupported constructs MUST be rejected rather than inferred. The same validated JSON MAY be consumed by a separate runtime capability without expanding this rendering contract.
(Previously: The boundary excluded runtime execution globally instead of narrowing that exclusion to this rendering capability.)

#### Scenario: Deferred complex semantics stay out of v1

- GIVEN a document attempts to encode history or orthogonal regions
- WHEN the document is validated
- THEN the system rejects the document as out of scope for HSM JSON v1

#### Scenario: Render pipeline stays non-executable

- GIVEN a document contains variables, initials, and `on_entry` or `on_exit` strings
- WHEN the document is validated and prepared for rendering
- THEN the capability preserves those fields as declarative data only
- AND no runtime execution semantics are introduced by rendering
