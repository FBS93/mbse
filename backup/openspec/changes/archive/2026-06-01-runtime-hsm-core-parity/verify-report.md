## Verification Report

**Change**: runtime-hsm-core-parity
**Version**: N/A
**Mode**: Strict TDD

### Completeness
| Metric | Value |
|--------|-------|
| Tasks total | 12 |
| Tasks complete | 12 |
| Tasks incomplete | 0 |

### Build & Tests Execution
**Build**: ✅ Passed
```text
No separate build step is required for this Python runtime slice.
Generated-engine source loading is exercised by the passing pytest suite.
```

**Tests**: ✅ 13 passed / ❌ 0 failed / ⚠️ 0 skipped
```text
Command: pytest tests/unit/mbse/test_prepare_hsm_engine.py tests/unit/mbse/test_generated_engine.py tests/unit/mbse/test_hsm_runtime.py tests/integration/test_generated_hsm_engine.py

============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /workspaces/MBSE
configfile: pyproject.toml
collected 13 items

tests/unit/mbse/test_prepare_hsm_engine.py ...                           [ 23%]
tests/unit/mbse/test_generated_engine.py ..                              [ 38%]
tests/unit/mbse/test_hsm_runtime.py .....                                [ 76%]
tests/integration/test_generated_hsm_engine.py ...                       [100%]

============================== 13 passed in 0.23s ==============================
```

**Coverage**: ➖ Not available

### TDD Compliance
| Check | Result | Details |
|-------|--------|---------|
| TDD Evidence reported | ✅ | Found in `openspec/changes/runtime-hsm-core-parity/apply-progress.md` |
| All tasks have tests | ✅ | 12/12 task rows cite existing test files |
| RED confirmed (tests exist) | ✅ | 12/12 rows reference present test files and real RED outcomes |
| GREEN confirmed (tests pass) | ✅ | 12/12 rows are covered by the passing targeted suite |
| Triangulation adequate | ✅ | 12/12 rows report multi-case or behaviorally distinct coverage |
| Safety Net for modified files | ✅ | 12/12 rows include pre-change safety-net evidence |

**TDD Compliance**: 6/6 checks passed

---

### Test Layer Distribution
| Layer | Tests | Files | Tools |
|-------|-------|-------|-------|
| Unit | 10 | 3 | pytest |
| Integration | 3 | 1 | pytest |
| E2E | 0 | 0 | not installed |
| **Total** | **13** | **4** | |

---

### Changed File Coverage
Coverage analysis skipped — no coverage tool detected (`pytest-cov` not installed; `--cov` rejected by pytest).

---

### Assertion Quality
**Assertion quality**: ✅ All assertions verify real behavior

---

### Quality Metrics
**Linter**: ➖ Not available (`ruff` configured in `pyproject.toml` but not installed in this environment)
**Type Checker**: ➖ Not available

### Spec Compliance Matrix
| Requirement | Scenario | Test | Result |
|-------------|----------|------|--------|
| Minimal Hierarchical Execution Semantics | Start follows the full initial chain | `tests/unit/mbse/test_hsm_runtime.py > test_hsm_runtime_init_follows_full_initial_chain_for_c_reference_topology` | ✅ COMPLIANT |
| Minimal Hierarchical Execution Semantics | Ancestor dispatch source can take a transition | `tests/unit/mbse/test_hsm_runtime.py > test_hsm_runtime_matches_transition_parity_cases_and_keeps_set_state_leaf_only` | ✅ COMPLIANT |
| Minimal Hierarchical Execution Semantics | Same-branch transition trims at the local ancestor | `tests/unit/mbse/test_hsm_runtime.py > test_hsm_runtime_matches_transition_parity_cases_and_keeps_set_state_leaf_only` | ✅ COMPLIANT |
| Minimal Hierarchical Execution Semantics | Ancestor target stops at that ancestor | `tests/unit/mbse/test_hsm_runtime.py > test_hsm_runtime_matches_transition_parity_cases_and_keeps_set_state_leaf_only` | ✅ COMPLIANT |
| Minimal Hierarchical Execution Semantics | Cross-branch target performs nested initial descent | `tests/unit/mbse/test_hsm_runtime.py > test_hsm_runtime_matches_transition_parity_cases_and_keeps_set_state_leaf_only` | ✅ COMPLIANT |
| Minimal Hierarchical Execution Semantics | Self transition re-enters the active leaf | `tests/unit/mbse/test_hsm_runtime.py > test_hsm_runtime_matches_transition_parity_cases_and_keeps_set_state_leaf_only` | ✅ COMPLIANT |
| Minimal Hierarchical Execution Semantics | Unhandled event is inert | `tests/unit/mbse/test_hsm_runtime.py > test_hsm_runtime_dispatches_to_parent_and_drops_unhandled_events_without_mutation`; `tests/integration/test_generated_hsm_engine.py > test_build_hsm_runtime_replays_reference_parity_sequence_deterministically` | ✅ COMPLIANT |
| Explicit v1 Exclusions And Safety | Action strings remain inert metadata | `tests/unit/mbse/test_hsm_runtime.py > test_build_hsm_runtime_init_resolves_leaf_snapshot_and_keeps_actions_inert`; `tests/integration/test_generated_hsm_engine.py > test_build_hsm_runtime_replays_reference_parity_sequence_deterministically` | ✅ COMPLIANT |
| Explicit v1 Exclusions And Safety | Embedded mechanics stay out of scope | `tests/integration/test_generated_hsm_engine.py > test_build_hsm_runtime_replays_reference_parity_sequence_deterministically` | ✅ COMPLIANT |

**Compliance summary**: 9/9 scenarios compliant

### Correctness (Static Evidence)
| Requirement | Status | Notes |
|------------|--------|-------|
| Start/init parity | ✅ Implemented | `HsmRuntime.init()` descends from root initial through nested local initials and records the deepest initial transition ID. |
| Hierarchical dispatch parity | ✅ Implemented | `send_event()` walks outward from the active leaf and treats the handling ancestor state as the transition source. |
| LCA-based transition trimming | ✅ Implemented | `_compute_transition_path()` uses ancestry tuples to trim exit/entry work at the shared ancestor. |
| Ancestor-target vs descendant/cross-branch behavior | ✅ Implemented | `should_descend_initials=target_id not in source_ancestry` preserves ancestor-target stop behavior while still descending below newly entered compound targets. |
| Embedded-only mechanics excluded | ✅ Implemented | Runtime logic uses parent/ancestry/transition metadata only; no AO queue, scheduler, reserved-event, static-buffer, or action-string execution behavior was added. |
| Public runtime API stability | ✅ Implemented | Public surface remains `build_hsm_runtime` and `HsmRuntime` methods (`init`, `send_event`, `set_state`, `get_state`, `get_snapshot`, variable accessors); changes are private helper/internal metadata only. |

### Coherence (Design)
| Decision | Followed? | Notes |
|----------|-----------|-------|
| Keep `HsmRuntime` as the public execution boundary | ✅ Yes | Integration tests drive the change through `build_hsm_runtime()` only. |
| Add private parity helpers instead of widening public APIs | ✅ Yes | Helper flow lives in `src/mbse/application/hsm_runtime.py`; `src/mbse/application/__init__.py` still exports the same two public symbols. |
| Generate richer metadata for ancestry and transition identity | ✅ Yes | Prepared/generated engine layers now expose `ancestry_by_state_id`, `initial_transition_ids`, and `transition_rows_by_state_id`. |
| Mirror C semantics without importing C mechanics | ✅ Yes | Tests prove Python-visible state outcomes only, while action strings remain inert and no embedded transport/runtime mechanics appear as requirements. |

### Issues Found
**CRITICAL**: None
**WARNING**:
- Coverage analysis could not run because `pytest-cov` is not installed.
- Ruff quality check could not run because `ruff` is not installed.
**SUGGESTION**: None

### Verdict
PASS WITH WARNINGS
Behavioral parity is verified by the required targeted pytest suite, and the only gaps are non-blocking tooling availability for coverage/lint reporting.
