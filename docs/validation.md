# Validation scope

The initial release was prepared on macOS with Python 3.11+ and the Codex CLI
0.153.0 available. The standalone skill installer, local registry, manifest, and
example profiles are the supported release surfaces. The plugin manifest passes
the Codex plugin-creator validator, and the skill passes skill-creator validation.

Automated tests run against temporary directories and fictional identities.
They exercise clean installation, repeat installation, safe uninstallation,
existing-path collisions, exact invocation/source routing, same-repository
parallel leads, one invocation spanning repositories, duplicate ownership,
concurrent updates, stale state, handoff, authorized takeover mechanics, and an
injected failure before atomic replacement followed by successful recovery.
Routing tests cover shared defaults, team overrides, separate consequential
review routing, unknown fields/teams, explicit model/effort pairs, configuration
provenance, and missing selected configuration. Optional native profile
installation is tested for collision preflight and safe removal.
GitHub Actions runs the same suite on Linux; its run status is the evidence for
that environment, not a claim that local testing covered it.

Behavioral validation uses the [scenario suite](../tests/scenarios.md) with a
fresh agent and fictional inputs. On 2026-09-24, a GPT-6 Luna High helper received
only the candidate skill and scenarios, without expected answers. Its dry-run
responses preserved invocation isolation, reconciled all six children, handled
duplicate receipts once, retained unsent decisions and evidence gaps, reused the
same reviewer for corrections, and closed the handoff window despite an
unavailable child. No real tasks or messages were used in that exercise.

On 2026-09-30, a separate fresh helper requested on the GPT-6 Luna High route
received only the candidate skill and fictional scenarios A–D and M–Q, without
expected answers. Effective model metadata was unavailable. Its dry-run actions
retained original message/turn, invocation/epoch and cursor provenance; separated
acceptance, cleanup, archival and binding retirement; and recovered six mixed
arrivals, duplicates, stale epochs and interrupted sends/finalization. It kept
unknown delivery pending, re-read successful-but-unobserved updates, preserved
unrelated owners, restored the same cleanup owner for an archived chat retaining
a worktree, and deferred retirement for an incomplete release or transferred
owner. No real messages, registry changes, publication or cleanup occurred.

These checks do not establish throughput, cost savings, defect reduction,
multi-host support, marketplace installation, or reliable background wakeups.
The registry helper checks supplied identities but cannot authenticate the
agent or enforce review, archival, and production authorization. All writers
must cooperate with its lock; direct file writes can bypass those protections.
