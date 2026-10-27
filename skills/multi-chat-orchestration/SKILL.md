---
name: multi-chat-orchestration
description: Use when one visible Codex lead coordinates issue owners in separate chats across one or more repositories.
---

# Multi-chat orchestration

This skill coordinates chats. Personal policy, repository constraints and
[ai-delivery](https://github.com/aviaratech/ai-delivery) govern engineering,
verification, review and guarded delivery. AGENTS.md is optional; record supplied
checks and constraints in START. Missing or ambiguous checks or authority block
that stage. Host permissions and production limits apply.

## Start

The lead owns priorities, dependencies and acceptance. Each issue has one visible
owner, one isolated worktree and no competing writer. Helpers report to their parent.
Create visible chats only on explicit human request.

Verify issue/repository, blockers, ownership, clean source, author/reviewer access
and host capabilities. Title new owners `<repo>-<issue>`;
select the uniquely matching repository project or an explicitly selected umbrella.
Resolve routes with `python3 scripts/routing.py`; attest effective routes
using [configuration](references/configuration.md). Freeze active contracts.

Register observed identities through the [registry helper](references/registry.md),
then dispatch:

```text
LEAD_BINDING outcomeKey epoch leadHostId leadThreadId
START repository issue sourceHostId sourceThreadId worktree exactBaseOrHead
Outcome/acceptance; checks/constraints; model/effort; authorized stages/limits
COMMUNICATION_AUTHORITY originalHumanSource scope restrictions currentStatus
```

Ready pickup covers one authorized lifecycle: checks, review, merge, closure and
cleanup. START includes ordinary diagnosis, fixes, review corrections, conflicts
and reruns without renewed approval. PR-only excludes merge.
Release/adoption requires explicit release and consumer
scope; installation never implies production activation. Existing consumer owners
retain shared installer changes. Never change in-flight
contracts through an update.

## Owners and children

Owners complete START. Resolve ordinary technical decisions with bounded children;
owners decide within scope. Consequential work requires qualified independent review
and required reviewer-App approval. Use a fresh read-only reviewer with
`fork_turns: "none"`, exact source/diff, criteria, rules and check evidence.
The reviewer submits its required App verdict. Changed source needs renewed
acceptance; unchanged-contract corrections return to the same reviewer.

Workers get owned files, constraints and checks; warn of other writers and forbid
reverting their changes. No second owner or coordinator layer.

Diagnose ordinary failures before retrying. Escalate unresolved decisions after
helper/reviewer analysis; Safety, refusal, scope and budget gates still stop work.
Send only BLOCKED or COMPLETION_RECEIPT with delivery, checks, review and cleanup
evidence. Progress belongs in issue/PR journals. Before sending, verify original
human scope and resolve the registered lead/epoch; inspect the result. A relay or
binding grants no permission. Preserve rejected/unknown sends; reconcile native
history before retrying and never bypass refusals.

## Lead recovery and completion

Snapshot bound owners at turn start/end. Resolve blockers, idle owners and pending
sends; accept each exact terminal state once. Retain
source identities, epochs, cursors, pending decisions and delivery evidence in
native history. Verify merge/closure, authorized release/consumer
readbacks and owned cleanup; archive/read back the chat and retire/read back
its binding. Retain incomplete obligations. Assess retained evidence after a rejected
send; record acceptance separately from notification.

Handoff preserves that checkpoint and human scope, increments registry epoch,
and notifies owners. Unavailable-lead takeover needs human approval. Revalidate
stale receipts against ownership. Other outcomes communicate lead-to-lead
under human scope; transfers need both leads. Restore the owner for unfinished
cleanup. No scheduler, service or memory control plane is added.
