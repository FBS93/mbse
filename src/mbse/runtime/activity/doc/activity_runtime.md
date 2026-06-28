# Activity Runtime

This package executes a validated `ActivityModel` as a mutable activity flow with runtime variables and execution tracing.

## Initialization semantics

Initialization is planned as one pending trace before user code runs.

- The authored `initial.target_id` becomes the first planned step.
- Action and final steps are planned structurally.
- Decision steps are planned as `pending_decision` nodes with both branches precalculated.
- The runtime starts paused.
- Variable defaults are copied from the optional `ContextModel`.

## Execution semantics

- `initial` records the first target.
- `action` executes its `executable` and then follows `transition.target_id`.
- `pending_decision` executes its `condition`, requires a `bool` result, records a resolved `decision`, and splices the chosen branch back into pending execution.
- `final` records termination and leaves no pending execution.

If a transition target id does not resolve to an action, decision, or final, execution fails explicitly.

## Executable context

Actions and decisions receive a mutable context object with:

- one attribute per runtime variable
- `variables`: the runtime variable dictionary

After each executable returns, updated variable attributes are persisted back into runtime state.

ActivityRuntime does not resolve executable references itself. It delegates every executable to the upper `Runtime` handler at the exact action or decision step where execution is required.

## Tracing

The execution log is append-only and stores activity traces as `entries`, matching the HSM runtime trace shape without events. The current runtime has one activity run, so the log contains one trace.

Pending entries are moved into the log as each `step()` executes. `pending_decision` entries are never logged directly; only their resolved `decision` result appears in the execution log.
