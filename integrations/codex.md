# Codex desktop adapter

Three native project skills live under .agents/skills/: sdlc-pr-write, sdlc-adopt-review and sdlc-upstream-review. They use standard SKILL.md name/description metadata and progressive disclosure. See [official skill guidance](https://developers.openai.com/codex/skills). Packaging tests do not prove a particular agent session selected or followed a skill.

Open the intended repository as a desktop Local project. After adding skills, use a new project chat to inspect actual discovery, explicitly read the relevant skill and verify its bounded role and pinned baseline. Use the integrated terminal and Git/Diff Review. No Codex CLI/session-resume command, global settings, Screen Recording, Accessibility or cross-app permission is required. Model identity is not a recovery dependency.

Adopted skills locate .sdlc/agentic-sdlc through .sdlc/install.json. Validators/discovery can run from that baseline with the locked environment. Installation planning/application requires the original pinned framework Git checkout to verify committed source. Preserve private overrides and project allowlists; report conflicts rather than widening them automatically.
