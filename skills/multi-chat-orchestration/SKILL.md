---
name: multi-chat-orchestration
description: Use when one visible Codex lead coordinates issue tasks, worktrees, native children, or delivery tracks across one or more repositories.
---

# Multi-Chat Orchestration

## Purpose

Each orchestration invocation has one operator-facing lead and an explicit
outcome. Multiple invocations may run in parallel, span repositories, or share
a repository. Each issue task belongs to exactly one invocation and lead.
Issue tasks work autonomously and contact the lead only when a decision
is genuinely unresolvable or delivery and cleanup are terminal.

Within an outcome, use one coordination workflow. Issue tasks invoke bounded
native reviewer or worker children directly; do not add a coordinator task or
a competing execution path.

Repository policy remains repository-owned. It supplies engineering, safety,
verification, review, merge, cleanup, production-authority, and tool-specific
rules. Operator and personal policies may impose additional requirements; this
skill never grants tool permissions or weakens governing instructions.

Before dispatch, confirm native task creation, reads, messages, bounded snapshots,
archival, direct subagents, GitHub access, and worktrees are available as needed.
Only create visible tasks when the operator explicitly requests task creation.
Without that authority, reuse an authorized existing owner or ask for the missing
authority. Do not silently replace unavailable tools with a new service.

All coordinated tasks must be able to read the same binding registry. This
release supports that shared-filesystem setup; separate hosts with divergent
local registries are unsupported.

## Topology and ownership

- One visible lead is the operator's coordination surface for its invocation.
- Invocation identity, not repository, task title, recency, shared working
  directory, memory scope, or the latest inbound sender, determines ownership.
  Starting another lead never implicitly takes over existing issue tasks.
- One mergeable issue has one visible task titled exactly `<repo>-<issue>`,
  fresh issue-specific context, and one prepared worktree. For new tasks, `repo`
  is the final path component of the verified issue-owning canonical repository,
  and `issue` is its native issue number. Do not use a product repository, project
  name, or role suffix in place of the issue owner. Existing task titles remain
  unchanged; titles are presentation, never routing identity.
- The issue task owns only that issue. It is the sole mutable owner of its
  implementation, verification, publication, review corrections, guarded
  delivery, terminal evidence, and cleanup when those stages are in scope.
- The lead owns outcome priority, architecture, cross-issue decisions,
  dependencies, capacity, handoff, receipt acceptance, and post-cleanup task
  archival. It does not duplicate the issue task's routine delivery work.
- Direct native children are invisible bounded helpers. They report only to
  their immediate parent and never contact the lead or operator.
- Never create a sibling implementation, second writer, manager layer, or
  alternate execution path for the same issue.

## Outcome contract

For a new invocation, resolve the operator's selected team and routing with
`python3 scripts/routing.py` from this skill's directory. See
[configuration](references/configuration.md) for the selected override file,
team selection, native profile setup, precedence, and model availability checks.
A team is reusable configuration, not an ownership or routing identity. Read
the resolved settings and attest actual host/profile support before dispatch;
record and freeze requested/effective routes in the invocation contract. An
existing invocation keeps its recorded settings unless explicitly rerouted.

Before dispatch, the lead records in native task history:

- operator outcome and the operational definition of delivered;
- current observable state and exact sources of truth;
- binary critical-path gates, owners, and the next proof;
- non-goals and authority boundaries;
- ETA assumptions and uncertainty;
- risks, stop conditions, and decisions still requiring the operator.
- selected team, configuration provenance, and requested/effective model routing.

Distinguish `built`, `verified`, `merged`, `deployed`, and
`operationally_delivered`. Do not substitute an earlier component state for the
requested outcome.

Every active issue must close a named outcome gate or an independently valuable
operator-approved result. Do not create work merely to keep tasks busy. A
second substantive workaround at the same owner triggers an Edge Pause:
identify the canonical owner, replace the wrong path, and retire the superseded
active source, test, documentation, and metadata before continuing.

## Binding registry

`~/.codex/orchestration/outcomes.json` is the only cross-task recovery index.
It is not a workflow engine, event log, receipt store, queue, or source of
engineering truth.

Minimal schema:

```json
{
  "schemaVersion": 1,
  "outcomes": {
    "invocation:fictional-release-a": {
      "lead": { "hostId": "host", "threadId": "fictional-lead", "epoch": 1 },
      "issueTasks": [
        {
          "hostId": "host",
          "provider": "provider",
          "repository": "owner/repository",
          "issue": 123,
          "threadId": "fictional-owner"
        }
      ]
    }
  }
}
```

Registry rules:

- `outcomeKey` is the immutable invocation identity. Generate a unique key for
  new invocations (for example `invocation:<UUID>`), even for another invocation
  in the same repository. Existing keys remain valid; do not rename live keys.
- The bound lead may mutate only its own invocation entry. Issue tasks never
  write the registry. All leads use [the registry helper](scripts/registry.py),
  which locks the shared file, compares the exact expected entry, preserves
  unrelated entries, and rejects duplicate issue/task ownership. Atomic rename
  alone does not prevent lost updates between parallel leads.
- Native issue identity includes provider, repository, and issue number. A
  native issue or source task cannot belong to two invocations. Register
  dependencies between invocations without registering a second owner.
- Every lead handoff increments `epoch`.
- Use helper `update` with the observed prior entry (JSON `null` for creation),
  one replacement entry, and the acting lead identity. Reconcile a stale-entry
  rejection before retrying. Never overwrite the entire registry from a stale
  snapshot. Unknown schemas or conflicting identities fail closed.
- All writers must use the same helper and local lock path. The helper checks
  supplied identities; it is not authentication or an authority grant. Do not
  use an automated fallback writer. See [registry operations](references/registry.md).
- Remove a terminal outcome only after accepting its completion receipt and
  archiving all of its issue tasks.
- Native task history remains the durable record of outcome snapshots, prompts,
  blockers, reviews, and completion receipts.

## Continuity and work tracking

Native task history preserves outcome snapshots, prompts, blockers, review
receipts, and completion evidence for the supported Codex workflow. GitHub issues
and native relationships own work tracking. Recover the known outcome and issue
identities before broad recency searches; revalidate original approvals, source,
artifacts, and runtime state before consequential action.

Use an operator-configured memory integration when required by governing policy.
For example, ai-memory can preserve scoped decisions and provenance across
harnesses. Follow that integration's retrieval, storage, and checkpoint rules;
it is not bundled or required by this skill. Without a verified integration,
make no cross-harness continuity claim. A worker checkpoint is not the lead's
complete outcome state. Missing or stale history remains explicit.

Memory never adds authority, a queue, an approval broker, or a second binding
registry. Keep one long-lived lead by default. Context compaction does not
itself require handoff and does not guarantee indefinite accuracy. Handoff only
when a transition is actually needed.

## Registration and START

Before `START`, prove the issue, task host/thread identity, repository,
worktree, exact base or head, clean state, dependencies, selected execution
route, and current registry binding do not conflict.

For a new issue task, verify the issue's canonical `owner/repo` against its
source repository before deriving the title or selecting a project. Prefer a
saved repository project only when exactly one project matches that canonical
repository identity. If none matches or matches are ambiguous, use an explicitly
selected, unambiguous umbrella project and record the fallback in the task
contract. If no such umbrella is selected, resolve the project choice with the
operator before creation. Never infer repository ownership from a project,
sidebar placement, task title, or a similarly named repository.

Initial dispatch includes:

```text
LEAD_BINDING outcomeKey epoch leadHostId leadThreadId
START repository issue sourceHostId sourceThreadId worktree exactState authority acceptance
```

`START` authorizes the one issue task to continue through every ordinary
in-scope lifecycle stage without milestone approval. Grant the complete outcome
and routine correction loop once, within a finite resource and authority
envelope wherever governing contracts permit. Size bounds from the actual
command graph (including hooks and prerequisite builds), available measurements,
and headroom; distinguish sampled stop thresholds from enforced hard ceilings.
Do not use an arbitrary undersized grant that makes ordinary work impossible.
If repository policy prevents a workable envelope, identify the exact rule and
propose the smallest owner-specific amendment to the authorized decision maker.

The same owner reproduces, diagnoses, corrects, verifies, and delivers through
ordinary environment, dependency, test, build, integration, and review failures,
head drift, merge conflicts, and cleanup residue. Unknown root cause starts
investigation; it does not establish a blocker or justify a blind retry. Keep
routine corrections inside the existing envelope without per-step lead grants
or architectural reapproval for an unchanged outcome. Re-verify exact source
and provenance after changes. Never widen caps, repeat a consumed one-use model
attempt, bypass required review, or infer production authority from delivery ownership.

During a substantial process or dependency wait, use available capacity for a
bounded pass over existing logs, receipts, and measurements to find a concrete
improvement to performance, durable checkpoint/resume, or progress, health, and
ETA reporting.
Check once when the wait or new evidence warrants it, not on every poll. A
completion, failure, or resource signal from the primary work takes priority.
Low-value waits and waits with no new evidence may remain idle.

Make an improvement during the wait only within the current issue's scope,
ownership, isolation, resource limits, and review authority. Do not alter a
running job's source, inputs, configuration, or cache, contend for its resource
class, bypass a hold or required review, or start another task or agent just to
investigate. If a useful change needs broader authority or a conflicting
resource, prepare a concrete proposal linked to the existing owner or issue:
cite the evidence, expected benefit and unknowns, smallest change, and proof.
Keep it in existing task history and receipts; it creates no finding quota,
mandatory report, or new upward message type.

## Dispatch and handoff attestation

At every task creation, `START`, or lead handoff, re-read this skill and the
current repository instructions. A handoff is state evidence, not authority to
downgrade the active workflow. A stale handoff cannot override current policy;
only an explicit operator instruction that names the intended workflow-policy
change can. Generic approval of an outcome or handoff is insufficient.

Before considering dispatch or takeover complete:

- Read back a new task's actual title and require exactly `<repo>-<issue>` from its verified issue-owning repository and native issue number; reject role suffixes. Preserve existing task titles during handoff and continuation.
- Read back its project: the unique saved project matching the canonical issue-owning repository, or the recorded explicit unambiguous umbrella fallback. Project placement never changes registered issue identity.
- Read back `START` and require the issue task to own its complete authorized lifecycle, including guarded merge, issue closure, and cleanup only when in scope. A PR-only outcome must not acquire merge authority.
- Read back the review route and reason under the review policy below and governing personal/repository rules: an eligible owner-only check, or one direct native reviewer child that is never another visible task.
- Read back explicit model/effort for the owner and any required reviewer; record requested and effective settings; preserve active routing unless explicitly changed.
- Read back that an unchanged contract returns corrections to the same reviewer child rather than creating a fresh reviewer.
- Read back the visible task list and reject a second issue owner, visible reviewer task, duplicate worktree, or conflicting binding.

When current policy supplies one answer, correct the mismatch in the same
registered task before allowing it to proceed, including stale task-role or
lifecycle-authority wording. Fail closed for an operator decision only when
current policies conflict, repository identity cannot be reconciled, or an
explicit policy-changing instruction leaves multiple valid workflow choices.

## Sparse upward protocol

After `START`, the issue task sends no progress, milestone, dependency-status,
review-ready, resource-ready, or ordinary correction message. It communicates
upward only with:

- `BLOCKED` — a concrete architecture or authority decision, credential, or
  external dependency that the issue task cannot resolve within its scope.
  A dependency or external condition warrants a blocker only when it prevents
  remaining useful work; continue independent work while waiting.
- `COMPLETION_RECEIPT` — verified terminal delivery and cleanup readback for the
  issue's in-scope lifecycle.

A blocker includes exact evidence, attempted diagnosis, options, recommendation,
and the precise decision or action needed. Name the owning track, artifact, and
native dependency when applicable. Separate capacity queues and approval waits
from code failures. Do not require exhaustive irrelevant experiments before a
legitimate design question. The lead challenges unsupported blockers, resolves
cross-track conflicts, and supplies Principal/Director-level architectural
direction without taking over routine diagnosis or duplicating sufficient
review. The same owner resumes delivery after the decision.

Before every upward send, use helper `resolve` with the task's immutable
`outcomeKey` and complete registered source identity. Use the returned current
lead host/thread and epoch. A missing or conflicting match means do not send;
retain the pending message locally and report the concrete routing gap. Never
select a lead by repository alone or follow the most recent message sender. An inherited `source_thread_id`, old bootstrap prompt,
or previously contacted lead is not the recipient authority.

Delivery is an explicit tool action: call
`mcp__codex_app__send_message_to_thread` with the bound lead's `threadId` and `hostId` and
the complete receipt in `prompt`, then inspect the result before ending the
turn. Omit `model` and `thinking`: they change the recipient's settings.
A final answer in the issue task, a sidebar output badge, or a memory checkpoint
does not send the receipt. If the send fails, retain the unsent receipt and
report the delivery failure locally; do not claim the lead was notified.
After a successful send, do not send it again merely because no acknowledgment
arrives. Failed attempts, instrumentation, preparation, review-ready state, and
cleanup are progress, not terminal delivery. Do not split ordinary delivery into
bounded-stage completion handoffs. An explicitly requested standalone
investigation may finish at its defined result; report that result and its
limits without implying the parent deliverable is complete.

Every upward message contains the current binding and registered source
identity:

```text
BLOCKED
  outcomeKey epoch sourceHostId sourceThreadId provider repository issue
  exactEvidence requiredAction

COMPLETION_RECEIPT
  outcomeKey epoch sourceHostId sourceThreadId provider repository issue
  exactEvidence terminalResult
```

The lead accepts a child message only when it is itself the lead bound to that
invocation and the outcome key, epoch, source host/thread, provider, repository,
and issue match the current registry. A valid receipt for a different lead is
not this lead's work: do not act on it, change bindings, or tell the child to
report here. Retain its identity and notify the correct lead of the routing
discrepancy without replaying authority; reconcile the original source once. Titles are never routing
authority. Reject stale or unregistered senders outside the bounded handoff
reconciliation window.

## Between independent invocations

Each issue task sends blockers and completion only to its bound lead. It does
not message another lead or another invocation's children. Its lead may exchange
one concrete dependency, shared-file/resource conflict, or capacity-release
handoff with the other bound lead. Include both invocation identities, the exact
artifact/resource, requested decision, and limits. This is peer coordination,
not an issue receipt, a binding change, or authority over the other lead's work.
Do not forward routine progress, retry reports, or grant instructions directly
to another lead's children. The receiving lead relays its own decisions.

Only an explicit authorized transfer can change a task's invocation. Quiesce
that owner, preserve unresolved actions and authority, and remove its old binding
before registering it under the agreed invocation; check global uniqueness and
attest the new binding before resuming. No automatic takeover or duplicate writer.

## Lead handoff

The outgoing lead records an `OUTCOME_CONTROL_SNAPSHOT` in native task history
with the outcome contract, active issue identities and cursors, current gates,
exact state, next proof, ETA, risks, stop conditions, retirement obligations,
and authority boundaries.

Ordinary handoff:

1. Record every active issue task's cursor and the handoff start time.
2. Atomically update the registry to the incoming lead at `epoch + 1`.
3. Send each active issue task (omit model/effort overrides on messages):

   ```text
   LEAD_BINDING outcomeKey epoch leadHostId leadThreadId
   ```

4. The incoming lead takes one bounded native task reconciliation from the
   recorded cursors.
5. During only that interval, accept an old-epoch blocker or completion when its
   source is still registered, cursor is newer than the baseline, and timestamp
   is inside the recorded handoff window. Record it under the current outcome;
   never ask the issue task to repeat it.
6. Close the window after one bounded reconciliation pass, with a deadline
   recorded before starting. Resume exact-epoch rejection even if a task is
   unavailable; reconcile its retained evidence under the new binding later.
   An unavailable task must not keep old-epoch acceptance open indefinitely.

If the outgoing lead is unavailable, only an operator-authorized incoming lead
may take over. Record the approval in native history and re-attest the registry,
every active issue task, pending actions, and prior lead state. Then use helper
`update --authorized-takeover` as the incoming lead with the exact expected entry,
unchanged issue owners, and `epoch + 1`. The flag is not approval. There is never
a second writer for that invocation; other invocation bindings remain unchanged.

## Review policy and native children

Every owner checks the final diff against requirements and performs the required
verification. Self-checking cannot supply independent acceptance of that owner's
work. Governing personal and repository rules may require stronger review:

- Owner-only review is eligible only for obvious, reversible, low-risk edits
  without consequential behavior, contract, security, data, or policy effects,
  and only when governing rules permit it. Record the reason and proof. Uncertain
  exemptions receive independent review.
- Ordinary behavioral changes receive one fresh, read-only independent reviewer.
- Security/permissions, money handling, trading/scientific validity, migrations,
  data integrity, consequential policy, and complex integration always receive
  independent review with the required expertise and model/identity constraints.

Select owner, helper, and reviewer model/effort explicitly under governing policy
and actual host availability. Example profiles are optional, not installed by the
skill. Preserve active model/effort unless explicitly rerouted. Record requested
and effective settings; if the required profile is unavailable, resolve that
route with the same owner rather than silently falling back or dropping review.
A model change cannot relax verification or authorization.

An issue task may use a direct worker for useful independent work whose benefit
justifies context and integration cost. Supply the objective, owned files or
responsibility, constraints, and required proof with `fork_turns: 'none'` by
default. State that other writers may exist, forbid reverting their work, and
keep integration and verification with the issue owner. Fixed profile settings
cannot be overridden by spawn arguments. Never create a second issue owner.

For required review, create one direct native reviewer child with fresh focused
context, not a visible task. The frozen review handoff contains:

- objective and acceptance, relevant governing policy, risk and review route;
- exact base/head and any uncommitted tree state, complete diff scope and owned
  source, target worktree, and verification evidence;
- read-only boundary and instruction to return only to its immediate parent.

The reviewer reads source and requirements, not the owner's full conversation.
It runs repository-mandated review checks when permitted; otherwise it reproduces
only checks needed to resolve an actual evidence gap. A check forbidden by its
read-only boundary remains an explicit gap, never a claimed pass. It returns one
`REVIEW_RECEIPT` with reviewed state, findings, checks, and verdict, and never
mutates, publishes, merges, creates visible tasks, or messages the lead.
Optional style or cleanup suggestions do not block acceptance.

The issue task validates findings, corrects them, and re-verifies. Under an
unchanged contract, return the exact corrected delta to the same reviewer for
targeted closure. A second ordinary failure alone does not justify escalation
or a new reviewer. Continue within the authorized envelope; repeated substantive
workarounds require consolidation at the canonical owner and escalation only
of unresolved scope, architecture, or authority decisions.

A material architecture, scope, or risk change creates one fresh reviewer.
Do not start another fresh review merely to relabel an unchanged-contract review
as terminal. Only a repository's explicit distinct terminal-review requirement
justifies that additional reviewer. Never reuse approval after reviewed state
changes: obtain updated acceptance for the final state. If the original reviewer
is unavailable, retain its findings and record the explicit replacement and
reason; do not treat the missing targeted closure as approval.

Use existing receipts to record the route/reason, correction rounds, material
findings, and model/effort. Compare total lead/owner/helper/reviewer usage and
accepted delivery, keeping waits and cached tokens separate when available.
Mark unavailable data unknown. Add no telemetry service or separate per-task
retro requirement.

## Reconcile every child and pending action

Native task messages are the primary notification path. At the start and end
of every lead turn, take one compact native snapshot of every outcome-critical
issue task in this invocation. Batch within the tool's target limit and retain
per-task cursors. Never infer progress from `active` status alone or assume an
empty/truncated message view proves there is no pending result.

In the existing `OUTCOME_CONTROL_SNAPSHOT` in native lead history, retain for
each child: registered identity, last observed cursor, current state, and any
pending lead action with its source message/turn identity. Record a decision as
sent only after inspecting the send result; received, pending, sent, and accepted
are distinct states. Retain unresolved actions across compaction and handoff.
This is the lead's existing outcome checkpoint, not a second queue or tracker.

Before starting additional tracks or yielding:

1. Reconcile every registered child, including those without a notification.
   Resolve missing or contradictory evidence with a focused task read. If the
   native view omits known content, inspect the retained source transcript when
   available; otherwise retain an explicit evidence gap. Do not guess.
2. For each blocker, send the in-scope decision/resume, record the exact external
   wait and responsible party, or present the concrete operator decision. An
   acknowledgment is not resolution. Keep useful independent work moving.
3. For each terminal result, validate binding, final state, required proof and
   cleanup; accept and archive, or return one concrete evidence/correction gap
   to the same owner. Repeated delivery of the same source message/state is
   idempotent; do not repeat acceptance or downstream actions.
4. Reconcile idle children that are neither externally blocked nor terminal:
   read their last turn, resolve the lead-owned gate, and resume the same owner.
5. Check the roster again before yielding and checkpoint unresolved actions.
   Do not leave a known actionable request only in prose or a notification badge.
   If backlog remains, reduce new starts rather than abandoning pending owners.

When a substantial wait leaves lead capacity, use the same evidence and authority
limits to consider a bounded improvement to the outcome path. Reconcile primary
signals and pending actions first; do not repeat the investigation at every
snapshot. Keep any proposal with the existing owner or issue and receipts, and
preserve the sparse upward protocol.

Size concurrent work by actual resource limits and the lead's ability to service
pending actions. There is no proven model-wide track limit. Six simultaneous
arrivals are a validation scenario, not a performance guarantee. Native messaging
also does not guarantee an idle lead wakes; this instruction-driven package makes
no unattended liveness promise.

Do not add a scheduled task, resident process, polling service, watcher, database,
memory control plane, or external supervisor by default. A reproduced native
notification limitation needs a separate smallest explicitly authorized change.

## Terminal state

The issue task proves its in-scope delivery, closure, terminal evidence, and
cleanup, then emits one epoch-bound `COMPLETION_RECEIPT`. The lead verifies the
registered identity and evidence, archives the issue task, and atomically
removes the terminal outcome or issue-task binding.

No milestone message substitutes for terminal evidence. Do not leave a second mutable workflow or binding registry active after
replacement. This package installer only links the skill; it does not manage
tasks, registry state, personal policy, or profiles.
