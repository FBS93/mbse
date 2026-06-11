# Proposal: HSM Executable Activities And Guards

## Intent

Bring MBSE runtime behavior closer to `example_hsm` by making lifecycle-slot activities, event-associated activities, and guards executable with the correct ordering semantics.

## Scope

### In Scope
- Execute reserved lifecycle slots: root/local initial behavior, `on_entry`, and `on_exit` in `example_hsm`-aligned order.
- Add event-handling transition candidates with optional guards and ordered event-associated activities.
- Resolve declarative callable references during runtime build/generation and verify parity with focused runtime tests.

### Out of Scope
- Timers, history, orthogonal regions, async/event queues, or embedded EDF transport mechanics.
- Arbitrary code-string execution or a registry that moves behavior outside the HSM model.
- Workbench/UI behavior beyond any metadata rendering needed to keep authored content inspectable.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `generated-hsm-engine`: replace inert behavior metadata with executable lifecycle slots, guarded event handling, and ordered event activities while preserving the public runtime API.

## Approach

Model behavior declaratively in the HSM document using callable references. Keep `on_entry` and `on_exit` as reserved lifecycle slots. Add ordered `activities` plus optional `guard` to normal event transitions, and ordered `activities` to initial transitions. Runtime dispatch must first search event candidates from active leaf outward; a failing guard is treated as unhandled and bubbling continues. After a transition is selected, execute: exits from current leaf up to the handling source, remaining exit path to the LCA, event-associated activities, entry path to the explicit target, then repeated local initial resolution. Initial behavior is a reserved execution slot triggered only after its owning compound state becomes active, not just another generic event activity.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/specs/generated-hsm-engine/spec.md` | Modified | Make executable semantics normative and remove inert-action exclusions |
| `src/mbse/domain/models.py`, `validation.py`, `hsm_schema_v1.json` | Modified | Add callable refs, guards, and initial/event activity fields |
| `src/mbse/application/build_hsm_runtime.py`, `prepare_hsm_engine.py`, `hsm_runtime.py` | Modified | Resolve callables and execute lifecycle/event behavior in order |
| `src/mbse/infrastructure/generated_engine.py`, `templates/hsm_v1_engine.py.j2` | Modified | Emit guarded candidate metadata instead of flat event→transition assumptions |
| `tests/unit/mbse/test_*.py` | Modified | Replace inertness assertions with executable-parity coverage |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Lifecycle vs event activity semantics drift from `example_hsm` | Med | Spec ordering from reference flow before implementation |
| Review size exceeds budget | High | Deliver as chained slices: model/schema, engine metadata, runtime execution, tests/docs |
| Callable resolution/import failures | Med | Fail deterministically at runtime-build time with targeted validation |

## Rollback Plan

Revert executable-behavior schema/runtime changes and restore inert activity metadata plus current transition selection semantics.

## Dependencies

- `openspec/changes/hsm-executable-activities-and-guards/exploration.md`
- `example_hsm/src/framework/src/edf_hsm.c`
- `example_hsm/test/hsm/src/hsm.c`

## Success Criteria

- [ ] Spec explicitly separates reserved lifecycle slots from normal event-associated activities.
- [ ] Runtime ordering matches `example_hsm`-visible behavior for guards, self transitions, ancestor/descendant paths, and nested initials.
- [ ] Delivery plan remains split into chained reviewable slices because 400-line budget risk stays high.
