📁 Week01/GuidedLab.md – Hardening a Linux DevSecOps Environment (Step-by-Step)

⸻

🛠️ Objective

Set up and harden a Linux virtual machine (VM) or EC2 instance that will serve as the base for your secure DevSecOps application lifecycle. This includes:
	•	Creating a secure user
	•	Locking down SSH access
	•	Hardening file permissions
	•	Auditing running processes
	•	Preparing for future CI/CD and service deployment

⸻

🧰 Prerequisites
	•	A local Linux VM (e.g., via VirtualBox/Vagrant) or an EC2 instance running Ubuntu 22.04+
	•	Your terminal with SSH or console access
	•	Root or sudo privileges

⸻

1. 🏗️ Create a Dedicated DevSecOps User

🔒 We’ll avoid using root for any DevOps activity.
Instead, we create devsecops as a non-root user with least privilege.

sudo adduser devsecops

Follow the prompts. Choose a strong password and secure shell.

# Add user to sudo (but we will restrict later)
sudo usermod -aG sudo devsecops

# Confirm
id devsecops


⸻

2. 📂 Prepare Directory Structure for App Deployment

We’ll begin preparing folders for our monorepo/microservices.

sudo mkdir -p /opt/notestream/{frontend,backend,automation,infra}
sudo chown -R devsecops:devsecops /opt/notestream
sudo chmod -R 750 /opt/notestream

	•	750 means: Owner can read/write/execute, group can read/execute, others have no access.

⸻

3. 🔐 Lock Down SSH Access

SSH is a primary attack vector. Harden it immediately.

✅ 3.1 Disable root SSH login

Edit /etc/ssh/sshd_config:

sudo nano /etc/ssh/sshd_config

Update or add the following lines:

PermitRootLogin no
PasswordAuthentication no
AllowUsers devsecops

Then reload the SSH daemon:

sudo systemctl reload sshd

✅ 3.2 Add Public Key for devsecops

Log in as devsecops and create .ssh directory:

su - devsecops
mkdir -p ~/.ssh
chmod 700 ~/.ssh

Paste your public key into ~/.ssh/authorized_keys:

nano ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys


⸻

4. 🧼 Remove Unnecessary Packages and Services

# List active services
sudo systemctl list-units --type=service --state=running

# Disable unneeded services (example)
sudo systemctl disable cups.service
sudo systemctl disable bluetooth.service

# Autoremove junk
sudo apt autoremove -y


⸻

5. 🔎 Inspect Running Processes

ps aux --sort=-%mem | head -n 15

Understand which processes are consuming resources. You’ll use this later to detect anomalies (Week 14).

⸻

6. 🔍 Install Audit Tools

# System auditing
sudo apt update
sudo apt install auditd lynis -y

# Run baseline audit
sudo lynis audit system


⸻

✅ Verification Checklist

Task	Verified
devsecops user created with sudo	✅
/opt/notestream structure created and secured	✅
Root login disabled via SSH	✅
SSH key-based login configured	✅
Unnecessary services disabled	✅
Basic audit tools installed	✅


⸻

🧪 Run: First Security Scan

sudo lynis audit system > ~/lynis_report.txt
less ~/lynis_report.txt

Save this report. You’ll compare it against future hardened states in Week 8 and Week 14.

⸻
