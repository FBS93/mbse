"""Minimal project JSON model loading, validation, and query helpers."""

from __future__ import annotations

from pathlib import Path

from mbse.model.mbse_model import MbseModel


_PROJECT_MODEL_SCHEMA_PATH = Path(__file__).with_name("project_model.json")


class ProjectModel(MbseModel):
  """Authored project model plus read-only project queries."""

  _SCHEMA_PATH = _PROJECT_MODEL_SCHEMA_PATH

  def getProjectRoot(self) -> str:
    """Return the authored project root path."""

    return self.document["project_root"]

  def getEntrypoint(self) -> str:
    """Return the document id of the initial execution model."""

    return self.document["entrypoint"]
