---
name: sdlc-pr-write
description: Draft or refresh a PR description from the actual diff and verification evidence, then validate the complete body.
---

Locate the pinned baseline from `.sdlc/install.json` when adopted, or this framework checkout. Read its `templates/pull_request.md`, `templates/pr-standard.json` and `core/evidence.md`; preserve project-required review, privacy and publication gates.

Inspect actual base/head, full diff and current source/docs. Explain the problem and resulting behavior, group meaningful components, and gather revision-bound commands/results/counts, actual CI links and separately identified independent review. Missing checks are NOT RUN; real running CI is PENDING. Self-tests are not independent QA.

Write a complete public-safe body in an ignored local file. Set sdlc-head metadata to the reviewed full source SHA. Run the baseline's `scripts/check_pr.py --body-file <file> --head <reviewed-full-sha>` with Python. It checks shape/freshness, not factual truth or authority. Review its body digest, evidence and conditional sections.

If publication is authorized, send the exact validated bytes using `gh pr create --body-file`, `gh pr edit --body-file` or the explicit API body field. Read back the result. Never assume GitHub inserts the template for an explicit body. After material implementation/review changes, refresh the complete description and revision, rerun validation and review evidence before updating. This skill grants no remote-write, merge, release or deployment authority.
