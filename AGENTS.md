# Agentic SDLC repository instructions

For ordinary contributions, read `CONTRIBUTING.md` and task-relevant core/workflow guidance; the initial-build mission is complete. For initial-mission recovery or evidence reconciliation, read `CHARTER.md`, `IMPLEMENTATION_STATE.md`, `IMPLEMENTATION_PLAN.md`, `DECISIONS.md`, `VALIDATION.md`, and `RECOVERY.md` under `docs/development/`. Git and filesystem evidence override notes. Preserve existing work.

Only this repository is writable under the initial mission. The reference repository is read-only; inspect tracked workflow files only, never private owner instructions or real user data. Do not spawn independent writers, alter global agent settings, merge, deploy, or modify other repositories.

Use English for public artifacts. Keep source-specific audit details in ignored `.local/`. Never commit secrets, private findings, session transcripts, or machine-specific paths. No public push until licensing, security, and mandatory tests pass. Authorized initial publication target: `gh-slee/agentic-sdlc`, public, branch `main`; inspect remote reality before retries. This authorization does not extend to other repositories.

Work in bounded units: implement, verify, record actual evidence, update state, inspect diff, commit locally, identify next task, continue. Distinguish planned, implemented, tested, verified, and published. Self-review is not independent QA. Do not invent approvals or test outcomes.

The implementation checkpoint documents govern this initial build, not every adopting repository. Core policy is loaded on demand once implemented. Use the desktop app Local workspace and integrated terminal; no Codex CLI session-resume dependency or computer-use permissions are needed.

## Tickets and parallel agents

All planned and in-progress work is tracked in [tickets/](tickets/README.md), one
Markdown file per ticket; [tickets/ROADMAP.md](tickets/ROADMAP.md) orders it. Several
agents (any vendor or model) may work at once, one ticket each:

- Find work with `python3 scripts/tickets.py next --tier <any|standard|frontier>`;
  claim it with `python3 scripts/tickets.py claim <ID> --agent <tool/model> --worktree`
  and work only in that ticket's worktree and branch. Never take a live claim or a
  ticket whose resources another live claim holds.
- Read the ticket's Handoff first. Keep Handoff current, commit and push the ticket
  branch, and run `heartbeat` at every checkpoint, because a usage limit can stop you
  at any time. Resume someone else's stale claim with `resume` and `takeover`.
- Edit only your own ticket file; file new tickets for follow-ups. `gate: owner`
  tickets need recorded owner approval before work starts. Use the claim's
  `isolation_id` and `port_base` for Docker, databases and ports.
- This section governs ordinary contributions after the initial mission. It does not
  widen publication, merge or spawning limits above; agents start only when the owner
  starts them. Ticket statuses map to execution states in `core/lifecycle.md` only;
  see ADR-002 in `docs/development/DECISIONS.md` and the gotchas in `tickets/README.md`.
