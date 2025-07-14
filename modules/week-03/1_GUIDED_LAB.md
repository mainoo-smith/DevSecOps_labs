# 🛠 Week 3 Guided Lab — Version Control in Action

## 🔍 5W1H: Why This Lab?

- **Who**: Any engineer who collaborates on code or config.
- **What**: Practice daily Git operations.
- **When**: Every change you make to IaC, pipelines, scripts.
- **Where**: Local and pushed to your remote repo.
- **Why**: So you don’t lose work, break pipelines, or deploy old code.
- **How**: Hands-on steps below!

---

## 1️⃣ Clone Your Bootcamp Repo

```bash
git clone https://github.com/YOUR_USERNAME/devops-bootcamp.git
cd devops-bootcamp
```

---

## 2️⃣ Create a Feature Branch

```bash
git checkout -b feature/week3-lab
```

Add a new file: `touch week3/notes.md`

---

## 3️⃣ Commit & Push

```bash
git add week3/notes.md
git commit -m "Add Week 3 notes file"
git push origin feature/week3-lab
```

---

## 4️⃣ Create a Pull Request

- Open a PR (or Merge Request if using GitLab).
- Add a clear description: *“Added notes file for Week 3 guided lab.”*

---

## 5️⃣ Simulate a Merge Conflict

- In `main`, edit `notes.md` and push.
- In your branch, edit the same line and push.
- Try to merge → Git will show a conflict.

Resolve:
```bash
git pull origin main
# Open file, fix conflict markers <<<< ===== >>>>
git add .
git commit -m "Resolve conflict"
git push
```

---

## 6️⃣ Stash Changes

- Modify a file but don’t commit:
```bash
echo "WIP change" >> week3/notes.md
git stash
```

- Apply stash:
```bash
git stash apply
```

---

## 7️⃣ Roll Back a Commit

- Undo the last commit but keep changes staged:
```bash
git reset --soft HEAD~1
```

---

## ✅ Deliverables

- Feature branch created and merged.
- Conflict resolved in `notes.md`.
- Commit history clean and pushed.
- Save key commands in `week3/git_commands.md`.

---

## 🗝️ Analogy

Conflict resolution is like two people editing the same paragraph in Google Docs —  
Git helps you merge those changes safely, but *you* have to decide which version wins.