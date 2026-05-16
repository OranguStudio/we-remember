# CLAUDE.md

This file is the reference guide for AI agents (Claude Code, Codex, etc.)
working on the We Remember codebase.

## Project Overview

Privacy-first, self-hostable calendar app.
No trackers, no Google — data stays local.
License: AGPL-3.0

## Tech Stack (v0.0)

- **Backend**: Django 5+ with DRF
- **Frontend**: HTMX + Alpine.js
- **Database**: PostgreSQL (dev via Docker Compose, prod on Hetzner VPS)
- **Package manager**: uv
- **Deploy**: Docker Compose

## Branching Strategy (GitHub Flow)

- `main` is always deployable
- Never commit directly to `main`
- Create a feature branch for every change linked to an issue:
  `<type>/<issue-number>-<short-description>`
- Branch naming examples:
  - `feat/1-django-project-setup`
  - `fix/12-timezone-offset`
  - `chore/3-update-dependencies`
  - `docs/7-self-hosting-guide`
- Open a PR → merge into `main`

## Commit Conventions (Conventional Commits)

Format: `type(scope): description`

| Type | When to use |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `chore` | Maintenance, dependencies, refactoring |
| `docs` | Documentation only |

- Scope is optional but encouraged: `feat(events): add RRULE support`
- Keep descriptions short and imperative: "add", "fix", "update" not "added", "fixed"
- Breaking changes: add `!` after type → `feat!: drop Python 3.11 support`

## Development Workflow

### Commit sequencing

Before starting work on an issue, plan the commit sequence.
Each commit should be atomic: one logical change, independently
reviewable, and passing CI on its own.

Write the sequence in the issue before touching any code.
This applies whether you are working manually or with an AI agent —
the sequence is the plan, and the plan comes first.

**Example — issue #1 (Django project setup):**
```
docs: update CLAUDE.md with commit sequencing workflow
feat: scaffold django project with uv
feat(settings): split django settings
chore: add environment example and ignore local env
feat: add ruff and configure linting
feat: add pytest and django test config
feat: add configuration smoke test
ci: add github actions pipeline
docs: update README with local setup instructions
docs: update CLAUDE.md with project conventions
```

Rules:
- Infrastructure before features
- Tooling (linting, testing) before application code
- CI after tooling is confirmed working locally
- Docs last — written after the code, not before

### Working with AI agents

AI agents (Claude Code, Codex, etc.) follow the same workflow as
any contributor: one commit per logical change, conventional commit
format, CI must pass.

When using an agent, provide the planned commit sequence from the
issue as context. The agent implements one commit at a time —
review before moving to the next.

Agents are used for implementation and acceleration, not for
planning. Planning (issue scoping, commit sequencing, architecture
decisions) happens before the agent is involved.

## Project Conventions

### Django configuration

- The Django project package is `config`
- Settings are split into:
  - `config.settings.base` for shared settings
  - `config.settings.development` for local development and tests
  - `config.settings.production` for future production configuration
- `manage.py`, `asgi.py`, and `wsgi.py` default to
  `config.settings.development`
- Secrets and environment-specific values are read with `os.environ`
- The codebase does not load `.env` files directly

### Python tooling

- Runtime and dev dependencies are managed with `uv`
- Linting uses Ruff: `uv run ruff check .`
- Tests use pytest and pytest-django: `uv run pytest`
- Test defaults live in root-level `conftest.py`

## Releases (release-please)

- Releases are managed automatically via `release-please` GitHub Action
- Every push to `main` updates the release PR
- Merging the release PR creates the tag and GitHub Release
- Version bumps follow semver based on commit types:
  - `fix:` → patch
  - `feat:` → minor
  - `feat!:` / `BREAKING CHANGE:` → major
  - `chore:`, `docs:` → no bump

## Current Milestone

**v0.0 — Foundation** (infrastructure only, no user-facing features)

See GitHub Milestones for open issues.
