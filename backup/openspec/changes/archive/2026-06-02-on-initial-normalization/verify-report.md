## Verification Report

**Change**: on-initial-normalization
**Version**: N/A
**Mode**: Strict TDD

### Completeness
| Metric | Value |
|--------|-------|
| Tasks total | 11 |
| Tasks complete | 11 |
| Tasks incomplete | 0 |

### Build & Tests Execution
**Build**: ✅ Passed
```text
$ python -m compileall src
Listing 'src'...
Listing 'src/mbse'...
Listing 'src/mbse/application'...
Listing 'src/mbse/cli'...
Listing 'src/mbse/domain'...
Listing 'src/mbse/infrastructure'...
Listing 'src/mbse/infrastructure/templates'...
Listing 'src/mbse/web'...
Listing 'src/mbse/web/static'...
```

**Tests**: ✅ 148 passed across the executed verification commands / ❌ 0 failed / ⚠️ 0 skipped
```text
$ python -m pytest tests/unit/mbse/test_hsm_validation.py tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_generated_engine.py tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /workspaces/MBSE
configfile: pyproject.toml
collected 46 items

tests/unit/mbse/test_hsm_validation.py ...........                       [ 23%]
tests/unit/mbse/test_prepare_hsm_engine.py .....                         [ 34%]
tests/unit/mbse/test_generated_engine.py ....                            [ 43%]
tests/unit/mbse/test_hsm_runtime.py ......                               [ 56%]
tests/unit/mbse/test_hsm_render_view.py ...........                      [ 80%]
tests/integration/test_hsm_json_workbench.py .........                   [100%]

============================== 46 passed in 0.58s ==============================

$ python -m pytest
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /workspaces/MBSE
configfile: pyproject.toml
testpaths: tests
collected 102 items

tests/integration/test_generated_hsm_engine.py ....                      [  3%]
tests/integration/test_hsm_json_workbench.py .........                   [ 12%]
tests/integration/test_mbse_session_build.py ..                          [ 14%]
tests/integration/test_mbse_workbench.py ............................    [ 42%]
tests/unit/mbse/test_cli_main.py ...                                     [ 45%]
tests/unit/mbse/test_generated_engine.py ....                            [ 49%]
tests/unit/mbse/test_hsm_render_view.py ...........                      [ 59%]
tests/unit/mbse/test_hsm_runtime.py ......                               [ 65%]
tests/unit/mbse/test_hsm_validation.py ...........                       [ 76%]
tests/unit/mbse/test_prepare_hsm_engine.py .....                         [ 81%]
tests/unit/mbse/test_svg_contract.py ..                                  [ 83%]
tests/unit/mbse/test_test_hsm_demo.py ..                                 [ 85%]
tests/unit/mbse/test_validation.py ..........                            [ 95%]
tests/unit/mbse/test_web_runtime_bridge.py .....                         [100%]

============================= 102 passed in 2.97s ==============================
```

**Coverage**: ➖ Not available

### TDD Compliance
| Check | Result | Details |
|-------|--------|---------|
| TDD Evidence reported | ✅ | Engram topic `sdd/on-initial-normalization/apply-progress` now includes a `## TDD Cycle Evidence` table with four task-group rows covering tasks 1.1-4.3. |
| All tasks have tests | ✅ | All 11 completed tasks are covered by the table's mapped test files, with 9 referenced files and 62 collected tests across the changed verification scope. |
| RED confirmed (tests exist) | ✅ | Every test file named in the TDD table exists in the repo: validation, engine prep, generated engine, runtime, render, workbench integration, generated-engine integration, demo, and schema/contract regression files. |
| GREEN confirmed (tests pass) | ✅ | The targeted verification suite passes now (`46/46`), and the full regression suite also passes (`102/102`), confirming the table's GREEN claims against runtime execution. |
| Triangulation adequate | ✅ | The task rows map to multiple scenarios across validation, runtime ordering, engine metadata, render DOT/SVG output, fixture/demo behavior, and regression coverage; no single trivial assertion row was used to justify a multi-scenario requirement. |
| Safety Net for modified files | ✅ | Each task-group row reports baseline or regression-suite safety-net evidence (`45/45` baseline targeted suite for phases 1-3, final targeted/full regression runs for phase 4), and the referenced files are modified-existing tests rather than unexplained `N/A (new)` rows. |

**TDD Compliance**: 6/6 checks passed

---

### Test Layer Distribution
| Layer | Tests | Files | Tools |
|-------|-------|-------|-------|
| Unit | 49 | 7 | pytest |
| Integration | 13 | 2 | pytest |
| E2E | 0 | 0 | not installed |
| **Total** | **62** | **9** | |

---

### Changed File Coverage
Coverage analysis skipped — no coverage tool detected (`python -m pytest --cov=src/mbse ...` failed because `pytest-cov` is not installed and `--cov` is unrecognized).

---

### Assertion Quality
**Assertion quality**: ✅ All assertions in the changed validation/runtime/render/example files check real behavior; no tautologies, ghost loops, smoke-only assertions, or mock-heavy trivial tests were found during manual audit.

---

### Quality Metrics
**Linter**: ➖ Not available (`python -m ruff --version` failed: module not installed)
**Type Checker**: ➖ Not available (`python -m mypy --version` failed: module not installed)

### Spec Compliance Matrix
| Requirement | Scenario | Test | Result |
|-------------|----------|------|--------|
| Minimal Hierarchical Execution Semantics | Start follows the full initial chain | `tests/unit/mbse/test_hsm_runtime.py::test_hsm_runtime_init_executes_entry_and_initial_order`; `tests/integration/test_generated_hsm_engine.py::test_build_hsm_runtime_replays_executable_parity_trace_deterministically` | ✅ COMPLIANT |
| Minimal Hierarchical Execution Semantics | Guard-false handling bubbles outward | `tests/unit/mbse/test_hsm_runtime.py::test_hsm_runtime_guard_false_bubbles_leaf_to_root_before_taking_parent_transition` | ✅ COMPLIANT |
| Minimal Hierarchical Execution Semantics | Handled event without transition still runs activities | `tests/unit/mbse/test_hsm_runtime.py::test_hsm_runtime_internal_transition_handles_event_without_state_change`; `tests/integration/test_generated_hsm_engine.py::test_build_hsm_runtime_replays_executable_parity_trace_deterministically` | ✅ COMPLIANT |
| Minimal Hierarchical Execution Semantics | Self transition re-enters the source state | `tests/unit/mbse/test_hsm_runtime.py::test_hsm_runtime_self_transition_reenters_source_in_order` | ✅ COMPLIANT |
| Minimal Hierarchical Execution Semantics | Ancestor and descendant paths preserve `example_hsm` ordering | `tests/unit/mbse/test_hsm_runtime.py::test_hsm_runtime_preserves_ancestor_and_descendant_transition_ordering`; `tests/integration/test_generated_hsm_engine.py::test_build_hsm_runtime_replays_reference_parity_sequence_deterministically` | ✅ COMPLIANT |
| Executable Behavior Model Contract | State lifecycle slots are declared distinctly | `tests/unit/mbse/test_hsm_validation.py::test_validate_hsm_document_accepts_behavioral_metadata_without_runtime`; `tests/unit/mbse/test_validation.py::test_hsm_schema_accepts_callable_refs_in_lifecycle_internal_and_transition_slots` | ✅ COMPLIANT |
| Executable Behavior Model Contract | Initial objects stay structural only | `tests/unit/mbse/test_hsm_validation.py::test_load_hsm_document_rejects_executable_initial_activities` | ✅ COMPLIANT |
| Executable Behavior Model Contract | Event handling declares activities and guard | `tests/unit/mbse/test_hsm_validation.py::test_validate_hsm_document_accepts_behavioral_metadata_without_runtime`; `tests/unit/mbse/test_prepare_hsm_engine.py::test_prepare_hsm_engine_view_builds_lifecycle_and_initial_resolution_plans` | ✅ COMPLIANT |
| Executable Behavior Model Contract | Internal transitions are authored without a target | `tests/unit/mbse/test_hsm_validation.py::test_load_hsm_document_rejects_transition_only_fields_on_internal_transition`; `tests/unit/mbse/test_validation.py::test_hsm_schema_requires_event_id_for_internal_transitions` | ✅ COMPLIANT |
| Canonical HSM JSON v1 Document | Minimal FSM-form document is valid | `tests/unit/mbse/test_hsm_validation.py::test_load_hsm_document_accepts_minimal_fsm_document`; `tests/unit/mbse/test_hsm_validation.py::test_load_hsm_schema_accepts_minimal_hsm_v1_document` | ✅ COMPLIANT |
| Canonical HSM JSON v1 Document | Behavioral metadata is valid | `tests/unit/mbse/test_hsm_validation.py::test_validate_hsm_document_accepts_behavioral_metadata_without_runtime`; `tests/unit/mbse/test_validation.py::test_hsm_schema_accepts_callable_refs_in_lifecycle_internal_and_transition_slots` | ✅ COMPLIANT |
| Supported Hierarchy And Initials For v1 | Hierarchical state with local initial is valid | `tests/unit/mbse/test_hsm_render_view.py::test_prepare_hsm_render_view_preserves_depth_first_and_authored_order` | ✅ COMPLIANT |
| Supported Hierarchy And Initials For v1 | Invalid or executable initial is rejected | `tests/unit/mbse/test_hsm_validation.py::test_load_hsm_document_rejects_invalid_local_initial_target`; `tests/unit/mbse/test_hsm_validation.py::test_load_hsm_document_rejects_executable_initial_activities` | ✅ COMPLIANT |
| Deterministic Prepared Render Contract | Same input yields same prepared output | `tests/integration/test_hsm_json_workbench.py::test_build_workbench_session_accepts_hsm_json_and_emits_deterministic_prepared_output` | ✅ COMPLIANT |
| Deterministic Prepared Render Contract | Top summary banner is absent | `tests/unit/mbse/test_hsm_render_view.py::test_prepare_hsm_render_view_omits_top_summary_blocks_and_preserves_ids`; `tests/integration/test_hsm_json_workbench.py::test_build_workbench_session_preserves_exact_svg_ids_for_hsm_contract` | ✅ COMPLIANT |
| Deterministic Prepared Render Contract | Every highlightable element keeps its authored ID exactly | `tests/unit/mbse/test_hsm_render_view.py::test_render_hsm_dot_uses_template_with_exact_authored_ids`; `tests/integration/test_hsm_json_workbench.py::test_build_workbench_session_preserves_exact_svg_ids_for_hsm_contract`; `tests/integration/test_hsm_json_workbench.py::test_build_workbench_session_keeps_distinct_ids_when_labels_repeat` | ✅ COMPLIANT |
| Deterministic Prepared Render Contract | State-owned hooks render without competing initial text | `tests/unit/mbse/test_hsm_render_view.py::test_prepare_hsm_render_view_shapes_ordered_state_body_sections`; `tests/unit/mbse/test_hsm_render_view.py::test_prepare_hsm_render_view_formats_transition_labels_without_initial_transition_body_text`; `tests/integration/test_hsm_json_workbench.py::test_build_workbench_session_renders_on_initial_text_without_new_public_ids` | ✅ COMPLIANT |
| Deterministic Prepared Render Contract | Initial source pseudostates stay visible | `tests/unit/mbse/test_hsm_render_view.py::test_render_hsm_dot_uses_template_with_exact_authored_ids`; `tests/integration/test_hsm_json_workbench.py::test_build_workbench_session_real_graphviz_keeps_visible_source_dots_and_hides_private_anchors` | ✅ COMPLIANT |
| Deterministic Prepared Render Contract | Private target and compound routing anchors stay private | `tests/unit/mbse/test_hsm_render_view.py::test_prepare_hsm_render_view_keeps_public_ids_and_routes_compound_edges_to_anchor`; `tests/integration/test_hsm_json_workbench.py::test_build_workbench_session_keeps_private_anchors_out_of_public_svg_ids` | ✅ COMPLIANT |
| Deterministic Prepared Render Contract | Root and local initials route cleanly to compound targets | `tests/unit/mbse/test_hsm_render_view.py::test_prepare_hsm_render_view_routes_local_initial_targets_to_compound_anchors`; `tests/integration/test_hsm_json_workbench.py::test_build_workbench_session_routes_local_initials_to_private_compound_anchors` | ✅ COMPLIANT |

**Compliance summary**: 20/20 scenarios compliant

### Correctness (Static Evidence)
| Requirement | Status | Notes |
|------------|--------|-------|
| Initial objects are structural-only across schema and model | ✅ Implemented | `src/mbse/domain/hsm_schema_v1.json`, `src/mbse/domain/models.py`, and `src/mbse/domain/validation.py` all restrict initials to `id` and `target_id` only. |
| Prepared/generated engine initials are metadata-only | ✅ Implemented | `src/mbse/application/prepare_hsm_engine.py`, `src/mbse/infrastructure/generated_engine.py`, and `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` keep `initial_target_ids` and `initial_transition_ids` but expose no `initial_rows_by_owner_id` or `HsmPreparedEngineInitialRow`. |
| Runtime executes only state-owned lifecycle behavior during init descent | ✅ Implemented | `src/mbse/application/hsm_runtime.py` runs `on_entry` plus state-owned `on_initial` during root/nested descent and never executes initial-object activities. |
| Render output removes competing initial-transition behavior text | ✅ Implemented | `src/mbse/application/prepare_hsm_render.py` emits `on_initial:`, `on_entry:`, `on_exit:`, and internal transitions only; initial edge labels remain `None`. |
| Example/fixture contract matches normalized semantics | ✅ Implemented | `test_hsm/hsm.json` authors `on_initial` on `session` and no longer authors any `initial.activities` field. |

### Coherence (Design)
| Decision | Followed? | Notes |
|----------|-----------|-------|
| Remove `HsmInitialTransition.activities` entirely | ✅ Yes | `HsmInitialTransition` now has only `id` and `target_id`, and validation rejects extra executable fields on initials. |
| Reduce prepared engine metadata to `initial_target_ids` + `initial_transition_ids` | ✅ Yes | Engine-preparation and generated-engine layers keep those two maps and no initial activity row abstraction. |
| Run only state-owned hooks during descent | ✅ Yes | `init()` and `_descend_initial_chain()` execute `on_entry` and `_run_on_initial()` only. |
| Remove `initial_transition:` render body text | ✅ Yes | State body formatting contains lifecycle and internal-transition sections only; render tests confirm `initial_transition:` never appears. |

### Issues Found
**CRITICAL**: None.

**WARNING**:
- Coverage analysis could not run because `pytest-cov` is not installed in this environment.
- Ruff quality checks could not run because `ruff` is not installed in this environment.
- Type-checker verification could not run because `mypy` is not installed in this environment.

**SUGGESTION**: None.

### Verdict
PASS WITH WARNINGS
Implementation behavior matches the proposal, both delta specs, the design, and all completed tasks; strict-TDD evidence is now present and cross-checked against passing runtime tests, with only non-blocking tooling gaps for coverage/lint/type metrics.
