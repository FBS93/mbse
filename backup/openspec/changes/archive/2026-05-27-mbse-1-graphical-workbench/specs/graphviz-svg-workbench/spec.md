# graphviz-svg-workbench Specification

## Purpose

Define slice 1 as a read-only local SVG workbench in `src/mbse_1` for inspecting and highlighting one Graphviz-rendered diagram through exact SVG IDs.

## Requirements

### Requirement: Slice-1 Session Artifacts

The system MUST create one bounded workbench session from one prepared Graphviz input. Slice 1 MUST expose exactly these session artifacts: the prepared source document, one rendered `diagram.svg`, and one `workbench-session.json`. The session JSON MUST include `document_id`, `svg_url`, and `highlightable_ids` as the minimal backend/frontend contract. This capability MUST live in `src/mbse_1` and MUST NOT require behavior changes in `src/mbse`.

#### Scenario: Session opens from the bounded artifact set

- GIVEN one prepared input was rendered successfully
- WHEN the workbench session is created
- THEN the session exposes `diagram.svg` and `workbench-session.json`
- AND the frontend can load the SVG from `svg_url`

### Requirement: SVG IDs Are The Only Visual Source Of Truth

The system MUST treat the exact SVG `id` attributes preserved by Graphviz as the only visual identity contract for highlightable elements. `workbench-session.json.highlightable_ids` MUST contain only IDs that exist in `diagram.svg`, and the system MUST NOT derive highlight targets from visible text, labels, titles, or heuristic SVG text parsing.

#### Scenario: Exact Graphviz IDs drive inspection

- GIVEN `highlightable_ids` contains `state_idle`
- WHEN the frontend resolves that ID in the loaded SVG
- THEN it targets the DOM element whose `id` is exactly `state_idle`

#### Scenario: Visible text is not a selector

- GIVEN an SVG label shows `Idle` but no highlightable ID equals `Idle`
- WHEN the user asks to highlight `Idle`
- THEN the system does not infer a target from visible text

### Requirement: Minimal Highlight Request Contract

The backend MUST expose one JSON highlight operation that accepts only an ordered list of exact SVG IDs: `{ "ids": [string] }`. The response MUST return `{ "active_ids": [string], "unknown_ids": [string] }`. The backend and frontend MUST compare IDs by exact string equality and MUST NOT normalize, rewrite, or reinterpret them.

#### Scenario: Highlight request succeeds for known IDs

- GIVEN the session declares `state_idle` and `edge_start`
- WHEN the frontend requests highlight for those IDs
- THEN the backend returns them in `active_ids`
- AND `unknown_ids` is empty

#### Scenario: Unknown IDs are rejected explicitly

- GIVEN the session does not declare `state_missing`
- WHEN the frontend requests highlight for `state_missing`
- THEN the backend returns `state_missing` in `unknown_ids`
- AND the frontend does not claim that highlight was applied

### Requirement: Contract Robustness Validation

The system MUST reject a session as invalid when `diagram.svg` contains duplicate highlightable IDs, when `workbench-session.json` references an ID absent from the SVG, or when the SVG omits an authored Graphviz ID that the session declares highlightable. A valid session SHALL guarantee that every accepted highlight ID resolves to exactly one SVG element.

#### Scenario: Session creation fails on ID mismatch

- GIVEN `workbench-session.json` lists an ID missing from `diagram.svg`
- WHEN the session is validated
- THEN the system returns an actionable contract error
- AND the workbench does not start a misleading highlight session

### Requirement: Slice-1 Scope Boundary

Slice 1 MUST remain a read-only SVG inspection and highlight workbench. It MUST NOT include text-diagram authoring, text-to-diagram editing workflows, runtime execution, runtime synchronization, multi-document workspaces, or heuristic element discovery beyond the declared SVG IDs.

#### Scenario: Deferred features stay out of slice 1

- GIVEN a user opens the workbench successfully
- WHEN they inspect the available actions
- THEN only read-only inspection and ID-based highlight are available
- AND deferred editor or runtime features are absent
