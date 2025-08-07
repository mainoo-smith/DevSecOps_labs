📁 Week7/Reflection.md

Title: Reflection – CI/CD Security with AWS CodePipeline & CodeBuild

⸻

🧠 What We Did

This week, we deepened our CI/CD pipeline capabilities by moving beyond GitHub Actions and GitLab CI to use AWS-native tools:
	•	AWS CodePipeline for orchestration
	•	AWS CodeBuild for building, testing, scanning
	•	Integrated secure deploys to ECS staging
	•	Enforced security gates using Trivy, SBOMs, and IAM isolation

⸻

🔍 Key Takeaways

1. Pipeline Security Is Non-Negotiable

Pipelines are the delivery engine for all software — and therefore a critical attack surface.
If they’re not secured:
	•	You can accidentally ship malware
	•	Secrets can leak into build logs
	•	CVEs can go unaddressed into production

✅ This week we built pipelines that enforce security as a first-class citizen.

⸻

2. IAM Isolation Prevents Cross-Service Attacks

Giving each CodeBuild job its own scoped IAM role:
	•	Limits the impact of any misbehavior or compromise
	•	Prevents one service from accessing another’s secrets, buckets, or deploy targets
	•	Makes it easier to audit and rotate credentials

Least privilege at the build stage is just as critical as in runtime.

⸻

3. Automated CVE Scanning Must Block Deployment

By integrating Trivy and scan enforcement logic:
	•	You prevent vulnerable images from being deployed
	•	Developers are alerted early — shift-left security in action
	•	Every build outputs a machine-readable and human-readable SBOM

SBOMs + scan results = proof of software supply chain due diligence.

⸻

4. Security Must Be Continuous, Not a Checkbox

Each part of the pipeline enforces security:
	•	Buildspec verifies dependencies and code quality
	•	Trivy checks images for vulnerabilities
	•	IAM roles restrict build context
	•	SBOM is archived per build
	•	Only passing builds are deployed

Security isn’t a final step — it’s woven into the CI/CD lifecycle.

⸻

🔄 What We Would Improve

Area	Opportunity
Deployment flexibility	Could introduce manual approvals, version pinning, and rollback support
Multi-account setup	Next step is to separate pipelines into dev/staging/prod accounts
Notifications	Slack/SNS/Teams alerts would improve developer feedback loop
Cost optimization	Some builds could be batched or containerized to reduce execution time


⸻

🧩 DevSecOps Principles Reinforced

Principle	Application
🔐 Least Privilege	IAM per service and per stage
🧱 Defense in Depth	Secure secrets, scan enforcement, deploy verification
🧪 Shift-Left Security	Vulnerabilities caught during build phase
📜 Security as Code	IAM, policies, buildspec, deploy logic all version-controlled
📦 Supply Chain Security	SBOMs and scan logs stored for auditability


⸻

🧳 What We’re Taking Into Week 8

Next, we move into Secrets Management:
	•	Vault for dynamic secrets and encryption
	•	SOPS for file-level encryption in Git
	•	Sealed Secrets for K8s-native secret sealing

We’ll ensure secrets are:
	•	Encrypted at rest and in transit
	•	Auditable and versionable
	•	Never committed to source

🔐 Week 8 will power up your pipeline with enterprise-grade secret hygiene.