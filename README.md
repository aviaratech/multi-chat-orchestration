# Multi-Chat Orchestration

A Codex workflow for parallel leads, each coordinating its own invocation across
one or more repositories, with one accountable task per issue, bounded helpers,
independent review, and explicit
delivery receipts. Published by [Aviara Tech](https://github.com/aviaratech)
under the [MIT license](LICENSE).

The workflow is a skill: instructions interpreted by the agent. It is not an
orchestration server, a security boundary, or a guarantee of delivery. Repository
rules, actual tool permissions, and operator authority still apply.

## What it does

- Keeps implementation, verification, corrections, and authorized delivery with
  the same issue owner.
- Names new issue tasks `<repo>-<issue>` from the verified issue-owning
  repository and places them in its uniquely matching saved project when present.
- Gives the lead dependencies and outcome acceptance, while direct helpers
  report to their parent.
- Separates self-checking from independent review and reuses the reviewer for
  corrections within an unchanged contract.
- Routes blockers and completion receipts using registered task identities and
  a lead generation number, including an explicit handoff procedure.
- Isolates invocations sharing a repository and reconciles every child and pending
  lead action before yielding. Cross-invocation dependencies stay lead-to-lead.
- Uses native task messages and bounded snapshots rather than adding a service.
- Uses substantial waits for bounded, evidence-based improvements within the
  current owner's authority while primary work retains priority.

## Requirements and limits

The initial target is Codex desktop with native task creation, reading,
messaging, snapshots, archival, and direct subagents, plus GitHub access and Git
worktrees. Tool availability varies by host and account. The lead checks it
before dispatch; installing this skill does not grant capabilities or permission
to create tasks, push, merge, or deploy.

The binding registry is a local recovery index. All participating tasks must
read the same file. A small helper serializes updates and rejects stale bindings
and duplicate ownership; each lead changes only its own invocation. All writers
must use it. This is local-filesystem locking, not a distributed store. Separate
hosts without that shared view are unsupported. Native messages do not guarantee that an idle lead will
wake; check snapshots when the lead runs. This package adds no background monitor.

Bundled routing defaults use GPT-6 Sol Medium for ordinary owners, Luna High for
bounded helpers, and Astra XHigh for leads, reviewers, and consequential work.
Users can override them by role and team through a validated TOML file. Native
example profiles leave model selection to that explicit routing contract.
Availability and repository review rules still apply; no model is silently
substituted. These defaults carry no measured cost or quality superiority claim.

## Install the skill

Requires Python 3.11+ and a filesystem supporting symlinks. Supported platforms
are macOS and Linux; local validation covers macOS, and Linux CI is configured.
Clone into a persistent location, then install the skill:

```bash
git clone https://github.com/aviaratech/multi-chat-orchestration.git
cd multi-chat-orchestration
python3 scripts/install.py install --skills-dir "$HOME/.codex/skills"
```

The command creates only a `multi-chat-orchestration` symlink in the supplied
skills directory. It refuses to replace an existing directory, file, or foreign
symlink. To also install the two model-neutral native profiles, explicitly add
`--agents-dir "$HOME/.codex/agents"`. The installer checks all targets before
changing links and refuses collisions. It does not edit `AGENTS.md`, existing
profiles, or active configuration.
Start a new Codex task and check that the skill is available. If your host uses
a different skill directory, pass that directory explicitly. Do not install
both the standalone skill and the plugin into the same environment.

The symlink follows this checkout. Review changes before pulling updates; use
a separate pinned checkout if you need a stable version. Uninstall only the
link belonging to this checkout:

```bash
python3 scripts/install.py uninstall --skills-dir "$HOME/.codex/skills"
```

If profiles were installed, pass the same `--agents-dir` to remove their owned
links too. A permission or I/O failure during installation may leave some links;
fix the reported failure and rerun the same command, which is idempotent.

The root [portable plugin manifest](plugin.json), with a
[Codex compatibility overlay](.codex-plugin/plugin.json), also supports packaging
the skill as a Codex plugin. This repository does not register a marketplace
or submit a public directory listing. See the official
[plugin documentation](https://developers.openai.com/plugins/build/plugins)
for host-specific plugin distribution.

## Configure and use

1. Adapt the [sample repository contract](examples/AGENTS.md) to the repository
   being worked on. Keep its engineering and authorization rules there.
2. The default child routing names `mco_worker` and `mco_reviewer`. Install those
   [profiles](examples/agents) with the explicit `--agents-dir` option above or
   select existing suitable profiles in configuration. Restart/reload Codex as
   needed and confirm the chosen profiles are available before dispatch.
3. Optionally save [example configuration](examples/config.toml) as
   `~/.codex/multi-chat-orchestration/config.toml`, or select another file when
   invoking the skill. This is the plugin's documented local file, separate from
   Codex's native `config.toml`. Read the
   [configuration reference](skills/multi-chat-orchestration/references/configuration.md)
   for defaults, team overrides, validation, and model/profile precedence.
4. Inspect the selected team before starting (from this checkout):

   ```bash
   python3 skills/multi-chat-orchestration/scripts/routing.py \
     --config examples/config.toml --team product
   ```

5. Invoke the skill and state the outcome, issues, authority, and acceptance.
   Explicitly authorize new visible tasks if you want them created. For example:

   > Use $multi-chat-orchestration to coordinate issues #12 and #13 in my
   > repository. Create one task and worktree for each. Delivered means both
   > changes pass repository checks and have approved pull requests. Stop before
   > merging. Use the product team from my selected configuration, including
   > its explicit models and efforts. Report any authority or routing conflict.

For each new issue task, verify the issue's canonical repository and native
number, then use its repository basename in the title. Prefer the uniquely
matching saved repository project. If the match is missing or ambiguous, use an
explicitly selected, unambiguous umbrella project; otherwise resolve the project
choice before creation. A product project, title, or sidebar location does not
establish issue ownership. Existing task titles and projects are left as they are.

An organization can define several teams sharing role defaults. Each invocation
binds actual lead and engineer tasks to one outcome. Team names and repository
names never substitute for those exact runtime bindings. Configuration changes
apply to new invocations; they do not reroute in-progress work.

Read the [worked example](examples/worked-example.md) for the complete route,
including a review correction and a stale receipt. All example identities are
fictional and must be replaced with observed runtime identities.

## Memory and measurement

Native task history and GitHub are sufficient for the supported single-harness
workflow. A memory service such as ai-memory is an optional integration selected
by the operator; this package does not install or require it. Cross-harness
continuity requires an explicitly configured and verified integration. Memory
never supplies missing approval or replaces source evidence.

Use existing task/review receipts to compare accepted delivery time, correction
rounds, material review findings, escaped defects, and total lead/owner/helper/
reviewer usage. Separate waiting from execution and cached from uncached tokens;
record requested and effective model/effort, and mark missing data unknown.
There is no telemetry collector, automatic routing, or benchmark in this package.

## Validation and contributing

```bash
python3 -m unittest discover -s tests -v
git diff --check
```

Tests exercise installation into temporary directories, collisions, uninstallation,
parallel registry updates, exact routing, handoff, stale state, and package
consistency. The [scenario suite](tests/scenarios.md)
is for behavioral forward testing by a fresh agent. Passing it evaluates a
sample of instruction following; it does not prove all live orchestration paths.
See [validation notes](docs/validation.md) for the release evidence and limits.

Keep changes focused and public-safe. Do not submit real receipts, sessions,
private repository content, credentials, or runtime bindings. This repository
contains an extracted workflow with fresh public history; personal policy,
private histories, and operational data are not part of the distribution.
