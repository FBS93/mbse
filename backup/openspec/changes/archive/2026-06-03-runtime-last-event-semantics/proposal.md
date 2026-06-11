# Proposal: Runtime Last-Event Semantics

## Intent

Make the runtime/viewer snapshot describe the last received event, not only the active leaf. Iteration 1 stays semantic-only so internal-transition handling is explicit without render targeting or styling.

## Scope

### In Scope
- Add snapshot fields for `event_id`, handled/unhandled, handler kind/id, `transition_path_ids` only when a transition occurs, and `executed_activities`.
- Represent internal handling explicitly: active state may stay the same while the handled internal transition and its executed activities are still reported.
- Update viewer bridge/client to consume semantic execution data.

### Out of Scope
- Per-activity SVG IDs, render-fragment targeting, or text-ID mapping.
- Viewer styling/highlight changes.
- Diagram-definition or render-preparation work beyond existing authored IDs used as semantic origins.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `generated-hsm-engine`: extend runtime snapshot semantics from latest state/path only to last-received-event execution reporting.
- `graphviz-svg-workbench`: extend the runtime bridge/viewer payload so the viewer consumes semantic execution data without implying a taken external arrow for internal handling.

## Approach

Keep layer boundaries strict. Runtime is the source of truth for last-event semantics. For each `send_event`, it records whether the event was handled, which handler matched (`internal` or `transition`), whether any transition path was taken, and ordered `executed_activities` with authored-ID origin metadata. The bridge serializes that result; the viewer only consumes it. Render mapping stays in iteration 2.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `src/mbse/domain/models.py` | Modified | Add last-event semantic DTOs to runtime/viewer snapshots. |
| `src/mbse/application/hsm_runtime.py` | Modified | Capture last-event outcome, handler identity, transition-path presence, and executed activities. |
| `src/mbse/application/web_runtime_bridge.py` | Modified | Serialize runtime semantic execution for the viewer. |
| `src/mbse/web/static/viewer.js` | Modified | Consume semantic execution fields without styling/render targeting. |
| `tests/unit/mbse/test_hsm_runtime.py` | Modified | Lock internal vs external semantics. |
| `tests/unit/mbse/test_web_runtime_bridge.py`, `tests/integration/test_mbse_workbench.py` | Modified | Lock payload shape end-to-end. |
| `openspec/specs/generated-hsm-engine/spec.md` | Modified | Make last-event execution reporting normative. |
| `openspec/specs/graphviz-svg-workbench/spec.md` | Modified | Make viewer-consumed semantic execution normative. |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Scope creeps into render targeting | Medium | Keep `executed_activities` metadata semantic-only. |
| Internal handling is misread as a taken edge | Medium | Require `transition_path_ids` only when a transition occurs. |
| Snapshot churn breaks consumers/tests | Medium | Update runtime, bridge, viewer, and tests in one slice. |

## Rollback Plan

Revert the snapshot, bridge, and viewer semantic additions together, restoring the current state-plus-`last_transition_id` contract.

## Dependencies

- Prior exploration conclusion: split highlighting into two iterations; do iteration 1 semantics only.

## Success Criteria

- [ ] Specs state that snapshots report the last received event outcome, not only the active state.
- [ ] Internal transitions are representable as handled events with unchanged active state and no implied external path.
- [ ] `executed_activities` includes stable origin metadata sufficient for later render/view mapping, without adding render-target IDs now.
