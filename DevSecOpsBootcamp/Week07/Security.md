📁 Week7/Security.md

Title: CI/CD Pipeline Security – AWS CodePipeline & CodeBuild Hardening

⸻

🔐 Why Pipeline Security Matters in DevSecOps

CI/CD pipelines are high-value targets. If compromised, they can:
	•	Deploy malware directly to production
	•	Leak credentials or API keys to public logs
	•	Skip critical vulnerability checks
	•	Allow lateral movement across services

This week, we focused on building secure, least-privilege, auditable pipelines that minimize these risks.

⸻

🔍 What We Secured

Area	Security Mechanism
Secrets	Pulled at runtime from Secrets Manager or SSM, never stored in repo or logs
IAM Roles	Scoped per service and per stage — CodeBuild and CodePipeline have isolated permissions
Scan Enforcement	Pipeline blocks deployment if critical CVEs are detected via Trivy
SBOM & Artifacts	Stored in S3 per-service with versioning and path restrictions
Deployment	Controlled by post-scan approval stage, and run via secure scripts only
Logging	Enabled CloudWatch logs for build/test/scan/deploy stages
Notification (optional)	Alerting on pipeline failures via SNS or Slack for visibility


⸻

💣 Real-World CI/CD Threats Prevented

Threat	Mitigation in This Week
🔓 Leaked secrets in logs	Secrets pulled securely using secretsmanager:GetSecretValue
🎯 Compromised build container	IAM role scoped only to what it needs (no deploy access)
🚫 Unscanned image deployed	Trivy enforced via buildspec with fail-on-CVE gate
🎭 Cross-service artifact poisoning	S3 bucket write paths scoped to auth-service/ or notes-service/ only
🧪 Bypassed approvals	Manual or scan-based gate required before deploy
🪓 Lateral movement	CodeBuild cannot affect other builds or deploy other services
🕵️‍♀️ Lack of traceability	All events logged and tracked via CloudWatch + build logs


⸻

🔑 IAM Best Practices Used

✅ Per-service IAM Role Scoping

Each CodeBuild job gets its own IAM role, limited to:
	•	Reading only its own secrets
	•	Uploading its own artifacts
	•	Pulling images from ECR (read-only)

🧠 This prevents one pipeline from being used to attack another service.

⸻

✅ Stage-specific Privileges

CodePipeline and CodeBuild have separate IAM roles:
	•	codebuild-auth-service-role → fetch secrets, scan images, upload SBOM
	•	codepipeline-master-role → orchestrate pipeline stages, trigger deploys

⸻

✅ No Wildcard Secrets Access

You should avoid policies like:

"Resource": "*"

Instead, use:

"Resource": "arn:aws:secretsmanager:us-east-1:111111111111:secret:auth-service/db*"

This restricts to only secrets tagged to auth-service.

⸻

🔐 Secrets Security Deep Dive

Technique	Why It Matters
AWS Secrets Manager	Provides versioning, rotation, encryption-at-rest
buildspec secrets-manager: syntax	Ensures secrets are never stored in plaintext on disk
Environment variable handling	Scripts must avoid echo $SECRET or writing secrets to logs
.env.example and dotenv validation	Used only for local development, not production builds


⸻

📦 SBOM, Trivy, and Artifact Hardening

✅ SBOM Artifacts
	•	Generated per build using Trivy in cyclonedx format
	•	Converted to HTML via custom Python
	•	Uploaded to:

s3://devsecops-staging-artifacts/notes-service/{build-id}/sbom.json



🛡️ All files stored securely and versioned for audit purposes.

⸻

✅ CVE Scan Enforcement

Trivy exits with status code if any CRITICAL CVEs are found:

if [ "$CRITICALS" -gt 0 ]; then
  echo "❌ Blocking deploy due to critical vulnerabilities"
  exit 1
fi

✅ This enforces security policy as code — your pipeline won’t silently deploy vulnerable containers.

⸻

🔍 Logging & Observability
	•	CodeBuild sends logs to CloudWatch Logs
	•	You can subscribe to these logs for:
	•	Anomaly detection
	•	Post-mortem analysis
	•	Integration into GuardDuty or SIEMs

⸻

🧠 DevSecOps Concepts Applied

Principle	Implementation
🔐 Least privilege	IAM roles scoped to service, stage, and action
🧱 Defense in depth	Secrets, scans, deploys, and IAM all enforced independently
🧪 Shift-left testing	Vulnerabilities are scanned before deploy
📜 Security as code	IAM, policies, buildspecs all codified in Git
📦 Software supply chain security	SBOMs generated, stored, and versioned for every build


⸻

✅ Your Security Wins This Week
	•	CI/CD builds and deploys are now gated by security
	•	Each microservice is isolated from others in terms of permissions
	•	Every pipeline action is auditable and enforceable
	•	Security failures are loud, visible, and logged