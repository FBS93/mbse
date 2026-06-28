from __future__ import annotations

import json
from pathlib import Path

import pytest

from mbse.model.project.project_registry import ProjectRegistry
from mbse.runtime.runtime import Runtime


def _write_json(path: Path, payload: dict[str, object]) -> Path:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(json.dumps(payload), encoding="utf-8")
  return path


def _project_payload(entrypoint: str) -> dict[str, object]:
  return {
    "schema_version": "mbse-project-model-v0",
    "document_id": "test_project",
    "project_root": "models",
    "entrypoint": entrypoint,
  }


def _context_payload() -> dict[str, object]:
  return {
    "schema_version": "mbse-context-model-v0",
    "document_id": "shared_context",
    "enums": [],
    "variables": [
      {
        "name": "counter",
        "type": "signed",
        "min": -10,
        "max": 10,
        "default_value": 1,
      }
    ],
  }


def _model_call_context_payload() -> dict[str, object]:
  return {
    "schema_version": "mbse-context-model-v0",
    "document_id": "shared_context",
    "enums": [],
    "variables": [
      {
        "name": "output_prepared",
        "type": "bool",
        "default_value": False,
      },
      {
        "name": "result",
        "type": "bool",
        "default_value": False,
      },
    ],
  }


def _hsm_payload() -> dict[str, object]:
  return {
    "schema_version": "mbse-hsm-model-v0",
    "document_id": "main_hsm",
    "events": [{"id": "go", "label": "Go"}],
    "initial_transition": {"target_id": "idle"},
    "states": [
      {
        "id": "idle",
        "label": "Idle",
        "external_transitions": [
          {
            "event_id": "go",
            "target_id": "done",
          }
        ],
      },
      {"id": "done", "label": "Done"},
    ],
  }


def _hsm_model_activity_payload() -> dict[str, object]:
  return {
    "schema_version": "mbse-hsm-model-v0",
    "document_id": "main_hsm",
    "events": [{"id": "go", "label": "Go"}],
    "initial_transition": {"target_id": "idle"},
    "states": [
      {
        "id": "idle",
        "label": "Idle",
        "external_transitions": [
          {
            "event_id": "go",
            "target_id": "done",
            "activities": [{"kind": "model", "model_id": "child_activity"}],
          }
        ],
      },
      {"id": "done", "label": "Done"},
    ],
  }


def _hsm_model_guard_payload() -> dict[str, object]:
  return {
    "schema_version": "mbse-hsm-model-v0",
    "document_id": "main_hsm",
    "events": [{"id": "go", "label": "Go"}],
    "initial_transition": {"target_id": "idle"},
    "states": [
      {
        "id": "idle",
        "label": "Idle",
        "external_transitions": [
          {
            "event_id": "go",
            "guard_condition": {
              "guard_activity": {"kind": "model", "model_id": "child_activity"},
              "true_branch": {"target_id": "accepted"},
              "false_branch": {"target_id": "rejected"},
            },
          }
        ],
      },
      {"id": "accepted", "label": "Accepted"},
      {"id": "rejected", "label": "Rejected"},
    ],
  }


def _activity_payload() -> dict[str, object]:
  return {
    "schema_version": "mbse-activity-model-v0",
    "document_id": "main_activity",
    "initial": {"target_id": "done"},
    "actions": [],
    "decisions": [],
    "finals": [{"id": "done", "label": "Done"}],
  }


def _activity_action_model_call_payload() -> dict[str, object]:
  return {
    "schema_version": "mbse-activity-model-v0",
    "document_id": "main_activity",
    "initial": {"target_id": "call_child"},
    "actions": [
      {
        "id": "call_child",
        "label": "Call Child",
        "executable": {"kind": "model", "model_id": "child_activity"},
        "transition": {"target_id": "done"},
      }
    ],
    "decisions": [],
    "finals": [{"id": "done", "label": "Done"}],
  }


def _activity_decision_model_call_payload() -> dict[str, object]:
  return {
    "schema_version": "mbse-activity-model-v0",
    "document_id": "main_activity",
    "initial": {"target_id": "check_child"},
    "actions": [],
    "decisions": [
      {
        "id": "check_child",
        "label": "Check Child",
        "condition": {"kind": "model", "model_id": "child_activity"},
        "true_transition": {"target_id": "accepted"},
        "false_transition": {"target_id": "rejected"},
      }
    ],
    "finals": [
      {"id": "accepted", "label": "Accepted"},
      {"id": "rejected", "label": "Rejected"},
    ],
  }


def _child_activity_payload(function_name: str) -> dict[str, object]:
  return {
    "schema_version": "mbse-activity-model-v0",
    "document_id": "child_activity",
    "initial": {"target_id": "run"},
    "actions": [
      {
        "id": "run",
        "label": "Run",
        "executable": {
          "kind": "action_language",
          "module": "tests.reference_model.activity.reference_activity_executables",
          "name": function_name,
        },
        "transition": {"target_id": "done"},
      }
    ],
    "decisions": [],
    "finals": [{"id": "done", "label": "Done"}],
  }


def _write_project(
  tmp_path: Path,
  entrypoint: str,
  *models: dict[str, object],
) -> Path:
  project_path = _write_json(tmp_path / "project.json", _project_payload(entrypoint))
  for index, model in enumerate(models):
    _write_json(tmp_path / "models" / f"model_{index}.json", model)
  return project_path


def _init_runtime(project_path: Path) -> Runtime:
  registry = ProjectRegistry.load(project_path)
  runtime = Runtime()
  runtime.init(registry)
  return runtime


def test_runtime_wraps_hsm_next_step(tmp_path: Path) -> None:
  project_path = _write_project(
    tmp_path,
    "main_hsm",
    _context_payload(),
    _hsm_payload(),
  )

  runtime = _init_runtime(project_path)

  assert runtime.isPaused() is True
  assert runtime.getNextStep() == {
    "runtime": "hsm",
    "model_id": "main_hsm",
    "step": {
      "kind": "initial_transition",
      "source_state_id": None,
      "source_state_label": None,
      "target_state_id": "idle",
      "target_state_label": "Idle",
      "activity": None,
    },
  }


def test_runtime_wraps_hsm_execution_log(tmp_path: Path) -> None:
  project_path = _write_project(tmp_path, "main_hsm", _hsm_payload())
  runtime = _init_runtime(project_path)

  assert runtime.play() is True

  assert runtime.getExecutionLog() == [
    {
      "runtime": "hsm",
      "model_id": "main_hsm",
      "trace": {
        "event": {
          "event_id": None,
          "parameters": {},
        },
        "entries": [
          {
            "kind": "initial_transition",
            "source_state_id": None,
            "source_state_label": None,
            "target_state_id": "idle",
            "target_state_label": "Idle",
            "activity": None,
          },
          {
            "kind": "change_active_state",
            "target_state_id": "idle",
            "target_state_label": "Idle",
          },
        ],
      },
    }
  ]


def test_runtime_delegates_hsm_events(tmp_path: Path) -> None:
  project_path = _write_project(tmp_path, "main_hsm", _hsm_payload())
  runtime = _init_runtime(project_path)

  runtime.play()
  assert runtime.sendEvent("go") is True

  log = runtime.getExecutionLog()
  assert log[1]["trace"]["event"] == {
    "event_id": "go",
    "parameters": {},
  }
  assert log[1]["trace"]["entries"][-1] == {
    "kind": "change_active_state",
    "target_state_id": "done",
    "target_state_label": "Done",
  }


def test_runtime_exposes_hsm_state_and_event_queue(tmp_path: Path) -> None:
  project_path = _write_project(tmp_path, "main_hsm", _hsm_payload())
  runtime = _init_runtime(project_path)

  assert runtime.getState() == {"id": None, "label": None}
  assert runtime.getEventQueue() == []

  runtime.play()
  runtime.pause()
  runtime.sendEvent("go")

  assert runtime.getEventQueue() == []


def test_runtime_wraps_activity_next_step_and_log(tmp_path: Path) -> None:
  project_path = _write_project(
    tmp_path,
    "main_activity",
    _activity_payload(),
  )

  runtime = _init_runtime(project_path)

  assert runtime.getNextStep() == {
    "runtime": "activity",
    "model_id": "main_activity",
    "step": {
      "kind": "initial",
      "target_id": "done",
      "target_label": "Done",
      "target_type": "final",
    },
  }

  runtime.play()

  assert runtime.getExecutionLog() == [
    {
      "runtime": "activity",
      "model_id": "main_activity",
      "trace": {
        "entries": [
          {
            "kind": "initial",
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
      },
    }
  ]


def test_runtime_delegates_variables(tmp_path: Path) -> None:
  project_path = _write_project(
    tmp_path,
    "main_activity",
    _context_payload(),
    _activity_payload(),
  )
  runtime = _init_runtime(project_path)

  assert runtime.getVariable("counter") == 1

  runtime.setVariable("counter", 2)

  assert runtime.getVariable("counter") == 2


def test_runtime_executes_activity_model_action(tmp_path: Path) -> None:
  project_path = _write_project(
    tmp_path,
    "main_activity",
    _model_call_context_payload(),
    _activity_action_model_call_payload(),
    _child_activity_payload("prepare_output"),
  )
  runtime = _init_runtime(project_path)

  assert runtime.play() is True

  assert runtime.getVariable("output_prepared") is True
  assert [entry["model_id"] for entry in runtime.getExecutionLog()] == [
    "main_activity",
    "child_activity",
  ]


def test_runtime_uses_activity_model_result_for_decision(tmp_path: Path) -> None:
  project_path = _write_project(
    tmp_path,
    "main_activity",
    _model_call_context_payload(),
    _activity_decision_model_call_payload(),
    _child_activity_payload("set_result_true"),
  )
  runtime = _init_runtime(project_path)

  assert runtime.play() is True

  assert runtime.getVariable("result") is True
  parent_trace = runtime.getExecutionLog()[0]["trace"]
  assert parent_trace["entries"][1] == {
    "kind": "decision",
    "decision_id": "check_child",
    "decision_label": "Check Child",
    "condition": {"kind": "model", "model_id": "child_activity"},
    "result": True,
    "target_id": "accepted",
    "target_label": "Accepted",
    "target_type": "final",
  }


def test_runtime_executes_hsm_model_activity(tmp_path: Path) -> None:
  project_path = _write_project(
    tmp_path,
    "main_hsm",
    _model_call_context_payload(),
    _hsm_model_activity_payload(),
    _child_activity_payload("prepare_output"),
  )
  runtime = _init_runtime(project_path)

  runtime.play()
  assert runtime.sendEvent("go") is True

  assert runtime.getVariable("output_prepared") is True
  assert [entry["model_id"] for entry in runtime.getExecutionLog()] == [
    "main_hsm",
    "main_hsm",
    "child_activity",
  ]


def test_runtime_uses_activity_model_result_for_hsm_guard(tmp_path: Path) -> None:
  project_path = _write_project(
    tmp_path,
    "main_hsm",
    _model_call_context_payload(),
    _hsm_model_guard_payload(),
    _child_activity_payload("set_result_true"),
  )
  runtime = _init_runtime(project_path)

  runtime.play()
  assert runtime.sendEvent("go") is True

  assert runtime.getVariable("result") is True
  assert runtime.getState() == {"id": "accepted", "label": "Accepted"}


def test_runtime_rejects_events_for_activity_entrypoint(
  tmp_path: Path,
) -> None:
  project_path = _write_project(tmp_path, "main_activity", _activity_payload())
  runtime = _init_runtime(project_path)

  with pytest.raises(TypeError, match="Only HSM runtimes accept events."):
    runtime.sendEvent("go")

  with pytest.raises(TypeError, match="Only HSM runtimes expose state."):
    runtime.getState()

  with pytest.raises(TypeError, match="Only HSM runtimes expose an event queue."):
    runtime.getEventQueue()
