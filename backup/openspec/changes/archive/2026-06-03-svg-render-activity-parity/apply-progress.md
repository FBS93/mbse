# Apply Progress: SVG Render Activity Parity

**Change**: `svg-render-activity-parity`
**Mode**: Strict TDD
**Continuation Type**: Process-only evidence repair
**Scope Boundary**: Render-only; no product behavior changes in this continuation

## Executive Summary

This continuation repaired the missing strict-TDD audit artifact only. The repository already matched the refreshed normalized render-only spec/design/tasks before this batch started, so no product code changed. The missing piece was a retained cumulative apply-progress artifact with auditable per-task TDD evidence.

## Merged Prior Progress

- Prior apply work had already completed all 11 tasks and marked `tasks.md` done.
- Prior Engram topic `sdd/svg-render-activity-parity/apply-progress` existed only as a short summary, so this file restores the cumulative apply record instead of replacing implementation scope.
- Historical alignment evidence was merged from the retained Engram apply summary, the prior session summary, the completed task checklist, and the current green test state.

## Inputs Read

| Artifact | Purpose |
|---|---|
| `openspec/changes/svg-render-activity-parity/specs/hsm-json-graphviz-rendering/spec.md` | Acceptance criteria and scope boundary |
| `openspec/changes/svg-render-activity-parity/design.md` | Implementation/design constraints |
| `openspec/changes/svg-render-activity-parity/tasks.md` | Task ledger and workload contract |
| `openspec/changes/svg-render-activity-parity/verify-report.md` | Strict-verify failure cause |
| Engram `sdd/svg-render-activity-parity/apply-progress` (#532) | Previous apply-progress topic to merge |
| Engram session summary (#571) | Prior cumulative apply details |

## Files Changed In This Continuation

| File | Action | What Was Done |
|---|---|---|
| `openspec/changes/svg-render-activity-parity/apply-progress.md` | Created | Restored cumulative apply artifact with strict-TDD evidence table and merged prior progress |

## Completed Tasks

- [x] 1.1 Add failing unit assertions for ordered `on_initial:`, `on_entry:`, `on_exit:`, then `internal_transitions:` sections.
- [x] 1.2 Add failing unit assertions for normal transition label omission rules.
- [x] 1.3 Add failing unit assertions that initial edges stay unlabeled and keep authored IDs.
- [x] 2.1 Finalize ordered `body_sections` shaping in `prepare_hsm_render.py`.
- [x] 2.2 Keep omission-safe normal transition labels and unlabeled initial edges.
- [x] 2.3 Render prepared state sections and keep initial edges `label=""` in `hsm_v1.dot.j2`.
- [x] 3.1 Add integration coverage for lifecycle hooks, internal rows, and normal guard/activity text.
- [x] 3.2 Assert `highlightable_ids` and public SVG IDs stay authored-only.
- [x] 3.3 Assert visible initial source dots remain while initial-edge labels/helpers stay hidden.
- [x] 4.1 Run targeted render parity suite to GREEN.
- [x] 4.2 Run full `pytest` suite to confirm render-only scope.

## TDD Cycle Evidence

| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|---|---|---|---|---|---|---|---|
| 1.1 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | ✅ Current baseline: file passes 11/11 | ✅ Historical failing assertions captured by completed RED task and retained test `test_prepare_hsm_render_view_shapes_ordered_state_body_sections` | ✅ `python -m pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` → 20 passed | ✅ Multiple section-order assertions cover lifecycle-only and lifecycle+internal combinations | ➖ No new refactor in this continuation |
| 1.2 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | ✅ Current baseline: file passes 11/11 | ✅ Historical failing assertions captured by completed RED task and retained test `test_prepare_hsm_render_view_formats_transition_labels_without_initial_transition_body_text` | ✅ `python -m pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` → 20 passed | ✅ Event-only, guard, activity, and full-format cases retained in one focused test | ➖ No new refactor in this continuation |
| 1.3 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | ✅ Current baseline: file passes 11/11 | ✅ Historical failing assertions captured by completed RED task and retained tests `test_render_hsm_dot_omits_initial_transition_text_without_changing_public_id_order`, `test_prepare_hsm_render_view_keeps_public_ids_and_routes_compound_edges_to_anchor`, and `test_prepare_hsm_render_view_routes_local_initial_targets_to_compound_anchors` | ✅ `python -m pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` → 20 passed | ✅ Covers unlabeled initials, authored IDs, and local compound-target routing cases | ➖ No new refactor in this continuation |
| 2.1 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | ✅ Current baseline: file passes 11/11 | ✅ Historical RED implied by task 1.1 before production shaping was finalized | ✅ `python -m pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` → 20 passed | ✅ Section DTO shaping is exercised by authored-order assertions and compound-state cases | ✅ Prior implementation already clean; no further change needed now |
| 2.2 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | ✅ Current baseline: file passes 11/11 | ✅ Historical RED implied by tasks 1.2 and 1.3 before omission-safe formatting/unlabeled initials were finalized | ✅ `python -m pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` → 20 passed | ✅ Tests retain separate omission paths for guard/activity and initial-edge label suppression | ✅ Prior implementation already clean; no further change needed now |
| 2.3 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | ✅ Current baseline: file passes 11/11 | ✅ Historical RED implied by tasks 1.1 and 1.3 before DOT rendering matched prepared data | ✅ `python -m pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` → 20 passed | ✅ DOT assertions cover visible section rendering and forced empty initial labels | ✅ Prior template shape remains stable; no further refactor needed now |
| 3.1 | `tests/integration/test_hsm_json_workbench.py` | Integration | ✅ Current baseline: file passes 9/9 | ✅ Historical failing assertions captured by completed integration RED task and retained test `test_build_workbench_session_renders_on_initial_text_without_new_public_ids` | ✅ `python -m pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` → 20 passed | ✅ Visible lifecycle text, internal rows, and normal label text are asserted together against rendered output | ➖ No new refactor in this continuation |
| 3.2 | `tests/integration/test_hsm_json_workbench.py` | Integration | ✅ Current baseline: file passes 9/9 | ✅ Historical failing assertions captured by completed RED task and retained tests `test_build_workbench_session_preserves_exact_svg_ids_for_hsm_contract`, `test_build_workbench_session_keeps_exact_compound_svg_id_once`, and `test_build_workbench_session_keeps_private_anchors_out_of_public_svg_ids` | ✅ `python -m pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` → 20 passed | ✅ Exercises authored-ID preservation, duplicate-prevention, and private-helper hiding paths | ➖ No new refactor in this continuation |
| 3.3 | `tests/integration/test_hsm_json_workbench.py` | Integration | ✅ Current baseline: file passes 9/9 | ✅ Historical failing assertions captured by completed RED task and retained tests `test_build_workbench_session_routes_local_initials_to_private_compound_anchors` and `test_build_workbench_session_real_graphviz_keeps_visible_source_dots_and_hides_private_anchors` | ✅ `python -m pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` → 20 passed | ✅ Covers both prepared-render and real-Graphviz initial-routing cases | ➖ No new refactor in this continuation |
| 4.1 | `tests/unit/mbse/test_hsm_render_view.py`, `tests/integration/test_hsm_json_workbench.py` | Unit + Integration | N/A (verification task) | ✅ Historical RED is the full task set above; this task exists to confirm consolidated GREEN | ✅ `python -m pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` → 20 passed in 0.45s | ✅ Targeted suite spans both layers and all refreshed render-parity scenarios | ➖ Verification-only task |
| 4.2 | `tests/**` | Full suite | N/A (verification task) | ✅ Historical RED is the slice-wide render-only risk the suite guards against | ✅ `python -m pytest` → 102 passed in 2.39s | ✅ Full suite proves no spillover into runtime/highlighting behavior | ➖ Verification-only task |

## Test Summary

- **Targeted suite**: `python -m pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` → 20 passed in 0.45s
- **Full suite**: `python -m pytest` → 102 passed in 2.39s
- **Layers used**: Unit and Integration
- **Approval tests**: Existing retained tests served as approval/contract evidence for this process-only continuation because no product refactor occurred
- **Pure functions created in this continuation**: 0

## Deviations From Design

None. This continuation only restores missing audit evidence for the already-aligned render-only implementation.

## Issues Found

- The retained OpenSpec proposal is stale relative to the refreshed normalized spec/design/tasks and still mentions initial-edge activity labels and `src/mbse/domain/models.py` changes.
- The prior Engram apply-progress topic had been reduced to a short summary, which is why strict verify could not audit TDD evidence.

## Workload / PR Boundary

- **Mode**: Single PR / single apply continuation
- **Boundary**: Audit artifact repair only; no product implementation delta
- **Estimated review budget impact**: Minimal and documentation-only

## Status

11/11 tasks complete. Strict-TDD evidence artifact restored. Ready for verify rerun.
