#!/usr/bin/env bash
# Usage: bash docs/setup/labels.sh <owner/repo>
REPO="${1:?Usage: $0 owner/repo}"

DEFAULT_LABELS=("bug" "documentation" "duplicate" "enhancement" \
  "good first issue" "help wanted" "invalid" "question" "wontfix")

for label in "${DEFAULT_LABELS[@]}"; do
  gh label delete "$label" --repo "$REPO" --yes 2>/dev/null || true
done

gh label create "bug"              --color "d73a4a" --description "Something isn't working"       --force --repo "$REPO"
gh label create "feature"          --color "0075ca" --description "New feature or request"         --force --repo "$REPO"
gh label create "chore"            --color "e4e669" --description "Maintenance, tooling, deps"     --force --repo "$REPO"
gh label create "docs"             --color "bfd4f2" --description "Documentation only"             --force --repo "$REPO"
gh label create "refactor"         --color "7936a5" --description "Code change, no behavior delta" --force --repo "$REPO"
gh label create "good first issue" --color "008672" --description "Suitable for newcomers"        --force --repo "$REPO"
gh label create "help wanted"      --color "008672" --description "Extra attention needed"         --force --repo "$REPO"
gh label create "wontfix"          --color "cfd3d7" --description "Intentionally not addressed"    --force --repo "$REPO"
gh label create "duplicate"        --color "cfd3d7" --description "Already tracked elsewhere"      --force --repo "$REPO"
