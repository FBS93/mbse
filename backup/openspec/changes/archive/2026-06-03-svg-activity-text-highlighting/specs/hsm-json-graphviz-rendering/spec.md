# Delta for hsm-json-graphviz-rendering

## ADDED Requirements

### Requirement: Private Render-Owned Text Fragment Targets

The prepared render metadata MUST include a private render-owned fragment-target contract for text-level highlighting. The contract SHALL map authored semantic refs to normalized private SVG fragment targets for transition event/activity text, `on_initial`, `on_entry`, `on_exit` section labels plus executed activity text, and internal-transition section/row text. It MUST preserve authored/public SVG `id` values and `highlightable_ids` exactly, MUST keep current shape/edge targets unchanged, and MUST NOT move runtime or viewer concerns into the diagram-definition layer.

#### Scenario: Lifecycle and transition text get private targets

- GIVEN a state body renders `on_initial`, `on_entry`, `on_exit` content and an external transition renders event/activity text
- WHEN SVG marker hints are normalized into prepared metadata
- THEN the metadata includes private targets for those labels and activity fragments
- AND the public/authored SVG IDs remain unchanged

#### Scenario: Internal-transition rows stay distinguishable

- GIVEN one state renders `internal_transitions:` with multiple internal transition rows
- WHEN prepared metadata is produced
- THEN the contract includes one section-label target plus row-scoped event/activity targets keyed by `internal_transition_id`
- AND no new public SVG IDs are introduced for those rows

#### Scenario: Missing unique fragment stays unmapped

- GIVEN normalization cannot identify one unique fragment for a text target
- WHEN the contract is emitted
- THEN that private target is omitted instead of retargeting a different fragment
- AND the renderer does not mint or expose a replacement public ID
