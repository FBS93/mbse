# Tasks: Web Runtime Bridge

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 420-520 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 backend bridge -> PR 2 HTTP wiring -> PR 3 viewer + batch verify |
| Delivery strategy | chained by explicit user decision |
| Chain strategy | stacked-to-main |

Decision needed before apply: Resolved
Chained PRs recommended: Yes
Chain strategy: stacked-to-main
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Backend bridge state and no-file session contract | PR 1 | Base slice; remove `workbench-session.json` writes/reads |
| 2 | Server + CLI runtime endpoints | PR 2 | Depends on PR 1; keep HTTP separate from runtime bridge |
| 3 | Viewer wiring and final verification batch | PR 3 | Depends on PR 2; no visual redesign |

## Phase 1: Foundation

- [x] 1.1 RED: add `tests/integration/test_mbse_session_build.py` coverage proving `build_workbench_session()` no longer emits `workbench-session.json` and still writes `prepared-document.json` + `diagram.svg`.
- [x] 1.2 Modify `src/mbse/domain/models.py` to replace `WorkbenchSession` usage with runtime-viewer payload/app-state dataclasses for metadata, snapshot, and declared IDs.
- [x] 1.3 Modify `src/mbse/application/build_session.py` and `src/mbse/infrastructure/session_store.py` so session build returns in-memory metadata and persists render artifacts only.

## Phase 2: Runtime Bridge

- [x] 2.1 RED: add `tests/unit/mbse/test_web_runtime_bridge.py` for exact `active_path` -> `active_ids`, unknown `event_id` / `variable_id` rejection, and reset rebuilding the initial snapshot.
- [x] 2.2 Create `src/mbse/application/web_runtime_bridge.py` to own snapshot serialization, declared-ID validation, reset/init, `send_event`, and `set_variable` around `HsmRuntime`.
- [x] 2.3 REFACTOR: remove obsolete highlight-only flow in `src/mbse/application/highlight.py` and update imports/callers so runtime bridge is the only viewer-state source.

## Phase 3: Server and Viewer Wiring

- [x] 3.1 RED: update `tests/integration/test_mbse_workbench.py` and `tests/unit/mbse/test_cli_main.py` for injected app state, `/api/session.json`, `/api/runtime/reset`, `/api/runtime/events`, and `/api/runtime/variables` without reading persisted session JSON.
- [x] 3.2 Modify `src/mbse/web/server.py` and `src/mbse/cli/main.py` to build/inject one in-memory app state, keep static file serving separate, and return full session payload on every mutation.
- [x] 3.3 Modify `src/mbse/web/static/index.html` and `src/mbse/web/static/viewer.js` to replace manual highlight input with minimal reset/event/variable controls, backend snapshot rendering, and exact-ID highlight refresh only.

## Phase 4: Batch Verification

- [x] 4.1 Run unit batch: `pytest tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_web_runtime_bridge.py tests/unit/mbse/test_cli_main.py`.
- [x] 4.2 Run integration batch: `pytest tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py tests/integration/test_hsm_json_workbench.py`.
- [x] 4.3 Cleanup assertions/docs in touched tests and code comments to confirm no event parameters, no visual redesign, and no `workbench-session.json` references remain.
