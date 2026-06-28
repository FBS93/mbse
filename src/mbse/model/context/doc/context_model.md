# Context Model

This package defines the JSON authoring format for shared context models and exposes read-only structural queries over validated model data.

## Document shape

A context model document contains:

- `schema_version`: must be `mbse-context-model-v0`.
- `document_id`: stable identifier for the context document.
- `enums`: shared reusable enumerations.
- `variables`: shared typed runtime variables with default values.
