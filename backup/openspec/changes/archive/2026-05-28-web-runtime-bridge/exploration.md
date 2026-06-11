## Exploration: web-runtime-bridge

### Current State
The repo already has the two halves needed for this slice, but they are still disconnected. `build_workbench_session()` can start from raw HSM JSON and produce `prepared-document.json`, `diagram.svg`, and the minimal `workbench-session.json` used by the current read-only web viewer. Separately, `build_hsm_runtime()` can build an executable runtime from the same HSM JSON and expose `init`, `send_event`, `set_variable`, and `get_snapshot()`.

The important constraint is architectural: the current web contract is artifact-first and intentionally tiny, while the runtime currently lives only in memory and cannot be reconstructed from `prepared-document.json` alone. That means the bridge cannot be bolted onto the existing highlight endpoint only; the backend must own one runtime-backed session source of truth and publish snapshot data that the viewer can consume.

### Affected Areas
- `src/mbse/application/build_session.py` — today it accepts raw HSM JSON but only persists prepared render artifacts; the bridge needs a way to retain runtime-capable source/session metadata.
- `src/mbse/infrastructure/session_store.py` — current artifact writer only stores `prepared-document.json`, `diagram.svg`, and `workbench-session.json`.
- `src/mbse/web/server.py` — current server is stateless except for highlight requests; this is the natural place to host one in-memory runtime session and new JSON endpoints.
- `src/mbse/web/static/viewer.js` — current client only loads the SVG once and submits manual highlight requests; it would need to fetch runtime snapshots and reapply backend-driven highlights.
- `src/mbse/application/hsm_runtime.py` — already provides the exact minimal operations needed for reset, event injection, variable mutation, and snapshot reads.
- `src/mbse/domain/models.py` — current `WorkbenchSession` shape is too small if the frontend must also know runtime-facing variable/event IDs or a richer snapshot contract.
- `openspec/specs/graphviz-svg-workbench/spec.md` — current slice explicitly excludes runtime synchronization, so this new change must define the contract expansion cleanly instead of smuggling it in.
- `openspec/specs/generated-hsm-engine/spec.md` — defines the stable runtime API that the bridge should compose rather than bypass.

### Approaches
1. **Session-backed runtime bridge with snapshot API** — keep the existing stdlib server/viewer pattern, add one backend-owned runtime per workbench session, and expose a minimal runtime JSON contract for reset, event dispatch, variable mutation, and current snapshot/highlight IDs.
   - Pros: Smallest change that respects existing architecture; keeps backend as source of truth for state, variables, and highlight IDs; reuses the stable runtime API directly; avoids frontend inference.
   - Cons: Requires extending the session artifact contract because `prepared-document.json` alone cannot recreate runtime behavior.
   - Effort: Low/Medium

2. **Frontend-driven bridge using existing highlight API plus ad-hoc runtime calls** — keep `workbench-session.json` mostly unchanged and let the browser stitch together separate calls for runtime control and highlight updates.
   - Pros: Smaller apparent backend diff.
   - Cons: Splits source of truth across endpoints and frontend logic; easy to desynchronize snapshot vs highlight; pushes orchestration into JS for no real gain.
   - Effort: Medium

3. **Single generic command endpoint** — add one `/api/runtime/command` endpoint that accepts multiple operations and returns mixed payloads.
   - Pros: One HTTP entry point.
   - Cons: Weak contract clarity; harder to test; encourages protocol creep immediately.
   - Effort: Medium

### Recommendation
Choose **Session-backed runtime bridge with snapshot API**.

Smallest controlled slice:

- Keep the current local web architecture: Python `http.server`, static HTML/JS, server-owned session state.
- Promote the backend to the single source of truth for runtime state.
- Build one runtime from the canonical HSM JSON that already feeds rendering, call `init()` once, and keep that runtime instance inside the server session.
- Expose one read model such as `runtime-session.json` or `GET /api/runtime.json` that always returns at least:
  - current leaf `state_id`
  - current `active_path`
  - current variable map
  - backend-derived `active_ids` for SVG highlighting
  - declared variable IDs and event IDs needed by the minimal web controls
- Expose only three mutations:
  - reset to initial state
  - send one event by `event_id`
  - set one variable by `variable_id` and raw JSON `value`
- Make every mutation return the same full snapshot payload, so the frontend never computes derived runtime state locally.
- Derive SVG highlight IDs in the backend from `runtime.get_snapshot().active_path`, because authored state IDs already equal the exact SVG IDs contract.
- Preserve the current exact-ID highlight behavior for arbitrary manual inspection if desired, but DO NOT use it as the runtime sync mechanism.

The one structural change this slice cannot avoid is persistence of runtime-capable source data in the session. The safest minimal path is to store the canonical HSM JSON alongside the existing artifacts and let the web server load both render/session artifacts and runtime source from that bounded directory.

### Risks
- `workbench-session.json` is currently asserted as an exact three-field contract in tests, so expanding it directly may create unnecessary churn; a separate runtime session payload may be safer.
- `prepared-document.json` cannot rebuild runtime semantics, so any approach that does not persist canonical HSM JSON will paint itself into a corner.
- Variable writes currently accept any `variable_id` in runtime storage; the bridge should decide whether web mutations are restricted to declared HSM variables before proposal/spec work.
- `send_event()` is event-ID-only in v1; event parameter transport should stay out of this slice or it will expand scope immediately.

### Ready for Proposal
Yes — propose `web-runtime-bridge` as a minimal backend-owned runtime session layered onto the existing workbench, with explicit snapshot/reset/event/set-variable APIs and backend-derived SVG active IDs, while deferring UI improvements, event parameters, and richer runtime semantics.
