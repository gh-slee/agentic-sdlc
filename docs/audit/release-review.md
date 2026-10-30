# Initial release review

## Licensing and dependencies

Original framework work uses the canonical Apache-2.0 license fetched over verified TLS from apache.org. NOTICE and THIRD_PARTY_NOTICES preserve authorship/source acknowledgment; the source workflow MIT notice is retained. No competing framework code or downloaded skill is vendored. All seven inspected research license files and exact hashes/revisions are recorded; BMAD trademark/API classification differences are explicit.

The isolated validation environment installs six exact dependency versions with published wheel hashes, using --require-hashes and --only-binary. Installed wheel license text was inspected: five MIT packages and typing_extensions under PSF-2.0. Wheels/venv are ignored and excluded from distribution. OSV querybatch on 2026-10-30 returned no advisories for all six pinned versions. This is a point-in-time database check, not proof that vulnerabilities are absent.

Official checkout v7.0.1 and setup-python v7.1.0 resolve to recorded immutable commits. CI uses read-only contents, no persisted credentials, no privileged PR trigger and parses body text as data. No private source repository is required by CI.

## Review scope and limitations

Implementing-agent source review examined filesystem traversal, exclusive add-only writes, revision/hash binding, stale plans, interrupted writes, schema trust, exact PR body submission, policy precedence, single-writer guidance and absence of automatic external operations. Development-only tools and original mission state are excluded from adoption payloads. Independent QA/model behavioral evaluation was NOT RUN; self-review is not presented as independent.

Worktree/index/reachable-history scans and final full-suite results are recorded in development validation. The manifest lists every intended public path; no private source snapshot, virtual environment, owner override, financial input, session transcript or machine-specific path is authorized for publication. Pattern scanning supplements manual review. Publication remains pending until M10 remote verification.

## Acceptance coverage before publication

| Release criterion | Evidence |
|---|---|
| Domain independence and no source-domain core leakage | Structural checker, domain audit and five portability tests |
| Source rules classified; specialized safeguards retained | 36-rule matrix, 26-file pinned audit, disposable source guard rejection |
| Five roles, permissions and no unnecessary agents | Role contracts, core authority/ownership, no agents spawned |
| PR standard and truthful evidence | Template/skill, positive/negative/freshness/event tests; evidence limits explicit |
| New/existing adoption and local-rule preservation | Add-only real Git integration tests; exact bytes, conflicts and NOOP |
| Verifiable version provenance | Installed version/source commit/adapter/file hashes and installed-baseline smoke |
| Adoption/upstream structured review evidence | Two actual source analysis reports plus schema and synthetic examples |
| No paid API requirement | Coding-agent semantic review; no model API client in core |
| Cross-project deterministic validation | Five unrelated substrates; 56 tests pass in source and clean clone |
| New-session and interruption recovery | Twelve required scenarios, extra negatives, fresh process and real clean-checkout diagnostic |
| External side-effect reconciliation | Unknown/empty/matching/divergent remote diagnostic tests; no blind retries |
| Security and licensing | Public manifest/index/history scans, dependency license/hash review and least-privilege CI |
| Public publication | PENDING M10 actual remote verification; no completion claimed yet |

Executed candidate revision: ed560ad. Full suite: 56 passed, 0 failed/errors, 0 skipped, 37.535 seconds on macOS CPython 3.12. A clean committed clone independently reran the same 56 tests successfully without ignored files. Installed core/PR/report validators and discovery passed; licenses present; development/private content excluded; repeated install returned NOOP. These are implementing-agent executed tests, not independent QA.
