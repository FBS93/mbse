# Tasks: HSM Executable Activities And Guards

## Review Workload Forecast

| Field | Value |
|---|---|
| Estimated changed lines | 650-950 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR1 schema+validation (+ internal/external transition correction) → PR2 prepared/generated engine candidate metadata → PR3 runtime ordering → PR4 parity tests+docs |
| Delivery strategy | ask-always → resolved to chained PRs |
| Chain strategy | feature-branch-chain |

Decision needed before apply: Resolved
Chained PRs recommended: Yes
Chain strategy: feature-branch-chain
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|---|---|---|---|
| 1 | Callable-ref schema/model validation | PR 1 | Independent RED→GREEN slice |
| 2 | Ordered candidate metadata generation for internal + external event candidates | PR 2 | Base can stack on PR 1 |
| 3 | Runtime guard/activity execution order | PR 3 | Depends on PR 2 metadata |
| 4 | Parity/spec cleanup | PR 4 | Finish tests and wording alignment |

## Phase 1: Foundation

- [x] 1.1 RED: update `tests/unit/mbse/test_hsm_validation.py` and `tests/unit/mbse/test_validation.py` for callable refs, optional `on_initial`/`on_entry`/`on_exit`, and inline-string rejection.
- [x] 1.2 GREEN: extend `src/mbse/domain/hsm_schema_v1.json` with callable-ref defs plus optional lifecycle fields, first-class `internal_transitions`, and guarded external `transitions`.
- [x] 1.3 GREEN: update `src/mbse/domain/models.py` to add callable-ref value objects, `on_initial` on `HsmState`, and distinct internal/external transition rows.
- [x] 1.4 GREEN: update `src/mbse/domain/validation.py` to parse optional lifecycle hooks, validate internal-vs-external transition shapes, validate refs/signatures, and reject raw strings with clear errors.

## Phase 2: Prepared Engine Metadata

- [x] 2.1 RED: extend `tests/unit/mbse/test_prepare_hsm_engine.py` for ordered mixed event candidates, lifecycle plans, and initial-transition activities.
- [x] 2.2 GREEN: update `src/mbse/application/prepare_hsm_engine.py` to resolve callable plans at build time and preserve declaration order per state/event across internal and external transitions.
- [x] 2.3 GREEN: update `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` and `src/mbse/infrastructure/generated_engine.py` to emit/load candidate lists and resolved handlers instead of flat event maps.

## Phase 3: Runtime Execution

- [x] 3.1 RED: rewrite `tests/unit/mbse/test_hsm_runtime.py` around trace spies for init ordering, guard-false bubbling, internal-transition handling, and self/ancestor/descendant cases.
- [x] 3.2 GREEN: update `src/mbse/application/hsm_runtime.py` to expose live dispatch context, evaluate guards leaf→root, run internal-transition activities without state change, and run exits/activities/entries in `example_hsm` order.
- [x] 3.3 REFACTOR: keep `src/mbse/application/build_hsm_runtime.py` API stable while threading resolved engine metadata into runtime execution.

## Phase 4: Integration And Parity

- [x] 4.1 RED/GREEN: update `tests/unit/mbse/test_generated_engine.py` and `tests/integration/test_generated_hsm_engine.py` for deterministic executable behavior, root initial ordering parity, and generated-handler privacy.
- [x] 4.2 RED/GREEN: verify `tests/integration/test_mbse_session_build.py` and related runtime-facing flows no longer assume inert executable behavior; no assertion changes were required in this slice.

## Phase 5: Spec And Task Cleanup

- [x] 5.1 Update `openspec/changes/hsm-executable-activities-and-guards/specs/generated-hsm-engine/spec.md` wording so states MAY define optional `on_initial`, `on_entry`, and `on_exit` hooks when activities are linked.
- [x] 5.2 Correct change artifacts so internal transitions are modeled separately from external transitions before PR2 metadata work.
- [x] 5.3 Re-check `openspec/changes/hsm-executable-activities-and-guards/tasks.md` slices after Phase 1 estimates; chain choice is resolved to feature-branch-chain for the approved chained delivery.
