## Exploration: mbse-1-graphical-workbench

### Current State
The repo already has a Python-first local browser surface in `src/mbse/viewer/`, implemented with `http.server`, static HTML/CSS, and a small handwritten JS file. It is intentionally read-only and artifact-driven: it serves an existing `diagram.svg`, optional `semantic-map.json`, and optional runtime sync for one HSM session.

The current workbench flow in `src/mbse/workbench/` is not a new GUI. It is a CLI orchestrator that discovers JSON HSM models, renders through the HSM-specific pipeline, and opens the existing viewer. The rendering side in `src/mbse/rendering/` is also HSM-shaped today: `render_model()` requires a validated `HsmModel`, and the semantic mapping contract assumes HSM `state` and `transition` kinds.

There is no `src/mbse_1` package yet. That means the cleanest way to respect the boundary is to introduce a parallel package that does not modify `src/mbse` and does not inherit the HSM-specific contracts as its public architecture.

### Affected Areas
- `src/mbse/viewer/server.py` — proves the repo already accepts a Python stdlib HTTP server + tiny static client pattern.
- `src/mbse/viewer/static/index.html` — shows the current viewer is mostly static HTML with a small JS bootstrap, not a frontend app.
- `src/mbse/viewer/static/viewer.js` — shows the existing browser logic is intentionally small but still handwritten and HSM/runtime-aware.
- `src/mbse/rendering/artifacts.py` — current artifact contract is stable (`diagram.puml`, `diagram.svg`, `semantic-map.json`) but tied to `HsmModel` rendering.
- `src/mbse/rendering/mapping.py` — current semantic mapping kinds are HSM-specific (`state`, `transition`), which is too narrow for a reusable PlantUML GUI base.
- `src/mbse/workbench/launcher.py` — current "workbench" is orchestration around HSM render + existing viewer, not a standalone GUI boundary.
- `docs/prd-hsm-mvp.md` — confirms the long-term architecture should outlive HSM and treat PlantUML as a rendering backend only.
- `openspec/specs/rendered-svg-web-viewer/spec.md` — captures the current read-only viewer boundary that should inform, but not constrain, `src/mbse_1`.

### Approaches
1. **Artifact-first local web workbench in `src/mbse_1`** — Build a new isolated Python package that owns a tiny local server, server-rendered pages, and a minimal JS layer only for loading SVG and lightweight interactions. Its core contract is generic PlantUML artifacts: source `.puml`, rendered `.svg`, and optional sidecar metadata. HSM becomes just one future adapter, not the foundation.
   - Pros: Best fit for the repo's current Python-first direction; keeps `src/mbse` untouched; generic for any PlantUML diagram type; smallest path to a real GUI without introducing Node or a SPA.
   - Cons: Some browser JS still exists, even if small; generic metadata rules must be designed carefully so they do not accidentally inherit HSM semantics.
   - Effort: Low

2. **Desktop wrapper GUI in `src/mbse_1`** — Use a Python desktop shell such as Tkinter/pywebview/Qt around a rendered HTML preview.
   - Pros: Feels more like a native app and reduces browser-launch concerns.
   - Cons: Adds toolkit decisions and packaging complexity immediately; worse fit for the repo's already-working local web pattern; higher risk for a first bounded slice.
   - Effort: Medium

3. **Clone and generalize the current `mbse` viewer/workbench behavior into `src/mbse_1`** — Copy the existing viewer/workbench structure and progressively remove HSM assumptions.
   - Pros: Fastest on paper because the pattern already exists.
   - Cons: High duplication risk; easy to drag HSM-specific naming and contracts into the new package; weak architecture signal for future non-HSM diagram types.
   - Effort: Medium

### Recommendation
Choose **Artifact-first local web workbench in `src/mbse_1`**.

The SMALLEST controlled slice is not "build a full editor" and not "port the old viewer." It is a new isolated package with an explicit artifact boundary:

1. `src/mbse_1` owns a generic `DiagramDocument` / `WorkbenchSession` style contract around PlantUML input and rendered SVG output.
2. The first GUI loop is file-open -> render -> preview -> inspect basic metadata.
3. The first UI is server-rendered HTML plus tiny progressive JS, reusing the repository's proven local-browser pattern instead of introducing a frontend stack.
4. HSM-specific semantic/runtime behavior stays OUT of slice 1.
5. Any future HSM integration should happen through an adapter that feeds `src/mbse_1`, not by making `src/mbse_1` depend on `HsmModel` as its core domain.

Recommended first implementation boundary for proposal/spec:
- create `src/mbse_1` as a parallel package only,
- accept explicit PlantUML file inputs first (not workspace discovery, not model editing),
- render through a generic PlantUML subprocess boundary,
- serve one local page that shows source path, render status, SVG preview, and optional metadata panel,
- keep JS limited to fetch/render/selection behavior,
- defer HSM runtime sync, semantic mapping richness, file watching, editing, and multi-document workspaces.

This keeps loops small: one input, one render contract, one preview surface, one package boundary.

### Risks
- The current repo's richest viewer behaviors are HSM-driven, so reusing ideas without reusing contracts requires discipline; otherwise `src/mbse_1` will quietly become HSM-shaped.
- A "generic PlantUML GUI" can sprawl fast if it includes discovery, editing, live reload, and runtime features in the first slice.
- If the first contract requires semantic metadata for all diagram types, the team will block itself on a taxonomy problem before delivering a useful preview GUI.

### Ready for Proposal
Yes — propose `mbse-1-graphical-workbench` as a bounded new package in `src/mbse_1` for an artifact-first, Python-first local web GUI around generic PlantUML render/preview, explicitly deferring HSM runtime coupling and richer frontend behavior.
