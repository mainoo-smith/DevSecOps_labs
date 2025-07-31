# 📁 Week01/ChallengeLab.md – Simulating a Multi-User DevSecOps System with Secure Isolation

⸻

### 🎯 Objective

You’ll simulate a real-world scenario where:

  * Multiple users (e.g., DevOps, App, and Auditor roles) exist on a shared Linux system.
  * Each role must have limited access, isolated permissions, and logging controls.
  * You’ll apply DevSecOps principles like least privilege, role separation, and secure service execution.

⸻

### 🧪 Scenario Setup

You’ve been asked to prepare a Linux server where:

  * `devops_user` is responsible for deploying services.
  * `app_user` runs the actual backend/frontend application processes.
  * `auditor_user` can only read logs and audit reports, but nothing else.
  * Each user’s activities must be separated and logged.

⸻

### 🧱 Step 1: Create Role-Based Users and Groups

```bash
# Create groups for each role
sudo groupadd devops
sudo groupadd app
sudo groupadd auditors

# Create users and assign them
sudo useradd -m -s /bin/bash -G devops devops_user
# -m creates the users home directory if it doesn't already exist
# -s creates a shell for the user when logged in. In this case, a bash shell
# -G is the group to assign the user
sudo useradd -m -s /bin/bash -G app app_user
sudo useradd -m -s /bin/bash -G auditors auditor_user

# Set passwords (or configure SSH keys)
sudo passwd devops_user
sudo passwd app_user
sudo passwd auditor_user
```

⸻

### 🗄️ Step 2: Prepare App Directory Access Control

Create application directories and apply strict permissions.

```bash
sudo mkdir -p /opt/notestream/{frontend,backend,logs}

# Set group ownership
sudo chown -R app_user:app /opt/notestream/{frontend,backend}
sudo chown -R auditor_user:auditors /opt/notestream/logs

# Set permissions
sudo chmod -R 750 /opt/notestream/{frontend,backend}
sudo chmod -R 740 /opt/notestream/logs
```

**Explanation of permissions:**
The numbers `750` and `740` are octal representations of permission sets for different types of users:

  * **Owner (U):** The user who owns the file or directory.
  * **Group (G):** Users who are members of the file's or directory's group.
  * **Others (O):** All other users on the system who are not the owner or in the group.

Each digit in the octal number corresponds to the permissions for one of these categories (Owner, Group, Others), in that specific order.

The numerical values for permissions are:

  * `4`: Read (r)
  * `2`: Write (w)
  * `1`: Execute (x)
  * `0`: No permissions (-)

You combine these numbers to get the desired permission set:

  * Read + Write + Execute = `4 + 2 + 1 = 7`
  * Read + Execute = `4 + 1 = 5`
  * Read Only = `4`
  * No Permissions = `0`

**Resulting Permissions:**

  * `app_user` can deploy/run apps.
  * `devops_user` cannot touch the app runtime directories.
  * `auditor_user` can only read logs.

Test this by switching users:

```bash
su - auditor_user
ls /opt/notestream/backend  # should fail
ls /opt/notestream/logs     # should succeed
```

⸻

### 🔒 Step 3: Disable `sudo` Where Not Needed

Lock down `sudo` permissions so only `devops_user` has elevated rights:

```bash
# Add a user to a group
sudo usermod -G sudo devops_user 

# Remove a user from a group
sudo deluser app_user sudo 
sudo deluser auditor_user sudo 
```

**Configuring `sudoers` policy:**

  * `sudo visudo`: The recommended and safe way to edit the `sudoers` file. It performs syntax checks to prevent saving a broken configuration.
  * `-f`: This flag allows you to specify a different file to edit, rather than the default `/etc/sudoers`.
  * `/etc/sudoers.d/devsecops-policy`: A best practice for adding custom `sudo` rules so they are separate from the main `sudoers` file.

Add the following policy to grant `devops_user` limited `NOPASSWD` access:

```bash
sudo visudo -f /etc/sudoers.d/devsecops-policy
```

Add the following line to the file:

```
devops_user ALL=(ALL) NOPASSWD: /bin/systemctl, /usr/bin/docker
```

**Explanation of the `sudoers` policy:**

  * **`devops_user`**: The user this policy applies to.
  * **`ALL=`**: This specifies the host(s) that this rule applies to (`ALL` means any host).
  * **`(ALL)`**: Specifies the user(s) that `devops_user` can run commands as (`(ALL)` means any user, including root).
  * **`NOPASSWD:`**: This is a key part. It means that `devops_user` will **not** be prompted for a password when running the specified commands.
  * **`/bin/systemctl, /usr/bin/docker`**: A comma-separated list of the commands that `devops_user` can run with `sudo` and without a password.

This limits `devops_user` to only control services or containers — not unrestricted `sudo`.

⸻

### 📋 Step 4: Setup Audit Logging for All Users

Ensure command logging is enabled system-wide:

```bash
# Edit /etc/bash.bashrc and append the following line:
sudo nano /etc/bash.bashrc

# Linux Command Auditing with rsyslog

This document outlines a common security measure used to audit user activity on a Linux system. This configuration is a common practice for systems that require strict logging and compliance.

We will break down exactly what each part of this configuration does.

-----

### 1\. Auditing Shell Commands in `/etc/bash.bashrc`

The core of this command auditing is a powerful and clever way to log every command executed in a Bash shell. You will append the following line to the system-wide Bash configuration file:

```bash
export PROMPT_COMMAND='RETRN_VAL=$?;logger -p local1.notice -t bash[$$] "$(whoami) [$$]: $(history 1 | sed "s/^[ ]*[0-9]\+[ ]*//")"'

# Then configure rsyslog to write local1 logs to a secure file:
echo 'local1.* /var/log/command_audit.log' | sudo tee /etc/rsyslog.d/90-audit.conf
sudo systemctl daemon-reload
```

Now, all terminal commands will be logged per user.

**Command Explanations:**
This configuration is a security measure used to audit user activity on a Linux system. It is a common practice for systems that require strict logging and compliance.

**1. Editing `/etc/bash.bashrc`**

`export PROMPT_COMMAND='...'` is the core of the command auditing. It's a clever way to log every command executed in a Bash shell.

  * **`export PROMPT_COMMAND='...'`**: `PROMPT_COMMAND` is a special Bash variable. Its value is executed as a command *just before* the primary prompt (`$PS1`) is displayed, ensuring it runs before every new command.
  * **`logger`**: A command-line utility that sends a message to the system's `syslog` (via `rsyslog`).
  * **`-p local1.notice`**: Specifies the logging "facility" (`local1`) and "priority" (`notice`).
  * **`-t bash[$$]`**: Sets the "tag" for the log message, including the shell's Process ID (`$$`).
  * **`"$(whoami) [$$]: $(history 1 | sed "...")"`**: The log message content. It combines the username, PID, and the last command from history (`history 1`), cleaned up with `sed`.

**What the `/etc/bash.bashrc` modification achieves:**
It configures every new Bash shell to automatically log every command typed to the `rsyslog` daemon, including the user, PID, and the command itself.

**2. Configuring `rsyslog`**

`echo '...' | sudo tee ...` and `sudo systemctl restart rsyslog` are administrative commands to configure the logging service.

  * **`echo 'local1.* /var/log/command_audit.log'`**: This generates the `rsyslog` rule. `local1.*` selects all messages from the `local1` facility, and the path tells `rsyslog` where to write them.
  * **`| sudo tee /etc/rsyslog.d/90-audit.conf`**: The `tee` command writes the rule into a new configuration file. This is a best practice for separating custom rules.
  * **`sudo systemctl restart rsyslog`**: This command restarts the `rsyslog` service to apply the new configuration.

**What the `rsyslog` configuration achieves:**
It creates a specific rule to intercept all shell command logs and writes them to a dedicated, secure log file (`/var/log/command_audit.log`), separate from other system logs.

⸻

### 🧪 Bonus Hardening Task (Optional)

Set a restricted shell for `auditor_user` so they can only run `less`, `cat`, and `grep`.

```bash
sudo apt install rssh
sudo chsh -s /usr/bin/rssh auditor_user
```

⸻

### ✅ Challenge Goals Recap

| Requirement | Verified |
|---|---|
| 3 isolated users with roles | ✅ |
| App directories with restricted access | ✅ |
| Sudo restricted to devops | ✅ |
| Logs readable only by auditors | ✅ |
| Command auditing enabled | ✅ |
