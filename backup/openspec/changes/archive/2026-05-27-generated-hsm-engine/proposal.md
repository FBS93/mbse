# Proposal: Generated HSM Engine

## Intent

Deliver the FIRST executable HSM slice from authored JSON by generating QPC/C-style state functions behind a tiny handwritten runtime API. This proves the JSON can drive execution without expanding into full action-language semantics.

## Scope

### In Scope
- Generate one engine module from validated HSM JSON with one handler function per state plus static parent/initial/transition indexes.
- Add a handwritten stable API exposing only `init`, `set_variable`, `get_variable`, `send_event`, `set_state`, `get_state`, and `get_snapshot`.
- Define minimal execution semantics: deterministic initial resolution, one active leaf path, event dispatch to current state with parent fallback, and context-backed variable storage.

### Out of Scope
- Executing `on_entry`/`on_exit` strings, transition actions, guards, timers, history, orthogonal regions, queues, or async behavior.
- Replacing JSON as source of truth, exposing generated internals as public API, or broad workbench/runtime UX.
- Treating `set_state` as normal business flow rather than a controlled test/inspection hook.

## Capabilities

### New Capabilities
- `generated-hsm-engine`: Generate and run a minimal executable HSM engine from validated JSON through a stable handwritten runtime boundary.

### Modified Capabilities
- `hsm-json-graphviz-rendering`: Narrow the existing boundary so render concerns stay declarative while the same JSON model may also feed a separate runtime capability.

## Approach

Keep the split hard: JSON defines structure, generation freezes structure into code, and handwritten runtime owns execution state and public API. Slice 1 resolves root/local initials, stores current leaf + ancestry path, and dispatches events outward through parents until handled or dropped. Authored `on_entry`/`on_exit` remain inert metadata only; no `eval`/`exec`, no DSL.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/changes/generated-hsm-engine/` | New | Proposal and downstream delta artifacts |
| `openspec/specs/generated-hsm-engine/spec.md` | New | Runtime capability contract |
| `openspec/specs/hsm-json-graphviz-rendering/spec.md` | Modified | Clarify render-only boundary vs new runtime capability |
| `src/mbse/domain/` | Modified | Reuse validated HSM model as generator input |
| `src/mbse/application/` + generated runtime area | Modified | Add generator/runtime boundary without leaking generated internals |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Runtime semantics sprawl past slice 1 | Med | Lock spec to initials, parent fallback, variables, snapshot only |
| Generated/handwritten boundary blurs | Med | Public API lives only in handwritten layer |
| Action strings explode scope | High | Keep `on_entry`/`on_exit` non-executable in v1 |

## Rollback Plan

Remove the generated-engine path and handwritten runtime API additions; keep JSON validation/rendering flow unchanged.

## Dependencies

- Existing validated HSM JSON model remains the only source input.
- Jinja2 MAY be used narrowly for deterministic code generation.

## Success Criteria

- [ ] One JSON document can produce a generated engine plus stable handwritten runtime API.
- [ ] `init` and `send_event` implement deterministic initial resolution and parent-fallback dispatch for one active leaf path.
- [ ] `on_entry`/`on_exit` authored strings remain stored metadata and are not executed in slice 1.
