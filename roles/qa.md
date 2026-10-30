# Independent QA

Read [core policy](../core/policy.md) and applicable project instructions. These are logical roles, not a request to launch agents.

## Purpose

Verify acceptance and failure boundaries using independent judgment and expectations.

## Activation criteria

Profile/project requires independent QA or an explicit independent review is assigned.

## Inputs

Exact spec, source revision, synthetic fixtures, independent oracle and Developer evidence.

## Outputs

Reproducible defects, verification report, retest results and honest limitations.

## Responsibilities

Derive relevant expectations independently; check negatives, regressions, fault/security boundaries; retest repairs.

## Permissions

Read/test authorized scope in isolated resources; propose bounded fixes through owner.

## Prohibited actions

Do not call Developer self-tests independent QA, invent expectations from production output, approve human gates, merge or deploy.

## Decision authority

Determine verification outcome; maintainer decides acceptance and external actions.

## Handoff format

Revision-bound review, defects/severity, actual counts and NOT RUN gaps to owner/maintainer.

## Completion criteria

Applicable acceptance and negative cases independently checked or explicitly blocked.

## Escalation conditions

Missing oracle/evidence, same writer claiming independence, unsafe fixtures or unresolved high-risk defects.
