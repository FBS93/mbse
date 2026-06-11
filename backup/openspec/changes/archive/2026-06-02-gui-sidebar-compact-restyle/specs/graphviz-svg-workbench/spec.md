# Delta for graphviz-svg-workbench

## ADDED Requirements

### Requirement: Compact Restyle Stays Presentation-Only

The visual restyle MUST remain frontend-only and MUST NOT change runtime semantics, backend contracts, or action outcomes.

#### Scenario: Cosmetic changes do not alter runtime behavior

- GIVEN the compact restyle is present
- WHEN the operator uses existing sidebar actions
- THEN the same runtime and backend behaviors still occur

## MODIFIED Requirements

### Requirement: Persistent Operator Sidebar

The workbench UI MUST keep one sidebar visible beside the SVG pane at normal workbench widths. The sidebar MUST present `Reset`, then `Events`, then `Variables`. The sidebar MUST NOT show `Status`, `Current state`, `Current snapshot`, or a separate title/intro block. `Reset runtime` and `Reset view` MUST appear together in one compact row while preserving their existing distinct behaviors. Sidebar controls MUST stay compact and SHOULD reduce unnecessary sidebar scrolling before true overflow occurs. The system MUST keep this as a frontend-only hierarchy simplification and MUST NOT alter runtime semantics.
(Previously: The sidebar stayed visible and compact, but it did not forbid a separate intro block or require one compact reset row.)

#### Scenario: Compact reordered sidebar remains continuously available

- GIVEN the workbench session loads successfully
- WHEN the user inspects the page at a normal workbench width
- THEN the sidebar remains visible while the SVG pane is also visible
- AND only compact `Reset`, `Events`, and `Variables` sections are shown in that order

#### Scenario: Removed status section is not required UI

- GIVEN the workbench renders or refreshes after a runtime action
- WHEN the sidebar contract is evaluated
- THEN no visible `Status` section is required
- AND runtime behavior still uses the existing backend snapshot and mutation flow

#### Scenario: Intro block is removed without removing controls

- GIVEN the sidebar is rendered
- WHEN the operator looks above the control sections
- THEN no separate title or intro block is shown
- AND the existing controls remain available

#### Scenario: Reset actions stay grouped but distinct

- GIVEN the reset controls are visible
- WHEN the operator inspects that section
- THEN `Reset runtime` and `Reset view` appear together in one compact row
- AND each control keeps its own existing behavior

#### Scenario: Sidebar overflow appears only when needed

- GIVEN the compact sidebar controls fit within the visible height
- WHEN the operator opens the workbench at a normal desktop size
- THEN the sidebar does not require vertical scrolling
- AND independent sidebar overflow still appears if later content exceeds that height

### Requirement: Compact One-Line Variable Rows

The workbench UI MUST render each declared `variable_id` as one compact row that keeps the variable name, editable value control, and submit action visible together without expanding into per-variable cards. The editable textbox MUST be the primary visible presentation of the current value from the existing snapshot flow. The row MUST still show an explicit inline unset state when no current value exists.
(Previously: Variable rows had to stay compact, but the textbox was not required to be the primary current-value presentation.)

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

#### Scenario: Textbox shows the current value directly

- GIVEN a declared variable has a current value
- WHEN the row is rendered or refreshed
- THEN the editable textbox shows that value directly
- AND no separate current-value line is required
