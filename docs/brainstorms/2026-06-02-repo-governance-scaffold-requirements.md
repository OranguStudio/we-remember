---
date: 2026-06-02
topic: repo-governance-scaffold
---

# Repo Governance Scaffold

## Summary

Establish a complete, dependency-respecting governance scaffold for `we-remember`: replace GitHub's default labels with a semantic set, define Conventional Commits + GitHub Flow in `CLAUDE.md`, add issue and PR templates aligned to those conventions, then lock `main` with a branch ruleset that enforces the resulting workflow.

---

## Problem Frame

A fresh repo inherits GitHub's default label rainbow, has no commit convention, no branch strategy, and no templates — meaning every contributor (or future agent) has to invent these locally. Setting them up as a coordinated scaffold before any real work lands means conventions are load-bearing from day one rather than retrofitted later.

---

## Key Decisions

**Setup order: Labels → CLAUDE.md → Templates → Branch Ruleset.**
Each step depends on the previous. Labels are fully independent and establish vocabulary first. CLAUDE.md defines the conventions that templates reference. Templates encode the PR/issue workflow the ruleset will protect. Defining before enforcing avoids a ruleset that blocks PRs on rules nobody wrote down.

**Conventional Commits as the commit convention.**
Maps directly to the label taxonomy (`feat:` → `feature`, `fix:` → `bug`, `chore:` → `chore`, `docs:` → `docs`, `refactor:` → `refactor`), fits GitHub Flow's PR-per-branch model, and makes future changelog automation straightforward.

**GitHub Flow as the branch strategy.**
`main` is always deployable; all work happens on short-lived feature branches merged via PR. Simple enough for a small team or solo work, compatible with the branch ruleset constraints below.

**Minimal ruleset until CI exists.**
No required status checks in the initial ruleset — adding them before CI is wired up would block every PR. The ruleset ships as a named placeholder slot for checks; CI wires in later.

---

## Requirements

**Labels**

R1. All default GitHub labels are removed before new labels are created.

R2. The following semantic labels are created:

| Label | Color family | Purpose |
|---|---|---|
| `bug` | Red | Something isn't working |
| `feature` | Blue | New feature or request |
| `chore` | Yellow | Maintenance, tooling, deps |
| `docs` | Light blue | Documentation only |
| `refactor` | Purple | Code change, no behavior delta |
| `good first issue` | Green | Suitable for newcomers |
| `help wanted` | Green | Extra attention needed |
| `wontfix` | Grey | Intentionally not addressed |
| `duplicate` | Grey | Already tracked elsewhere |

R3. Type labels (`bug`, `feature`, `chore`, `docs`, `refactor`) share one color family; contribution labels (`good first issue`, `help wanted`) share another; resolution labels (`wontfix`, `duplicate`) are grey. Colors are consistent within each group.

**CLAUDE.md**

R4. `CLAUDE.md` at the repo root documents Conventional Commits as the commit convention, with the following prefixes: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `ci:`. Breaking changes use the `!` suffix (e.g., `feat!:`).

R4a. `CLAUDE.md` documents an atomic commit discipline: each commit covers exactly one concern type. Implementation, test, and documentation changes are never mixed in a single commit. A `feat:` commit contains only source changes; a `test:` commit contains only test additions or updates; a `docs:` commit contains only documentation changes. No enforced ordering between concern types within a branch.

R5. `CLAUDE.md` documents GitHub Flow: `main` is always in a deployable state; all work happens on short-lived branches; branches merge to `main` via PR and are deleted after merge.

R6. `CLAUDE.md` documents the branch naming convention: `<type>/<issue-number>-<short-description>`, where `<type>` matches the primary Conventional Commits prefix for the branch (`feat`, `fix`, `chore`, `docs`, `refactor`), `<issue-number>` is the GitHub issue number the branch addresses, and `<short-description>` is a lowercase kebab-case summary. Example: `feat/42-add-memory-export`, `fix/17-null-pointer-on-empty-list`.

**Issue and PR Templates**

R7. `.github/ISSUE_TEMPLATE/bug_report.md` covers: description, steps to reproduce, expected vs. actual behavior, environment info.

R8. `.github/ISSUE_TEMPLATE/feature_request.md` covers: motivation / problem being solved, proposed behavior, alternatives considered.

R8a. `.github/ISSUE_TEMPLATE/chore.md` covers: description of the maintenance task, motivation / why it is needed now, definition of done. Applies to dependency updates, refactoring, tooling changes, and other non-feature non-bug work — ensures every `chore/*` branch has a properly-framed issue to reference per the branch naming convention in R6.

R9. `.github/PULL_REQUEST_TEMPLATE.md` covers: summary of change, type of change (checklist: bug fix / new feature / chore / docs / refactor), brief test plan, linked issue reference (`Closes #<issue>`).

R10. Issue templates include a label suggestion field or front-matter `labels:` pointing to the label taxonomy in R2, so the right label is pre-selected on open.

**Branch Ruleset**

R11. A ruleset named `main-protection` is configured on the `main` branch via repository settings (Branch Rulesets, not the legacy Branch Protection Rules).

R12. The ruleset blocks direct pushes to `main`.

R13. The ruleset requires at least one pull request before merging (approval count: 0 for solo work, 1 for team work — set at configuration time).

R14. The ruleset does not require status checks in this initial version; a comment in the ruleset config (or in `CLAUDE.md`) notes the slot to add checks once CI is established.

R15. Force-push to `main` is blocked.

---

## Key Flows

- F1. **Setup sequence**
  - **Step 1 — Labels:** Delete all existing default labels via GitHub CLI or UI. Create the 9 labels from R2 with correct colors.
  - **Step 2 — CLAUDE.md:** Create `CLAUDE.md` at repo root with commit convention (R4), branch strategy (R5), and branch naming (R6).
  - **Step 3 — Templates:** Create `.github/ISSUE_TEMPLATE/bug_report.md`, `.github/ISSUE_TEMPLATE/feature_request.md`, `.github/ISSUE_TEMPLATE/chore.md`, and `.github/PULL_REQUEST_TEMPLATE.md` per R7–R10.
  - **Step 4 — Ruleset:** In GitHub repo settings → Rules → Rulesets, create `main-protection` targeting the `main` branch per R11–R15.

- F2. **First PR after scaffold**
  - Developer opens a GitHub issue, gets its number, creates a branch (`feat/7-add-export` per R6), commits atomically using Conventional Commits (R4, R4a), opens a PR — PR template auto-populates (R9), labels are available (R2), and the ruleset blocks merge until PR is opened (R12–R13).

---

## Scope Boundaries

**Deferred for later:**
- CI/CD pipeline and required status checks — ruleset has a placeholder slot; wire in when CI exists
- Automated label sync via GitHub Actions (e.g., label management as code in YAML)
- Release workflow, changelog generation, semantic-release tooling
- `CODEOWNERS` file — relevant when the team grows or ownership becomes non-trivial

**Outside this scaffold's scope:**
- Repository-level secrets or environment configuration
- Issue/PR automation (auto-assign, auto-label bots)

---

## Dependencies / Assumptions

- Repo is hosted on GitHub (required for Rulesets, which are a GitHub-native feature).
- Branch Rulesets (not legacy Branch Protection Rules) are used — available on all GitHub plan tiers as of 2024.
- Solo or very small team context: PR approval count defaults to 0 (solo) or 1 (team); adjust R13 at configuration time.
