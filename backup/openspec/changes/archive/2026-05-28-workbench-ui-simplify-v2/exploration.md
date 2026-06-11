## Exploration: workbench-ui-simplify-v2

### Current State
The current workbench already keeps runtime semantics in the backend and UI behavior in static assets only: `index.html` defines the sidebar/diagram shell, `viewer.js` fetches `/api/session.json` plus the three existing runtime mutation endpoints, and `viewer.css` provides the two-pane layout with a scrollable `#svg-viewport`. The current UI still exposes `Current state`, `Current snapshot`, a separate runtime reset section below variables, button-only zoom controls, and a selected-variable editor form that mirrors the clicked variable row.

### Affected Areas
- `src/mbse/web/static/index.html` — reorder/remove sidebar sections and simplify visible controls
- `src/mbse/web/static/viewer.js` — keep the same runtime calls, reuse `applyZoom()`, and adapt variable/event wiring to the simplified shell
- `src/mbse/web/static/viewer.css` — preserve the two-pane layout while tightening spacing after section removal and reset relocation
- `tests/integration/test_mbse_workbench.py` — update HTML assertions and add/adjust client behavior expectations for wheel zoom and removed headings
- `tests/support/viewer_browser_harness.py` — likely extend the browser harness if wheel zoom is verified with executed client behavior instead of source-string checks
- `openspec/specs/graphviz-svg-workbench/spec.md` — current main spec still explicitly requires a `current state` sidebar section and `Zoom in` / `Zoom out` / `Reset view` controls, so this v2 simplification needs a spec delta before apply

### Approaches
1. **Markup simplification + wheel zoom over existing zoom state** — keep backend/runtime untouched, remove the two obsolete readout sections, move `Reset runtime` to the top, keep variables/events driven by the same existing session payload, and bind mouse wheel on `#svg-viewport` to the already existing `applyZoom()` state.
   - Pros: Smallest safe slice, no API/runtime drift, reuses current `zoomScale` and mutation flows, aligns with natural diagram interaction
   - Cons: Needs a small test harness extension for wheel behavior if we want executed evidence; must decide whether visible zoom buttons stay temporarily or are removed in the same delta
   - Effort: Low

2. **Ctrl+wheel gated zoom** — reuse the same client-only zoom state but require `Ctrl` while scrolling.
   - Pros: Lower risk of accidental zoom while the user just wants to scroll the viewport
   - Cons: Less natural than requested, worse discoverability, and unnecessary unless accidental wheel capture becomes a demonstrated problem
   - Effort: Low

### Recommendation
Use **Markup simplification + wheel zoom over existing zoom state**. It is the narrowest change because the diagram viewport is already scrollable, `viewer.js` already owns bounded client-side zoom state, and the requested sidebar cleanup lives entirely in static HTML/CSS/JS.

For safety, keep the runtime contract frozen: no server changes, no new payload fields, no mutation flow changes. The implementation path should reuse the current `applyZoom()` clamp and bind wheel handling only inside `#svg-viewport`; `Variables` should remain derived from `session.variable_ids` + `session.snapshot.variables`, and `Events` should stay a simple `select` + `Send` button using `/api/runtime/events`.

### Risks
- The current main spec explicitly requires a `current state` section and named zoom controls, so removing those UI elements is not spec-compliant until the new change writes a delta.
- Natural wheel zoom can fight normal scroll behavior if `preventDefault()` is applied too aggressively; it should be scoped strictly to the diagram viewport and validated against the existing overflow behavior.
- The current variable editor is selection-based (`hidden variable_id` + shared input). Converting it to feel like a simple live editable list without changing runtime semantics must still preserve the exact `{ variable_id, value }` mutation contract.

### Ready for Proposal
Yes — propose a UI-only delta that explicitly updates the sidebar structure, permits wheel-based client zoom in the diagram viewport, and preserves the exact existing backend/runtime semantics.
