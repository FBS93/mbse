from __future__ import annotations

import importlib.util
from pathlib import Path
import re

import pytest

import mbse_web_viewer
import mbse_web_viewer.svg_render
from mbse_web_viewer.app.server import start_viewer_server
from mbse_web_viewer.app.session import build_viewer_session
from mbse_web_viewer.main import build_and_start_viewer


def _find_spec_or_none(module_name: str):
  try:
    return importlib.util.find_spec(module_name)
  except ModuleNotFoundError:
    return None


def test_package_root_exposes_only_application_entrypoints():
  assert mbse_web_viewer.__all__ == [
    "build_and_start_viewer",
    "build_viewer_session",
    "start_viewer_server",
  ]
  assert mbse_web_viewer.build_and_start_viewer is build_and_start_viewer
  assert mbse_web_viewer.build_viewer_session is build_viewer_session
  assert mbse_web_viewer.start_viewer_server is start_viewer_server


@pytest.mark.parametrize(
  "import_name",
  [
    "PreparedGraphvizDocument",
    "RunningViewerServer",
    "RuntimeViewerSession",
    "RuntimeViewerTextTargets",
    "ViewerAppState",
    "ViewerRuntimeBridge",
    "load_prepared_document",
    "validate_prepared_document",
  ],
)
def test_package_root_does_not_reexport_internal_viewer_details(import_name):
  with pytest.raises(ImportError):
    exec(f"from mbse_web_viewer import {import_name}", {})


def test_svg_render_root_exposes_only_public_render_api():
  assert mbse_web_viewer.svg_render.__all__ == [
    "PreparedGraphvizDocument",
    "extract_svg_ids",
    "load_prepared_document",
    "normalize_svg_text_fragments",
    "prepare_hsm_render_view",
    "render_hsm_dot",
    "render_svg",
    "validate_prepared_document",
    "validate_rendered_contract",
  ]


@pytest.mark.parametrize(
  "import_name",
  [
    "GraphvizRenderError",
    "HsmPreparedRenderView",
    "HsmRenderGuardNode",
    "HsmRenderInitialEdge",
    "HsmRenderRoutingHelper",
    "HsmRenderStateNode",
    "HsmRenderStateSection",
    "HsmRenderTextFragment",
    "HsmRenderTextLine",
    "HsmRenderTransitionEdge",
    "extract_authored_ids",
    "load_runtime_viewer_text_targets",
  ],
)
def test_svg_render_root_does_not_reexport_internal_modules(import_name):
  with pytest.raises(ImportError):
    exec(f"from mbse_web_viewer.svg_render import {import_name}", {})


def test_app_modules_replace_legacy_top_level_viewer_modules():
  assert importlib.util.find_spec("mbse_web_viewer.models") is None
  assert importlib.util.find_spec("mbse_web_viewer.main") is not None
  assert importlib.util.find_spec("mbse_web_viewer.app.server") is not None
  assert importlib.util.find_spec("mbse_web_viewer.app.session") is not None
  assert importlib.util.find_spec("mbse_web_viewer.app.runtime_bridge") is not None
  assert (
    importlib.util.find_spec("mbse_web_viewer.app.viewer_state_types")
    is not None
  )
  assert importlib.util.find_spec("mbse_web_viewer.app") is not None
  assert importlib.util.find_spec("mbse_web_viewer.server") is None
  assert importlib.util.find_spec("mbse_web_viewer.session") is None
  assert importlib.util.find_spec("mbse_web_viewer.runtime_bridge") is None
  assert importlib.util.find_spec("mbse_web_viewer.viewer_state_types") is None

  python_tracked_paths = (
    Path("src/mbse_web_viewer"),
    Path("tests/unit/mbse"),
    Path("tests/integration"),
  )
  legacy_python_import_pattern = re.compile(
    r"(?:from\s+mbse_web_viewer\.(?:server|session|runtime_bridge|viewer_state_types)\s+import|import\s+mbse_web_viewer\.(?:server|session|runtime_bridge|viewer_state_types)|from\s+mbse_web_viewer\s+import\s+app\b)"
  )
  for tracked_path in python_tracked_paths:
    for tracked_file in tracked_path.rglob("*.py"):
      contents = tracked_file.read_text(encoding="utf-8")
      assert legacy_python_import_pattern.search(contents) is None

  vscode_tasks = Path(".vscode/tasks.json").read_text(encoding="utf-8")
  assert "mbse_web_viewer.app\"" not in vscode_tasks


def test_viewer_graphviz_modules_replace_legacy_module_names():
  assert (
    _find_spec_or_none(
      "mbse_web_viewer.svg_render.graphviz.prepared_document"
    )
    is not None
  )
  assert (
    _find_spec_or_none(
      "mbse_web_viewer.svg_render.graphviz.contract_validation"
    )
    is not None
  )
  assert _find_spec_or_none("mbse_web_viewer.svg_render.render") is not None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.render_types") is not None
  assert (
    _find_spec_or_none(
      "mbse_web_viewer.svg_render.graphviz.generator.generator"
    )
    is not None
  )
  assert (
    _find_spec_or_none(
      "mbse_web_viewer.svg_render.graphviz.runner"
    )
    is not None
  )
  assert _find_spec_or_none("mbse_web_viewer.model_to_svg_render") is None
  assert _find_spec_or_none("mbse_web_viewer.graphviz_document") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.contract") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.graphviz.graphviz_data") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.graphviz.view_data") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.graphviz_document") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.svg_contract_validation") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.prepare_hsm_render") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.graphviz.prepared_view_data") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.graphviz.svg_data") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.view") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.view.render") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.view.render_types") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.view.prepare_hsm_render") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.view.models") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.dot_template") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.graphviz_runner") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.graphviz.dot_template") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.graphviz.graphviz_runner") is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.contract.graphviz_document") is None
  assert _find_spec_or_none(
    "mbse_web_viewer.svg_render.contract.graphviz_contract_validation"
  ) is None
  assert _find_spec_or_none("mbse_web_viewer.svg_render.models") is None
  assert (
    _find_spec_or_none(
      "mbse_web_viewer.graphviz_text_targets_parser"
    )
    is None
  )
