📁 Week7/ChallengeLab.md

Title: Zero-Trust CI/CD with AWS CodePipeline – From Source to Staging

⸻

🧪 Scenario

You’re now in charge of setting up staging deployments for two services:
	•	auth-service
	•	notes-service

Both services must:
	•	Be scanned for vulnerabilities before deployment
	•	Generate a daily SBOM (stored in S3 and versioned)
	•	Deploy only if scans return zero critical CVEs
	•	Fetch all secrets from AWS SSM or Secrets Manager
	•	Support version-based deploys in ECS (e.g. deploy auth-service:v2.1.3 to staging)

You must:
	1.	Build and deploy a fully separated CI/CD pipeline for each service
	2.	Enforce stage-level IAM isolation
	3.	Use CloudFormation or CDK to define the infra
	4.	Write buildspec.yml for both services
	5.	Add scan enforcement gates before deployment
	6.	Set up log exports to CloudWatch

⸻

📦 Deliverables

Item	Format
infra/auth-pipeline/buildspec.yml	YAML
infra/notes-pipeline/buildspec.yml	YAML
infra/cdk/ or infra/cloudformation/*.yaml	CodePipeline & CodeBuild definitions
scripts/deploy/staging_deploy.sh	ECS deployment logic
scripts/sbom/gen_sbom.py	Reuse from earlier weeks
trivy-scan-summary.json	Trivy CVE summary per build
S3 structure	s3://devsecops-staging-artifacts/{service}/{build-id}/


⸻

🛠️ Tasks

⸻

✅ 1. Use CDK or CloudFormation to define separate CodePipelines

Each service should have:
	•	Source (GitHub or CodeCommit)
	•	Build stage with:
	•	SBOM generation
	•	Trivy scan
	•	Artifact packaging
	•	Approval gate:
	•	Fail pipeline if critical CVEs > 0
	•	Deploy stage:
	•	Push image tag auth-service:vX.Y.Z or notes-service:vX.Y.Z to ECS staging
	•	Send Slack/SNS notification (optional)

⸻

✅ 2. Write buildspec.yml with scan enforcement logic

Add Trivy logic like:

CRITICALS=$(trivy image --severity CRITICAL --exit-code 0 --format json -o trivy.json $IMAGE_NAME | jq '.Results[].Vulnerabilities[] | select(.Severity=="CRITICAL")' | wc -l)

if [ "$CRITICALS" -gt 0 ]; then
  echo "❌ Critical CVEs found: $CRITICALS"
  exit 1
fi

Also store:

aws s3 cp sbom.json s3://devsecops-staging-artifacts/$SERVICE/$BUILD_ID/


⸻

✅ 3. Build a Secure staging_deploy.sh Script

#!/bin/bash
set -euo pipefail

VERSION="$1"
SERVICE="$2"

aws ecs update-service \
  --cluster notes-staging \
  --service "$SERVICE" \
  --force-new-deployment \
  --desired-count 2 \
  --deployment-configuration maximumPercent=200,minimumHealthyPercent=100

echo "✅ $SERVICE deployed version $VERSION to staging"

Integrate it only after successful scan.

⸻

✅ 4. IAM Role Scoping

Each CodeBuild project must have an IAM role with:
	•	ssm:GetParameter
	•	secretsmanager:GetSecretValue
	•	s3:PutObject scoped only to its service
	•	No permissions to deploy to other services

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "s3:PutObject",
      "Effect": "Allow",
      "Resource": "arn:aws:s3:::devsecops-staging-artifacts/auth-service/*"
    }
  ]
}


⸻

✅ 5. Artifact Versioning & Logs

Use CloudWatch Logs to:
	•	Log scan results
	•	Log SBOM generation
	•	Log SSM access

Bucket structure example:

s3://devsecops-staging-artifacts/
├── auth-service/
│   ├── build-20250725/
│   │   ├── sbom.json
│   │   ├── trivy.json
├── notes-service/
    ├── build-20250725/
        ├── sbom.json
        ├── trivy.json


⸻

🔐 DevSecOps Requirements

✅ Secrets must never be hardcoded
✅ CVE gate must block deployment
✅ IAM must be scoped to per-service access
✅ Deploy must tag and version ECS correctly
✅ Logs must avoid sensitive data

⸻

🎯 Success Criteria

You succeed when:
	•	CodePipelines for both services are working
	•	Trivy enforces no critical vulnerabilities
	•	SBOMs are uploaded per build
	•	Versioned image deploys happen to staging
	•	IAM is scoped and logs do not leak secrets
