"""Minimal activity JSON model loading, validation, and query API."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from mbse.model.mbse_model import MbseModel


_ACTIVITY_MODEL_SCHEMA_PATH = Path(__file__).with_name("activity_model.json")


class ActivityModel(MbseModel):
  """Authored activity model plus read-only structural queries."""

  _SCHEMA_PATH = _ACTIVITY_MODEL_SCHEMA_PATH

  def getInitial(self) -> dict[str, Any]:
    """Return the authored initial entry point."""

    return self.document["initial"]

  def getInitialTargetId(self) -> str:
    """Return the initial target id."""

    return self.getInitial()["target_id"]

  def getActions(self) -> list[dict[str, Any]]:
    """Return the authored action declarations."""

    return self.document["actions"]

  def getActionById(self, action_id: str) -> dict[str, Any]:
    """Return one action by id."""

    for action in self.getActions():
      if action["id"] == action_id:
        return action

    raise KeyError(f"Unknown action_id '{action_id}'.")

  def getActionLabel(self, action_id: str) -> str:
    """Return the authored label for one action."""

    return self.getActionById(action_id)["label"]

  def getDecisions(self) -> list[dict[str, Any]]:
    """Return the authored decision declarations."""

    return self.document["decisions"]

  def getDecisionById(self, decision_id: str) -> dict[str, Any]:
    """Return one decision by id."""

    for decision in self.getDecisions():
      if decision["id"] == decision_id:
        return decision

    raise KeyError(f"Unknown decision_id '{decision_id}'.")

  def getDecisionLabel(self, decision_id: str) -> str:
    """Return the authored label for one decision."""

    return self.getDecisionById(decision_id)["label"]

  def getFinals(self) -> list[dict[str, Any]]:
    """Return the authored final declarations."""

    return self.document["finals"]

  def getFinalById(self, final_id: str) -> dict[str, Any]:
    """Return one final by id."""

    for final in self.getFinals():
      if final["id"] == final_id:
        return final

    raise KeyError(f"Unknown final_id '{final_id}'.")

  def getFinalLabel(self, final_id: str) -> str:
    """Return the authored label for one final."""

    return self.getFinalById(final_id)["label"]
