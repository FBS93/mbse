# Archive Report

- **Change**: `init-transition-rendering-cleanup`
- **Mode**: OpenSpec
- **Archived On**: `2026-06-01`
- **Verification Gate**: PASS WITH SUGGESTION (no critical issues; see archived `verify-report.md`)

## Archive Decision

Archive approved. Verification passed with no critical or warning issues, all 9 tasks are complete, and the delta cleanly tightens the render contract around visible initial-source markers versus private routing anchors.

## Source-of-Truth Sync

| Domain | Action | Details |
|---|---|---|
| `hsm-json-graphviz-rendering` | Updated | 1 modified requirement synced into main spec; 0 new requirements added; 0 requirements removed |

## Final Change Scope

- Preserved exact authored public SVG IDs for states, compound clusters, transitions, and initial transitions.
- Kept root and local initial source pseudostates visibly rendered as black points.
- Kept private target and compound routing anchors internal-only, non-highlightable, and invisible in final SVG output.
- Preserved clean compound/init routing without stray destination dots or helper ellipses.

## Archive Verification

- [x] Main spec updated before archiving
- [x] Change folder contains proposal, spec delta, design, tasks, apply progress, verify report, and archive report
- [x] Archive destination prepared: `openspec/changes/archive/2026-06-01-init-transition-rendering-cleanup/`

## Warnings Carried Forward

- None.

## Suggested Follow-Up

- Real Graphviz still leaves helper names in non-public SVG comments/edge titles; tighten that boundary later if any downstream consumer starts treating titles/comments as API.
