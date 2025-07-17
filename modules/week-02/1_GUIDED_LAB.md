# Guided Lab – Week 2: Linux + SSH + Server Hardening

---

## 🔧 Project Setup: First EC2 for Internal DevOps Tools

You're about to secure your **first EC2 instance** which will be used later to:

- Run Ansible playbooks
- Execute early CI/CD deployment jobs
- Possibly expose a staging frontend or API
- Log backups or cron-based scripts

This will serve as your **internal platform ops server**.

---

## ☁️ Step 1: Provision an EC2 Instance

- Use AWS Console or Terraform to provision:
  - OS: Ubuntu 22.04 LTS or Amazon Linux 2
  - Instance type: t2.micro or t3.small
  - Key pair: select or generate one

---

## 🔑 Step 2: Connect Securely via SSH Key

```bash
ssh-keygen -t rsa -b 4096 -C "you@example.com"
#Use ssh-copy-id or manually copy public key:
ssh ec2-user@<public-ip>  # AWS default user
```

## 👤 Step 3: Create a DevOps User for Platform Tasks
```bash
sudo adduser devops
sudo usermod -aG sudo devops

#Setup their SSH access:
sudo mkdir /home/devops/.ssh
sudo cp ~/.ssh/authorized_keys /home/devops/.ssh/
sudo chown -R devops:devops /home/devops/.ssh

```

## 🚫 Step 4: Harden the SSH Config
```bash
sudo nano /etc/ssh/sshd_config
# Make these changes:
PermitRootLogin no
PasswordAuthentication no
AllowUsers devops

# Then restart:
sudo systemctl restart sshd

```

## 🔐 Step 5: Install Basic Defense Tools
```bash
sudo apt update && sudo apt install ufw fail2ban -y
sudo ufw allow OpenSSH
sudo ufw enable
sudo systemctl enable fail2ban
```

## 🧪 Step 6: Write a Health Script
```bash
#This script can be reused for alerting or pre-deploy checks:
touch system-check.sh && chmod +x system-check.sh
#Content:
#!/bin/bash
echo "=== SYSTEM CHECK ==="
uptime
df -h
free -m
last -a | head -5

#run it
./system-check.sh
Later, we’ll run this via Ansible or CI runner
```

## ✅ Outcome
You’ve:
    Created a secure DevOps user
    Hardened SSH access
    Installed essential security packages
    Created your first health-check script
    Prepared an EC2 instance for upcoming CI/CD and automation flows
