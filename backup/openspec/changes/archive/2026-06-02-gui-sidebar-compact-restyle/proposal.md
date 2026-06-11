# Proposal: Workbench Sidebar Compact Restyle

## Intent

Refresh the workbench sidebar with a darker, cleaner visual treatment and denser layout so operators see more controls with less scrolling, without changing runtime behavior, workflows, or feature scope.

## Scope

### In Scope
- Darken sidebar/background surfaces and apply small modern polish to borders, spacing, and section treatments.
- Remove the top title/intro block to reclaim vertical space.
- Present `Reset runtime` and `Reset view` side by side in one compact action row.
- Flatten variable rows so the editable textbox is the visible current value; keep explicit unset treatment inline.
- Tighten section, row, and control spacing across the sidebar while preserving existing behavior.
- Allow small tasteful frontend-only aesthetic improvements that support the compact restyle.

### Out of Scope
- Backend endpoints, runtime semantics, snapshot shape, or mutation contracts.
- Workflow changes, new features, mobile redesign, or new status surfaces.
- Any change to reset/event/variable functionality beyond presentation and layout.

## Capabilities

### New Capabilities
None.

### Modified Capabilities
- `graphviz-svg-workbench`: refine sidebar presentation requirements for denser surfaces, compact reset actions, and textbox-first variable value display while keeping existing frontend/runtime contracts.

## Approach

Apply the exploration recommendation: keep this as a compact markup refresh. Update `index.html` and `viewer.css` for layout/visual changes, narrow `viewer.js` changes to variable row markup only, and sync browser-harness plus integration assertions to the new HTML/CSS contract.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/mbse/web/static/index.html` | Modified | Remove intro block; compact reset section layout |
| `src/mbse/web/static/viewer.css` | Modified | Darker surfaces, tighter spacing, modernized sidebar styling |
| `src/mbse/web/static/viewer.js` | Modified | Render textbox as visible variable value without changing submit flow |
| `tests/support/viewer_browser_harness.py` | Modified | Align regex parser with updated variable row markup |
| `tests/integration/test_mbse_workbench.py` | Modified | Update assertions tied to removed header and restyled markup/CSS |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Harness regex breaks on row markup change | Med | Update parser alongside JS markup change |
| Brittle UI assertions fail on cosmetic edits | Med | Update integration assertions to new intentional contract |

## Rollback Plan

Revert the sidebar HTML/CSS/JS changes and corresponding test updates, restoring the prior intro block, button placement, and variable row markup.

## Dependencies

- `openspec/changes/gui-sidebar-compact-restyle/exploration.md`

## Success Criteria

- [ ] Sidebar shows a darker, denser restyle with no intro block and no added functionality.
- [ ] `Reset runtime` and `Reset view` render side by side and keep their current distinct behaviors.
- [ ] Variable rows remain editable, visibly show current or unset value through the textbox/inline state, and require less vertical space.
- [ ] Tests reflect the new frontend contract without backend/runtime changes.
