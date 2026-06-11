# Design: Workbench Sidebar Compact Restyle

## Technical Approach

Implement the change as a frontend-only markup and CSS refresh inside the existing workbench shell. Keep the current runtime endpoints, fetch flow, session payload shape, and submit handlers intact; only simplify static sidebar structure in `index.html`, narrow `viewer.js` changes to variable-row HTML output, and update test fixtures that parse or assert the old markup/CSS contract.

## Architecture Decisions

| Decision | Options | Choice | Rationale |
|---|---|---|---|
| Simplify sidebar structure without behavior changes | CSS-only polish; compact markup refresh | Compact markup refresh | Removing the intro block and keeping only `Reset`, `Events`, and `Variables` matches the delta spec and reduces vertical waste without touching JS control wiring. Existing IDs and forms stay in place, so behavior remains unchanged. |
| Group reset actions | Keep separate stacked controls; place in one shared row | One compact action row containing the existing reset form button plus the existing view-reset button | This satisfies the spec while preserving the current split in behavior: runtime reset stays a form submit to `/api/runtime/reset`; view reset stays a local click handler. |
| Compact variable rows | Keep `.value-display`; move value into textbox | Make the textbox the visible current-value surface and keep inline unset signaling | This removes duplicated value presentation, shortens each row, and keeps the existing `set_variable(variable_id, value)` flow unchanged. Unset state remains explicit through compact inline text/badge treatment rather than a second line. |
| Visual restyle scope | Rework layout; restyle surfaces only | Darker/denser surface restyle inside existing layout and overflow boundaries | The workbench already has correct page, sidebar, and viewport overflow ownership. The change should modernize palette, borders, spacing, and control chrome without changing grid structure, splitter behavior, or viewport contracts. |
| Test contract updates | Rewrite tests broadly; adjust intentional selectors/parsers only | Update harness parser and brittle static assertions only where contract changed | The risky part is markup/CSS coupling, not runtime semantics. Narrow test updates keep coverage focused on preserved behavior plus the new presentation contract. |

## Data Flow

Runtime flow stays unchanged:

`index.html` structure / `viewer.css` styles
→ `viewer.js` loads session and renders controls
→ existing POST actions (`reset`, `events`, `variables`)
→ backend returns full snapshot
→ `viewer.js` rerenders sidebar rows and highlights

Only the rendered HTML shape for variable rows changes; request/response flow does not.

## File Changes

| File | Action | Description |
|---|---|---|
| `src/mbse/web/static/index.html` | Modify | Remove `.sidebar-header`; keep section order; wrap both reset controls in one compact row/container without changing IDs or form ownership. |
| `src/mbse/web/static/viewer.css` | Modify | Darken page/panel/sidebar surfaces; tighten section and control spacing; style shared reset row; flatten variable rows; preserve layout grid, splitter, and overflow ownership. |
| `src/mbse/web/static/viewer.js` | Modify | Change `renderVariableRow()` markup so the input is the primary value display, submit action stays inline, and unset state is shown compactly without `.value-display`. |
| `tests/support/viewer_browser_harness.py` | Modify | Replace regex assumptions tied to `.value-display` with parsing for the new compact row structure and inline unset marker while keeping current snapshot fields exposed to tests. |
| `tests/integration/test_mbse_workbench.py` | Modify | Remove assertions for the deleted intro/title block and old exact CSS grid string; add assertions for compact reset grouping, absent intro block, textbox-first variable rows, and preserved behavior. |

## Interfaces / Contracts

- No backend, API, or payload changes.
- Preserve existing element IDs used by JS/tests: `reset-form`, `reset-runtime-button`, `reset-view-button`, `event-form`, `event-select`, `variable-list`, `layout-splitter`.
- Variable-row DOM contract changes intentionally: tests/harness must stop depending on `.value-display` and instead read the textbox value plus explicit unset marker.
- Overflow contract remains: page scroll disabled, sidebar owns sidebar overflow, SVG viewport owns diagram overflow.

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Unit-ish harness | Variable rendering, unset/current display, reset-view locality | Update `ViewerBrowserHarness` snapshots to parse compact rows and keep existing action simulation. |
| Integration | Static HTML/CSS contract and preserved runtime endpoints | Update assertions to check removed intro block, section order, reset controls present together, preserved JS endpoints, and preserved overflow/layout primitives without overfitting exact cosmetic values. |
| E2E | None | No E2E layer is configured in this repo. |

## Migration / Rollout

No migration required.

## Open Questions

- [ ] Choose the final inline unset treatment (`text`, badge, or placeholder styling) during apply, while keeping it explicit and single-line.
