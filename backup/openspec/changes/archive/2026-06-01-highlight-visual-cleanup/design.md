# Design: Highlight Visual Cleanup

## Technical Approach

Keep highlight assignment in `viewer.js` exactly as it is today: the backend still returns exact SVG IDs, and the frontend still adds `is-active-state` or `is-active-transition` to the matching `<g>` wrapper. The change stays frontend-only by narrowing `viewer.css` from broad group styling to descendant selectors that target only visual shapes, never label text.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Highlight mechanism | Keep JS group-class assignment unchanged | JS descendant mutation/tagging | Code evidence shows IDs already land on Graphviz wrapper groups (`viewer.js`, Graphviz SVG structure). CSS targeting is the smallest change and preserves the exact-ID contract. |
| State emphasis | Style descendant contour/background shapes under `.is-active-state` | Recolor whole group; backend/SVG changes | Meets the spec goal: labels stay neutral while active states gain contour emphasis plus a mild same-hue background bump. |
| Transition emphasis | Style only descendant edge/arrowhead shapes under `.is-active-transition` | Group-wide stroke rules | Transition groups mix `path`, arrowhead `polygon`, and label `text`; descendant targeting isolates the visible edge without touching labels. |

## Data Flow

Backend snapshot
  -> `active_ids` + optional `last_transition_id`
  -> `viewer.js` adds highlight class to exact SVG `<g id="...">`
  -> `viewer.css` styles only approved descendants inside that group

No runtime, API, or SVG generation flow changes are required.

## File Changes

| File | Action | Description |
|------|--------|-------------|
| `src/mbse/web/static/viewer.css` | Modify | Replace broad `.is-active-*` rules with descendant selectors for state shapes vs transition shapes. |
| `tests/support/viewer_browser_harness.py` | Modify | Expose enough SVG descendant structure from highlighted groups to assert selector intent in browser-facing tests. |
| `tests/integration/test_mbse_workbench.py` | Modify | Add integration coverage for label exclusion and shape-only emphasis. |

## Interfaces / Contracts

No API or data-model changes.

Selector strategy:
- **Leaf states**: target direct shape descendants inside `.is-active-state`, with `text` explicitly untouched. Prefer direct-child selectors such as `.is-active-state > polygon` / `.is-active-state > path` over broad descendant walks.
- **Compound states**: target the cluster wrapper’s direct contour/background shapes the same way, still excluding `text`. Keep selectors narrow enough that nested child-state labels are not restyled through the parent cluster.
- **Transition groups**: target `.is-active-transition > path` for the edge line and `.is-active-transition > polygon` for the arrowhead; do not style `text`.

If code validation shows Graphviz emits extra direct-child polygons that should stay neutral, refine the selector to a smaller direct-child subset before adding any JS mutation.

## Testing Strategy

| Layer | What to Test | Approach |
|-------|-------------|----------|
| Unit-ish browser harness | Highlight groups still receive exact classes | Keep current class-ID assertions intact. |
| Browser harness / integration | Highlighted leaf state exposes only shape descendants as targets, not text | Extend harness snapshot with highlighted group child tags / raw descendant summary and assert text remains outside the target set. |
| Browser harness / integration | Compound-state groups use the same exclusion rule | Add an SVG fixture with a compound cluster and verify only contour/background descendants are considered highlightable. |
| Integration | Transition highlight targets edge path and arrowhead only | Add an SVG fixture containing `path`, arrowhead `polygon`, and label `text`, then assert only path/polygon are targeted. |
| Static asset check | CSS contains the expected descendant selectors | Extend existing `viewer.css` assertions with the new selector strings. |

## Migration / Rollout

No migration required.

## Open Questions

- [ ] Confirm whether active leaf-state SVG output includes only safe direct-child shape nodes, or whether one selector needs narrowing to avoid internal divider emphasis.
