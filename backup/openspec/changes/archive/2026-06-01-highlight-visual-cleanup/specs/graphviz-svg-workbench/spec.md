# Delta for graphviz-svg-workbench

## MODIFIED Requirements

### Requirement: Backend-Driven Exact-ID Highlight Sync

The system MUST derive runtime highlight state in the backend from the current runtime snapshot and MUST return `active_ids` that match SVG element IDs by exact string equality. `active_ids` MUST represent only the current active leaf state, even when `active_path` includes parent compounds. The snapshot MAY include one optional `last_transition_id`, and when present it MUST identify the final exact SVG transition ID that led into the current leaf state. The frontend MUST apply only those returned exact IDs, MUST render state highlight and transition highlight as visually distinct treatments, MUST keep all state and transition label text visually neutral, MUST emphasize active states through contour treatment plus a slightly stronger same-hue background, MUST emphasize active transitions only on the edge line and arrowhead, and MUST NOT infer targets from labels, titles, text, or heuristics.
(Previously: The frontend had to keep state highlight subtle and transition highlight distinct, but it did not yet define text exclusion or shape-only emphasis precisely.)

#### Scenario: Leaf-only state highlight is applied by exact ID

- GIVEN the backend snapshot reports a compound parent and one active leaf in `active_path`
- WHEN the snapshot response is produced
- THEN `active_ids` contains only the exact SVG ID for the active leaf
- AND the viewer highlights only that returned state ID

#### Scenario: Final transition into the leaf is highlighted separately

- GIVEN entry into the current leaf required one or more transitions
- WHEN the snapshot response is produced
- THEN `last_transition_id` identifies only the final transition into that leaf when such an SVG ID exists
- AND the viewer applies a transition highlight that is visually distinct from the state highlight

#### Scenario: Highlight styling excludes labels and targets only intended shapes

- GIVEN the active state or transition SVG group also contains visible text labels
- WHEN the frontend applies highlight styling for the returned exact IDs
- THEN text descendants keep their normal visual treatment
- AND only state contours/background shapes or transition edge/arrowhead shapes receive highlight emphasis
