# Implementation plan

All tasks P0. P1: optional Spec Kit integration/advanced updates/additional adapters. P2: orchestration, scheduling, dashboards. Follow charter scope boundaries. DONE requires actual verification, never documents alone.

| Task | Work unit | Depends on | Acceptance / verification | Status |
|---|---|---|---|---|
| M0.1 | Foundation and environment | none | Recovery documents exist; actual environment recorded; fresh-session review succeeds | DONE |
| M0.2 | Initialize safe Git checkpoint | M0.1 | Reviewed public-safe initial commit on main | DONE |
| M1.1 | Tracked source audit and provenance | M0.2 | Material workflow files and representative PR evidence inspected | DONE |
| M1.2 | Preservation matrix and boundaries | M1.1 | Every material rule classified with enforcement and migration risk | DONE |
| M2.1 | Current framework research | M1.2 | Seven official frameworks and modern Spec Kit features compared | DONE |
| M2.2 | Build versus reuse ADR | M2.1 | Minimal architecture and licenses justified | DONE |
| M3.1 | Core roles profiles lifecycle workflows | M2.2 | Five complete role contracts and distinct lifecycle/authority states | DONE |
| M3.2 | Structural conformance checks | M3.1 | Core references metadata profiles and override boundaries tested | DONE |
| M4.1 | PR template skill validator | M3.2 | Mandatory sections and evidence states validated with fixtures | DONE |
| M4.2 | PR workflow regression tests | M4.1 | Valid invalid stale/missing evidence cases pass expected assertions | DONE |
| M5.1 | Review skills and structured contract | M4.2 | Adoption/upstream read-only workflows and schema implemented | DONE |
| M5.2 | Structured report examples and negative tests | M5.1 | Invalid evidence classifications injection and unavailable model handled | DONE |
| M6.1 | Controlled adoption and provenance | M5.2 | New/existing/no-op/partial adoption preserve local files | DONE |
| M6.2 | Safe updates and rollback documentation | M6.1 | Pinned version commit hashes and reviewed manual update path demonstrated | DONE |
| M7.1 | Five portability fixtures and domain audit | M6.2 | CLI frontend API infrastructure docs fixtures use same core | DONE |
| M7.2 | Reference compatibility simulation | M7.1 | Disposable tracked workflow copy retains stricter controls and allowlists | DONE |
| M8.1 | Recovery diagnostic and scenarios | M7.2 | All twelve mandatory recovery scenarios exercised | DONE |
| M8.2 | Context-free recovery exercise | M8.1 | Artifacts alone identify safe next task without destructive operations | DONE |
| M9.1 | Open-source docs licensing CI | M8.2 | All required guides license notices and least-privilege CI reviewed | DONE |
| M9.2 | Full tests and publication security gate | M9.1 | Tracked/staged/history/secrets/paths/symlinks/dependencies reviewed | DONE |
| M10.1 | Reconcile remote and publish | M9.2 | Correct authenticated owner; create/push only incomplete authorized steps | IN_PROGRESS |
| M10.2 | Verify public publication | M10.1 | Visibility default branch SHA README LICENSE CI remotely confirmed | TODO |
