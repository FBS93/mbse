# Runtime Layer

The runtime layer executes authored models as mutable runtime instances.

It is responsible for state progression, event queuing, variable mutation, hook and activity execution, and execution tracing.

## Runtime

`Runtime` is the top-level public execution facade. It consumes a `ProjectRegistry` or one loaded executable model, initializes the entrypoint HSM or activity runtime, and owns the global execution log.

`Runtime` owns executable resolution. Local HSM and Activity runtimes decide when an executable step must run, but do not resolve executable references themselves.

Supported executable kinds:

- `kind: "action_language"`: executes the referenced action-language function with the current runtime context.
- `kind: "model"`: resolves `model_id` through the project registry and runs that model to completion.

Model executables synchronize shared runtime variables with their caller. If a model executable is used where a value is required, such as a guard or decision condition, the callee's shared `result` variable is used as the return value. The owning slot still validates the value type, so guards and decision conditions require `result` to be `bool`.

`getNextStep()` returns:

- `runtime`: active runtime kind, currently `hsm` or `activity`.
- `model_id`: `document_id` of the active model.
- `step`: native runtime step.

`getExecutionLog()` returns global traces collected by `Runtime`:

- `runtime`: runtime kind.
- `model_id`: model document id.
- `trace`: native runtime trace.

Local HSM and activity runtime logs are not modified. Their native traces are stored under `trace` before a local runtime instance can be discarded.

## TODO: Public Runtime Types

HSM-specific viewer code currently imports HSM trace and step types from the HSM runtime implementation module. This is acceptable while the HSM viewer remains HSM-specific, but the cleaner long-term boundary is to expose public runtime data contracts from dedicated type modules.

Proposed future structure:

- `mbse.runtime.hsm.hsm_runtime_types`: public HSM runtime trace, pending-step, event, and entry types.
- `mbse.runtime.activity.activity_runtime_types`: public Activity runtime trace, pending-step, and entry types.

Concrete runtime implementations and upper layers such as server/render adapters would import those public types instead of importing type aliases from implementation modules. This keeps strong typing without pretending the upper layer does not understand HSM or Activity semantics through untyped `dict[str, Any]` values.
