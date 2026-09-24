# Local registry operations

Use Python 3.11+ on macOS/Linux. All participating tasks need the same local
registry path; all writers must use this helper and its adjacent `.lock` file.
Do not remove the lock file to clear a wait: file locks release when the process
exits. This is not a multi-host locking protocol, authentication, or a service.

The normal registry is `~/.codex/orchestration/outcomes.json`. Runtime entries
contain private task identities; never commit them. Obtain identities from native
tools, not example values or task titles. Schema 1 and existing outcome keys are
retained. New invocations use a generated unique `invocation:<UUID>` key.

From the installed skill directory, inspect one entry:

```bash
python3 scripts/registry.py --registry "$HOME/.codex/orchestration/outcomes.json" \
  show --outcome 'invocation:fictional-release-a'
```

The following examples contain fictional identities. Use private temporary JSON
files for an exact previously observed entry and its proposed replacement. For
creation, expected JSON is `null` and the lead starts at epoch 1. For retirement,
replacement is `null` and the current entry must have no remaining issue owners.

```bash
python3 scripts/registry.py --registry "$HOME/.codex/orchestration/outcomes.json" \
  update --outcome 'invocation:fictional-release-a' \
  --actor-host local --actor-thread fictional-lead-a \
  --expected /tmp/example-expected.json --replacement /tmp/example-next.json
```

`update` locks, re-reads, validates the expected entry and actor, changes only the
named invocation, validates global ownership, and atomically writes and reads
back. Other invocations are preserved. A stale expected entry requires fresh
reconciliation, not automatic retry with an overwritten snapshot. The helper
trusts the supplied actor identity; policy and original approvals supply authority.
If a write reports failure after replacement, read current state before retrying.

A lead handoff changes only that invocation's lead and increments its epoch once.
The current lead normally performs it. For an unavailable lead, an incoming lead
with separately verified operator approval may pass `--authorized-takeover` with
its own actor identity; issue owners must remain unchanged. Record approval and
the handoff snapshot in native history first. This flag grants no permission.

Before a child sends its receipt, resolve its exact binding:

```bash
python3 scripts/registry.py --registry "$HOME/.codex/orchestration/outcomes.json" \
  resolve --outcome 'invocation:fictional-release-a' \
  --source-host local --source-thread fictional-owner-12 \
  --provider github.com --repository example/app --issue 12
```

Send with the returned host/thread/epoch and inspect the tool result. A routing
failure means retain the pending message and resolve the identity gap; never
guess another lead. The recipient revalidates the binding when accepting, so a
handoff between resolution and delivery cannot grant stale authority.
