# 🔒 Week 3 Security — Git & Secrets Management

## Key Principles (5W1H)

- **Who** must protect credentials? You, always.
- **What** should be ignored? `.env`, keys, passwords.
- **When** do you scan? Before pushing — every commit.
- **Where** do secrets belong? Secret managers, not repos.
- **Why**? Public repos leaking secrets are a major attack vector.
- **How**? Use `.gitignore`, scan commits, rotate keys immediately if exposed.

---

## Practical Example

Imagine you accidentally commit an AWS key — it gets picked up by bots in minutes.  
Always use tools like `git-secrets` or `truffleHog` to scan repos.

## Analogy

Git is like your company’s knowledge vault — you wouldn’t tape your office safe’s combination to the front door!
