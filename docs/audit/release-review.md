# Initial release review

## Licensing and dependencies

Original framework work uses the canonical Apache-2.0 license fetched over verified TLS from apache.org. NOTICE and THIRD_PARTY_NOTICES preserve authorship/source acknowledgment; the source workflow MIT notice is retained. No competing framework code or downloaded skill is vendored. All seven inspected research license files and exact hashes/revisions are recorded; BMAD trademark/API classification differences are explicit.

The isolated validation environment installs six exact dependency versions with published wheel hashes, using --require-hashes and --only-binary. Installed wheel license text was inspected: five MIT packages and typing_extensions under PSF-2.0. Wheels/venv are ignored and excluded from distribution. OSV querybatch on 2026-10-30 returned no advisories for all six pinned versions. This is a point-in-time database check, not proof that vulnerabilities are absent.

Official checkout v7.0.1 and setup-python v7.1.0 resolve to recorded immutable commits. CI uses read-only contents, no persisted credentials, no privileged PR trigger and parses body text as data. No private source repository is required by CI.

## Review scope and limitations

Implementing-agent source review examined filesystem traversal, exclusive add-only writes, revision/hash binding, stale plans, interrupted writes, schema trust, exact PR body submission, policy precedence, single-writer guidance and absence of automatic external operations. Development-only tools and original mission state are excluded from adoption payloads. Independent QA/model behavioral evaluation was NOT RUN; self-review is not presented as independent.

Worktree/index/reachable-history scans and final full-suite results are recorded in development validation. The manifest lists every intended public path; no private source snapshot, virtual environment, owner override, financial input, session transcript or machine-specific path is authorized for publication. Pattern scanning supplements manual review. Publication remains pending until M10 remote verification.
