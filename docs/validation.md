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

These checks do not establish throughput, cost savings, defect reduction,
multi-host support, marketplace installation, or reliable background wakeups.
The registry helper checks supplied identities but cannot authenticate the
agent or enforce review, archival, and production authorization. All writers
must cooperate with its lock; direct file writes can bypass those protections.
