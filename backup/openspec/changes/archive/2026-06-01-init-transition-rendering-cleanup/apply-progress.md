# Apply Progress: Init Transition Rendering Cleanup

## Implementation Progress

**Change**: `init-transition-rendering-cleanup`
**Mode**: Strict TDD

### Completed Tasks
- [x] 1.1 In `tests/unit/mbse/test_hsm_render_view.py`, add failing assertions that `routing_helpers` distinguish `root_initial_source`, `local_initial_source`, and `compound_anchor`, with deterministic order and authored-only `highlightable_ids`.
- [x] 1.2 In `tests/integration/test_hsm_json_workbench.py`, add a fake-Graphviz failing contract that visible initial-source dots render, private anchors never surface as public SVG IDs, and authored IDs remain exact and unique.
- [x] 1.3 In `tests/integration/test_hsm_json_workbench.py`, add/refresh a real-`dot` regression (skip only when `dot` is unavailable) proving visible source dots stay present while stray target dots/helper ellipses disappear.
- [x] 2.1 In `src/mbse/domain/models.py`, extend `HsmRenderRoutingHelper` metadata so helper kind and visibility explicitly separate visible source markers from private anchors.
- [x] 2.2 In `src/mbse/application/prepare_hsm_render.py`, register root/local initial sources as visible helpers and compound targets as private anchors, keeping endpoint ownership and ordering deterministic.
- [x] 3.1 In `src/mbse/infrastructure/templates/hsm_v1.dot.j2`, render visible initial-source helpers as black `shape=point` nodes without public `id=` attributes and keep compound anchors invisible in the correct scope.
- [x] 3.2 In `src/mbse/domain/validation.py`, enforce that only private helper kinds are leak-checked while public SVG IDs for states, clusters, transitions, and initial transitions stay exact, unique, and unambiguous.
- [x] 4.1 Refactor shared helper fixtures/assertions in `tests/unit/mbse/test_hsm_render_view.py` and `tests/integration/test_hsm_json_workbench.py` so source-marker and private-anchor expectations stay readable.
- [x] 4.2 Run `pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` and confirm root/local visible source dots return, private anchors stay invisible, and authored public IDs remain stable.

### Files Changed
| File | Action | What Was Done |
|------|--------|---------------|
| `tests/unit/mbse/test_hsm_render_view.py` | Modified | Added RED-to-GREEN routing-helper visibility assertions and extracted a shared helper assertion. |
| `tests/integration/test_hsm_json_workbench.py` | Modified | Added fake/real Graphviz visibility regressions plus a shared DOT authored-ID assertion helper. |
| `src/mbse/domain/models.py` | Modified | Added explicit routing-helper `visibility` metadata. |
| `src/mbse/application/prepare_hsm_render.py` | Modified | Registered root/local initial sources as visible helpers and compound anchors as private helpers deterministically. |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modified | Rendered visible source markers as black point nodes and kept private anchors invisible. |
| `src/mbse/domain/validation.py` | Modified | Tightened prepared-document validation so authored public IDs stay exact and no extra public IDs leak. |
| `openspec/changes/init-transition-rendering-cleanup/tasks.md` | Modified | Marked all correction-batch tasks complete. |
| `openspec/changes/init-transition-rendering-cleanup/apply-progress.md` | Created | Recorded cumulative strict-TDD implementation evidence for the change. |

### TDD Cycle Evidence
| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 / 2.1 / 2.2 | `tests/unit/mbse/test_hsm_render_view.py` | Unit | ✅ `pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` (16/16) | ✅ Wrote visibility/kind expectations before production changes | ✅ `pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` (16/16) | ✅ Covered root initial, local initial, and compound-anchor code paths | ✅ Extracted `_assert_routing_helpers()` after green |
| 1.2 / 1.3 / 3.1 | `tests/integration/test_hsm_json_workbench.py` | Integration | ✅ `pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` (16/16) | ✅ Tightened fake/real Graphviz expectations before template changes | ✅ `pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` (16/16) | ✅ Fake Graphviz plus real `dot` regression proved visible sources and hidden target anchors | ✅ Extracted `_assert_dot_contains_exact_public_ids()` to keep expectations readable |
| 3.2 / 4.1 / 4.2 | `tests/integration/test_hsm_json_workbench.py` | Integration | ✅ Prior targeted suite green from earlier GREEN step | ✅ Added authored-ID exactness assertions before validation tightening | ✅ `pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` (16/16) | ✅ Verified exact authored IDs across flat, duplicate-label, and compound routing cases | ✅ Validation cleanup stayed minimal; no further refactor needed |

### Test Summary
- **Total tests written**: 5
- **Total tests passing**: 16
- **Layers used**: Unit (8), Integration (8), E2E (0)
- **Approval tests**: None — the spec intentionally changed rendering behavior
- **Pure functions created**: 0

### Deviations from Design
None — implementation matches design.

### Issues Found
- The Jinja helper-emission macro originally collapsed adjacent helper nodes onto one line, which broke the fake-Graphviz visibility contract; adding explicit helper line breaks fixed the regression without changing public IDs.

### Remaining Tasks
- [ ] None.

### Workload / PR Boundary
- Mode: single PR
- Current work unit: Unit 1
- Boundary: routing-helper visibility, validation contract, and targeted render regression coverage only
- Estimated review budget impact: stays inside the forecasted low-risk single-PR budget

### Status
9/9 tasks complete. Ready for verify.
