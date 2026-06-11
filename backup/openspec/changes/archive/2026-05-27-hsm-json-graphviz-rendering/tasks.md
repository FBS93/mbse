# Tasks: HSM JSON Graphviz Rendering

## Review Workload Forecast

| Field | Value |
|-------|-------|
| Estimated changed lines | 420-560 |
| 400-line budget risk | High |
| Chained PRs recommended | Yes |
| Suggested split | PR 1 schema+validation -> PR 2 render prep+Jinja2 -> PR 3 session integration+batch verification |
| Delivery strategy | ask-always |
| Chain strategy | pending |

Decision needed before apply: Yes
Chained PRs recommended: Yes
Chain strategy: pending
400-line budget risk: High

### Suggested Work Units

| Unit | Goal | Likely PR | Notes |
|------|------|-----------|-------|
| 1 | Lock HSM v1 schema and rejection rules | PR 1 | Base boundary for future slices; no runtime semantics |
| 2 | Add deterministic render prep and minimal Jinja2 DOT path | PR 2 | Depends on PR 1; keep template dumb |
| 3 | Wire workbench path and prove SVG ID contract | PR 3 | Depends on PR 2; verification-heavy |

## Phase 1: Schema First

- [x] 1.1 RED: add `tests/unit/mbse/test_hsm_validation.py` for valid minimal HSM, duplicate IDs, bad refs, invalid local initials, and unsupported runtime-like fields from spec scenarios.
- [x] 1.2 GREEN: extend `src/mbse/domain/models.py` with HSM v1 document/value types and a prepared render-view type that carries authored order explicitly.
- [x] 1.3 GREEN: extend `src/mbse/domain/validation.py` with `load_hsm_document()` and `validate_hsm_document()` enforcing exact IDs, global uniqueness, direct-child local initials, and additional-properties rejection.
- [x] 1.4 REFACTOR: keep prepared-document validation intact while isolating HSM validation helpers in `src/mbse/domain/validation.py`; reject runtime/history/orthogonal constructs explicitly.

## Phase 2: Deterministic Render Prep

- [x] 2.1 RED: add `tests/unit/mbse/test_hsm_render_view.py` for depth-first state order, authored transition order, `open_evt(source)` formatting, annotation blocks, and ordered `highlightable_ids`.
- [x] 2.2 GREEN: create `src/mbse/application/prepare_hsm_render.py` to flatten states, resolve initials/transitions, assemble display strings, and return one deterministic render view.
- [x] 2.3 GREEN: create `src/mbse/infrastructure/templates/hsm_v1.dot.j2` with only presentation logic for states, initials, transitions, events, variables, `on_entry`, and `on_exit`.
- [x] 2.4 GREEN: create `src/mbse/infrastructure/dot_template.py` and minimally update `pyproject.toml` to introduce Jinja2 only for loading/rendering `hsm_v1.dot.j2`.

## Phase 3: Workbench Integration

- [x] 3.1 RED: add `tests/integration/test_hsm_json_workbench.py` covering JSON -> DOT -> SVG determinism and exact downstream SVG IDs for states, transitions, and initials.
- [x] 3.2 GREEN: update `src/mbse/application/build_session.py` to accept HSM JSON input through the new validation/preparation/template path while preserving `PreparedGraphvizDocument` output and current session contract.
- [x] 3.3 REFACTOR: keep CLI/web/runtime boundaries unchanged in `src/mbse/cli/main.py` and related callers; do not add execution semantics, editing, or alternate inputs beyond this adapter.

## Phase 4: Batch Verification

- [x] 4.1 Run batch A after Unit 1: `pytest tests/unit/mbse/test_hsm_validation.py tests/unit/mbse/test_validation.py`.
- [x] 4.2 Run batch B after Unit 2: `pytest tests/unit/mbse/test_hsm_render_view.py tests/unit/mbse/test_hsm_validation.py`.
- [x] 4.3 Run batch C after Unit 3: `pytest tests/integration/test_hsm_json_workbench.py tests/integration/test_mbse_session_build.py tests/integration/test_mbse_workbench.py`.
