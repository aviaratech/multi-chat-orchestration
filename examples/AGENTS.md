# Sample repository contract — adapt before use

This is a fictional application repository contract, not this package's policy.

- One issue owner uses one isolated worktree. Do not revert other writers.
- Record requirements, owned paths, non-goals, dependencies, and acceptance before
  editing. Preserve public interfaces unless the issue explicitly changes them.
- Run the repository's documented lint, typecheck, and relevant test commands;
  record the exact revision and results. Do not invent a passing check.
- Self-check every final diff. Ordinary behavioral changes require one fresh,
  read-only independent reviewer. Reuse that reviewer for unchanged-contract
  corrections. Consequential security, money, data, migration, or scientific
  changes require a reviewer qualified for the risk and any pinned model rules.
- Record requested and effective model/effort. Do not silently substitute models.
- Delivery for this example ends at a verified, independently approved PR.
  Pushing the issue branch and opening that PR are authorized. Merging, deploying,
  using production credentials, and changing repository policy require separate
  explicit authority. A review approval does not grant it.
- Include PR URL, revision, verification, review, and worktree disposition in the
  completion receipt. Preserve a worktree still needed by the open PR; record
  that retained state instead of calling it deleted.
- Keep runtime bindings and private evidence out of commits.
