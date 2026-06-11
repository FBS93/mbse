# Design: Runtime Last-Event Semantics

## Technical Approach

Iteration 1 introduces one semantic source of truth: `last_event`. The runtime records the outcome of the latest received event, `get_snapshot()` exposes it, the bridge forwards it, and the viewer accepts it without deriving SVG targets from `executed_activities`. This keeps the slice runtime/viewer-semantic only while preserving existing active-state behavior.

## Architecture Decisions

| Decision | Options | Choice | Rationale |
|---|---|---|---|
| Last-event storage | Reconstruct from variables/history; store explicit runtime record | Store explicit `last_event` on `HsmRuntime` | Minimal, deterministic, and does not depend on side effects or future render layers. |
| Activity payload | Include SVG/render IDs now; emit semantic origins only | Emit ordered `executed_activities` with `activity_id` and `{owner_kind, owner_id}` | Matches the spec boundary and gives iteration 2 enough authored context without leaking render contracts. |
| Compatibility for `last_transition_id` | Remove everywhere now; keep everywhere; keep runtime-only alias | Keep `HsmRuntimeSnapshot.last_transition_id` as a derived deprecated alias from `last_event.transition_path_ids`, but remove it from `RuntimeViewerSnapshot`/bridge JSON | Limits churn inside runtime tests/callers while making the viewer contract semantic immediately. |

## Data Flow

```text
send_event(event_id)
  -> runtime resolves matching candidate on active ancestry
  -> runtime records handled/unhandled + handler metadata
  -> runtime executes exit/activity/entry/initial plans in order
  -> runtime appends ordered executed_activities and taken transition IDs
  -> get_snapshot() returns state + variables + last_event
  -> bridge maps runtime snapshot to viewer snapshot
  -> viewer keeps active state highlighting only; no SVG inference from executed_activities yet
```

Internal transition: `handled=true`, `handler_kind="internal_transition"`, unchanged `active_path`, empty `transition_path_ids`, non-empty `executed_activities` when activities ran.

External transition: `handled=true`, `handler_kind="transition"`, `transition_path_ids` contains only the authored transition plus any nested initial transitions actually descended, in execution order.

Unhandled event: `handled=false`, empty `transition_path_ids`, empty `executed_activities`, previous active state preserved.

## File Changes

| File | Action | Description |
|---|---|---|
| `src/mbse/domain/models.py` | Modify | Add `HsmRuntimeLastEvent`, `HsmExecutedActivity`, and viewer DTO equivalents; keep runtime-only deprecated `last_transition_id` alias. |
| `src/mbse/application/hsm_runtime.py` | Modify | Track per-event semantic outcome, wrap activity execution with origin capture, reset semantics for `init()`/`set_state()`, and derive compatibility transition IDs. |
| `src/mbse/application/web_runtime_bridge.py` | Modify | Map runtime `last_event` into viewer snapshot, preserve `active_ids`, stop emitting viewer `last_transition_id`. |
| `src/mbse/web/static/viewer.js` | Modify | Read `snapshot.last_event` shape but do not derive transition/activity SVG highlights in this iteration. |
| `tests/unit/mbse/test_hsm_runtime.py` | Modify | Cover unhandled events, internal transitions, external transition ordering, and compatibility alias behavior. |
| `tests/unit/mbse/test_web_runtime_bridge.py` | Modify | Lock viewer payload shape and removal of bridge-level `last_transition_id`. |
| `tests/integration/test_mbse_workbench.py` | Modify | Lock server JSON payloads and viewer behavior for semantic snapshots without render inference. |
| `tests/integration/test_generated_hsm_engine.py` | Modify | Update deterministic snapshot assertions to compare `last_event` (and runtime alias only where needed). |

## Interfaces / Contracts

```python
@dataclass(frozen=True)
class HsmExecutedActivity:
  activity_id: str
  owner_kind: str  # state_on_entry | state_on_exit | state_on_initial | transition | internal_transition
  owner_id: str

@dataclass(frozen=True)
class HsmRuntimeLastEvent:
  event_id: str | None
  handled: bool
  handler_kind: str | None
  handler_id: str | None
  transition_path_ids: tuple[str, ...] = ()
  executed_activities: tuple[HsmExecutedActivity, ...] = ()
```

Implementation note: activity origin metadata can be derived from existing plan IDs (`state:{id}:on_entry:{n}`, `transition:{id}:activities:{n}`, etc.), so no render-layer dependency is required.

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Unit | Internal transition semantics | Assert unchanged state, empty `transition_path_ids`, ordered `executed_activities`, `handler_kind="internal_transition"`. |
| Unit | External transition path ordering | Assert authored transition ID precedes nested initial transition IDs. |
| Unit | Unhandled events | Assert `handled=false` and no semantic execution leakage from prior event. |
| Integration | Bridge/session JSON | Assert `last_event` is serialized, viewer payload omits `last_transition_id`, and empty-runtime snapshot still shapes correctly. |
| Integration | Viewer behavior | Assert active-state highlight still works and no transition/activity highlight is inferred from semantic data alone. |

## Migration / Rollout

No data migration required. Roll out as one reviewable slice across runtime DTOs, bridge mapping, viewer payload consumption, and tests.

## Open Questions

- [ ] None blocking for iteration 1.
