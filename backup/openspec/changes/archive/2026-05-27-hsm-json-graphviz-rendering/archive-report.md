# Archive Report: hsm-json-graphviz-rendering

## Change

- **Name**: `hsm-json-graphviz-rendering`
- **Archived On**: `2026-05-27`
- **Persistence Mode**: `openspec`
- **Archive Destination**: `openspec/changes/archive/2026-05-27-hsm-json-graphviz-rendering/`

## Readiness Check

- Verification status: **PASS WITH WARNINGS**
- Critical issues: **None**
- Tasks complete: **17/17**
- User decision on remaining warning: **Accepted; do not pursue orthogonal-regions warning before archive**
- Archive gate result: **Ready to archive**

## Spec Sync

| Domain | Action | Details |
|--------|--------|---------|
| `hsm-json-graphviz-rendering` | Created | Promoted the delta spec as a new source-of-truth domain spec in `openspec/specs/hsm-json-graphviz-rendering/spec.md`. |

## Verification Evidence

- Targeted tests: **25 passed**
- Full suite: **31 passed**
- Compliance matrix: **8/9 scenarios compliant, 1 partial, 0 failing**
- TDD checks: **5/6 passed**
- Static correctness/design checks: **All listed implementation/design checks passed**

## Warnings Carried Forward

- The `Deferred complex semantics stay out of v1` scenario is still only partially covered by runtime tests because orthogonal-region-like rejection lacks a direct explicit test.
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
- `specs/hsm-json-graphviz-rendering/spec.md`

## Outcome

The `hsm-json-graphviz-rendering` change completed the SDD cycle. The active source of truth now includes HSM JSON v1 plus the deterministic `JSON HSM -> Jinja2 DOT -> Graphviz SVG -> workbench` render contract, while preserving the downstream exact SVG ID behavior and intentionally excluding runtime semantics from v1.
