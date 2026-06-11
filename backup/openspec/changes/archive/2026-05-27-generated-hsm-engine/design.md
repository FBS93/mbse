# Design: Generated HSM Engine

## Technical Approach

Mirror the existing render pipeline: validate JSON into `HsmDocument`, lower it into a deterministic engine view, render one private Python engine module, and wrap that module with a handwritten runtime facade. The generated module freezes structure; the handwritten layer owns state, variables, dispatch flow, inspection, and the only public API. This satisfies the spec while keeping `on_entry`/`on_exit` inert in v1.

## Architecture Decisions

### Decision: Keep generation and execution split

| Option | Tradeoff | Decision |
|---|---|---|
| Interpret `HsmDocument` directly | Less codegen, weaker QPC fit | Rejected |
| Generate private engine + handwritten facade | Slightly more plumbing, clear boundary | Chosen |

**Rationale**: It matches the repo's `prepare_*` + renderer pattern and keeps generated internals off the public surface.

### Decision: Materialize QPC as one function per state

| Option | Tradeoff | Decision |
|---|---|---|
| Giant switch/table dispatcher | Smaller generated file, loses state-function model | Rejected |
| `state_<id>(ctx, event_id)` per state | More emitted functions, explicit and debuggable | Chosen |

**Rationale**: This is the requested QPC/C mental model without dragging in full entry/exit semantics.

### Decision: Runtime owns hierarchical walk

| Option | Tradeoff | Decision |
|---|---|---|
| Generated handlers call parents recursively | More generated coupling | Rejected |
| Runtime walks `active_path` leaf→root | Slight runtime logic, simpler generation | Chosen |

**Rationale**: Minimal hierarchy is easier to test and easier to keep deterministic.

## Data Flow

`HsmDocument` -> `prepare_hsm_engine_view()` -> `render_hsm_engine_source()` -> private module -> `HsmRuntime`

`send_event()` flow:

    active leaf -> generated leaf handler
                -> parent handler (if unhandled)
                -> root handler (if unhandled)
                -> drop event

If a handler returns a transition target, the runtime replaces the active path with:

    target state ancestry + nested local initials until leaf

No `on_entry`/`on_exit`, guard, or action execution runs in this slice.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `src/mbse/domain/models.py` | Modify | Add engine-view and snapshot dataclasses used by generation/runtime. |
| `src/mbse/application/prepare_hsm_engine.py` | Create | Flatten `HsmDocument` into deterministic parents, initials, transition rows, and leaf IDs. |
| `src/mbse/infrastructure/generated_engine.py` | Create | Render/load the generated private engine module in memory. |
| `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` | Create | Jinja template for one function per state plus static indexes. |
| `src/mbse/application/hsm_runtime.py` | Create | Handwritten runtime facade, context, dispatch loop, transition application, and inspection hooks. |
| `src/mbse/application/build_hsm_runtime.py` | Create | Top-level builder from validated JSON/document to `HsmRuntime`. |
| `tests/unit/mbse/test_prepare_hsm_engine.py` | Create | Lock deterministic lowering order and indexes. |
| `tests/unit/mbse/test_hsm_runtime.py` | Create | Cover init, parent fallback, variable access, inert events, and `set_state`. |
| `tests/integration/test_generated_hsm_engine.py` | Create | Prove JSON -> generated engine -> runtime contract end to end. |

## Interfaces / Contracts

```python
@dataclass(frozen=True)
class HsmRuntimeSnapshot:
  state_id: str
  active_path: tuple[str, ...]
  variables: dict[str, object]

class HsmRuntime:
  def init(self) -> None: ...
  def set_variable(self, variable_id: str, value: object) -> None: ...
  def get_variable(self, variable_id: str) -> object | None: ...
  def send_event(self, event_id: str) -> bool: ...
  def set_state(self, state_id: str) -> None: ...
  def get_state(self) -> str: ...
  def get_snapshot(self) -> HsmRuntimeSnapshot: ...
```

Generated module contract:

```python
PARENTS = {"idle_waiting": "idle", "idle": None, "open": None}
INITIAL_TARGETS = {None: "idle", "idle": "idle_waiting"}
LEAF_STATES = frozenset({"idle_waiting", "open"})

def state_idle_waiting(ctx, event_id):
  if event_id == "open_evt":
    return ("transition", "open")
  return ("unhandled", None)
```

`ctx` is a narrow handwritten context object with variable storage only; it does NOT expose `set_state`, so generated code cannot use the inspection hook. `set_state()` validates that the target is a known leaf, recomputes ancestry from `PARENTS`, and never runs actions.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Lowering and generated indexes | Assert depth-first order, parent map, initials, transition buckets. |
| Unit | Runtime semantics | Assert `init`, parent fallback, dropped event, transition resolution, variable reads/writes, and forced-state validation. |
| Integration | Public API only | Build runtime from sample JSON and assert deterministic snapshots without importing generated internals. |

## Migration / Rollout

No migration required.

## Open Questions

- [ ] `send_event` stays `event_id`-only in v1; event parameter binding remains deferred even though event metadata already exists.
