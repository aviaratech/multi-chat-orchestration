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
snapshot predates these events:

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
