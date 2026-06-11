# Design: Runtime HSM Core Parity

## Technical Approach

Keep `HsmRuntime` as the public execution boundary and port the C core algorithm at the semantic level only. The runtime will split transition handling into four explicit helpers: transition-source lookup, transition-path/LCA computation, transition execution, and nested initial descent. Prepared/generated metadata will expand so those helpers can reason about ancestry and transition identity without importing C-only reserved signals, fixed buffers, or AO mechanics.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Runtime shape | Add private parity helpers inside `HsmRuntime`; keep public methods unchanged | Replace runtime with generated algorithm, or expose new public inspection APIs | Preserves the stable handwritten API while making parity logic explicit and testable. |
| Metadata contract | Generate parent/ancestry and event-transition descriptors, including transition IDs and explicit targets | Keep only `event_id -> target_id` maps and infer everything during dispatch | Current metadata cannot identify the state that handled the event or compute trimmed exit/entry paths. |
| Python adaptation boundary | Mirror C semantics, not C mechanics | Emulate reserved signals / fixed-depth arrays exactly | The user explicitly wants host-PC Python behavior with semantic parity, not embedded implementation baggage. |

## Data Flow

```text
HSM document
  -> prepare_hsm_engine_view()
     emits parent + ancestry + transition descriptors
  -> load_generated_engine()
     exposes handlers and runtime metadata
  -> HsmRuntime.send_event()
     find_transition_source()
     -> compute_transition_path()
     -> execute_transition()
     -> descend_nested_initials()
  -> snapshot/public API
```

Dispatch flow:
1. Start from the active leaf and call generated handlers outward until one returns a transition.
2. Treat the handler state as the transition source and the authored target as the explicit target.
3. Compute `exit_path` from current leaf up to source, then extend to the LCA boundary; compute `entry_path` from LCA down to target.
4. Apply exit order leaf-up, entry order ancestor-down, then repeatedly follow nested initials below the target until the final leaf is reached.

## File Changes

| File | Action | Description |
|---|---|---|
| `openspec/changes/runtime-hsm-core-parity/design.md` | Create | Design artifact for parity implementation |
| `src/mbse/application/hsm_runtime.py` | Modify | Refactor `init`/`send_event` around explicit parity helpers |
| `src/mbse/application/prepare_hsm_engine.py` | Modify | Prepare richer runtime metadata for ancestry and transition lookup |
| `src/mbse/domain/models.py` | Modify | Extend prepared-engine dataclasses for parity metadata |
| `src/mbse/infrastructure/generated_engine.py` | Modify | Preserve new metadata on the wrapper without widening the public runtime API |
| `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` | Modify | Emit transition descriptors/lookup tables consumed by the runtime |
| `tests/unit/mbse/test_prepare_hsm_engine.py` | Modify | Assert prepared metadata shape and ancestry facts |
| `tests/unit/mbse/test_generated_engine.py` | Modify | Assert generated wrapper exposes parity metadata and handler behavior |
| `tests/unit/mbse/test_hsm_runtime.py` | Modify | Add parity cases for start, self, ancestor, descendant, cross-branch, inert events |
| `tests/integration/test_generated_hsm_engine.py` | Modify | Replay parity-oriented event sequences through the public API |

## Interfaces / Contracts

```python
@dataclass(frozen=True)
class HsmPreparedEngineTransitionRow:
  transition_id: str
  event_id: str
  source_id: str
  target_id: str

@dataclass(frozen=True)
class HsmPreparedEngineView:
  parent_ids: dict[str, str | None]
  ancestry_by_state_id: dict[str, tuple[str, ...]]
  initial_target_ids: dict[str | None, str]
  initial_transition_ids: dict[str | None, str]
  transition_rows_by_state_id: dict[str, tuple[HsmPreparedEngineTransitionRow, ...]]
```

`GeneratedEngine` should carry the same metadata plus a fast `event_transition_ids_by_state_id` index. `HsmRuntime` private helpers should look like `_find_transition_source(event_id)`, `_compute_transition_path(source_id, target_id)`, `_execute_transition(path, transition_id)`, and `_descend_initials(state_id, transition_id)`.

Why this metadata matters: parent/ancestry data gives LCA trimming; transition IDs preserve snapshot parity; source-aware transition rows distinguish “current leaf exited” from “ancestor handled”; initial-transition maps let runtime continue from explicit targets into nested local initials deterministically.

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Unit | Metadata preparation | Add assertions for ancestry, initial maps, and transition descriptors from fixture machines mirroring the C topology |
| Unit | Runtime parity helpers | Drive `init()`/`send_event()` through self, ancestor-target, descendant-target, same-branch, cross-branch, and unhandled-event cases; assert final leaf, active path, and last transition ID |
| Integration | Stable API + deterministic replay | Use `build_hsm_runtime()` only, replay reference-style sequences, and verify equal snapshots across runs |

## Migration / Rollout

No migration required. Public runtime methods remain stable; only internal runtime/engine contracts change.

## Open Questions

- [ ] Whether `set_state()` should remain leaf-only or also accept compound states for parity fixtures; current design keeps leaf-only unless tests prove a blocker.
