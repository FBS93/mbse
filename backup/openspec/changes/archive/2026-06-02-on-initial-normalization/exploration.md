## Exploration: on-initial-normalization

### Current State
`on_initial` is already modeled as a state-owned hook in schema, parsing, validation, engine preparation, generated engine metadata, and runtime execution. The competing concept still present is `initial.activities` on both document-level and state-level initial transitions. Runtime executes both: `on_initial` first when a compound state becomes active, then the corresponding `initial.activities`, then child `on_entry`. Rendering also exposes the split: `on_initial:` is a state-body section while local `initial.activities` render separately as `initial_transition:` in the state body. There is also an existing render-spec contradiction: the active `svg-render-activity-parity` spec says initial-transition activities render on edges, but current code/tests assert they do **not** render on edges and instead appear in state-body text.

### Affected Areas
- `src/mbse/domain/hsm_schema_v1.json` — `initial` still allows `activities` at root and local state scope.
- `src/mbse/domain/models.py` — `HsmInitialTransition` still owns `activities`; prepared engine rows still carry `activity_plan_ids` for initials.
- `src/mbse/domain/validation.py` — parser and validator still accept/validate `initial.activities` and reject/inspect them as executable behavior.
- `src/mbse/application/prepare_hsm_engine.py` — builds callable plans for document/state initial-transition activities and stores them in `initial_rows_by_owner_id`.
- `src/mbse/infrastructure/generated_engine.py` — generated wrapper exposes initial rows with `activity_plan_ids` and resolves those handlers.
- `src/mbse/application/hsm_runtime.py` — executes root `initial.activities` during `init()` and local `initial.activities` during `_descend_initial_chain()`.
- `src/mbse/application/prepare_hsm_render.py` — still renders local `state.initial.activities` as `initial_transition:`.
- `tests/unit/mbse/test_hsm_validation.py` — asserts schema/model acceptance of `initial.activities`.
- `tests/unit/mbse/test_prepare_hsm_engine.py` and `tests/unit/mbse/test_generated_engine.py` — assert initial activity plan rows/ids exist.
- `tests/unit/mbse/test_hsm_runtime.py` and `tests/integration/test_generated_hsm_engine.py` — assert runtime traces that include distinct initial-transition activity execution.
- `tests/unit/mbse/test_hsm_render_view.py` and `tests/integration/test_hsm_json_workbench.py` — assert `initial_transition:` render output.
- `test_hsm/hsm.json` — example still authors both `on_initial` and `initial.activities`.
- `openspec/specs/generated-hsm-engine/spec.md` — currently codifies `on_initial` as state-owned but still permits distinct initial-transition activities.
- `openspec/changes/svg-render-activity-parity/specs/hsm-json-graphviz-rendering/spec.md` — still discusses initial-transition activity rendering and currently contradicts implementation/tests.

### Approaches
1. **Hard normalization now** — remove `initial.activities` everywhere and require authors to move that behavior into state `on_initial`.
   - Pros: Fully consistent mental model; no parallel lifecycle concept left.
   - Cons: Touches schema, validation, engine prep, generated engine, runtime, render, tests, demo JSON, and specs at once; breaks existing authored payloads.
   - Effort: Medium

2. **Render-only cleanup** — stop showing `initial_transition:` but leave runtime/schema support intact.
   - Pros: Small diff.
   - Cons: WRONG direction; leaves semantic contradiction in model/runtime and hides behavior instead of normalizing it.
   - Effort: Low

### Recommendation
Take **Hard normalization now**, but keep it tightly scoped to behavior-model consistency only:

1. Remove `activities` from `initial` in schema + parser/validator.
2. Remove initial-transition activity storage from domain/prepared/generated engine models.
3. Remove runtime execution of root/local initial-transition activities, keeping only transition IDs/targets.
4. Remove `initial_transition:` render sections.
5. Update tests, `test_hsm/hsm.json`, and the generated-engine/render specs so they no longer describe or assert a competing initial-transition activity concept.

Do **not** spend effort on new rendering features or highlighting. The minimum coherent set is domain contract + runtime pipeline + render output + tests/specs, because leaving any one of those behind creates contradictions.

### Risks
- Existing example payloads and tests rely on `initial.activities`; the change is intentionally breaking and must be updated atomically.
- The render spec in `svg-render-activity-parity` already disagrees with code; if not corrected in the same slice, downstream SDD artifacts stay misleading.
- Root-level initial behavior currently has no state owner; normalizing strictly to state-owned `on_initial` implies root `initial.activities` must be removed, not migrated 1:1.

### Ready for Proposal
Yes — this fits one reviewable PR if kept to schema/model/runtime/render/test/spec consistency only, with no extra viewer/highlighting work. Forecast: ~250-380 changed lines, low-to-medium risk, no chaining needed.
