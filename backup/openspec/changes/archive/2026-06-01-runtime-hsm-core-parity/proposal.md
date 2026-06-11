# Proposal: Runtime HSM Core Parity

## Intent

Bring MBSE's Python runtime up to the C example's core HSM execution semantics so hierarchical machines behave the same at runtime, while deliberately adapting away embedded-only mechanics.

## Scope

### In Scope
- Port semantic parity for `start`/`init`, hierarchical dispatch, transition path computation, LCA trimming, and nested initial descent.
- Enrich prepared/generated engine metadata so the handwritten runtime can compute source/target ancestry and execute the correct exit/entry order.
- Add parity-focused tests for self, ancestor/descendant, cross-branch, and unhandled-event cases.

### Out of Scope
- AO/pub-sub, scheduler/event queue, reserved event objects, static-memory/fixed-depth buffers, or other embedded transport/mechanics.
- Guards, action execution, timers, history, orthogonal regions, or workbench/UI changes.
- Changing the public Python runtime API unless proposal follow-up proves a missing inspection hook.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `generated-hsm-engine`: strengthen runtime requirements from minimal hierarchical behavior to C-parity core execution semantics, while keeping Python-specific implementation freedom and existing v1 exclusions.

## Approach

Keep the handwritten Python runtime as the execution boundary, but port the C algorithm at the semantic level only. Refactor runtime flow into explicit phases: find the transition source that handled the event, compute exit/entry segments via ancestry + LCA logic, execute the transition path, then follow nested initials until the final active leaf is reached. Use Python lists/tuples and richer generated metadata instead of fixed arrays, reserved signals, or static buffers.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/specs/generated-hsm-engine/spec.md` | Modified | Make parity semantics normative and keep non-runtime concerns excluded |
| `src/mbse/application/hsm_runtime.py` | Modified | Replace reduced transition resolution with explicit parity helpers |
| `src/mbse/application/prepare_hsm_engine.py` | Modified | Prepare ancestry/transition metadata needed by runtime path logic |
| `src/mbse/infrastructure/templates/hsm_v1_engine.py.j2` | Modified | Emit runtime-facing transition/parent facts instead of flat mappings |
| `src/mbse/domain/models.py` + tests | Modified | Extend prepared-engine structures and add parity coverage |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Semantic drift from C reference in edge transitions | Med | Spec exact cases from C tests before implementation |
| Generated metadata change ripples into runtime assumptions | Med | Keep public API stable and confine change to internal contracts |
| Embedded details leak into Python design | Med | Enforce semantic parity, mechanical adaptation boundary in spec/design |

## Rollback Plan

Revert the runtime-path parity changes and restore the prior minimal transition resolution while keeping the current public API and unrelated runtime/workbench behavior unchanged.

## Dependencies

- `example_hsm/src/framework/src/edf_hsm.c` and reference tests as the semantic oracle.

## Success Criteria

- [ ] `generated-hsm-engine` spec explicitly defines parity for start/init, dispatch escalation, LCA-based transition paths, and nested initials.
- [ ] Python runtime preserves current public API while matching C-visible state outcomes for self, ancestor, descendant, and cross-branch transitions.
- [ ] AO/pub-sub, scheduler, and static-memory concerns remain explicitly excluded from this slice.
