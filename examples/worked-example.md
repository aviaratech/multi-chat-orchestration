# Worked example: two leads, three issues

All names, identities, issue numbers, and revisions here are fictional.

The operator requests invocation A for example/app#12 and invocation B for
example/app#13 plus example/library#14. Both outcomes end at approved PRs;
merging and deploying are outside the grant. The operator explicitly authorizes
creating each issue task and worktree. Each lead records its outcome and sources.
In original fictional native messages `human-a` and `human-b`, the operator also
authorizes each lead to instruct its own registered owners and those owners to
return blockers and terminal receipts to their current bound lead, including an
authorized successor. Each START retains a reference to that original human
source, its scope, restrictions and current status separately from lifecycle
authority and the registry. Those original human records also authorize the two
leads and their authorized successors to exchange concrete dependencies between
these invocations. Agent quotations alone cannot establish either approval.

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

Lead-a dispatches task `app-12` in the unique saved project for example/app,
binding its observed host, task, prepared worktree, source revision, authority,
acceptance, and review route. Lead-b dispatches `app-13` there. No saved project
matches example/library, so the operator explicitly selects one unambiguous
umbrella project for `library-14`; its registered repository remains
example/library. Sharing example/app does not share ownership. Task 12
must not switch leads when lead-b becomes the most recent active task.

Owner 12 implements, checks its diff, and runs the required verification. It
starts one fresh, read-only reviewer child. A correctness finding leads to a
fix and re-verification; the same reviewer closes the exact corrected state.
Owner 12 opens the authorized PR and records retained worktree disposition.

Before sending, owner 12 verifies its original human communication scope still
covers the action and resolves its complete source identity within invocation
A. It sends lead-a one completion receipt, including the current epoch, PR and
revision, check results, updated review acceptance, and cleanup/retention proof.
A local final answer alone is not notification. A repeated copy of the same
receipt does not authorize a second acceptance or duplicate downstream action.

If the host rejects an authorized return send, the owner retains the complete
unsent receipt, exact rejection, binding and human provenance in native history.
The lead authenticates that local result through its existing compact reconciliation
and applies the same evidence requirements, recording recovery separately from
delivery. Useful unrelated work continues. Neither participant claims a successful
send, repeatedly asks for the same approval, bypasses the host gate or requests a
duplicate send after recovery. Missing or revoked authority instead leaves only
the concrete missing permission to resolve through an authorized path.

Lead-a checks all its bound children, validates owner 12's evidence, accepts the
approved-PR outcome, archives the task, and removes its binding with the helper.
It never merges the PR without authority. Lead-b's entries and pending decisions
remain intact throughout the update.

If owner 13 needs an artifact from issue 12, it tells lead-b. Lead-b coordinates
the exact dependency with lead-a; neither lead directs the other's children.
An artifact handoff transfers evidence, not issue ownership or merge permission.

If lead-b hands its invocation to lead-c, only B's epoch increments. The handoff
snapshot includes child cursors and pending decisions. It preserves the original
human communication scope and source unchanged; this example's approval covers
the authorized successor. After the registry update, incoming lead-c resolves its
registered owners and sends their binding notifications under that scope.
An approval restricted to lead-b would need new human permission for sends to
lead-c. During one declared, bounded reconciliation window, eligible old-epoch
messages are reconciled once;
after its deadline, late messages require current-binding source reconciliation.
An unavailable child does not keep that window open indefinitely. A's bindings
are unaffected.
