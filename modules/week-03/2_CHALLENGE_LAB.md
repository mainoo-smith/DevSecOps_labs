
---

### ✅ **`challenge.md`**

```markdown
# 🚀 Week 3 Challenge — Build a Real Git Workflow

## 🎯 Goal

Simulate a small team’s workflow:
- Branching strategy
- PRs/MRs
- Code reviews
- Rollbacks

---

## 5W1H

- **Who**: You + any collaborator (or simulate with two branches).
- **What**: Use feature/hotfix branches, PRs, and rebases.
- **When**: Always in real projects.
- **Where**: GitHub or GitLab.
- **Why**: Build habits for clean, safe automation and CI/CD.
- **How**: Do it hands-on.

---

## Steps

1️⃣ Create 2 new branches: `feature/add-script` and `hotfix/typo-fix`.  
2️⃣ Add a sample shell script in `week3/`.
3️⃣ Push both branches, open PRs.
4️⃣ Review & merge `feature/add-script` first.
5️⃣ Rebase `hotfix/typo-fix` onto `main` and merge it.
6️⃣ Tag your repo at this point: `v0.1`.

---

## ✅ Success Criteria

- Repo has multiple branches and a clean history.
- Conflicts handled properly.
- Tags used for releases.
- Push all to your remote repo.


---

### 🏆 **Updated Challenge**

```markdown
## ✅ Week 3 Challenge (Extended) — Production-Ready Git Controls

**Scenario:**  
Your team’s `main` branch is the single source of truth for deployments to staging and production. You must ensure every change is reviewed, tested, and signed.

**Task:**  
- Add a `main` branch protection rule.
- Require at least 1 review, passing CI checks, and signed commits.
- Simulate a push that gets rejected.
- Open a PR, get approval (or simulate with a second account).
- Document the workflow in `week3/protected-branch-playbook.md`.

✅ **Bonus:** Connect this to your pipeline:
- How does your CI/CD verify commits before deploying?

