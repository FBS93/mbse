from __future__ import annotations

from copy import deepcopy
import importlib
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from mbse.model.activity.activity_model import ActivityModel
from mbse.model.context.context_model import ContextModel
from mbse.runtime.activity.activity_runtime import ActivityRuntime


FIXTURE_PATH = (
  Path(__file__).resolve().parents[3]
  / "reference_model"
  / "activity"
  / "reference_activity_model.json"
)
CONTEXT_PATH = (
  Path(__file__).resolve().parents[3]
  / "reference_model"
  / "context"
  / "reference_context_model.json"
)


def _build_runtime() -> ActivityRuntime:
  model = ActivityModel.loadAndValidate(FIXTURE_PATH)
  context = ContextModel.loadAndValidate(CONTEXT_PATH)
  runtime = ActivityRuntime()
  runtime.setExecutableHandler(_execute_action_language)
  runtime.init(model, context)
  return runtime


def _execute_action_language(
  executable_ref: dict[str, Any],
  runtime: ActivityRuntime,
  _event: dict[str, Any] | None,
) -> Any:
  module = importlib.import_module(executable_ref["module"])
  handler = getattr(module, executable_ref["name"])
  ctx = SimpleNamespace(**runtime.variables)
  ctx.variables = runtime.variables

  result = handler(ctx)

  for name in runtime.variables:
    if hasattr(ctx, name):
      runtime.variables[name] = getattr(ctx, name)

  return result


def _traceKinds(runtime: ActivityRuntime) -> list[str]:
  return [entry["kind"] for entry in runtime.getExecutionLog()[0]["entries"]]


def test_activity_init_starts_paused_with_initial_step_planned() -> None:
  runtime = _build_runtime()

  assert runtime.isPaused() is True
  assert runtime.hasPendingExecution() is True
  assert runtime.getExecutionLog() == [{"entries": []}]
  assert runtime.getNextStep() == {
    "kind": "initial",
    "target_id": "check_ready",
    "target_label": "Check Ready",
    "target_type": "decision",
  }


def test_activity_play_executes_true_path_to_final() -> None:
  runtime = _build_runtime()

  assert runtime.play() is True

  assert runtime.hasPendingExecution() is False
  assert runtime.getVariable("output_prepared") is True
  assert _traceKinds(runtime) == ["initial", "decision", "action", "final"]
  assert runtime.getExecutionLog()[0]["entries"][-1] == {
    "kind": "final",
    "final_id": "done",
    "final_label": "Done",
  }


def test_activity_decision_false_takes_false_path_to_final() -> None:
  runtime = _build_runtime()
  runtime.setVariable("is_ready", False)

  assert runtime.play() is True

  assert runtime.hasPendingExecution() is False
  assert runtime.getVariable("output_prepared") is False
  assert _traceKinds(runtime) == ["initial", "decision", "final"]
  assert runtime.getExecutionLog()[0]["entries"][1] == {
    "kind": "decision",
    "decision_id": "check_ready",
    "decision_label": "Check Ready",
    "condition": {
      "kind": "action_language",
      "module": "tests.reference_model.activity.reference_activity_executables",
      "name": "is_ready",
    },
    "result": False,
    "target_id": "skipped",
    "target_label": "Skipped",
    "target_type": "final",
  }


def test_activity_action_executable_mutates_runtime_variable() -> None:
  runtime = _build_runtime()

  assert runtime.getVariable("output_prepared") is False

  runtime.play()

  assert runtime.getVariable("output_prepared") is True


def test_activity_decision_requires_bool_result() -> None:
  model = ActivityModel.loadAndValidate(FIXTURE_PATH)
  bad_document = deepcopy(model.document)
  bad_document["decisions"][0]["condition"] = {
    "kind": "action_language",
    "module": "tests.reference_model.activity.reference_activity_executables",
    "name": "return_not_bool",
  }
  context = ContextModel.loadAndValidate(CONTEXT_PATH)
  runtime = ActivityRuntime()
  runtime.setExecutableHandler(_execute_action_language)
  runtime.init(ActivityModel(bad_document), context)

  assert runtime.step() is True
  with pytest.raises(TypeError, match="Decision condition executable must return a bool"):
    runtime.step()


def test_activity_step_advances_step_by_step() -> None:
  runtime = _build_runtime()

  assert runtime.step() is True
  assert _traceKinds(runtime) == ["initial"]
  assert runtime.getNextStep() == {
    "kind": "pending_decision",
    "decision_id": "check_ready",
    "decision_label": "Check Ready",
    "condition": {
      "kind": "action_language",
      "module": "tests.reference_model.activity.reference_activity_executables",
      "name": "is_ready",
    },
    "true_target_id": "prepare_output",
    "true_target_label": "Prepare Output",
    "true_target_type": "action",
    "false_target_id": "skipped",
    "false_target_label": "Skipped",
    "false_target_type": "final",
    "true_branch": [
      {
        "kind": "action",
        "action_id": "prepare_output",
        "action_label": "Prepare Output",
        "executable": {
          "kind": "action_language",
          "module": "tests.reference_model.activity.reference_activity_executables",
          "name": "prepare_output",
        },
        "target_id": "done",
        "target_label": "Done",
        "target_type": "final",
      },
      {
        "kind": "final",
        "final_id": "done",
        "final_label": "Done",
      },
    ],
    "false_branch": [
      {
        "kind": "final",
        "final_id": "skipped",
        "final_label": "Skipped",
      }
    ],
  }

  assert runtime.step() is True
  assert _traceKinds(runtime) == ["initial", "decision"]
  assert runtime.getNextStep()["kind"] == "action"
  assert runtime.getVariable("output_prepared") is False

  assert runtime.step() is True
  assert _traceKinds(runtime) == ["initial", "decision", "action"]
  assert runtime.getNextStep() == {
    "kind": "final",
    "final_id": "done",
    "final_label": "Done",
  }
  assert runtime.getVariable("output_prepared") is True

  assert runtime.step() is True
  assert _traceKinds(runtime) == ["initial", "decision", "action", "final"]
  assert runtime.hasPendingExecution() is False

  assert runtime.step() is False


def test_activity_execution_log_contains_expected_sequence() -> None:
  runtime = _build_runtime()

  runtime.play()

  assert runtime.getExecutionLog() == [
    {
      "entries": [
        {
          "kind": "initial",
          "target_id": "check_ready",
          "target_label": "Check Ready",
          "target_type": "decision",
        },
        {
          "kind": "decision",
          "decision_id": "check_ready",
          "decision_label": "Check Ready",
          "condition": {
            "kind": "action_language",
            "module": "tests.reference_model.activity.reference_activity_executables",
            "name": "is_ready",
          },
          "result": True,
          "target_id": "prepare_output",
          "target_label": "Prepare Output",
          "target_type": "action",
        },
        {
          "kind": "action",
          "action_id": "prepare_output",
          "action_label": "Prepare Output",
          "executable": {
            "kind": "action_language",
            "module": "tests.reference_model.activity.reference_activity_executables",
            "name": "prepare_output",
          },
          "target_id": "done",
          "target_label": "Done",
          "target_type": "final",
        },
        {
          "kind": "final",
          "final_id": "done",
          "final_label": "Done",
        },
      ]
    }
  ]
