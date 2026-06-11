## Exploration: init-transition-rendering-cleanup

### Current State
`prepare_hsm_render.py` already centralizes edge preparation enough to route compound endpoints through private `__anchor` helpers for normal transitions, the root initial, and now local initials as well. The public/highlightable contract stays on authored IDs only (`state.id`, transition IDs, initial IDs), while the DOT template emits extra point nodes such as `__root_init__`, `{state}__init`, and `{state}__anchor` to satisfy Graphviz routing constraints around clusters. With real Graphviz, those helper nodes do not reuse the private names as SVG IDs; they render as generic `nodeN` groups with visible black ellipses, which is the remaining visual noise.

### Affected Areas
- `src/mbse/application/prepare_hsm_render.py` — current routing policy, helper-ID construction, and initial/transition preparation.
- `src/mbse/domain/models.py` — prepared render view currently models public states/edges but not private helper routing explicitly.
- `src/mbse/infrastructure/templates/hsm_v1.dot.j2` — emits visible point helpers for root init, local init connectors, and compound anchors.
- `src/mbse/domain/validation.py` — enforces the authored/public ID contract and prepared-document highlightable ID integrity.
- `tests/unit/mbse/test_hsm_render_view.py` — current coverage for routed compound initials and DOT output.
- `tests/integration/test_hsm_json_workbench.py` — prepared-document/session contract coverage, but mostly with fake Graphviz and limited real-SVG assertions.

### Approaches
1. **Minimal visual suppression on existing helpers** — keep the current helper-node architecture, but render helper nodes as invisible routing scaffolding while preserving their endpoint role.
   - Pros: Smallest code change; preserves current routing behavior; low risk to public IDs and runtime/workbench contracts.
   - Cons: Still leaves helper concepts implicit and spread across state flattening, edge preparation, and template rules; improves appearance more than architecture.
   - Effort: Low

2. **Explicit private-routing layer with invisible helpers** — introduce a first-class internal routing model in the prepared render view (for root/local init connectors and compound anchors), keep authored IDs as the only public/highlightable IDs, and have the template render private routing helpers invisibly and only when needed.
   - Pros: Makes the public/private boundary explicit; keeps one coherent routing policy for all edge kinds; supports cleaner tests around “public IDs vs private routing”; solves the visual noise without relying on ad hoc template literals.
   - Cons: Moderate refactor across models, preparation, template, and tests; requires careful regression coverage so helper invisibility does not break layout/routing.
   - Effort: Medium

3. **Remove helpers and rely on cluster routing tricks** — try to route directly to/from clusters via Graphviz cluster attributes or edge metadata instead of internal helper nodes.
   - Pros: Conceptually removes helper nodes from the model.
   - Cons: High risk. Graphviz clusters are not real edge endpoints, local initials still need an internal source, and the exact public-ID contract becomes harder to reason about and test. This is likely to reintroduce ghost-node behavior or ambiguous routing.
   - Effort: High

### Recommendation
Choose **Approach 2**. The problem is NOT just one stray dot; the architecture currently treats private routing helpers as a side effect of state/template rendering instead of a deliberate render-internal layer. Make that layer explicit in the prepared view, keep helper creation on-demand, and render those helpers invisibly so Graphviz can still route edges through real endpoints without exposing visual noise. This keeps the authored/public SVG ID contract exact, preserves the recent compound-init fix, and gives proposal/design/apply phases a clean boundary to implement and test.

Implementation direction inside that recommendation:
- Separate **public renderables** (authored state/transition/initial IDs) from **private routing helpers**.
- Generate helper records only for: root initial source, local initial sources, and compound-state anchor endpoints actually referenced by edges.
- Update the DOT template to render private helpers as invisible routing nodes rather than visible point dots.
- Add at least one real-Graphviz assertion for helper invisibility/absence of stray helper ellipses, because the current fake Graphviz path validates IDs but not visual cleanup.

### Risks
- Real Graphviz behavior may differ from fake-render tests, so invisibility needs one integration check with the actual `dot` binary.
- Refactoring the prepared render model can break template assumptions if helper ownership is not kept deterministic.
- Over-aggressive helper removal could regress compound endpoint routing and recreate ghost nodes or duplicate public identities.

### Ready for Proposal
Yes — proposal should scope this as a render-only cleanup that formalizes private routing helpers, keeps exact public IDs unchanged, and adds real-SVG regression coverage for visual cleanliness.
