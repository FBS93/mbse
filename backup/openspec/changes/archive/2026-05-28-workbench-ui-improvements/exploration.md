## Exploration: workbench-ui-improvements

### Current State
The workbench is a thin static HTML/CSS/JS viewer served by `src/mbse/web/server.py`. The frontend loads one runtime session from `/api/session.json`, renders `diagram.svg`, highlights `snapshot.active_ids`, and exposes reset/event/variable mutation forms. The left panel currently shows only form controls plus a raw JSON snapshot, so variable values are not persistently visible except inside that JSON blob. The SVG area has no zoom controls, no viewport state, and only `max-width: 100%` styling.

### Affected Areas
- `src/mbse/web/static/index.html` — current two-panel structure and control placeholders
- `src/mbse/web/static/viewer.js` — session rendering, snapshot display, highlight refresh, runtime form wiring
- `src/mbse/web/static/viewer.css` — layout, panel sizing, SVG presentation, active highlight styling
- `tests/integration/test_mbse_workbench.py` — runtime-ready viewer expectations and static asset assertions
- `openspec/specs/graphviz-svg-workbench/spec.md` — current scope explicitly excludes visual redesign/polish, so a delta spec will be needed before implementation

### Approaches
1. **Frontend-only visibility slice** — keep backend/runtime contract unchanged and derive the improved UI entirely from existing `event_ids`, `variable_ids`, and `snapshot` data.
   - Pros: Smallest slice, no runtime semantic changes, reuses existing API, low regression risk
   - Cons: Variable panel can only show IDs plus current JSON values; no richer metadata like labels or types
   - Effort: Low

2. **Frontend plus richer session metadata** — extend `/api/session.json` to include structured variable/event descriptors for nicer UI copy and future controls.
   - Pros: Better long-term UI model, cleaner future extensibility
   - Cons: Expands backend contract, touches app-state models, larger review surface than the requested slice
   - Effort: Medium

### Recommendation
Use **Frontend-only visibility slice** first. Build a persistent left sidebar that always renders every declared variable ID with its current value (or an explicit `unset` state) by combining `session.variable_ids` with `session.snapshot.variables`. Replace the raw snapshot-first presentation with clearer sections: current state, active path, variables, runtime actions, and status/errors. Add SVG toolbar controls (`Zoom in`, `Zoom out`, `Reset view`) implemented client-side in the diagram pane only, with no backend changes.

For the zoom implementation, prefer a small client-side viewport state around the loaded SVG container rather than changing the runtime contract. This keeps the slice aligned with the user's priority: better visibility and navigation without changing execution semantics.

### Risks
- The current main spec marks visual redesign/polish as out of scope, so implementation should not start until a change proposal/spec explicitly widens that boundary.
- A CSS-transform zoom approach is simpler but can introduce clipping/scroll quirks if the diagram container is not made scrollable.
- Because variables are currently identified only by ID, the improved panel can show stable values but not human-friendly labels unless a later change expands metadata.

### Ready for Proposal
Yes — propose a narrow UI-only delta: persistent variables/status sidebar, clearer snapshot presentation, and client-side SVG zoom controls with no runtime-semantic or server-contract changes.
