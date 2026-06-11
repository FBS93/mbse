# Design: SVG Render Activity Parity

## Technical Approach

Keep this slice strictly render-only and aligned to the normalized `on_initial` model. Reuse the current prepared-render pipeline in `prepare_hsm_render_view()` to emit ordered state-body sections for `on_initial`, `on_entry`, `on_exit`, and `internal_transitions`, plus compact normal-transition labels. Initial transitions remain routing-only edges: they keep authored IDs and visible source dots, but never render activity text or `initial_transition:` copy. This matches the updated spec and avoids pulling future activity-highlighting work into this slice.

## Architecture Decisions

| Decision | Choice | Alternatives considered | Rationale |
|---|---|---|---|
| Render seam | Keep behavior shaping in `prepare_hsm_render_view()` and keep the DOT template presentation-only | Move formatting into Jinja | Deterministic ordering and punctuation rules are easier to test in Python than in template branches. |
| State-body structure | Reuse ordered `body_sections` for `on_initial`, `on_entry`, `on_exit`, then `internal_transitions:` | Collapse everything back into ad-hoc `body_lines` strings | The codebase already has section DTOs; using them keeps authored order explicit and fits the current model cleanly. |
| Initial-transition handling | Keep initials unlabeled and routing-only after normalization | Render `/activity` text on initial edges or revive `initial_transition:` sections | The spec now explicitly forbids visible initial activity labels. This slice must follow the normalized model, not the older authored-edge idea. |
| Scope boundary | Do not add activity-level public IDs, viewer hooks, or runtime changes | Sneak in highlighting groundwork | The change must stay reviewable and preserve the public SVG contract. Highlighting is a separate change. |

## Data Flow

Author JSON → `load_hsm_document()` → `prepare_hsm_render_view()` → `render_hsm_dot()` → Graphviz SVG

- Event metadata is formatted once into deterministic event signatures.
- State nodes gather authored lifecycle hooks plus state-owned internal transitions in authored order.
- Normal transitions format visible labels as `event [guard]/activity`, omitting missing parts without placeholder punctuation.
- Initial transitions only resolve routing endpoints and authored/public IDs; no visible activity text is prepared.
- The DOT template renders existing public IDs and private routing helpers without exposing helper IDs in `highlightable_ids`.

## File Changes

| File | Action | Description |
|---|---|---|
| `src/mbse/application/prepare_hsm_render.py` | Modify | Finalize normalized parity shaping: keep ordered state-body sections, compact internal-transition rows, normal-transition guard/activity labels, and unlabeled initial edges. |
| `src/mbse/infrastructure/templates/hsm_v1.dot.j2` | Modify | Keep state-body section rendering and ensure initial edges stay `label=""` while normal transitions render prepared labels only. |
| `tests/unit/mbse/test_hsm_render_view.py` | Modify | Lock authored ordering, omission rules, unlabeled initial-edge behavior, and exact public-ID order in DOT. |
| `tests/integration/test_hsm_json_workbench.py` | Modify | Prove prepared DOT/SVG show lifecycle/internal/normal-transition parity text while preserving authored public IDs and hiding private helpers. |

## Interfaces / Contracts

- State body contract:
  - Render sections in authored order: `on_initial:`, `on_entry:`, `on_exit:`.
  - Append `internal_transitions:` after lifecycle sections when present.
  - Internal-transition rows use compact `event/activity` text and omit `/activity` when none exists.
- Normal transition label contract:
  - Base text is the existing event signature.
  - Guard renders as ` [guard]` only when present.
  - Activities render as `/activity1, activity2` only when present.
  - Never emit empty `[]`, dangling `/`, or doubled spacing.
- Initial transition contract:
  - Public IDs remain the authored initial IDs.
  - Source pseudostates stay visible.
  - Visible labels remain empty; no authored `initial.activities` text is surfaced in DOT or SVG.
- Public ID contract:
  - `highlightable_ids` remain limited to authored states, initial transitions, and normal transitions.
  - Hooks, internal rows, guards, activities, and routing helpers never become public SVG IDs.

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Unit | Ordered state-body shaping | Assert exact `body_sections` content for `on_initial`, `on_entry`, `on_exit`, and `internal_transitions:`. |
| Unit | Normal-transition label formatting | Cover event-only, guard-only-with-event, activity-only-with-event, and full `event [guard]/activity` cases. |
| Unit | Initial-edge routing-only behavior | Assert all initial-edge labels stay `None` and DOT keeps `label=""` for initials. |
| Integration | Prepared document and SVG contract | Verify visible parity text appears for lifecycle/internal/normal transitions while `highlightable_ids` and authored SVG IDs remain unchanged and helpers stay private. |

## Migration / Rollout

No migration required. This is a render-only refinement over existing normalized behavior.

## Open Questions

- [x] None blocking. Activity highlighting remains intentionally out of scope for this slice.
