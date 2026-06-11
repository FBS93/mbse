# Tasks: Workbench Sidebar Compact Restyle

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 260-360 |
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
|------|------|-----------|-------|
| 1 | Compact sidebar restyle plus contract updates | PR 1 | Single cohesive frontend slice; split only if CSS/test churn grows past budget |

## Phase 1: RED Contract Updates

- [x] 1.1 In `tests/integration/test_mbse_workbench.py`, add/adjust failing assertions for removed `.sidebar-header`, compact reset row, preserved section order, absent status/intro UI, and textbox-first variable rows.
- [x] 1.2 In `tests/support/viewer_browser_harness.py`, write failing parser/snapshot expectations for compact variable rows that read textbox values and an explicit inline unset marker without `.value-display`.

## Phase 2: Markup and Style Implementation

- [x] 2.1 In `src/mbse/web/static/index.html`, remove the sidebar intro block and wrap `reset-form` plus `reset-view-button` in one shared compact reset-row container while preserving existing IDs.
- [x] 2.2 In `src/mbse/web/static/viewer.css`, restyle sidebar/panel surfaces, tighten section spacing, and add compact reset-row styles without changing the layout grid, splitter, or overflow ownership.
- [x] 2.3 In `src/mbse/web/static/viewer.css`, flatten `.variable-row` into a single-line desktop layout with responsive fallback, and define the explicit inline unset treatment chosen during apply.

## Phase 3: GREEN Rendering Updates

- [x] 3.1 In `src/mbse/web/static/viewer.js`, update `renderVariableRow()` so the input shows the current value directly, the submit button stays inline, and unset variables render an explicit compact inline marker.
- [x] 3.2 Keep `wireResetForm()`, `wireResetViewButton()`, `wireEventForm()`, and `submitRuntimeAction()` behavior unchanged, verifying the restyle remains presentation-only.

## Phase 4: Verification and Cleanup

- [x] 4.1 Make the new integration and harness tests pass, confirming reset/event/variable endpoints and highlight behavior are unchanged.
- [x] 4.2 Trim brittle CSS/string assertions in `tests/integration/test_mbse_workbench.py` so they check layout/overflow contracts and new DOM hooks without pinning exact cosmetic values.
- [x] 4.3 Run `pytest tests/integration/test_mbse_workbench.py` and record any follow-up split if the actual diff starts pushing beyond the 400-line budget.
