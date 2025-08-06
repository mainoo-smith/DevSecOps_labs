📁 Week5/Security.md

Title: Scripting Security: Threat Surfaces, Mitigations, and DevSecOps Practices

⸻

🧠 Why This Matters

Scripting is powerful — but without care, it becomes one of the top sources of security breaches, especially in DevOps pipelines and automation tasks.

A misplaced $VAR, insecure file permissions, or a leaked log can expose secrets, credentials, or production data.

This section analyzes common attack surfaces in Bash and Python scripting, and how to prevent them in real-world DevSecOps pipelines.

⸻

⚠️ Common Scripting Threats

Threat	Description	Exploit Example
🧨 Shell Injection	Unsanitized inputs used in eval, exec, backticks	$(rm -rf /) injected via env var
🧪 Hardcoded Secrets	Static API keys, tokens, or DB credentials in scripts	Secrets committed to Git repo
🔓 Insecure File Handling	World-readable .env, log, or SBOM files	Leaked secrets or CVEs in logs
🦥 Improper Error Handling	Scripts silently failing or ignoring errors	Missed backup, broken deploy
🔁 Privilege Abuse	Scripts that assume or run as root	Escalation vector in compromised CI/CD
🗃️ Environment Leakage	Dumping entire env into logs	Secrets exposed in log collectors


⸻

🛡️ DevSecOps Security Practices

Here’s how your Week 5 scripts mitigate these risks:

⸻

✅ 1. Use set -euo pipefail in Bash

set -euo pipefail

Prevents:
	•	Silent errors (-e)
	•	Use of unset vars (-u)
	•	Ignored broken pipes (-o pipefail)

📌 Why: Hard to troubleshoot broken automation when failures are masked.

⸻

✅ 2. Avoid eval, backticks, or shell expansion from user inputs

Instead of:

eval "aws ${user_input}"

Use:

aws ecs describe-services --cluster "$CLUSTER_NAME"

📌 Why: Prevents arbitrary command execution via user input or CI injection.

⸻

✅ 3. Externalize secrets – never hardcode

✅ Load from:
	•	.env files (with .gitignore)
	•	AWS SSM Parameter Store (via aws ssm get-parameter)
	•	GitHub/GitLab Secrets

📌 Why: Hardcoded secrets lead to breaches, Git leaks, and audit failures.

⸻

✅ 4. Sanitize and validate all inputs

In Bash:

if [[ -z "$CLUSTER_NAME" ]]; then echo "Missing cluster"; exit 1; fi

In Python:

if not input_file.endswith(".json"):
    raise ValueError("Invalid file format")

📌 Why: Prevent malformed or malicious input from causing damage.

⸻

✅ 5. Secure file permissions
	•	SBOMs should not be world-readable
	•	Log archives must not include secrets
	•	.env should have chmod 600

📌 Why: Files created in CI/CD are often globally readable if not explicitly locked down.

⸻

✅ 6. Use IAM-scoped roles
	•	Grant ssm:GetParameter, kms:Decrypt, s3:PutObject only where needed
	•	Use temporary credentials via CI roles or federated access

📌 Why: Scripts should never use long-lived credentials or over-privileged IAM roles.

⸻

✅ 7. Log responsibly

Instead of:

echo "Secret is $DB_PASSWORD"

Do:

echo "Fetched DB_PASSWORD from SSM"

📌 Why: Secrets in logs are a top CVE exploitation path (especially in CloudWatch, Papertrail, etc.)

⸻

🔐 Extra Defenses You Can Add

Technique	Description
sh -n or shellcheck	Validate Bash scripts statically
Python bandit	Linter for insecure Python practices
Audit logging	Log script invocations (not contents)
Encrypted S3 buckets	Secure backups + logs in transit and at rest
KMS encryption	Encrypt .gz, .json, .html files with customer-managed keys


⸻

🚧 Real-World Security Failure Scenarios

Scenario	Root Cause	Prevention
CI job accidentally commits .env with secrets	.env wasn’t gitignored	Add .env to .gitignore and use vault
Trivy report with CVEs gets exposed via public S3 bucket	No S3 bucket policy or permissions	Apply strict S3 bucket policy
Python log script fails silently during pipeline	No error handling in subprocess	Use try/except with logging
Log archive includes DEBUG output with token	Over-verbose logging	Sanitize logs and scrub sensitive info
