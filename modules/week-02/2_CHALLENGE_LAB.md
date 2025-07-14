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