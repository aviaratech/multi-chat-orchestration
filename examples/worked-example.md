# Worked example: two leads, three issues

All names, identities, issue numbers, and revisions here are fictional.

The operator requests invocation A for example/app#12 and invocation B for
example/app#13 plus example/library#14. Both outcomes end at approved PRs;
merging and deploying are outside the grant. The operator explicitly authorizes
creating each issue task and worktree. Each lead records its outcome and sources.

The leads register unique invocation keys through the locked registry helper.
The selected owner and reviewer models are recorded in their native contracts.

```json
{
  "schemaVersion": 1,
  "outcomes": {
    "invocation:fictional-a": {
      "lead": {"hostId": "local", "threadId": "lead-a", "epoch": 1},
      "issueTasks": [
        {"hostId": "local", "threadId": "owner-12", "provider": "github.com", "repository": "example/app", "issue": 12}
      ]
    },
    "invocation:fictional-b": {
      "lead": {"hostId": "local", "threadId": "lead-b", "epoch": 1},
      "issueTasks": [
        {"hostId": "local", "threadId": "owner-13", "provider": "github.com", "repository": "example/app", "issue": 13},
        {"hostId": "local", "threadId": "owner-14", "provider": "github.com", "repository": "example/library", "issue": 14}
      ]
    }
  }
}
```

Lead-a dispatches task `12`, binding its observed host, task, prepared worktree,
source revision, authority, acceptance, and review route. Lead-b does the same
for tasks `13` and `14`. Sharing example/app does not share ownership. Task 12
must not switch leads when lead-b becomes the most recent active task.

Owner 12 implements, checks its diff, and runs the required verification. It
starts one fresh, read-only reviewer child. A correctness finding leads to a
fix and re-verification; the same reviewer closes the exact corrected state.
Owner 12 opens the authorized PR and records retained worktree disposition.

Before sending, owner 12 resolves its complete source identity within invocation
A. It sends lead-a one completion receipt, including the current epoch, PR and
revision, check results, updated review acceptance, and cleanup/retention proof.
A local final answer alone is not notification. A repeated copy of the same
receipt does not authorize a second acceptance or duplicate downstream action.

Lead-a checks all its bound children, validates owner 12's evidence, accepts the
approved-PR outcome, archives the task, and removes its binding with the helper.
It never merges the PR without authority. Lead-b's entries and pending decisions
remain intact throughout the update.

If owner 13 needs an artifact from issue 12, it tells lead-b. Lead-b coordinates
the exact dependency with lead-a; neither lead directs the other's children.
An artifact handoff transfers evidence, not issue ownership or merge permission.

If lead-b hands its invocation to lead-c, only B's epoch increments. The handoff
snapshot includes child cursors and pending decisions. During one declared,
bounded reconciliation window, eligible old-epoch messages are reconciled once;
after its deadline, late messages require current-binding source reconciliation.
An unavailable child does not keep that window open indefinitely. A's bindings
are unaffected.
