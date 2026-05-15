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