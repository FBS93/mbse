# Skill Registry

Generated: 2026-05-26
Project: MBSE

## Project Convention Files

- None found in the repository root or supported subpaths (`AGENTS.md`, `agents.md`, `CLAUDE.md`, `.cursorrules`, `GEMINI.md`, `copilot-instructions.md`).

## Project Skills

- None found in `skills/`, `.opencode/skills/`, `.claude/skills/`, `.gemini/skills/`, `.cursor/skills/`, `.github/skills/`, `.codex/skills/`, `.qwen/skills/`, `.kiro/skills/`, `.openclaw/skills/`, `.pi/skills/`, `.agent/skills/`, `.agents/skills/`, or `.atl/skills/`.

## User Skills Index

| Name | Scope | Trigger / Description | Path |
| --- | --- | --- | --- |
| branch-pr | user | Create Gentle AI pull requests with issue-first checks. Trigger: creating, opening, or preparing PRs for review. | `/home/vscode/.config/opencode/skills/branch-pr/SKILL.md` |
| chained-pr | user | Trigger: PRs over 400 lines, stacked PRs, review slices. Split oversized changes into chained PRs that protect review focus. | `/home/vscode/.config/opencode/skills/chained-pr/SKILL.md` |
| cognitive-doc-design | user | Design docs that reduce cognitive load. Trigger: writing guides, READMEs, RFCs, onboarding, architecture, or review-facing docs. | `/home/vscode/.config/opencode/skills/cognitive-doc-design/SKILL.md` |
| comment-writer | user | Write warm, direct collaboration comments. Trigger: PR feedback, issue replies, reviews, Slack messages, or GitHub comments. | `/home/vscode/.config/opencode/skills/comment-writer/SKILL.md` |
| customize-opencode | user | Use ONLY when the user is editing or creating opencode's own configuration: opencode.json, opencode.jsonc, files under .opencode/, or files under ~/.config/opencode/. Also use when creating or fixing opencode agents, subagents, skills, plugins, MCP servers, or permission rules. Do not use for the user's own application code, or for any project that is not configuring opencode itself. | `file:///workspaces/MBSE/%3Cbuilt-in%3E` |
| go-testing | user | Trigger: Go tests, go test coverage, Bubbletea teatest, golden files. Apply focused Go testing patterns. | `/home/vscode/.config/opencode/skills/go-testing/SKILL.md` |
| issue-creation | user | Create Gentle AI issues with issue-first checks. Trigger: creating GitHub issues, bug reports, or feature requests. | `/home/vscode/.config/opencode/skills/issue-creation/SKILL.md` |
| judgment-day | user | Trigger: judgment day, dual review, adversarial review, juzgar. Run blind dual review, fix confirmed issues, then re-judge. | `/home/vscode/.config/opencode/skills/judgment-day/SKILL.md` |
| skill-creator | user | Trigger: new skills, agent instructions, documenting AI usage patterns. Create LLM-first skills with valid frontmatter. | `/home/vscode/.config/opencode/skills/skill-creator/SKILL.md` |
| skill-improver | user | Trigger: improve skills, audit skills, refactor skills, skill quality. Audit and upgrade existing LLM-first skills. | `/home/vscode/.config/opencode/skills/skill-improver/SKILL.md` |
| work-unit-commits | user | Plan commits as reviewable work units. Trigger: implementation, commit splitting, chained PRs, or keeping tests and docs with code. | `/home/vscode/.config/opencode/skills/work-unit-commits/SKILL.md` |

## Notes

- `sdd-*`, `_shared`, and `skill-registry` skills were intentionally excluded per registry rules.
- Project-level skills would override user-level skills with the same name if added later.
