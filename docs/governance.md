# Governance

Maintainers own canonical core safeguards, schemas, profiles and release criteria. Projects own their stack, commands, domain constraints, stronger gates and custom instructions. Adapters own tool compatibility, never permission expansion. Link canonical policies instead of duplicating them.

Use SemVer with compatibility review for mandatory semantic/schema changes. Framework version, installed version, resolved commit, report-schema version, adapter version and project customizations are distinct. The initial source is 0.1.0, report schema 1.0.0, adapter codex-1. See [safe updates](versioning.md); no automatic upgrade or weakening path exists.

Contributions explain the problem and resulting behavior, preserve public/private boundaries, add appropriate positive/negative tests and use accurate PR evidence. Security-sensitive changes need maintainer review of trust boundaries, failures, compatibility and recovery. Required independent QA must be actual independent work; initial implementing-agent self-review is not independent QA.

Release criteria: implemented P0; reviewed preservation/domain audits; required tests/portability/recovery pass; gaps explicit; license/dependency provenance reviewed; tracked/staged/reachable-history safety checks pass; exact authorized target/visibility/branch/revision verified after publication. A source version file is not a tag, GitHub release or deployment. Advanced integrations and automation remain future work.
