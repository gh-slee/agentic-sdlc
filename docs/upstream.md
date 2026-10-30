# Upstream promotion

Use sdlc-upstream-review to compare a relevant public project improvement with its pinned installed framework commit. Classify evidence-backed findings as universal, optional, adapter, framework bug, project/domain-only, security regression, conflicting, no reusable change or needs review. Explain generalization, compatibility and regression tests. Validate the report with `.venv/bin/python scripts/check_report.py REPORT.json`.

Project/domain-specific rules stay local. Security regressions and blocking conflicts stay BLOCKED; missing evidence or an unavailable semantic reviewer stays NEEDS_REVIEW/BLOCKED. NO_REUSABLE_CHANGE is a valid outcome. Do not invent an upstream change to fill a report.

Present a concrete proposal for human review. This skill does not edit or push the master. A separately authorized normal contribution uses a bounded branch/fork, actual tests/docs, exact validated PR body and supported GitHub tools. Maintainers decide acceptance; publication does not imply merge, release or deployment authority. Automated discovery is future work.
