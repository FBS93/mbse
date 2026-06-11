## Archive Report

**Change**: gui-sidebar-compact-restyle
**Archived On**: 2026-06-02
**Mode**: openspec
**Verification Gate**: PASS WITH WARNINGS — no CRITICAL issues in `verify-report.md`

### Specs Synced

| Domain | Action | Details |
|--------|--------|---------|
| `graphviz-svg-workbench` | Updated | Added `Compact Restyle Stays Presentation-Only`; modified `Persistent Operator Sidebar` to remove the intro/status surfaces, require one compact reset row, and carry the compact overflow expectation; modified `Compact One-Line Variable Rows` so the textbox is the primary current-value surface with an explicit inline unset state. |

### Source Artifacts Reviewed

- `openspec/changes/gui-sidebar-compact-restyle/exploration.md`
- `openspec/changes/gui-sidebar-compact-restyle/proposal.md`
- `openspec/changes/gui-sidebar-compact-restyle/specs/graphviz-svg-workbench/spec.md`
- `openspec/changes/gui-sidebar-compact-restyle/design.md`
- `openspec/changes/gui-sidebar-compact-restyle/tasks.md`
- `openspec/changes/gui-sidebar-compact-restyle/apply-progress.md`
- `openspec/changes/gui-sidebar-compact-restyle/verify-report.md`
- `openspec/specs/graphviz-svg-workbench/spec.md`

### Verification Evidence

- Verdict: `PASS WITH WARNINGS`
- Tasks complete: `10/10`
- Tests: `pytest tests/integration/test_mbse_workbench.py` → `28 passed`; focused recheck `pytest tests/integration/test_mbse_workbench.py -k "serves_runtime_ready_static_viewer or serves_runtime_session_endpoints_and_svg"` → `2 passed`
- Warning carried forward: the scenario `Sidebar overflow appears only when needed` is still only partially proven because current tests validate overflow ownership and isolated scrolling, but do not directly prove that a normal desktop render begins with no required sidebar vertical scroll.
- Warning carried forward: `design.md` still documents the superseded darker/denser palette direction, while the verified and user-accepted final UI restored light sidebar/control/viewport surfaces.

### Archive Verification

- Main spec was updated before archiving.
- The archived change folder retains exploration, proposal, delta specs, design, tasks, apply-progress, verification, and this archive report.
- The active change directory no longer contains `gui-sidebar-compact-restyle` after the move.

### Final Archive Path

`openspec/changes/archive/2026-06-02-gui-sidebar-compact-restyle/`

### Notes

This archive finalizes the compact sidebar restyle in the main OpenSpec source of truth while preserving the verification audit trail, including the remaining overflow-proof gap and the design narrative drift about the superseded darker palette.
