## Exploration: hsm-executable-activities-and-guards

### Current State
The current MBSE runtime only resolves structural HSM behavior: root/local initial descent, hierarchical event bubbling, LCA-based path calculation, and final active leaf tracking. `src/mbse/application/hsm_runtime.py` never executes `on_entry`/`on_exit`, never evaluates guards, and never runs transition behavior. The generated engine (`src/mbse/infrastructure/templates/hsm_v1_engine.py.j2`) emits only `if event_id == ...: return ("transition", target)` handlers, so runtime semantics are limited to target selection.

`example_hsm` is stricter. In `example_hsm/src/framework/src/edf_hsm.c`, dispatch first bubbles from leaf to ancestors until a handler returns `RET_TRANSITION`; that handling state becomes the transition source. The framework then executes: (1) exit from current leaf up to the handling source, (2) exit path from source up to but excluding the LCA, (3) entry path from LCA down to the explicit target, and then (4) repeated local initial transitions, each entered only after its owning compound state is active. `EDF_hsm_executeTransition()` also shows the exact initial flow shape: nested initial behavior is triggered by dispatching `EDF_HSM_INIT_SIGNAL` to the newly active compound state, not by treating initials as normal event transitions.

That means the missing MBSE pieces are executable behavior metadata in the model plus runtime support for four behavior points: state entry, state exit, explicit transition activities, and initial-transition activities/guards semantics. Guard-false behavior should match `example_hsm`'s `RET_UNHANDLED` path: the candidate transition is ignored and dispatch keeps bubbling.

### Affected Areas
- `src/mbse/domain/models.py` — needs executable behavior fields on transitions and initial transitions, plus callable-reference model types.
- `src/mbse/domain/validation.py` — must accept/validate declarative callable references, guard fields, and initial-transition activities.
- `src/mbse/domain/hsm_schema_v1.json` — schema must evolve from inert string snippets to explicit executable reference fields.
- `src/mbse/application/prepare_hsm_engine.py` — must prepare ordered behavior metadata, not just target maps.
- `src/mbse/infrastructure/generated_engine.py` — needs richer generated wrapper data and callable resolution support.
- `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` — generated handlers must evaluate ordered transition candidates with guards.
- `src/mbse/application/hsm_runtime.py` — must execute exit/transition/entry/initial behavior in reference order using live `ctx`.
- `src/mbse/application/build_hsm_runtime.py` — likely needs an optional callable resolver/registry input.
- `tests/unit/mbse/test_hsm_runtime.py` — current assertions explicitly prove activities are inert; those tests must be replaced/expanded.
- `tests/unit/mbse/test_generated_engine.py` and `tests/unit/mbse/test_prepare_hsm_engine.py` — generated shape/index expectations will change.
- `tests/unit/mbse/test_hsm_validation.py` — schema/validation coverage must add callable refs, guards, and rejection cases.
- `example_hsm/src/framework/src/edf_hsm.c` — reference for exact dispatch/initial semantics.
- `example_hsm/test/hsm/src/hsm.c` and `example_hsm/test/hsm/doc/test_hsm.md` — reference topology and parity expectations, including self-transition and parent-init reentry cases.

### Approaches
1. **Declarative callable refs in the HSM model** — add explicit executable metadata to states/transitions/initial transitions and resolve Python callables at runtime build.
   - Pros: Matches user constraints; keeps JSON declarative; supports exact runtime ordering; preserves generated-engine architecture; easy to parity-test against `example_hsm`.
   - Cons: Broad schema/model/test churn; needs careful import-path validation and resolution errors; generated engine must stop assuming one event→one transition map.
   - Effort: High

2. **External behavior registry layered over current JSON** — keep JSON mostly structural and attach activities/guards from a separate Python registry keyed by transition/state IDs.
   - Pros: Smaller schema delta; avoids storing Python import paths in JSON.
   - Cons: Violates the request that the HSM model store declarative references; splits source of truth; makes exported models less portable; harder to inspect/render.
   - Effort: Medium

3. **Inline Python snippets in JSON** — execute authored strings for entry/exit/guard/effects.
   - Pros: Fastest to prototype.
   - Cons: Explicitly forbidden by the user; poor safety/debuggability; diverges from current architecture and from future maintainability.
   - Effort: Low

### Recommendation
Use **Approach 1**.

Recommended model shape:

- Keep state-level `on_entry` and `on_exit`, but redefine them as ordered **activity callable references**, not inline code snippets.
- Extend `HsmTransition` with:
  - `guard`: optional callable reference
  - `activities`: ordered callable references
- Extend `HsmInitialTransition` with:
  - `activities`: ordered callable references
- Do **not** add a separate state-level `on_initial` field. The user’s clarification maps better to **initial transition activities** because `example_hsm` models initial flow as an INIT-triggered transition owned by the compound state. The behavior should run only when that initial transition is actually taken.

Recommended execution semantics to match `example_hsm` as closely as MBSE allows:

- **Dispatch**: offer the event from active leaf outward. For each state, evaluate authored transition candidates in order.
- **Guard**: if event matches and guard returns `False`, treat that candidate as unhandled and continue searching. If no candidate in that state passes, bubble to the parent. Guards receive only the live `ctx` and return `bool`.
- **Transition source**: the state whose handler/candidate actually passes its guard becomes the source.
- **Exit order**: exit current active leaf upward until the handling source is reached, then execute the computed exit path from source upward excluding the LCA. Exit activities run inner→outer.
- **Explicit transition activities**: run after all exits and before any entries.
- **Entry order**: enter from LCA child downward to the explicit target. Entry activities run outer→inner.
- **Initial transition activities**: after a compound state becomes active, if its initial transition fires, run that initial transition’s activities before entering the target subpath of that initial. This is the closest Python-host equivalent to `EDF_HSM_INIT_SIGNAL`-driven flow.
- **Nested initials**: repeat until the active leaf has no local initial.
- **Self transition**: exit the source state, run explicit transition activities, and re-enter the same state.
- **Ancestor target**: do not re-enter the target ancestor.
- **Descendant target**: do not exit the ancestor source; only enter the path below it.

Implementation note: resolve callable references once during `build_hsm_runtime()` (or generated-engine load) and keep the resolved callables in engine/runtime metadata. Pass the same mutable `HsmRuntimeContext` instance to every guard/activity so mutations are live. Snapshot serialization may still copy variables for inspection, but behavior execution must never receive a copied context.

Callable reference tradeoff:

- Prefer a structured JSON object (for example `{ "module": "pkg.hsm_callbacks", "name": "enter_open" }`) over free-form strings.
- Why: easier schema validation, clearer error messages, and less ambiguous than parsing `module:function` strings.
- If minimal authoring friction matters more than schema strictness, a single import-path string is acceptable, but then runtime validation must be excellent.

### Risks
- Current tests and base spec explicitly enforce inert `on_entry`/`on_exit`; this change deliberately reverses that contract and will ripple through unit/integration expectations.
- `GeneratedEngine.event_transition_ids_by_state_id` currently assumes one event key per state; guarded alternatives on the same event will require a list-based structure or removal of that map.
- Import-time callable resolution can fail due to missing modules, renamed functions, circular imports, or non-callable targets; errors must be deterministic and surfaced at runtime-build time.
- Guard side effects are dangerous. If guards mutate `ctx`, parity/debuggability drop fast. Validation/docs should strongly state guards are predicates and SHOULD be side-effect free even if Python cannot enforce it.
- Matching `example_hsm` “exactly” is limited by architecture: MBSE has no reserved event objects or state-handler functions, so parity should be defined in terms of observable ordering and final runtime state, not EDF internals.
- Review budget risk is **High**. This touches schema, domain models, engine generation, runtime semantics, and many tests. Expect well over the 400-line review budget unless delivered as chained slices.

### Ready for Proposal
Yes — with a proposal that scopes delivery into chained slices. Suggested forecast for later phases: **Decision needed before apply: Yes**; **Chained PRs recommended: Yes**; **400-line budget risk: High**.
