# Tasks: Workbench SVG Render Improvements

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 220-340 |
| 400-line budget risk | Medium |
| Chained PRs recommended | No |
| Suggested split | Single PR, applied in 3 internal batches |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Medium

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Lock render-model contract first | PR 1 | RED tests for banner removal and exact IDs |
| 2 | Implement render data + template changes | PR 1 | Render-only files only; no runtime edits |
| 3 | Prove SVG/public-id contract end-to-end | PR 1 | Integration assertions for exact IDs and private anchors |

## Phase 1: Contract Locking

- [x] 1.1 In `tests/unit/mbse/test_hsm_render_view.py`, add RED assertions that prepared render output omits graph-level `Variables`/`Events` blocks.
- [x] 1.2 In `tests/unit/mbse/test_hsm_render_view.py`, add RED assertions for exact `title_text` and `body_lines` on flat and compound states, preserving highlightable ID order.
- [x] 1.3 In `tests/integration/test_hsm_json_workbench.py`, add RED assertions that every highlightable SVG element uses the exact authored JSON `id`, including compound parents, and that `__anchor` stays non-public.

## Phase 2: Render-Only Model Updates

- [x] 2.1 Update `src/mbse/domain/models.py` to replace string label fields with render-only `title_text` and `body_lines` fields on the prepared render models.
- [x] 2.2 Update `src/mbse/application/prepare_hsm_render.py` to stop populating `variables_block` / `events_block` and to build deterministic title/body data from label, `on_entry`, and `on_exit`.
- [x] 2.3 Keep depth-first state ordering, `highlightable_ids`, compound public IDs, and private `{state.id}__anchor` routing unchanged in `src/mbse/application/prepare_hsm_render.py`.

## Phase 3: DOT Template Rendering

- [x] 3.1 Update `src/mbse/infrastructure/templates/hsm_v1.dot.j2` to remove any `graph [label=...]` banner emission.
- [x] 3.2 Render leaf states with HTML-like table labels that separate title from body while keeping `id="{{ state.id }}"` exact.
- [x] 3.3 Render compound clusters with the same title/body partition, preserving the cluster public ID exactly and keeping anchors private/unhighlightable.

## Phase 4: Batch Verification

- [x] 4.1 Batch A: run `pytest tests/unit/mbse/test_hsm_render_view.py` after Phase 1-2 to turn RED to GREEN without touching runtime files.
- [x] 4.2 Batch B: run `pytest tests/integration/test_hsm_json_workbench.py` after Phase 3 to verify exact SVG ID uniqueness and compound-state public-ID preservation.
- [x] 4.3 Batch C: run `pytest` if the targeted suites pass, then confirm no files outside the render pipeline and its tests changed.
