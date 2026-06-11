# Archive Report: generated-hsm-engine

## Outcome

- Status: archived
- Archived on: 2026-05-27
- Verify verdict: PASS
- Persistence mode: openspec

## Source Artifacts

- `openspec/changes/generated-hsm-engine/proposal.md`
- `openspec/changes/generated-hsm-engine/specs/hsm-json-graphviz-rendering/spec.md`
- `openspec/changes/generated-hsm-engine/specs/generated-hsm-engine/spec.md`
- `openspec/changes/generated-hsm-engine/design.md`
- `openspec/changes/generated-hsm-engine/tasks.md`
- `openspec/changes/generated-hsm-engine/verify-report.md`

## Spec Sync Summary

| Domain | Action | Details |
|--------|--------|---------|
| `hsm-json-graphviz-rendering` | Updated | Replaced `Explicit v1 Boundary` to narrow the non-executable rule to rendering and added the render-pipeline inertness scenario. |
| `generated-hsm-engine` | Created | Promoted the new runtime capability spec into main specs as a new source-of-truth domain. |

## Verified Boundaries Preserved

- Generated engine remains derived from validated JSON HSM documents.
- State handling follows the QPC-style one-function-per-state approach.
- Runtime stays handwritten and minimal behind the stable public API.
- `on_entry` and `on_exit` remain inert metadata in this iteration.
- No advanced runtime scope was added during archive.

## Archive Verification Checklist

- [x] Main specs updated before archive move.
- [x] Verified change report contains no CRITICAL issues.
- [x] Change folder is ready to move into dated archive.
- [x] Archive report included in archived audit trail.
