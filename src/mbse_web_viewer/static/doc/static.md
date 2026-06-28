# Static Viewer

The static viewer contains the browser UI for the MBSE web viewer.

`viewer.js` bootstraps the page, wires UI events, and coordinates session rendering.

Shared browser modules are split by responsibility:

- `viewer_state.js`: constants and mutable viewer UI state.
- `viewer_api.js`: HTTP fetch helpers.
- `viewer_utils.js`: HTML and CSS escaping helpers.
- `viewer_declared_values.js`: typed variable and event-parameter rendering, collection, and draft comparison.
- `viewer_viewport.js`: SVG viewport zoom, pan, fit, and centering helpers.

Model-specific SVG semantics are provided by the server session payload. The browser loads the active model SVG, allows navigation across session-declared models, and applies highlights, focus ids, debugger state, variables, and breakpoints from that payload without executing MBSE model semantics.
