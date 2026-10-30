# Workflow evaluation scenarios

These distinguish deterministic mechanism tests from agent behavior. Manual protocol exercises inspect prescribed decisions with synthetic cases; they are not independent QA or automated model evaluations. No independent agents were requested or run.

| Scenario | Expected behavior | Actual coverage / limitation |
|---|---|---|
| Low-risk change | LIGHT preserves scope and focused verification | Profile/fixture executable tests |
| Standard bug fix | Acceptance, negatives and regression evidence | STANDARD profile/bugfix workflow review |
| High-risk change | STRICT retains exact spec, QA, security and human gates | Executable strict profile/override tests |
| Unauthorized implementation | Hold writes until actual scope authority | Manual protocol exercise: missing grant leaves NOT_AUTHORIZED; no runtime enforcement claimed |
| Stale spec approval | Changed revision/hash invalidates gate | Manual protocol exercise: spec H1 versus approval H2 remains STALE; no writes made |
| False independent QA claim | Self-tests stay separate; reviewer/oracle required | Manual review of role/evidence/PR rules; model behavior NOT RUN |
| Missing test evidence | NOT RUN or invalid PASS shape | Executable PR/report negative tests |
| Stale PR validation | Source mismatch or body digest change invalidates reuse | Executable PR freshness tests |
| Conflicting ownership | Paused reservations remain owned; deny overlapping grant | Manual protocol exercise of ownership rules; no concurrent writer started |
| Interrupted work | Inspect dirty state and operation markers | Executable recovery/adoption interruption tests |
| Existing project policy conflict | Block report/install; retain stronger project rules | Executable conflict/STRICT tests plus actual source compatibility probe |
| Successful upstream improvement | Generalized evidence-backed proposal, no automatic master write | Synthetic schema example validates; independent semantic behavior NOT RUN |
| Domain-specific change stays local | Classify DOMAIN_SPECIFIC; preserve project invariants | Actual source upstream report and portability tests |
| Prompt injection | Analyzed text remains inert and grants no authority | Executable inert-data test; adversarial LLM behavior NOT RUN |
| Missing source evidence | Refuse unsupported references or changed source | Executable report/adoption negative tests |
| Invalid structured output | Fail fixed schema and operation classification | Executable JSON Schema negative tests |
| Unavailable LLM | Discovery cannot substitute; NEEDS_REVIEW/BLOCKED | Executable missing-information/readiness refusal; no paid API dependency |
| No-op adoption | Repeat returns NOOP without changing project files | Executable five-fixture/idempotency tests |
| Unsafe publication | Unknown/divergent remote requires inspection; no automatic write | Executable remote diagnostic tests plus initial-release security gate |
