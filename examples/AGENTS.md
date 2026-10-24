# Optional repository facts

This fictional example is optional. Supply these facts directly in START when
there is no AGENTS.md. Personal policy and explicitly supplied constraints still
apply; the plugins provide the generic workflow.

- Repository: `example/garden`; one owner in an isolated worktree.
- Check: `python3 -m unittest discover -s tests -v`.
- Public interfaces stay compatible unless the issue explicitly changes them.
- Review: one fresh read-only ordinary reviewer; consequential changes need a
  qualified independent reviewer and the required reviewer-App approval.
- Delivery: verified, independently approved PR. Pushing its issue branch and
  opening the PR are authorized; merge and deployment require separate authority.
- Production: no production writes or credentials are authorized.
- Cleanup: retain the worktree while the approved PR remains open; record it.
- Keep runtime bindings and private evidence out of commits.

Missing checks, access or authority must be resolved before the affected stage.
This example supplies no credentials and authorizes no real repository actions.
