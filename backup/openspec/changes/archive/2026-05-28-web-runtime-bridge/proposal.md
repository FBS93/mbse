# Proposal: Web Runtime Bridge

## Intent

Add a SMALL runtime-backed web slice to the existing SVG workbench so a user can reset/init, inject events, set HSM variables, and always see the latest backend-owned snapshot and SVG highlight state. This is a software bridge only, NOT a visual redesign.

## Scope

### In Scope
- Add one minimal backend runtime session for each workbench session, built from the canonical HSM JSON already used for rendering.
- Expose only four web operations: read current snapshot, reset/init, send one event by `event_id`, and set one variable by `variable_id` with raw JSON value.
- Return backend-derived `active_ids` on every snapshot/mutation and preserve exact SVG ID equality as the highlight contract.

### Out of Scope
- Visual redesign, richer controls, animation, or UX polish beyond wiring the minimal controls.
- Event parameters, event queues, timers, history, guards, async runtime behavior, or multi-session/multi-user support.
- Any heuristic SVG targeting, label-based lookup, or weakening of the exact-ID contract.

## Capabilities

### New Capabilities
- None.

### Modified Capabilities
- `graphviz-svg-workbench`: extend the workbench from read-only highlight to minimal backend-owned runtime synchronization while preserving exact SVG ID semantics and keeping the UI layer intentionally thin.

## Approach

Keep the current Python server + static viewer architecture. Persist the canonical HSM JSON alongside existing session artifacts, build one runtime from that source, initialize it on session load, and expose a minimal JSON snapshot contract. The frontend stays dumb: every mutation round-trips to the backend and re-renders from the returned snapshot. Backend highlight state MUST come from `runtime.get_snapshot().active_path`, mapped directly to exact SVG IDs.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `openspec/specs/graphviz-svg-workbench/spec.md` | Modified | Add runtime-backed web slice requirements and preserve exact-ID rules |
| `src/mbse/application/build_session.py` | Modified | Retain runtime-capable source in the session bundle |
| `src/mbse/infrastructure/session_store.py` | Modified | Persist canonical HSM JSON or equivalent runtime source artifact |
| `src/mbse/web/server.py` | Modified | Host minimal runtime snapshot/mutation endpoints |
| `src/mbse/web/static/viewer.js` | Modified | Refresh snapshot/highlight from backend responses |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Expanding `workbench-session.json` causes avoidable contract churn | Med | Prefer a separate runtime payload if needed |
| Runtime/web state desynchronizes | Low | Make backend the single source of truth; return full snapshot on every mutation |
| Scope creeps into richer runtime semantics | Med | Exclude event params and UI improvements in spec |

## Rollback Plan

Remove the runtime bridge endpoints and viewer wiring, stop persisting runtime source artifacts, and fall back to the current read-only SVG workbench.

## Dependencies

- Existing `generated-hsm-engine` runtime API and current HSM JSON + SVG render pipeline.

## Success Criteria

- [ ] A user can open the existing web workbench and always read the latest backend snapshot without manual SVG-only sync.
- [ ] Reset/init, event injection, and variable mutation each return an updated snapshot plus exact `active_ids` for SVG highlight.
- [ ] The slice ships without visual redesign and without adding event parameters or richer runtime semantics.
