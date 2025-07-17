# Guided Lab – Week 1: Git + Collaboration

### ✅ Goal:
Simulate how real teams use Git to collaborate, review code, and protect critical branches.

---

## 🧪 Step 1: Initialize the Git Project

```bash
git init ecommerce-platform
cd ecommerce-platform
mkdir frontend backend-api auth-service db
git add .
git commit -m "Initialize project structure" 
```

## 🔀 Step 2: Create a Feature Branch (e.g., Auth)
```bash git checkout -b feature/auth-service
touch auth-service/main.py
git add .
git commit -m "Add placeholder for auth service"
```

## 📤 Step 3: Push to Remote Repo
```bash git remote add origin https://github.com/YOUR_USER/ecommerce-platform.git
git push -u origin feature/auth-service
```

## 📥 Step 4: Pull Request + Review Simulation
1. Go to GitHub → Compare & Pull Request.
2. Review your own PR or invite a teammate.
3. Enable branch protection:
   - Require PR review before merging
   - Require status checks to pass
   - Prevent force pushes

## 🔁 Step 5: Merge + Rebase Flow
Create a new branch
```bash 
git checkout -b feature/backend-api
echo "print('Hello from backend')" > backend-api/main.py
git add .
git commit -m "Initial backend service"
git push -u origin feature/backend-api
```
Merge auth branch first via PR - then try to rebase backend:

```bash
git checkout feature/backend-api
git pull origin main --rebase
# resolve conflicts if any
git push -f origin feature/backend-api
```
## 🧼 Step 6: Squash Commits Before Merge
Use GitHub’s “Squash & Merge” to keep main history clean.

## ✅ Outcome:
 - Project repo initialized with real structure
 - Two features merged via PRs
 - Branch protection + rebase flow in action
