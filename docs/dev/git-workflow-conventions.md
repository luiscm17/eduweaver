# Git Workflow Conventions

This document outlines the Git workflow conventions for the Eduweaver project, including commit messages, branch naming, and contribution guidelines.

## Table of Contents

1. [Commit Message Convention](#commit-message-convention)
2. [Branch Naming Convention](#branch-naming-convention)
3. [Git Workflow Process](#git-workflow-process)
4. [Pull Request Guidelines](#pull-request-guidelines)
5. [Code Review Process](#code-review-process)
6. [Release Process](#release-process)

---

## Commit Message Convention

### Golden Rules

1. **One change per commit:** If you fixed a bug AND changed a button color, make **two** separate commits.
2. **Use English:** All commit messages must be in English and start with lowercase.
3. **Use imperative mood:** Write "add method" instead of "added" or "adding". It's like giving a command to the code.
4. **Fixed structure:** Always use the format `type: description`.

### Message Structure

All commits must follow this format:

```bash
type: short description in lowercase
```

*Example: `feat: add validation to registration form`*

### Commit Types

| Type         | When to Use                                                        |
| ------------ | ------------------------------------------------------------------ |
| **feat**     | A new feature (e.g., new endpoint, agent, or functionality)        |
| **fix**      | Bug fix or error resolution                                        |
| **docs**     | Documentation changes only (README, comments, docs/)               |
| **style**    | Visual/formatting changes (spaces, commas) that don't affect logic |
| **refactor** | Code changes that neither fix a bug nor add a feature              |
| **test**     | Adding or correcting unit tests                                    |
| **chore**    | Maintenance tasks, dependency updates, configuration changes       |
| **perf**     | Performance improvements                                           |
| **ci**       | CI/CD configuration changes                                        |

### Commit Message Examples

**Bad (Avoid these):**

- `fix: it works now` (Vague and doesn't describe the solution)
- `changes` (Missing type and in Spanish)
- `feat: fix login and change footer and delete logo` (Too many responsibilities)

**Good:**

- `feat: connect products api`
- `fix: resolve typo in username field`
- `docs: update installation instructions in README.md`
- `style: fix indentation in auth controller`
- `refactor: extract validation logic to separate method`
- `test: add unit tests for research agent`
- `chore: update dependencies to latest versions`

### Extended Commit Format (Optional)

For complex changes, use the extended format:

```bash
type: short description

More detailed explanatory text, wrapped to 72 characters. Explain
what and why, not how. Use imperative mood.

Closes #123
```

---

## Branch Naming Convention

### Main Branches

| Branch    | Purpose                                    |
| --------- | ------------------------------------------ |
| `main`    | Production-ready code, always deployable   |
| `develop` | Integration branch for features (optional) |

### Supporting Branches

#### Feature Branches

```bash
feature/agent-name
feature/research-integration
feature/quality-enhancement
```

#### Bugfix Branches

```bash
fix/typo-in-configuration
fix/memory-leak-agent
fix/validation-error
```

#### Hotfix Branches

```bash
hotfix/critical-security-patch
hotfix/production-bug-fix
```

#### Release Branches

```bash
release/v1.0.0
release/v1.1.0
```

#### Documentation Branches

```bash
docs/api-documentation
docs/user-guide-update
```

### Branch Naming Rules

1. **Use lowercase** and hyphens (`-`) instead of underscores (`_`)
2. **Be descriptive** but concise (max 50 characters)
3. **Use prefixes** to indicate branch type
4. **Include ticket/issue number** when applicable: `feature/123-research-agent`

---

## Git Workflow Process

### 1. Create Feature Branch

```bash
# Create and switch to new feature branch
git checkout -b feature/research-intelligence

# Or create from develop (if using develop branch)
git checkout -b feature/research-intelligence develop
```

### 2. Make Changes

```bash
# Make your changes...
git add .
git commit -m "feat: implement research intelligence agent"
```

### 3. Keep Branch Updated

```bash
# Before creating PR, update with latest changes
git checkout main
git pull origin main
git checkout feature/research-intelligence
git rebase main
```

### 4. Create Pull Request

- Use descriptive PR title following commit convention
- Fill PR template with details
- Link related issues
- Request appropriate reviewers

---

## Pull Request Guidelines

### PR Title Format

Follow the same convention as commits:

```bash
feat: add research intelligence agent
fix: resolve memory leak in content generation
docs: update api documentation
```

### PR Description Template

Example:

```markdown
## Description
Brief description of changes made.

- Add research intelligence agent
- Update agent logic for better performance
- Modify agent logic for better performance
- Rename variables for better clarity

## Key Commits
- feat: implement research intelligence agent
- fix: resolve memory leak in content generation
- docs: update api documentation
```

### PR Requirements

1. **Clean history**: No merge commits in feature branches
2. **Tests included**: New features must include tests
3. **Documentation updated**: API changes require documentation updates
4. **Code quality**: Passes all linting and formatting checks

---

## Code Review Process

### Reviewer Guidelines

1. **Be constructive**: Focus on code quality, not personal preferences
2. **Explain reasoning**: Provide clear explanations for suggested changes
3. **Check functionality**: Verify the code works as intended
4. **Test coverage**: Ensure adequate test coverage
5. **Documentation**: Confirm documentation is accurate

### Author Responsibilities

1. **Address feedback**: Respond to all review comments
2. **Update PR**: Make requested changes promptly
3. **Communicate**: Explain if you disagree with suggestions
4. **Keep updated**: Rebase if main branch changes significantly

---

## Release Process

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with release notes
3. **Create release branch**: `git checkout -b release/v1.2.0`
4. **Final testing** on release branch
5. **Merge to main**: `git checkout main && git merge release/v1.2.0`
6. **Tag release**: `git tag v1.2.0`
7. **Push tags**: `git push origin v1.2.0`
8. **Delete release branch**: `git branch -d release/v1.2.0`

---

## Additional Guidelines

### Git Hooks

Consider using git hooks for:

- Pre-commit: Linting and formatting checks
- Pre-push: Running tests
- Commit-msg: Validating commit message format

### IDE Integration

Configure your IDE to:

- Show branch name in status bar
- Highlight uncommitted changes
- Integrate with Git workflows

### Conflict Resolution

1. **Communicate early**: Let team know about potential conflicts
2. **Small PRs**: Keep pull requests small to reduce conflicts
3. **Regular updates**: Rebase frequently with main branch
4. **Clean merges**: Use rebase instead of merge for feature branches

---

## Quick Reference

### Common Commands

```bash
# Start new feature
git checkout -b feature/your-feature-name

# Commit with proper message
git add .
git commit -m "feat: add your feature description"

# Update with latest main
git fetch origin
git rebase origin/main

# Create PR (using GitHub CLI)
gh pr create --title "feat: add your feature" --body "Description of changes"

# Clean up after merge
git checkout main
git pull origin main
git branch -d feature/your-feature-name
```

### Commit Message Template

```bash
type: brief description

Detailed explanation (optional)

Closes #issue-number
```

### Branch Name Template

```bash
type/description-with-hyphens
feature/research-agent
fix/validation-error
docs/api-update
release/v1.2.0
```

---

This document should be reviewed and updated as the project evolves. All team members should follow these conventions to maintain consistency and collaboration efficiency.
