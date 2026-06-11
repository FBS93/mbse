from __future__ import annotations

from importlib import import_module
from pathlib import Path

from mbse.runtime import hsm
from mbse.runtime.hsm import build_hsm_runtime
from mbse.runtime.hsm import HsmExecutedActivity
from mbse.runtime.hsm import HsmRuntime
from mbse.runtime.hsm import HsmRuntimeLastEvent
from mbse.runtime.hsm import HsmRuntimeMetadata
from mbse.runtime.hsm import HsmRuntimeSnapshot
from mbse.runtime.hsm.generator.generator import GeneratedRuntime
from mbse.runtime.hsm.generator.generator import load_generated_runtime
from mbse.runtime.hsm.generator.generator import render_generated_runtime_source
from mbse.runtime.hsm.runtime_model.runtime_model_builder import derive_event_handler_slot_order
from mbse.runtime.hsm.runtime_model.runtime_model_builder import prepare_hsm_generated_runtime_view
from mbse.runtime.hsm.runtime_model.runtime_model_types import HsmGeneratedRuntimeView


def test_runtime_package_exposes_hsm_subpackage_only():
  assert hsm.__name__ == "mbse.runtime.hsm"


def test_hsm_package_limits_public_api_to_runtime_consumer_surface():
  assert hsm.__all__ == [
    "build_hsm_runtime",
    "HsmRuntime",
    "HsmRuntimeMetadata",
    "HsmRuntimeSnapshot",
    "HsmRuntimeLastEvent",
    "HsmExecutedActivity",
  ]
  assert hsm.build_hsm_runtime is build_hsm_runtime
  assert hsm.HsmRuntime is HsmRuntime
  assert hsm.HsmRuntimeMetadata is HsmRuntimeMetadata
  assert hsm.HsmRuntimeSnapshot is HsmRuntimeSnapshot
  assert hsm.HsmRuntimeLastEvent is HsmRuntimeLastEvent
  assert hsm.HsmExecutedActivity is HsmExecutedActivity


def test_hsm_package_does_not_reexport_internal_generation_or_prepare_helpers():
  for name in (
      "GeneratedRuntime",
      "load_generated_runtime",
      "render_generated_runtime_source",
      "prepare_hsm_generated_runtime_view",
      "derive_event_handler_slot_order",
      "HsmGeneratedRuntimeView",
  ):
    assert not hasattr(hsm, name)


def test_runtime_model_modules_expose_preparation_types_from_hsm_layout():
  runtime_model_types = import_module(
    "mbse.runtime.hsm.runtime_model.runtime_model_types"
  )

  assert runtime_model_types.HsmGeneratedRuntimeView is HsmGeneratedRuntimeView
  assert runtime_model_types.HsmGeneratedRuntimeCallablePlan.__module__ == (
    "mbse.runtime.hsm.runtime_model.runtime_model_types"
  )


def test_runtime_model_builder_module_exposes_preparation_builders_from_hsm_layout():
  runtime_model_builder = import_module(
    "mbse.runtime.hsm.runtime_model.runtime_model_builder"
  )

  assert (
    runtime_model_builder.prepare_hsm_generated_runtime_view
    is prepare_hsm_generated_runtime_view
  )
  assert (
    runtime_model_builder.derive_event_handler_slot_order
    is derive_event_handler_slot_order
  )


def test_runtime_package_removes_legacy_prepared_model_modules():
  runtime_dir = Path(__file__).resolve().parents[3] / "src" / "mbse" / "runtime"

  assert not (runtime_dir / "prepared_model.py").exists()
  assert not (runtime_dir / "prepared_model_builder.py").exists()


def test_runtime_package_uses_hsm_runtime_builder_module_name():
  runtime_dir = Path(__file__).resolve().parents[3] / "src" / "mbse" / "runtime"
  runtime_builder = import_module("mbse.runtime.hsm.runtime_builder")

  assert runtime_builder.build_hsm_runtime is build_hsm_runtime
  assert build_hsm_runtime.__module__ == "mbse.runtime.hsm.runtime_builder"
  assert (runtime_dir / "hsm" / "runtime_builder.py").exists()
  assert not (runtime_dir / "runtime_builder.py").exists()


def test_runtime_package_uses_hsm_generator_module_name():
  runtime_dir = Path(__file__).resolve().parents[3] / "src" / "mbse" / "runtime"
  generator = import_module("mbse.runtime.hsm.generator.generator")

  assert generator.GeneratedRuntime is GeneratedRuntime
  assert generator.load_generated_runtime is load_generated_runtime
  assert generator.render_generated_runtime_source is render_generated_runtime_source
  assert GeneratedRuntime.__module__ == "mbse.runtime.hsm.generator.generator"
  assert load_generated_runtime.__module__ == (
    "mbse.runtime.hsm.generator.generator"
  )
  assert render_generated_runtime_source.__module__ == (
    "mbse.runtime.hsm.generator.generator"
  )
  assert generator.TEMPLATE_NAME == "generator_template.py.j2"
  assert (runtime_dir / "hsm" / "generator" / "generator.py").exists()
  assert sorted(
    path.name
    for path in (runtime_dir / "hsm" / "generator").iterdir()
    if path.is_file()
  ) == ["generator.py", "generator_template.py.j2"]
  assert not (runtime_dir / "hsm_generator").exists()
