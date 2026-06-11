# Tasks: Render Hierarchy Colors And Empty Actions

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 120-220 |
| 400-line budget risk | Low |
| Chained PRs recommended | No |
| Suggested split | single PR |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: No
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Low

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Render-only colors + empty partition + contract tests | PR 1 | Single small batch; no runtime touch |

## Phase 1: RED / Contract Tests

- [x] 1.1 Extend `tests/unit/mbse/test_hsm_render_view.py` to lock depth `0/1/2` colors, same-depth equality, and the always-visible body row for flat + compound states with empty actions.
- [x] 1.2 Extend `tests/integration/test_hsm_json_workbench.py` to reassert exact public SVG IDs while proving empty partitions still render and private anchors stay private.

## Phase 2: GREEN / Render Preparation

- [x] 2.1 Update `src/mbse/domain/models.py` so `HsmRenderStateNode` carries render-only `depth`, `fill_rgb`, and `has_body_content` fields without changing runtime models.
- [x] 2.2 Update `src/mbse/application/prepare_hsm_render.py` to propagate depth, compute deterministic tint from base `#DCE8F2`, and preserve authored ordering plus current public/private ID routing.

## Phase 3: GREEN / Template Wiring

- [x] 3.1 Update `src/mbse/infrastructure/templates/hsm_v1.dot.j2` to always emit the second row with a placeholder when `body_lines` is empty and apply prepared colors to leaf + compound visuals.

## Phase 4: REFACTOR / Verify

- [x] 4.1 Run `pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` and keep only the minimal render-only diff needed to pass.
