---
name: multi-chat-orchestration
description: Use when one visible Codex lead coordinates issue owners in separate chats across one or more repositories.
---

# Multi-chat orchestration

This skill owns chat coordination. Personal policy, repository constraints and
[ai-delivery](https://github.com/aviaratech/ai-delivery) govern engineering,
verification, review and guarded delivery. AGENTS.md is optional; record supplied
checks and constraints in START. Missing or ambiguous checks or authority block
that stage. Actual host permissions and production limits always apply.

## Start

The lead owns priorities, dependencies, decisions and acceptance. Each issue has
one visible owner, one isolated worktree and no competing writer. Helpers report
only to their immediate parent. Create visible chats only on explicit human request.

Verify canonical issue/repository, blockers, existing ownership, clean source,
author/reviewer access and host capabilities. Title new owners `<repo>-<issue>`;
select the uniquely matching repository project or an explicitly selected umbrella.
Resolve models/efforts with `python3 scripts/routing.py`; attest effective routes
using [configuration](references/configuration.md). Freeze active contracts.

Register observed identities through the [registry helper](references/registry.md),
then send:

```text
LEAD_BINDING outcomeKey epoch leadHostId leadThreadId
START repository issue sourceHostId sourceThreadId worktree exactBaseOrHead
Outcome/acceptance; checks/constraints; model/effort; authorized stages/limits
COMMUNICATION_AUTHORITY originalHumanSource scope restrictions currentStatus
```

START covers listed stages and ordinary corrections, conflicts and reruns.
PR-only excludes merge. Release/adoption requires explicit release and consumer
scope; installation never implies production activation. Existing consumer owners
retain shared installer changes. Never change in-flight
contracts through an update.

## Owners and children

Owners implement, verify, correct, publish, obtain independent review, deliver and
clean up within START. Consequential work requires qualified independent review
and any required reviewer-App approval. Use a fresh read-only child with
`fork_turns: "none"`, exact source/diff, criteria, rules and check evidence.
The reviewer submits its own required App verdict. Changed source needs renewed
acceptance; unchanged-contract corrections return to the same reviewer.

A bounded worker gets owned files, constraints and checks; tell it other writers
exist and forbid reverting their changes. No second owner or coordinator layer.

Owners send only BLOCKED for an unresolvable decision, or COMPLETION_RECEIPT
with exact delivery, checks, review and cleanup evidence. Progress belongs in
issue/PR journals. Before sending, verify original human communication scope and
resolve the current registered lead/epoch; inspect the send result. A relay or
binding grants no permission. Preserve rejected/unknown sends; reconcile native
history before retrying and never bypass refusals.

## Lead recovery and completion

At turn start/end, snapshot every bound owner. Resolve blockers, reconcile idle
owners and pending sends, and accept each exact terminal state once. Retain
source identities, epochs, cursors, pending decisions and delivery evidence in
native history. Verify merge/closure, any authorized release and consumer
readbacks, then owned cleanup; archive/read back the chat and retire/read back
its binding. Retain incomplete obligations. Assess retained evidence after a rejected
send; record acceptance separately from notification.

Handoff preserves that checkpoint and human scope, increments registry epoch,
and notifies owners. Unavailable-lead takeover needs human approval. Revalidate
stale receipts against current ownership. Other outcomes communicate lead-to-lead
under human scope; transfers need both leads. Restore the same owner for unfinished
cleanup. No scheduler, service or memory control plane is added.
