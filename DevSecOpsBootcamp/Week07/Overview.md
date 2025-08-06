📁 Week7/Overview.md

Title: 🏗️ CI/CD Pipelines Part II – AWS CodePipeline & CodeBuild
Focus: Building secure, production-grade CI/CD workflows using AWS-native tooling and integrating prior automation.

⸻

🧠 Conceptual Overview

🧭 Why AWS CodePipeline in DevSecOps?

CI/CD is a critical automation layer — and in AWS-native environments, using CodePipeline + CodeBuild can give you:
	•	Tighter IAM-based security boundaries
	•	Fully managed scalability with zero runners
	•	Built-in integration with CodeCommit, ECR, S3, and CloudFormation
	•	Direct control of source → build → test → deploy flows
	•	Easier traceability and event-driven automation

But misconfigured CodePipelines can:
	•	Leak secrets
	•	Deploy unscanned images
	•	Bypass security controls

This module teaches you how to secure CodePipeline from commit to deploy, integrating SBOM, secrets injection, and controlled IAM roles.

⸻

🧩 Evolving the App This Week

This week, you’ll:
	•	Build a secure AWS CodePipeline for your notes-service
	•	Use CodeBuild to:
	•	Run unit tests
	•	Run Trivy image scans
	•	Generate SBOMs
	•	Store SBOM + scan reports to S3
	•	Deploy your app to ECS (or Lambda) if all checks pass
	•	Use CloudWatch Logs and SNS alerts for pipeline observability

⸻

🔐 DevSecOps Learning Objectives

By the end of this week, you’ll be able to:

✅ Configure CodePipeline using YAML (via AWS CDK or console)
✅ Write secure buildspec.yml files for CodeBuild
✅ Inject and use secrets from AWS SSM securely
✅ Automate SBOM generation and Trivy scans inside CodeBuild
✅ Enforce security gates before deploy (scan must pass)
✅ Isolate build and deploy stages using scoped IAM roles
✅ Push artifacts securely to S3, ECR, or downstream stages

⸻

🧱 What You’ll Build

Component	Description
pipeline.yaml	Defines pipeline structure (CDK or CloudFormation)
buildspec.yml	Tells CodeBuild how to test, scan, generate SBOM
aws-secrets-inject.sh	Reuses secure scripting from Week 5
deploy-to-ecs.sh	Deployment logic gated by scan status
infra/pipeline/	Infra-as-code directory for the pipeline


⸻

📦 Pipeline Stages

Stage	Tool	Purpose
Source	GitHub / CodeCommit	Pull app source
Build	CodeBuild	Test + scan + SBOM
Approval	Manual / Scan check	Block unverified deploys
Deploy	ECS / Lambda	Trigger secure deploy
Notify	SNS / Slack	Optional alerts for failures


⸻

🧰 Tools & Services

Service	Use
CodePipeline	CI/CD orchestration
CodeBuild	Runs build, test, scan, SBOM
SSM Parameter Store	Secure secret injection
ECS or Lambda	Target deployment platform
S3	Artifact and report storage
CloudWatch Logs	Log pipeline and build output
CDK	Optional: Pipeline definition as code


⸻

🧠 Why CodePipeline Security Matters

Poorly secured pipelines often:
	•	Expose environment variables in logs
	•	Let unscanned code go to prod
	•	Fail to isolate build credentials
	•	Ignore IAM boundaries between build/test/deploy

This week, you’ll solve all of these by:
	•	Using secretsManager or ssm:GetParameter for secrets
	•	Applying IAM-per-stage security
	•	Generating SBOM + Trivy scan gates
	•	Storing build artifacts securely in S3
