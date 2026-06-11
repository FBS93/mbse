# Design: Web Runtime Bridge

## Technical Approach

Keep the current local web stack (`build session` -> stdlib HTTP server -> static viewer) but move runtime ownership into one explicit in-memory server state object. The server process, not persisted session files, becomes the source of truth for runtime snapshot and viewer metadata. `diagram.svg` remains a file artifact for rendering; runtime snapshot, declared `event_ids`, declared `variable_ids`, and derived `active_ids` are served from memory on every read or mutation.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Server structure | Split file serving from runtime bridge logic behind one server-owned app state | Keep loading `workbench-session.json` inside request handlers | Preserves current web shape while removing file-backed runtime coupling. |
| Runtime location | Keep one `HsmRuntime` instance plus viewer metadata in memory for the life of the Python server | Persist runtime/session state to disk; rebuild from `workbench-session.json` | Matches the mandatory constraint: no session persistence and live Python is the source of truth. |
| Web contract | Serve one snapshot read endpoint plus three narrow mutations: reset/init, send one event, set one variable | Reuse `/api/highlight` for sync; add one generic command endpoint | Small, testable, and prevents protocol creep. |
| Runtime/viewer separation | Add an application-level bridge that translates runtime snapshots into viewer payloads | Put translation/validation directly in `server.py` or inside `HsmRuntime` | Avoids mixing HTTP concerns with engine/runtime semantics. |

## Data Flow

```text
HSM JSON input
  -> build_workbench_session(...)
       writes prepared-document.json + diagram.svg
       returns viewer/session metadata
  -> build_hsm_runtime(hsm_document)
  -> runtime.init()
  -> WorkbenchRuntimeBridge(runtime, metadata)
  -> start_workbench_server(session_dir, app_state)
  -> GET /api/session.json returns svg_url + controls metadata + snapshot
  -> POST mutation returns the same full payload
  -> viewer re-renders controls/result and applies returned active_ids only
```

`active_ids` are derived as the exact `state_id` values present in `runtime.get_snapshot().active_path`, filtered by declared SVG-highlightable IDs. No label lookup, SVG text parsing, or heuristic mapping is allowed.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `src/mbse/application/build_session.py` | Modify | Return enough in-memory viewer metadata for server startup without requiring `workbench-session.json` as runtime input. |
| `src/mbse/application/web_runtime_bridge.py` | Create | Own snapshot serialization, `active_ids` derivation, and narrow mutation methods around `HsmRuntime`. |
| `src/mbse/domain/models.py` | Modify | Add viewer/runtime payload types for snapshot, controls metadata, and server app state inputs. |
| `src/mbse/infrastructure/session_store.py` | Modify | Keep artifact persistence bounded to render artifacts; any JSON session file becomes optional/read-only, not authoritative. |
| `src/mbse/web/server.py` | Modify | Accept injected in-memory app state, expose snapshot/mutation endpoints, and keep static asset serving separate from runtime actions. |
| `src/mbse/web/static/index.html` | Modify | Preserve current layout while replacing manual-only controls with minimal reset/event/variable controls and snapshot output. |
| `src/mbse/web/static/viewer.js` | Modify | Load server-owned snapshot/metadata, call narrow mutation endpoints, and apply returned `active_ids`. |
| `src/mbse/cli/main.py` | Modify | Build runtime-backed app state before starting the server. |

## Interfaces / Contracts

```python
@dataclass(frozen=True)
class RuntimeViewerSnapshot:
  state_id: str
  active_path: tuple[str, ...]
  active_ids: tuple[str, ...]
  variables: dict[str, object]

@dataclass(frozen=True)
class RuntimeViewerSession:
  document_id: str
  svg_url: str
  event_ids: tuple[str, ...]
  variable_ids: tuple[str, ...]
  snapshot: RuntimeViewerSnapshot
```

HTTP shape:

- `GET /api/session.json` -> `RuntimeViewerSession`
- `POST /api/runtime/reset` -> `RuntimeViewerSession`
- `POST /api/runtime/events` body `{ "event_id": string }`
- `POST /api/runtime/variables` body `{ "variable_id": string, "value": json }`

Mutations should reject unknown declared IDs with `400` rather than silently writing arbitrary viewer input.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit | Bridge snapshot mapping | Assert `active_path` -> exact `active_ids`, preserving backend-only derivation. |
| Unit | Mutation validation | Reject unknown `event_id` / `variable_id`; reset rebuilds initial snapshot. |
| Integration | CLI/server wiring | Start workbench from HSM JSON and assert snapshot endpoint works without reading runtime state from persisted session JSON. |
| Integration | Viewer API contract | Assert each mutation returns the full session payload used for re-render. |

## Migration / Rollout

No migration required. This is a bounded extension of the existing workbench slice.

## Open Questions

- [ ] Whether `workbench-session.json` should remain emitted for backward compatibility or be dropped immediately once tests are updated.
