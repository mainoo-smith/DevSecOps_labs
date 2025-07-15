# 🚀 Week 2 Challenge — Automate Server Security

## 🎯 Goal
Automate a repeatable secure server setup.

## 5W1H
**Who**: Any engineer spinning up VMs.  
**What**: Script basic security tasks.  
**When**: Each new server or container base image.  
**Where**: Cloud or on-prem.  
**Why**: Manual setup is error-prone; automation saves time.  
**How**: Use bash scripting.

## Steps
1️⃣ Write `secure_server.sh` to:
- Add new sudo user
- Setup SSH keys
- Disable root login
- Enable UFW with port 22 open only
- Log actions to `/var/log/secure_server.log`

2️⃣ Test on a fresh VM.

3️⃣ Push script to `week2/` in repo.

## Analogy
It’s like using a master checklist to lock every door in a new office building.


---

### ✅ **`challenge.md`**

```markdown
# 🚀 Week 2 Challenge — Build a Hardened Linux Template

## 🎯 Goal

Create a **golden image checklist** for your company.

---

## 5W1H

- **Who**: All engineers must start servers from this baseline.
- **What**: Secure SSH, fail2ban, firewalls, logging.
- **When**: For every new server or container.
- **Where**: Local VM → cloud → containers.
- **Why**: Consistency & compliance.
- **How**: Write it up & script what you can.

---

## Steps

1️⃣ Harden SSH config, firewall, fail2ban.

2️⃣ Script user creation & cron tasks.

3️⃣ Document monitoring & audit commands.

✅ Save it all in `week2/hardened-template.md`.

✅ Bonus: Test your script on a fresh VM.
