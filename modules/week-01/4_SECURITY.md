# Security – Week 1: Git & Branch Protection

## 🛡️ Why This Matters:
- Main branch is your **production infrastructure**
- Bad merges = broken apps or exposed secrets

## ✅ Git Security Best Practices:
- Require PR reviews
- Require signed commits (`git config commit.gpgsign true`)
- Protect `main` with:
   - Status checks
   - Disallow force pushes
   - Require up-to-date branches

## 🧠 Bonus:
Try setting up `CODEOWNERS` to define who can approve certain files/services.

