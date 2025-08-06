# 🛠️ Hardening a Linux DevSecOps Environment (Step-by-Step)

## Objective
Set up and harden a Linux virtual machine (VM) or EC2 instance that will serve as the base for your secure DevSecOps application lifecycle. This includes:

- Creating a secure user
- Locking down SSH access
- Hardening file permissions
- Auditing running processes
- Preparing for future CI/CD and service deployment

---

## 🧰 Prerequisites
- A local Linux VM (e.g., via VirtualBox/Vagrant) or an EC2 instance running Ubuntu 22.04+
- Your terminal with SSH or console access
- Root or `sudo` privileges

---

### 1. 🏗️ Create a Dedicated DevSecOps User
🔒 We'll avoid using `root` for any DevOps activity. Instead, we create `devsecops` as a non-root user with the least privilege.

```bash
# Create the user
sudo adduser devsecops

# Follow the prompts. Choose a strong password.

# Add user to the sudo group (we will restrict this later)
sudo usermod -aG sudo devsecops

# Confirm the user and group membership
id devsecops

2. 📂 Prepare Directory Structure for App Deployment
We’ll begin preparing folders for our monorepo/microservices.
# Create the directory structure
sudo mkdir -p /opt/notestream/{frontend,backend,automation,infra}

# Set ownership to the new user
sudo chown -R devsecops:devsecops /opt/notestream

# Set secure permissions
sudo chmod -R 750 /opt/notestream

> Note on 750 permissions: Owner can read/write/execute, group can read/execute, and others have no access at all.
> 

3. 🔐 Lock Down SSH Access
SSH is a primary attack vector. Harden it immediately.
✅ 3.1 Disable Root Login and Password Authentication
Edit the SSH configuration file:
sudo nano /etc/ssh/sshd_config

Update or add the following lines to disable direct root login and force key-based authentication:
PermitRootLogin no
PasswordAuthentication no
AllowUsers devsecops

Then, reload the SSH daemon to apply the changes:
sudo systemctl reload sshd

✅ 3.2 Add Your Public Key for the devsecops User
Log in as the devsecops user and create the .ssh directory:
su - devsecops
mkdir -p ~/.ssh
chmod 700 ~/.ssh

Paste your public SSH key into the authorized_keys file and set its permissions:
# Use nano or your preferred editor to paste your key
nano ~/.ssh/authorized_keys

# Secure the file
chmod 600 ~/.ssh/authorized_keys

4. 🧼 Remove Unnecessary Packages and Services
A minimal system has a smaller attack surface.
# List all active services
sudo systemctl list-units --type=service --state=running

# Disable unneeded services (examples below)
sudo systemctl disable cups.service
sudo systemctl disable bluetooth.service

# Remove orphaned and unnecessary packages
sudo apt autoremove -y

5. 🔎 Inspect Running Processes

Understand what's running on your system. This is a baseline for future anomaly detection.
# List processes sorted by memory usage
ps aux --sort=-%mem | head -n 15

6. 🔍 Install Audit Tools
Install auditd for system call auditing and lynis for security scanning.
sudo apt update
sudo apt install auditd lynis -y

✅ Verification Checklist

| Task | Verified |
|---|---|
| devsecops user created with sudo | ✅ |
| /opt/notestream structure secured | ✅ |
| Root login disabled via SSH | ✅ |
| SSH key-based login configured | ✅ |
| Unnecessary services disabled | ✅ |
| Basic audit tools installed | ✅ |

🧪 Run: First Security Scan

Run a baseline audit with lynis and save the report. You'll compare this against future hardened states.
sudo lynis audit system > ~/lynis_report.txt
less ~/lynis_report.txt

🔜 Coming Next:
 * ChallengeLab.md: Multi-user simulation and privilege isolation
 * Security.md: Misconfigurations, SUID/SGID, and hardening tools
 * Reflection.md: Theory deep dive + preparing for network hardening
<!-- end list -->