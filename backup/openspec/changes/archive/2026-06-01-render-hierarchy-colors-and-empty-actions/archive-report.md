# Archive Report

- **Change**: `render-hierarchy-colors-and-empty-actions`
- **Mode**: OpenSpec
- **Archived On**: `2026-06-01`
- **Verification Gate**: PASS WITH WARNINGS (archived after resolving the documented design drift in `design.md`)

## Archive Decision

Archive approved. Verification found no critical issues, all runtime evidence stayed green, and the only warning was closed by aligning `design.md` with the implemented hierarchy color algorithm before archive.

## Source-of-Truth Sync

| Domain | Action | Details |
|---|---|---|
| `hsm-json-graphviz-rendering` | Updated | 2 modified requirements synced into main spec; 2 new requirements added; 0 requirements removed |

## Final Change Scope

- Applied deterministic hierarchy-derived fills from one base color without changing public SVG IDs.
- Kept empty entry/exit partitions visibly rendered for flat and compound states.
- Preserved private routing anchors as internal-only helpers.
- Kept runtime behavior, validation, and workbench shell behavior out of scope.

## Archive Verification

- [x] Main spec updated before archiving
- [x] Change folder contains proposal, spec delta, design, tasks, apply progress, verify report, and archive report
- [x] Archive destination prepared: `openspec/changes/archive/2026-06-01-render-hierarchy-colors-and-empty-actions/`

## Warnings Carried Forward

- None.

## Recommended Follow-Up

- None.
