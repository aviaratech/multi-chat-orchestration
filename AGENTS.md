# Maintainer instructions

Keep this package limited to a portable Codex workflow, safe installation,
examples, and validation. Do not add a service, private memory dependency,
automatic model switching, or machine-specific policy.

Run `python3 -m unittest discover -s tests -v` and `git diff --check` for changes.
Workflow, authority, identity routing, review, and installer changes require
independent read-only review. Forward-test changed coordination behavior with
a fresh bounded subagent using fictional inputs and no external side effects.
Preserve actual review and test evidence outside public source; include only
sanitized validation results and reproducible scenarios in this repository.

Never commit runtime bindings, real task identifiers, receipts, transcripts,
credentials, personal policy files, or private project artifacts. Public
examples must be visibly fictional. Repository publication does not authorize
actions against any repository used as an example.
