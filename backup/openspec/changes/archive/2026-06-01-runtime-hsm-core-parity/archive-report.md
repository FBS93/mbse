## Archive Report

**Change**: runtime-hsm-core-parity
**Archived on**: 2026-06-01
**Mode**: openspec
**Verification gate**: PASS WITH WARNINGS

### Inputs Reviewed
- `openspec/changes/runtime-hsm-core-parity/proposal.md`
- `openspec/changes/runtime-hsm-core-parity/specs/generated-hsm-engine/spec.md`
- `openspec/changes/runtime-hsm-core-parity/design.md`
- `openspec/changes/runtime-hsm-core-parity/tasks.md`
- `openspec/changes/runtime-hsm-core-parity/verify-report.md`
- `openspec/specs/generated-hsm-engine/spec.md`

### Spec Sync Summary
| Domain | Action | Details |
|--------|--------|---------|
| `generated-hsm-engine` | Updated | Merged 2 modified requirements from delta into the main spec; preserved unrelated requirements (`Stable Runtime API`, `Generated Engine And Handwritten Runtime Stay Separated`). |

### Merge Details
- Replaced `Minimal Hierarchical Execution Semantics` with the verified parity semantics for full initial descent, handler-source dispatch, LCA-trimmed paths, nested initial descent, and explicit self/ancestor/descendant/cross-branch outcomes.
- Replaced `Explicit v1 Exclusions And Safety` with the verified exclusion set that keeps AO/pub-sub, scheduler behavior, reserved events, fixed-depth buffers, and other embedded-only mechanics out of scope.
- Preserved main-spec requirements not mentioned by the delta.

### Archive Verification
- [x] Main spec updated before archive move
- [x] Change folder contains proposal, specs, design, tasks, verify report, and archive report
- [x] Verification report has no CRITICAL issues
- [x] Archive destination uses ISO date prefix

### Warnings Carried Forward
- Coverage analysis could not run because `pytest-cov` is not installed.
- Ruff quality checks could not run because `ruff` is not installed.

### Result
The delta spec has been synchronized into `openspec/specs/generated-hsm-engine/spec.md`, and the change is ready to move into the OpenSpec archive as the completed audit trail.
