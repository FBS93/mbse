## Exploration: transition-path-highlight-cleanup

### Current State
`HsmRuntime` stores `last_transition_id` as a single optional string and overwrites it during nested-initial descent, so snapshots expose only the final transition that reached the active leaf. `WorkbenchRuntimeBridge` forwards that single ID only if it is present in `highlightable_ids`. `viewer.js` treats the field as one exact SVG ID and applies one transition class, while `viewer.css` still intensifies active states with both border and fill. Tests across runtime, bridge, generated-engine parity, and workbench integration all assert the scalar contract.

### Affected Areas
- `src/mbse/application/hsm_runtime.py` — runtime currently collapses each resolution chain to one remembered transition ID.
- `src/mbse/domain/models.py` — snapshot dataclasses type `last_transition_id` as `str | None` in both runtime and viewer models.
- `src/mbse/application/web_runtime_bridge.py` — bridge filters one transition ID instead of a sequence.
- `src/mbse/web/static/viewer.js` — viewer applies transition highlighting for one ID only.
- `src/mbse/web/static/viewer.css` — active-state highlight still increases fill intensity.
- `tests/unit/mbse/test_hsm_runtime.py` — unit expectations assume only the final transition ID survives.
- `tests/unit/mbse/test_web_runtime_bridge.py` — bridge tests assume one optional filtered ID.
- `tests/integration/test_generated_hsm_engine.py` — deterministic replay snapshots store one optional ID.
- `tests/integration/test_mbse_workbench.py` — API payloads and viewer harness assertions assume one transition highlight ID and the current CSS contract.

### Approaches
1. **In-place tuple migration** — change `last_transition_id` to `tuple[str, ...]` everywhere and treat it as the ordered set of transition IDs executed during the most recent init/event resolution.
   - Pros: matches the requested no-compatibility direction; keeps the field name stable; viewer can already consume JSON arrays with a tiny loop change; runtime semantics become explicit for nested initials.
   - Cons: requires broad test churn because every scalar assertion becomes a tuple/JSON-array assertion; spec wording that says “final transition” will need follow-up updates in later SDD phases.
   - Effort: Medium

2. **Hybrid scalar-plus-derived handling behind the same name** — keep internal runtime logic building a tuple but collapse back to one value at some boundary.
   - Pros: slightly smaller blast radius in the viewer and some integration tests.
   - Cons: violates the user constraint and preserves the ambiguity we are trying to remove; creates a fake migration layer with no long-term value.
   - Effort: Low

### Recommendation
Use **In-place tuple migration**. In runtime, replace the scalar memory with an ordered tuple builder: `init()` should produce the root initial plus every nested initial (`("machine_init", "idle_init")` style), `_execute_transition()` should return the explicit event transition plus any nested initials under the target, ancestor/self transitions without nested initials should yield a one-item tuple, and `set_state()` / uninitialized bridge fallbacks should use `()`. Then update the bridge to filter the tuple element-by-element against `highlightable_ids`, update `viewer.js` to apply the transition class to every returned ID, and simplify `viewer.css` so `.is-active-state` changes only contour stroke styling without fill intensification. This keeps the change as one simple combined iteration and preserves end-to-end exact-ID ownership in the backend.

### Risks
- Main-spec wording and archived design docs currently define `last_transition_id` as the final transition only; proposal/spec work must realign that contract before implementation is treated as compliant.
- Workbench integration fixtures and harness expectations will need systematic tuple/JSON-array updates, especially cases that currently use `None` and browser assertions that currently expect one highlighted transition.
- If any rendered SVG omits one transition in the executed chain, bridge filtering will drop only that member; tests should lock in that partial filtering behavior deliberately.

### Ready for Proposal
Yes — the implementation path is clear. The next phase should state that `last_transition_id` now means “ordered tuple of executed transition IDs from the latest resolution, including nested initials,” and that active-state styling becomes border-only while transition highlighting may apply to multiple exact SVG edges.
