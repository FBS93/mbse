## Exploration: generated-hsm-engine

### Current State
`src/mbse` already has the correct upstream/downstream split for the render pipeline: `mbse.domain.validation.load_hsm_document()` validates HSM JSON v1 into immutable dataclasses, `mbse.application.prepare_hsm_render_view()` lowers that model into a deterministic view, and `mbse.application.build_session()` adapts either HSM JSON or prepared Graphviz into the existing SVG workbench contract.

The important constraint is that the current main spec explicitly allows declarative runtime-shaped metadata (`variables`, `events`, `on_entry`, `on_exit`, initials) while also explicitly excluding runtime execution semantics. So the repo already knows how to PARSE and RENDER runtime-flavored data, but it does not yet define how to EXECUTE it. The smallest safe engine slice is therefore not “full runtime semantics”; it is “generated state-dispatch structure plus a very small handwritten runtime API/kernel.”

### Affected Areas
- `src/mbse/domain/models.py` — current immutable HSM dataclasses are the right generator input boundary.
- `src/mbse/domain/validation.py` — current validation enforces IDs/references/hierarchy, but runtime execution rules are not defined here yet.
- `src/mbse/application/build_session.py` — proves the repo already accepts raw HSM JSON as source-of-truth input without requiring a prepared intermediate file.
- `src/mbse/application/prepare_hsm_render.py` — shows the existing pattern: small Python lowering step before a downstream representation; the generator should mirror this separation.
- `tests/unit/mbse/test_hsm_validation.py` — confirms current JSON v1 intentionally accepts metadata like `on_entry`/`on_exit` without defining executable semantics.
- `tests/integration/test_hsm_json_workbench.py` — locks the existing JSON -> deterministic artifact contract that the engine must preserve as an independent concern.
- `openspec/specs/hsm-json-graphviz-rendering/spec.md` — current source of truth for JSON shape and explicit boundary that runtime execution is out of scope today.

### Approaches
1. **Generated state-functions + tiny handwritten runtime kernel** — generate one Python module from validated HSM JSON where each state is emitted as a function, while a small handwritten runtime owns dispatch flow, current state/path, variable store, and the stable public API.
   - Pros: Matches the requested QPC-style mental model; keeps JSON, generation, and runtime API clearly separated; smallest path that is still genuinely generated; easy to test at generated-artifact and runtime-API levels.
   - Cons: Requires defining a narrow first-pass execution contract, especially for hierarchy and action strings.
   - Effort: Low/Medium

2. **Pure interpreter over the JSON/dataclass model** — keep everything dynamic and execute directly from `HsmDocument` without generating code.
   - Pros: Less codegen machinery up front.
   - Cons: Violates the requested generated-engine shape; weaker fit for C/QPC-like per-state functions; makes later “inspect generated engine” debugging less concrete.
   - Effort: Low

3. **Generate a full rich runtime including action execution DSL** — codegen state functions plus executable semantics for `on_entry`, `on_exit`, transition work, payload binding, and richer tracing.
   - Pros: More complete end state.
   - Cons: This is EXACTLY how teams overbuild slice 1; current JSON spec does not define those semantics yet, so this would force too many decisions at once.
   - Effort: High

### Recommendation
Choose **Generated state-functions + tiny handwritten runtime kernel**.

Smallest controlled first iteration:

- **Source of truth**: keep authored HSM JSON v1 unchanged as the only model input.
- **Generation boundary**: add a generator that consumes validated `HsmDocument` and emits a Python engine module, for example into a generated-runtime area, with:
  - one generated handler function per authored state;
  - generated static indexes for transitions/initial targets/parent links;
  - generated constants for document/state/event IDs.
- **Handwritten runtime boundary**: add a very small runtime layer that owns the required stable API:
  - `init`
  - `set_variable`
  - `get_variable`
  - `send_event`
  - `set_state`
  - `get_state`
  - `get_snapshot`
- **Dispatch model**: `send_event(event_id, **payload)` asks the generated current-state function to handle the event, walking outward through parents when needed for hierarchical fallback.
- **State representation**: runtime stores the current active leaf state ID plus its active ancestry path; `get_state()` returns the leaf state ID, and `get_snapshot()` returns richer inspection data.
- **Initialization**: `init()` resolves root initial and nested local initials deterministically using the already-validated hierarchy.
- **Variables**: first iteration variable semantics stay explicit and boring — values live in the runtime context dictionary and are mutated only through `set_variable()` or explicit runtime internals, not by evaluating JSON strings.
- **Critical scope cut**: treat authored `on_entry` / `on_exit` strings as non-executable metadata in iteration 1. They may be surfaced in generated comments, traces, or snapshot metadata, but MUST NOT be `eval`/`exec`’d. That avoids inventing a DSL or unsafe Python execution before the semantics are designed.
- **`set_state` role**: keep it as a controlled escape hatch for tests/workbench/manual forcing, not as the main transition mechanism.

This split keeps responsibilities clean:

- **JSON** defines machine structure and IDs.
- **Generator** freezes structure into code.
- **Runtime API** provides the only operational surface above generated code.

### Risks
- The current JSON spec deliberately excludes runtime semantics, so proposal/spec work must define the minimal execution contract instead of assuming render metadata is executable behavior.
- If iteration 1 tries to execute `on_entry`/`on_exit` strings, the change will explode into DSL/sandbox/safety design immediately.
- Hierarchical dispatch can get subtle fast; the first slice should constrain itself to one active leaf path, initials, and parent fallback before considering history/orthogonality/guards.
- `set_state` can undermine determinism if treated as a normal business operation rather than a controlled test/inspection hook.

### Ready for Proposal
Yes — propose `generated-hsm-engine` as a small generated-runtime slice that adds code generation plus a handwritten stable API, while explicitly deferring executable action strings, guards, timers, orthogonal regions, and other rich runtime semantics.
