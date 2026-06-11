# Archive Report

- **Change**: `workbench-svg-render-improvements`
- **Mode**: OpenSpec
- **Archived On**: `2026-05-29`
- **Verification Gate**: PASS WITH WARNINGS (see archived `verify-report.md` alongside this report)

## Archive Decision

Archive approved. Verification reported no critical issues, the change stayed render-only, and the remaining warnings are about regression strength rather than current correctness.

## Source-of-Truth Sync

| Domain | Action | Details |
|---|---|---|
| `hsm-json-graphviz-rendering` | Updated | 2 modified requirements synced into main spec; 1 new requirement added; no requirements removed |

## Final Change Scope

- Removed the top `Variables` / `Events` banner from rendered SVG output.
- Clarified flat and compound state visuals with distinct title/body partitioning.
- Preserved exact authored public SVG ids, including compound-state ids.
- Kept private `__anchor` routing internal only.
- Kept runtime, viewer-shell UX beyond render output, and slices A/B out of scope.

## Archive Verification

- [x] Main spec updated before archiving
- [x] Change folder contains proposal, spec delta, design, tasks, apply progress, verify report, and archive report
- [x] Archive destination prepared: `openspec/changes/archive/2026-05-29-workbench-svg-render-improvements/`

## Warnings Carried Forward

- Automated integration coverage still relies on a fake Graphviz command, so final-SVG text/layout regressions against the real `dot` binary are not fully protected by the regular suite.
- Apply history records one stale integration expectation early in Batch B, although the final suite and verification are green.

## Recommended Follow-Up

- Add one automated integration path that exercises the real `dot` binary when available, so the final SVG contract is protected without manual spot-checks during verify.
