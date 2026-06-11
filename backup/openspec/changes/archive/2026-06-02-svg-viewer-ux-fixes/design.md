# Design: SVG Viewer UX Fixes

## Technical Approach

Keep the existing scroll-based viewer model and correct the UX at the edges instead of replacing it. The change stays inside the current static frontend assets and test harness: tighten pan gesture ownership in `viewer.js`, recompute the fit baseline from live viewport geometry, and make layout overflow ownership explicit in `viewer.css` and existing markup.

## Architecture Decisions

### Decision: Preserve the scroll-based pan model

| Option | Tradeoff | Decision |
|---|---|---|
| Rewrite pan/zoom around freeform transforms | More flexibility, but breaks scope and increases regression risk | Rejected |
| Keep scroll offsets as the pan source of truth | Matches current code and tests; smaller, reviewable fix | Chosen |

Rationale: the spec only requires UX correction. Current pan already uses viewport scroll offsets, so the safest path is to make drag ownership reliable without changing the navigation model.

### Decision: Capture pan at the document level during active drag

| Option | Tradeoff | Decision |
|---|---|---|
| Keep `mousemove`/`mouseup` only on `#svg-viewport` | Loses drag continuity when pointer exits viewport; selection side effects remain likely | Rejected |
| Bind move/end handlers to `document` for active pan and suppress selection only during the gesture | Slightly more state, but continuous drag and isolated side-effect control | Chosen |

Rationale: on `mousedown` inside the viewport, the viewer should record starting pointer and scroll offsets, mark a pan-active state, temporarily disable selection/cursor side effects, and release that state on `mouseup`/cancel. This preserves drag continuity even if the pointer crosses SVG text or leaves the viewport briefly.

### Decision: Split fit-baseline computation from interactive zoom bounds

| Option | Tradeoff | Decision |
|---|---|---|
| Keep using clamped zoom for fit baseline | Large diagrams can never fully fit below `MIN_ZOOM`, so reset/load stay clipped | Rejected |
| Store a recomputed fit baseline separately from user zoom stepping | Adds one more concept, but matches spec and existing scroll model | Chosen |

Rationale: baseline fit must come from current viewport and SVG dimensions, even when that fit is below the normal wheel-zoom minimum. Reset and first load should recompute this baseline; wheel zoom can still clamp relative interactive values afterward.

### Decision: Make overflow ownership explicit by container responsibility

| Option | Tradeoff | Decision |
|---|---|---|
| Let body, sidebar, and canvas all scroll opportunistically | Ambiguous ownership and page drift | Rejected |
| Lock page overflow, keep sidebar vertical overflow local, and let viewport own diagram overflow via stage sizing | Requires coordinated CSS + stage sizing updates, but behavior is deterministic | Chosen |

Rationale: the page should be fixed while the workbench is open. The sidebar owns its own overflow; the canvas owns only diagram overflow. To make that truthful, `#svg-stage` dimensions must track effective scaled content size so scrollbars appear only when zoom/pan exceed fitted bounds.

## Data Flow

`loadSession()` → inject SVG → measure viewport + SVG → compute fit baseline → apply zoom + stage size + scroll offsets

`mousedown` in viewport → set pan state + drag guards → `document.mousemove` updates viewport scroll → `document.mouseup` clears pan state

splitter drag / reset view / resize-sensitive change → recompute fit baseline from current viewport → apply baseline

## File Changes

| File | Action | Description |
|---|---|---|
| `src/mbse/web/static/viewer.js` | Modify | Add pan lifecycle guards, document-scoped drag continuity, recomputed fit baseline, and scaled stage sizing tied to effective zoom. |
| `src/mbse/web/static/viewer.css` | Modify | Lock page scroll, isolate sidebar overflow, define viewport/stage sizing, and add pan-active selection suppression hooks. |
| `src/mbse/web/static/index.html` | Modify | Keep structure, but allow any minimal class/attribute hooks needed for pan-active and overflow semantics. |
| `tests/support/viewer_browser_harness.py` | Modify | Expose document-level drag end/move behavior, viewport resize/reset assertions, and selection-state snapshots. |
| `tests/integration/test_mbse_workbench.py` | Modify | Add regression coverage for drag continuity, fit recomputation after width/viewport changes, and scroll ownership rules. |

## Interfaces / Contracts

No backend or API contract changes. Frontend-only contract additions are internal:
- viewer state tracks whether a pan gesture is active
- fit baseline is recomputed from live viewport geometry on first load, reset, and layout-affecting viewport changes
- stage sizing derives from measured SVG size × effective zoom

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Unit-ish harness | Baseline fit math, reset after sidebar resize, stage overflow behavior | Extend `ViewerBrowserHarness` snapshots and interaction helpers |
| Integration | No extra runtime requests, pan continuity, isolated sidebar/canvas scroll behavior | Add focused pytest cases in `test_mbse_workbench.py` |
| E2E | None | Not available in repo |

## Migration / Rollout

No migration required.

## Open Questions

- [ ] None.
