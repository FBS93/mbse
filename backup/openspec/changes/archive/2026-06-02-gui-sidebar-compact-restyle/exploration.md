## Exploration: gui-sidebar-compact-restyle

### Current State
The workbench sidebar lives in `index.html` and is styled entirely by `viewer.css`. It currently renders a title/intro block, then separate `Reset`, `Events`, and `Variables` sections. The reset controls are separate elements, and variable rows are already editable inline but still duplicate the current value in a dedicated `.value-display` span, which makes each row taller than necessary. Runtime behavior is driven by `viewer.js`, and the current variable markup is also parsed by `tests/support/viewer_browser_harness.py` with a regex that assumes the existing HTML structure.

### Affected Areas
- `src/mbse/web/static/index.html` — remove the top title/intro block and regroup reset buttons into one compact horizontal action row.
- `src/mbse/web/static/viewer.css` — darker background, tighter spacing, modernized surfaces, more compact sidebar sections, inline reset actions, and slimmer variable rows.
- `src/mbse/web/static/viewer.js` — simplify variable row markup so the editable textbox is the primary current-value presentation while preserving the existing submit contract.
- `tests/support/viewer_browser_harness.py` — update the regex-based variable row parser if the row markup changes.
- `tests/integration/test_mbse_workbench.py` — update static HTML/CSS assertions that currently expect the header text and exact CSS strings.

### Approaches
1. **CSS-only polish** — Keep the existing markup and only restyle spacing, colors, and button placement.
   - Pros: Lowest risk; minimal test churn; no runtime or harness contract changes.
   - Cons: Cannot fully remove duplicated variable value presentation; compactness gain is limited.
   - Effort: Low

2. **Compact markup refresh** — Remove the sidebar intro, place both reset buttons side by side, and flatten each variable row so the input is the visible current value while keeping submit behavior unchanged.
   - Pros: Best match to the user request; meaningfully reduces sidebar height; keeps scope frontend-only.
   - Cons: Requires coordinated updates in the browser harness and integration assertions.
   - Effort: Medium

### Recommendation
Use **Compact markup refresh**. It stays inside the current frontend boundary, satisfies the compactness goal, and does not require backend or runtime contract changes. Keep `viewer.js` logic changes narrow: only adjust rendered variable HTML, not submission parsing or runtime endpoints.

Review forecast:
- Decision needed before apply: No
- Chained PRs recommended: No
- 400-line budget risk: Low
- Expected review size: roughly 180-280 changed lines across HTML/CSS/JS/tests

### Risks
- The browser harness parses variable rows with a regex tied to `.value-display`, so markup changes can break tests even if runtime behavior is unchanged.
- Integration tests assert exact header text and exact CSS lines, so harmless visual refactors will need synchronized assertion updates.
- Making unset variables compact still needs an explicit visual state; replacing the extra value line with a subtle inline unset badge or placeholder must remain clear.

### Ready for Proposal
Yes — propose a frontend-only restyle that removes the sidebar intro, modernizes the palette, compacts spacing, aligns reset actions horizontally, and simplifies variable rows without changing runtime behavior.
