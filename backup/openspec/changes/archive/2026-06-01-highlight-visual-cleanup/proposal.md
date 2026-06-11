# Proposal: Highlight Visual Cleanup

## Intent

Tighten active highlight visuals in the SVG workbench so users can read state and transition labels without highlight noise, while still making the active path clearer.

## Scope

### In Scope
- Refine frontend highlight styling so state and transition label text stays visually neutral.
- Strengthen active state emphasis through contour treatment plus a slightly stronger same-hue background.
- Limit active transition emphasis to the edge line and arrowhead only.

### Out of Scope
- Backend, runtime, or snapshot contract changes.
- Graphviz/Jinja SVG generation changes or any new authored-ID behavior.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `graphviz-svg-workbench`: Clarify the frontend highlight visual contract so text labels are excluded from active highlight treatment and state/transition emphasis is applied only to the intended SVG shapes.

## Approach

Keep `viewer.js` exact-ID group highlighting unchanged. Update `viewer.css` to style descendants of `.is-active-state` and `.is-active-transition` selectively: state contours/background shapes get emphasis, transition `path` and arrowhead `polygon` get emphasis, and `text` stays unstyled. Add browser-facing assertions for descendant-targeting behavior.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/mbse/web/static/viewer.css` | Modified | Replace broad group-level highlight rules with descendant selectors. |
| `tests/support/viewer_browser_harness.py` | Modified | Expose enough browser-harness state to assert refined highlight targeting. |
| `tests/integration/test_mbse_workbench.py` | Modified | Verify label text stays neutral and only intended SVG shapes are emphasized. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Graphviz state variants use different child shapes | Medium | Validate selectors against leaf and compound-state SVG output. |
| Selectors catch unintended polygons/dividers | Medium | Add focused browser assertions on contour/background targets. |

## Rollback Plan

Revert the CSS selector changes and related frontend tests, restoring the current broad highlight styling without touching runtime or SVG generation contracts.

## Dependencies

- Existing Graphviz SVG child structure for state groups and transition groups remains stable enough for CSS descendant targeting.

## Success Criteria

- [ ] Active state and transition label text remains outside highlight styling.
- [ ] Active states show clearer contour emphasis plus a mild stronger same-hue background.
- [ ] Active transitions emphasize only the arrow line and arrowhead.
- [ ] No backend, runtime, or exact-SVG-ID contract changes are required.
