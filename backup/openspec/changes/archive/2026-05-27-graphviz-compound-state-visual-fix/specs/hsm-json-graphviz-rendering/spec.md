# Delta for hsm-json-graphviz-rendering

## ADDED Requirements

### Requirement: Compound State Cluster Visual Contract

Compound states MUST render their public parent visual on the enclosing Graphviz cluster. The cluster MUST carry the exact authored compound-state `id` and the visible parent label. The system MUST NOT emit a second visible internal parent node for that same compound state. If Graphviz routing needs an internal endpoint for local initials or transitions, the system MAY emit one internal anchor, but that anchor MUST NOT replace, duplicate, or expose a second public SVG identity for the authored compound state. This change MUST preserve the exact public SVG `id` contract for compound states and MUST NOT change flat-state rendering, transition semantics, validation rules, or workbench highlight behavior.

#### Scenario: Compound parent renders as container title

- GIVEN a compound state with authored `id` `state_parent`, label `Parent`, and nested children
- WHEN the document is prepared and rendered to SVG
- THEN the enclosing cluster exposes the exact public SVG `id` `state_parent`
- AND the visible parent title appears on the cluster rather than as a child state box

#### Scenario: Visible duplicate parent box is absent

- GIVEN a compound state with nested children and an internal routing anchor
- WHEN the document is rendered
- THEN no second visible internal node represents the parent state inside its own child region
- AND the compound state still supports local initials and transitions through internal routing only

#### Scenario: Exact compound-state IDs remain stable

- GIVEN a compound state authored with `id` `state_parent`
- WHEN the workbench validates `diagram.svg` against `highlightable_ids`
- THEN exactly one public highlightable SVG element resolves for `state_parent`
- AND no rewritten, prefixed, or anchor-derived SVG `id` replaces that authored ID

#### Scenario: Non-compound behavior stays unchanged

- GIVEN a document containing flat states, transitions, and non-compound labels
- WHEN the compound-state visual fix is applied
- THEN their prepared IDs and rendered behavior remain unchanged
- AND the system does not expand the change into runtime or layout tuning beyond compound-state visuals
