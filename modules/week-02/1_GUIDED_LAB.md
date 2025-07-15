# 🛠 Week 2 Guided Lab — Advanced Linux & OS Essentials

## 🔍 5W1H: Why This Lab?

- **Who**: You, acting as a SysAdmin for production workloads.
- **What**: Secure, monitor, and automate on Linux.
- **When**: Daily — for container images, cloud servers, pipelines.
- **Where**: Local VM or cloud EC2.
- **Why**: 80% of incidents come from poor OS config & monitoring.
- **How**: Practice these tasks step-by-step.

---

## 📌 Prerequisites

- Local Linux VM or cloud VM (AWS Free Tier).
- SSH key pair.

---

## 1️⃣ Hardening SSH

✅ Disable root login:
```bash
sudo nano /etc/ssh/sshd_config
# Set PermitRootLogin no
sudo systemctl restart ssh
```

✅ Change default SSH port to 2222 for extra obscurity:
```bash
# Change Port 22 to Port 2222 in sshd_config
sudo systemctl restart ssh
```

✅ Test:
```bash
ssh -p 2222 devopsstudent@your-server-ip
```

---

## 2️⃣ Install fail2ban

```bash
sudo apt update
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
sudo fail2ban-client status
```

---

## 3️⃣ System Monitoring

✅ Use:
```bash
top
htop
ps aux --sort=-%mem | head
df -h
journalctl -xe
```

✅ Identify suspicious processes & disk usage.

---

## 4️⃣ Automate with cron

✅ Create a cron job:
```bash
crontab -e
# Example: run script every day at 2am
0 2 * * * /home/devopsstudent/scripts/backup.sh
```

✅ Write `backup.sh`:
```bash
#!/bin/bash
tar -czvf /home/devopsstudent/backup_$(date +%F).tar.gz /home/devopsstudent/data/
```

✅ Log output to `/var/log/backup.log`.

---

## 5️⃣ User Audit & Cleanup

✅ List all users:
```bash
cut -d: -f1 /etc/passwd
```

✅ Check last login:
```bash
last
```

✅ Lock old or unused accounts:
```bash
sudo usermod -L olduser
```

✅ Use `auditd` (optional advanced):
```bash
sudo apt install auditd
sudo auditctl -w /etc/passwd -p wa
```

Monitor `/var/log/audit/audit.log`.

---

## ✅ Deliverables

- `hardening-notes.md` describing your SSH & fail2ban setup.
- `backup.sh` in your repo.
- Screenshots/logs for monitoring tools.

---

## 🏗️ Real Project Context

You’ll use this hardened VM as your **base image** for cloud instances and Docker containers later.