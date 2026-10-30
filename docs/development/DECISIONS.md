# Architectural decisions

## ADR-000 — Durable repository checkpoints (accepted)

Context: agent sessions and external operations can be interrupted. Alternatives: chat-only continuity, centralized state service, repository files and Git. Choose concise repository plan/state/decisions/validation/recovery documents plus small Git commits. No service dependency; notes can become stale, so Git/filesystem/external reality always wins. Current commit cannot contain its own SHA: state records a previously verified anchor; `git rev-parse HEAD` identifies the actual current checkpoint. Preserve the resulting SHA in the next state update.
