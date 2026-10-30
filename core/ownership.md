# Ownership and handoffs

One bounded task has one designated writer. A coordinator serially checks current reservations across active, paused and blocked work before granting ownership. Record task/spec revision, approved scope, base revision, owner/coordinator, branch/checkout, paths, contracts, exclusive resources, isolation identifiers, status and next action. Mark irrelevant resources with a reason.

Separate checkouts do not isolate external resources, services, ports, credentials, caches or shared schemas. Shared contracts need an integration owner and order. Issues and Markdown records are coordination evidence, not atomic locks or leases. When ownership disagrees or coordination is lost, stop dependent writes and reconcile.

Pause retains the claim regardless of elapsed time or quota reset. Transfer requires stopping the old writer and writing processes, fencing pending writes, inspecting diff/evidence, then recording old/new ownership and resources before a new grant. If stopping cannot be verified, keep the claim paused. A transferred former writer must not resume on the old grant.

Use the [handoff template](../templates/handoff.md). On resume inspect filesystem, Git and external state before retrying an operation; a missing success message is not failure evidence. Record test interruptions honestly. No scheduler or independent agent runtime is required.
