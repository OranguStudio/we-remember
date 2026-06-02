# Repository Conventions

## Commit Convention

Use Conventional Commits.

| Prefix | Use |
|---|---|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `chore:` | Maintenance, tooling, dependencies |
| `docs:` | Documentation only |
| `refactor:` | Code change with no behavior delta |
| `test:` | Tests only |
| `ci:` | CI configuration |

Use `!` after the type or scope for breaking changes, such as `feat!:` or `feat(api)!:`.

Use scopes when they clarify the affected area, such as `feat(memory): add export`.

## Atomic Commit Discipline

Use one concern per commit. Implementation, tests, and documentation are always separate commits.

A `feat:` commit contains only source changes. A `test:` commit contains only test changes. A `docs:` commit contains only documentation.

There is no enforced ordering between commit types within a branch.

## Branch Strategy

Use GitHub Flow.

`main` is always deployable. All work happens on short-lived branches. Branches merge to `main` via pull request and are deleted after merge.

## Branch Naming

Use this pattern:

```text
<type>/<issue-number>-<short-description>
```

The type matches the primary commit prefix. The issue number is mandatory; every branch must reference a tracked issue. The short description is lowercase kebab-case.

Examples:

```text
feat/42-add-memory-export
fix/17-null-pointer-on-empty
chore/8-upgrade-dependencies
```

## CI Placeholder

The `main-protection` branch ruleset currently requires no status checks. This slot is reserved for CI checks once a pipeline is established.
