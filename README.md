# Agentic SDLC

A reusable, domain-agnostic framework for engineering workflows, coding-agent roles, quality gates, PR standards and cross-repository governance. Codex is the first adapter; the core uses versioned files and needs no paid LLM API or orchestration service.

Use LIGHT for small reversible changes, STANDARD for ordinary development and STRICT for consequential changes. Retain your project's stronger approvals, domain invariants, tests and publication rules. Five logical role contracts guide work without automatically starting agents.

## Quick start

Clone this repository, select a reviewed commit and record `git rev-parse HEAD`. Framework tools require Git and CPython 3.12+ on macOS/Linux; adopted application stacks are unrestricted.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --only-binary=:all: --require-hashes -r requirements.lock
.venv/bin/python scripts/check_framework.py
.venv/bin/python -m unittest discover -s tests -v
```

Open this repository as a Local project in the Codex desktop app and use the relevant native skill:

- **sdlc-pr-write** drafts and validates a complete PR body against actual diff/evidence.
- **sdlc-adopt-review** produces an evidence-backed adoption proposal; read-only by default.
- **sdlc-upstream-review** proposes reusable improvements while keeping project/domain rules local; read-only by default.

For adoption, run `.venv/bin/python scripts/adopt.py discover --target PROJECT_ROOT`, produce a semantic report in the current agent session, validate it, review the deterministic file plan and apply only the exact authorized additions. See [the adoption guide](docs/adoption.md) for executable commands, new/existing repositories, safe repeats and interrupted installation. Existing AGENTS.md and project-owned rules are preserved. `.sdlc/install.json` records version, commit and file hashes. Use [the reviewed update/rollback path](docs/versioning.md); automatic upgrades are not implemented.

## Components

| Component | Entry point |
|---|---|
| Policy, lifecycle, ownership and evidence | [Core](core/policy.md) |
| Five logical roles | [Requirements](roles/requirements.md), [Architect](roles/architect.md), [Developer](roles/developer.md), [QA](roles/qa.md), [Coordinator](roles/coordinator.md) |
| Risk and project rules | [Profiles](profiles/risk.json), [customization](docs/customization.md) |
| PR format and integration | [PR standard](docs/pr-standard.md), [GitHub](integrations/github.md) |
| Structured review reports | [Schema](schemas/review-v1.schema.json), [examples](examples/reports/README.md) |
| Adoption and upstream promotion | [Adoption](docs/adoption.md), [upstream](docs/upstream.md) |
| Architecture and governance | [Architecture](docs/architecture.md), [governance](docs/governance.md) |
| Portability and preservation | [Domain audit](docs/audit/domain-independence.md), [matrix](docs/audit/preservation.md), [compatibility](docs/audit/compatibility.md) |
| Tests, security and recovery | [Contributing](CONTRIBUTING.md), [security](docs/security-model.md), [validation](docs/development/VALIDATION.md), [recovery tests](docs/recovery-validation.md) |

Validators check structure, consistency and selected filesystem/provenance boundaries. They do not prove semantic equivalence, human consent, test truth or independent QA. Pattern scans supplement manual content/history review. CI runs without write credentials. Portability substrates test governance integration, not full application builds. [Evaluation coverage](docs/agent-evaluations.md) separates executable checks from unrun independent/model behavior.

To resume initial framework development in a new chat, read [state](docs/development/IMPLEMENTATION_STATE.md), [charter](docs/development/CHARTER.md) and [recovery](docs/development/RECOVERY.md), then inspect actual Git/filesystem/remote state. No CLI session resume, global configuration, fixed model or automatic quota-reset continuation is required.

Original work is Apache-2.0; see [LICENSE](LICENSE) and [notices](THIRD_PARTY_NOTICES.md). Source version 0.1.0 does not imply a GitHub tag, release or deployment. Deferred P1: Spec Kit bundles/presets, advanced updates and more adapters/evaluations. P2: scheduled drift/discovery, automatic upgrade PRs, orchestration and dashboards.
