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
sudo usermod -G sudo devops_user #adds <user> to sudo group
sudo deluser app_user sudo # removes a <user> from <group>
sudo deluser auditor_user sudo # removes a <user> from <group>

# sudo visudo: visudo is the recommended and safe way to edit the sudoers file. It opens the file in a text editor (like vi or nano), checks the syntax for errors when you save, and prevents you from saving a broken configuration that could lock you out of sudo.

# -f: This flag allows you to specify a different file to edit, rather than the default /etc/sudoers.

# /etc/sudoers.d/devsecops-policy: This is the path to the new file you are creating or editing. It's a best practice to put custom sudo rules in the /etc/sudoers.d/ directory so they are separate from the main /etc/sudoers file and easier to manage.

# The sudoers File Content
# devops_user ALL=(ALL) NOPASSWD: /bin/systemctl, /usr/bin/docker

# This line is a specific sudo policy for devops_user. Let's break down its syntax:

# devops_user: The user account this policy applies to.

# ALL=: This specifies the host(s) that this rule applies to. ALL means any host.

# (ALL): This specifies the user(s) that devops_user can run commands as. (ALL) means devops_user can use sudo to run commands as any user (including root).

# NOPASSWD:: This is a key part. It means that devops_user will not be prompted for a password when running the commands that follow this keyword.

# /bin/systemctl, /usr/bin/docker: This is a comma-separated list of the commands that devops_user can run with sudo and without a password.

# /bin/systemctl: A common command used for managing system services.

# /usr/bin/docker: The main Docker command.

sudo visudo -f /etc/sudoers.d/devsecops-policy
sudo visudo -f /etc/sudoers.d/devsecops-policy
Add:

devops_user ALL=(ALL) NOPASSWD: /bin/systemctl, /usr/bin/docker
```
This limits devops_user to only control services or containers — not unrestricted sudo.

⸻

📋 Step 4: Setup Audit Logging for All Users

Ensure command logging is enabled system-wide:

# Linux Command Auditing with rsyslog

This document outlines a common security measure used to audit user activity on a Linux system. This configuration is a common practice for systems that require strict logging and compliance.

We will break down exactly what each part of this configuration does.

-----

### 1\. Auditing Shell Commands in `/etc/bash.bashrc`

The core of this command auditing is a powerful and clever way to log every command executed in a Bash shell. You will append the following line to the system-wide Bash configuration file:

```bash
export PROMPT_COMMAND='RETRN_VAL=$?;logger -p local1.notice -t bash[$$] "$(whoami) [$$]: $(history 1 | sed "s/^[ ]*[0-9]\+[ ]*//")"'
```

  * **`export PROMPT_COMMAND='...'`**: `PROMPT_COMMAND` is a special Bash shell variable. When set, its value is executed as a command *just before* the primary prompt (`$PS1`) is displayed. This ensures the command inside the quotes runs every single time the shell is ready to accept a new command.
  * **`RETRN_VAL=$?`**: The `$?` variable holds the exit status of the most recently executed foreground command. A value of `0` typically indicates success, while any other value indicates an error.
  * **`logger`**: This is a command-line utility that sends a message to the system's `syslog` (via `rsyslog` on most modern systems). This is how the shell command gets into the central logging system.
  * **`-p local1.notice`**: This flag specifies the "facility" and "priority" of the log message.
      * **`local1`**: This is a "local" facility, often used for custom application logging.
      * **`notice`**: This is a priority level, indicating that the message is of normal but significant status.
  * **`-t bash[$$]`**: This sets the "tag" for the log message.
      * **`bash`**: The name of the program sending the log message.
      * **`[$$]`**: The `$$` variable holds the Process ID (PID) of the current shell. This is a very useful piece of information for auditing.
  * **`"$(whoami) [$$]: ... "`**: This is the actual log message content.
      * **`$(whoami) [$$]:`**: This part identifies the user who ran the command and their shell's PID.
      * **`$(history 1 | sed "s/^[ ]*[0-9]\+[ ]*//")`**: This is the clever part that gets the actual command.
          * **`history 1`**: This command outputs the last command from the user's history.
          * **`|`**: The pipe sends the output of `history 1` to the `sed` command.
          * **`sed "s/^[ ]*[0-9]\+[ ]*//"`**: This `sed` command uses a regular expression to remove the history number and any leading spaces, leaving just the raw command string.

**What this modification achieves:**
It configures every new Bash shell for every user to automatically log every single command they type to the `rsyslog` daemon. The log message includes the username, the shell's PID, and the command itself.

-----

### 2\. Configuring `rsyslog` to Store the Logs

This part takes the log messages being generated by `bash.bashrc` and stores them in a dedicated, secure file. You will use the following commands on the command line:

```bash
echo 'local1.* /var/log/command_audit.log' | sudo tee /etc/rsyslog.d/90-audit.conf
sudo systemctl restart rsyslog
```

  * **`echo 'local1.* /var/log/command_audit.log'`**: This command generates the configuration line for `rsyslog`.
      * **`local1.*`**: This is the "selector." It tells `rsyslog` to look for any message with the `local1` facility, regardless of its priority (`*`).
      * **`/var/log/command_audit.log`**: This is the "action." It tells `rsyslog` to write any matching message to this specific file.
  * **`| sudo tee /etc/rsyslog.d/90-audit.conf`**:
      * **`|`**: The pipe sends the output of `echo` to the `tee` command.
      * **`sudo tee`**: The `tee` command reads from standard input and writes to a file with `sudo` privileges. This is a common way to write to a root-owned file from a non-root command.
      * **`/etc/rsyslog.d/90-audit.conf`**: This is the destination file for the `rsyslog` configuration. Placing custom configurations in the `/etc/rsyslog.d/` directory is a best practice.
  * **`sudo systemctl restart rsyslog`**: This command restarts the `rsyslog` service. The `rsyslog` daemon reads its configuration files on startup, so this step is necessary to apply the new rule.

**What this configuration achieves:**
It creates a specific rule to intercept all shell command logs (those tagged as `local1`) and writes them to a dedicated log file (`/var/log/command_audit.log`), separate from other system logs. This makes auditing easier and more secure.

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


