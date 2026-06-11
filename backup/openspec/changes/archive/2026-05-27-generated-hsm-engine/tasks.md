# Tasks: Generated HSM Engine

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 450-700 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 generator view+tests -> PR 2 generated module+runtime API -> PR 3 integration+cleanup |
| Delivery strategy | chained by explicit user decision |
| Chain strategy | stacked-to-main |

Decision needed before apply: Resolved
Chained PRs recommended: Yes
Chain strategy: stacked-to-main
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Freeze engine view + indexes | PR 1 | Base slice; no public runtime yet |
| 2 | Add generated module boundary + runtime facade | PR 2 | Depends on PR 1; keep generated internals private |
| 3 | Prove JSON->runtime flow + docs cleanup | PR 3 | Depends on PR 2; batch verification included |

## Phase 1: Foundation

- [x] 1.1 RED: add `tests/unit/mbse/test_prepare_hsm_engine.py` for depth-first state order, parent map, root/local initials, and event transition buckets from validated `HsmDocument`.
- [x] 1.2 Extend `src/mbse/domain/models.py` with frozen engine-view and snapshot dataclasses only; keep public runtime API types handwritten.
- [x] 1.3 GREEN: create `src/mbse/application/prepare_hsm_engine.py` to lower `HsmDocument` into deterministic parents, initials, leaf IDs, and per-state event rows.

## Phase 2: Generated Boundary

- [x] 2.1 RED: add focused template/render tests in `tests/unit/mbse/test_prepare_hsm_engine.py` or a sibling unit file for one generated function per state and static indexes.
- [x] 2.2 Create `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` with private `state_<id>(ctx, event_id)` handlers returning only `("transition", target)` or `("unhandled", None)`.
- [x] 2.3 Create `src/mbse/infrastructure/generated_engine.py` to render/load the private engine module without exposing generated symbols through package exports.

## Phase 3: Runtime Facade

- [x] 3.1 RED: add `tests/unit/mbse/test_hsm_runtime.py` for `init`, parent fallback, inert unhandled events, variables, `set_state`, and inert `on_entry`/`on_exit` behavior.
- [x] 3.2 Create `src/mbse/application/hsm_runtime.py` with handwritten context, active-path recomputation, dispatch walk leaf->root, and snapshot API.
- [x] 3.3 Create `src/mbse/application/build_hsm_runtime.py` to build `HsmRuntime` from validated JSON/document while keeping the top public API stable.

## Phase 4: Integration And Batch Verification

- [x] 4.1 RED/GREEN: add `tests/integration/test_generated_hsm_engine.py` covering JSON -> generated engine -> runtime, public API only, and deterministic replay.
- [x] 4.2 Update package wiring only where needed in `src/mbse/application/__init__.py` or adjacent imports; do not surface generated internals.
- [x] 4.3 Batch verify with `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_hsm_runtime.py tests/integration/test_generated_hsm_engine.py` before widening to full `pytest`.
