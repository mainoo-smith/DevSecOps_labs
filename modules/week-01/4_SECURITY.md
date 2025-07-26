📁 Week01/Security.md – Linux OS Hardening, Misconfigurations, and Key DevSecOps Controls

⸻

🔐 Why OS-Level Security Matters in DevSecOps

In many modern systems, the first successful attack doesn’t happen through the app or the network — it happens at the OS level. Misconfigured users, open permissions, lingering SUID binaries, or overly permissive sudo rights can allow attackers to escalate privileges or exfiltrate data.

In DevSecOps, we shift security left by defining and enforcing secure defaults at every system layer — and the OS is layer zero.

⸻

🛠️ Common OS Misconfigurations in the Real World

Risk	Example	Impact
Weak or shared root access	Default passwords or shared keys	Full system compromise
Open SSH or FTP ports	sshd_config allows root, password auth enabled	Brute-force exposure
World-writable directories	/opt/app has 777	Anyone can drop malicious scripts
Over-permissive sudo	sudo ALL=(ALL) ALL	No audit trail, full access
Insecure $PATH or shell aliases	Modified .bashrc	Command hijacking
Unnecessary SUID binaries	/usr/bin/nmap, /bin/mount	Local privilege escalation


⸻

🔍 Special Permissions: SUID, SGID, Sticky Bit

✅ SetUID (s on user bit)
	•	Allows execution of a file with the permissions of its owner (often root).
	•	Dangerous when used carelessly (e.g., /usr/bin/passwd is OK, /usr/bin/vim is NOT)

find / -perm -4000 -type f 2>/dev/null


⸻

✅ SetGID (s on group bit)
	•	Forces files created in a directory to inherit the group ID
	•	Used safely in group collaboration scenarios

find / -perm -2000 -type f 2>/dev/null


⸻

✅ Sticky Bit (t on other bit)
	•	Used mostly on shared directories (like /tmp) to restrict file deletions to the owner

ls -ld /tmp        # should show drwxrwxrwt


⸻

📦 Recommended OS Hardening Steps

Task	Why It Matters
Disable password auth in SSH	Forces key-based auth, reduces brute-force risk
Enforce umask 027	Prevents files from being world-readable
Remove unneeded packages	Minimizes attack surface
Set up auditd	Tracks all command executions and file access
Install lynis	Regular system security auditing
Restrict sudo commands	Minimizes lateral movement opportunities
Limit open ports with ufw or firewalld	Prevents unnecessary service exposure
Use AppArmor or SELinux profiles	Mandatory Access Control enforcement


⸻

🛠️ Tools You Should Know

Tool	Usage
auditd	Kernel-level auditing for file and command activity
lynis	System security scanner for hardening assessment
chkrootkit / rkhunter	Rootkit detection
ufw / iptables	Host-level firewall
logrotate	Ensures logs don’t overflow disks
psacct or acct	Per-user command tracking


⸻

🔄 DevSecOps Integration Patterns

Practice	Application
Use hardened base OS AMIs	Prevent unknown defaults in EC2/K8s nodes
Include auditd config in AMI/packer templates	CI/CD-enforced runtime logging
Rotate SSH keys with automation	Weekly or on incident
Validate permissions in CI/CD (e.g., ls -l)	Pre-deployment security gate
Include lynis in image scanning stages	Fails pipeline if insecure defaults exist


⸻

🚩 Red Team Insight

Red teamers often look for:
	•	Loose SUID binaries
	•	Writable scripts in /etc/init.d/
	•	Backup files with sensitive creds (.bak, ~)
	•	Crontabs that call writable scripts
	•	Unrestricted /etc/sudoers entries

Your job as a DevSecOps engineer is to hunt these first before attackers do.
