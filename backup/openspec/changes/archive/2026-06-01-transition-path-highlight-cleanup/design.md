# Design: Transition Path Highlight Cleanup

## Technical Approach

Change the runtime snapshot contract in place so `last_transition_id` always represents the full ordered transition path for the latest resolution. The runtime becomes the only producer of that ordered tuple, the backend bridge filters the tuple member-by-member against exact SVG IDs, and the viewer applies highlight classes to every returned transition while keeping active-state emphasis on borders only. This follows the existing repository structure: Python dataclasses define the contract, bridge code serializes it, and static viewer assets consume it directly.

## Architecture Decisions

| Decision | Options | Choice | Rationale |
|---|---|---|---|
| Runtime history shape | Keep scalar final ID; add new field; replace with tuple | Replace `last_transition_id` with `tuple[str, ...]` | Matches user constraint: no compatibility path and no new field. Keeps one source of truth. |
| Initial descent accumulation | Track only final nested initial; append all taken transitions | Append every taken transition in execution order | Needed so `init()` and event resolutions expose the full path, not just the leaf-entering tail. |
| Bridge filtering | Filter whole field once; filter each member | Filter each tuple member by exact equality | Preserves valid IDs, drops missing ones, and matches the spec’s partial-path behavior. |
| Viewer highlight behavior | Highlight one transition; highlight all returned IDs | Highlight all returned IDs | Keeps frontend dumb and faithful to backend ordering/selection. |
| Active state styling | Border + fill; border only | Border only | Matches the requested visual cleanup and avoids competing with transition emphasis. |

## Data Flow

```text
init()/send_event()
  -> HsmRuntime builds ordered tuple of executed transition IDs
  -> HsmRuntimeSnapshot.last_transition_id: tuple[str, ...]
  -> WorkbenchRuntimeBridge filters each ID against highlightable_ids
  -> RuntimeViewerSnapshot.last_transition_id: tuple[str, ...]
  -> JSON response serializes tuple as array
  -> viewer.js applies transition class to every returned ID
```

Runtime accumulation rules:

- `init()`: start with the root initial transition ID (if present), then append each nested initial transition encountered by `_descend_initials()` until the active leaf is reached.
- `send_event()`: start with the explicit event transition ID, then append nested initials entered after the target state when `should_descend_initials` is true.
- `set_state()` and snapshots after no taken transition use `()`.

Implementation fit:

- `_descend_initials()` should stop returning only the last ID and instead return `(leaf_state_id, transition_ids)`.
- `_execute_transition()` should return `(active_path, transition_ids)`.
- `send_event()` should preserve the previous tuple when dispatch returns `False`, because the latest successful resolution has not changed.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `src/mbse/domain/models.py` | Modify | Change runtime/viewer snapshot dataclasses so `last_transition_id` is `tuple[str, ...]` with empty-tuple defaults. |
| `src/mbse/application/hsm_runtime.py` | Modify | Accumulate ordered transition tuples for `init()` and `send_event()`, and clear to `()` on `set_state()`. |
| `src/mbse/application/web_runtime_bridge.py` | Modify | Filter transition IDs member-by-member and serialize only surviving exact matches. |
| `src/mbse/web/static/viewer.js` | Modify | Treat `last_transition_id` as an array and apply highlights to all returned IDs. |
| `src/mbse/web/static/viewer.css` | Modify | Remove active-state fill intensification; keep border-only state highlight and transition edge/arrowhead styling. |
| `tests/unit/mbse/test_hsm_runtime.py` | Modify | Update runtime assertions to ordered tuples, especially init chains and event+initial chains. |
| `tests/unit/mbse/test_web_runtime_bridge.py` | Modify | Update bridge assertions for tuple filtering and empty-tuple behavior. |
| `tests/integration/test_generated_hsm_engine.py` | Modify | Lock deterministic tuple snapshots across parity runs. |
| `tests/integration/test_mbse_workbench.py` | Modify | Update JSON payloads, viewer harness expectations, and multi-transition highlight cases. |

## Interfaces / Contracts

```python
@dataclass(frozen=True)
class HsmRuntimeSnapshot:
  last_transition_id: tuple[str, ...] = ()

@dataclass(frozen=True)
class RuntimeViewerSnapshot:
  last_transition_id: tuple[str, ...] = ()
```

Breaking contract: models, bridge payloads, fixture payloads, and tests MUST stop treating `last_transition_id` as `str | None`. JSON now emits `[]` or `[`...`]` only.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Runtime tuple accumulation | Assert `init()`, direct events, event+initial chains, self-transitions, and `set_state()` clearing. |
| Unit | Bridge filtering | Assert exact-ID filtering preserves order and drops unmatched members without scalar fallback. |
| Integration | Generated engine parity | Re-record expected snapshot tuples for the deterministic transition sequence. |
| Integration | Workbench/viewer contract | Assert session JSON arrays, multi-ID transition highlight application, and border-only state styling hooks. |

## Migration / Rollout

No phased rollout. This is a deliberate breaking change applied in one iteration across runtime, bridge, viewer, fixtures, and tests with no backward compatibility.

## Open Questions

- [ ] None.
