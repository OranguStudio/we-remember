---
date: 2026-06-02
status: active
origin: docs/brainstorms/2026-06-02-repo-governance-scaffold-requirements.md
topic: repo-governance-scaffold
type: chore
---

# chore: Scaffold Repo Governance

## Summary

Replace GitHub's default labels with a 9-label semantic set, author `CLAUDE.md` with Conventional Commits and GitHub Flow conventions, create three issue templates and a PR template aligned to those conventions, and configure a `main-protection` branch ruleset via `gh api`. Setup follows a define-before-enforce order: labels → CLAUDE.md → templates → ruleset.

---

## Problem Frame

A fresh repo inherits GitHub's default label rainbow, has no commit convention, no branch strategy, and no templates — every contributor (or future agent) must invent these locally. Scaffolding them as a coordinated set before real work lands makes the conventions load-bearing from day one rather than retrofitted later. (see origin: `docs/brainstorms/2026-06-02-repo-governance-scaffold-requirements.md`)

---

## Key Technical Decisions

**Label management via committed shell script.** `docs/setup/labels.sh` uses `gh label` commands to delete all defaults and create the 9 semantic labels with concrete hex colors. This makes the configuration reproducible and version-controlled rather than a one-time, undocumented manual action.

**Ruleset documented as `gh api` JSON payload.** GitHub branch rulesets are server-side configuration — they cannot live as a repo file that auto-applies. `docs/setup/github-ruleset.md` holds the complete `gh api` command with an inline JSON payload, making the ruleset auditable and re-runnable without UI navigation.

**Issue template `labels:` front-matter for auto-selection.** GitHub supports pre-selecting labels via YAML front matter in issue templates. Using this field eliminates the need for contributors to remember the label taxonomy when opening an issue.

**CLAUDE.md as single source of truth for all conventions.** Commit, branch, and flow conventions live in one root-level file that both human contributors and Claude Code read before taking action. Keeping all conventions co-located prevents drift between multiple docs files.

---

## Output Structure

```
we-remember/
├── CLAUDE.md                                   ← new
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md                       ← new
│   │   ├── feature_request.md                  ← new
│   │   └── chore.md                            ← new
│   └── PULL_REQUEST_TEMPLATE.md                ← new
└── docs/
    └── setup/
        ├── labels.sh                           ← new
        └── github-ruleset.md                  ← new
```

---

## Implementation Units

### U1. Replace GitHub labels

**Goal:** Remove all default GitHub labels and create the 9 semantic labels with concrete hex colors.

**Requirements:** R1, R2, R3

**Dependencies:** none

**Files:**
- `docs/setup/labels.sh` — create

**Approach:**

The script deletes GitHub's 9 default labels by name, then creates the semantic set. Concrete colors per group:

| Label | Hex | Group |
|---|---|---|
| `bug` | `#d73a4a` | type — red |
| `feature` | `#0075ca` | type — blue |
| `chore` | `#e4e669` | type — yellow |
| `docs` | `#bfd4f2` | type — light blue |
| `refactor` | `#7936a5` | type — purple |
| `good first issue` | `#008672` | contribution — green |
| `help wanted` | `#008672` | contribution — green |
| `wontfix` | `#cfd3d7` | resolution — grey |
| `duplicate` | `#cfd3d7` | resolution — grey |

Default labels to delete: `bug`, `documentation`, `duplicate`, `enhancement`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`.

Script shape (directional — not copy-paste implementation):

```bash
#!/usr/bin/env bash
# Usage: bash docs/setup/labels.sh <owner/repo>
REPO="${1:?Usage: $0 owner/repo}"

# Delete defaults
DEFAULT_LABELS=("bug" "documentation" "duplicate" "enhancement" \
  "good first issue" "help wanted" "invalid" "question" "wontfix")
for label in "${DEFAULT_LABELS[@]}"; do
  gh label delete "$label" --repo "$REPO" --yes 2>/dev/null || true
done

# Create semantic labels
gh label create "bug"             --color "d73a4a" --description "Something isn't working"       --force --repo "$REPO"
gh label create "feature"         --color "0075ca" --description "New feature or request"         --force --repo "$REPO"
gh label create "chore"           --color "e4e669" --description "Maintenance, tooling, deps"     --force --repo "$REPO"
gh label create "docs"            --color "bfd4f2" --description "Documentation only"             --force --repo "$REPO"
gh label create "refactor"        --color "7936a5" --description "Code change, no behavior delta" --force --repo "$REPO"
gh label create "good first issue" --color "008672" --description "Suitable for newcomers"        --force --repo "$REPO"
gh label create "help wanted"     --color "008672" --description "Extra attention needed"         --force --repo "$REPO"
gh label create "wontfix"         --color "cfd3d7" --description "Intentionally not addressed"   --force --repo "$REPO"
gh label create "duplicate"       --color "cfd3d7" --description "Already tracked elsewhere"     --force --repo "$REPO"
```

**Patterns to follow:** No existing patterns — establishing conventions from scratch.

**Test scenarios:**
- After running the script, `gh label list --repo owner/repo` returns exactly 9 labels matching the names in R2.
- No default GitHub labels remain (`documentation`, `enhancement`, `invalid`, `question` are gone).
- Each label shows the correct color hex when listed.
- Running the script a second time does not error (idempotent: `--yes` flag and `|| true` handle missing-label deletes gracefully; duplicate creates should be handled via `--force` flag if needed).

**Verification:** `gh label list --repo owner/repo --json name,color | jq .` shows exactly the 9 labels with correct colors. All defaults absent.

---

### U2. Create CLAUDE.md

**Goal:** Document Conventional Commits with atomic discipline, GitHub Flow, and the issue-number branch naming convention as the single source of truth for all repo conventions.

**Requirements:** R4, R4a, R5, R6, R14 (CI slot note)

**Dependencies:** none

**Files:**
- `CLAUDE.md` — create

**Approach:**

CLAUDE.md contains five sections:

1. **Commit Convention** — Conventional Commits prefix table (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `ci:`), breaking change suffix (`!`), and scope usage.

2. **Atomic Commit Discipline** — One concern per commit. Implementation, tests, and documentation are always in separate commits. A `feat:` commit contains only source changes; `test:` only test changes; `docs:` only documentation. No enforced ordering between types within a branch.

3. **Branch Strategy (GitHub Flow)** — `main` is always deployable. All work happens on short-lived branches. Branches merge to `main` via PR and are deleted after merge.

4. **Branch Naming** — Pattern: `<type>/<issue-number>-<short-description>`. Type matches the primary commit prefix. Issue number is mandatory (every branch must reference a tracked issue). Short description is lowercase kebab-case. Examples: `feat/42-add-memory-export`, `fix/17-null-pointer-on-empty`, `chore/8-upgrade-dependencies`.

5. **CI Placeholder note** — A section or comment noting that the `main-protection` branch ruleset currently requires no status checks; this slot is reserved for CI checks once a pipeline is established.

**Patterns to follow:** No existing patterns — establishing conventions from scratch.

**Test scenarios:**
- `Test expectation: none — CLAUDE.md is a documentation file, not executable code.`

**Verification:** File exists at repo root. All five topic areas are present and internally consistent (branch naming examples match the pattern; commit prefixes in the table align with the label taxonomy in U1).

---

### U3. Create issue templates and PR template

**Goal:** Create three issue templates (bug, feature, chore) with pre-selected labels and a PR template with type checklist and issue reference.

**Requirements:** R7, R8, R8a, R9, R10

**Dependencies:** U1 (label names must exist before `labels:` front-matter references them), U2 (PR template references commit convention)

**Files:**
- `.github/ISSUE_TEMPLATE/bug_report.md` — create
- `.github/ISSUE_TEMPLATE/feature_request.md` — create
- `.github/ISSUE_TEMPLATE/chore.md` — create
- `.github/PULL_REQUEST_TEMPLATE.md` — create

**Approach:**

Each issue template uses GitHub YAML front matter. Directional shape:

```yaml
---
name: Bug Report
about: Report something that isn't working
title: "[Bug] "
labels: bug
assignees: ""
---
```

Bug report body sections: **Description**, **Steps to Reproduce**, **Expected Behavior**, **Actual Behavior**, **Environment**.

Feature request body sections: **Motivation / Problem**, **Proposed Behavior**, **Alternatives Considered**.

Chore body sections: **Task Description**, **Motivation / Why Now**, **Definition of Done**.

PR template (no YAML front matter — applies to all PRs in the repo) contains:

- **Summary** — one-paragraph description of the change
- **Type of change** — checklist: `[ ] bug fix`, `[ ] new feature`, `[ ] chore`, `[ ] docs`, `[ ] refactor`
- **Test plan** — brief description of how the change was tested
- **Linked issue** — `Closes #` line

**Patterns to follow:** Standard GitHub issue template YAML front-matter format. PR template uses no YAML front matter (GitHub auto-loads `.github/PULL_REQUEST_TEMPLATE.md`).

**Test scenarios:**
- On GitHub, navigating to Issues → New Issue shows three templates: "Bug Report", "Feature Request", "Chore" — each with the correct pre-selected label visible in the sidebar.
- Opening a new PR populates the description with the PR template body.
- Bug report template pre-selects the `bug` label; feature request pre-selects `feature`; chore pre-selects `chore`.
- All template section headers match the requirements (Steps to Reproduce present in bug; Definition of Done present in chore; Closes # line present in PR template).

**Verification:** Open a test issue using each template on GitHub. Confirm pre-selected label, section headers, and placeholder text match requirements. Open a test PR and confirm the template populates.

---

### U4. Document branch ruleset via gh api

**Goal:** Produce a reproducible `gh api` setup guide that configures the `main-protection` ruleset: no direct push, PRs required, no force push.

**Requirements:** R11, R12, R13, R14, R15

**Dependencies:** U2 (CLAUDE.md defines the conventions the ruleset enforces; both should exist before the ruleset is applied)

**Files:**
- `docs/setup/github-ruleset.md` — create

**Approach:**

The setup guide contains:

1. A brief explanation of what the ruleset enforces.
2. The complete `gh api` command with an inline heredoc JSON payload. Directional shape:

```bash
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /repos/OWNER/REPO/rulesets \
  --input - <<'EOF'
{
  "name": "main-protection",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["~DEFAULT_BRANCH"],
      "exclude": []
    }
  },
  "rules": [
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": false
      }
    },
    { "type": "non_fast_forward" },
    { "type": "deletion" }
  ]
}
EOF
```

3. A note that `required_approving_review_count` is set to `0` for solo use; bump to `1` for team use.
4. A placeholder comment: `# TODO: add "type": "required_status_checks" rule here once CI is established`.
5. Verification steps: after running, navigate to GitHub → Settings → Rules → Rulesets to confirm `main-protection` appears as active.

**Patterns to follow:** No existing patterns — establishing conventions from scratch.

**Test scenarios:**
- After running the `gh api` command, `gh api /repos/OWNER/REPO/rulesets` lists a ruleset named `main-protection` with `enforcement: active`.
- Attempting `git push origin main` from a local commit directly (bypassing PR) is rejected with a ruleset error.
- Force-push (`git push --force origin main`) is rejected.
- Opening a PR and merging normally succeeds.

**Verification:** Ruleset appears in GitHub Settings → Rules → Rulesets as active. Direct push to main blocked. Normal PR merge succeeds.

---

## Scope Boundaries

### Deferred for later
- CI/CD pipeline and required status checks — the ruleset JSON in U4 includes a placeholder comment for the `required_status_checks` rule
- Automated label sync via GitHub Actions
- Release workflow, changelog generation, semantic-release tooling
- `CODEOWNERS` file

### Outside this scaffold's scope
- Repository-level secrets or environment configuration
- Issue/PR automation (auto-assign, auto-label bots)

---

## Dependencies / Assumptions

- GitHub CLI (`gh`) is authenticated and has write access to the repo before running `docs/setup/labels.sh` and `docs/setup/github-ruleset.md`.
- Branch Rulesets (not legacy Branch Protection Rules) are used — available on all GitHub plan tiers.
- `required_approving_review_count` in U4 defaults to `0`; adjust to `1` if a reviewer is required.
- CI status checks are not yet defined — the ruleset intentionally omits `required_status_checks` and documents where to add them later.
