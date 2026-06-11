# Apply Progress: web-runtime-bridge

## Scope

- Delivery mode: chained PR slice
- Chain strategy: stacked-to-main
- Current work unit: Work Unit 3 / viewer wiring + final verification batch
- Boundary: replace the legacy manual highlight UI with backend-owned runtime controls, verify the scoped unit/integration batches, and close the slice without expanding into event parameters or UI redesign
- Previous work units: Work Unit 1 / backend bridge state and no-file session contract; Work Unit 2 / server + CLI runtime endpoints
- Follow-up batch: None
- Follow-up boundary: Verify phase only

## Completed Tasks

- [x] 1.1 RED: add `tests/integration/test_mbse_session_build.py` coverage proving `build_workbench_session()` no longer emits `workbench-session.json` and still writes `prepared-document.json` + `diagram.svg`.
- [x] 1.2 Modify `src/mbse/domain/models.py` to replace `WorkbenchSession` usage with runtime-viewer payload/app-state dataclasses for metadata, snapshot, and declared IDs.
- [x] 1.3 Modify `src/mbse/application/build_session.py` and `src/mbse/infrastructure/session_store.py` so session build returns in-memory metadata and persists render artifacts only.
- [x] 2.1 RED: add `tests/unit/mbse/test_web_runtime_bridge.py` for exact `active_path` -> `active_ids`, unknown `event_id` / `variable_id` rejection, and reset rebuilding the initial snapshot.
- [x] 2.2 Create `src/mbse/application/web_runtime_bridge.py` to own snapshot serialization, declared-ID validation, reset/init, `send_event`, and `set_variable` around `HsmRuntime`.
- [x] 2.3 REFACTOR: remove obsolete highlight-only flow in `src/mbse/application/highlight.py` and update imports/callers so runtime bridge is the only viewer-state source.
- [x] 3.1 RED: update `tests/integration/test_mbse_workbench.py` and `tests/unit/mbse/test_cli_main.py` for injected app state, `/api/session.json`, `/api/runtime/reset`, `/api/runtime/events`, and `/api/runtime/variables` without reading persisted session JSON.
- [x] 3.2 Modify `src/mbse/web/server.py` and `src/mbse/cli/main.py` to build/inject one in-memory app state, keep static file serving separate, and return full session payload on every mutation.
- [x] 3.3 Modify `src/mbse/web/static/index.html` and `src/mbse/web/static/viewer.js` to replace manual highlight input with minimal reset/event/variable controls, backend snapshot rendering, and exact-ID highlight refresh only.
- [x] 4.1 Run unit batch: `pytest tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_web_runtime_bridge.py tests/unit/mbse/test_cli_main.py`.
- [x] 4.2 Run integration batch: `pytest tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py tests/integration/test_hsm_json_workbench.py`.
- [x] 4.3 Cleanup assertions/docs in touched tests and code comments to confirm no event parameters, no visual redesign, and no `workbench-session.json` references remain.

## Remaining Tasks

- None.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 | `tests/integration/test_mbse_session_build.py` | Integration | ✅ `pytest tests/integration/test_mbse_session_build.py tests/integration/test_hsm_json_workbench.py tests/unit/mbse/test_highlight.py` passed `8 passed` before changing shared session artifacts | ✅ `pytest tests/integration/test_mbse_session_build.py tests/integration/test_hsm_json_workbench.py` failed during collection with `ImportError: cannot import name 'WorkbenchAppState'` after the test was written first | ✅ `pytest tests/integration/test_mbse_session_build.py tests/integration/test_hsm_json_workbench.py` passed `6 passed` after removing the persisted session file contract | ✅ Prepared-document input proves render artifacts still exist while HSM JSON input proves declared `event_ids` and `variable_ids` are carried in returned metadata | ➖ None needed |
| 1.2 | `tests/integration/test_mbse_session_build.py` | Integration | ✅ Same `8 passed` safety net protected the shared model contract before extension | ✅ Same RED import failure proved the runtime app-state dataclass contract did not exist before implementation | ✅ Same targeted command passed `6 passed` after adding app-state + runtime-viewer dataclasses | ✅ The two exercised inputs force empty declared IDs for prepared docs and non-empty declared IDs for HSM JSON | ➖ None needed |
| 1.3 | `tests/integration/test_mbse_session_build.py` | Integration | ✅ Same `8 passed` safety net protected `build_session.py` and `session_store.py` before modification | ✅ Same RED failure proved the new in-memory contract was missing before build/session-store changes | ✅ `pytest tests/integration/test_mbse_session_build.py tests/integration/test_hsm_json_workbench.py tests/unit/mbse/test_highlight.py` passed `8 passed` after persisting render artifacts only | ✅ Assertions cover two code paths: prepared input preserves the original prepared artifact, and HSM input regenerates prepared output while exposing declared IDs in memory | ✅ Removed unused persisted-session serialization from `session_store.py` and kept helper outputs narrow |
| 2.1 | `tests/unit/mbse/test_web_runtime_bridge.py` | Unit | N/A (new) | ✅ `pytest tests/unit/mbse/test_web_runtime_bridge.py` failed during collection with `ModuleNotFoundError: No module named 'mbse.application.web_runtime_bridge'` after the test was written first | ✅ `pytest tests/unit/mbse/test_web_runtime_bridge.py` passed `4 passed` after adding the bridge module | ✅ Covered both full-path and filtered-path `active_ids`, plus mutation/reset paths with distinct outcomes | ➖ None needed |
| 2.2 | `tests/unit/mbse/test_web_runtime_bridge.py` | Unit | N/A (new) | ✅ Same RED collection failure proved the runtime bridge contract did not exist before implementation | ✅ Same targeted command passed `4 passed` after adding snapshot serialization, ID validation, and reset/init behavior | ✅ Event dispatch, variable mutation, and reset all execute different code paths against one backend-owned runtime wrapper | ✅ Kept bridge API narrow around session/read/reset/event/variable operations |
| 2.3 | `tests/integration/test_mbse_workbench.py`, `tests/unit/mbse/test_cli_main.py` | Integration + Unit | ⚠️ `pytest tests/integration/test_mbse_workbench.py tests/unit/mbse/test_cli_main.py tests/unit/mbse/test_highlight.py tests/unit/mbse/test_hsm_runtime.py` reported one pre-existing failure because the old workbench test still expected `workbench-session.json` after Work Unit 1 removed it | ✅ Rewriting the workbench/CLI tests to the runtime-endpoint contract created failing assertions for injected runtime state and endpoint wiring before production changes | ✅ `pytest tests/unit/mbse/test_web_runtime_bridge.py tests/integration/test_mbse_workbench.py tests/unit/mbse/test_cli_main.py` passed `11 passed` after removing highlight-only wiring and injecting the runtime bridge | ✅ Triangulated across server endpoint success paths, 400 rejection for unknown IDs, and CLI injection behavior | ✅ Deleted obsolete highlight-only module/tests and removed legacy model exports |
| 3.1 | `tests/integration/test_mbse_workbench.py`, `tests/unit/mbse/test_cli_main.py` | Integration + Unit | ⚠️ Same pre-existing failure above identified the stale session-file expectations that had to be replaced in this slice | ✅ `pytest tests/integration/test_mbse_workbench.py tests/unit/mbse/test_cli_main.py` failed `5 failed, 2 passed` before the new runtime-server wiring existed | ✅ `pytest tests/unit/mbse/test_web_runtime_bridge.py tests/integration/test_mbse_workbench.py tests/unit/mbse/test_cli_main.py` passed `11 passed` after updating server/CLI wiring | ✅ Tests cover GET snapshot, variable mutation, event mutation, reset, unknown-ID rejection, and CLI startup injection | ➖ None needed |
| 3.2 | `tests/integration/test_mbse_workbench.py`, `tests/unit/mbse/test_cli_main.py` | Integration + Unit | ⚠️ Same stale-test safety-net failure showed the old `/api/highlight` + file-backed session path was already invalid after Work Unit 1 | ✅ Same `5 failed, 2 passed` RED confirmed `runtime_bridge` injection and `build_runtime_bridge()` did not exist yet; later `pytest tests/integration/test_mbse_workbench.py -k prepared_graphviz_input_bootable` failed because prepared Graphviz input still tried to boot a real HSM runtime | ✅ `pytest tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_web_runtime_bridge.py tests/unit/mbse/test_cli_main.py tests/integration/test_mbse_workbench.py tests/integration/test_hsm_json_workbench.py` passed `19 passed` after the in-memory runtime endpoints and prepared-input fallback were wired | ✅ Separate assertions force independent server paths for session read, reset, events, variables, SVG serving, SVG-ID contract validation, and prepared-input boot fallback | ✅ Server stays focused on HTTP/static concerns while the bridge owns runtime serialization/validation |
| 3.3 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ `pytest tests/integration/test_mbse_workbench.py` passed `5 passed` before modifying the served viewer HTML/JS | ✅ `pytest tests/integration/test_mbse_workbench.py -k runtime_ready_static_viewer` failed because the page still rendered `Apply highlight` and exposed no runtime controls | ✅ `pytest tests/integration/test_mbse_workbench.py -k "runtime_ready_static_viewer or keeps_prepared_graphviz_input_bootable"` passed `2 passed` after wiring reset/event/variable controls and backend snapshot rendering | ✅ HSM JSON input verifies runtime controls + endpoint wiring, while prepared Graphviz input proves the same minimal UI stays bootable with empty declared IDs | ✅ Removed the legacy manual highlight form and kept the frontend thin around backend-owned session payloads |
| 4.1 | `tests/unit/mbse/test_hsm_runtime.py`, `tests/unit/mbse/test_web_runtime_bridge.py`, `tests/unit/mbse/test_cli_main.py` | Unit | ✅ The relevant unit files already passed within the Work Unit 2 scoped suite (`10 passed` subset preserved before final verification) | ✅ Verification task executes already-authored RED/GREEN coverage; no new production behavior was introduced in 4.1 | ✅ `pytest tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_web_runtime_bridge.py tests/unit/mbse/test_cli_main.py` passed `10 passed` | ➖ Triangulation skipped: verification task confirms the existing unit behaviors together | ➖ None needed |
| 4.2 | `tests/integration/test_mbse_session_build.py`, `tests/integration/test_mbse_workbench.py`, `tests/integration/test_hsm_json_workbench.py` | Integration | ✅ The modified integration surfaces had already passed in focused runs before the final batch | ✅ Verification task executes already-authored RED/GREEN coverage; no new production behavior was introduced in 4.2 | ✅ `pytest tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py tests/integration/test_hsm_json_workbench.py` passed `11 passed` | ➖ Triangulation skipped: batch verification aggregates the existing scenarios for session build, runtime endpoints, and HSM JSON viewer flow | ➖ None needed |
| 4.3 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ The focused viewer integration file passed before cleanup (`5 passed`) | ✅ The cleanup assertions were written first in `test_build_and_start_workbench_serves_runtime_ready_static_viewer()` to reject legacy highlight-only strings and require runtime-control copy | ✅ Same focused viewer command and the final integration batch stayed green after removing remaining highlight-only frontend references | ✅ Assertions now cover both positive runtime-control strings and negative legacy-contract strings (`Apply highlight`, `/api/highlight`); repo search confirmed no source-side `workbench-session.json` references remain | ➖ Triangulation skipped: cleanup task is assertion/documentation tightening rather than new branching logic |

## Test Summary

- **Total tests written**: 4 new unit tests plus 10 updated integration/unit assertions across all work units (including viewer wiring assertions in Work Unit 3)
- **Total tests passing**: 21 tests across the final unit + integration verification batches
- **Layers used**: Unit (10), Integration (11), E2E (0)
- **Approval tests**: None — the runtime bridge intentionally replaces the legacy highlight-only server contract
- **Pure functions created**: 0

## Files Changed

- `tests/integration/test_mbse_session_build.py` — strict-TDD coverage for no `workbench-session.json` and retained render artifacts
- `tests/integration/test_hsm_json_workbench.py` — triangulation for declared `event_ids` and `variable_ids` on HSM JSON input
- `tests/unit/mbse/test_web_runtime_bridge.py` — strict-TDD unit coverage for snapshot serialization, ID validation, and reset semantics
- `tests/integration/test_mbse_workbench.py` — runtime endpoint contract coverage for injected in-memory app state and exact-ID validation
- `tests/unit/mbse/test_cli_main.py` — CLI wiring coverage for runtime-bridge construction/injection
- `src/mbse/domain/models.py` — runtime-viewer dataclasses kept; legacy highlight-only session/result types removed
- `src/mbse/domain/__init__.py` — removed obsolete `WorkbenchSession` export
- `src/mbse/application/build_session.py` — returns in-memory app-state metadata and declared IDs while still validating exact SVG IDs
- `src/mbse/application/web_runtime_bridge.py` — bridge around `HsmRuntime` for session serialization, reset, event dispatch, and variable mutation
- `src/mbse/infrastructure/session_store.py` — persists only `prepared-document.json` and `diagram.svg`
- `src/mbse/web/server.py` — injects runtime bridge and serves `/api/session.json`, `/api/runtime/reset`, `/api/runtime/events`, `/api/runtime/variables`
- `src/mbse/cli/main.py` — builds one runtime bridge from the input payload, falling back to an inert in-memory snapshot for prepared Graphviz input, and injects it into server startup
- `src/mbse/web/static/index.html` — replaces the manual highlight form with minimal reset/event/variable controls plus snapshot/status output
- `src/mbse/web/static/viewer.js` — loads backend session payloads, renders controls from declared IDs, posts runtime mutations, and refreshes exact-ID highlights from `active_ids`
- `openspec/changes/web-runtime-bridge/tasks.md` — cumulative task checklist updated through Work Unit 3 and final verification

## Verification Commands

- `pytest tests/integration/test_mbse_session_build.py tests/integration/test_hsm_json_workbench.py tests/unit/mbse/test_highlight.py` — Work Unit 1 safety net passed `8 passed`
- `pytest tests/integration/test_mbse_session_build.py tests/integration/test_hsm_json_workbench.py` — Work Unit 1 RED failed during collection with `ImportError: cannot import name 'WorkbenchAppState'`
- `pytest tests/integration/test_mbse_session_build.py tests/integration/test_hsm_json_workbench.py` — Work Unit 1 GREEN passed `6 passed`
- `pytest tests/integration/test_mbse_session_build.py tests/integration/test_hsm_json_workbench.py tests/unit/mbse/test_highlight.py` — Work Unit 1 verification passed `8 passed`
- `pytest tests/integration/test_mbse_workbench.py tests/unit/mbse/test_cli_main.py tests/unit/mbse/test_highlight.py tests/unit/mbse/test_hsm_runtime.py` — Work Unit 2 safety net exposed `1 failed, 9 passed` because the stale workbench test still referenced removed `workbench-session.json`
- `pytest tests/unit/mbse/test_web_runtime_bridge.py` — Work Unit 2 RED failed during collection with `ModuleNotFoundError: No module named 'mbse.application.web_runtime_bridge'`
- `pytest tests/integration/test_mbse_workbench.py tests/unit/mbse/test_cli_main.py` — server/CLI RED failed `5 failed, 2 passed` before runtime-bridge injection existed
- `pytest tests/unit/mbse/test_web_runtime_bridge.py` — bridge GREEN passed `4 passed`
- `pytest tests/unit/mbse/test_web_runtime_bridge.py tests/integration/test_mbse_workbench.py tests/unit/mbse/test_cli_main.py` — server/CLI GREEN passed `11 passed`
- `pytest tests/integration/test_mbse_workbench.py -k prepared_graphviz_input_bootable` — prepared-input RED/green check passed after adding the inert fallback bridge
- `pytest tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_web_runtime_bridge.py tests/unit/mbse/test_cli_main.py tests/integration/test_mbse_workbench.py tests/integration/test_hsm_json_workbench.py` — Work Unit 2 verification passed `19 passed`
- `pytest tests/integration/test_mbse_workbench.py` — Work Unit 3 safety net passed `5 passed`
- `pytest tests/integration/test_mbse_workbench.py -k runtime_ready_static_viewer` — Work Unit 3 RED failed because the served page still lacked runtime controls and still exposed the highlight-only UI
- `pytest tests/integration/test_mbse_workbench.py -k "runtime_ready_static_viewer or keeps_prepared_graphviz_input_bootable"` — Work Unit 3 GREEN/triangulation passed `2 passed`
- `pytest tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_web_runtime_bridge.py tests/unit/mbse/test_cli_main.py` — Work Unit 3 unit verification passed `10 passed`
- `pytest tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py tests/integration/test_hsm_json_workbench.py` — Work Unit 3 integration verification passed `11 passed`

## Deviations

- None — implementation matches the Work Unit 3 boundary and keeps the viewer thin, backend-owned, and free of event parameters or UI redesign.

## Notes

- The old read-only highlight flow is fully removed from active code paths; runtime session payloads now come only from `WorkbenchRuntimeBridge`.
- `build_runtime_bridge()` boots real HSM JSON input into `HsmRuntime`, but prepared Graphviz input falls back to an inert in-memory snapshot so the no-file contract stays bootable without inventing runtime semantics.
- The served frontend now derives all control options and highlight refreshes from backend responses only; no `/api/highlight`, event parameters, or persisted session-state contract remain.
