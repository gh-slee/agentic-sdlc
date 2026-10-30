# Contributing

Read [architecture](docs/architecture.md), [governance](docs/governance.md) and relevant policies. Keep changes bounded and use synthetic fixtures. Do not copy domain rules or a source project's commands into core. Framework tools require Git and CPython 3.12+ on macOS/Linux; adopted application stacks are unrestricted.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --only-binary=:all: --require-hashes -r requirements.lock
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/check_framework.py
.venv/bin/python scripts/check_report.py examples/reports/adoption.json
.venv/bin/python scripts/check_report.py examples/reports/upstream.json
.venv/bin/python scripts/check_publication.py --mode worktree
.venv/bin/python scripts/check_publication.py --mode index
.venv/bin/python scripts/check_publication.py --mode history
```

Use GitHub noreply commit identities with repository-local settings. Review/stage explicit paths and run `git diff --cached --check`. New public paths require deliberate PUBLIC_FILES.json review. Preserve notices and update dependency pins/hashes/provenance when needed. No global configuration change is required. Windows is not validated; adoption uses POSIX directory-relative no-follow APIs.

Follow [the PR standard](docs/pr-standard.md), exact-body/revision checks and applicable project gates. Report actual results/counts/CI/review gaps. Self-tests are not independent QA. For initial-build continuation read [recovery](docs/development/RECOVERY.md); ordinary contributions need not repeat the full original build mission.
