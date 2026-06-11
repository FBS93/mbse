# Proposal: HSM JSON Graphviz Rendering

## Intent

Define a small, deterministic slice that turns one product-owned HSM JSON v1 document into Graphviz SVG for the existing workbench pipeline. The JSON Schema/model document is the source of truth, so this slice must lock the HSM shape before adding richer behavior.

## Scope

### In Scope
- Define HSM JSON v1 structure and JSON Schema as the canonical contract.
- Validate one HSM JSON document, then render deterministic DOT through one Jinja2 template.
- Produce Graphviz-ready output that preserves stable authored IDs for downstream SVG/workbench use.

### Out of Scope
- Runtime execution, simulation, synchronization, or editing workflows.
- Advanced HSM semantics, compiler layers, or broad preprocessing beyond minimal render support.
- Multi-document inputs, reverse parsing, or workbench feature expansion.

## Capabilities

### New Capabilities
- `hsm-json-graphviz-rendering`: Define, validate, and render one HSM JSON v1 document into deterministic DOT/SVG-ready output for the existing workbench flow.

### Modified Capabilities
- None.

## Approach

Use the simplest safe path: `JSON HSM -> minimal preprocessing -> Jinja2 DOT -> Graphviz SVG -> workbench`. Keep JSON direct-to-template by default; allow only thin preparation for stable ordering, computed IDs, and values the template should not recompute. Put hierarchy/rendering constraints in the schema/model contract early so the template stays dumb and deterministic.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/changes/hsm-json-graphviz-rendering/` | New | Proposal/spec/design/tasks for this slice |
| `openspec/specs/hsm-json-graphviz-rendering/spec.md` | New | Source-of-truth capability for HSM JSON v1 and render contract |
| `src/mbse/domain/` | Modified | Add HSM JSON validation/model boundary |
| `src/mbse/application/` | Modified | Adapt HSM input into existing prepared Graphviz document flow |
| `src/mbse/infrastructure/` | Modified | Add DOT template/render support while reusing Graphviz runner |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Schema leaves identity ambiguous | Med | Define stable ID and naming rules in v1 |
| Template logic grows too smart | Med | Limit preprocessing and reject unsupported semantics early |
| Hierarchy semantics expand prematurely | Med | Keep v1 to render-only structure, defer runtime meaning |

## Rollback Plan

Remove the HSM JSON adapter and template path, then continue using the existing prepared Graphviz input flow unchanged.

## Dependencies

- Existing `graphviz-svg-workbench` contract remains intact.
- Jinja2 added narrowly for DOT templating.

## Success Criteria

- [ ] One HSM JSON v1 schema/model contract is defined as the authoritative input.
- [ ] The same valid JSON produces deterministic DOT and stable authored IDs across runs.
- [ ] Generated output can feed the existing Graphviz SVG workbench flow without changing its visual ID contract.
