# Apply Progress: hsm-json-graphviz-rendering

## Scope

- Delivery mode: chained PR slice
- Chain strategy: stacked-to-main
- Current work unit: Work Unit 3 / workbench integration + SVG ID contract verification
- Boundary: accept HSM JSON through the existing session-build entrypoint, emit the same prepared-document/session artifacts, preserve authored SVG IDs exactly, and keep CLI/web/runtime boundaries unchanged
- Follow-up batch: post-verify critical fix slice for schema artifact + duplicate-label identity evidence
- Follow-up boundary: add one concrete HSM v1 JSON Schema artifact, wire it into structural validation, prove duplicate labels stay distinct by authored IDs, and keep the downstream SVG/runtime boundaries unchanged

## Completed Tasks

- [x] 1.1 RED: add `tests/unit/mbse/test_hsm_validation.py` for valid minimal HSM, duplicate IDs, bad refs, invalid local initials, and unsupported runtime-like fields from spec scenarios.
- [x] 1.2 GREEN: extend `src/mbse/domain/models.py` with HSM v1 document/value types and a prepared render-view type that carries authored order explicitly.
- [x] 1.3 GREEN: extend `src/mbse/domain/validation.py` with `load_hsm_document()` and `validate_hsm_document()` enforcing exact IDs, global uniqueness, direct-child local initials, and additional-properties rejection.
- [x] 1.4 REFACTOR: keep prepared-document validation intact while isolating HSM validation helpers in `src/mbse/domain/validation.py`; reject runtime/history/orthogonal constructs explicitly.
- [x] 4.1 Run batch A after Unit 1: `pytest tests/unit/mbse/test_hsm_validation.py tests/unit/mbse/test_validation.py`.
- [x] 2.1 RED: add `tests/unit/mbse/test_hsm_render_view.py` for depth-first state order, authored transition order, `open_evt(source)` formatting, annotation blocks, and ordered `highlightable_ids`.
- [x] 2.2 GREEN: create `src/mbse/application/prepare_hsm_render.py` to flatten states, resolve initials/transitions, assemble display strings, and return one deterministic render view.
- [x] 2.3 GREEN: create `src/mbse/infrastructure/templates/hsm_v1.dot.j2` with only presentation logic for states, initials, transitions, events, variables, `on_entry`, and `on_exit`.
- [x] 2.4 GREEN: create `src/mbse/infrastructure/dot_template.py` and minimally update `pyproject.toml` to introduce Jinja2 only for loading/rendering `hsm_v1.dot.j2`.
- [x] 4.2 Run batch B after Unit 2: `pytest tests/unit/mbse/test_hsm_render_view.py tests/unit/mbse/test_hsm_validation.py`.
- [x] 3.1 RED: add `tests/integration/test_hsm_json_workbench.py` covering JSON -> DOT -> SVG determinism and exact downstream SVG IDs for states, transitions, and initials.
- [x] 3.2 GREEN: update `src/mbse/application/build_session.py` to accept HSM JSON input through the new validation/preparation/template path while preserving `PreparedGraphvizDocument` output and current session contract.
- [x] 3.3 REFACTOR: keep CLI/web/runtime boundaries unchanged in `src/mbse/cli/main.py` and related callers; do not add execution semantics, editing, or alternate inputs beyond this adapter.
- [x] 4.3 Run batch C after Unit 3: `pytest tests/integration/test_hsm_json_workbench.py tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py`.
- [x] 5.1 RED/GREEN: add a real HSM v1 JSON Schema artifact plus a loader test, then wire schema validation into `load_hsm_document()` so the JSON document remains the structural source of truth.
- [x] 5.2 RED/GREEN: add duplicate-label integration coverage proving distinct authored IDs survive prepared-document generation and rendered SVG output unchanged.
- [x] 5.3 Run post-verify fix batch: `pytest tests/unit/mbse/test_hsm_validation.py tests/unit/mbse/test_validation.py tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py`.

## Remaining Tasks

- None.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 | `tests/unit/mbse/test_hsm_validation.py` | Unit | ✅ `pytest tests/unit/mbse/test_validation.py` passed `7 passed` before modifying shared validation files | ✅ `pytest tests/unit/mbse/test_hsm_validation.py` failed during collection with `ImportError: cannot import name 'HsmDocument'` after writing tests first | ✅ `pytest tests/unit/mbse/test_hsm_validation.py` passed `6 passed` after adding HSM document types and validation | ✅ Covered minimal valid input, behavioral metadata, duplicate global IDs, broken references, invalid local initial target, and unsupported runtime-like fields | ✅ Kept prepared-document validation unchanged and moved HSM checks into focused helper functions |
| 1.2 | `tests/unit/mbse/test_hsm_validation.py` | Unit | ✅ Same `7 passed` safety net protected existing `models.py`/`validation.py` behavior | ✅ Same RED collection failure proved the HSM dataclasses and render-view type did not exist yet | ✅ Same targeted command passed `6 passed` with `HsmDocument`, nested value objects, and `HsmPreparedRenderView` added | ✅ Behavioral metadata test exercises variables, event parameters, `on_entry`, `on_exit`, and root initial data through the real parser | ✅ Dataclasses stay immutable and narrowly scoped for later render preparation |
| 1.3 | `tests/unit/mbse/test_hsm_validation.py` | Unit | ✅ Same `7 passed` safety net | ✅ RED already established by missing HSM imports before implementation | ✅ Same targeted command passed `6 passed` with `load_hsm_document()` and `validate_hsm_document()` implemented | ✅ Different failing scenarios force distinct validation paths: duplicate IDs, missing state target, and invalid local initial target | ✅ Parsing, additional-property rejection, ID validation, and reference checks are isolated in small helpers |
| 1.4 | `tests/unit/mbse/test_hsm_validation.py`, `tests/unit/mbse/test_validation.py` | Unit | ✅ `pytest tests/unit/mbse/test_validation.py` passed `7 passed` before refactoring shared validation code | ✅ RED remained the HSM test collection failure before the helpers existed | ✅ `pytest tests/unit/mbse/test_hsm_validation.py tests/unit/mbse/test_validation.py` passed `13 passed` after refactoring | ✅ Unsupported `history` property and preserved prepared-document checks exercise two different code paths in the shared module | ✅ Explicit additional-property rejection now blocks runtime/history-style fields without touching the downstream exact-ID validator |
| 4.1 | `tests/unit/mbse/test_hsm_validation.py`, `tests/unit/mbse/test_validation.py` | Verify | ✅ baseline already recorded above | ✅ Verification scope was fixed by the tasks artifact before execution | ✅ `pytest tests/unit/mbse/test_hsm_validation.py tests/unit/mbse/test_validation.py` passed `13 passed` | ➖ Triangulation skipped: verification task re-executes the already-authored RED/GREEN coverage | ➖ None needed |
| 2.1 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | ✅ `pytest tests/unit/mbse/test_hsm_validation.py` passed `6 passed` before modifying shared HSM model contracts | ✅ `pytest tests/unit/mbse/test_hsm_render_view.py` failed during collection with `ModuleNotFoundError: No module named 'mbse.application.prepare_hsm_render'` after writing tests first | ✅ `pytest tests/unit/mbse/test_hsm_render_view.py` passed `3 passed` after adding the render-prep and template path | ✅ Covered depth-first state order, initial/transition authored order, exact `open_evt(source)` formatting, annotation blocks, and ordered `highlightable_ids` | ✅ The tests forced a small prepared render-view contract before any workbench integration |
| 2.2 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | ✅ Same `6 passed` safety net protected existing HSM validation behavior while extending shared dataclasses | ✅ Same RED collection failure proved the preparation entry point did not exist yet | ✅ Same targeted command passed `3 passed` with `prepare_hsm_render_view()` flattening states, resolving initials, and assembling blocks | ✅ Hierarchical and flat inputs exercise different traversal paths plus event/no-event transition formatting | ✅ Preparation logic stays pure and deterministic with authored order preserved end-to-end |
| 2.3 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | N/A (new) | ✅ Same RED test file required a template-backed DOT renderer before implementation | ✅ Same targeted command passed `3 passed` with `hsm_v1.dot.j2` emitting authored IDs and presentation-only labels | ✅ DOT assertions cover state IDs, initial IDs, transition IDs, and global variables/events blocks from the rendered template | ➖ None needed |
| 2.4 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | N/A (new) | ✅ Same RED test file required `mbse.infrastructure.dot_template` before implementation | ✅ Same targeted command passed `3 passed` with explicit Jinja2 `FileSystemLoader` rendering `hsm_v1.dot.j2` | ✅ Re-running the same preparation+render path against hierarchical input and metadata-heavy input forced both loader and template usage | ✅ Jinja2 stayed isolated to one infrastructure module plus the template file and a minimal `pyproject.toml` dependency |
| 4.2 | `tests/unit/mbse/test_hsm_render_view.py`, `tests/unit/mbse/test_hsm_validation.py` | Verify | ✅ baseline already recorded above | ✅ Verification scope was fixed by the tasks artifact before execution | ✅ `pytest tests/unit/mbse/test_hsm_render_view.py tests/unit/mbse/test_hsm_validation.py` passed `9 passed` | ➖ Triangulation skipped: verification task re-executes the already-authored RED/GREEN coverage | ➖ None needed |
| 3.1 | `tests/integration/test_hsm_json_workbench.py` | Integration | ✅ `pytest tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py` passed `5 passed` before modifying the shared session-build path | ✅ `pytest tests/integration/test_hsm_json_workbench.py` failed with `ValidationError: Prepared document missing required field 'dot_source'.` after writing the HSM JSON integration tests first | ✅ `pytest tests/integration/test_hsm_json_workbench.py` passed `2 passed` after wiring the HSM JSON adapter into `build_workbench_session()` | ✅ Covered two distinct cases: deterministic prepared-document output across repeated runs and exact authored SVG IDs for states, transitions, and initials | ✅ The new coverage locked the adapter boundary before changing any CLI or web callers |
| 3.2 | `tests/integration/test_hsm_json_workbench.py` | Integration | ✅ Same `5 passed` safety net protected the existing prepared-document and workbench flows | ✅ Same RED failure proved the session builder still only accepted prepared Graphviz JSON before implementation | ✅ Same targeted command passed `2 passed` after validating HSM JSON, preparing the render view, rendering DOT, and serializing a canonical `prepared-document.json` artifact | ✅ Repeated-run and exact-ID scenarios forced both the new HSM input path and the legacy prepared-document path to coexist safely | ✅ Extracted `_load_session_document()` so the adapter stays narrow and still returns `PreparedGraphvizDocument` to the existing downstream flow |
| 3.3 | `tests/integration/test_hsm_json_workbench.py`, `tests/integration/test_mbse_session_build.py`, `tests/integration/test_mbse_workbench.py` | Integration | ✅ Same `5 passed` safety net protected CLI/workbench callers before touching `build_session.py` | ✅ RED remained the failing HSM integration file until the adapter existed | ✅ `pytest tests/integration/test_hsm_json_workbench.py tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py` passed `7 passed` with no CLI/web changes required | ✅ HSM JSON runs and legacy prepared-document runs now exercise different entry conditions against the same session/workbench contract | ✅ CLI/web/runtime boundaries stayed unchanged because the new logic is isolated inside `build_session.py` |
| 4.3 | `tests/integration/test_hsm_json_workbench.py`, `tests/integration/test_mbse_session_build.py`, `tests/integration/test_mbse_workbench.py` | Verify | ✅ baseline already recorded above | ✅ Verification scope was fixed by the tasks artifact before execution | ✅ `pytest tests/integration/test_hsm_json_workbench.py tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py` passed `7 passed` | ➖ Triangulation skipped: verification task re-executes the already-authored RED/GREEN coverage | ➖ None needed |
| 5.1 | `tests/unit/mbse/test_hsm_validation.py` | Unit | ✅ `pytest tests/unit/mbse/test_hsm_validation.py tests/integration/test_hsm_json_workbench.py` passed `8 passed` before modifying shared validation code | ✅ `pytest tests/unit/mbse/test_hsm_validation.py tests/integration/test_hsm_json_workbench.py` failed during collection with `ModuleNotFoundError: No module named 'mbse.domain.schema'` after writing the schema-loader test first | ✅ `pytest tests/unit/mbse/test_hsm_validation.py tests/integration/test_hsm_json_workbench.py` passed `10 passed` after adding `src/mbse/domain/hsm_schema_v1.json`, `src/mbse/domain/schema.py`, and schema-backed validation in `load_hsm_document()` | ✅ Covered two distinct structural paths: the schema artifact itself accepts the minimal v1 payload, and the runtime validation path still accepts the same document after schema enforcement | ✅ Kept the semantic ID/reference checks intact while isolating the schema artifact loader and first-error translation helpers |
| 5.2 | `tests/integration/test_hsm_json_workbench.py` | Integration | ✅ Same `8 passed` safety net protected the HSM render/session path before the duplicate-label evidence was added | ✅ Same RED collection failure proved the new duplicate-label scenario test was authored before the schema loader existed | ✅ Same targeted command passed `10 passed` with duplicate labels rendering to distinct authored IDs in DOT/SVG output | ✅ The existing exact-ID scenario and the new duplicate-label scenario force two different identity cases: unique labels and repeated labels with distinct IDs | ➖ None needed |
| 5.3 | `tests/unit/mbse/test_hsm_validation.py`, `tests/unit/mbse/test_validation.py`, `tests/unit/mbse/test_hsm_render_view.py`, `tests/integration/test_hsm_json_workbench.py`, `tests/integration/test_mbse_session_build.py`, `tests/integration/test_mbse_workbench.py` | Verify | ✅ baseline already recorded above | ✅ Verification scope was fixed by the critical-fix boundary before execution | ✅ `pytest tests/unit/mbse/test_hsm_validation.py tests/unit/mbse/test_validation.py tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py` passed `25 passed` | ➖ Triangulation skipped: verification task re-executes the already-authored RED/GREEN coverage | ➖ None needed |

## Test Summary

- **Total tests written**: 13
- **Total tests passing**: 13 authored HSM tests overall; post-verify fix batch passed `25 passed`
- **Layers used**: Unit (10), Integration (3), E2E (0)
- **Approval tests**: None — existing prepared-document behavior was protected by the safety-net suite instead of rewritten
- **Pure functions created**: 15

## Files Changed

- `tests/unit/mbse/test_hsm_validation.py` — new unit coverage for HSM JSON v1 acceptance and rejection rules
- `src/mbse/domain/hsm_schema_v1.json` — concrete HSM v1 JSON Schema artifact used as the structural source of truth
- `src/mbse/domain/schema.py` — cached schema loader for the packaged HSM v1 JSON Schema artifact
- `tests/unit/mbse/test_hsm_render_view.py` — strict-TDD coverage for deterministic render prep and the minimal Jinja2 DOT path
- `src/mbse/domain/models.py` — HSM document/value-object dataclasses plus prepared render-view contract stub
- `src/mbse/application/prepare_hsm_render.py` — deterministic HSM render-view preparation and authored-order highlight ID assembly
- `src/mbse/infrastructure/dot_template.py` — explicit Jinja2 loader/render entry point for the HSM DOT template
- `src/mbse/infrastructure/templates/hsm_v1.dot.j2` — presentation-only Graphviz DOT template for HSM v1
- `pyproject.toml` — minimal render/validation dependency declarations for Jinja2 and jsonschema
- `src/mbse/domain/validation.py` — HSM loading/validation pipeline and isolated schema/reference helpers
- `tests/integration/test_hsm_json_workbench.py` — strict-TDD integration coverage for HSM JSON session building, deterministic prepared output, and exact downstream SVG IDs
- `src/mbse/application/build_session.py` — narrow HSM JSON adapter that still hands a `PreparedGraphvizDocument` into the existing render/session flow
- `openspec/changes/hsm-json-graphviz-rendering/tasks.md` — cumulative task checklist with all three work units and verification batches marked complete

## Verification Commands

- `pytest tests/unit/mbse/test_validation.py` — safety net passed `7 passed`
- `pytest tests/unit/mbse/test_hsm_validation.py` — RED failed during collection with `ImportError: cannot import name 'HsmDocument'`
- `pytest tests/unit/mbse/test_hsm_validation.py` — GREEN passed `6 passed`
- `pytest tests/unit/mbse/test_validation.py tests/unit/mbse/test_hsm_validation.py` — batch A passed `13 passed`
- `pytest tests/unit/mbse/test_hsm_validation.py` — Work Unit 2 safety net passed `6 passed`
- `pytest tests/unit/mbse/test_hsm_render_view.py` — RED failed during collection with `ModuleNotFoundError: No module named 'mbse.application.prepare_hsm_render'`
- `pytest tests/unit/mbse/test_hsm_render_view.py` — GREEN passed `3 passed`
- `pytest tests/unit/mbse/test_hsm_render_view.py tests/unit/mbse/test_hsm_validation.py` — batch B passed `9 passed`
- `pytest tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py` — Work Unit 3 safety net passed `5 passed`
- `pytest tests/integration/test_hsm_json_workbench.py` — RED failed with `ValidationError: Prepared document missing required field 'dot_source'.`
- `pytest tests/integration/test_hsm_json_workbench.py` — GREEN passed `2 passed`
- `pytest tests/integration/test_hsm_json_workbench.py tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py` — batch C passed `7 passed`
- `pytest tests/unit/mbse/test_hsm_validation.py tests/integration/test_hsm_json_workbench.py` — post-verify safety net passed `8 passed`
- `pytest tests/unit/mbse/test_hsm_validation.py tests/integration/test_hsm_json_workbench.py` — RED failed during collection with `ModuleNotFoundError: No module named 'mbse.domain.schema'`
- `pytest tests/unit/mbse/test_hsm_validation.py tests/integration/test_hsm_json_workbench.py` — GREEN passed `10 passed`
- `pytest tests/unit/mbse/test_hsm_validation.py tests/unit/mbse/test_validation.py tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py` — post-verify fix batch passed `25 passed`

## Notes

- The JSON/model document is now the source-of-truth boundary for HSM v1 structure and rejection rules.
- `src/mbse/domain/hsm_schema_v1.json` is now the concrete structural contract, and `load_hsm_document()` runs schema validation before the existing semantic ID/reference checks.
- Runtime/history-style constructs are rejected at parse time via explicit additional-property checks, which keeps v1 render-only.
- `HsmPreparedRenderView` now carries ordered state nodes, initial/transition edges, preformatted annotation blocks, and ordered `highlightable_ids`, which keeps the Jinja2 template presentation-only.
- Compound-state local initials render through non-highlightable connector nodes (`{state_id}__init`) so authored highlight IDs remain unchanged for states, transitions, and initials.
- The container image did not ship with Jinja2 preinstalled, so local verification required installing the declared dependency before running pytest.
- `build_workbench_session()` now accepts either canonical HSM JSON (`schema_version`) or an already-prepared Graphviz document, but downstream Graphviz/SVG/session behavior still works only with `PreparedGraphvizDocument` after the adapter normalizes the HSM path.
- HSM JSON inputs are serialized into a canonical `prepared-document.json` session artifact, while legacy prepared-document inputs still preserve the original file name and byte-for-byte content.
- This devcontainer did not have `jsonschema` preinstalled even though `requirements-dev.txt` declared it, so local execution required `python -m pip install --break-system-packages jsonschema` before the new schema-backed tests could run.
