"""Top-level runtime that exposes the common execution API."""

from __future__ import annotations

import importlib
from types import SimpleNamespace
from typing import Any
from typing import Literal
from typing import TypeAlias
from typing import TypedDict

from mbse.model.activity.activity_model import ActivityModel
from mbse.model.context.context_model import ContextModel
from mbse.model.hsm.hsm_model import HsmModel
from mbse.model.project.project_registry import ProjectRegistry
from mbse.runtime.activity.activity_runtime import ActivityRuntime
from mbse.runtime.hsm.hsm_runtime import HsmRuntime


RuntimeKind: TypeAlias = Literal["hsm", "activity"]
InnerRuntime: TypeAlias = HsmRuntime | ActivityRuntime


class RuntimeStep(TypedDict):
  """One top-level pending step with model metadata."""

  runtime: RuntimeKind
  model_id: str
  step: dict[str, Any]


class RuntimeTrace(TypedDict):
  """One top-level execution trace with model metadata."""

  runtime: RuntimeKind
  model_id: str
  trace: dict[str, Any]


class RuntimeFrame(TypedDict):
  """One active or suspended local runtime frame."""

  runtime: InnerRuntime
  runtime_kind: RuntimeKind
  model_id: str
  log_cursor: int


class Runtime:
  """Mutable runtime facade for a loaded MBSE model or project."""

  def __init__(self) -> None:
    """Runtime initialization."""

    self.registry: ProjectRegistry | None = None
    self.context: ContextModel | None = None
    self.stack: list[RuntimeFrame] = []
    self.execution_log: list[RuntimeTrace] = []

  def init(self, registry: ProjectRegistry) -> None:
    """Initialize the runtime from a loaded project registry."""

    self.registry = registry
    self.context = registry.getContext()
    self._initFrame(registry.getEntrypointModel())

  def initModel(
    self,
    model: HsmModel | ActivityModel,
    context: ContextModel | None = None,
  ) -> None:
    """Initialize the runtime from one loaded executable model."""

    self.registry = None
    self.context = context
    self._initFrame(model)

  def _initFrame(self, model: HsmModel | ActivityModel) -> None:
    """Initialize the root runtime frame."""

    frame = self._createFrame(model)
    self.stack = [frame]
    self.execution_log = []
    self._syncFrameExecutionLog(frame)

  def _createFrame(self, model: HsmModel | ActivityModel) -> RuntimeFrame:
    """Create one local runtime frame for an executable model."""

    if isinstance(model, HsmModel):
      runtime = HsmRuntime()
      runtime.setExecutableHandler(self._executeExecutable)
      runtime.init(model, self.context)
      runtime_kind: RuntimeKind = "hsm"
    elif isinstance(model, ActivityModel):
      runtime = ActivityRuntime()
      runtime.setExecutableHandler(self._executeExecutable)
      runtime.init(model, self.context)
      runtime_kind = "activity"
    else:
      raise TypeError("Runtime must be initialized with an executable model.")

    return {
      "runtime": runtime,
      "runtime_kind": runtime_kind,
      "model_id": model.getDocumentId(),
      "log_cursor": 0,
    }

  def play(self) -> bool:
    """Resume execution and drain pending work in the active runtime."""

    frame = self._requireFrame()
    result = frame["runtime"].play()
    self._syncFrameExecutionLog(frame)
    return result

  def pause(self) -> None:
    """Pause automatic execution in the active runtime."""

    self._requireFrame()["runtime"].pause()

  def isPaused(self) -> bool:
    """Return whether the active runtime is paused."""

    return self._requireFrame()["runtime"].isPaused()

  def step(self) -> bool:
    """Advance exactly one planned step in the active runtime."""

    frame = self._requireFrame()
    result = frame["runtime"].step()
    self._syncFrameExecutionLog(frame)
    return result

  def sendEvent(
    self,
    event_id: str,
    parameters: dict[str, Any] | None = None,
  ) -> bool:
    """Send one event to an HSM entrypoint runtime."""

    frame = self._requireFrame()
    runtime = frame["runtime"]
    if not isinstance(runtime, HsmRuntime):
      raise TypeError("Only HSM runtimes accept events.")
    result = runtime.sendEvent(event_id, parameters)
    self._syncFrameExecutionLog(frame)
    return result

  def getState(self) -> dict[str, str | None]:
    """Return the active HSM state."""

    runtime = self._requireFrame()["runtime"]
    if not isinstance(runtime, HsmRuntime):
      raise TypeError("Only HSM runtimes expose state.")
    return runtime.getState()

  def getEventQueue(self) -> list[dict[str, Any]]:
    """Return queued HSM events."""

    runtime = self._requireFrame()["runtime"]
    if not isinstance(runtime, HsmRuntime):
      raise TypeError("Only HSM runtimes expose an event queue.")
    return runtime.getEventQueue()

  def hasPendingExecution(self) -> bool:
    """Return whether the active runtime has planned work to complete."""

    return self._requireFrame()["runtime"].hasPendingExecution()

  def getNextStep(self) -> RuntimeStep | None:
    """Return the next pending step with model metadata."""

    frame = self._requireFrame()
    runtime = frame["runtime"]
    step = runtime.getNextStep()
    if step is None:
      return None

    return {
      "runtime": frame["runtime_kind"],
      "model_id": frame["model_id"],
      "step": step,
    }

  def getExecutionLog(self) -> list[RuntimeTrace]:
    """Return global execution traces for the active runtime."""

    self._syncFrameExecutionLog(self._requireFrame())
    return self.execution_log

  def getVariable(self, name: str) -> Any:
    """Get one runtime variable value from the active runtime."""

    return self._requireFrame()["runtime"].getVariable(name)

  def setVariable(self, name: str, value: Any) -> None:
    """Set one runtime variable value in the active runtime."""

    self._requireFrame()["runtime"].setVariable(name, value)

  def _executeExecutable(
    self,
    executable_ref: dict[str, Any],
    source_runtime: InnerRuntime,
    event: dict[str, Any] | None,
  ) -> Any:
    """Execute one runtime executable reference."""

    if executable_ref["kind"] == "action_language":
      return self._executeActionLanguageExecutable(
        executable_ref,
        source_runtime,
        event,
      )

    if executable_ref["kind"] == "model":
      return self._executeModelExecutable(executable_ref, source_runtime)

    raise ValueError(f"Unknown executable kind '{executable_ref['kind']}'.")

  def _executeActionLanguageExecutable(
    self,
    executable_ref: dict[str, Any],
    source_runtime: InnerRuntime,
    event: dict[str, Any] | None,
  ) -> Any:
    """Execute one action-language executable and persist ctx mutations."""

    module = importlib.import_module(executable_ref["module"])
    handler = getattr(module, executable_ref["name"])
    ctx = SimpleNamespace(**source_runtime.variables)
    ctx.variables = source_runtime.variables

    if isinstance(source_runtime, HsmRuntime):
      ctx.event_id = event["event_id"] if event is not None else None
      ctx.event_parameters = event["parameters"] if event is not None else {}
      ctx.send_event = lambda nested_event_id, nested_parameters=None: (
        source_runtime.sendEvent(nested_event_id, nested_parameters)
      )

    result = handler(ctx)

    for name in source_runtime.variables:
      if hasattr(ctx, name):
        source_runtime.variables[name] = getattr(ctx, name)

    return result

  def _executeModelExecutable(
    self,
    executable_ref: dict[str, Any],
    caller_runtime: InnerRuntime,
  ) -> Any:
    """Execute a model reference as a nested runtime frame."""

    registry = self._requireRegistry()
    caller_frame = self._requireFrame()
    child_frame = self._createFrame(registry.getModel(executable_ref["model_id"]))
    self._copySharedVariables(caller_runtime, child_frame["runtime"])
    self._syncFrameExecutionLog(caller_frame)

    self.stack.append(child_frame)
    try:
      self._syncFrameExecutionLog(child_frame)
      child_frame["runtime"].play()
      self._syncFrameExecutionLog(child_frame)
    finally:
      self.stack.pop()

    self._copySharedVariables(child_frame["runtime"], caller_runtime)
    variables = child_frame["runtime"].variables
    if "result" in variables:
      return variables["result"]
    return None

  def _copySharedVariables(
    self,
    source: InnerRuntime,
    target: InnerRuntime,
  ) -> None:
    """Copy variable values that exist in both runtime frames."""

    for name, value in source.variables.items():
      if name in target.variables:
        target.variables[name] = value

  def _syncFrameExecutionLog(self, frame: RuntimeFrame) -> None:
    """Append new local-runtime traces to the global runtime log."""

    runtime = frame["runtime"]
    runtime_kind = frame["runtime_kind"]
    model_id = frame["model_id"]

    for trace in runtime.getExecutionLog()[frame["log_cursor"]:]:
      self.execution_log.append(
        {
          "runtime": runtime_kind,
          "model_id": model_id,
          "trace": trace,
        }
      )
      frame["log_cursor"] += 1

  def _requireFrame(self) -> RuntimeFrame:
    """Return the active runtime frame or fail."""

    if not self.stack:
      raise RuntimeError("Runtime has not been initialized with a model or project.")
    return self.stack[-1]

  def _requireRegistry(self) -> ProjectRegistry:
    """Return the initialized project registry or fail."""

    if self.registry is None:
      raise RuntimeError("Model executables require a project registry.")
    return self.registry
