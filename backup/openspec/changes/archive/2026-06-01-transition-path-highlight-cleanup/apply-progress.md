# Apply Progress: Transition Path Highlight Cleanup

## Implementation Progress

**Change**: transition-path-highlight-cleanup
**Mode**: Strict TDD

### Completed Tasks
- [x] 1.1 Update `tests/unit/mbse/test_hsm_runtime.py` to expect ordered tuple paths for `init()`, event+initial chains, self-transition, and `set_state()` clearing to `()`.
- [x] 1.2 Update `tests/unit/mbse/test_web_runtime_bridge.py` so bridge snapshots keep tuple order, drop unknown IDs member-by-member, and never emit scalar fallback.
- [x] 1.3 Update `tests/integration/test_generated_hsm_engine.py` and `tests/integration/test_mbse_workbench.py` fixtures/assertions to require JSON arrays, multi-edge highlight cases, and border-only active-state behavior.
- [x] 2.1 Change `src/mbse/domain/models.py` dataclasses so runtime and viewer `last_transition_id` are `tuple[str, ...]` with empty-tuple defaults.
- [x] 2.2 Refactor `src/mbse/application/hsm_runtime.py` so `_descend_initials()` and `_execute_transition()` accumulate the full ordered executed path, `send_event()` preserves the prior tuple on rejected events, and `set_state()` resets to `()`.
- [x] 2.3 Update `src/mbse/application/web_runtime_bridge.py` to filter each transition ID by exact membership in `highlightable_ids`, preserve surviving order, and serialize only arrays.
- [x] 3.1 Update `src/mbse/web/static/viewer.js` to treat `snapshot.last_transition_id` as an array and apply `is-active-transition` to every returned exact ID.
- [x] 3.2 Update `src/mbse/web/static/viewer.css` so `.is-active-state` affects borders/contours only, while `.is-active-transition` still targets just edge lines and arrowheads, not labels.
- [x] 4.1 Reconcile any workbench helpers touched by the new contract in `tests/support/viewer_browser_harness.py` or `tests/integration/test_hsm_json_workbench.py` only if Phase 1 failures prove they still assume scalars.
- [x] 4.2 Run `pytest tests/unit/mbse/test_hsm_runtime.py tests/unit/mbse/test_web_runtime_bridge.py tests/integration/test_generated_hsm_engine.py tests/integration/test_mbse_workbench.py` and finish with a full `pytest` pass before handoff.

### Files Changed
| File | Action | What Was Done |
|------|--------|---------------|
| `src/mbse/domain/models.py` | Modified | Changed runtime and viewer snapshots to tuple-based `last_transition_id` defaults. |
| `src/mbse/application/hsm_runtime.py` | Modified | Accumulated the full executed transition path for init and event resolutions, while clearing on `set_state()`. |
| `src/mbse/application/web_runtime_bridge.py` | Modified | Filtered transition IDs member-by-member and exposed tuple-backed arrays only. |
| `src/mbse/web/static/viewer.js` | Modified | Applied transition highlight classes to every returned transition ID. |
| `src/mbse/web/static/viewer.css` | Modified | Removed active-state fill intensification while keeping border and transition emphasis. |
| `tests/unit/mbse/test_hsm_runtime.py` | Modified | Locked runtime tuple-path behavior for init chains, event chains, self transitions, and `set_state()`. |
| `tests/unit/mbse/test_web_runtime_bridge.py` | Modified | Locked bridge tuple filtering behavior and empty-tuple fallback rules. |
| `tests/integration/test_generated_hsm_engine.py` | Modified | Updated deterministic parity snapshots to tuple transition paths. |
| `tests/integration/test_mbse_workbench.py` | Modified | Updated JSON array expectations and multi-edge viewer highlight coverage. |
| `tests/integration/test_mbse_session_build.py` | Modified | Brought prepared-document fixtures back in sync with authored-ID validation for full-suite verification. |
| `openspec/changes/transition-path-highlight-cleanup/tasks.md` | Modified | Marked the planned apply tasks complete. |
| `openspec/changes/transition-path-highlight-cleanup/apply-progress.md` | Created | Recorded cumulative apply progress and TDD evidence. |

### TDD Cycle Evidence
| Task | Test File | Layer | Safety Net | RED | GREEN | TRIANGULATE | REFACTOR |
|------|-----------|-------|------------|-----|-------|-------------|----------|
| 1.1 | `tests/unit/mbse/test_hsm_runtime.py` | Unit | ✅ 31/31 focused baseline | ✅ Written | ✅ Focused pytest passed | ✅ Init chains + event chains + clearing | ✅ Runtime tuple accumulation simplified |
| 1.2 | `tests/unit/mbse/test_web_runtime_bridge.py` | Unit | ✅ 31/31 focused baseline | ✅ Written | ✅ Focused pytest passed | ✅ Exact-ID keep/drop cases | ✅ Tuple filtering kept inline and minimal |
| 1.3 | `tests/integration/test_generated_hsm_engine.py`, `tests/integration/test_mbse_workbench.py` | Integration | ✅ 31/31 focused baseline | ✅ Written | ✅ Focused pytest passed | ✅ JSON array + multi-edge highlight cases | ✅ Fixture updates kept behavior explicit |
| 2.1 | `tests/unit/mbse/test_hsm_runtime.py`, `tests/unit/mbse/test_web_runtime_bridge.py` | Unit | ✅ 31/31 focused baseline | ✅ Written | ✅ Focused pytest passed | ✅ Empty tuple + single/multi-step cases | ✅ Dataclass defaults aligned with contract |
| 2.2 | `tests/unit/mbse/test_hsm_runtime.py`, `tests/integration/test_generated_hsm_engine.py` | Unit/Integration | ✅ 31/31 focused baseline | ✅ Written | ✅ Focused pytest passed | ✅ Init, event, self-transition, rejected-event cases | ✅ Extracted tuple-building path without compatibility logic |
| 2.3 | `tests/unit/mbse/test_web_runtime_bridge.py`, `tests/integration/test_mbse_workbench.py` | Unit/Integration | ✅ 31/31 focused baseline | ✅ Written | ✅ Focused pytest passed | ✅ Mixed known/unknown transition IDs | ✅ Bridge serialization stayed exact-match only |
| 3.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 31/31 focused baseline | ✅ Written | ✅ Focused pytest passed | ✅ Single + multi-edge highlight cases | ✅ Highlight application stayed generic |
| 3.2 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 31/31 focused baseline | ✅ Written | ✅ Focused pytest passed | ✅ State border-only + transition-only shape coverage | ✅ CSS change limited to fill removal |
| 4.1 | `tests/integration/test_mbse_workbench.py` | Integration | ✅ 31/31 focused baseline | ✅ Written | ✅ Focused pytest passed | ✅ Viewer harness proved array support without extra helper changes | ➖ None needed |
| 4.2 | `tests/integration/test_mbse_session_build.py`, full `pytest` | Integration | ✅ 31/31 focused baseline | ✅ Written | ✅ 74/74 pytest passed | ✅ Focused command + full suite | ✅ Full-suite fixture repaired to current validation contract |

### Test Summary
- **Total tests written**: Updated 10 existing tests and added 1 bridge test plus expanded integration assertions.
- **Total tests passing**: 74
- **Layers used**: Unit, Integration
- **Approval tests** (refactoring): None — behavior changed intentionally under spec.
- **Pure functions created**: 0

### Deviations from Design
None — implementation matches design.

### Issues Found
- Full-suite verification exposed two stale prepared-document integration fixtures that no longer matched authored-ID validation; they were updated so verification reflects the current contract.

### Remaining Tasks
- [ ] None.

### Workload / PR Boundary
- Mode: single PR
- Current work unit: Unit 1 — breaking path-array contract end-to-end
- Boundary: runtime/viewer contract cleanup from tuple production through browser highlighting and verification
- Estimated review budget impact: within the planned low-risk single-PR slice

### Status
10/10 tasks complete. Ready for verify.
