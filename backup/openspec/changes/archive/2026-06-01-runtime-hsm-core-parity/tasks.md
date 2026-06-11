# Tasks: Runtime HSM Core Parity

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 500-800 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 metadata/tests -> PR 2 generated engine -> PR 3 runtime parity + integration |
| Delivery strategy | ask-on-risk |
| Chain strategy | feature-branch-chain |

Decision needed before apply: No — resolved to feature-branch-chain
Chained PRs recommended: Yes
Chain strategy: feature-branch-chain
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Extend prepared metadata contract first | PR 1 | Dataclasses + prep tests; safe base slice |
| 2 | Emit/load generated parity metadata | PR 2 | Depends on PR 1; keep template/wrapper review isolated |
| 3 | Port runtime parity helpers and replay tests | PR 3 | Depends on PR 2; runtime + integration verification |

## Phase 1: Metadata Foundation

- [x] 1.1 RED: Expand `tests/unit/mbse/test_prepare_hsm_engine.py` to assert `ancestry_by_state_id`, `source_id` on transition rows, and initial-transition maps for C-like topologies.
- [x] 1.2 GREEN: Update `src/mbse/domain/models.py` dataclasses so `HsmPreparedEngineTransitionRow` carries `source_id` and `HsmPreparedEngineView` carries ancestry metadata.
- [x] 1.3 GREEN: Refactor `src/mbse/application/prepare_hsm_engine.py` to build ancestry tuples, preserve depth-first order, and collect event transition rows by handling state.

## Phase 2: Generated Engine Metadata Wiring

- [x] 2.1 RED: Extend `tests/unit/mbse/test_generated_engine.py` to require generated parent/ancestry facts, transition descriptors, and event-to-transition lookup indexes.
- [x] 2.2 GREEN: Update `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` to emit parity-facing transition metadata instead of only flat target returns.
- [x] 2.3 GREEN: Update `src/mbse/infrastructure/generated_engine.py` to load/store the new metadata on `GeneratedEngine` without widening the public runtime API.

## Phase 3: Runtime Parity Algorithm

- [x] 3.1 RED: Add focused cases in `tests/unit/mbse/test_hsm_runtime.py` for full initial descent, same-branch trim, ancestor target, cross-branch target, self transition, and inert events.
- [x] 3.2 GREEN: Refactor `src/mbse/application/hsm_runtime.py` to add private helpers for transition-source lookup, LCA path computation, transition execution, and nested initial descent.
- [x] 3.3 REFACTOR: Keep `set_state()` leaf-only unless a failing parity fixture proves otherwise; if touched, document the constraint in runtime tests.

## Phase 4: Integration Parity Verification

- [x] 4.1 RED: Expand `tests/integration/test_generated_hsm_engine.py` with reference-style event sequences that assert deterministic snapshots and final leaves through `build_hsm_runtime()` only.
- [x] 4.2 GREEN: Verify runtime/infrastructure glue preserves `last_transition_id`, active path trimming, and inert action strings across repeated runs.
- [x] 4.3 VERIFY: Run `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_generated_engine.py tests/unit/mbse/test_hsm_runtime.py tests/integration/test_generated_hsm_engine.py`.
