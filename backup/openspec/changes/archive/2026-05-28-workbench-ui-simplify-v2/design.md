# Design: Workbench UI Simplify v2

## Technical Approach

Keep the change inside the existing static viewer shell only. `index.html`, `viewer.js`, and `viewer.css` will be reduced to one simpler operator sidebar plus wheel-based viewport zoom, while the Python runtime bridge, payload shape, and mutation endpoints stay exactly as they are today.

## Architecture Decisions

| Decision | Options | Choice | Rationale |
|---|---|---|---|
| Sidebar structure | Keep current sections; simplify in place | Keep header, then order sections as `Reset`, `Variables`, `Events`, `Status` | Smallest DOM change that matches the delta spec and removes the two obsolete readouts cleanly |
| Variable editing | Keep selected-row shared editor; inline per-row editor | Render one compact form per variable row | Better matches “editable list entry”, removes selection state, and still submits the same `{ variable_id, value }` contract |
| Event controls | Buttons per event; keep current select+button | Keep one `select` plus one `Send` button | Already matches the spec delta and avoids any runtime/API drift |
| Zoom interaction | Keep buttons; ctrl+wheel; plain wheel | Bind plain wheel on `#svg-viewport` and clamp with existing zoom constants | Requested behavior, frontend-only, and reuses the current client zoom state without backend work |

## Data Flow

```text
/api/session.json -> renderSession()
                    |- renderVariableList(variable_ids, snapshot.variables)
                    |- renderSelectOptions(event_ids)
                    |- renderStatus()
                    `- applyHighlights(active_ids)

variable row form submit -> POST /api/runtime/variables
                         -> returned session -> renderSession()

event form submit -> POST /api/runtime/events
                  -> returned session -> renderSession()

reset form submit -> POST /api/runtime/reset
                  -> returned session -> renderSession()

wheel on #svg-viewport -> applyZoom(clampedScale)
```

## File Changes

| File | Action | Description |
|---|---|---|
| `openspec/changes/workbench-ui-simplify-v2/design.md` | Create | Short technical design for this slice |
| `src/mbse/web/static/index.html` | Modify | Remove `Current state`, shared variable editor, `Current snapshot`, and zoom toolbar; keep header plus `Reset`, `Variables`, `Events`, `Status` sections |
| `src/mbse/web/static/viewer.js` | Modify | Replace selected-variable logic with per-row variable forms, keep existing reset/event/runtime calls, and bind wheel zoom on `#svg-viewport` only |
| `src/mbse/web/static/viewer.css` | Modify | Tighten sidebar spacing, style inline variable rows/forms, and remove toolbar-specific styles no longer used |
| `tests/integration/test_mbse_workbench.py` | Modify | Update HTML/source assertions for removed headings/buttons, variable list structure, and wheel-zoom behavior staying client-side |
| `tests/support/viewer_browser_harness.py` | Modify | Add enough DOM/event support to simulate per-row variable forms and wheel events in executed browser-style tests |

## Interfaces / Contracts

No backend or runtime contract changes.

- Variables still derive from `session.variable_ids` + `session.snapshot.variables`.
- Each variable row submits only `{ variable_id, value }` to `/api/runtime/variables`.
- Events still submit only `{ event_id }` to `/api/runtime/events`.
- Zoom updates only local `viewerState.zoomScale`; it does not fetch, post, or alter runtime state.

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Integration | Simplified sidebar structure | Update server-rendered HTML assertions to require `Reset`, `Variables`, `Events`, `Status` and forbid removed headings |
| Integration | Editable variable list | Use the browser harness to verify all declared variables render with current/unset values and editable row inputs |
| Integration | Wheel zoom stays client-side | Simulate wheel events in the harness, assert `scale(...)` changes, and confirm no extra runtime fetches occur |

## Migration / Rollout

No migration required.

## Open Questions

- [ ] None. The slice is fully constrained to static frontend assets and test support.
