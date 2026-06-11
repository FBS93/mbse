# Design: Workbench UI Improvements

## Technical Approach

Keep the existing static viewer (`index.html` + `viewer.css` + `viewer.js`) and widen it into a stronger two-pane operator layout without changing Python server/runtime contracts. The left pane becomes a persistent sidebar rendered from `session.event_ids`, `session.variable_ids`, and `session.snapshot`; the right pane adds a small SVG viewport toolbar with client-only zoom state.

## Architecture Decisions

| Decision | Options | Choice | Rationale |
|---|---|---|---|
| Two-panel layout | Rebuild page shell; refine current grid | Refine current grid into `sidebar + canvas` | Smallest slice, matches current structure, keeps review scope in static assets only |
| Variable editing UX | Keep one global form; add backend metadata; inline row editing using current IDs | Sidebar variable list plus one shared editor bound to selected row | Preserves `set_variable(variable_id, value)` exactly, avoids backend change, keeps DOM/simple JS manageable |
| SVG zoom | Re-render from backend; manipulate SVG `viewBox`; scale inner wrapper with scroll container | Client-side scale state on a diagram stage inside a scrollable pane | No server/API drift, minimal risk, easy reset behavior |

## Data Flow

```text
/api/session.json ──→ renderSession()
                        ├─→ sidebar sections
                        │    ├─→ state + active path
                        │    ├─→ variable rows from variable_ids + snapshot.variables
                        │    └─→ event/reset controls + status
                        └─→ SVG highlights

variable row/select ──→ shared editor form ──→ POST /api/runtime/variables
                                             └─→ refreshed session ──→ renderSession()

zoom buttons ──→ local zoom state ──→ CSS transform / scrollable stage only
```

## File Changes

| File | Action | Description |
|---|---|---|
| `openspec/changes/workbench-ui-improvements/design.md` | Create | Technical design for this slice |
| `src/mbse/web/static/index.html` | Modify | Introduce semantic sidebar sections, variable list container, shared variable editor, diagram toolbar, and scrollable SVG viewport wrappers |
| `src/mbse/web/static/viewer.css` | Modify | Define persistent two-pane layout, sidebar section hierarchy, variable row styling, sticky/visible toolbar, and overflow-safe SVG viewport behavior |
| `src/mbse/web/static/viewer.js` | Modify | Render variable/state sections, keep shared editor synced to selected variable, handle status messages, and implement local zoom/reset state |
| `tests/integration/test_mbse_workbench.py` | Modify | Assert new static labels/containers and confirm runtime endpoints remain unchanged |

## Interfaces / Contracts

No backend contract changes.

Existing payload remains the source of truth:

```json
{
  "document_id": "...",
  "svg_url": "/artifacts/diagram.svg",
  "event_ids": ["..."],
  "variable_ids": ["..."],
  "snapshot": {
    "state_id": "...",
    "active_path": ["..."],
    "active_ids": ["..."],
    "variables": {"speed": 3}
  }
}
```

Frontend rendering rule: iterate `variable_ids` as the declared order, look up each value in `snapshot.variables`, and show `unset` when absent. Variable submission still sends `{ variable_id, value }` to `/api/runtime/variables`; invalid JSON stays a client-side error/status and does not create a new endpoint shape.

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Integration | New page structure is present | Extend `test_mbse_workbench.py` HTML assertions for sidebar sections and zoom controls |
| Integration | Runtime contract stays identical | Keep current JSON endpoint assertions unchanged while adding UI text checks |
| Integration | Static assets carry new client behavior | Assert `viewer.js` still references only existing runtime endpoints and includes zoom handler identifiers |

## Migration / Rollout

No migration required.

## Open Questions

- [ ] Small-width behavior: this design assumes a normal desktop width; implementation should stack panes below that breakpoint without inventing a new mobile workflow.
- [ ] Zoom bounds should be capped during implementation (for example min/max scale) to avoid unreadable or excessively large canvases.
