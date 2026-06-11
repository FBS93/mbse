# Delta for graphviz-svg-workbench

## ADDED Requirements

### Requirement: Scroll Ownership Remains Isolated Across Surfaces

The workbench UI MUST keep page scrolling disabled while the workbench is open. The sidebar MUST own vertical overflow only for sidebar content, and the diagram canvas MUST own overflow only when zoomed or panned diagram content exceeds the current viewport.

#### Scenario: Page scroll stays fixed while sidebar content overflows

- GIVEN the workbench page is open and sidebar content exceeds the visible sidebar height
- WHEN the user scrolls outside the diagram canvas
- THEN the document page position does not move
- AND only the sidebar scroll position changes

#### Scenario: Diagram scrollbars appear only for zoomed or panned overflow

- GIVEN the full diagram is fitted inside the current viewport
- WHEN the user has not zoomed or panned beyond the fitted bounds
- THEN the diagram canvas does not require scrollbars

## MODIFIED Requirements

### Requirement: Client-Side SVG View Controls

The workbench UI MUST keep mouse-wheel zoom inside the SVG viewport only, and wheel input over the sidebar MUST scroll only the sidebar vertically. The diagram viewport MUST support click-and-drag pan by moving viewport scroll offsets. During an active pan gesture, the viewport MUST NOT trigger browser text selection, text-underlining, or other selection side effects that interrupt drag ownership. Zoom and pan behavior MUST operate entirely in client-side view state and MUST NOT change SVG IDs, runtime state, or backend requests beyond the already existing workbench operations.
(Previously: Drag pan and wheel isolation were required, but the requirement did not forbid browser text-selection side effects during panning.)

#### Scenario: Sidebar wheel scroll stays isolated from diagram zoom

- GIVEN sidebar content exceeds the visible sidebar height
- WHEN the user uses the mouse wheel over the sidebar
- THEN only the sidebar scroll position changes vertically
- AND the diagram zoom level does not change

#### Scenario: Diagram wheel zoom stays isolated from sidebar scroll

- GIVEN the diagram is loaded in the workbench
- WHEN the user uses the mouse wheel inside the SVG viewport
- THEN the visible SVG viewport zoom changes accordingly
- AND the sidebar scroll position does not change because of that wheel input

#### Scenario: Drag pans the diagram viewport without selection side effects

- GIVEN the diagram viewport has scrollable overflow at the current zoom
- WHEN the user clicks and drags inside the SVG viewport
- THEN the viewport scroll position updates to pan the diagram continuously
- AND no text selection or underline styling appears because of that drag

### Requirement: Fit-Based Initial View With Preserved Zoom And Pan

On initial diagram load, the workbench UI MUST start from a full-diagram fit baseline computed from the current viewport size so the complete rendered diagram is visible inside the viewport. `Reset view` MUST recompute and restore that full-diagram fit baseline from the current viewport size at the time of reset. After that baseline is established, existing client-side wheel zoom and drag-pan MUST continue to operate on top of it.
(Previously: Initial load and Reset view restored a stored fit baseline, but the requirement did not require recomputation from the current viewport size.)

#### Scenario: Initial view fits the whole diagram in the current viewport

- GIVEN the SVG diagram has loaded successfully
- WHEN the first usable workbench view is presented
- THEN the complete diagram is fit within the current viewport
- AND no diagram region starts outside the visible baseline view

#### Scenario: Reset view refits after viewport size changes

- GIVEN the user changed the sidebar width or viewport size after initial load
- WHEN they activate `Reset view`
- THEN the visible diagram view is recomputed from the current viewport size
- AND the complete diagram becomes visible again within that viewport

#### Scenario: Zoom and pan remain available after fit

- GIVEN the diagram opened from the fit baseline
- WHEN the user zooms or pans the viewport
- THEN the existing client-side zoom and pan interactions still work
- AND those interactions remain layered on top of the fit-based starting view
