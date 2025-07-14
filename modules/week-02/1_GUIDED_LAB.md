# 🛠 Week 2 Guided Lab — Working with Linux

## 5W1H: Why This Lab?
**Who**: You, acting as a junior DevOps engineer.  
**What**: Learn to set up & secure a Linux server.  
**When**: Every time you deploy or maintain servers.  
**Where**: Local, cloud, or containers.  
**Why**: Secure infra is your first line of defense.  
**How**: Practice real tasks, repeat often.

## 📌 Prerequisites
- Cloud or local VM.
- SSH client.

## 1️⃣ Launch a Linux VM
- Use AWS EC2 Free Tier, DigitalOcean, or VirtualBox.

## 2️⃣ Connect via SSH
```bash
ssh -i mykey.pem ubuntu@your-vm-ip
whoami
hostname
```

## 3️⃣ Create a Non-Root User
```bash
sudo adduser devopsstudent
sudo usermod -aG sudo devopsstudent
su - devopsstudent
```

## 4️⃣ Navigate & Manage Files
Try:
- `ls`, `cd`, `pwd`
- `chmod`, `chown`
- Create `scripts/` and `logs/` directories.

## 5️⃣ Write & Run a Script
```bash
nano hello.sh
```
```bash
#!/bin/bash
echo "Hello!"
date
```
Make it executable: `chmod +x hello.sh`

## 6️⃣ Basic Networking
- `ip a`, `ss -tuln`, `ping`, `curl`

## ✅ Deliverables
- Non-root user with sudo.
- SSH keys configured.
- Script working.
- `week2/cli_notes.md` in your repo.

## Analogy
Think of `chmod` as setting who can open which doors in your building.