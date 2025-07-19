# Guided Lab – Week 2: Linux + SSH + Server Hardening

---

## 🔧 Project Setup: First EC2 for Internal DevOps Tools

You're about to secure your **first EC2 instance** which will be used later to:

- Run Ansible playbooks
- Execute early CI/CD deployment jobs
- Possibly expose a staging frontend or API
- Log backups or cron-based scripts

This will serve as your **internal platform ops server**.
Note: Depending of the EC2 instance type, these commands may change slightly. Example, Amazon Linus 2 and Ubuntu may have different 
Comands and path names
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

#Test ssh in a new terminal
ssh -i your-key.pem devops@<public-ip>

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

===================================================================
# Guided Lab – Week 2: Secure EC2 for App Deployment

---

## ☁️ Objective

Provision and harden an EC2 instance that will host your `backend-api` microservice in staging.

---

## 🧪 Step 1: Provision EC2 on AWS

- Ubuntu 22.04 or Amazon Linux 2
- t2.micro or t3.small
- Allow ports: 22 (SSH), 3000 (API), deny all others

---

## 🔐 Step 2: Create SSH Key Pair & Access Server

```bash
ssh-keygen -t rsa -b 4096 -C "you@example.com"
ssh -i ~/.ssh/id_rsa ubuntu@<EC2_PUBLIC_IP>
```

---

## 👤 Step 3: Create `devops` User

```bash
sudo adduser devops
sudo usermod -aG sudo devops
sudo mkdir -p /home/devops/.ssh
sudo cp ~/.ssh/authorized_keys /home/devops/.ssh/
sudo chown -R devops:devops /home/devops/.ssh
```

---

## 🔐 Step 4: Harden SSH

```bash
sudo nano /etc/ssh/sshd_config
```

Update:
```
PermitRootLogin no
PasswordAuthentication no
AllowUsers devops
```

Restart SSH:
```bash
sudo systemctl restart sshd
```

---

## 🧱 Step 5: Set Up Firewall & Fail2Ban

```bash
sudo apt update && sudo apt install ufw fail2ban -y
sudo ufw allow 22/tcp
sudo ufw allow 3000/tcp
sudo ufw enable
```

---

## 🛠️ Step 6: Write Health Check Script

Create `/opt/backend-api/health-check.sh`

```bash
#!/bin/bash
echo "==== Health Check ===="
uptime
df -h
free -m
systemctl status backend-api.service
```

```bash
chmod +x /opt/backend-api/health-check.sh
```

---

## ✅ Outcome

- EC2 instance secured for staging use
- `devops` user created for GitHub Actions or Ansible access
- API service monitored via health script
