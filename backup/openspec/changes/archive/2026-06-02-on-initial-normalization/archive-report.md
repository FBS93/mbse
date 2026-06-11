# Archive Report: on-initial-normalization

## Change

- **Name**: `on-initial-normalization`
- **Archived On**: `2026-06-02`
- **Persistence Mode**: `openspec`
- **Archive Destination**: `openspec/changes/archive/2026-06-02-on-initial-normalization/`

## Readiness Check

- Verification status: **PASS WITH WARNINGS**
- Critical issues: **None**
- Tasks complete: **11/11**
- Archive gate result: **Ready to archive**

## Spec Sync

| Domain | Action | Details |
|--------|--------|---------|
| `generated-hsm-engine` | Updated | Synced the runtime source-of-truth spec so root and local `initial` objects are routing-only, `on_initial` is the only executable initial hook, and `initial.activities` is explicitly rejected. |
| `hsm-json-graphviz-rendering` | Updated | Synced the JSON/render source-of-truth spec so states may declare `on_initial`, initials stay structural-only, and render output never exposes competing `initial_transition:` behavior text. |

## Verification Evidence

- Targeted tests: **46 passed**
- Full suite: **102 passed**
- Compliance matrix: **20/20 scenarios compliant**
- TDD checks: **6/6 passed**
- Static correctness/design checks: **All listed implementation/design checks passed**

## Warnings Carried Forward

- Coverage evidence was unavailable because `pytest-cov` is not installed in this environment.
- Lint verification was unavailable because `ruff` is not installed in this environment.
- Type-checker verification was unavailable because `mypy` is not installed in this environment.

## Archived Artifacts

- `proposal.md`
- `exploration.md`
- `design.md`
- `tasks.md`
- `verify-report.md`
- `archive-report.md`
- `specs/generated-hsm-engine/spec.md`
- `specs/hsm-json-graphviz-rendering/spec.md`

## Outcome

The `on-initial-normalization` change completed the SDD cycle. The source of truth now states that executable initial behavior belongs only to state-owned `on_initial` hooks, while root and local `initial` objects remain structural routing metadata across schema, runtime, generated engine, and render contracts.
