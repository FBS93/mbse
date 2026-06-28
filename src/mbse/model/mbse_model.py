"""Shared MBSE model loading and validation helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from typing import ClassVar
from typing import Self

from jsonschema import Draft202012Validator
from referencing import Registry
from referencing import Resource


_MBSE_MODEL_SCHEMA_PATH = Path(__file__).with_name("mbse_model.json")


class MbseModel:
  """Authored MBSE model plus schema-backed loading and validation."""

  _SCHEMA_PATH: ClassVar[Path]

  def __init__(self, model: dict[str, Any]) -> None:
    """MbseModel initialization."""

    self.document = model

  @classmethod
  def load(cls, modelPath: str | Path) -> Self:
    """Load an MBSE model JSON file."""

    with Path(modelPath).open("r", encoding="utf-8") as modelFile:
      return cls(json.load(modelFile))

  @classmethod
  def validate(cls, model: dict[str, Any]) -> None:
    """Validate a model dictionary against the model JSON Schema."""

    with cls._SCHEMA_PATH.open("r", encoding="utf-8") as schemaFile:
      schema = json.load(schemaFile)
    with _MBSE_MODEL_SCHEMA_PATH.open("r", encoding="utf-8") as schemaFile:
      mbse_schema = json.load(schemaFile)

    registry = Registry().with_resource(
      mbse_schema["$id"],
      Resource.from_contents(mbse_schema),
    )
    Draft202012Validator(schema, registry=registry).validate(model)

  @classmethod
  def loadAndValidate(cls, modelPath: str | Path) -> Self:
    """Load and validate an MBSE model JSON file."""

    model = cls.load(modelPath)
    cls.validate(model.document)
    return model

  def getDocumentId(self) -> str:
    """Return the authored document id."""

    return self.document["document_id"]

  def getSchemaVersion(self) -> str:
    """Return the authored schema version."""

    return self.document["schema_version"]
