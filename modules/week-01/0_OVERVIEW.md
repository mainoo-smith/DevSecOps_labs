📁 Week01/Overview.md – Linux & OS Fundamentals for DevSecOps

⸻

🧠 Module Theory: Why Linux and OS Concepts Matter in DevSecOps

In DevSecOps, security starts from the ground up. The operating system is the foundation upon which your CI/CD tools, containers, microservices, and cloud infrastructure all run.

While DevOps often emphasizes automation and pipelines, DevSecOps demands awareness of what’s happening under the hood — how permissions work, how processes behave, what file ownership means, and how attackers might exploit insecure configurations.

You’ll also encounter real-world cases where container escapes, privilege escalations, or insecure SSH setups were entry points for attackers. Knowing how to secure the OS and understand its audit signals is non-negotiable.

⸻

🎯 Objectives

By the end of this module, you will:
	•	Understand core Linux OS concepts that impact security:
	•	Users, groups, permissions, processes, file hierarchy
	•	SUID/SGID/sticky bits, chroot, sudo, SSH hardening
	•	Set up a secure Linux-based environment for your evolving DevSecOps app
	•	Build the first layer of your DevSecOps-friendly development VM
	•	Apply OS-level hardening techniques used in production environments

⸻

📦 Application Tie-In: Evolving the Project

This week, we start the project from the bottom:
	•	Provision the initial development and deployment VM
	•	Create an isolated Linux user that will run the application and CI/CD agents
	•	Prepare the directory structure where the “Notes App” microservices will live
	•	Set file and execution permissions based on least privilege principles

As the app evolves, this VM/instance will:
	•	Host Git runners and deploy services (early)
	•	Later be containerized and deployed to ECS/K8s (week 6+)
	•	Serve as a runtime hardening sandbox (week 12+)

⸻

🔧 Tools & Technologies
	•	Linux (Ubuntu/Debian-based VM or EC2)
	•	SSH, Bash
	•	chmod, chown, sudo, groups, ps, top
	•	Optional: ufw, fail2ban, auditd, lynis

⸻

🛡️ DevSecOps Concepts Introduced

Concept	Relevance
Principle of Least Privilege	Preventing unauthorized access to files and commands
User and Group Segmentation	Isolating services and users
Secure Defaults	File system and SSH security
Auditing and Logging	Tracking what happened and when
OS Hardening	Disabling unnecessary features or access paths


⸻

📁 Deliverables
	•	A hardened development Linux VM or EC2 instance
	•	A secure user environment for DevSecOps tooling
	•	A locked-down SSH access mechanism
	•	File permission settings tailored to security best practices
	•	A README.md summarizing system security controls configured

⸻

🔜 Coming up next:
	•	Week01/GuidedLab.md: We’ll walk through setting up the hardened VM and user
	•	Week01/ChallengeLab.md: You’ll simulate a multi-user system and secure it
	•	Week01/Security.md: Discuss common misconfigurations and tools like Lynis
	•	Week01/Reflection.md: Deep questions + preparation for Week 2 (networking)
