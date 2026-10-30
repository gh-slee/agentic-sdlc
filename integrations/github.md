# GitHub integration

Copy the reusable PR template deliberately or use sdlc-pr-write; adoption never replaces an existing template. Validate `scripts/check_pr.py --body-file FILE --head FULL_SHA`, then send those exact bytes with `gh pr create --body-file FILE`, `gh pr edit --body-file FILE` or an explicit supported API body. Read back the result and follow host-required PR attachment behavior. Validation alone creates no PR.

CI checks policy structure, tests, PR body shape/freshness and public worktree/index/history. Actions are pinned official commits with read-only contents and no persisted credentials. PR metadata names the branch head, not a synthetic merge SHA. Edits/synchronization retrigger checks. Changed code requires evidence/body revision refresh; CI format does not authenticate test truth or consent.

Before remote writes inspect auth, exact owner/name, credential-free fetch/push URLs, visibility, branches, commits and ancestry. Record intended side effects. Existing empty remote means creation may already have succeeded; matching SHA means verify rather than push again. Unknown/auth failure is not absence. Divergence needs review, never force-push. Initial publication is distinct from feature PRs, tags/releases, merge and deployment.
