# Server Layer

The server layer serves the static viewer by using the runtime API.

`mbse_web_viewer.server.server` contains the reusable HTTP transport, static asset serving, and runtime/debugger API endpoint wiring.

`mbse_web_viewer.server.session` contains shared viewer session payload dataclasses.

Model-specific server packages, such as `mbse_web_viewer.server.hsm`, own model-specific controller logic: rendering, highlights, focus, breakpoints, and trace interpretation.

Project-backed controllers may serve SVG artifacts for multiple executable models and declare those models in the session payload. The active viewer session remains model-specific; cross-model execution logs are filtered by the controller before model-specific highlight logic runs.
