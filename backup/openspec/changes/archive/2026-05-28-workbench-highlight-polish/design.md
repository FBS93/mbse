# Design: Workbench Highlight Polish Slice B

## Technical Approach

Keep the current backend-owned highlight contract and change only the snapshot metadata the viewer already consumes. `active_path` stays for observability, `active_ids` becomes leaf-only, and the backend adds one optional `last_transition_id` for the exact SVG edge that most recently led into the active leaf. The frontend keeps exact-ID lookup, applies two CSS classes, and does not inspect labels or SVG internals.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Highlight source of truth | Backend emits leaf-only `active_ids` plus optional `last_transition_id` | Let frontend infer parent/transition highlight from `active_path` | Transition IDs cannot be derived reliably in the browser, especially for nested initial entry. Keep semantics centralized in Python. |
| Nested initialization semantics | `last_transition_id` is the FINAL transition into the resolved active leaf | Highlight the first transition (`machine_init` / event transition), or multiple transitions | Matches the proposal/spec and avoids dual/high-noise highlighting during compound entry. |
| Frontend styling | Separate classes for state and transition highlight on existing SVG IDs only | Rework SVG structure or add DOM wrappers | Preserves the current exact-ID contract and stays inside Slice B. |

## Data Flow

```text
HSM document
  -> prepare_hsm_engine_view()
     adds initial-transition metadata
  -> GeneratedEngine wrapper
     keeps initial-transition and event-transition lookup tables
  -> HsmRuntime
     resolves active leaf + final transition id
  -> WorkbenchRuntimeBridge
     filters to exact SVG ids and serializes snapshot
  -> viewer.js
     adds state/transition classes
```

Nested init/reset resolution:

1. Start with the explicit transition that entered the target (`None -> root`, or an event transition).
2. Follow engine initial targets until a leaf is reached.
3. Each time an initial transition is followed, replace the remembered transition id.
4. Serialize the leaf ancestry as `active_path`, the leaf only as `active_ids`, and the remembered id as `last_transition_id`.

That means `machine_init -> parent -> parent_init -> child_a` highlights `parent_init`, and `open_to_idle -> idle_init -> idle_waiting` highlights `idle_init`.

## File Changes

| File | Action | Description |
|---|---|---|
| `openspec/changes/workbench-highlight-polish/design.md` | Create | Slice B design artifact |
| `src/mbse/domain/models.py` | Modify | Add optional `last_transition_id` to runtime/viewer snapshot types and initial-transition metadata to prepared engine view / generated engine wrapper types |
| `src/mbse/application/prepare_hsm_engine.py` | Modify | Collect `initial_transition_ids` keyed by source state (`None` for root) |
| `src/mbse/infrastructure/generated_engine.py` | Modify | Preserve lookup metadata needed by runtime without changing SVG/render pipeline |
| `src/mbse/application/hsm_runtime.py` | Modify | Track final transition into resolved leaf on init/reset and event dispatch |
| `src/mbse/application/web_runtime_bridge.py` | Modify | Emit leaf-only `active_ids` and pass through filtered `last_transition_id` |
| `src/mbse/web/static/viewer.js` | Modify | Clear/apply separate state and transition classes from snapshot data |
| `src/mbse/web/static/viewer.css` | Modify | Soften state highlight and define distinct transition highlight |
| `tests/unit/mbse/test_prepare_hsm_engine.py` | Modify | Assert initial-transition metadata |
| `tests/unit/mbse/test_generated_engine.py` | Modify | Assert generated wrapper preserves lookup metadata |
| `tests/unit/mbse/test_hsm_runtime.py` | Modify | Assert final-transition behavior for init and compound re-entry |
| `tests/unit/mbse/test_web_runtime_bridge.py` | Modify | Assert leaf-only `active_ids` and filtered `last_transition_id` |
| `tests/integration/test_mbse_workbench.py` | Modify | Assert JSON contract, JS/CSS class usage, and browser behavior |
| `tests/support/viewer_browser_harness.py` | Modify | Expose applied SVG classes so frontend tests can distinguish state vs transition highlight |

## Interfaces / Contracts

```python
@dataclass(frozen=True)
class RuntimeViewerSnapshot:
  state_id: str
  active_path: tuple[str, ...]
  active_ids: tuple[str, ...]           # leaf-only
  last_transition_id: str | None = None
  variables: dict[str, object]
```

`HsmRuntimeSnapshot` gets the same optional field. Engine metadata adds `initial_transition_ids: dict[str | None, str]`.

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Unit | Nested init chooses final transition | Extend runtime/engine tests with compound-entry fixtures |
| Unit | Bridge contract stays exact-ID and leaf-only | Update snapshot serialization assertions |
| Integration | Viewer applies distinct classes with no extra endpoints | Extend browser harness snapshot + workbench tests |

## Migration / Rollout

No migration required.

## Open Questions

- [ ] None blocked for Slice B.
