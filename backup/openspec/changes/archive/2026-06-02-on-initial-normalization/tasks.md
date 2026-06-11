# Tasks: Normalize `on_initial`

## Review Workload Forecast

| Field | Value |
|---|---|
| Estimated changed lines | 260-360 |
| 400-line budget risk | Medium |
| Chained PRs recommended | No |
| Suggested split | Single PR |
| Delivery strategy | ask-always |
| Chain strategy | pending |

Decision needed before apply: Yes
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Medium

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|---|---|---|---|
| 1 | Keep `on_initial` as the only executable initial hook | Single PR | Light cleanup; keep tests/docs in same slice |

## Phase 1: Contract RED/GREEN

- [x] 1.1 RED: add/update `tests/unit/mbse/test_hsm_validation.py` to reject authored `initial.activities` and expect `HsmInitialTransition(id, target_id)` only.
- [x] 1.2 GREEN: remove `activities` from `src/mbse/domain/hsm_schema_v1.json`, `src/mbse/domain/models.py`, and `src/mbse/domain/validation.py`.
- [x] 1.3 REFACTOR: simplify any helpers/types made redundant by the smaller initial contract.

## Phase 2: Engine and runtime cleanup

- [x] 2.1 RED: update `tests/unit/mbse/test_prepare_hsm_engine.py` and `tests/unit/mbse/test_generated_engine.py` to assert initials keep only target/id metadata and no initial activity plans/rows remain.
- [x] 2.2 GREEN: remove `HsmPreparedEngineInitialRow` and `initial_rows_by_owner_id` from `src/mbse/application/prepare_hsm_engine.py`, `src/mbse/infrastructure/generated_engine.py`, and `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2`.
- [x] 2.3 RED/GREEN: update `tests/unit/mbse/test_hsm_runtime.py` and then `src/mbse/application/hsm_runtime.py` so `init()` and nested descent run `on_entry` + state-owned `on_initial` only.

## Phase 3: Render cleanup

- [x] 3.1 RED: update `tests/unit/mbse/test_hsm_render_view.py` and `tests/integration/test_hsm_json_workbench.py` to require `on_initial:` sections and forbid `initial_transition:` / initial activity text.
- [x] 3.2 GREEN: change `src/mbse/application/prepare_hsm_render.py` so initial edges stay routing-only and state bodies render only lifecycle sections.

## Phase 4: Fixtures and verification

- [x] 4.1 Remove authored `initial.activities` from `test_hsm/hsm.json` and any test fixtures that still model executable initials.
- [x] 4.2 Run `pytest tests/unit/mbse/test_hsm_validation.py tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_generated_engine.py tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py`.
- [x] 4.3 Run full `pytest` to confirm no other contract or rendering expectations still depend on `initial.activities`.
