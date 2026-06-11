# Apply Progress: Render Hierarchy Colors And Empty Actions

## Implementation Progress

**Change**: `render-hierarchy-colors-and-empty-actions`
**Mode**: Strict TDD

### Completed Tasks
- [x] 1.1 Extend `tests/unit/mbse/test_hsm_render_view.py` to lock depth `0/1/2` colors, same-depth equality, and the always-visible body row for flat + compound states with empty actions.
- [x] 1.2 Extend `tests/integration/test_hsm_json_workbench.py` to reassert exact public SVG IDs while proving empty partitions still render and private anchors stay private.
- [x] 2.1 Update `src/mbse/domain/models.py` so `HsmRenderStateNode` carries render-only `depth`, `fill_rgb`, and `has_body_content` fields without changing runtime models.
- [x] 2.2 Update `src/mbse/application/prepare_hsm_render.py` to propagate depth, compute deterministic tint from base `#DCE8F2`, and preserve authored ordering plus current public/private ID routing.
- [x] 3.1 Update `src/mbse/infrastructure/templates/hsm_v1.dot.j2` to always emit the second row with a placeholder when `body_lines` is empty and apply prepared colors to leaf + compound visuals.
- [x] 4.1 Run `pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` and keep only the minimal render-only diff needed to pass.

### Files Changed
| File | Action | What Was Done |
|------|--------|---------------|
| `tests/unit/mbse/test_hsm_render_view.py` | Modified | Added RED contract tests for deterministic depth colors and always-visible empty body partitions. |
| `tests/integration/test_hsm_json_workbench.py` | Modified | Added integration coverage for empty partitions while preserving exact public SVG IDs and private anchors. |
| `src/mbse/domain/models.py` | Modified | Extended `HsmRenderStateNode` with render-only depth/color/body metadata. |
| `src/mbse/application/prepare_hsm_render.py` | Modified | Propagated depth and derived deterministic fill colors without changing routing/runtime behavior; follow-up switched from same-hue tinting to soft hue rotation for stronger real parent/child contrast. |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modified | Always renders the body row placeholder and applies prepared colors to leaf/compound visuals. |
| `openspec/changes/render-hierarchy-colors-and-empty-actions/tasks.md` | Modified | Marked the apply batch tasks complete. |

### TDD Cycle Evidence
| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 / 2.1 / 2.2 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | ✅ 9/9 | ✅ Written first | ✅ 7/7 passed | ✅ Depth 0/1/2 + same-depth + cross-depth color separation + empty flat/compound cases | ✅ Kept helper logic small and deterministic |
| 1.2 / 3.1 | `tests/integration/test_hsm_json_workbench.py` | Integration | ✅ 9/9 | ✅ Written first | ✅ 5/5 passed | ✅ Exact IDs + private anchors + empty partition scenario | ➖ None needed |
| 4.1 | `tests/unit/mbse/test_hsm_render_view.py` + `tests/integration/test_hsm_json_workbench.py` | Unit + Integration | N/A | ✅ Existing RED/GREEN evidence above | ✅ 12/12 passed | ✅ Combined verification run | ✅ Minimal render-only diff retained |

### Test Summary
- **Total tests written**: 3
- **Total tests passing**: 12
- **Layers used**: Unit (7), Integration (5), E2E (0)
- **Approval tests**: None — behavior change slice, not refactor-only
- **Pure functions created**: 1 (`_derive_fill_rgb`)

### Deviations from Design
Adjusted the fill derivation from same-hue lightening to a soft hue-rotation algorithm rooted in `#DCE8F2`, so parent/child levels visibly differ in color while staying pastel and render-only.

### Issues Found
None.

### Follow-up Fix
- Re-ran the color contract in RED by updating the expected depth `1/2` hex values, then replaced ratio-only tinting with deterministic hue rotation plus lightness clamping without touching IDs or runtime behavior.

### Remaining Tasks
- [x] None.

### Workload / PR Boundary
- Mode: single PR
- Current work unit: Unit 1 — render-only colors + empty partition + contract tests
- Boundary: starts at render preparation/template/tests and ends before any runtime or workbench-shell changes
- Estimated review budget impact: Stayed within the small single-batch forecast

### Status
6/6 tasks complete. Ready for verify.
