# Tasks: Runtime Last-Event Semantics

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 420-520 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 runtime+DTOs+unit tests -> PR 2 bridge+viewer+integration tests |
| Delivery strategy | ask-always |
| Chain strategy | pending |

Decision needed before apply: Yes
Chained PRs recommended: Yes
Chain strategy: pending
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Runtime semantic record + DTO compatibility | PR 1 | Base slice; includes RED/GREEN unit coverage in `test_hsm_runtime.py` and `test_generated_hsm_engine.py`. |
| 2 | Bridge/viewer semantic payload adoption | PR 2 | Depends on PR 1; remove viewer-facing `last_transition_id`, then lock JSON/browser behavior. |

## Phase 1: RED Runtime Semantics Tests

- [x] 1.1 Extend `tests/unit/mbse/test_hsm_runtime.py` with failing cases for unhandled events, handled internal transitions, external transition ordering, and deprecated runtime-only `last_transition_id` alias derivation.
- [x] 1.2 Extend `tests/integration/test_generated_hsm_engine.py` with failing deterministic snapshot assertions against `last_event` and `executed_activities` ordering.

## Phase 2: Runtime DTO and Recording

- [x] 2.1 Update `src/mbse/domain/models.py` to add `HsmExecutedActivity`, `HsmRuntimeLastEvent`, viewer `last_event` DTOs, and keep `HsmRuntimeSnapshot.last_transition_id` as a derived deprecated alias only.
- [x] 2.2 Refactor `src/mbse/application/hsm_runtime.py` to store/reset explicit `last_event` on `init()`, `send_event()`, and `set_state()`, including handled/unhandled status and handler identity.
- [x] 2.3 Wrap runtime activity execution in `src/mbse/application/hsm_runtime.py` so semantic origin metadata is captured from plan ownership and `executed_activities` stays execution-ordered.
- [x] 2.4 Derive `transition_path_ids` only for taken external transitions and preserve empty paths for internal handling or unhandled events.

## Phase 3: Bridge and Viewer Mapping

- [x] 3.1 Extend `tests/unit/mbse/test_web_runtime_bridge.py` with failing payload-shape checks for `snapshot.last_event` and removal of viewer-facing `last_transition_id`.
- [x] 3.2 Update `src/mbse/application/web_runtime_bridge.py` to map runtime `last_event` into `RuntimeViewerSnapshot`, preserve `active_ids`, and stop serializing bridge `last_transition_id`.
- [x] 3.3 Update `src/mbse/web/static/viewer.js` to consume `snapshot.last_event` without adding transition/activity SVG targeting or styling behavior.

## Phase 4: Integration Verification

- [x] 4.1 Extend `tests/integration/test_mbse_workbench.py` to lock session/event/reset JSON payloads for handled internal transitions, external transitions, unhandled events, and viewer compatibility without render inference.
- [x] 4.2 Run `pytest tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_web_runtime_bridge.py tests/integration/test_generated_hsm_engine.py tests/integration/test_mbse_workbench.py` and keep the slice limited to iteration-1 runtime/viewer semantics.
