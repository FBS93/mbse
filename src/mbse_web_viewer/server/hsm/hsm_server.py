from __future__ import annotations

"""Serve one HSM runtime session together with its rendered SVG viewer."""

import argparse
from copy import deepcopy
from pathlib import Path
from typing import Any
import webbrowser

from mbse.model.context.context_model import ContextModel
from mbse.model.activity.activity_model import ActivityModel
from mbse.model.hsm.hsm_model import HsmExternalTransitionRelation
from mbse.model.hsm.hsm_model import HsmGuardedTransitionBranchRelation
from mbse.model.hsm.hsm_model import HsmModel
from mbse.model.hsm.hsm_model import HsmRelatedState
from mbse.model.project.project_registry import ProjectRegistry
from mbse.runtime.hsm.hsm_runtime import HsmRuntimeExternalTransition
from mbse.runtime.hsm.hsm_runtime import HsmRuntimeGuardBranchTransition
from mbse.runtime.hsm.hsm_runtime import HsmRuntimeGuardCondition
from mbse.runtime.hsm.hsm_runtime import HsmRuntimeInitialTransition
from mbse.runtime.hsm.hsm_runtime import HsmRuntimeInternalTransition
from mbse.runtime.hsm.hsm_runtime import HsmRuntimeOnEntry
from mbse.runtime.hsm.hsm_runtime import HsmRuntimeOnExit
from mbse.runtime.hsm.hsm_runtime import HsmRuntimePendingExecutionTypeAlias
from mbse.runtime.hsm.hsm_runtime import HsmRuntimeTrace
from mbse.runtime.runtime import Runtime
from mbse_web_viewer.render.activity.activity_render import ActivityRender
from mbse_web_viewer.render.hsm.hsm_render import HsmRender
from mbse_web_viewer.server.session import ViewerBreakpointTarget
from mbse_web_viewer.server.session import ViewerFocus
from mbse_web_viewer.server.session import ViewerHighlight
from mbse_web_viewer.server.session import ViewerSession
from mbse_web_viewer.server.session import ViewerTrace
from mbse_web_viewer.server.server import RunningViewerServer
from mbse_web_viewer.server.server import startViewerServer


class HsmViewerServerController:
  """Own the rendered SVG, runtime instance, and derived viewer session."""

  def __init__(self, model: HsmModel, context: ContextModel | None = None) -> None:
    """Initialize the controller from one validated HSM model."""

    self._model = model
    self._context = context
    self._rendered_svg = HsmRender()
    self._rendered_svg.render(model)
    self._breakpoint_enabled_by_id: dict[str, bool] = {}
    self._breakpoint_targets = self._buildBreakpointTargets()
    self._breakpoint_target_ids = tuple(self._breakpoint_targets)
    self._breakpoint_order: list[str] = []
    self._runtime = self._buildRuntime()
    self._changed_variable_ids: tuple[str, ...] = ()
    self._advanceToNextExecutableStepForViewer()
    self._last_highlight = self._buildCurrentTraceHighlight()

  def getSvgText(self) -> str:
    """Return the rendered SVG document served by the viewer."""

    return self._rendered_svg.getSvgText()

  def getModelSvgText(self, model_id: str) -> str:
    """Return the rendered SVG document for one model id."""

    if model_id != self._model.getDocumentId():
      raise KeyError(f"Unknown model_id '{model_id}'.")
    return self.getSvgText()

  def _getViewerModels(self) -> tuple[dict[str, object], ...]:
    """Return models available to the current viewer session."""

    return (
      {
        "model_id": self._model.getDocumentId(),
        "kind": "hsm",
        "svg_url": "/artifacts/diagram.svg",
        "is_entrypoint": True,
      },
    )

  def _getActiveModelId(self) -> str:
    """Return the model id currently emphasized by this controller."""

    return self._model.getDocumentId()

  def getSession(self) -> ViewerSession:
    """Return the current serialized browser session."""

    return ViewerSession(
      document_id=self._model.getDocumentId(),
      active_model_id=self._getActiveModelId(),
      svg_url="/artifacts/diagram.svg",
      models=self._getViewerModels(),
      enums=tuple(dict(enum) for enum in self._getContextEnums()),
      events=tuple(dict(event) for event in self._model.getEvents()),
      variables=tuple(dict(variable) for variable in self._getContextVariables()),
      state=self._runtime.getState(),
      variable_values={
        variable["name"]: self._runtime.getVariable(variable["name"])
        for variable in self._getContextVariables()
      },
      changed_variable_ids=self._changed_variable_ids,
      execution_log=self._serializeExecutionLog(),
      debugger=self._serializeDebuggerState(),
      highlight=self._last_highlight,
      focus=self._buildCurrentStateFocus(),
      last_trace=self._serializeLastTrace(),
      breakpoints=self._serializeBreakpoints(),
    )

  def reset(self) -> ViewerSession:
    """Reset the runtime and return the refreshed browser session."""

    self._runtime = self._buildRuntime()
    self._changed_variable_ids = ()
    self._advanceToNextExecutableStepForViewer()
    self._last_highlight = self._buildCurrentTraceHighlight()
    return self.getSession()

  def sendEvent(
    self,
    event_id: str,
    parameters: dict[str, Any] | None = None,
  ) -> ViewerSession:
    """Send one runtime event and return the refreshed browser session."""

    self._requireDeclaredEventId(event_id)
    initial_variable_values = self._snapshotVariableValues()
    should_run_to_breakpoint = (
      self._hasEnabledBreakpoints() and not self._runtime.isPaused()
    )
    if should_run_to_breakpoint:
      self._runtime.pause()
    self._runtime.sendEvent(event_id, parameters)
    if should_run_to_breakpoint:
      self._playUntilBreakpoint()
    else:
      self._advanceToNextExecutableStepForViewer()
    self._changed_variable_ids = self._diffVariableIds(initial_variable_values)
    self._last_highlight = self._buildCurrentTraceHighlight()
    return self.getSession()

  def play(self) -> ViewerSession:
    """Run the runtime until the current pending work and queue are drained."""

    initial_variable_values = self._snapshotVariableValues()
    if self._hasEnabledBreakpoints():
      self._playUntilBreakpoint()
    else:
      self._runtime.play()
    self._changed_variable_ids = self._diffVariableIds(initial_variable_values)
    self._last_highlight = self._buildCurrentTraceHighlight()
    return self.getSession()

  def pause(self) -> ViewerSession:
    """Pause future automatic execution and return the refreshed session."""

    self._runtime.pause()
    self._last_highlight = self._buildCurrentTraceHighlight()
    return self.getSession()

  def stepExecution(self) -> ViewerSession:
    """Advance the runtime to the next debugger step."""

    initial_variable_values = self._snapshotVariableValues()
    self._runtime.step()
    self._advanceToNextExecutableStepForViewer()
    self._changed_variable_ids = self._diffVariableIds(initial_variable_values)
    self._last_highlight = self._buildCurrentTraceHighlight()
    return self.getSession()

  def setVariable(self, variable_id: str, value: Any) -> ViewerSession:
    """Set one runtime variable and return the refreshed browser session."""

    self._requireDeclaredVariableId(variable_id)
    initial_variable_values = self._snapshotVariableValues()
    self._runtime.setVariable(variable_id, value)
    self._changed_variable_ids = self._diffVariableIds(initial_variable_values)
    self._last_highlight = self._buildCurrentTraceHighlight()
    return self.getSession()

  def toggleBreakpoint(self, breakpoint_id: str) -> ViewerSession:
    """Toggle one declared debugger breakpoint target."""

    if breakpoint_id not in self._breakpoint_targets:
      raise KeyError(f"Unknown breakpoint_id '{breakpoint_id}'.")
    if breakpoint_id in self._breakpoint_enabled_by_id:
      del self._breakpoint_enabled_by_id[breakpoint_id]
      self._breakpoint_order = [
        ordered_breakpoint_id
        for ordered_breakpoint_id in self._breakpoint_order
        if ordered_breakpoint_id != breakpoint_id
      ]
    else:
      self._breakpoint_enabled_by_id[breakpoint_id] = True
      self._breakpoint_order.append(breakpoint_id)
    self._last_highlight = self._buildCurrentTraceHighlight()
    return self.getSession()

  def removeBreakpoint(self, breakpoint_id: str) -> ViewerSession:
    """Remove one set debugger breakpoint."""

    if breakpoint_id not in self._breakpoint_targets:
      raise KeyError(f"Unknown breakpoint_id '{breakpoint_id}'.")
    self._breakpoint_enabled_by_id.pop(breakpoint_id, None)
    self._breakpoint_order = [
      ordered_breakpoint_id
      for ordered_breakpoint_id in self._breakpoint_order
      if ordered_breakpoint_id != breakpoint_id
    ]
    self._last_highlight = self._buildCurrentTraceHighlight()
    return self.getSession()

  def setBreakpointEnabled(
    self,
    breakpoint_id: str,
    enabled: bool,
  ) -> ViewerSession:
    """Enable or disable one existing debugger breakpoint."""

    if breakpoint_id not in self._breakpoint_targets:
      raise KeyError(f"Unknown breakpoint_id '{breakpoint_id}'.")
    if breakpoint_id not in self._breakpoint_enabled_by_id:
      raise KeyError(f"Breakpoint '{breakpoint_id}' is not set.")
    self._breakpoint_enabled_by_id[breakpoint_id] = enabled
    self._last_highlight = self._buildCurrentTraceHighlight()
    return self.getSession()

  def reorderBreakpoints(self, breakpoint_ids: list[str]) -> ViewerSession:
    """Persist one explicit order for the currently set debugger breakpoints."""

    ordered_breakpoint_ids: list[str] = []
    seen_breakpoint_ids: set[str] = set()
    for breakpoint_id in breakpoint_ids:
      if breakpoint_id not in self._breakpoint_targets:
        raise KeyError(f"Unknown breakpoint_id '{breakpoint_id}'.")
      if breakpoint_id not in self._breakpoint_enabled_by_id:
        raise ValueError(f"Breakpoint '{breakpoint_id}' is not set.")
      if breakpoint_id in seen_breakpoint_ids:
        raise ValueError(f"Breakpoint '{breakpoint_id}' was provided more than once.")
      seen_breakpoint_ids.add(breakpoint_id)
      ordered_breakpoint_ids.append(breakpoint_id)

    current_set_breakpoint_ids = set(self._breakpoint_enabled_by_id)
    if seen_breakpoint_ids != current_set_breakpoint_ids:
      raise ValueError(
        "Breakpoint reorder payload must include every set breakpoint exactly once."
      )

    self._breakpoint_order = ordered_breakpoint_ids
    self._last_highlight = self._buildCurrentTraceHighlight()
    return self.getSession()

  def _buildRuntime(self) -> Runtime:
    """Create and initialize one fresh runtime from the current model."""

    runtime = Runtime()
    runtime.initModel(self._model, self._context)
    return runtime

  def _getNextStep(self) -> HsmRuntimePendingExecutionTypeAlias | None:
    """Return the native pending HSM step from the top-level runtime."""

    wrapped_step = self._runtime.getNextStep()
    if wrapped_step is None:
      return None
    return wrapped_step["step"]

  def _getExecutionLog(self) -> list[HsmRuntimeTrace]:
    """Return native HSM traces from the top-level runtime."""

    return [
      wrapped_trace["trace"]
      for wrapped_trace in self._runtime.getExecutionLog()
      if (
        wrapped_trace["runtime"] == "hsm"
        and wrapped_trace["model_id"] == self._model.getDocumentId()
      )
    ]

  def _getContextEnums(self) -> list[dict[str, Any]]:
    """Return context enum declarations available to the viewer."""

    return [] if self._context is None else self._context.getEnums()

  def _getContextVariables(self) -> list[dict[str, Any]]:
    """Return context variable declarations available to the runtime."""

    return [] if self._context is None else self._context.getVariables()

  def _snapshotVariableValues(self) -> dict[str, Any]:
    """Return a detached snapshot of current runtime variable values."""

    return {
      variable["name"]: deepcopy(self._runtime.getVariable(variable["name"]))
      for variable in self._getContextVariables()
    }

  def _diffVariableIds(self, initial_variable_values: dict[str, Any]) -> tuple[str, ...]:
    """Return variable ids whose current value differs from one snapshot."""

    return tuple(
      variable["name"]
      for variable in self._getContextVariables()
      if (
        self._runtime.getVariable(variable["name"])
        != initial_variable_values[variable["name"]]
      )
    )

  def _playUntilBreakpoint(self) -> None:
    """Run pending work until idle or before the next active breakpoint step."""

    skipped_breakpoint_id = self._getPendingBreakpointId()

    while True:
      self._advanceToNextExecutableStepForViewer(
        stop_on_breakpoint=True,
        skipped_breakpoint_id=skipped_breakpoint_id,
      )
      next_step = self._getNextStep()
      if next_step is None:
        if not self._runtime.getEventQueue():
          self._runtime.play()
          return
        self._runtime.step()
        skipped_breakpoint_id = None
        continue

      breakpoint_id = self._breakpointIdForStep(next_step)
      if (
        breakpoint_id is not None
        and self._isBreakpointEnabled(breakpoint_id)
        and breakpoint_id != skipped_breakpoint_id
      ):
        self._runtime.pause()
        return

      self._runtime.step()
      skipped_breakpoint_id = None

  def _advanceToNextExecutableStepForViewer(
    self,
    *,
    stop_on_breakpoint: bool = True,
    skipped_breakpoint_id: str | None = None,
  ) -> None:
    """Consume pending entries that should be shown only as completed path."""

    while True:
      next_step = self._getNextStep()
      if next_step is None:
        return
      breakpoint_id = self._breakpointIdForStep(next_step)
      if (
        stop_on_breakpoint
        and breakpoint_id is not None
        and self._isBreakpointEnabled(breakpoint_id)
        and breakpoint_id != skipped_breakpoint_id
      ):
        self._runtime.pause()
        return
      if next_step["kind"] == "change_active_state":
        self._runtime.step()
        continue
      if self._isNonExecutableTransitionStep(next_step):
        self._runtime.step()
        continue
      return

  def _isNonExecutableTransitionStep(
    self,
    step: HsmRuntimePendingExecutionTypeAlias,
  ) -> bool:
    """Return whether one pending transition has no executable to execute."""

    return (
      step["kind"] in {
        "external_transition",
        "guarded_transition",
        "guard_branch_transition",
        "initial_transition",
        "internal_transition",
      }
      and step["activity"] is None
    )

  def _serializeLastTrace(self) -> ViewerTrace:
    """Serialize the latest runtime trace for lightweight browser inspection."""

    execution_log = self._getExecutionLog()
    if not execution_log:
      return ViewerTrace(event_id=None, entries=[])

    trace = execution_log[-1]
    return ViewerTrace(
      event_id=trace["event"]["event_id"],
      entries=[dict(entry) for entry in trace["entries"]],
    )

  def _serializeExecutionLog(self) -> list[dict[str, object]]:
    """Serialize the full runtime execution log without viewer formatting."""

    return [
      {
        "event": dict(trace["event"]),
        "entries": [dict(entry) for entry in trace["entries"]],
      }
      for trace in self._getExecutionLog()
    ]

  def _serializeDebuggerState(self) -> dict[str, object]:
    """Serialize the minimal debugger state needed by the browser UI."""

    queued_events = [dict(event) for event in self._runtime.getEventQueue()]
    has_pending_execution = self._runtime.hasPendingExecution()
    current_event = None
    execution_log = self._getExecutionLog()
    if has_pending_execution and execution_log:
      current_event = dict(execution_log[-1]["event"])
    elif queued_events:
      current_event = dict(queued_events[0])
    completed_traces = execution_log
    if has_pending_execution and completed_traces:
      completed_traces = completed_traces[:-1]
    return {
      "is_paused": self._runtime.isPaused(),
      "current_event": current_event,
      "queued_events": queued_events,
      "event_history": [
        dict(trace["event"])
        for trace in completed_traces
        if trace["event"]["event_id"] is not None
      ],
      "has_pending_execution": has_pending_execution,
      "can_step": has_pending_execution or bool(queued_events),
    }

  def _serializeBreakpoints(self) -> tuple[ViewerBreakpointTarget, ...]:
    """Serialize all available breakpoint targets with current active state."""

    return tuple(
      ViewerBreakpointTarget(
        id=target.id,
        label=target.label,
        svg_ids=target.svg_ids,
        text_ids=target.text_ids,
        is_set=target.id in self._breakpoint_enabled_by_id,
        enabled=self._isBreakpointEnabled(target.id),
      )
      for target in (
        self._breakpoint_targets[breakpoint_id]
        for breakpoint_id in self._iterSerializedBreakpointIds()
      )
    )

  def _iterSerializedBreakpointIds(self) -> tuple[str, ...]:
    """Return breakpoint ids ordered for viewer serialization."""

    ordered_set_breakpoint_ids = [
      breakpoint_id
      for breakpoint_id in self._breakpoint_order
      if breakpoint_id in self._breakpoint_enabled_by_id
    ]
    remaining_set_breakpoint_ids = [
      breakpoint_id
      for breakpoint_id in self._breakpoint_target_ids
      if (
        breakpoint_id in self._breakpoint_enabled_by_id
        and breakpoint_id not in ordered_set_breakpoint_ids
      )
    ]
    unset_breakpoint_ids = [
      breakpoint_id
      for breakpoint_id in self._breakpoint_target_ids
      if breakpoint_id not in self._breakpoint_enabled_by_id
    ]
    return tuple(
      ordered_set_breakpoint_ids + remaining_set_breakpoint_ids + unset_breakpoint_ids
    )

  def _hasEnabledBreakpoints(self) -> bool:
    """Return whether any set breakpoint is currently enabled."""

    return any(self._breakpoint_enabled_by_id.values())

  def _isBreakpointEnabled(self, breakpoint_id: str) -> bool:
    """Return whether one breakpoint is set and enabled."""

    return self._breakpoint_enabled_by_id.get(breakpoint_id, False)

  def _buildBreakpointTargets(self) -> dict[str, ViewerBreakpointTarget]:
    """Build semantic debugger breakpoint targets backed by rendered SVG text ids."""

    targets: dict[str, ViewerBreakpointTarget] = {}
    for state in self._model.iterStates():
      state_id = state["id"]
      self._addBreakpointTarget(
        targets,
        breakpoint_id=self._breakpointKey("change_active_state", state_id),
        label=f"Enter state: {self._model.getStateLabel(state_id)}",
        svg_ids=(self._rendered_svg.getStateId(state_id),),
        text_ids=self._rendered_svg.getStateLabelTextIds(state_id),
      )

      for section_name, activities in (
        ("on_entry", self._model.getStateOnEntry(state_id)),
        ("on_exit", self._model.getStateOnExit(state_id)),
      ):
        for activity in activities:
          activity_key = self._executableKey(activity)
          self._addBreakpointTarget(
            targets,
            breakpoint_id=self._breakpointKey(section_name, state_id, activity_key),
            label=(
              f"{self._formatHookName(section_name)}: "
              f"{self._model.getStateLabel(state_id)} / {self._executableLabel(activity)}"
            ),
            svg_ids=(self._rendered_svg.getStateId(state_id),),
            text_ids=self._rendered_svg.getStateHookActivityTextIds(
              state_id,
              section_name,
              activity,
            ),
          )

      for transition in self._model.getStateInternalTransitions(state_id):
        event_id = transition["event_id"]
        for activity in transition.get("activities", []):
          activity_key = self._executableKey(activity)
          transition_ids = self._rendered_svg.getInternalTransitionIds(state_id, event_id)
          text_ids: list[str] = []
          for transition_id in transition_ids:
            text_ids.extend(
              self._rendered_svg.getInternalTransitionActivityTextIds(
                transition_id,
                activity,
              )
            )
          self._addBreakpointTarget(
            targets,
            breakpoint_id=self._breakpointKey(
              "internal_transition",
              state_id,
              event_id,
              activity_key,
            ),
            label=(
              "Internal transition: "
              f"{self._model.getStateLabel(state_id)} / {event_id} / {self._executableLabel(activity)}"
            ),
            svg_ids=transition_ids,
            text_ids=tuple(text_ids),
          )

      if self._model.hasStateInitialTransition(state_id):
        target_state_id = self._model.getStateInitialTargetId(state_id)
        transition_id = self._rendered_svg.getInitialTransitionId(state_id)
        for activity in self._model.getStateInitialTransitionActivities(state_id):
          activity_key = self._executableKey(activity)
          self._addBreakpointTarget(
            targets,
            breakpoint_id=self._breakpointKey(
              "initial_transition",
              state_id,
              target_state_id,
              activity_key,
            ),
            label=(
              "Initial transition: "
              f"{self._model.getStateLabel(state_id)} -> "
              f"{self._model.getStateLabel(target_state_id)} / {self._executableLabel(activity)}"
            ),
            svg_ids=(transition_id,),
            text_ids=self._rendered_svg.getInitialTransitionActivityTextIds(
              transition_id,
              activity,
            ),
          )

      for transition in self._model.getOutgoingExternalTransitions(state_id):
        self._appendExternalBreakpointTargets(targets, state_id, transition)

    return targets

  def _appendExternalBreakpointTargets(
    self,
    targets: dict[str, ViewerBreakpointTarget],
    state_id: str,
    transition: dict[str, Any],
  ) -> None:
    """Append breakpoint targets for one authored external transition."""

    event_id = transition["event_id"]
    guard_condition = transition.get("guard_condition")
    if guard_condition is None:
      target_state_id = transition["target_id"]
      transition_ids = self._rendered_svg.getExternalTransitionIds(
        state_id,
        event_id,
        target_state_id,
      )
      for activity in transition.get("activities", []):
        self._addTransitionActivityBreakpointTarget(
          targets,
          kind="external_transition",
          state_id=state_id,
          event_id=event_id,
          target_state_id=target_state_id,
          transition_ids=transition_ids,
          activity=activity,
        )
      return

    guard_activity = guard_condition["guard_activity"]
    guard_activity_key = self._executableKey(guard_activity)
    self._addBreakpointTarget(
      targets,
      breakpoint_id=self._breakpointKey("guard_condition", state_id, event_id, guard_activity_key),
      label=(
        "Guard: "
        f"{self._model.getStateLabel(state_id)} / {event_id} / {self._executableLabel(guard_activity)}"
      ),
      svg_ids=self._rendered_svg.getGuardNodeIds(state_id, event_id),
      text_ids=self._rendered_svg.getGuardNodeTextIds(state_id, event_id),
    )

    guarded_ids = self._rendered_svg.getGuardedTransitionIds(state_id, event_id)
    for activity in transition.get("activities", []):
      self._addTransitionActivityBreakpointTarget(
        targets,
        kind="guarded_transition",
        state_id=state_id,
        event_id=event_id,
        target_state_id="guard",
        transition_ids=guarded_ids,
        activity=activity,
      )

    for result, branch_key in ((True, "true_branch"), (False, "false_branch")):
      branch = guard_condition[branch_key]
      target_state_id = branch["target_id"]
      branch_ids = self._rendered_svg.getGuardBranchIds(
        state_id,
        event_id,
        outcome=result,
        target_state_id=target_state_id,
      )
      for activity in branch.get("activities", []):
        activity_key = self._executableKey(activity)
        text_ids: list[str] = []
        for branch_id in branch_ids:
          text_ids.extend(
            self._rendered_svg.getExternalTransitionActivityTextIds(
              branch_id,
              activity,
            )
          )
        self._addBreakpointTarget(
          targets,
          breakpoint_id=self._breakpointKey(
            "guard_branch_transition",
            state_id,
            event_id,
            str(result),
            target_state_id,
            activity_key,
          ),
          label=(
            "Guard branch: "
            f"{event_id} {'true' if result else 'false'} -> "
            f"{self._model.getStateLabel(target_state_id)} / {self._executableLabel(activity)}"
          ),
          svg_ids=branch_ids,
          text_ids=tuple(text_ids),
        )

  def _addTransitionActivityBreakpointTarget(
    self,
    targets: dict[str, ViewerBreakpointTarget],
    *,
    kind: str,
    state_id: str,
    event_id: str,
    target_state_id: str,
    transition_ids: tuple[str, ...],
    activity: dict[str, str],
  ) -> None:
    """Append one external-transition activity breakpoint target."""

    activity_key = self._executableKey(activity)
    target_label = (
      "guard"
      if target_state_id == "guard"
      else self._model.getStateLabel(target_state_id)
    )
    text_ids: list[str] = []
    for transition_id in transition_ids:
      text_ids.extend(
        self._rendered_svg.getExternalTransitionActivityTextIds(
          transition_id,
          activity,
        )
      )
    self._addBreakpointTarget(
      targets,
      breakpoint_id=self._breakpointKey(
        kind,
        state_id,
        event_id,
        target_state_id,
        activity_key,
      ),
      label=(
        "Transition: "
        f"{self._model.getStateLabel(state_id)} --{event_id}--> "
        f"{target_label} / {self._executableLabel(activity)}"
      ),
      svg_ids=transition_ids,
      text_ids=tuple(text_ids),
    )

  def _addBreakpointTarget(
    self,
    targets: dict[str, ViewerBreakpointTarget],
    *,
    breakpoint_id: str,
    label: str,
    svg_ids: tuple[str, ...],
    text_ids: tuple[str, ...],
  ) -> None:
    """Store one breakpoint target when it has a rendered text anchor."""

    if not text_ids:
      return
    targets[breakpoint_id] = ViewerBreakpointTarget(
      id=breakpoint_id,
      label=label,
      svg_ids=svg_ids,
      text_ids=text_ids,
      is_set=breakpoint_id in self._breakpoint_enabled_by_id,
      enabled=self._isBreakpointEnabled(breakpoint_id),
    )

  def _buildCurrentTraceHighlight(self) -> ViewerHighlight:
    """Resolve the latest runtime trace into SVG ids for highlighting."""

    trace = self._getExecutionLog()[-1]
    state_ids = self._buildStateHighlightIds()
    transition_ids = list(self._buildTraceTransitionIds(trace))
    text_ids = list(self._buildTraceTextIds(trace, transition_ids))
    current_transition_ids: tuple[str, ...] = ()
    current_text_ids: tuple[str, ...] = ()
    next_step = self._getNextStep()
    if next_step is not None:
      if next_step["kind"] == "change_active_state":
        current_transition_ids = (
          self._rendered_svg.getStateId(next_step["target_state_id"]),
        )
        current_text_ids = self._rendered_svg.getStateLabelTextIds(
          next_step["target_state_id"]
        )
      else:
        current_transition_ids, current_text_ids = self._buildCurrentEntryHighlightIds(next_step)
    return ViewerHighlight(
      state_ids=state_ids,
      transition_ids=tuple(dict.fromkeys(transition_ids)),
      text_ids=tuple(dict.fromkeys(text_ids)),
      current_transition_ids=tuple(dict.fromkeys(current_transition_ids)),
      current_text_ids=tuple(dict.fromkeys(current_text_ids)),
    )

  def _getPendingBreakpointId(self) -> str | None:
    """Return the breakpoint id for the current pending step, if any."""

    next_step = self._getNextStep()
    if next_step is None:
      return None
    return self._breakpointIdForStep(next_step)

  def _breakpointIdForStep(
    self,
    step: HsmRuntimePendingExecutionTypeAlias,
  ) -> str | None:
    """Return the semantic breakpoint id matching one pending runtime step."""

    event_id = self._getPendingEventId()
    kind = step["kind"]
    if kind in {"on_entry", "on_exit"}:
      return self._breakpointKey(
        kind,
        step["source_state_id"],
        self._executableKey(step["activity"]),
      )
    if kind == "change_active_state":
      return self._breakpointKey(kind, step["target_state_id"])
    if kind == "initial_transition" and step["activity"] is not None:
      return self._breakpointKey(
        kind,
        step["source_state_id"],
        step["target_state_id"],
        self._executableKey(step["activity"]),
      )
    if kind == "internal_transition" and event_id is not None and step["activity"] is not None:
      return self._breakpointKey(
        kind,
        step["source_state_id"],
        event_id,
        self._executableKey(step["activity"]),
      )
    if kind == "external_transition" and event_id is not None and step["activity"] is not None:
      return self._breakpointKey(
        kind,
        step["source_state_id"],
        event_id,
        step["target_state_id"],
        self._executableKey(step["activity"]),
      )
    if kind == "guarded_transition" and event_id is not None and step["activity"] is not None:
      return self._breakpointKey(
        kind,
        step["source_state_id"],
        event_id,
        "guard",
        self._executableKey(step["activity"]),
      )
    if kind == "guard_branch_transition" and event_id is not None and step["activity"] is not None:
      return self._breakpointKey(
        kind,
        step["source_state_id"],
        event_id,
        str(step["result"]),
        step["target_state_id"],
        self._executableKey(step["activity"]),
      )
    if kind == "pending_guard_condition" and event_id is not None:
      return self._breakpointKey(
        "guard_condition",
        step["source_state_id"],
        event_id,
        self._executableKey(step["guard_activity"]),
      )
    return None

  def _breakpointKey(self, *parts: object) -> str:
    """Return one stable serialized breakpoint key."""

    return "|".join("" if part is None else str(part) for part in parts)

  def _executableKey(self, activity: dict[str, str]) -> str:
    """Return one stable executable key matching render-layer text targeting."""

    if activity["kind"] == "model":
      return activity["model_id"]
    return f"{activity['module']}.{activity['name']}"

  def _executableLabel(self, activity: dict[str, str]) -> str:
    """Return one readable executable label."""

    if activity["kind"] == "model":
      return activity["model_id"]
    return activity["name"]

  def _formatHookName(self, section_name: str) -> str:
    """Return a readable label for one state hook section."""

    return "On entry" if section_name == "on_entry" else "On exit"

  def _buildCurrentStateFocus(self) -> ViewerFocus:
    """Resolve state-focus and trace-focus contexts for the viewer."""

    return ViewerFocus(
      state_related_ids=self._buildStateModeRelatedIds(),
      trace_related_ids=self._buildTraceModeRelatedIds(),
      state_viewport_focus_ids=self._buildStateModeViewportFocusIds(),
      trace_viewport_focus_ids=self._buildTraceModeViewportFocusIds(),
    )

  def _buildStateModeRelatedIds(self) -> tuple[str, ...]:
    """Return the non-dimmed ids for focus-current-state mode."""

    state_id = self._getEffectiveFocusStateId()
    if state_id is None:
      return ()

    related = self._model.getStateRelatedElements(state_id)
    related_ids = self._buildStateFocusIds(related.states)

    for chain in related.initial_entry_chains:
      for transition in chain:
        if transition.source_state_id is None:
          related_ids.append(self._rendered_svg.getRootInitialTransitionId())
          related_ids.append(self._rendered_svg.getRootInitialTransitionSourceId())
          continue
        related_ids.append(
          self._rendered_svg.getInitialTransitionId(transition.source_state_id)
        )
        related_ids.append(
          self._rendered_svg.getInitialTransitionSourceId(transition.source_state_id)
        )

    for transition in related.outgoing_external_transitions:
      related_ids.extend(self._buildExternalTransitionFocusIds(transition))

    for transition in related.incoming_external_transitions:
      related_ids.extend(self._buildExternalTransitionFocusIds(transition))

    for branch in related.guarded_transition_branches:
      related_ids.extend(self._buildGuardedBranchFocusIds(branch))

    related_ids.extend(self._buildHighlightFocusIds())
    return self._normalizeFocusIds(related_ids)

  def _buildTraceModeRelatedIds(self) -> tuple[str, ...]:
    """Return the non-dimmed ids for focus-trace mode."""

    execution_log = self._getExecutionLog()
    if not execution_log:
      return ()

    trace = execution_log[-1]
    related_ids = self._buildHighlightFocusIds()
    state_ids = self._getTraceStateIds(trace)
    state_ids.update(self._getPendingTraceStateIds())
    if not state_ids:
      state_id = self._getEffectiveFocusStateId()
      if state_id is not None:
        state_ids.add(state_id)

    for state_id in sorted(state_ids):
      related_ids.extend(self._buildStateOwnedFocusIds(state_id))

    for entry in trace["entries"]:
      if entry["kind"] != "initial_transition":
        continue
      source_state_id = entry["source_state_id"]
      if source_state_id is None:
        related_ids.append(self._rendered_svg.getRootInitialTransitionSourceId())
      else:
        related_ids.append(self._rendered_svg.getInitialTransitionSourceId(source_state_id))

    return self._normalizeFocusIds(related_ids)

  def _buildStateModeViewportFocusIds(self) -> tuple[str, ...]:
    """Return the viewport target for focus-current-state mode."""

    state_ids = self._last_highlight.state_ids
    if state_ids:
      return state_ids
    return self._last_highlight.transition_ids

  def _buildTraceModeViewportFocusIds(self) -> tuple[str, ...]:
    """Return the viewport target for focus-trace mode."""

    if self._last_highlight.current_transition_ids:
      return self._last_highlight.current_transition_ids

    if self._last_highlight.current_text_ids:
      return self._last_highlight.current_text_ids

    state_ids = self._last_highlight.state_ids
    if state_ids:
      return state_ids
    return self._last_highlight.transition_ids

  def _buildHighlightFocusIds(self) -> list[str]:
    """Return all currently highlighted ids so focus mode never dims them."""

    return list(
      self._last_highlight.state_ids
      + self._last_highlight.transition_ids
      + self._last_highlight.text_ids
      + self._last_highlight.current_transition_ids
      + self._last_highlight.current_text_ids
    )

  def _normalizeFocusIds(self, related_ids: list[str]) -> tuple[str, ...]:
    """Expand focused states to their full state-owned ids and deduplicate."""

    return self._expandStateFocusIds(related_ids)

  def _expandStateFocusIds(self, related_ids: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    """Expand any included state ids to all visible ids owned by those states."""

    normalized_ids = list(related_ids)
    related_id_set = set(related_ids)
    for state in self._model.iterStates():
      state_id = state["id"]
      state_svg_id = self._rendered_svg.getStateId(state_id)
      if state_svg_id not in related_id_set:
        continue
      normalized_ids.extend(self._buildStateOwnedFocusIds(state_id))
    return tuple(dict.fromkeys(normalized_ids))

  def _buildStateFocusIds(self, related_states: tuple[HsmRelatedState, ...]) -> list[str]:
    """Resolve state and state-owned text ids for the related state set."""

    related_ids: list[str] = []

    for related_state in related_states:
      related_ids.extend(self._buildRelatedStateFocusIds(related_state))

    return related_ids

  def _buildRelatedStateFocusIds(self, related_state: HsmRelatedState) -> list[str]:
    """Resolve one related state and all its state-owned visible ids."""

    state_id = related_state.state_id
    related_ids = [self._rendered_svg.getStateId(state_id)]

    for section_name, activities in (
      ("on_entry", related_state.on_entry_activities),
      ("on_exit", related_state.on_exit_activities),
    ):
      related_ids.extend(
        self._rendered_svg.getStateHookSectionTextIds(state_id, section_name)
      )
      for activity in activities:
        related_ids.extend(
          self._rendered_svg.getStateHookActivityTextIds(
            state_id,
            section_name,
            activity,
          )
        )

    for transition in related_state.internal_transitions:
      event_id = transition["event_id"]
      internal_ids = self._rendered_svg.getInternalTransitionIds(state_id, event_id)
      related_ids.extend(internal_ids)
      related_ids.extend(
        self._rendered_svg.getInternalTransitionSectionTextIds(state_id, event_id)
      )
      for transition_id in internal_ids:
        related_ids.extend(
          self._rendered_svg.getInternalTransitionEventTextIds(transition_id)
        )
        for activity in transition.get("activities", []):
          related_ids.extend(
            self._rendered_svg.getInternalTransitionActivityTextIds(
              transition_id,
              activity,
            )
          )

    return related_ids

  def _buildStateOwnedFocusIds(self, state_id: str) -> list[str]:
    """Resolve one state and its own visible ids for transition focus."""

    return self._buildRelatedStateFocusIds(
      HsmRelatedState(
        state_id=state_id,
        on_entry_activities=tuple(self._model.getStateOnEntry(state_id)),
        on_exit_activities=tuple(self._model.getStateOnExit(state_id)),
        internal_transitions=tuple(self._model.getStateInternalTransitions(state_id)),
      )
    )

  def _buildExternalTransitionFocusIds(
    self,
    transition: HsmExternalTransitionRelation,
  ) -> list[str]:
    """Resolve one unguarded external transition and its related ids."""

    related_ids: list[str] = []
    transition_ids = self._rendered_svg.getExternalTransitionIds(
      transition.source_state_id,
      transition.event_id,
      transition.target_state_id,
    )
    related_ids.extend(transition_ids)
    related_ids.extend(self._buildStateOwnedFocusIds(transition.source_state_id))
    related_ids.extend(self._buildStateOwnedFocusIds(transition.target_state_id))
    for transition_id in transition_ids:
      related_ids.extend(
        self._rendered_svg.getExternalTransitionLabelTextIds(transition_id)
      )
      for activity in transition.activities:
        related_ids.extend(
          self._rendered_svg.getExternalTransitionActivityTextIds(
            transition_id,
            activity,
          )
        )
    return related_ids

  def _buildGuardedBranchFocusIds(
    self,
    branch: HsmGuardedTransitionBranchRelation,
  ) -> list[str]:
    """Resolve one guarded branch relation and its related ids."""

    related_ids: list[str] = []
    guarded_ids = self._rendered_svg.getGuardedTransitionIds(
      branch.source_state_id,
      branch.event_id,
    )
    guard_node_ids = self._rendered_svg.getGuardNodeIds(
      branch.source_state_id,
      branch.event_id,
    )
    branch_ids = self._rendered_svg.getGuardBranchIds(
      branch.source_state_id,
      branch.event_id,
      outcome=branch.guard_result,
      target_state_id=branch.target_state_id,
    )
    related_ids.extend(guarded_ids)
    related_ids.extend(guard_node_ids)
    related_ids.extend(branch_ids)
    related_ids.extend(self._buildStateOwnedFocusIds(branch.source_state_id))
    related_ids.extend(self._buildStateOwnedFocusIds(branch.target_state_id))

    for guarded_id in guarded_ids:
      related_ids.extend(
        self._rendered_svg.getExternalTransitionLabelTextIds(guarded_id)
      )
      for activity in branch.transition_activities:
        related_ids.extend(
          self._rendered_svg.getExternalTransitionActivityTextIds(
            guarded_id,
            activity,
          )
        )

    for branch_id in branch_ids:
      related_ids.extend(
        self._rendered_svg.getExternalTransitionLabelTextIds(branch_id)
      )
      for activity in branch.branch_activities:
        related_ids.extend(
          self._rendered_svg.getExternalTransitionActivityTextIds(
            branch_id,
            activity,
          )
        )

    return related_ids

  def _buildStateHighlightIds(self) -> tuple[str, ...]:
    """Return the highlight ids for the current active state."""

    if self._isPendingInitialTracePreviewMode():
      return (self._rendered_svg.getRootInitialTransitionSourceId(),)

    state_id = self._getEffectiveFocusStateId()
    if state_id is None:
      return ()
    return (self._rendered_svg.getStateId(state_id),)

  def _getEffectiveFocusStateId(self) -> str | None:
    """Return the state id used for focus while step execution is in progress."""

    state_id = self._runtime.getState()["id"]
    if state_id is not None:
      return state_id

    execution_log = self._getExecutionLog()
    if not self._runtime.hasPendingExecution() or not execution_log:
      return None

    trace = execution_log[-1]
    if trace["event"]["event_id"] is not None:
      return None

    if not trace["entries"]:
      return None

    for entry in reversed(trace["entries"]):
      source_state_id = entry.get("source_state_id")
      if source_state_id is not None:
        return source_state_id
      target_state_id = entry.get("target_state_id")
      if target_state_id is not None:
        return target_state_id

    return self._model.getRootInitialTargetId()

  def _getTraceStateIds(self, trace: HsmRuntimeTrace) -> set[str]:
    """Return the set of states touched structurally by one runtime trace."""

    state_ids: set[str] = set()
    for entry in trace["entries"]:
      source_state_id = entry.get("source_state_id")
      if source_state_id is not None:
        state_ids.add(source_state_id)
      target_state_id = entry.get("target_state_id")
      if target_state_id is not None:
        state_ids.add(target_state_id)
    return state_ids

  def _getPendingTraceStateIds(self) -> set[str]:
    """Return states semantically owned by the next pending debugger step."""

    next_step = self._getNextStep()
    if next_step is None:
      return set()

    state_ids: set[str] = set()
    if next_step["kind"] in {
      "on_entry",
      "on_exit",
      "internal_transition",
      "pending_guard_condition",
      "guarded_transition",
    }:
      source_state_id = next_step["source_state_id"]
      if source_state_id is not None:
        state_ids.add(source_state_id)
      return state_ids

    if next_step["kind"] == "change_active_state":
      state_ids.add(next_step["target_state_id"])
      return state_ids

    if next_step["kind"] in {"external_transition", "guard_branch_transition"}:
      source_state_id = next_step["source_state_id"]
      target_state_id = next_step["target_state_id"]
      if source_state_id is not None:
        state_ids.add(source_state_id)
      if target_state_id is not None:
        state_ids.add(target_state_id)
      return state_ids

    if next_step["kind"] == "initial_transition":
      source_state_id = next_step["source_state_id"]
      if source_state_id is not None:
        state_ids.add(source_state_id)

    return state_ids

  def _isPendingInitialTracePreviewMode(self) -> bool:
    """Return whether the runtime is paused before the first init step executes."""

    execution_log = self._getExecutionLog()
    return (
      self._runtime.isPaused()
      and self._runtime.hasPendingExecution()
      and bool(execution_log)
      and execution_log[-1]["event"]["event_id"] is None
    )

  def _buildTraceTransitionIds(
    self,
    trace: HsmRuntimeTrace,
  ) -> tuple[str, ...]:
    """Resolve structural transition ids from one completed runtime trace."""

    event_id = trace["event"]["event_id"]
    resolved_ids: list[str] = []

    for entry in trace["entries"]:
      if entry["kind"] == "initial_transition":
        source_state_id = entry["source_state_id"]
        if source_state_id is None:
          resolved_ids.append(self._rendered_svg.getRootInitialTransitionId())
        else:
          resolved_ids.append(
            self._rendered_svg.getInitialTransitionId(source_state_id)
          )
        continue

      if event_id is None:
        continue

      if entry["kind"] == "internal_transition":
        resolved_ids.extend(
          self._rendered_svg.getInternalTransitionIds(
            entry["source_state_id"],
            event_id,
          )
        )
        continue

      if entry["kind"] == "guard_condition":
        source_state_id = entry["source_state_id"]
        resolved_ids.extend(
          self._rendered_svg.getGuardNodeIds(source_state_id, event_id)
        )
        continue

      if entry["kind"] == "guarded_transition":
        resolved_ids.extend(
          self._getGuardedTransitionIds(entry["source_state_id"], event_id)
        )
        continue

      if entry["kind"] == "guard_branch_transition":
        resolved_ids.extend(
          self._rendered_svg.getGuardBranchIds(
            entry["source_state_id"],
            event_id,
            outcome=entry["result"],
            target_state_id=entry["target_state_id"],
          )
        )
        continue

      if entry["kind"] == "external_transition":
        resolved_ids.extend(
          self._rendered_svg.getExternalTransitionIds(
            entry["source_state_id"],
            event_id,
            entry["target_state_id"],
          )
        )
    return tuple(resolved_ids)

  def _buildTraceTextIds(
    self,
    trace: HsmRuntimeTrace,
    transition_ids: list[str],
  ) -> tuple[str, ...]:
    """Resolve the text fragment ids associated with the latest trace."""

    event_id = trace["event"]["event_id"]
    resolved_ids: list[str] = []

    for transition_id in transition_ids:
      resolved_ids.extend(
        self._rendered_svg.getInitialTransitionLabelTextIds(transition_id)
      )
      resolved_ids.extend(
        self._rendered_svg.getExternalTransitionLabelTextIds(transition_id)
      )

    for entry in trace["entries"]:
      if entry["kind"] in {"on_entry", "on_exit"}:
        source_state_id = entry["source_state_id"]
        resolved_ids.extend(
          self._rendered_svg.getStateHookSectionTextIds(
            source_state_id,
            entry["kind"],
          )
        )
        resolved_ids.extend(
          self._rendered_svg.getStateHookActivityTextIds(
            source_state_id,
            entry["kind"],
            entry["activity"],
          )
        )
        continue

      if event_id is None:
        if entry["kind"] != "initial_transition" or entry["activity"] is None:
          continue
        transition_id = self._rendered_svg.getRootInitialTransitionId()
        if entry["source_state_id"] is not None:
          transition_id = self._rendered_svg.getInitialTransitionId(entry["source_state_id"])
        resolved_ids.extend(
          self._rendered_svg.getInitialTransitionActivityTextIds(
            transition_id,
            entry["activity"],
          )
        )
        continue

      if entry["kind"] == "initial_transition":
        if entry["activity"] is None:
          continue
        transition_id = self._rendered_svg.getInitialTransitionId(entry["source_state_id"])
        resolved_ids.extend(
          self._rendered_svg.getInitialTransitionActivityTextIds(
            transition_id,
            entry["activity"],
          )
        )
        continue

      if entry["kind"] == "internal_transition":
        source_state_id = entry["source_state_id"]
        transition_ids_for_entry = self._rendered_svg.getInternalTransitionIds(
          source_state_id,
          event_id,
        )
        if entry["activity"] is None:
          for transition_id in transition_ids_for_entry:
            resolved_ids.extend(
              self._rendered_svg.getInternalTransitionSectionTextIds(
                source_state_id,
                event_id,
              )
            )
            resolved_ids.extend(
              self._rendered_svg.getInternalTransitionEventTextIds(
                transition_id,
              )
            )
          continue
        for transition_id in transition_ids_for_entry:
          resolved_ids.extend(
            self._rendered_svg.getInternalTransitionActivityTextIds(
              transition_id,
              entry["activity"],
            )
          )
        continue

      if entry["kind"] == "guard_condition":
        source_state_id = entry["source_state_id"]
        resolved_ids.extend(
          self._rendered_svg.getGuardNodeTextIds(source_state_id, event_id)
        )
        continue

      if entry["kind"] == "guard_branch_transition":
        if entry["activity"] is None:
          continue
        branch_ids = self._rendered_svg.getGuardBranchIds(
          entry["source_state_id"],
          event_id,
          outcome=entry["result"],
          target_state_id=entry["target_state_id"],
        )
        for branch_id in branch_ids:
          resolved_ids.extend(
            self._rendered_svg.getExternalTransitionActivityTextIds(
              branch_id,
              entry["activity"],
            )
          )
        continue

      if entry["kind"] != "external_transition":
        if entry["kind"] != "guarded_transition":
          continue

      if entry["activity"] is None:
        continue
      if entry["kind"] == "guarded_transition":
        transition_ids_for_entry = self._getGuardedTransitionIds(
          entry["source_state_id"],
          event_id,
        )
      else:
        transition_ids_for_entry = self._rendered_svg.getExternalTransitionIds(
          entry["source_state_id"],
          event_id,
          entry["target_state_id"],
        )
      for transition_id in transition_ids_for_entry:
        resolved_ids.extend(
          self._rendered_svg.getExternalTransitionActivityTextIds(
            transition_id,
            entry["activity"],
          )
        )
    return tuple(resolved_ids)

  def _buildCurrentEntryHighlightIds(
    self,
    current_entry: HsmRuntimePendingExecutionTypeAlias,
  ) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Resolve the live debugger emphasis for the next pending entry."""

    event_id = self._getPendingEventId()

    if current_entry["kind"] == "initial_transition":
      source_state_id = current_entry["source_state_id"]
      transition_ids = (
        (
          self._rendered_svg.getRootInitialTransitionId(),
          self._rendered_svg.getRootInitialTransitionSourceId(),
        )
        if source_state_id is None
        else (
          self._rendered_svg.getInitialTransitionId(source_state_id),
          self._rendered_svg.getInitialTransitionSourceId(source_state_id),
        )
      )
      if current_entry["activity"] is None:
        return transition_ids, ()
      return transition_ids, (
        self._rendered_svg.getInitialTransitionLabelTextIds(transition_ids[0])
        + self._rendered_svg.getInitialTransitionActivityTextIds(
          transition_ids[0],
          current_entry["activity"],
        )
      )

    if current_entry["kind"] == "internal_transition" and event_id is not None:
      transition_ids = self._rendered_svg.getInternalTransitionIds(
        current_entry["source_state_id"],
        event_id,
      )
      resolved_ids: list[str] = []
      for transition_id in transition_ids:
        resolved_ids.extend(
          self._rendered_svg.getInternalTransitionSectionTextIds(
            current_entry["source_state_id"],
            event_id,
          )
        )
        resolved_ids.extend(
          self._rendered_svg.getInternalTransitionEventTextIds(transition_id)
        )
        if current_entry["activity"] is not None:
          resolved_ids.extend(
            self._rendered_svg.getInternalTransitionActivityTextIds(
              transition_id,
              current_entry["activity"],
            )
          )
      return transition_ids, tuple(resolved_ids)

    if current_entry["kind"] == "guarded_transition" and event_id is not None:
      transition_ids = self._getGuardedTransitionIds(
        current_entry["source_state_id"],
        event_id,
      )
      resolved_ids: list[str] = []
      for transition_id in transition_ids:
        resolved_ids.extend(
          self._rendered_svg.getExternalTransitionLabelTextIds(transition_id)
        )
        if current_entry["activity"] is not None:
          resolved_ids.extend(
            self._rendered_svg.getExternalTransitionActivityTextIds(
              transition_id,
              current_entry["activity"],
            )
          )
      return transition_ids, tuple(resolved_ids)

    if current_entry["kind"] == "external_transition" and event_id is not None:
      transition_ids = self._rendered_svg.getExternalTransitionIds(
        current_entry["source_state_id"],
        event_id,
        current_entry["target_state_id"],
      )
      resolved_ids: list[str] = []
      for transition_id in transition_ids:
        resolved_ids.extend(
          self._rendered_svg.getExternalTransitionLabelTextIds(transition_id)
        )
        if current_entry["activity"] is not None:
          resolved_ids.extend(
            self._rendered_svg.getExternalTransitionActivityTextIds(
              transition_id,
              current_entry["activity"],
            )
          )
      return transition_ids, tuple(resolved_ids)

    if current_entry["kind"] == "guard_branch_transition" and event_id is not None:
      branch_ids = self._rendered_svg.getGuardBranchIds(
        current_entry["source_state_id"],
        event_id,
        outcome=current_entry["result"],
        target_state_id=current_entry["target_state_id"],
      )
      resolved_ids: list[str] = []
      for branch_id in branch_ids:
        resolved_ids.extend(
          self._rendered_svg.getExternalTransitionLabelTextIds(branch_id)
        )
        if current_entry["activity"] is not None:
          resolved_ids.extend(
            self._rendered_svg.getExternalTransitionActivityTextIds(
              branch_id,
              current_entry["activity"],
            )
          )
      return branch_ids, tuple(resolved_ids)

    if current_entry["kind"] == "pending_guard_condition" and event_id is not None:
      return (
        self._rendered_svg.getGuardNodeIds(current_entry["source_state_id"], event_id),
        self._rendered_svg.getGuardNodeTextIds(current_entry["source_state_id"], event_id),
      )

    if current_entry["kind"] in {"on_entry", "on_exit"}:
      return (), (
        self._rendered_svg.getStateHookSectionTextIds(
          current_entry["source_state_id"],
          current_entry["kind"],
        )
        + self._rendered_svg.getStateHookActivityTextIds(
          current_entry["source_state_id"],
          current_entry["kind"],
          current_entry["activity"],
        )
      )

    return (), ()

  def _getPendingEventId(self) -> str | None:
    """Return the event id for the currently pending trace, if any."""

    execution_log = self._getExecutionLog()
    if not self._runtime.hasPendingExecution() or not execution_log:
      return None
    return execution_log[-1]["event"]["event_id"]

  def _getGuardedTransitionIds(
    self,
    source_state_id: str,
    event_id: str,
  ) -> tuple[str, ...]:
    """Return guarded transition ids when that state-event pair is rendered."""

    try:
      return self._rendered_svg.getGuardedTransitionIds(source_state_id, event_id)
    except KeyError:
      return ()

  def _requireDeclaredEventId(self, event_id: str) -> None:
    """Reject one event id that is not declared by the current model."""

    self._model.getEventById(event_id)

  def _requireDeclaredVariableId(self, variable_id: str) -> None:
    """Reject one variable id that is not declared by the current context."""

    if self._context is None:
      raise KeyError(f"Unknown variable_id '{variable_id}'.")
    self._context.getVariableByName(variable_id)


class HsmProjectViewerServerController(HsmViewerServerController):
  """HSM viewer controller backed by a multi-model project registry."""

  def __init__(self, registry: ProjectRegistry) -> None:
    """Initialize the controller from one loaded project registry."""

    entrypoint_model = registry.getEntrypointModel()
    if not isinstance(entrypoint_model, HsmModel):
      raise TypeError("HSM project viewer requires an HSM entrypoint model.")

    self._registry = registry
    self._rendered_svgs = self._renderProjectModels(registry)
    super().__init__(entrypoint_model, registry.getContext())

  def getModelSvgText(self, model_id: str) -> str:
    """Return the rendered SVG document for one project model id."""

    try:
      return self._rendered_svgs[model_id].getSvgText()
    except KeyError as error:
      raise KeyError(f"Unknown model_id '{model_id}'.") from error

  def _getViewerModels(self) -> tuple[dict[str, object], ...]:
    """Return executable project models available to the viewer session."""

    entrypoint_id = self._model.getDocumentId()
    return tuple(
      {
        "model_id": model.getDocumentId(),
        "kind": "hsm" if isinstance(model, HsmModel) else "activity",
        "svg_url": f"/artifacts/models/{model.getDocumentId()}/diagram.svg",
        "is_entrypoint": model.getDocumentId() == entrypoint_id,
      }
      for model in self._registry.iterExecutableModels()
    )

  def _getActiveModelId(self) -> str:
    """Return the model id currently emphasized by this controller."""

    return self._model.getDocumentId()

  def _buildRuntime(self) -> Runtime:
    """Create and initialize one fresh runtime from the project registry."""

    runtime = Runtime()
    runtime.init(self._registry)
    return runtime

  def _renderProjectModels(self, registry: ProjectRegistry) -> dict[str, Any]:
    """Render every executable project model by document id."""

    rendered_svgs: dict[str, Any] = {}
    for model in registry.iterExecutableModels():
      model_id = model.getDocumentId()
      if isinstance(model, HsmModel):
        rendered = HsmRender()
      elif isinstance(model, ActivityModel):
        rendered = ActivityRender()
      else:
        continue
      rendered.render(model)
      rendered_svgs[model_id] = rendered
    return rendered_svgs


def startHsmViewerServer(
  model: HsmModel,
  *,
  context: ContextModel | None = None,
  host: str = "127.0.0.1",
  port: int = 0,
) -> RunningViewerServer:
  """Start one local HSM viewer HTTP server for the given model."""

  return startViewerServer(
    HsmViewerServerController(model, context),
    host=host,
    port=port,
  )


def startHsmProjectViewerServer(
  registry: ProjectRegistry,
  *,
  host: str = "127.0.0.1",
  port: int = 0,
) -> RunningViewerServer:
  """Start one local HSM viewer HTTP server for a loaded project."""

  return startViewerServer(
    HsmProjectViewerServerController(registry),
    host=host,
    port=port,
  )


def startHsmProjectViewerServerFromProjectPath(
  project_path: str | Path,
  *,
  host: str = "127.0.0.1",
  port: int = 0,
  open_browser: bool = False,
) -> RunningViewerServer:
  """Load one project file and start the local HSM viewer server."""

  server = startHsmProjectViewerServer(
    ProjectRegistry.load(project_path),
    host=host,
    port=port,
  )
  if open_browser:
    webbrowser.open(server.base_url)
  return server


def startHsmViewerServerFromModelPath(
  model_path: str | Path,
  *,
  context_path: str | Path | None = None,
  host: str = "127.0.0.1",
  port: int = 0,
  open_browser: bool = False,
) -> RunningViewerServer:
  """Load one HSM model file and start the local viewer server."""

  server = startHsmViewerServer(
    HsmModel.loadAndValidate(model_path),
    context=(
      None
      if context_path is None
      else ContextModel.loadAndValidate(context_path)
    ),
    host=host,
    port=port,
  )
  if open_browser:
    webbrowser.open(server.base_url)
  return server


def main(argv: list[str] | None = None) -> int:
  """Start the HSM viewer server from the command line."""

  parser = argparse.ArgumentParser(description="Launch the MBSE HSM web viewer.")
  parser.add_argument("model_path")
  parser.add_argument("--context-path")
  parser.add_argument("--host", default="127.0.0.1")
  parser.add_argument("--port", default=0, type=int)
  parser.add_argument("--open-browser", action="store_true")
  args = parser.parse_args(argv)

  server = startHsmViewerServerFromModelPath(
    args.model_path,
    context_path=args.context_path,
    host=args.host,
    port=args.port,
    open_browser=args.open_browser,
  )
  print(server.base_url)
  try:
    server.waitUntilStopped()
  except KeyboardInterrupt:
    server.close()
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
