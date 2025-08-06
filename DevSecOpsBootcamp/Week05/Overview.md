📁 Week5/Overview.md

Title: ⚙️ Scripting & Automation with Bash & Python
Focus: Automating DevSecOps workflows across environments securely and efficiently

⸻

🧠 Conceptual Overview

🔧 Why Scripting Matters in DevSecOps

Scripting is the glue between infrastructure, CI/CD, security scanning, monitoring, and deployment. Whether you’re:
	•	Automating a cloud backup
	•	Generating a signed SBOM
	•	Or sending audit logs to a compliance bucket

…chances are, a script is behind it.

Scripting done right enables:
	•	Repeatability & reliability
	•	Secure execution of privileged tasks
	•	Team-wide operational consistency
	•	Lightweight automation without heavyweight pipelines

⸻

🐚 Bash vs 🐍 Python

Feature	Bash	Python
Great for	Shell tasks, chaining commands, log rotation	Complex logic, API integrations, report generation
Strengths	Native to UNIX, cron-friendly	Libraries (e.g. boto3, requests), readable
Weaknesses	Harder to test/scale	Slower for one-liners
DevSecOps Use	Glue scripts, log rotation, backups	Report generators, scanners, validations

We’ll use both in this module — in the right places and with security in mind.

⸻

🔐 Security Risks in Scripting

Common mistakes we’ll avoid:
	•	Hardcoding secrets
	•	Unsafe input parsing ($1, eval, os.system())
	•	Over-permissioned scripts (running as root)
	•	Logging sensitive info
	•	Shell injection ($(user_input))

You’ll learn to:
	•	Validate inputs
	•	Sanitize environment variables
	•	Use AWS SSM + .env for secure secrets loading
	•	Log responsibly

⸻

🧩 Evolving the App

This week we evolve the app with scripting:

Task	Tool	Scripted With
ECS service health check	AWS CLI	Bash
Trivy vulnerability report → SBOM	Trivy JSON → HTML	Python
Secrets fetch from SSM Parameter Store	AWS CLI + dotenv	Bash
App deployment pre-check (ports, version)	Axios + shell test	Python
Audit log archive to S3	AWS SDK	Python

Each of these will be implemented as:
	•	Standalone script (.sh or .py)
	•	CI/CD job template (GitHub/GitLab)
	•	Secure file (.env, IAM role, encrypted store)

⸻

🎯 DevSecOps Learning Objectives

By the end of this module, you’ll be able to:

✅ Write production-grade, reusable Bash and Python scripts
✅ Integrate those scripts into pipelines and automated workflows
✅ Use secure scripting practices (env vars, no hardcoding, input validation)
✅ Handle secrets and sensitive data responsibly
✅ Leverage automation in CI/CD, monitoring, backups, and reporting
✅ Explain scripting’s role in incident response, compliance, and DevOps scaling

⸻

🛠️ Tools & Services Covered

Tool	Use
Bash, cron, set -euo pipefail	Safety-first Bash scripting
Python 3.11+, argparse, os, json, boto3	CLI tools, AWS automation
AWS CLI + SSM + IAM	Secure secret fetch and resource automation
Trivy	SBOM generation for automation
GitHub Actions + GitLab CI	Script integration into CI/CD
