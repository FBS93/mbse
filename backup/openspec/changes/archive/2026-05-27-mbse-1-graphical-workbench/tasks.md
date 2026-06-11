# Tasks: MBSE 1 Graphical Workbench

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 420-560 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 -> PR 2 -> PR 3 |
| Delivery strategy | ask-on-risk |
| Chain strategy | pending |

Decision needed before apply: Yes
Chained PRs recommended: Yes
Chain strategy: pending
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Lock contract + isolation rules | PR 1 | Base for all later work; no web yet |
| 2 | Build Graphviz session pipeline | PR 2 | Depends on PR 1; artifacts + render validation |
| 3 | Add read-only web workbench | PR 3 | Depends on PR 2; API, static UI, CLI |

## Phase 1: Contract Foundation

- [x] 1.1 RED: add `tests/unit/mbse_1/test_validation.py` for missing fields, duplicate `highlightable_ids`, and forbidden `src.mbse` imports in `src/mbse_1/**`.
- [x] 1.2 GREEN: create `src/mbse_1/domain/models.py` and `src/mbse_1/domain/validation.py` for `PreparedGraphvizDocument`, `WorkbenchSession`, and exact-ID contract checks.
- [x] 1.3 REFACTOR: add `src/mbse_1/__init__.py` plus package markers under `src/mbse_1/{domain,application,infrastructure,web,cli}` with zero imports from `src/mbse`.

## Phase 2: Session Build Pipeline

- [x] 2.1 RED: add `tests/unit/mbse_1/test_svg_contract.py` and `tests/integration/test_mbse_1_session_build.py` for authored SVG IDs, duplicate SVG IDs, and missing rendered IDs.
- [x] 2.2 GREEN: create `src/mbse_1/infrastructure/graphviz_runner.py`, `src/mbse_1/infrastructure/svg_contract.py`, and `src/mbse_1/infrastructure/session_store.py` for `dot -Tsvg`, SVG ID extraction, and artifact writes.
- [x] 2.3 GREEN: create `src/mbse_1/application/build_session.py` to load prepared JSON, render SVG, validate exact IDs, and emit `diagram.svg` plus `workbench-session.json`.
- [x] 2.4 VERIFY: run `pytest tests/unit/mbse_1/test_svg_contract.py tests/integration/test_mbse_1_session_build.py`.

## Phase 3: Read-Only Highlight Workbench

- [x] 3.1 RED: add `tests/unit/mbse_1/test_highlight.py` and API assertions in `tests/integration/test_mbse_1_workbench.py` for ordered exact-match highlights and explicit `unknown_ids`.
- [x] 3.2 GREEN: create `src/mbse_1/application/highlight.py` and `src/mbse_1/web/server.py` for `/api/session.json`, `/api/highlight`, and `/artifacts/diagram.svg`.
- [x] 3.3 GREEN: create `src/mbse_1/web/static/index.html`, `viewer.css`, `viewer.js`, and `src/mbse_1/cli/main.py` for read-only SVG load, DOM highlight by exact ID, and local launch.
- [x] 3.4 VERIFY: run `pytest tests/unit/mbse_1/test_highlight.py tests/integration/test_mbse_1_workbench.py`; confirm no runtime, editing, or multi-document actions surface in the UI.
