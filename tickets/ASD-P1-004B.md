---
id: ASD-P1-004B
title: Document the opencode adapter
priority: P1
status: backlog
type: docs
parent: ASD-P1-004
depends_on: []
resources: [adapter-opencode]
risk: low
size: S
agent_tier: standard
gate: owner
gate_approval:
review: self
branch:
pr:
spec:
updated: 2026-11-06
---

# ASD-P1-004B: Document the opencode adapter

## Goal

Add `integrations/opencode.md` explaining how opencode loads AGENTS.md, the native skills and the PR workflow, with the same safety limits as integrations/codex.md.

## Acceptance criteria

- [ ] `integrations/opencode.md` exists, is listed in PUBLIC_FILES.json and passes the publication audits.
- [ ] A test checks that every path the document names exists.
- [ ] Full checks pass.

## Plan

- [ ] Read integrations/codex.md and the agent's official docs.
- [ ] Write the adapter document and test.
- [ ] Run checks and open a PR.

## Handoff

- State: Not started.
- Next step: Wait for owner approval on ASD-P1-004, then claim.
- Verify: `.venv/bin/python -m unittest discover -s tests -v`, `.venv/bin/python scripts/check_framework.py`, `.venv/bin/python scripts/check_publication.py --mode worktree` (also `--mode index` and `--mode history`) and `python3 scripts/tickets.py check`
- Gotchas: PUBLIC_FILES.json is shared by many tickets: add one line and rebase if another PR added a neighbouring line. Do not edit README.md.
- Open questions: None.

## Log

- 2026-11-06 claude/opus-5.5: created during ticket workflow installation.
