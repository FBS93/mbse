# Design: HSM Executable Activities And Guards

## Technical Approach

Extend the existing generated-engine pipeline instead of adding a second interpreter. The HSM document stays declarative: every state MAY define optional lifecycle slots `on_initial`, `on_entry`, and `on_exit`; initial transitions MAY define ordered `activities`; event reception in a state is authored as either an `internal transition` (activities only, no state change) or a normal `transition` (optional guard, ordered activities, explicit target). At runtime build, callable references are validated and resolved once, then the runtime executes them in `example_hsm` order while keeping the public `build_hsm_runtime()` / `send_event()` API unchanged.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Behavior model shape | Keep lifecycle slots on `HsmState` as optional tuples; add `activities` to `HsmInitialTransition`; model event reception as separate `HsmInternalTransition` and `HsmTransition` records | Put all behavior on one flat transition shape with optional target | Matches the user clarification exactly and removes the target-required mismatch for internal behavior. |
| Callable references | Store `{module, name}` callable refs in schema/model; reject raw strings | Inline Python, global registry keys | Importable refs are inspectable, serializable, and safe enough for v1 without embedding code. |
| Resolution point | Resolve/import all refs during `build_hsm_runtime()` / generated-engine load, not lazily on first event | Lazy import on dispatch | Fails deterministically before execution and keeps runtime dispatch simple. |
| Generated metadata | Replace `event_transition_ids_by_state_id` / one-event-one-target assumptions with ordered candidate lists per state/event across both internal and external transitions | Keep current single-target map | Guards plus first-class internal transitions require ordered candidates and “guard false means bubble/continue”, which the current map cannot represent. |

## Data Flow

Author JSON → `validation.py` / schema → `models.py` document (`transitions` + `internal_transitions`) → `prepare_hsm_engine.py` metadata + resolved callable plans → generated module wrapper → `HsmRuntime`

Runtime rules:
- `init()`: enter root target, run its `on_entry`, then for each newly active compound state run `on_initial`, initial-transition `activities`, child `on_entry`, repeating until a leaf is reached.
- Event with no transition: search leaf→root. If a state has matching candidates, evaluate them in the authored collection order between `internal_transitions` and `transitions`, preserving declaration order inside each collection. A matching internal transition handles the event by running its activities and leaving the active leaf unchanged. For external transitions, the first guard that passes handles the event and selects the explicit target.
- Guard false: treat that candidate as unhandled and continue with the next candidate or ancestor.
- Transition: execute exits from current leaf up to but excluding the handling source, then remaining exit path up to but excluding the LCA, then event `activities`, then entry path down to the explicit target, then nested initial resolution for each newly active compound target.
- Self target re-enters the source. Ancestor target does not re-enter the ancestor. Descendant target does not exit the ancestor source.

## File Changes

| File | Action | Description |
|---|---|---|
| `src/mbse/domain/hsm_schema_v1.json` | Modify | Add callable-ref definition plus optional lifecycle fields, external transition behavior, and first-class `internal_transitions`. |
| `src/mbse/domain/models.py` | Modify | Introduce callable-ref/value objects plus distinct initial/internal/external transition rows. |
| `src/mbse/domain/validation.py` | Modify | Parse optional lifecycle slots, initial/internal/external activities, guards, and surface import/shape errors clearly. |
| `src/mbse/application/prepare_hsm_engine.py` | Modify | Build ordered candidate metadata and resolved callable plans. |
| `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` | Modify | Emit ordered candidate lists instead of simple event→target handlers. |
| `src/mbse/infrastructure/generated_engine.py` | Modify | Load generated metadata and expose resolved handlers/guards to runtime. |
| `src/mbse/application/hsm_runtime.py` | Modify | Execute activities/guards with `example_hsm` ordering and mutable ctx. |
| `tests/unit/mbse/test_*.py` | Modify | Replace inertness expectations with ordering/guard parity coverage. |

## Interfaces / Contracts

- `ctx` remains one live mutable runtime object shared by guards and activities for the whole instance. Expose `ctx.variables` as today and add read-only event payload access for the current dispatch (`event_id`, params) during guard/activity invocation.
- Guard contract: callable `(ctx) -> bool`; SHOULD be side-effect free.
- Activity contract: callable `(ctx) -> None`.
- Resolution/import failures and bad signatures raise `ValidationError` during document load when structural, or `ValueError`/dedicated runtime-build error during `build_hsm_runtime()` when importable refs cannot be resolved.

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Unit | Schema/validation for optional slots, callable refs, bad refs, inline-string rejection, and internal-vs-external transition shape rules | `test_validation.py`, `test_hsm_validation.py` |
| Unit | Metadata preserves candidate order, lifecycle plans, nested initials, and internal/external candidate separation | `test_prepare_hsm_engine.py`, `test_generated_engine.py` |
| Integration | Runtime ordering for init, handled-no-transition, guard bubbling, self/ancestor/descendant, nested initials | `test_hsm_runtime.py` trace assertions using spy callables |

## Migration / Rollout

No migration required. This is a chained delivery change because 400-line risk is high: (1) schema/models/validation, (2) engine metadata generation, (3) runtime execution ordering, (4) parity tests/docs.

## Open Questions

- [x] Resolved: preserve the payload's authored collection order between `internal_transitions` and `transitions`, while keeping declaration order inside each collection.
