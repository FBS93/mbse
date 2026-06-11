## Exploration: svg-render-activity-parity

### Current State
The executable HSM model now carries richer behavior than the SVG renderer shows. `prepare_hsm_render.py` currently renders state body content only from `on_entry` and `on_exit`, and transition labels only from the event signature. It does not render `on_initial`, internal transitions, transition activities, guards, or initial-transition activities. The DOT template already supports multi-line state bodies and edge labels, so the parity gap is primarily in render-view preparation and the render-view model shape, not in the Graphviz pipeline itself.

### Affected Areas
- `src/mbse/application/prepare_hsm_render.py` — current render shaping omits executable behavior fields and will need state-scoped/internal/edge label formatting.
- `src/mbse/domain/models.py` — current render DTOs only expose `body_lines` and a flat edge `label`, which is enough for today but brittle for parity expansion.
- `src/mbse/infrastructure/templates/hsm_v1.dot.j2` — state body and edge label template will need minor updates to render the added sections cleanly.
- `tests/unit/mbse/test_hsm_render_view.py` — should expand coverage for lifecycle hooks, internal transitions, guards, and transition/initial activities.
- `tests/integration/test_hsm_json_workbench.py` — should prove prepared DOT/SVG output still preserves public IDs while showing the new authored behavior text.
- `openspec/specs/hsm-json-graphviz-rendering/spec.md` — currently documents `on_entry`/`on_exit` rendering but not the newly executable behavior now present in the model.

### Approaches
1. **String-format parity on top of current DTOs** — Extend the existing render prep to append more body lines and richer edge label strings.
   - Pros: Smallest change; low template churn; likely fastest path.
   - Cons: Bakes more semantics into ad-hoc strings; later activity highlighting will likely require a second refactor.
   - Effort: Medium

2. **Small structured render DTO expansion** — Keep the same public SVG contract, but replace flat body/label shaping with lightweight structured sections/parts before rendering them to DOT.
   - Pros: Reaches parity now and leaves a cleaner seam for the next highlighting iteration without exposing new public IDs yet.
   - Cons: Slightly larger refactor across models, prep, template, and tests.
   - Effort: Medium

### Recommendation
Use **Approach 2** with a STRICT scope boundary.

Render in this parity slice:
- state body sections for `on_initial`, `on_entry`, and `on_exit`
- an `internal_transitions:` section in each owning state's body, with lines like `ping_evt / do_health_check`
- normal transition labels as `event/activity`
- guard text on normal transitions
- initial-transition activities on initial edges

Keep out of this slice:
- runtime/viewer highlighting changes
- new public SVG IDs for per-activity rows
- bridge/API changes for activity-level active state

The one worthwhile groundwork step now is INTERNAL ONLY: shape render data as sections/parts instead of one flat body-line tuple plus one flat edge-label string. That keeps this slice render-only while avoiding a guaranteed rewrite when activity highlighting is explored next.

### Risks
- **Graphviz label density**: adding lifecycle/internal text can make compound-state labels visually cramped; formatting rules should stay compact and deterministic.
- **Initial-edge labeling**: current initial-edge DTO has no label field, so adding initial-transition activities touches models, prep, template, and prepared-output tests.
- **Guard notation choice**: the current specs do not define guard render syntax yet, so the proposal/spec phase must lock one explicit textual format before implementation.
- **Scope creep into highlighting**: adding per-line SVG IDs now would expand the public render contract and likely push the change past the intended scope.
- **Review budget**: pure parity looks like a medium slice; if highlighting scaffolding leaks into public contracts, the change can exceed the 400-line review budget quickly.

### Ready for Proposal
Yes — with a proposal that explicitly limits this change to render parity only, reserves activity highlighting for the next change, and forecasts a **Medium** implementation at roughly **220-320 changed lines** across render prep/models/template/tests. Risk stays **Medium** if the team defers public highlight scaffolding; it becomes **High** if the change also tries to solve per-activity SVG targeting now.
