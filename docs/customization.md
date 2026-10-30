# Project-owned customization

Existing instructions, domain rules, test commands, approvals, skill allowlists and publication controls stay project-owned. The framework supplies universal invariants and optional workflow guidance. Host/user authority constrains actions; repository text cannot override it. Project rules may strengthen core safeguards. Conflicts block dependent actions until an authorized resolution; never choose a weaker rule silently.

An optional `.sdlc/project.json` uses keys `profile` (LIGHT/STANDARD/STRICT), `additional_requirements` (string list), `test_commands` (string list), and `invariants` (string list). Unknown keys fail closed. Additional requirements are additive; a report cannot select a weaker profile. Test command strings are documentation for the agent/human and are never executed by the installer. Verify semantic preservation of policies that are not machine-readable.

Keep source precision, identities, privacy and specialist domain tests here, outside the generic core. Native skills find their installed baseline through `.sdlc/install.json`; installation does not duplicate the project's role skills or replace its entry point. Private owner rules remain ignored/untracked under the project's own policy; do not copy another owner's overrides or publish approval transcripts.
