# Architectural decisions

## ADR-000 — Durable repository checkpoints (accepted)

Context: agent sessions and external operations can be interrupted. Alternatives: chat-only continuity, centralized state service, repository files and Git. Choose concise repository plan/state/decisions/validation/recovery documents plus small Git commits. No service dependency; notes can become stale, so Git/filesystem/external reality always wins. Current commit cannot contain its own SHA: state records a previously verified anchor; `git rev-parse HEAD` identifies the actual current checkpoint. Preserve the resulting SHA in the next state update.

## ADR-001 — Hybrid core with optional adapters (accepted)

Context: preserve source engineering guarantees across unrelated projects without importing its stack or a large execution runtime. Evidence: `docs/audit/build-vs-reuse.md` and pinned research inventory.

Alternatives: A fully custom orchestration/update engine has unnecessary cost and authority surface. B thin governance on mandatory Spec Kit reuses mature tools but makes their installation/update and workflow assumptions mandatory; documented preset/refresh limitations conflict with the desired safe defaults. C original Markdown/JSON governance, native project skills and small Python validation/adoption scripts with optional future adapters meets P0 with the smallest required runtime. Choose C.

Python is tooling only, never an adopted project's mandated stack. Reuse the maintained `jsonschema` library for Draft 2020-12 validation; use Git for versioning/recovery and normal GitHub tools for publication. No LLM API client, orchestrator, daemon, scheduler or database. Adoption is deterministic discovery → agent semantic report → schema validation → human-reviewed proposal → add-only controlled application. Existing project-owned instructions are never overwritten. Installed files carry source revision and hashes; upgrades are reviewed manually in a branch, not automatic.

Trade-offs: no automatic semantic equivalence proof, multi-provider execution, agent behavior enforcement, atomic cross-process locks, or full upgrade automation. Docs and schema validation do not authenticate approvals. P1 Spec Kit bundling and other adapters require independent justification and tests.
