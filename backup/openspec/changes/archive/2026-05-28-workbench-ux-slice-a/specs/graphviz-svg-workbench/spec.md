# Delta for graphviz-svg-workbench

## ADDED Requirements

### Requirement: Compact One-Line Variable Rows

The workbench UI MUST render each declared `variable_id` as one compact visual row that keeps the variable name, editable value control, and submit action visible together without expanding into per-variable cards. The row MUST still show the current value or an explicit unset state through the existing snapshot flow.

#### Scenario: Declared variables stay compact and editable

- GIVEN the session declares one or more `variable_ids`
- WHEN the sidebar renders or refreshes from a snapshot
- THEN each declared variable appears as one compact row
- AND the row still exposes the existing edit flow for that variable

#### Scenario: Unset variables do not expand into a larger layout

- GIVEN a declared variable has no current value
- WHEN the variable row is shown
- THEN the row stays on the same one-line compact layout
- AND the UI shows an explicit unset state

### Requirement: Resizable Sidebar And Split Layout

The workbench UI MUST provide a horizontal resizable split between the operator sidebar and the SVG viewport. Adjusting that split MUST remain a frontend-only layout action and MUST NOT change runtime state, backend requests, or the event/variable mutation contract.

#### Scenario: User resizes sidebar width

- GIVEN the workbench is open at a normal desktop width
- WHEN the user drags the sidebar-canvas splitter
- THEN the sidebar width and SVG viewport width both update in the same page session
- AND no runtime mutation is triggered by that resize

### Requirement: Runtime Reset And View Reset Stay Separate

The workbench UI MUST expose `Reset runtime` and `Reset view` as distinct actions. `Reset runtime` MUST use the existing runtime reset flow only. `Reset view` MUST restore only client-side diagram view state and MUST NOT call backend/runtime reset behavior.

#### Scenario: Reset runtime does not replace reset view

- GIVEN the user wants to reinitialize runtime state
- WHEN they activate `Reset runtime`
- THEN the existing runtime reset operation runs
- AND the diagram view action remains a separate control

#### Scenario: Reset view stays client-only

- GIVEN the user has changed zoom or pan locally
- WHEN they activate `Reset view`
- THEN the visible diagram view returns to its stored baseline
- AND no backend or runtime reset request is introduced

### Requirement: Fit-Based Initial View With Preserved Zoom And Pan

On initial diagram load, the workbench UI MUST start from a full-diagram fit baseline that makes the complete rendered diagram visible inside the viewport. After that baseline is established, existing client-side wheel zoom and drag-pan MUST continue to operate on top of it, and `Reset view` MUST restore that same fit baseline.

#### Scenario: Initial view fits the whole diagram

- GIVEN the SVG diagram has loaded successfully
- WHEN the first usable workbench view is presented
- THEN the complete diagram is fit within the viewport as the initial baseline
- AND that baseline is the target restored by `Reset view`

#### Scenario: Zoom and pan remain available after fit

- GIVEN the diagram opened from the fit baseline
- WHEN the user zooms or pans the viewport
- THEN the existing client-side zoom and pan interactions still work
- AND those interactions remain layered on top of the fit-based starting view

### Requirement: Slice A Frontend Boundary

Slice A MUST stay frontend-only. It MAY add only compact one-line variable rows, a resizable sidebar/viewport split, separate `Reset runtime` and `Reset view` controls, and fit-based initial/reset view behavior. It MUST NOT change backend endpoints, runtime semantics, highlight behavior, internal SVG rendering, or later Slice B/C work.

#### Scenario: Backend and runtime remain unchanged

- GIVEN Slice A is implemented
- WHEN its behavior is evaluated
- THEN all runtime mutations still use the existing backend contract unchanged
- AND the change is limited to HTML/CSS/JS workbench UX behavior
