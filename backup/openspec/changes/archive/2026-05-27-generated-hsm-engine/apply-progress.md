# Apply Progress: generated-hsm-engine

## Scope

- Delivery mode: chained PR slice
- Chain strategy: stacked-to-main
- Current work unit: Work Unit 3 / integration + package wiring + batch verification
- Boundary: prove JSON -> generated engine -> runtime via the public application API only, wire only the stable package exports needed for that flow, and stop after the scoped batch verification command
- Previous work units: Work Unit 1 / freeze engine view + indexes; Work Unit 2 / generated module boundary + runtime facade
- Follow-up batch: None
- Follow-up boundary: Ready for verify; no further apply slice remains for this change

## Completed Tasks

- [x] 1.1 RED: add `tests/unit/mbse/test_prepare_hsm_engine.py` for depth-first state order, parent map, root/local initials, and event transition buckets from validated `HsmDocument`.
- [x] 1.2 Extend `src/mbse/domain/models.py` with frozen engine-view and snapshot dataclasses only; keep public runtime API types handwritten.
- [x] 1.3 GREEN: create `src/mbse/application/prepare_hsm_engine.py` to lower `HsmDocument` into deterministic parents, initials, leaf IDs, and per-state event rows.
- [x] 2.1 RED: add `tests/unit/mbse/test_generated_engine.py` for deterministic engine source rendering, per-state handlers, and a wrapper that keeps generated symbols private.
- [x] 2.2 Create `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` with private `state_<id>(ctx, event_id)` handlers that return only `("transition", target)` or `("unhandled", None)`.
- [x] 2.3 GREEN: create `src/mbse/infrastructure/generated_engine.py` to render/load a private in-memory engine module behind a handwritten wrapper.
- [x] 3.1 RED: add `tests/unit/mbse/test_hsm_runtime.py` for `init`, parent fallback, inert unhandled events, variables, `set_state`, inert `on_entry`/`on_exit`, and builder input forms.
- [x] 3.2 Create `src/mbse/application/hsm_runtime.py` with handwritten runtime context, active-path recomputation, leaf->root dispatch, and deterministic snapshots.
- [x] 3.3 GREEN: create `src/mbse/application/build_hsm_runtime.py` to build `HsmRuntime` from validated JSON payloads or `HsmDocument` instances.
- [x] 4.1 RED/GREEN: add `tests/integration/test_generated_hsm_engine.py` covering JSON -> generated engine -> runtime, public API only, and deterministic replay.
- [x] 4.2 Update package wiring only where needed in `src/mbse/application/__init__.py` or adjacent imports; do not surface generated internals.
- [x] 4.3 Batch verify with `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_hsm_runtime.py tests/integration/test_generated_hsm_engine.py` before widening to full `pytest`.

## Remaining Tasks

- None — all tasks for `generated-hsm-engine` are complete in apply.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 | `tests/unit/mbse/test_prepare_hsm_engine.py` | Unit | ✅ `pytest tests/unit/mbse/test_hsm_validation.py tests/unit/mbse/test_hsm_render_view.py` passed `11 passed` before modifying shared model contracts | ✅ `pytest tests/unit/mbse/test_prepare_hsm_engine.py` failed during collection with `ModuleNotFoundError: No module named 'mbse.application.prepare_hsm_engine'` after writing the tests first | ✅ `pytest tests/unit/mbse/test_prepare_hsm_engine.py` passed `2 passed` after adding the new lowering entrypoint | ✅ Covered hierarchical indexes/initials and a second path proving leaf-only collection plus eventless transitions are excluded from event buckets | ➖ None needed |
| 1.2 | `tests/unit/mbse/test_prepare_hsm_engine.py` | Unit | ✅ Same `11 passed` safety net protected `src/mbse/domain/models.py` before extension | ✅ Same RED collection failure proved the engine-view contract was missing before adding the dataclasses | ✅ Same targeted command passed `2 passed` with frozen engine-view/snapshot dataclasses in place | ✅ Assertions exercise parent maps, initial indexes, leaf IDs, and typed transition rows through real production objects | ➖ None needed |
| 1.3 | `tests/unit/mbse/test_prepare_hsm_engine.py` | Unit | ✅ Same `11 passed` safety net | ✅ Same RED collection failure proved the lowering module did not exist yet | ✅ Same targeted command passed `2 passed` with deterministic depth-first flattening, initial-target extraction, and per-state event rows | ✅ Two scenarios force different code paths: nested initial resolution and omission of eventless transitions from runtime event buckets | ✅ Helpers stay pure and focused (`_flatten_states`, `_collect_parent_ids`, `_collect_initial_targets`) |
| 2.1 | `tests/unit/mbse/test_generated_engine.py` | Unit | N/A (new) | ✅ `pytest tests/unit/mbse/test_generated_engine.py` failed during collection with `ModuleNotFoundError: No module named 'mbse.infrastructure.generated_engine'` after writing the tests first | ✅ `pytest tests/unit/mbse/test_generated_engine.py tests/unit/mbse/test_hsm_runtime.py` passed `5 passed` after adding the generated engine path | ✅ One scenario locks exact rendered indexes/handler source and a second scenario proves the wrapper dispatches transitions without exposing generated functions as public attributes | ✅ Literal formatting moved into Python helpers so the Jinja template stays presentation-only and deterministic |
| 2.2 | `tests/unit/mbse/test_generated_engine.py` | Unit | N/A (new) | ✅ Same RED collection failure proved the template/render path was missing before implementation | ✅ Same targeted command passed `5 passed` with private `state_<id>` handlers and static indexes emitted from `hsm_v1_engine.py.j2` | ✅ Tests cover event-driven handlers plus leaf states with no transitions returning `("unhandled", None)` | ➖ None needed |
| 2.3 | `tests/unit/mbse/test_generated_engine.py` | Unit | N/A (new) | ✅ Same RED collection failure proved no generated wrapper existed | ✅ Same targeted command passed `5 passed` with an in-memory private module wrapper and dispatch API | ✅ Assertions exercise parent/initial/leaf indexes plus two different handler outcomes (`transition` and `unhandled`) through real generated code | ✅ Wrapper returns only stable handwritten fields (`parent_ids`, `initial_target_ids`, `leaf_state_ids`, `dispatch`) |
| 3.1 | `tests/unit/mbse/test_hsm_runtime.py` | Unit | N/A (new) | ✅ `pytest tests/unit/mbse/test_hsm_runtime.py` failed during collection with `ModuleNotFoundError: No module named 'mbse.application.build_hsm_runtime'` after writing the tests first | ✅ `pytest tests/unit/mbse/test_generated_engine.py tests/unit/mbse/test_hsm_runtime.py` passed `5 passed` after adding runtime and builder modules | ✅ Three scenarios prove different code paths: initialization snapshot, dropped event vs parent fallback transition, and forced leaf state with document-input builder flow | ➖ None needed |
| 3.2 | `tests/unit/mbse/test_hsm_runtime.py` | Unit | N/A (new) | ✅ Same RED collection failure proved the handwritten runtime API was missing | ✅ Same targeted command passed `5 passed` with runtime context, active-path recomputation, and leaf->root dispatch | ✅ Tests cover root/local initial descent, parent fallback, unhandled inertness, variable storage, and forced-state validation | ✅ Runtime helpers stay small and pure around ancestry reconstruction |
| 3.3 | `tests/unit/mbse/test_hsm_runtime.py` | Unit | N/A (new) | ✅ Same RED collection failure proved the builder entrypoint was missing | ✅ Same targeted command passed `5 passed` with support for validated payload and `HsmDocument` inputs | ✅ Builder behavior is triangulated by constructing runtimes from both input forms and then exercising the same public API contract | ➖ None needed |
| 4.1 | `tests/integration/test_generated_hsm_engine.py` | Integration | N/A (new) | ✅ `pytest tests/integration/test_generated_hsm_engine.py` failed `2 failed` after writing the public-API tests first because `from mbse.application import build_hsm_runtime` resolved to a module object instead of a callable export | ✅ `pytest tests/integration/test_generated_hsm_engine.py` passed `2 passed` after wiring the stable application export | ✅ One scenario proves JSON -> runtime flow and snapshot semantics through the public API only; a second scenario proves deterministic replay across two instances | ➖ None needed |
| 4.2 | `tests/integration/test_generated_hsm_engine.py` | Integration | ✅ `pytest tests/unit/mbse/test_hsm_runtime.py` passed `3 passed` before modifying `src/mbse/application/__init__.py` | ✅ Same RED failure proved package wiring was missing for the stable public builder entrypoint | ✅ Same targeted integration command passed `2 passed` after exporting `build_hsm_runtime` and `HsmRuntime` from `mbse.application` | ✅ Public imports now exercise a different code path than direct module imports while still keeping generated internals private | ➖ None needed |
| 4.3 | `tests/integration/test_generated_hsm_engine.py` | Integration | N/A (verification only) | ✅ Verification scope was defined before execution and included the newly added integration coverage | ✅ `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_hsm_runtime.py tests/integration/test_generated_hsm_engine.py` passed `7 passed` | ➖ Single verification command required by the task | ➖ None needed |

## Test Summary

- **Total tests written**: 9
- **Total tests passing**: 9 targeted tests across touched files; Work Unit 3 batch verification scope passed `7 passed`
- **Layers used**: Unit (7), Integration (2), E2E (0)
- **Approval tests**: None — Work Units 1 and 2 added new behavior without refactoring legacy semantics
- **Pure functions created**: 7

## Files Changed

- `tests/unit/mbse/test_prepare_hsm_engine.py` — strict-TDD coverage for deterministic engine-view lowering
- `tests/unit/mbse/test_generated_engine.py` — strict-TDD coverage for deterministic engine source rendering and private wrapper dispatch
- `tests/unit/mbse/test_hsm_runtime.py` — strict-TDD coverage for runtime API semantics and builder input forms
- `src/mbse/domain/models.py` — frozen engine-view transition/view contracts plus runtime snapshot dataclass
- `src/mbse/application/prepare_hsm_engine.py` — pure lowering pipeline from validated `HsmDocument` to stable engine indexes
- `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` — private QPC-style generated engine template with one handler per state
- `src/mbse/infrastructure/generated_engine.py` — in-memory render/load wrapper that keeps generated symbols private
- `src/mbse/application/hsm_runtime.py` — handwritten runtime facade, context storage, ancestry resolution, and event dispatch
- `src/mbse/application/build_hsm_runtime.py` — top-level runtime builder from validated JSON or `HsmDocument`
- `tests/integration/test_generated_hsm_engine.py` — public-API integration coverage for JSON -> generated engine -> runtime flow and deterministic replay
- `src/mbse/application/__init__.py` — stable application exports for the runtime builder and handwritten facade
- `openspec/changes/generated-hsm-engine/tasks.md` — Work Unit 1 tasks marked complete and workload decision recorded
- `openspec/changes/generated-hsm-engine/tasks.md` — Work Unit 2 tasks marked complete for the generated boundary/runtime facade slice
- `openspec/changes/generated-hsm-engine/tasks.md` — Work Unit 3 tasks marked complete for integration, package wiring, and scoped batch verification

## Verification Commands

- `pytest tests/unit/mbse/test_hsm_validation.py tests/unit/mbse/test_hsm_render_view.py` — safety net passed `11 passed`
- `pytest tests/unit/mbse/test_prepare_hsm_engine.py` — RED failed during collection with `ModuleNotFoundError: No module named 'mbse.application.prepare_hsm_engine'`
- `pytest tests/unit/mbse/test_prepare_hsm_engine.py` — GREEN passed `2 passed`
- `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_hsm_validation.py tests/unit/mbse/test_hsm_render_view.py` — Work Unit 1 verification passed `13 passed`
- `pytest tests/unit/mbse/test_generated_engine.py tests/unit/mbse/test_hsm_runtime.py` — RED failed during collection with missing generated/runtime modules, then GREEN passed `5 passed`
- `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_generated_engine.py tests/unit/mbse/test_hsm_runtime.py` — Work Unit 2 verification passed `7 passed`
- `pytest tests/unit/mbse/test_hsm_runtime.py` — Work Unit 3 safety net passed `3 passed`
- `pytest tests/integration/test_generated_hsm_engine.py` — RED failed `2 failed` because the public application import exposed the module instead of the builder callable
- `pytest tests/integration/test_generated_hsm_engine.py` — GREEN passed `2 passed`
- `pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_hsm_runtime.py tests/integration/test_generated_hsm_engine.py` — Work Unit 3 verification passed `7 passed`

## Deviations

- None — implementation matches Work Unit 3 boundaries and still keeps generated internals off the public surface.

## Notes

- The lowering view intentionally buckets only event-driven transitions because this slice prepares handler data for `send_event(event_id)` semantics only.
- Eventless transitions remain in the validated source model but are not exposed in the Work Unit 1 runtime-event buckets.
- `on_entry` and `on_exit` metadata remain untouched and inert in this slice.
- The generated engine wrapper precomputes deterministic Python literals so the Jinja template stays focused on structure instead of formatting logic.
- The runtime resolves transition targets by following local initials first and then rebuilding ancestry from `PARENTS`, which keeps parent fallback and forced-state logic deterministic.
- The public `mbse.application` package now re-exports only the stable handwritten runtime entrypoints needed by consumers; generated engine helpers remain internal.
