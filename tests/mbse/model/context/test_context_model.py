from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from mbse.model.context.context_model import ContextModel


FIXTURE_PATH = (
  Path(__file__).resolve().parents[3]
  / "reference_model"
  / "context"
  / "reference_context_model.json"
)


def _load_fixture() -> dict[str, object]:
  with FIXTURE_PATH.open("r", encoding="utf-8") as fixture_file:
    return json.load(fixture_file)


def _write_model(tmp_path: Path, model: dict[str, object]) -> Path:
  model_path = tmp_path / "model.json"
  model_path.write_text(json.dumps(model), encoding="utf-8")
  return model_path


def test_load_and_validate_context_model() -> None:
  model = ContextModel.loadAndValidate(FIXTURE_PATH)

  assert model.getDocumentId() == "reference_context"
  assert model.getSchemaVersion() == "mbse-context-model-v0"
  assert model.getEnumValues("transition_mode") == ["normal", "forced"]
  assert model.getVariableDefaultValue("last_ping_value") == 0


def test_context_model_exposes_expected_structure_queries() -> None:
  model = ContextModel.loadAndValidate(FIXTURE_PATH)

  assert model.getEnums() == [
    {
      "id": "transition_mode",
      "values": ["normal", "forced"],
    }
  ]
  assert model.getVariableByName("current_mode") == {
    "name": "current_mode",
    "type": "enum",
    "enum_id": "transition_mode",
    "default_value": "normal",
  }


def test_context_model_raises_for_unknown_ids() -> None:
  model = ContextModel.loadAndValidate(FIXTURE_PATH)

  with pytest.raises(KeyError, match="Unknown enum_id 'missing'."):
    model.getEnumById("missing")

  with pytest.raises(KeyError, match="Unknown variable name 'missing'."):
    model.getVariableByName("missing")


def test_context_model_rejects_invalid_schema_payload(tmp_path: Path) -> None:
  invalid_model = _load_fixture()
  invalid_model.pop("document_id")

  with pytest.raises(ValidationError):
    ContextModel.loadAndValidate(_write_model(tmp_path, invalid_model))


def test_context_model_rejects_extra_variable_properties(tmp_path: Path) -> None:
  invalid_model = _load_fixture()
  invalid_model["variables"][0]["unexpected"] = True

  with pytest.raises(ValidationError):
    ContextModel.loadAndValidate(_write_model(tmp_path, invalid_model))
