# Evidence and quality

Map acceptance and negative cases to actual verification. Record source/base/HEAD, environment, fixture/oracle revision, command, outcome, pass/fail/skip counts, public-safe evidence references, defects and limitations. Use PASS, FAIL, NOT RUN or PENDING accurately; skips do not prove coverage. Refresh evidence affected by material code, baseline or fixture changes.

Developer self-tests, self-review, independent QA, architecture review, CI, human acceptance and publication consent are distinct. Independent QA requires an independent reviewer and expectations derived independently where required; a different model name is insufficient. If no independent execution occurred, report NOT RUN. A deterministic schema/format pass authenticates neither test results nor human approvals.

Keep documentation aligned with implemented behavior and commands. Include synthetic visual evidence where an interface change needs it. Public artifacts exclude private approval records, transcripts, credentials, local paths and real user data. Review dependency provenance, licenses, symlinks, staged/tracked content and reachable history before public publication. Pattern scanners supplement manual review and do not prove absence of sensitive information.
