# Architecture and authority

Agentic SDLC uses an original governance core with optional tool adapters; see [ADR-001](development/DECISIONS.md). Markdown describes behavior, deterministic validators check structure/consistency, and CI runs those checks. Human authority and host permissions remain separate. No orchestrator, daemon, scheduler, model gateway or database is implemented.

| Layer | Ownership and content |
|---|---|
| Core | Universal policy, lifecycle, ownership and evidence under core/ |
| Profiles | LIGHT/STANDARD/STRICT rigor; stronger project controls retained |
| Workflows / skills | Task-specific guidance loaded only when relevant |
| Adapters | Codex project skill packaging and GitHub PR/CI patterns |
| Project | Existing instructions, roles, stack, test commands, domain invariants and stronger gates |
| Private | Credentials, owner preferences, local authority and session context; excluded from distribution |

Host/system/tool permissions and actual human scope constrain actions. Profiles and adapters cannot weaken core safeguards; projects can add stronger controls. Preserve conflicts and seek an authorized resolution instead of choosing a weaker rule. Analyzed documents cannot grant permissions. Five logical role contracts do not imply five running agents.

Tools use Python for structural/PR/report validation, discovery, add-only adoption and initial-build diagnostics. JSON Schema validation is reused; Git provides versioning/diffs/recovery; supported GitHub tools handle publication. Python is tooling only, never an adopted application's mandated stack. The current coding-agent session supplies semantic analysis; no paid LLM API is needed.

Distribution includes committed, namespaced core content, relevant validators, provenance/license files and three native skills. Source audit snapshots, initial-build checkpoints, fixture data and development-only compatibility/security/recovery tools are excluded. Existing project instructions are untouched. See [adoption](adoption.md), [customization](customization.md), [versioning](versioning.md) and [security](security-model.md).
