📁 Week5/ChallengeLab.md

Title: End-to-End Secure Automation for a Production Microservice Stack

⸻

🧪 Scenario

You’re now part of the DevSecOps team managing a growing microservices-based app (auth-service, notes-service, notification-service) hosted on ECS and Lambda.

You’re tasked with scripting a secure and portable daily automation routine that:
	1.	Checks health of all deployed services
	2.	Rotates old logs from each container
	3.	Generates and stores daily SBOM reports
	4.	Uploads all logs + reports to a secure S3 archive
	5.	Runs automatically via cron or CI/CD pipeline

You must ensure:
	•	Secrets are never exposed
	•	IAM roles are scoped correctly
	•	Logging avoids sensitive data
	•	CI jobs can run securely in both GitHub and GitLab environments

⸻

🎯 Requirements

Task	Language	Tooling
ECS health & Lambda checks	Bash	AWS CLI
SBOM generation	Python	Trivy
Log rotation & archive	Bash + Python	gzip, boto3
Secrets loading	Bash	AWS SSM
GitOps integration	Both	GitHub Actions / GitLab CI


⸻

🛠️ Tasks

⸻

✅ 1. Create a unified Bash script scripts/automation/daily_ops.sh

This script should:
	•	Accept parameters (e.g. service name, region)
	•	Call other scripts to:
	•	Check service health (ECS + Lambda)
	•	Rotate & archive logs
	•	Generate SBOM and convert to HTML
	•	Upload artifacts to a specific devsecops-prod-logs S3 bucket
	•	Load secrets securely from SSM

The top of the script should look like:

#!/bin/bash
set -euo pipefail

ENV="${1:-prod}"
REGION="${2:-us-east-1}"

The script must log actions to a timestamped file in logs/ (not to stdout).

⸻

✅ 2. Write a Python script scripts/sbom/sbom_daily_report.py
	•	It should take an image name and output both .json and .html
	•	Store results in sbom/YYYY-MM-DD/ folders
	•	Upload to S3 automatically using boto3
	•	Send an optional summary to Slack (mock or print)

⸻

✅ 3. Secure .env file loading
	•	Create .env.example with:

AWS_REGION=
S3_ARCHIVE_BUCKET=
SLACK_WEBHOOK_URL=


	•	Bash and Python scripts should read this securely using dotenv or source .env
	•	In CI/CD: inject values via secrets manager (e.g., AWS_SECRET_ACCESS_KEY, SLACK_TOKEN)

⸻

✅ 4. GitLab or GitHub CI/CD Integration

Create a pipeline job to run your daily_ops.sh:

GitHub Actions example:

jobs:
  daily-automation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: |
          bash scripts/automation/daily_ops.sh prod us-east-1
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

GitLab CI example:

daily_ops:
  script:
    - bash scripts/automation/daily_ops.sh prod us-east-1
  only:
    - schedules


⸻

🔐 Security Requirements
	•	No secrets hardcoded in scripts
	•	Use IAM roles with least privilege (e.g., only allow upload to specific bucket)
	•	Avoid using eval, os.system() or unsanitized variables
	•	Set up .gitignore for .env, *.log, *.gz, and generated SBOM files

⸻

📦 Output Artifacts (Required)

Artifact	Format	Notes
Health Check Logs	logs/ecs_health_YYYY-MM-DD.log	Plaintext, timestamped
SBOM JSON	sbom/YYYY-MM-DD/*.json	CycloneDX
SBOM HTML	sbom/YYYY-MM-DD/*.html	For human consumption
Uploaded logs	s3://devsecops-prod-logs/...	Auto-versioned
Archived app logs	*.gz	Auto-uploaded


⸻

💡 Bonus Challenges
	•	Add Slack notifications using Python (requests.post) to alert if health check fails
	•	Encrypt log archives using AWS KMS before upload
	•	Support different environments (dev, qa, staging, prod) with config files

⸻

✅ Completion Criteria

You’ve succeeded if:
	•	All scripts are functional, reusable, secure
	•	You can trigger the automation manually or via CI/CD
	•	Logs, SBOMs, and outputs are archived to S3
	•	Scripts run without needing root access
	•	No secrets are visible in logs or source control
