# 📁 Week01/Reflection.md – Review, Key Learnings & Real-World DevSecOps Implications

⸻

### 🔁 What You Did This Week

* ✅ Set up a secure, hardened Linux instance that will serve as the DevSecOps base platform
* ✅ Created and isolated users by role: DevOps, App Runtime, Auditor
* ✅ Locked down file access, SSH access, sudo rights, and logging
* ✅ Simulated a real-world shared system with permission-based access controls
* ✅ Installed OS-level auditing and security monitoring tools
* ✅ Learned the risks of OS-level misconfigurations and privilege escalation

⸻

### 🧠 Key Concepts to Remember

| Concept | Why It Matters |
|---|---|
| Principle of Least Privilege | Minimizes the blast radius of compromise |
| SSH Hardening | Prevents one of the most common entry points |
| Role-Based Access Controls (RBAC) | Applies even before Kubernetes or IAM — starts at the OS |
| Audit Logging | Critical for post-breach investigation and compliance |
| SUID/SGID Awareness | Attackers escalate through insecure binaries and scripts |

⸻

### ❓ Self-Check Questions
1.  Why is it dangerous to allow password-based SSH login on a Linux server?
2.  What’s the difference between a user being in the `sudo` group and having limited `sudo` commands in `/etc/sudoers.d/`?
3.  How do SetUID and SetGID work? What can go wrong if misused?
4.  Why would an attacker want to find world-writable files or directories?
5.  How does audit logging change the DevSecOps feedback loop?

⸻

### 📚 Optional Exploration
* Research AppArmor or SELinux and compare their roles in Mandatory Access Control (MAC).
* Explore how to use `packer` or `cloud-init` to automate the hardening process.
* Try installing a `fail2ban` service to automatically block brute-force SSH attempts.
* Review your favorite DevSecOps tool’s system requirements — how do they assume the OS is secured?

⸻

### 🧩 How This Week Sets the Foundation

Everything from here forward — building containers, running CI/CD pipelines, deploying microservices — depends on this hardened system not becoming your weakest link.
