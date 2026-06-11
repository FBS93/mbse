# Apply Progress: graphviz-compound-state-visual-fix

## Status

- Mode: Strict TDD
- Delivery: Single batch, within review budget
- Result: Implementation already complete; this artifact restores missing administrative traceability only

## Completed Tasks

- [x] 1.1 Cluster now owns the public compound-state visual id/label in `src/mbse/infrastructure/templates/hsm_v1.dot.j2`.
- [x] 1.2 Compound clusters now keep one private `__anchor` routing node.
- [x] 2.1 Compound-state initial/transition endpoints route through `{state.id}__anchor` in `src/mbse/application/prepare_hsm_render.py`.
- [x] 2.2 `highlightable_ids` keep authored public ids only; flat-state behavior stays unchanged.
- [x] 3.1 Unit coverage added in `tests/unit/mbse/test_hsm_render_view.py`.
- [x] 3.2 Integration coverage added in `tests/integration/test_hsm_json_workbench.py`.
- [x] 4.1 Targeted pytest executed.
- [x] 4.2 Full pytest suite executed.

## TDD Cycle Evidence

| Task | RED | GREEN | REFACTOR |
|------|-----|-------|----------|
| 1.1-2.2 | Existing compound-state assertions in `tests/unit/mbse/test_hsm_render_view.py` and `tests/integration/test_hsm_json_workbench.py` represent the failing contract for the old duplicate-parent rendering path. | Current implementation passes targeted and full pytest runs recorded in `verify-report.md`. | Final shape keeps authored ids stable, routes only compound endpoints to `__anchor`, and leaves flat states unchanged. |
| 3.1 | Unit assertions would fail if the visible parent node still existed or if cluster/anchor ids were wrong. | `pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` passed (8/8). | Assertions pin the cluster label/id contract without expanding public API. |
| 3.2 | Integration assertions would fail if `diagram.svg` exposed duplicate or rewritten compound ids. | `pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py` passed (8/8). | Coverage proves exact SVG/workbench ids remain stable after the visual fix. |
| 4.1-4.2 | Safety net is the task-aligned targeted run plus full regression suite. | Full `pytest` passed (33/33) as recorded in `verify-report.md`. | No further product-code changes were required after the passing verification evidence. |

## Verify Evidence

```text
$ pytest tests/unit/mbse/test_hsm_render_view.py tests/integration/test_hsm_json_workbench.py
8 passed in 0.23s

$ pytest
33 passed in 1.36s
```

Source of execution record: `openspec/changes/graphviz-compound-state-visual-fix/verify-report.md`

## Files Implemented Earlier

- `src/mbse/infrastructure/templates/hsm_v1.dot.j2`
- `src/mbse/application/prepare_hsm_render.py`
- `tests/unit/mbse/test_hsm_render_view.py`
- `tests/integration/test_hsm_json_workbench.py`

## Deviations

- None. The implemented fix matches the proposal, spec, and design.

## Notes

- This apply artifact was added after implementation because verify failed on missing SDD admin artifacts, not on behavioral correctness.
- No product code was changed in this apply step.
