## Archive Report

**Change**: hsm-executable-activities-and-guards
**Archived On**: 2026-06-02
**Mode**: openspec
**Verification Gate**: PASS WITH WARNINGS — no CRITICAL issues in `verify-report.md`

### Specs Synced

| Domain | Action | Details |
|--------|--------|---------|
| `generated-hsm-engine` | Updated | Added `Executable Behavior Model Contract`; replaced `Minimal Hierarchical Execution Semantics` and `Explicit v1 Exclusions And Safety` with the verified executable-activities-and-guards semantics; preserved unrelated requirements (`Stable Runtime API`, `Generated Engine And Handwritten Runtime Stay Separated`). |

### Source Artifacts Reviewed

- `openspec/changes/hsm-executable-activities-and-guards/exploration.md`
- `openspec/changes/hsm-executable-activities-and-guards/proposal.md`
- `openspec/changes/hsm-executable-activities-and-guards/specs/generated-hsm-engine/spec.md`
- `openspec/changes/hsm-executable-activities-and-guards/design.md`
- `openspec/changes/hsm-executable-activities-and-guards/tasks.md`
- `openspec/changes/hsm-executable-activities-and-guards/verify-report.md`
- `openspec/specs/generated-hsm-engine/spec.md`

### Verification Evidence

- Verdict: `PASS WITH WARNINGS`
- Tasks complete: `15/15`
- Focused tests: `pytest tests/unit/mbse/test_hsm_validation.py tests/unit/mbse/test_validation.py tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_generated_engine.py tests/integration/test_generated_hsm_engine.py tests/integration/test_mbse_session_build.py -q` → `41 passed`
- Full suite: `pytest -q` → `95 passed`

### Warnings Carried Forward

- Apply-progress is missing an explicit TDD evidence row for cleanup task `5.1`, so strict-TDD evidence remains complete for `14/15` tasks rather than the full task list.
- Coverage analysis could not run because `pytest-cov` is not installed in this environment.
- Ruff quality checks could not run because `ruff` is not installed in this environment.
- Type-checker verification could not run because `mypy` is not installed in this environment.

### Archive Verification

- Main spec was updated before archiving.
- The archived change folder retains exploration, proposal, delta specs, design, tasks, verification, and this archive report.
- The active change directory will no longer contain `hsm-executable-activities-and-guards` after the move.

### Final Archive Path

`openspec/changes/archive/2026-06-02-hsm-executable-activities-and-guards/`

### Notes

This archive finalizes the generated HSM engine behavior update so lifecycle slots, internal transitions, guarded transitions, and ordered event activities are now part of the main OpenSpec source of truth while preserving the verification audit trail and warnings.
