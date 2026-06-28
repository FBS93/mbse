from __future__ import annotations

"""Internal render data shapes for the Activity render layer."""

from dataclasses import dataclass
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class ActivitySvgHighlightIndex:
  """Stable lookup index from Activity structure to highlightable SVG ids."""

  initial_transition_id: str
  initial_transition_source_id: str
  action_ids_by_action_id: dict[str, str]
  decision_ids_by_decision_id: dict[str, str]
  final_ids_by_final_id: dict[str, str]
  action_transition_ids_by_action_id: dict[str, str]
  decision_transition_ids_by_key: dict[tuple[str, bool], str]
  action_label_text_ids: dict[str, tuple[str, ...]]
  action_executable_text_ids: dict[tuple[str, str], tuple[str, ...]]
  decision_label_text_ids: dict[str, tuple[str, ...]]
  decision_condition_text_ids: dict[tuple[str, str], tuple[str, ...]]
  final_label_text_ids: dict[str, tuple[str, ...]]
  transition_label_text_ids: dict[str, tuple[str, ...]]
  highlightable_ids: tuple[str, ...]


@dataclass(frozen=True)
class RenderTextFragment:
  """One small text fragment optionally bound to one highlight payload."""

  text: str
  target_payload: str | None = None


@dataclass(frozen=True)
class RenderTextLine:
  """One logical line of text in the DOT label model."""

  fragments: tuple[RenderTextFragment, ...]


@dataclass(frozen=True)
class RenderActivityNode:
  """Prepared Activity node data consumed directly by the DOT template."""

  svg_id: str
  element_id: str
  shape: str
  label_lines: tuple[RenderTextLine, ...]


@dataclass(frozen=True)
class RenderActivityEdge:
  """Prepared Activity edge consumed directly by the DOT template."""

  svg_id: str
  source_id: str
  target_id: str
  label_line: RenderTextLine | None


@dataclass(frozen=True)
class RenderView:
  """Minimal template-ready view of one Activity diagram."""

  document_id: str
  initial_source_id: str
  nodes: tuple[RenderActivityNode, ...]
  edges: tuple[RenderActivityEdge, ...]


@dataclass(frozen=True)
class RenderBuildResult:
  """Prepared render view plus structural lookup tables for highlighting."""

  view: RenderView
  highlightable_ids: tuple[str, ...]
  initial_transition_id: str
  initial_transition_source_id: str
  action_ids_by_action_id: dict[str, str]
  decision_ids_by_decision_id: dict[str, str]
  final_ids_by_final_id: dict[str, str]
  action_transition_ids_by_action_id: dict[str, str]
  decision_transition_ids_by_key: dict[tuple[str, bool], str]


@dataclass(frozen=True)
class NormalizedSvgTextTargets:
  """Resolved text-fragment ids derived from Graphviz SVG output."""

  action_label_ids: dict[str, tuple[str, ...]]
  action_executable_ids: dict[tuple[str, str], tuple[str, ...]]
  decision_label_ids: dict[str, tuple[str, ...]]
  decision_condition_ids: dict[tuple[str, str], tuple[str, ...]]
  final_label_ids: dict[str, tuple[str, ...]]
  transition_label_ids: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class SvgTextFragment:
  """One fragment extracted from raw Graphviz SVG text output."""

  wrapper: ET.Element
  text_element: ET.Element
  payload: str | None
