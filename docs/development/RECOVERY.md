# Resume safely in a new desktop chat

Use: "Resume development of agentic-sdlc from its persisted implementation state. Verify repository and Git reality, identify the next incomplete task, and continue following the existing architecture, security boundaries, and acceptance criteria. Do not restart completed work."

1. Open this project in the desktop app Local workspace. Verify `git rev-parse --show-toplevel` is the intended agentic-sdlc checkout; inspect applicable AGENTS.md.
2. Read CHARTER.md, IMPLEMENTATION_PLAN.md, IMPLEMENTATION_STATE.md, DECISIONS.md, VALIDATION.md here. Conversation history, Goals and model identity are unnecessary.
3. Inspect `git status --short`, `git branch --show-current`, `git rev-parse HEAD`, `git log -5 --oneline`, and `git diff`. Compare reality to the recorded anchor. Do not reset, clean, overwrite, or stash unknown work.
4. Missing/stale state or a DONE claim without artifacts and test evidence requires reconstruction, not trust. Identify the earliest incomplete or invalidated task from the plan and source. Retain completed work.
5. Check running processes and ignored `.local/` operation records before retrying tests, installs, commits, or adoption. An interrupted test is NOT RUN/UNKNOWN until completed. Inspect staged diff and history before committing; do not create duplicate commits if the original succeeded.
6. Revalidate assumptions only where drift or changes matter. Do not repeat valid audits or expensive tests unnecessarily. Record exact revision, commands, counts, limitations, and next safe action.
7. For adoption, inspect destination/manifest/journal and preserve user content before rerunning. Never treat partial files as successful adoption.
8. For publication, verify authentication, target owner and visibility, origin URL, branch list, remote HEAD and commit ancestry before create/push. Missing success output is not failure evidence. If remote exists with matching local SHA, verify rather than push again; if empty, push only the authorized branch; divergent or unrelated history requires review, never force-push. Unknown/authentication failure is not absence.
9. Continue next authorized incomplete task, verify, update state/evidence, review security/diff and create a local checkpoint. Record its SHA as the next anchor. Continue while permitted. No background resumption after usage reset is assumed.

Initial publication alone is authorized after release gates; other external writes, delegation, merges and deployments need their own authority. Source repository stays read-only. Stronger project rules are preserved.
