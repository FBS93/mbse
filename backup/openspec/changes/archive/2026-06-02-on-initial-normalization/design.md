# Design: Normalize `on_initial`

## Technical Approach

Remove `initial.activities` as a supported concept across the full HSM pipeline and keep initials structural-only. Executable initial behavior remains only on the owning state's optional `on_initial`, matching the existing `on_entry` / `on_exit` pattern. This follows the proposal's one-slice cleanup and implements the delta specs for `generated-hsm-engine` and `hsm-json-graphviz-rendering` without expanding runtime or viewer scope.

## Architecture Decisions

| Decision | Options | Choice | Rationale |
|---|---|---|---|
| Initial model shape | Keep `HsmInitialTransition.activities` but ignore it; remove it entirely | Remove it entirely | Ignoring preserves a dead contract. Removing it makes schema, parser, validation, and docs agree. |
| Prepared engine metadata | Keep `initial_rows_by_owner_id` with empty activity plans; reduce initials to target/id maps | Reduce to `initial_target_ids` + `initial_transition_ids` only | `HsmPreparedEngineInitialRow` becomes redundant once initials stop carrying executable plans. |
| Runtime init flow | Keep two-step execution (`on_initial` + initial activities); run only state-owned hooks | Run only `on_entry` and state-owned `on_initial` during descent | Matches the spec: initials route, states own behavior. |
| Render contract | Keep `initial_transition:` body text as legacy display; remove it | Remove it | Render must stop expressing a competing executable concept. Initial edges stay routing-only. |

## Data Flow

Author JSON
  └─ initial { id, target_id }
        + state.on_initial[]
            ↓
Schema / parser / validator
  └─ HsmInitialTransition(id, target_id)
            ↓
prepare_hsm_engine_view()
  └─ initial_target_ids + initial_transition_ids
            ↓
GeneratedEngine / HsmRuntime
  └─ route through initials, run only state lifecycle plans
            ↓
prepare_hsm_render_view()
  └─ render on_initial/on_entry/on_exit sections only

## File Changes

| File | Action | Description |
|---|---|---|
| `src/mbse/domain/hsm_schema_v1.json` | Modify | Remove `activities` from the `initial` definition. |
| `src/mbse/domain/models.py` | Modify | Remove `HsmInitialTransition.activities`; delete `HsmPreparedEngineInitialRow` and `HsmPreparedEngineView.initial_rows_by_owner_id`. |
| `src/mbse/domain/validation.py` | Modify | Parse initials as `{id,target_id}` only; stop validating initial callable refs; keep additional-property rejection authoritative. |
| `src/mbse/application/prepare_hsm_engine.py` | Modify | Drop initial activity plan registration and stop building initial rows. |
| `src/mbse/infrastructure/generated_engine.py` | Modify | Remove initial-row metadata from wrapper, literal formatting, handler collection, and engine loading. |
| `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` | Modify | Stop emitting `HsmPreparedEngineInitialRow` imports/constants. |
| `src/mbse/application/hsm_runtime.py` | Modify | Remove execution of root/local initial activity plans in `init()` and `_descend_initial_chain()`. |
| `src/mbse/application/prepare_hsm_render.py` | Modify | Remove `initial_transition:` state-body sections; keep initial-edge labels empty. |
| `tests/unit/mbse/test_hsm_validation.py` | Modify | Reject authored `initial.activities`; update model equality expectations. |
| `tests/unit/mbse/test_prepare_hsm_engine.py` / `test_generated_engine.py` | Modify | Remove assertions for initial activity plans/rows; keep target/id metadata assertions. |
| `tests/unit/mbse/test_hsm_runtime.py` | Modify | Update trace order to exclude root/local initial-activity steps while preserving `on_initial` order. |
| `tests/unit/mbse/test_hsm_render_view.py` / `tests/integration/test_hsm_json_workbench.py` | Modify | Assert absence of `initial_transition:` text and no initial activity text anywhere. |
| `test_hsm/hsm.json` | Modify | Remove root/local `initial.activities` examples. |

## Interfaces / Contracts

```python
@dataclass(frozen=True)
class HsmInitialTransition:
  id: str
  target_id: str
```

Prepared/generated engine initials remain metadata-only:
- `initial_target_ids: dict[str | None, str]`
- `initial_transition_ids: dict[str | None, str]`

No replacement initial-activity field is introduced anywhere.

## Testing Strategy

| Layer | What to Test | Approach |
|---|---|---|
| Unit | Schema/parser/model cleanup | RED/GREEN tests for rejecting `initial.activities` and simplified model equality. |
| Unit | Engine/runtime cleanup | Verify no initial activity plans/rows exist and init traces include only entry + `on_initial` behavior. |
| Unit/Integration | Render cleanup | Verify DOT/SVG include `on_initial:` when authored, exclude `initial_transition:` and initial activity text. |

## Migration / Rollout

No runtime migration. This is a breaking authored-contract cleanup: any payload using root or local `initial.activities` must remove that field. Root-level behavior has no state-owned equivalent, so it is deleted rather than auto-migrated.

## Open Questions

- [ ] None.
