# Team and model configuration

This local Codex plugin uses TOML and native agent profile conventions. It does
not add unsupported fields to Codex's `config.toml` or pretend to offer a native
plugin settings form. Configuration contains non-secret routing preferences,
not credentials, permissions, live task identities, or runtime outcomes.

Run `python3 scripts/routing.py` from the installed skill directory. Selection:

1. Bundled `config/defaults.toml` supplies all role defaults.
2. `~/.codex/multi-chat-orchestration/config.toml`, when present, supplies overrides.
   `--config /path/to/config.toml` explicitly selects a different override file
   instead. There is no implicit repository-directory discovery.
3. `--team product` applies the selected file's named team overrides after its
   shared role overrides. The default team needs no table.

`--defaults-only` ignores user configuration for inspection or reproducible
tests. Missing explicitly selected files, unknown fields/teams, unsupported
schema versions, and malformed values fail clearly. Adding a model override
requires an explicit `model_reasoning_effort` alongside it. Model identifiers
are not hardcoded into the validator: verify availability and effort support
against the actual host before dispatch. No automatic fallback is permitted.

```toml
version = 1

[teams.product.roles.owner]
model = "gpt-6-sol"
model_reasoning_effort = "medium"

[teams.product.roles.reviewer]
model = "gpt-6-sol"
model_reasoning_effort = "high"
```

The six roles are `lead`, `owner`, `helper`, `reviewer`, `consequential_owner`,
and `consequential_reviewer`. Defaults are Astra XHigh for the lead and reviewers,
Sol Medium for ordinary owners, Luna High for helpers, and Astra XHigh for
consequential work. They are starting preferences, not benchmark conclusions.
Configure teams according to current work; do not create organizational layers
or extra visible tasks merely because a team exists in this file.

`helper`, `reviewer`, and `consequential_reviewer` also select `agent_type`.
The bundled example native profiles are model-neutral so explicit configured
spawn settings can apply. Install those profiles explicitly or select an existing
profile. If an existing custom profile pins a model/effort, those settings win
in Codex: reconcile that conflict before dispatch, never claim your override won.
The same native profile may serve ordinary and consequential review when its
effective settings satisfy the selected role's contract. A fixed Astra XHigh
profile can match consequential review even if it conflicts with an ordinary
Sol High preference; role selection follows the work's risk, not the profile name.

For visible issue tasks, pass the resolved owner model and effort explicitly
to task creation (`model` and `thinking`) only when the operator's explicit routing
selection and host tool authorize those overrides. Otherwise resolve the missing
selection before dispatch; do not treat bundled defaults as a new permission.
For direct children, use the selected
profile and the corresponding spawn model/effort when the host permits overrides.
Use fresh bounded context. If a fixed role forbids overrides, select an available
matching profile or resolve the conflict explicitly. For the lead, attest its
current effective settings; the resolver does not change the running lead.

Record selected team, source config hashes, resolved routing hash, and requested
and effective role settings in the existing invocation contract. Freeze them for
in-progress work: later edits or plugin updates affect new invocations only
unless an explicit routing decision changes an active contract. Invocation keys
remain unique; a team name never becomes a message recipient or ownership key.

Explicit operator instructions and governing personal/repository rules constrain
these preferences. Resolve a conflict before dispatch; configuration cannot
disable independent review or grant publishing, deployment, or production access.

Conventions: [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents),
[local plugin settings guidance](https://developers.openai.com/plugins/guides/submit-claude-plugin#replace-claude-userconfig).
