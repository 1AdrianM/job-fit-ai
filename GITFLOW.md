# Git Flow Branching Strategy

## 🌳 Branch Structure

```
main (production)
  ├── develop (integration)
  │   ├── feature/user-auth
  │   ├── feature/cv-upload
  │   └── feature/job-scraper
  ├── release/v1.0.0
  └── hotfix/critical-bug-fix
```

---

## 📋 Branch Types

### 🟢 `main` - Production
- **Purpose:** Production-ready code only
- **Protected:** Yes (requires PR + reviews)
- **Deploys to:** Render (production)
- **Lifetime:** Permanent

### 🟡 `develop` - Integration
- **Purpose:** Latest development changes
- **Protected:** Yes (requires PR)
- **Deploys to:** Render (staging/preview)
- **Lifetime:** Permanent

### 🔵 `feature/*` - New Features
- **Purpose:** Develop new features
- **Branched from:** `develop`
- **Merged into:** `develop`
- **Naming:** `feature/feature-name`
- **Example:** `feature/cv-upload`, `feature/email-templates`
- **Lifetime:** Temporary (deleted after merge)

### 🟣 `release/*` - Release Preparation
- **Purpose:** Prepare a new production release
- **Branched from:** `develop`
- **Merged into:** `main` AND `develop`
- **Naming:** `release/v1.0.0`
- **Lifetime:** Temporary (deleted after merge)

### 🔴 `hotfix/*` - Emergency Fixes
- **Purpose:** Critical production bug fixes
- **Branched from:** `main`
- **Merged into:** `main` AND `develop`
- **Naming:** `hotfix/critical-bug-name`
- **Example:** `hotfix/api-timeout`, `hotfix/security-patch`
- **Lifetime:** Temporary (deleted after merge)

---

## 🚀 Workflow

### Starting a new feature

```bash
# 1. Update develop
git checkout develop
git pull origin develop

# 2. Create feature branch
git checkout -b feature/my-awesome-feature

# 3. Work on your feature
git add .
git commit -m "feat: add awesome feature"

# 4. Push to remote
git push origin feature/my-awesome-feature

# 5. Open PR to develop on GitHub
# GitHub → Pull Requests → New Pull Request
# Base: develop ← Compare: feature/my-awesome-feature
```

### Preparing a release

```bash
# 1. Create release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# 2. Update version numbers, changelog, etc.
# Edit files...
git commit -m "chore: bump version to 1.0.0"

# 3. Push release branch
git push origin release/v1.0.0

# 4. Open TWO PRs:
#    PR 1: release/v1.0.0 → main (production deploy)
#    PR 2: release/v1.0.0 → develop (merge back changes)

# 5. After merging to main, tag the release
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### Hotfix for production

```bash
# 1. Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug

# 2. Fix the bug
git add .
git commit -m "fix: resolve critical bug"

# 3. Push hotfix
git push origin hotfix/critical-bug

# 4. Open TWO PRs:
#    PR 1: hotfix/critical-bug → main (immediate deploy)
#    PR 2: hotfix/critical-bug → develop (keep in sync)

# 5. After merging, tag if needed
git checkout main
git pull origin main
git tag -a v1.0.1 -m "Hotfix v1.0.1"
git push origin v1.0.1
```

---

## 🤖 Git Flow Helper Script

We provide a helper script for common operations:

```bash
# Start a new feature
./scripts/gitflow.sh feature start my-feature

# Finish a feature (creates PR)
./scripts/gitflow.sh feature finish

# Start a release
./scripts/gitflow.sh release start 1.0.0

# Start a hotfix
./scripts/gitflow.sh hotfix start critical-bug
```

---

## 📏 Branch Protection Rules

### `main` branch
- ✅ Require pull request before merging
- ✅ Require approvals (1)
- ✅ Require status checks to pass (CI tests)
- ✅ Require branches to be up to date
- ✅ Do not allow bypassing settings
- ✅ Do not allow force pushes
- ✅ Do not allow deletions

### `develop` branch
- ✅ Require pull request before merging
- ✅ Require status checks to pass (CI tests)
- ✅ Require branches to be up to date
- ✅ Do not allow force pushes
- ✅ Do not allow deletions

---

## 📝 Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add new feature
fix: fix a bug
docs: documentation changes
style: code style (formatting, etc)
refactor: code refactoring
test: add or update tests
chore: build/tooling changes
perf: performance improvements
ci: CI/CD changes
```

**Examples:**
```bash
git commit -m "feat: add CV upload functionality"
git commit -m "fix: resolve Gemini API timeout"
git commit -m "docs: update deployment guide"
git commit -m "test: add E2E tests for analysis flow"
```

---

## 🔄 CI/CD Integration

### Automated Testing
- **On:** Every push to any branch
- **Runs:** 17 Playwright E2E tests + linting
- **Result:** Must pass before merge

### Deployment
- **`main` branch → Production** (Render)
- **`develop` branch → Staging** (Render preview)
- **Feature branches → No deploy** (tests only)

---

## 📊 Version Numbering

We use [Semantic Versioning](https://semver.org/):

```
v1.2.3
│ │ │
│ │ └─ PATCH: Bug fixes, minor changes
│ └─── MINOR: New features (backward compatible)
└───── MAJOR: Breaking changes
```

**Examples:**
- `v1.0.0` → Initial release
- `v1.1.0` → Added job scraper feature
- `v1.1.1` → Fixed API bug
- `v2.0.0` → Changed API (breaking)

---

## 🎯 Best Practices

1. **Keep features small** - Easier to review and merge
2. **Update often** - Pull from develop frequently
3. **Write good commit messages** - Follow conventions
4. **Test before PR** - Run tests locally first
5. **Review your own PR** - Check the diff before requesting review
6. **Delete merged branches** - Keep the repo clean
7. **Use draft PRs** - For work in progress
8. **Tag releases** - Always tag production releases

---

## 🆘 Common Issues

### Merge conflicts?
```bash
# Update your branch with latest develop
git checkout feature/my-feature
git fetch origin
git merge origin/develop
# Resolve conflicts, then:
git add .
git commit -m "chore: resolve merge conflicts"
git push
```

### Accidentally committed to wrong branch?
```bash
# Move last commit to a new branch
git checkout -b feature/correct-branch
git checkout develop
git reset --hard HEAD~1
```

### Need to update a merged PR?
```bash
# Don't! Create a new PR instead
git checkout develop
git pull origin develop
git checkout -b feature/follow-up-fix
# Make changes...
git push origin feature/follow-up-fix
```

---

## 📚 Resources

- [Git Flow Cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)

---

## 🎓 Quick Reference

```bash
# Daily workflow
git checkout develop
git pull origin develop
git checkout -b feature/new-thing
# ... work work work ...
git add .
git commit -m "feat: add new thing"
git push origin feature/new-thing
# Open PR on GitHub: feature/new-thing → develop

# After PR merged
git checkout develop
git pull origin develop
git branch -d feature/new-thing
```

---

**Questions?** Open an issue or contact [@1AdrianM](https://github.com/1AdrianM)
