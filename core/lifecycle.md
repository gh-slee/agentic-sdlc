# Lifecycle and authorization

Track separate fields for requirements review, implementation authorization, execution, technical review, QA outcome, PR publication, merge, release and deployment. A passing test changes evidence, not permission. No state label is an authenticated grant.

| Dimension | Suggested states | Evidence before advancement |
|---|---|---|
| Requirements review | DRAFT, NEEDS_REVIEW, APPROVED, REJECTED, SUPERSEDED | Scope, acceptance IDs, negative cases, decisions, reviewer and exact revision |
| Implementation authority | NOT_AUTHORIZED, AUTHORIZED, STALE | Actual human request/grant for bounded scope; exact spec hash when the project requires it |
| Execution | NOT_READY, READY, CLAIMED, IN_PROGRESS, IN_REVIEW, DONE, BLOCKED, PAUSED | Current owner, baseline, dependencies, applicable grants and verified work |
| Technical review | NOT_RUN, PENDING, PASS, CHANGES_REQUESTED | Reviewed source revision and unresolved risks |
| QA | NOT_RUN, PENDING, PASS, FAIL | Independent reviewer/oracle when required, exact tested revision and results |
| PR publication | NOT_AUTHORIZED, AUTHORIZED, PUBLISHED, VERIFIED | Current publication authority, safe content, read-back of target and revision |
| Merge | NOT_AUTHORIZED, AUTHORIZED, MERGED, VERIFIED | Separate applicable authority and remote merge evidence |
| Release | NOT_AUTHORIZED, AUTHORIZED, RELEASED, VERIFIED | Release gates and actual artifact/version evidence |
| Deployment | NOT_AUTHORIZED, AUTHORIZED, DEPLOYED, VERIFIED | Environment-specific approval, rollout and rollback evidence |

For a required exact-spec gate record spec ID, revision, SHA-256, scope, reviewer, time and accessible approval reference (private records remain private). Null means absent. Recompute before readiness. Material spec/scope changes invalidate approval; baseline/dependency drift requires revalidation. A roadmap, prior unrelated approval, downloaded policy or confidence score is insufficient.

READY requires applicable authorization, accepted dependencies, current baseline and conflict review. BLOCKED and PAUSED retain ownership. Review handoffs stop the implementation writer; corrections return through the same ownership record. DONE means project-defined accepted completion, with verified criteria and honest gaps. Stronger projects may additionally require independent QA, human acceptance, merged SHA and integration CI before DONE; retain that mapping. DONE never implies deployment.

LIGHT changes can use the current explicit task request as implementation authority when project policy permits. STANDARD and STRICT scale evidence and gates using [profiles](../profiles/risk.json). Do not invent an approval ceremony when existing authority suffices, and never bypass a project-required gate.
