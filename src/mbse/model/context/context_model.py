"""Minimal context JSON model loading, validation, and query helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mbse.model.mbse_model import MbseModel


_CONTEXT_MODEL_SCHEMA_PATH = Path(__file__).with_name("context_model.json")


class ContextModel(MbseModel):
  """Authored context model plus read-only structural queries."""

  _SCHEMA_PATH = _CONTEXT_MODEL_SCHEMA_PATH

  def getEnums(self) -> list[dict[str, Any]]:
    """Return the authored global enum declarations."""

    return self.document.get("enums", [])

  def getEnumById(self, enum_id: str) -> dict[str, Any]:
    """Return one global enum declaration by id."""

    for enum in self.getEnums():
      if enum["id"] == enum_id:
        return enum

    raise KeyError(f"Unknown enum_id '{enum_id}'.")

  def getEnumValues(self, enum_id: str) -> list[str]:
    """Return the declared values for one global enum."""

    return self.getEnumById(enum_id)["values"]

  def getVariables(self) -> list[dict[str, Any]]:
    """Return the authored variable declarations."""

    return self.document.get("variables", [])

  def getVariableByName(self, name: str) -> dict[str, Any]:
    """Return one variable declaration by name."""

    for variable in self.getVariables():
      if variable["name"] == name:
        return variable

    raise KeyError(f"Unknown variable name '{name}'.")

  def getVariableDefaultValue(self, name: str) -> Any:
    """Return the authored default value for one variable."""

    return self.getVariableByName(name)["default_value"]
