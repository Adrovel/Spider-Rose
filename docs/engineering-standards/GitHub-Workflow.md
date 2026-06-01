# GitHub Workflow Standards

Version: 0.1.0  
Status: Active standard  
Last updated: 2026-06-01

Purpose: define how Spider Rose uses commits, branches, pushes, issues, pull requests, merges, and session closeout.

## Team Rule

Spider Rose currently has two active collaborators: Joel and Mukthar.

Because the team is small, fast merging is allowed. Joel and Mukthar may instantly merge pull requests when the change is understood and checks pass.

Still create pull requests for every code or docs change so history stays reviewable.

## Direction Conflict Rule

If Joel asks for approach X and Mukthar believes X does not make sense but approach Y does, Mukthar should build both paths instead of blocking the work:

- build Joel's requested approach X on one branch
- build Mukthar's proposed approach Y on a separate branch
- keep both branches small enough to compare directly
- document the tradeoff in the pull request descriptions
- let Joel make the final product decision after both options are visible

Do not replace X with Y silently. The point is to preserve product direction while still testing a technically better alternative.

## Fetching

At the start of every Codex session, run:

```bash
git fetch origin
git status --short --branch
```

Do this before editing, committing, or pushing.

If the branch is behind, sync it before starting work unless the user explicitly says not to.

## Branching

Do not commit directly to `main` unless the user explicitly asks.

Create a branch for every change:

```text
feature/<short-name>
fix/<short-name>
docs/<short-name>
```

For demo-only work, branch from `demo`.

For production-ready work, branch from `main`.

## Committing

Use small commits with one clear purpose.

Use conventional commit names:

```text
feat: add hello agent
fix: reuse existing visual server
docs: add github workflow standards
```

Do not mix unrelated UI, docs, and backend changes unless they are part of the same feature.

Run relevant checks before committing:

```bash
pytest
npm run build-storybook
```

Docs-only changes do not require tests unless links, commands, or examples changed.

## Pushing

Push branches after committing.

Pushing to production is allowed for Spider Rose, but production changes should normally reach `main` through a pull request merge.

Demo branch may be pushed directly for demo iteration.

Do not force-push shared branches unless explicitly approved.

Before pushing, confirm branch state:

```bash
git branch --show-current
git status --short --branch
```

## Issues

Create issues for:

- bugs
- roadmap features
- technical debt
- unclear product decisions
- recurring problems

Each issue should include:

- problem
- expected behavior
- current behavior
- proposed fix
- priority

For tiny changes already handled in a pull request, an issue is optional.

Keep issues actionable. Avoid vague issues such as "improve UI" unless they are broken into concrete work items.

## Pull Requests

Create a pull request for every change.

Each pull request should explain:

- what changed
- why it changed
- how it was tested
- docs updated, if relevant

UI pull requests should mention Storybook or visual review status.

Docs-only pull requests can be merged quickly after a basic read-through.

## Merging

Joel and Mukthar can instantly merge when:

- the pull request is understandable
- tests or checks pass, or skipped checks are explained
- the change does not delete or overwrite important work

Prefer squash merge for feature, docs, and fix branches.

After merge, delete the feature branch unless it is still active.

Do not merge experimental demo work into `main` until explicitly approved.

## Production

`main` is production.

"Push to production" means the final approved or session-complete change reaches `main`.

For Spider Rose, Codex should normally finish by committing, pushing, creating a pull request, and merging or pushing to `main` unless told otherwise.

Keep `main` install and README commands valid for real users.

## Codex Session Closeout

At the end of every Codex session:

1. Check local status.
2. Run relevant tests and checks.
3. Commit all intentional local changes.
4. Push the working branch.
5. Open or create a pull request.
6. Merge or push to `main` when the change is production-ready.

Engineering standards must be included in the session push whenever they changed, and this file should stay uploaded with the rest of the app docs.

If there are unrelated local changes, do not include them unless they are clearly part of the same task.

If tests fail, do not merge to `main`; commit only if the failure is documented and the user approves.

If the user explicitly says "don't execute" or "don't push," skip this closeout rule.
