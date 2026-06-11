# Archive Report: mbse-1-graphical-workbench

## Change

- **Name**: `mbse-1-graphical-workbench`
- **Archived On**: `2026-05-27`
- **Persistence Mode**: `openspec`
- **Archive Destination**: `openspec/changes/archive/2026-05-27-mbse-1-graphical-workbench/`

## Readiness Check

- Verification status: **PASS WITH WARNINGS**
- Critical issues: **None**
- Tasks complete: **11/11**
- Manual GUI confirmation: **Confirmed by user**
- Archive gate result: **Ready to archive**

## Spec Sync

| Domain | Action | Details |
|--------|--------|---------|
| `graphviz-svg-workbench` | Created | Promoted the delta spec as a new source-of-truth domain spec in `openspec/specs/graphviz-svg-workbench/spec.md`. |

## Verification Evidence

- Targeted tests: **18 passed**
- Full suite: **Blocked outside slice** (`pytest` collection fails in legacy `src/mbse` because `jsonschema` is missing in this environment)
- Compliance matrix: **6/7 scenarios compliant, 1 partial, 0 failing**
- TDD checks: **6/6 passed**
- Manual workbench run: **Satisfied**

## Warnings Carried Forward

- The frontend exact-ID DOM highlight path is still verified by source inspection plus backend/integration evidence, not by a browser-backed runtime assertion.
- Full-project `pytest` remains blocked by missing legacy dependency setup outside `src/mbse_1`.
- Coverage evidence was unavailable because `pytest-cov` is not installed in this environment.
- Lint/type-check evidence was unavailable because `ruff` and `mypy` are not installed in this environment.

## Archived Artifacts

- `proposal.md`
- `exploration.md`
- `design.md`
- `tasks.md`
- `apply-progress.md`
- `verify-report.md`
- `archive-report.md`
- `specs/graphviz-svg-workbench/spec.md`

## Outcome

The `mbse-1-graphical-workbench` change completed the SDD cycle. Its slice-1 read-only Graphviz SVG workbench contract now lives under `openspec/specs/graphviz-svg-workbench/spec.md` as the active source of truth, with implementation intentionally isolated under `src/mbse_1` and no dependency on `src/mbse`.
