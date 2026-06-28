"""Project model discovery and document registry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypeAlias

from mbse.model.activity.activity_model import ActivityModel
from mbse.model.context.context_model import ContextModel
from mbse.model.hsm.hsm_model import HsmModel
from mbse.model.project.project_model import ProjectModel


ProjectRegistryModel: TypeAlias = HsmModel | ActivityModel | ContextModel
ProjectRegistryExecutableModel: TypeAlias = HsmModel | ActivityModel


_MODEL_TYPES = {
  "mbse-context-model-v0": ContextModel,
  "mbse-hsm-model-v0": HsmModel,
  "mbse-activity-model-v0": ActivityModel,
}


class ProjectRegistry:
  """Loaded project plus discovered MBSE models indexed by document id."""

  def __init__(
    self,
    project: ProjectModel,
    project_path: Path,
    project_root_path: Path,
    models: dict[str, ProjectRegistryModel],
    context: ContextModel | None,
  ) -> None:
    """ProjectRegistry initialization."""

    self.project = project
    self.project_path = project_path
    self.project_root_path = project_root_path
    self.models = models
    self.context = context

  @classmethod
  def load(cls, project_path: str | Path) -> ProjectRegistry:
    """Load one project file and discover MBSE models under its root."""

    resolved_project_path = Path(project_path).resolve()
    project = ProjectModel.loadAndValidate(resolved_project_path)
    project_root_path = (
      resolved_project_path.parent / project.getProjectRoot()
    ).resolve()

    models: dict[str, ProjectRegistryModel] = {}
    context: ContextModel | None = None

    for model_path in sorted(project_root_path.rglob("*.json")):
      if model_path.resolve() == resolved_project_path:
        continue

      payload = cls._loadJson(model_path)
      schema_version = payload.get("schema_version")
      if not isinstance(schema_version, str):
        continue

      model_type = _MODEL_TYPES.get(schema_version)
      if model_type is None:
        continue

      model = model_type.loadAndValidate(model_path)
      document_id = model.getDocumentId()
      if document_id in models:
        raise ValueError(f"Duplicate document_id '{document_id}'.")

      if isinstance(model, ContextModel):
        if context is not None:
          raise ValueError("Project contains more than one ContextModel.")
        context = model

      models[document_id] = model

    entrypoint = project.getEntrypoint()
    if entrypoint not in models:
      raise KeyError(f"Unknown entrypoint model_id '{entrypoint}'.")

    if isinstance(models[entrypoint], ContextModel):
      raise TypeError("Project entrypoint must reference an executable model.")

    return cls(
      project,
      resolved_project_path,
      project_root_path,
      models,
      context,
    )

  def getProject(self) -> ProjectModel:
    """Return the loaded project model."""

    return self.project

  def getProjectPath(self) -> Path:
    """Return the resolved project file path."""

    return self.project_path

  def getProjectRootPath(self) -> Path:
    """Return the resolved project root path."""

    return self.project_root_path

  def getContext(self) -> ContextModel | None:
    """Return the discovered context model, if any."""

    return self.context

  def getModel(self, model_id: str) -> ProjectRegistryModel:
    """Return one discovered model by document id."""

    try:
      return self.models[model_id]
    except KeyError as error:
      raise KeyError(f"Unknown model_id '{model_id}'.") from error

  def getEntrypointModel(self) -> ProjectRegistryExecutableModel:
    """Return the executable model selected as project entrypoint."""

    model = self.getModel(self.project.getEntrypoint())
    if isinstance(model, ContextModel):
      raise TypeError("Project entrypoint must reference an executable model.")
    return model

  def iterExecutableModels(self) -> tuple[ProjectRegistryExecutableModel, ...]:
    """Return discovered executable models in deterministic document-id order."""

    return tuple(
      model
      for _model_id, model in sorted(self.models.items())
      if not isinstance(model, ContextModel)
    )

  def getHsmModel(self, model_id: str) -> HsmModel:
    """Return one discovered HSM model by document id."""

    model = self.getModel(model_id)
    if not isinstance(model, HsmModel):
      raise TypeError(f"Model_id '{model_id}' is not an HSM model.")
    return model

  def getActivityModel(self, model_id: str) -> ActivityModel:
    """Return one discovered Activity model by document id."""

    model = self.getModel(model_id)
    if not isinstance(model, ActivityModel):
      raise TypeError(f"Model_id '{model_id}' is not an Activity model.")
    return model

  @staticmethod
  def _loadJson(model_path: Path) -> dict[str, object]:
    """Load one JSON object from disk."""

    with model_path.open("r", encoding="utf-8") as model_file:
      payload = json.load(model_file)

    if not isinstance(payload, dict):
      raise ValueError(
        f"Project JSON document '{model_path}' must be an object."
      )

    return payload
