# Proposal: Normalize `on_initial`

## Intent

Make `on_initial` the only initial-behavior concept so it matches `on_entry` and `on_exit`: optional, state-owned lifecycle hooks with no competing `initial.activities` path.

## Scope

### In Scope
- Remove root/state `initial.activities` from schema, models, parser, and validation.
- Remove initial-transition activity storage/execution from engine prep, generated engine metadata, runtime, and render preparation.
- Update tests, example HSM JSON, and specs to describe only state-owned `on_initial` behavior.

### Out of Scope
- New rendering features, highlighting, or workbench/viewer changes.
- Unrelated runtime semantics beyond deleting the competing initial-transition activity concept.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `generated-hsm-engine`: remove distinct initial-transition activity semantics and codify `on_initial` as the sole initial lifecycle hook.
- `hsm-json-graphviz-rendering`: remove `initial.activities` from the JSON/render contract and stop rendering `initial_transition:` activity text.

## Approach

Apply one bounded cleanup slice across the full pipeline: schema/model contract first, then prepared/generated runtime data, then runtime/render consumers, then tests/specs. Root and local initials keep only `id` and `target_id`; executable behavior lives only on the activated state's optional `on_initial` hook.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/mbse/domain/*` | Modified | Remove `initial.activities` from schema, models, and validation. |
| `src/mbse/application/*` | Modified | Drop initial activity planning/execution and render-body `initial_transition:` output. |
| `src/mbse/infrastructure/generated_engine.py` | Modified | Stop exposing initial activity plan metadata. |
| `tests/**` | Modified | Replace split-behavior assertions with `on_initial`-only expectations. |
| `test_hsm/hsm.json` | Modified | Remove authored `initial.activities` examples. |
| `openspec/specs/**` | Modified | Align runtime/render specs with normalized semantics. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Breaking authored payloads/tests using `initial.activities` | Medium | Update schema, examples, runtime, and tests atomically in one slice. |
| Spec drift across runtime vs render artifacts | Medium | Update both affected capabilities in the same change. |

## Rollback Plan

Revert the slice restoring `initial.activities` schema/model/runtime/render/test/spec support together; do not partially roll back only one layer.

## Dependencies

- `openspec/changes/on-initial-normalization/exploration.md`

## Success Criteria

- [ ] No accepted schema/model path still allows `initial.activities`.
- [ ] Runtime/render/tests/specs consistently treat `on_initial` as the only executable initial hook.
- [ ] Change remains one reviewable cleanup slice with no viewer/highlighting expansion.
