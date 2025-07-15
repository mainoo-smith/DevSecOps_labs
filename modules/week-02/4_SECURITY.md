# 🔒 Week 2 Security — Secure the OS Layer

## Key Principles (5W1H)
- **Who** is responsible? You & your team — shared responsibility.
- **What** must be secured? Accounts, SSH, firewall.
- **When** to secure? During provisioning — “Shift Left”!
- **Where** does this apply? Cloud, local VMs, containers.
- **Why**? Misconfigurations = breach risk.
- **How**? Automate security best practices.

## Tips
- No root SSH login.
- SSH keys only.
- Keep OS updated.
- Least privilege access.

## Analogy
Securing Linux is like changing default door locks & giving keys only to those who really need them.

# 🔒 Week 2 Security — Real Linux Hardening

## Key Practices

- Rotate SSH keys regularly.
- Use fail2ban to block brute force attempts.
- Always use least privilege — never stay root.
- Automate audits & alert on suspicious logins.
- Keep OS up to date.

---

## Real-World Example

In 2022, a crypto mining botnet spread via poorly secured Linux SSH ports.  
Harden your base image and automate monitoring to catch issues fast.

---

## Analogy

Think of your Linux server like your home:
- SSH keys = locks
- fail2ban = alarm system
- logs = security cameras
- cron jobs = your housekeeper’s daily checklist
