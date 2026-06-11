## Change Archived

**Change**: svg-activity-text-highlighting
**Archived to**: `openspec/changes/archive/2026-06-03-svg-activity-text-highlighting/`

### Specs Synced
| Domain | Action | Details |
|--------|--------|---------|
| `graphviz-svg-workbench` | Updated | Merged the exact-ID highlight requirement changes for private text-fragment emphasis and row-specific internal-transition highlighting. |
| `hsm-json-graphviz-rendering` | Updated | Added the private render-owned text fragment target requirement and three acceptance scenarios. |

### Verification Used
- `pytest tests/integration/test_mbse_workbench.py::test_start_workbench_server_serves_runtime_session_endpoints_and_svg tests/integration/test_mbse_workbench.py::test_build_and_start_workbench_serves_runtime_ready_static_viewer`
- `pytest tests/integration/test_mbse_workbench.py`

### Archive Contents
- `proposal.md` ✅
- `specs/` ✅
- `design.md` ✅
- `tasks.md` ✅ (8/8 complete)
- `verify-report.md` ✅

### Source of Truth Updated
- `openspec/specs/graphviz-svg-workbench/spec.md`
- `openspec/specs/hsm-json-graphviz-rendering/spec.md`

### SDD Cycle Complete
The stale workbench expectations were aligned with the current init snapshot contract and the change is archived.
