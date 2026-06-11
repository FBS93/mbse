## Exploration: workbench-highlight-polish

### Current State
The workbench frontend applies highlight styling by toggling `.is-active` on every ID returned in `session.snapshot.active_ids`. The backend currently derives `active_ids` by filtering `snapshot.active_path`, so compound states highlight both parent and child when both IDs exist in the SVG. Highlight styling is a single aggressive stroke rule in `viewer.css`, and the runtime/session contract does not expose any "last transition" identifier for the frontend to highlight.

### Affected Areas
- `src/mbse/web/static/viewer.js` — applies highlight classes from `snapshot.active_ids` only
- `src/mbse/web/static/viewer.css` — defines the current single `.is-active` stroke treatment
- `src/mbse/application/web_runtime_bridge.py` — serializes `active_ids` from `active_path`
- `src/mbse/application/hsm_runtime.py` — owns runtime snapshot generation but does not retain the transition that most recently fired
- `src/mbse/domain/models.py` — viewer snapshot shape would need one small addition if transition highlighting becomes backend-driven
- `tests/unit/mbse/test_web_runtime_bridge.py` — contract tests for `active_ids`
- `tests/integration/test_mbse_workbench.py` — viewer/server contract tests for snapshot payload and static assets
- `tests/support/viewer_browser_harness.py` — would need snapshot visibility for highlighted SVG IDs/classes if frontend highlight behavior is asserted

### Approaches
1. **Frontend-only visual polish** — keep backend payload unchanged and only soften CSS.
   - Pros: Smallest diff, lowest risk.
   - Cons: Cannot highlight the transition that led to the current state; cannot fix parent+child highlight correctly because the frontend is supposed to trust backend `active_ids`.
   - Effort: Low

2. **Thin backend contract extension plus frontend class split** — backend returns leaf-only `active_ids` and one optional `last_transition_id`; frontend applies separate classes for active state vs transition.
   - Pros: Solves all Slice B goals with narrow surface area; preserves existing SVG structure and runtime behavior; keeps highlight targeting backend-owned and exact-ID based.
   - Cons: Requires a small runtime/session contract change and targeted test updates.
   - Effort: Medium

### Recommendation
Use **Thin backend contract extension plus frontend class split**. Keep `active_path` as-is for observability, change `active_ids` to represent only the active leaf state, and add an optional `last_transition_id` field produced by the runtime bridge. On the frontend, replace the single aggressive `.is-active` rule with separate, lighter classes such as a subtle state highlight plus a distinct transition highlight. This is the smallest safe approach that meets all Slice B goals without touching SVG structure or broad runtime semantics.

### Risks
- Initial-entry semantics are underspecified: nested startup can involve more than one initial transition (`machine_init` then `parent_init`), so Slice B should define whether `last_transition_id` means the final transition into the leaf or any full entry chain.
- Existing tests assert exact snapshot payloads and do not currently inspect highlighted SVG classes, so contract/test updates are unavoidable.
- If transition highlighting is added by overloading `active_ids` instead of a dedicated field, state and transition styling will be hard to distinguish safely.

### Ready for Proposal
Yes — the change is narrow enough. The proposal should explicitly lock `active_ids` to leaf-only state highlighting and define `last_transition_id` as an optional exact SVG ID exposed with minimal backend changes.
