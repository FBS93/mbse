# Delta for graphviz-svg-workbench

## MODIFIED Requirements

### Requirement: Backend-Driven Exact-ID Highlight Sync

The system MUST derive shape highlight state in the backend and MUST return `active_ids` that match SVG element IDs by exact equality. `active_ids` MUST represent only the current active leaf state, even when `active_path` includes parent compounds. `last_transition_id` MUST be returned as the ordered latest-resolution path after filtering each member against `highlightable_ids` by exact equality. The backend MUST preserve surviving order, MUST drop unmatched members, and MUST NOT use labels, substrings, prefixes, or other partial-ID matching. The frontend MUST apply every returned transition ID and MUST preserve the current active-state and taken-edge shape/arrow highlighting behavior. The frontend MAY additionally highlight visible text only when session metadata provides private render-owned fragment targets and `last_event` provides matching semantic refs. Text emphasis MUST avoid heavier font weight and SHOULD use text-safe accent treatment such as underline and subtle background. For internal transitions, the viewer MUST highlight `internal_transitions:` plus only the matching internal-transition event/activity text for the latest handled row.

(Previously: the frontend kept all labels visually neutral and highlighted only state borders plus transition edge/arrow shapes from exact SVG IDs.)

#### Scenario: Leaf-only state highlight is applied by exact ID

- GIVEN the backend snapshot reports a compound parent and one active leaf in `active_path`
- WHEN the snapshot response is produced
- THEN `active_ids` contains only the exact SVG ID for the active leaf
- AND the viewer highlights only that returned state ID with border emphasis and no fill intensification

#### Scenario: Mixed transition path is filtered member-by-member

- GIVEN the latest runtime resolution reports `["edge_enter", "edge_nested", "missing_edge"]` and only the first two are in `highlightable_ids`
- WHEN the snapshot response is produced
- THEN `last_transition_id` becomes `["edge_enter", "edge_nested"]` in that same order
- AND the viewer highlights both returned transitions without attempting a partial match for `missing_edge`

#### Scenario: Last-event semantics drive precise text emphasis

- GIVEN session metadata contains private targets for one transition label plus one state's `on_entry` label and executed activity text
- WHEN `last_event.transition_path_ids` and ordered `last_event.executed_activities` identify those semantic refs
- THEN the viewer highlights only the matching transition event/activity text and matching lifecycle label/activity fragments
- AND unrelated label text stays visually neutral

#### Scenario: Internal-transition highlighting stays row-specific

- GIVEN `last_event` reports a handled internal transition with no external transition path and the rendered state contains multiple internal-transition rows
- WHEN the viewer resolves private targets from the handled internal-transition semantic ref and executed activities
- THEN it highlights `internal_transitions:` and only that row's event/activity text
- AND no other internal-transition row or external edge receives highlight emphasis
