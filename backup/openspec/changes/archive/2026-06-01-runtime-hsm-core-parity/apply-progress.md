# Apply Progress: runtime-hsm-core-parity

## Scope

- Delivery mode: chained PR slice
- Chain strategy: feature-branch-chain
- Current work unit: PR 3 / Unit 3 — runtime parity algorithm + integration verification
- Boundary: port runtime parity helpers and parity-oriented integration replay on top of generated metadata while keeping the runtime public API unchanged
- Previous work units: PR 1 / Unit 1 — metadata foundation
- Previous work units: PR 2 / Unit 2 — generated engine metadata wiring
- Follow-up batch: None — targeted parity slice is complete and ready for verify/archive
- Follow-up boundary: N/A

## Completed Tasks

- [x] 1.1 RED: Expand `tests/unit/mbse/test_prepare_hsm_engine.py` to assert `ancestry_by_state_id`, `source_id` on transition rows, and initial-transition maps for C-like topologies.
- [x] 1.2 GREEN: Update `src/mbse/domain/models.py` dataclasses so `HsmPreparedEngineTransitionRow` carries `source_id` and `HsmPreparedEngineView` carries ancestry metadata.
- [x] 1.3 GREEN: Refactor `src/mbse/application/prepare_hsm_engine.py` to build ancestry tuples, preserve depth-first order, and collect event transition rows by handling state.
- [x] 2.1 RED: Extend `tests/unit/mbse/test_generated_engine.py` to require generated parent/ancestry facts, transition descriptors, and event-to-transition lookup indexes.
- [x] 2.2 GREEN: Update `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` to emit parity-facing transition metadata instead of only flat target returns.
- [x] 2.3 GREEN: Update `src/mbse/infrastructure/generated_engine.py` to load/store the new metadata on `GeneratedEngine` without widening the public runtime API.
- [x] 3.1 RED: Add focused cases in `tests/unit/mbse/test_hsm_runtime.py` for full initial descent, same-branch trim, ancestor target, cross-branch target, self transition, and inert events.
- [x] 3.2 GREEN: Refactor `src/mbse/application/hsm_runtime.py` to add private helpers for transition-source lookup, LCA path computation, transition execution, and nested initial descent.
- [x] 3.3 REFACTOR: Keep `set_state()` leaf-only unless a failing parity fixture proves otherwise; if touched, document the constraint in runtime tests.
- [x] 4.1 RED: Expand `tests/integration/test_generated_hsm_engine.py` with reference-style event sequences that assert deterministic snapshots and final leaves through `build_hsm_runtime()` only.
- [x] 4.2 GREEN: Verify runtime/infrastructure glue preserves `last_transition_id`, active path trimming, and inert action strings across repeated runs.
- [x] 4.3 VERIFY: Run `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_generated_engine.py tests/unit/mbse/test_hsm_runtime.py tests/integration/test_generated_hsm_engine.py`.

## Remaining Tasks

- None — tasks 1.1 through 4.3 are complete for this change slice.

### TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 | `tests/unit/mbse/test_prepare_hsm_engine.py` | Unit | ✅ `pytest tests/unit/mbse/test_prepare_hsm_engine.py` passed `2 passed` before modifying existing metadata tests | ✅ `pytest tests/unit/mbse/test_prepare_hsm_engine.py` failed `2 failed` after adding ancestry/source-aware assertions first (`AttributeError` on missing `ancestry_by_state_id` and `source_id`) | ✅ `pytest tests/unit/mbse/test_prepare_hsm_engine.py` passed `3 passed` after implementing the metadata contract | ✅ Two fixtures now exercise different paths: a small door machine and a deeper C-like hierarchy with nested initials and ancestor-owned transitions | ➖ None needed |
| 1.2 | `tests/unit/mbse/test_prepare_hsm_engine.py` | Unit | ✅ Same `2 passed` safety net protected `src/mbse/domain/models.py` before extending the dataclasses | ✅ Same RED failure proved the prepared view/row contract was missing required parity metadata | ✅ Same targeted command passed `3 passed` after adding `source_id` and `ancestry_by_state_id` | ✅ Assertions cover both leaf-owned and ancestor-owned transition rows plus deep ancestry tuples | ➖ None needed |
| 1.3 | `tests/unit/mbse/test_prepare_hsm_engine.py` | Unit | ✅ Same `2 passed` safety net protected `src/mbse/application/prepare_hsm_engine.py` before refactoring | ✅ Same RED failure proved preparation logic did not yet build ancestry tuples or source-aware rows | ✅ `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_generated_engine.py` passed `5 passed` after refactoring the preparation pipeline and checking adjacent generated-engine compatibility | ✅ The C-like fixture forces recursive ancestry construction while the existing fixture proves eventless transitions stay out of event buckets | ✅ Extracted pure `_collect_ancestry_by_state_id()` helper and kept depth-first flattening unchanged |
| 2.1 | `tests/unit/mbse/test_generated_engine.py` | Unit | ✅ `pytest tests/unit/mbse/test_generated_engine.py` passed `2 passed` before modifying generated-engine tests | ✅ `pytest tests/unit/mbse/test_generated_engine.py` failed `2 failed` after adding ancestry/transition-row wrapper assertions first (`AttributeError` on missing `ancestry_by_state_id` plus missing generated source import/metadata constants) | ✅ `pytest tests/unit/mbse/test_generated_engine.py` passed `2 passed` after wiring generated parity metadata | ✅ Source assertions cover emitted literals while wrapper assertions prove the loaded engine preserves ancestry, transition rows, and event lookup indexes across states with and without handlers | ➖ None needed |
| 2.2 | `tests/unit/mbse/test_generated_engine.py` | Unit | ✅ Same `2 passed` safety net protected `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` before changing generated source layout | ✅ Same RED failure proved the template still emitted only flat runtime constants and lacked parity metadata literals | ✅ Same targeted command passed `2 passed` after the template emitted ancestry and transition-row constants alongside private handlers | ✅ The emitted source now covers ancestor-aware tuples and a descriptor row for an ancestor-owned transition, not just leaf target returns | ➖ None needed |
| 2.3 | `tests/unit/mbse/test_generated_engine.py` | Unit | ✅ Same `2 passed` safety net protected `src/mbse/infrastructure/generated_engine.py` before expanding the wrapper | ✅ Same RED failure proved `GeneratedEngine` did not yet load/store ancestry and transition descriptors | ✅ `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_generated_engine.py` passed `5 passed` after loading the new metadata without changing dispatch behavior | ✅ Verification covers both populated and empty event indexes, plus wrapper access to prepared transition rows for future runtime parity work | ➖ None needed |
| 3.1 | `tests/unit/mbse/test_hsm_runtime.py` | Unit | ✅ `pytest tests/unit/mbse/test_hsm_runtime.py tests/integration/test_generated_hsm_engine.py` passed `5 passed` before modifying runtime tests | ✅ Same targeted command failed `2 failed` after adding C-parity runtime and integration assertions first (`AssertionError: assert 's2111' == 's2'` on ancestor-target parity) | ✅ `pytest tests/unit/mbse/test_hsm_runtime.py` passed `5 passed` after refactoring runtime parity helpers | ✅ The runtime tests cover full initial descent, ancestor-handled dispatch, same-branch trim, ancestor target stop, cross-branch nested initial descent, self transition, inert ping, and the documented leaf-only `set_state()` constraint | ✅ Extracted explicit transition-source, LCA/path, transition execution, and nested-initial helpers without widening the public runtime API |
| 3.2 | `tests/unit/mbse/test_hsm_runtime.py` | Unit | ✅ Same `5 passed` safety net protected `src/mbse/application/hsm_runtime.py` before changing runtime flow | ✅ Same RED failure proved compound ancestor targets were still auto-descending into initials instead of stopping at the explicit ancestor target | ✅ Same targeted unit command passed `5 passed` after introducing the parity helpers and source-aware execution path | ✅ Door-machine regression coverage plus C-reference parity coverage force two different transition families through the same helper pipeline | ✅ Replaced the monolithic `_resolve_active_path()` flow with smaller helpers that make parity semantics explicit |
| 3.3 | `tests/unit/mbse/test_hsm_runtime.py` | Unit | ✅ Same `5 passed` safety net covered the pre-existing leaf-only runtime API | ✅ The new parity test explicitly asserts `set_state("s2")` raises `ValueError`, documenting the unchanged leaf-only contract before any runtime refactor | ✅ Same targeted unit command passed `5 passed` with the parity refactor in place and `set_state()` still leaf-only | ✅ Existing door-machine coverage exercises `set_state("open")` while the new C-reference coverage proves compound states remain rejected | ➖ None needed |
| 4.1 | `tests/integration/test_generated_hsm_engine.py` | Integration | ✅ `pytest tests/unit/mbse/test_hsm_runtime.py tests/integration/test_generated_hsm_engine.py` passed `5 passed` before expanding parity replay coverage | ✅ Same targeted command failed `2 failed` after adding deterministic C-reference replay assertions first (`AssertionError` on the expected `("s2",)` snapshot after the ancestor-target transition) | ✅ `pytest tests/integration/test_generated_hsm_engine.py` passed `3 passed` after the runtime parity refactor | ✅ Replays now cover init, ancestor-handled dispatch, same-branch transition, ancestor target stop, inert event retention, cross-branch nested initial descent, and self transition across two independent runtime builds | ➖ None needed |
| 4.2 | `tests/integration/test_generated_hsm_engine.py` | Integration | ✅ Same `5 passed` safety net protected public runtime/build glue before replay verification | ✅ Same RED failure proved runtime/build glue still surfaced the wrong active path and `last_transition_id` for the ancestor-target case | ✅ Same integration command passed `3 passed` after the parity helpers preserved `last_transition_id`, active-path trimming, and inert action strings across repeated runs | ✅ Two identical runs prove deterministic snapshots while the C-reference payload's inert entry/exit strings verify that v1 action strings remain metadata only | ➖ None needed |
| 4.3 | `tests/unit/mbse/test_prepare_hsm_engine.py`, `tests/unit/mbse/test_generated_engine.py`, `tests/unit/mbse/test_hsm_runtime.py`, `tests/integration/test_generated_hsm_engine.py` | Unit + Integration | ✅ Prior targeted GREEN runs established each modified file passed in isolation before final verification | ✅ The slice stayed honest because the earlier RED command failed before implementation on the same parity scenarios now covered by the full suite | ✅ `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_generated_engine.py tests/unit/mbse/test_hsm_runtime.py tests/integration/test_generated_hsm_engine.py` passed `13 passed` | ✅ The final suite spans metadata prep, generated-engine wiring, runtime parity helpers, and public-API replay coverage | ➖ None needed |

## Test Summary

- **Total tests written**: 8 targeted tests across the parity slice files
- **Total tests passing**: 13 targeted parity tests in the final verification suite
- **Layers used**: Unit (10), Integration (3), E2E (0)
- **Approval tests**: None — this slice extended metadata contracts and preparation logic without preserving legacy output via approval fixtures
- **Pure functions created**: 3

## Files Changed

- `tests/unit/mbse/test_prepare_hsm_engine.py` — added strict-TDD parity expectations for ancestry, initial-transition maps, and source-aware transition rows
- `tests/unit/mbse/test_generated_engine.py` — added strict-TDD parity expectations for emitted ancestry metadata, transition descriptors, and wrapper lookup indexes
- `src/mbse/domain/models.py` — extended prepared-engine dataclasses with transition `source_id` and `ancestry_by_state_id`
- `src/mbse/application/prepare_hsm_engine.py` — built ancestry tuples and emitted source-aware transition rows while keeping depth-first order
- `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` — emits ancestry tuples and transition-row descriptors for future runtime parity helpers
- `src/mbse/infrastructure/generated_engine.py` — loads generated ancestry/transition metadata while keeping the dispatch API unchanged
- `tests/unit/mbse/test_hsm_runtime.py` — added C-reference strict-TDD parity coverage for init, transition families, inert events, and the leaf-only `set_state()` constraint
- `tests/integration/test_generated_hsm_engine.py` — added deterministic reference-style replay coverage through `build_hsm_runtime()` only
- `src/mbse/application/hsm_runtime.py` — refactored runtime flow into source lookup, LCA/path computation, transition execution, and nested initial descent helpers
- `openspec/changes/runtime-hsm-core-parity/tasks.md` — marks only slice-3 tasks complete for this batch while preserving prior slice completion
- `openspec/changes/runtime-hsm-core-parity/apply-progress.md` — merged PR 3 / Unit 3 strict-TDD evidence into the cumulative apply progress artifact

## Verification Commands

- `pytest tests/unit/mbse/test_prepare_hsm_engine.py` — safety net passed `2 passed`
- `pytest tests/unit/mbse/test_prepare_hsm_engine.py` — RED failed `2 failed` after new assertions referenced missing metadata
- `pytest tests/unit/mbse/test_prepare_hsm_engine.py` — GREEN passed `3 passed`
- `pytest tests/unit/mbse/test_generated_engine.py` — safety net passed `2 passed`
- `pytest tests/unit/mbse/test_generated_engine.py` — RED failed `2 failed` after new assertions referenced missing generated metadata
- `pytest tests/unit/mbse/test_generated_engine.py` — GREEN passed `2 passed`
- `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_generated_engine.py` — slice verification passed `5 passed`
- `pytest tests/unit/mbse/test_hsm_runtime.py tests/integration/test_generated_hsm_engine.py` — safety net passed `5 passed`
- `pytest tests/unit/mbse/test_hsm_runtime.py tests/integration/test_generated_hsm_engine.py` — RED failed `2 failed` after new parity assertions exposed the ancestor-target descent bug
- `pytest tests/unit/mbse/test_hsm_runtime.py` — GREEN passed `5 passed`
- `pytest tests/integration/test_generated_hsm_engine.py` — GREEN passed `3 passed`
- `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_generated_engine.py tests/unit/mbse/test_hsm_runtime.py tests/integration/test_generated_hsm_engine.py` — slice verification passed `13 passed`

## Deviations

- None — implementation matches the runtime parity design and keeps the public runtime API unchanged.

## Notes

- The C-like topology fixture uses lowercase IDs to satisfy the current schema while preserving the reference hierarchy shape needed for parity checks.
- Ancestor-target transitions intentionally stop at the explicit ancestor target instead of auto-following that state's initial chain; cross-branch transitions still descend nested initials below newly entered compound targets.
- Action strings remain inert throughout init and replay verification; the Python runtime now mirrors the C state outcomes without importing embedded-only limits, buffers, or reserved-event mechanics.
