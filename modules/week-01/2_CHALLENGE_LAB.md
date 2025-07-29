📁 Week01/ChallengeLab.md – Simulating a Multi-User DevSecOps System with Secure Isolation

⸻

🎯 Objective

You’ll simulate a real-world scenario where:
	•	Multiple users (e.g., DevOps, App, and Auditor roles) exist on a shared Linux system.
	•	Each role must have limited access, isolated permissions, and logging controls.
	•	You’ll apply DevSecOps principles like least privilege, role separation, and secure service execution.

⸻

🧪 Scenario Setup

You’ve been asked to prepare a Linux server where:
	•	devops_user is responsible for deploying services.
	•	app_user runs the actual backend/frontend application processes.
	•	auditor_user can only read logs and audit reports, but nothing else.
	•	Each user’s activities must be separated and logged.

⸻

🧱 Step 1: Create Role-Based Users and Groups

```bash
# Create groups for each role
sudo groupadd devops
sudo groupadd app
sudo groupadd auditors

# Create users and assign them
sudo useradd -m -s /bin/bash -G devops devops_user
# -m creates the users home directory if not already exists
# -s creates a shell for the user when logged in. In this case bash shell
# -G is the group to assing the user
sudo useradd -m -s /bin/bash -G app app_user
sudo useradd -m -s /bin/bash -G auditors auditor_user

# Set passwords (or configure SSH keys)
sudo passwd devops_user
sudo passwd app_user
sudo passwd auditor_user
```

⸻

🗄️ Step 2: Prepare App Directory Access Control

Create application directories and apply strict permissions.
```bash
sudo mkdir -p /opt/notestream/{frontend,backend,logs}

# Set group ownership
sudo chown -R app_user:app /opt/notestream/{frontend,backend}
sudo chown -R auditor_user:auditors /opt/notestream/logs

# Set permissions
sudo chmod -R 750 /opt/notestream/{frontend,backend}
sudo chmod -R 740 /opt/notestream/logs

# The numbers 750 and 740 are octal representations of permission sets for different types of users:

#Owner (U): The user who owns the file or directory.

#Group (G): Users who are members of the file's or directory's group.

#Others (O): All other users on the system who are not the owner or in the group.

# Each digit in the octal number corresponds to the permissions for one of these categories (Owner, Group, Others), in that specific order.

# The numerical values for permissions are:

# 4: Read (r)

# 2: Write (w)

# 1: Execute (x)

# 0: No permissions (-)

# You combine these numbers to get the desired permission set:

# Read + Write + Execute = 4 + 2 + 1 = 7

# Read + Write = 4 + 2 = 6

# Read + Execute = 4 + 1 = 5

# Read Only = 4

# Write Only = 2

# Execute Only = 1

# No Permissions = 0

```
Now:
	•	app_user can deploy/run apps
	•	devops_user cannot touch app runtime
	•	auditor_user can only read logs

Test this by switching users:
```bash
su - auditor_user
ls /opt/notestream/backend         # should fail
ls /opt/notestream/logs            # should succeed
```

⸻

🔒 Step 3: Disable sudo Where Not Needed

Lock down sudo permissions so only devops_user has elevated rights:

```bash
sudo usermod -G sudo devops_user
sudo deluser app_user sudo
sudo deluser auditor_user sudo

Edit /etc/sudoers.d/devsecops-policy:

sudo visudo -f /etc/sudoers.d/devsecops-policy

Add:

devops_user ALL=(ALL) NOPASSWD: /bin/systemctl, /usr/bin/docker
```
This limits devops_user to only control services or containers — not unrestricted sudo.

⸻

📋 Step 4: Setup Audit Logging for All Users

Ensure command logging is enabled system-wide:

Edit /etc/bash.bashrc and append:

export PROMPT_COMMAND='RETRN_VAL=$?;logger -p local1.notice -t bash[$$] "$(whoami) [$$]: $(history 1 | sed "s/^[ ]*[0-9]\+[ ]*//")"'

Then configure rsyslog to write local1 logs to a secure file:

echo 'local1.*    /var/log/command_audit.log' | sudo tee /etc/rsyslog.d/90-audit.conf
sudo systemctl restart rsyslog

Now, all terminal commands will be logged per user.

⸻

🧪 Bonus Hardening Task (Optional)

Set a restricted shell for auditor_user so they can only run less, cat, and grep.

sudo apt install rssh
sudo chsh -s /usr/bin/rssh auditor_user


⸻

✅ Challenge Goals Recap

Requirement	Verified
3 isolated users with roles	✅
App directories with restricted access	✅
Sudo restricted to devops	✅
Logs readable only by auditors	✅
Command auditing enabled	✅


