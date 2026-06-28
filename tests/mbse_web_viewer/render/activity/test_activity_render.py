from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from mbse.model.activity.activity_model import ActivityModel
from mbse_web_viewer.render.activity.activity_render import ActivityRender


FIXTURE_PATH = (
  Path(__file__).resolve().parents[3]
  / "reference_model"
  / "activity"
  / "reference_activity_model.json"
)


def test_activity_svg_renders_reference_model_with_expected_highlight_ids() -> None:
  model = ActivityModel.loadAndValidate(FIXTURE_PATH)

  rendered = ActivityRender()
  rendered.render(model)

  assert (
    rendered.getSvgText().lstrip().startswith("<?xml")
    or "<svg" in rendered.getSvgText()
  )
  assert rendered.getInitialTransitionSourceId() == "initial_source"
  assert rendered.getInitialTransitionId() == "initial_transition_to_check_ready"
  assert rendered.getActionId("prepare_output") == "action_prepare_output"
  assert rendered.getDecisionId("check_ready") == "decision_check_ready"
  assert rendered.getFinalId("done") == "final_done"
  assert rendered.getActionTransitionId("prepare_output") == (
    "action_transition_prepare_output_to_done"
  )
  assert rendered.getDecisionTransitionId("check_ready", outcome=True) == (
    "decision_transition_check_ready_true_to_prepare_output"
  )
  assert rendered.getDecisionTransitionId("check_ready", outcome=False) == (
    "decision_transition_check_ready_false_to_skipped"
  )
  assert "id=\"action_prepare_output\"" in rendered.getSvgText()
  assert "id=\"decision_check_ready\"" in rendered.getSvgText()


def test_activity_svg_exposes_text_targets() -> None:
  model = ActivityModel.loadAndValidate(FIXTURE_PATH)

  rendered = ActivityRender()
  rendered.render(model)

  assert rendered.getActionLabelTextIds("prepare_output")
  assert rendered.getActionExecutableTextIds(
    "prepare_output",
    {
      "kind": "action_language",
      "module": "tests.reference_model.activity.reference_activity_executables",
      "name": "prepare_output",
    },
  )
  assert rendered.getDecisionLabelTextIds("check_ready")
  assert rendered.getDecisionConditionTextIds(
    "check_ready",
    {
      "kind": "action_language",
      "module": "tests.reference_model.activity.reference_activity_executables",
      "name": "is_ready",
    },
  )
  assert rendered.getFinalLabelTextIds("done")
  assert rendered.getTransitionLabelTextIds(
    "decision_transition_check_ready_true_to_prepare_output"
  )


def test_activity_svg_exposes_model_executable_text_targets() -> None:
  model = ActivityModel.loadAndValidate(FIXTURE_PATH)
  document = deepcopy(model.document)
  document["actions"][0]["executable"] = {
    "kind": "model",
    "model_id": "child_activity",
  }
  model = ActivityModel(document)

  rendered = ActivityRender()
  rendered.render(model)

  assert rendered.getActionExecutableTextIds(
    "prepare_output",
    {"kind": "model", "model_id": "child_activity"},
  )
