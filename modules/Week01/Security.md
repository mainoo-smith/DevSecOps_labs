🔐 Linux OS Hardening, Misconfigurations, and Key DevSecOps Controls
> In many modern systems, the first successful attack happens at the OS level, not through the application or network. Misconfigured users, open permissions, lingering SUID binaries, or overly permissive sudo rights can be exploited by attackers to escalate privileges or exfiltrate data. DevSecOps aims to shift security left by defining and enforcing secure defaults at every system layer—and the OS is layer zero.
> 
🛠️ Common OS Misconfigurations in the Real World
| Risk | Example | Impact |
|---|---|---|
| Weak or shared root access | Default passwords or shared keys | Full system compromise |
| Open SSH or FTP ports | sshd_config allows root, password auth enabled | Brute-force exposure |
| World-writable directories | /opt/app has 777 permissions | Anyone can drop malicious scripts |
| Over-permissive sudo | sudo ALL=(ALL) ALL | No audit trail, full access |
| Insecure $PATH or aliases | Modified .bashrc | Command hijacking |
| Unnecessary SUID binaries | /usr/bin/nmap, /bin/mount | Local privilege escalation |
🔍 Special Permissions: SUID, SGID, & Sticky Bit
✅ SetUID (s on user bit)
Allows a file to be executed with the permissions of its owner (often root).
 * Risk: Dangerous when used carelessly (e.g., /usr/bin/passwd is okay, but /usr/bin/vim is not).
 * How to find: find / -perm -4000 -type f 2>/dev/null
✅ SetGID (s on group bit)
Forces files created in a directory to inherit the group ID.
 * Use Case: Used safely in group collaboration scenarios.
 * How to find: find / -perm -2000 -type f 2>/dev/null
✅ Sticky Bit (t on other bit)
Used mostly on shared directories (like /tmp) to restrict file deletions to the file's owner.
 * How to check: ls -ld /tmp (should show drwxrwxrwt)
📦 Recommended OS Hardening Steps
| Task | Why It Matters |
|---|---|
| Disable password auth in SSH | Forces key-based auth, reducing brute-force risk |
| Enforce umask 027 | Prevents files from being world-readable |
| Remove unneeded packages | Minimizes the attack surface |
| Set up auditd | Tracks all command executions and file access |
| Install lynis | Provides regular system security auditing |
| Restrict sudo commands | Minimizes lateral movement opportunities |
| Limit open ports with ufw | Prevents unnecessary service exposure |
| Use AppArmor or SELinux | Enforces Mandatory Access Control (MAC) |
🛠️ Tools You Should Know
| Tool | Usage |
|---|---|
| auditd | Kernel-level auditing for file and command activity |
| lynis | System security scanner for hardening assessment |
| chkrootkit / rkhunter | Rootkit detection |
| ufw / iptables | Host-level firewall |
| logrotate | Ensures logs don't overflow disks |
| psacct or acct | Per-user command tracking |
🔄 DevSecOps Integration Patterns
| Practice | Application |
|---|---|
| Use hardened base OS AMIs | Prevents unknown defaults in EC2/K8s nodes |
| Include auditd config in AMI | CI/CD-enforced runtime logging |
| Rotate SSH keys with automation | Can be done weekly or on incident |
| Validate permissions in CI/CD | Use checks like ls -l as a pre-deployment gate |
| Include lynis in image scanning | Fails the pipeline if insecure defaults exist |
🚩 Red Team Insight
Red teamers often look for these common vulnerabilities:
 * Loose SUID binaries
 * Writable scripts in /etc/init.d/
 * Backup files with sensitive credentials (.bak, ~)
 * Crontabs that call writable scripts
 * Unrestricted /etc/sudoers entries
Your job as a DevSecOps engineer is to hunt for and fix these security flaws before an attacker does.
