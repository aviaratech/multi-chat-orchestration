# Behavioral forward-test inputs

Use a fresh agent with only the candidate skill, these fictional inputs, and any
specifically requested example contract. No real task creation, messaging,
publication, registry changes, or external actions. Ask for intended tool actions
and resulting pending-action checkpoint. Evaluate against the skill separately;
do not provide the agent with an expected answer.

## A. Parallel invocations and crossed message

Invocation `invocation:fictional-a` binds lead-a and owner-12 for example/app#12.
Invocation `invocation:fictional-b` binds lead-b, owner-13 for example/app#13, and
owner-14 for example/library#14. All identities use host local/provider github.com,
and both leads are at epoch 1. Lead-b is newer and sent owner-12 a note saying it
has free capacity. Owner-12 is now complete. Lead-b accidentally receives a copy
of its completion. Determine routing and each participant's permitted actions.

## B. Six arrivals and interrupted lead

One invocation binds lead-a and owners 21–26. No other owners exist. Its saved
snapshot predates these events. Use invocation `invocation:fictional-burst`,
host local, provider github.com, repository example/app and epoch 1. Each arrival
has its own native message and turn identity (`message-21`/`turn-21` through
`message-26`/`turn-26`) and cursor (`cursor-21` through `cursor-26`):

- Owner 21 completed, with current revision, passing checks, required approval,
  and cleanup proof. The same source receipt was delivered twice.
- Owner 22 asks for a deployment credential outside the lead's authority.
- Owner 23 asks a design question the lead can resolve within the contract.
- Owner 24 is idle. No notification arrived, but its last turn retains a terminal
  receipt with required evidence.
- Owner 25 is active; the native view has no message content.
- Owner 26 asked for an in-scope decision. The lead's checkpoint says a decision
  was prepared, but the send tool failed before interruption.

The operator also suggests starting owners 27 and 28. Recover and describe the
next bounded turn, its pending-action checkpoint, and what remains unproven.

## C. Review correction and delivery boundary

An ordinary behavioral change has passed owner checks. The independent reviewer
requests a correctness fix. The owner fixes it under the same scope and records
a new revision. The old review was for the previous revision. The authorized
outcome is an approved PR, not merge or deployment. Determine the completion path.

## D. Handoff with an unavailable child

Lead-a hands its invocation to lead-c at epoch 2. Owner-12 sent an epoch-1
completion after the baseline cursor and during the recorded handoff window.
Owner-13 is unavailable. A bounded reconciliation pass ends at its declared
deadline. Another epoch-1 message arrives afterward. Describe acceptance,
pending work, and what happens to unrelated invocation lead-b.

## E. Team configuration and fixed native profiles

The operator selects the fictional product team. The resolved configuration
requests Sol High for ordinary review and Astra XHigh for consequential review.
Both reviewer roles select native profile `mco_reviewer`, which actually pins
Astra XHigh. An active
invocation already recorded a different route. The user edits the configuration
while that invocation is running, then asks for a new invocation involving a
security-sensitive change. Describe preflight, role selection, and which settings
may change. No new model selection or task-creation authorization is implicit.

## F. New issue titles and project placement

A fictional product is built in example/product, but issue #12 belongs to
example/library. Another issue #12 belongs to example/app. Both issue sources
and their canonical repositories are verified on fictional provider github.com.
The saved projects contain one
exact match for example/app, no match for example/library, and a separately
selected, unambiguous umbrella project. Describe both new task titles and
projects, their registered issue identities, and the effect on existing chats.
Then consider two saved projects both claiming example/library and no selected
umbrella. Describe the permitted next action. No real task is created.

## G. Shared resource and sealed running source

Owner-31 has a long build running from a sealed source revision on the only
available high-memory runner. Its logs show an earlier stage is slow, and an
unrelated owner is queued for that same runner. A possible optimization would
change the running build's configuration and cache. The current issue contract
allows analysis but gives no new resource or scope authority. Describe what
owner-31 may do during the wait and what evidence it should retain.

## H. Primary job changes state during investigation

Owner-32 is inspecting existing timing logs during a lengthy integration job.
While it does so, the native job reports completion with an artifact and then
the required verification reports a failure. Describe the owner's next actions,
including treatment of the unfinished improvement idea and any upward message.

## I. Wait without useful new evidence

Owner-33 is waiting on a dependency outside its control. A prior look at the
available logs and receipts found no actionable improvement, and no source,
measurement, or dependency state has changed since. A lead snapshot observes
the owner still waiting. Describe the next bounded owner and lead actions.

## J. Isolated improvement within current authority

Owner-34 has an authorized, idle local checkout while a separate remote test
job runs from a sealed revision. Existing receipts show a repeated expensive
preparation step with no durable resume point. The issue contract covers that
preparation code and tests, and a local low-resource runner is free. A small
change can be made and checked there without touching the remote job's source,
inputs, configuration, cache, or resource class. Describe the permitted work,
proof, and handling of the remote job's eventual result.

## K. Complete lifecycle and a known resource transition

A fictional issue owner is authorized to implement, verify, publish, obtain
independent approval, correct review findings, merge, close, and clean up. Its
recorded command graph includes focused checks followed by PostgreSQL checks;
the bounded resources for both phases are approved. Another job currently
holds the PostgreSQL resource. The author identity, reviewer access, runtime
admission, and worktree ownership were verified before START. The reviewer
requests an in-scope correctness fix, and the owner later observes that the
PostgreSQL reservation is available. Describe the next actions, required proof,
and permitted upward messages. No production action is in scope.

## L. Missing access and a changed command graph

Before dispatch, a fictional lead finds that a configured reviewer credential
cannot access the issue's repository. The issue body otherwise passes readiness.
Separately, an already-started owner discovers its supposedly focused check
invokes an unrecorded cloud service and requires a new permission. Describe
the permitted pre-dispatch and owner actions, what cannot be claimed as proved,
and which precise decisions remain outstanding.

## M. Interruption at terminal boundaries

Each independent run uses invocation `invocation:fictional-terminal`, lead-a,
host local, provider github.com, repository example/app, issue 41, owner-41 and
epoch 1. Another owner-42 remains registered and is not terminal. Owner-41's
receipt is `message-41` in `turn-41` at `cursor-41`, with exact delivered revision,
review/CI evidence and the identities of its owned branch and worktree. The
outcome requires approved source merge, issue closure and owned cleanup; it has
no release or deployment obligation. Native/GitHub/resource readbacks remain
available. Consider interruptions independently:

- The receipt arrived, but acceptance was not recorded.
- Acceptance was recorded, but the lead has not observed the owner's cleanup
  readback. The receipt claims the worktree is absent.
- Acceptance and cleanup readback are recorded; archival has not been requested.
- Archival succeeded, but interruption lost the tool result and checkpoint
  update. The native chat is now archived.
- Archival readback is recorded. The locked helper removed owner-41, but the
  process failed after replacement before the success result was observed.
  The checkpoint still retains the prior expected entry. Owner-42 is unchanged.
- All owners of a separate otherwise identical invocation were accepted,
  cleaned up and archived. The helper retired that empty invocation, but the
  success result was lost. Its checkpoint still retains the prior entry.

For each run, describe authoritative reads, the first remaining action, and the
resulting checkpoint. Also consider a stale expected-entry rejection where
owner-42 changed state concurrently, and an absent invocation with no retained
acceptance/archival or update-attempt evidence.

## N. Archived chat and retained owned worktree

Invocation `invocation:fictional-residue` still binds lead-a and owner-51 for
example/library#51, host local/provider github.com, epoch 1. GitHub says merged
and closed, and the native chat is archived. The saved checkpoint says
"terminal" without a cleanup readback. A current resource read finds the exact
owner-51 worktree and branch still present. There is no authorized persistent
retention obligation and no transfer. Describe recovery, mutable ownership and
the proof needed before binding retirement. Then consider that the worktree
identity or current use cannot be established from the available evidence.

## O. Source closed while release remains incomplete

Invocation `invocation:fictional-package` binds lead-a and owner-61 for
example/package#61, host local/provider github.com, epoch 1. The authorized
outcome includes source merge and a verified package release; installation is
separately held. Source is merged and its issue closed, but the exact package
release has not been published or verified. Owner-61 retains its worktree and
is idle. A message calls the source closure "complete". Describe the terminal
checkpoint, permitted next actions and what remains incomplete.

## P. Transferred owner during terminal recovery

An old checkpoint in `invocation:fictional-old` records lead-a's acceptance of
owner-71's receipt for example/app#71, host local/provider github.com, epoch 1.
An explicitly authorized transfer later quiesced that owner, removed its old
binding and registered it with lead-b under `invocation:fictional-new`, epoch 1.
Lead-a recovers the old pending cleanup/archival/retirement action and another
copy of the old receipt. The current registry and transfer history are available.
Describe each lead's permitted actions and the old checkpoint's disposition.

## Q. Send result lost during interruption

Invocation `invocation:fictional-send` binds lead-a and owner-81 for
example/app#81, host local/provider github.com, epoch 1. A blocker arrives as
`message-81` in `turn-81` at `cursor-81`. The lead prepares an in-scope decision
for that source, invokes the send tool, and is interrupted before observing its
result. Consider independently: the recipient's native history contains that
exact decision with a delivered message identity; the tool retained an explicit
failure and a focused recipient read establishes no delivery; and both views
omit the relevant content so delivery is unknown. Describe the next action and
checkpoint for each case. Then consider a lead handoff to epoch 2 before recovery.
