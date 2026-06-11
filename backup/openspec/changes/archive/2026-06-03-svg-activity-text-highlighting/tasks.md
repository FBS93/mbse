# Tasks: SVG Activity Text Highlighting

## Review Workload Forecast

| Field | Value |
|---|---|
| Estimated changed lines | 300-380 |
| 400-line budget risk | Medium |
| Chained PRs recommended | No |
| Suggested split | Single PR |
| Delivery strategy | ask-always |
| Chain strategy | pending |

Decision needed before apply: Yes
Chained PRs recommended: No
Chain strategy: pending
400-line budget risk: Medium

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|---|---|---|---|
| 1 | Render-owned text targets end to end | Single PR | Keep scope to listed files/tests so review stays under budget. |

## Phase 1: Contract RED

- [x] 1.1 Add failing contract tests in `tests/unit/mbse/test_web_runtime_bridge.py` and `tests/integration/test_mbse_session_build.py` for private text targets, exact public ID preservation, and unchanged `active_ids` / edge highlights.
- [x] 1.2 Add failing render/normalization tests in `tests/unit/mbse/test_hsm_render_view.py` and `tests/unit/mbse/test_svg_contract.py` for lifecycle, transition, and internal-transition marker output plus omission of unstable wrappers.

## Phase 2: Render + Normalize GREEN

- [x] 2.1 Extend `src/mbse/domain/models.py` and `src/mbse/application/prepare_hsm_render.py` with private text-target DTOs and semantic marker plans for lifecycle slots, transition labels, and internal-transition rows.
- [x] 2.2 Update `src/mbse/infrastructure/templates/hsm_v1.dot.j2` and `src/mbse/infrastructure/svg_contract.py` to emit marker-delimited text, normalize exact private fragment IDs, strip markers, and omit ambiguous targets without changing authored SVG IDs.

## Phase 3: Session + Viewer Wiring

- [x] 3.1 Wire normalized targets through `src/mbse/application/build_session.py` and `src/mbse/application/web_runtime_bridge.py` as viewer-only metadata while preserving current `last_event`, state, and edge contracts.
- [x] 3.2 Update `src/mbse/web/static/viewer.js` and `src/mbse/web/static/viewer.css` to resolve semantic refs to exact fragments, preserve current shape/edge highlight behavior, and use underline + subtle accent instead of heavier font weight.

## Phase 4: Verification + Refactor

- [x] 4.1 Add integration/browser coverage in `tests/integration/test_hsm_json_workbench.py`, `tests/integration/test_mbse_workbench.py`, and `tests/support/viewer_browser_harness.py` for precise fragment targeting, internal-transition-only text highlighting, and neutral unrelated text.
- [x] 4.2 Refactor shared fixtures only where needed, then run `pytest` for render, bridge, session-build, and workbench suites to prove text highlights coexist with current state/edge highlights.
