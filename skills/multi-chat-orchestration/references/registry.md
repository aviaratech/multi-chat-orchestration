# Local registry operations

`~/.codex/orchestration/outcomes.json` is the shared-filesystem recovery index.
Only leads write it, through `python3 scripts/registry.py`; run `--help` for
arguments. All writers share its adjacent lock; never delete that lock.
The helper checks identities, not permission. Keep real entries private.

Use `show` to observe an entry. New invocations get unique `invocation:<UUID>`
keys; schema 1 and existing keys stay unchanged. `update` compares an exact
expected JSON entry with its replacement, locks, preserves unrelated invocations,
rejects duplicate ownership and reads back. Creation expects `null`. Stale state
requires reconciliation before retrying; after uncertain writes, read current state.

Use `resolve` with outcome, source host/thread, provider, repository and issue
before sending. Verify original human communication scope separately. Never guess
a recipient after failure.

Handoff preserves owners and increments epoch. Unavailable-lead takeover requires
human approval before `--authorized-takeover`. Remove an owner only after terminal
acceptance, cleanup and archival readbacks. Retire an empty invocation separately;
absence alone proves none of those steps.
