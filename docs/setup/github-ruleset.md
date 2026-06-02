# GitHub Ruleset Setup

This ruleset configures `main-protection` for the default branch. It requires pull requests, blocks force pushes, and blocks branch deletion.

Run this command with `OWNER` and `REPO` replaced:

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

`required_approving_review_count` is set to `0` for solo use; bump it to `1` for team use.

```bash
# TODO: add "type": "required_status_checks" rule here once CI is established
```

## Verification

After running the command, navigate to GitHub -> Settings -> Rules -> Rulesets and confirm `main-protection` appears as active.
