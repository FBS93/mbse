## Exploration: runtime-hsm-core-parity

### Current State
MBSE currently implements a reduced hierarchical runtime. `HsmRuntime.init()` follows root/local initials to a leaf, and `send_event()` bubbles from the active leaf to ancestors until a generated state handler returns `("transition", target_id)` or the event is dropped. After a transition, `_resolve_active_path()` rebuilds the target ancestry and re-applies nested initials, but it does **not** compute transition source/target paths, lowest common ancestor trimming, or distinct self/ancestor/branch transition cases like the C runtime does. The generated engine only exposes event-to-target mappings; it does not expose enough structure to mirror `start`, `dispatch`, `getTransitionPath`, and `executeTransition` semantics directly. Python/host-PC should keep the C runtime's observable HSM behavior, but should **not** copy embedded concerns such as AO/pub-sub, reserved event objects, fixed-depth arrays, or static buffers.

### Affected Areas
- `src/mbse/application/hsm_runtime.py` — current `init`/`send_event` logic is where semantic parity must land.
- `src/mbse/application/prepare_hsm_engine.py` — prepared engine view likely needs richer transition metadata than `(event_id, target_id)`.
- `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` — generated handlers probably need to expose parent escalation and/or transition descriptors instead of only flat target returns.
- `src/mbse/infrastructure/generated_engine.py` — runtime-facing generated engine contract will need new metadata/helpers.
- `src/mbse/domain/models.py` — prepared engine structures likely need path/transition metadata fields.
- `tests/unit/mbse/test_hsm_runtime.py` — current tests cover reduced semantics only; parity cases must be added.
- `example_hsm/src/framework/src/edf_hsm.c` — semantic reference for `start`, hierarchical dispatch, LCA/path computation, and recursive initial entry.
- `example_hsm/test/hsm/src/test_hsm.c` and `example_hsm/test/hsm/src/hsm.c` — reference transition matrix for self, ancestor→descendant, descendant→ancestor, and cross-branch cases.

### Approaches
1. **Runtime-path port over enriched Python metadata** — keep the handwritten Python runtime, but enrich generated/prepared metadata so runtime helpers can compute exit path, entry path, LCA trimming, and nested initials using Python lists/tuples.
   - Pros: Best semantic match to the C core; clean Python adaptation; avoids porting AO/pub-sub/embedded limits; keeps public runtime API stable.
   - Cons: Requires widening the generated engine contract and rewriting current transition resolution.
   - Effort: Medium

2. **Reserved-signal style engine emulation** — make generated Python state handlers emulate `RET_SUPER` / `RET_TRANSITION` / internal signals so `hsm_runtime.py` looks structurally close to `edf_hsm.c`.
   - Pros: Closest code-shape parity with the C example; easier line-by-line comparison against the reference algorithm.
   - Cons: Imports embedded implementation style into Python, adds indirection, and risks copying non-semantic C patterns that the user explicitly does not want.
   - Effort: High

### Recommendation
Use **Runtime-path port over enriched Python metadata**. Port the C algorithm at the semantic level, not the mechanism level: add helpers that (1) identify the transition source that handled the event, (2) compute exit and entry segments between source and target using ancestry/LCA logic, and (3) execute nested initial descent after the target is entered. In Python, model paths with dynamic tuples/lists and pure helper methods instead of fixed arrays and reserved internal events. Keep `on_entry`/`on_exit` payloads inert for now because current MBSE spec explicitly excludes action execution; however, the runtime should still compute the same entry/exit traversal order so future action hooks can attach without redesign.

Implementation-oriented port plan:
- Extend prepared/generated engine metadata to expose complete ancestry/transition facts needed for path computation.
- Refactor `init()` into explicit `start`-like logic that builds the top-most entry path and then repeatedly follows nested initials.
- Refactor `send_event()` to separate: hierarchical handler lookup, transition source capture, transition-path computation, transition execution, and final active-leaf update.
- Add internal helpers mirroring the C concepts: `find_transition_source`, `get_transition_path`, `execute_transition`, and `resolve_initial_chain`.
- Keep public API unchanged unless proposal work proves a new inspection hook is necessary.
- Build tests from the C reference cases, but assert Python-visible outcomes only (active path, state, last transition id, inert actions).

### Risks
- Current runtime spec is intentionally minimal, so proposal/spec work must define which C semantics become normative and which remain excluded.
- Generated engine changes may ripple into runtime construction and snapshot assumptions.
- If entry/exit traversal is implemented without action execution, tests must be careful to verify semantics through state/path outcomes, not nonexistent callbacks.
- The C tests validate final active state more than full traversal order, so MBSE may need stronger Python tests than the reference provides.

### Ready for Proposal
Yes — ready for proposal. The proposal should lock the semantic scope to: C-style start/dispatch/LCA/transition-path/initial-chain behavior, preserved Python public API, no AO/pub-sub/scheduler port, no fixed-depth/static-memory limits, and no execution of authored entry/exit strings in this slice.
