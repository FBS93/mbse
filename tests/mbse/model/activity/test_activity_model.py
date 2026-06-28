from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from mbse.model.activity.activity_model import ActivityModel


FIXTURE_PATH = (
  Path(__file__).resolve().parents[3]
  / "reference_model"
  / "activity"
  / "reference_activity_model.json"
)


def _load_fixture() -> dict[str, object]:
  with FIXTURE_PATH.open("r", encoding="utf-8") as fixture_file:
    return json.load(fixture_file)


def _write_model(tmp_path: Path, model: dict[str, object]) -> Path:
  model_path = tmp_path / "model.json"
  model_path.write_text(json.dumps(model), encoding="utf-8")
  return model_path


def test_load_and_validate_activity_model() -> None:
  model = ActivityModel.loadAndValidate(FIXTURE_PATH)

  assert model.getDocumentId() == "reference_activity"
  assert model.getSchemaVersion() == "mbse-activity-model-v0"
  assert model.getInitialTargetId() == "check_ready"


def test_activity_model_exposes_expected_structure_queries() -> None:
  model = ActivityModel.loadAndValidate(FIXTURE_PATH)

  assert model.getInitial() == {"target_id": "check_ready"}
  assert [action["id"] for action in model.getActions()] == ["prepare_output"]
  assert [decision["id"] for decision in model.getDecisions()] == ["check_ready"]
  assert [final["id"] for final in model.getFinals()] == ["done", "skipped"]

  assert model.getActionById("prepare_output") == {
    "id": "prepare_output",
    "label": "Prepare Output",
    "executable": {
      "kind": "action_language",
      "module": "tests.reference_model.activity.reference_activity_executables",
      "name": "prepare_output",
    },
    "transition": {
      "target_id": "done",
    },
  }
  assert model.getDecisionById("check_ready")["true_transition"] == {
    "target_id": "prepare_output"
  }
  assert model.getDecisionById("check_ready")["false_transition"] == {
    "target_id": "skipped"
  }
  assert model.getFinalById("skipped") == {
    "id": "skipped",
    "label": "Skipped",
  }


def test_activity_model_exposes_labels() -> None:
  model = ActivityModel.loadAndValidate(FIXTURE_PATH)

  assert model.getActionLabel("prepare_output") == "Prepare Output"
  assert model.getDecisionLabel("check_ready") == "Check Ready"
  assert model.getFinalLabel("done") == "Done"


def test_activity_model_raises_for_unknown_ids() -> None:
  model = ActivityModel.loadAndValidate(FIXTURE_PATH)

  with pytest.raises(KeyError, match="Unknown action_id 'missing'."):
    model.getActionById("missing")

  with pytest.raises(KeyError, match="Unknown decision_id 'missing'."):
    model.getDecisionById("missing")

  with pytest.raises(KeyError, match="Unknown final_id 'missing'."):
    model.getFinalById("missing")


def test_activity_model_rejects_invalid_schema_payload(tmp_path: Path) -> None:
  invalid_model = _load_fixture()
  invalid_model.pop("document_id")
  invalid_path = tmp_path / "invalid_reference_activity.json"
  invalid_path.write_text(json.dumps(invalid_model), encoding="utf-8")

  with pytest.raises(ValidationError):
    ActivityModel.loadAndValidate(invalid_path)
