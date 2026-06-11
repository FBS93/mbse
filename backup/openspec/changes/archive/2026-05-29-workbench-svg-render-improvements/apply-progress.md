# Apply Progress: Workbench SVG Render Improvements

## Implementation Progress

**Change**: `workbench-svg-render-improvements`
**Mode**: Strict TDD

### Completed Tasks
- [x] 1.1 In `tests/unit/mbse/test_hsm_render_view.py`, add RED assertions that prepared render output omits graph-level `Variables`/`Events` blocks.
- [x] 1.2 In `tests/unit/mbse/test_hsm_render_view.py`, add RED assertions for exact `title_text` and `body_lines` on flat and compound states, preserving highlightable ID order.
- [x] 1.3 In `tests/integration/test_hsm_json_workbench.py`, add RED assertions that every highlightable SVG element uses the exact authored JSON `id`, including compound parents, and that `__anchor` stays non-public.
- [x] 2.1 Update `src/mbse/domain/models.py` to replace string label fields with render-only `title_text` and `body_lines` fields on the prepared render models.
- [x] 2.2 Update `src/mbse/application/prepare_hsm_render.py` to stop populating `variables_block` / `events_block` and to build deterministic title/body data from label, `on_entry`, and `on_exit`.
- [x] 2.3 Keep depth-first state ordering, `highlightable_ids`, compound public IDs, and private `{state.id}__anchor` routing unchanged in `src/mbse/application/prepare_hsm_render.py`.
- [x] 3.1 Update `src/mbse/infrastructure/templates/hsm_v1.dot.j2` to remove any `graph [label=...]` banner emission.
- [x] 3.2 Render leaf states with HTML-like table labels that separate title from body while keeping `id="{{ state.id }}"` exact.
- [x] 3.3 Render compound clusters with the same title/body partition, preserving the cluster public ID exactly and keeping anchors private/unhighlightable.
- [x] 4.1 Batch A: run `pytest tests/unit/mbse/test_hsm_render_view.py` after Phase 1-2 to turn RED to GREEN without touching runtime files.
- [x] 4.2 Batch B: run `pytest tests/integration/test_hsm_json_workbench.py` after Phase 3 to verify exact SVG ID uniqueness and compound-state public-ID preservation.
- [x] 4.3 Batch C: run `pytest` if the targeted suites pass, then confirm no files outside the render pipeline and its tests changed.

### Files Changed
| File | Action | What Was Done |
|------|--------|---------------|
| `tests/unit/mbse/test_hsm_render_view.py` | Modified | Added RED-to-GREEN assertions for banner removal and explicit title/body render fields. |
| `tests/integration/test_hsm_json_workbench.py` | Modified | Added final-SVG exact-ID assertions for flat, duplicate-label, and compound cases, including private-anchor absence. |
| `src/mbse/domain/models.py` | Modified | Replaced prepared render label fields with `title_text` and `body_lines`. |
| `src/mbse/application/prepare_hsm_render.py` | Modified | Removed top-summary block generation and built deterministic render body lines while preserving exact-ID routing. |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modified | Rendered leaf nodes and compound clusters with a shared HTML-like table label macro while preserving exact public IDs and private anchors. |
| `openspec/changes/workbench-svg-render-improvements/tasks.md` | Modified | Marked completed Batch A and Batch B tasks. |
| `openspec/changes/workbench-svg-render-improvements/apply-progress.md` | Modified | Merged Batch B and Batch C progress into the cumulative strict-TDD artifact. |

### TDD Cycle Evidence
| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 / 2.2 / 3.1 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | ✅ 4/4 passing baseline | ✅ Written first | ✅ `pytest tests/unit/mbse/test_hsm_render_view.py` (5/5) | ✅ Non-empty DOT and render-view cases cover banner absence in prepared view and DOT output | ✅ Minimal template adaptation kept behavior stable |
| 1.2 / 2.1 / 2.3 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | ✅ 4/4 passing baseline | ✅ Written first | ✅ `pytest tests/unit/mbse/test_hsm_render_view.py` (5/5) | ✅ Flat, compound, and empty-body state cases force real title/body shaping logic | ➖ None needed |
| 1.3 / 4.2 | `tests/integration/test_hsm_json_workbench.py` | Integration | ⚠️ 3/4 baseline (`test_build_workbench_session_keeps_exact_compound_svg_id_once` was already stale against Batch A output) | ✅ Tightened exact-ID and final-SVG assertions before template changes | ✅ `pytest tests/integration/test_hsm_json_workbench.py` (4/4) | ✅ Flat, duplicate-label, and compound cases prove exact authored IDs stay public once while `__anchor` stays private | ✅ Extracted `_assert_svg_contains_exact_public_ids()` to remove duplication |
| 3.2 / 3.3 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | ✅ 5/5 passing baseline | ✅ Updated DOT expectations to require HTML-like labels before editing the template | ✅ `pytest tests/unit/mbse/test_hsm_render_view.py` (5/5) | ✅ Compound and leaf assertions force the shared label macro to cover both code paths | ✅ Extracted `render_state_label` Jinja macro for reuse |
| 4.3 | `tests/` | Integration | ✅ Targeted suites already green from Batch A/B | ➖ Verification-only task (no new behavior added) | ✅ `pytest` (59/59) | ➖ Full regression pass only | ➖ None needed |

### Test Summary
- **Total tests written**: 6
- **Total tests passing**: 9
- **Layers used**: Unit (5), Integration (4), E2E (0)
- **Approval tests**: None — behavior change was specified by the delta spec
- **Pure functions created**: 1 (`_format_state_body_lines`)

### Deviations from Design
None — implementation matches design.

### Issues Found
- The integration safety net started with one stale compound-label expectation left behind by Batch A; Batch B replaced it with the final HTML-label + exact-public-ID contract.
- Scope check after the full-suite pass found only render-pipeline files, their tests, and OpenSpec artifacts touched for this change (`src/mbse/application/prepare_hsm_render.py`, `src/mbse/domain/models.py`, `src/mbse/infrastructure/templates/hsm_v1.dot.j2`, `tests/unit/mbse/test_hsm_render_view.py`, `tests/integration/test_hsm_json_workbench.py`, and `openspec/changes/workbench-svg-render-improvements/*`).

### Remaining Tasks
- [ ] None.

### Workload / PR Boundary
- Mode: single PR
- Current work unit: Batch C
- Boundary: full pytest regression plus scope confirmation only; no additional behavior and no runtime edits
- Estimated review budget impact: stays within the forecasted medium-risk slice

### Status
11/11 tasks complete across Batches A-C. Ready for verify.
