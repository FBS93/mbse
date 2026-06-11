# Archive Report: runtime-last-event-semantics

## Summary

Archived `runtime-last-event-semantics` after verified PASS WITH WARNINGS. Synced the verified delta requirements into the main runtime and workbench specs, then preserved the whole change folder as a dated audit trail.

## Quick Path

1. Merged the verified delta requirements into the main OpenSpec source of truth.
2. Preserved the warning context about skipped evidence-only strict-TDD artifact reconstruction as archive-only history.
3. Prepared the change folder for dated archive move.

## Specs Synced

| Domain | Action | Details |
|---|---|---|
| `generated-hsm-engine` | Updated | 1 modified requirement synced (`Stable Runtime API`) with last-event semantics and scenarios for unhandled, internal, and external handling. |
| `graphviz-svg-workbench` | Updated | 1 modified requirement synced (`In-Memory Runtime Bridge Contract`) so viewer snapshots consume semantic `last_event` data without reviving viewer-facing `last_transition_id`. |

## Archive Verification

- [x] Main specs updated from the verified deltas.
- [x] Verify report shows no critical blocker and records targeted `44/44` plus full `103/103` pytest passes.
- [x] Archive keeps proposal, specs, design, tasks, verify report, and archive report together.
- [x] Active changes should no longer list `runtime-last-event-semantics` after move.

## Warnings Carried Forward

- Strict-TDD evidence-only artifact reconstruction was intentionally skipped by explicit user direction. This remains archived warning context only and does not reopen implementation or planning.
- Coverage, lint, and type-check evidence were not added in this lightweight closure.

## Archived To

`openspec/changes/archive/2026-06-03-runtime-last-event-semantics/`
