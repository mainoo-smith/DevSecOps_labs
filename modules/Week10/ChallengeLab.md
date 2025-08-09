# 🧪 Week 10 – Challenge Lab: Securing and Remediating IaC in Production

## 🎯 Challenge Objectives

Your goal is to simulate a real-world DevSecOps incident where:

- Misconfigured infrastructure is discovered via static scans and drift detection
- Secrets were accidentally exposed in ECS container logs
- Overly permissive IAM roles are remediated
- Infrastructure is refactored to enforce secure-by-default patterns

---

## 🔧 Scenario Setup – Simulated Misconfiguration

### ✅ Step 1: Introduce Drift

Go to the AWS Console or use the AWS CLI and manually update a resource **outside of Terraform/CDK**.

Example:
```bash
aws ecs update-service \
  --cluster secure-cluster \
  --service auth-service \
  --desired-count 0
💡 This simulates unauthorized or accidental changes by a team member or system.

🔍 Step 2: Detect Drift Using driftctl
Run this from your Terraform root:

driftctl scan \
  --from tfstate+s3://my-secure-terraform-state/dev/terraform.tfstate \
  --deep
Expected Output:

Found 1 deleted resource outside of Terraform
[DELETED] aws_ecs_service.auth-service
✅ Fix:

terraform apply -var-file="environments/dev.tfvars"
🔐 Why: Drift can indicate security incidents, privilege misuse, or poor Git discipline. Always monitor infra with IaC-aware tools.

🧪 Scenario 2: Secret Appears in Logs
🔥 Problem:
A team member added a line to Dockerfile for debugging:

RUN echo "DB_PASSWORD=${DB_PASSWORD}" >> /var/log/app.log
It leaked into CloudWatch logs via ECS.

✅ Challenge:
Detect the leak via aws logs

Rotate the secret in AWS Secrets Manager

Re-deploy ECS service with new secret version

Steps:

aws secretsmanager rotate-secret --secret-id auth-service-db-secret

# Trigger ECS redeploy to refresh task definition
aws ecs update-service \
  --cluster secure-cluster \
  --service auth-service \
  --force-new-deployment
🔐 Best Practice: Rotate secrets immediately after suspected exposure. Add log-sanitizers to pipelines.

🛑 Scenario 3: Overly Permissive IAM Role
Problem:
The ECS task role has this in your iam.tf:

policy = jsonencode({
  Version = "2012-10-17",
  Statement = [{
    Effect = "Allow",
    Action = "*",
    Resource = "*"
  }]
})
✅ Task:
Replace * with only the needed permissions

Validate the refactor with tfsec, tflint, and checkov

Example Fix:

actions = [
  "secretsmanager:GetSecretValue",
  "logs:CreateLogStream",
  "logs:PutLogEvents"
]
resources = [
  aws_secretsmanager_secret.auth.arn,
  "arn:aws:logs:*:*:*"
]
🔒 Scenario 4: Block Insecure Deployments
Goal:
Prevent a deploy when:

Secrets are hardcoded

Public subnets expose sensitive services

IAM has wildcard permissions

✅ Task:
Add tfsec + checkov + cdk-nag as pre-commit or CI pipeline jobs

Fail the pipeline if security violations are found

Example for GitLab CI:

security_scan:
  stage: test
  image: aquasec/tfsec
  script:
    - tfsec .
  allow_failure: false
📍 DevSecOps Tie-in: This is "shift-left" security — catching violations before deployment.

✅ Completion Checklist
Task	Verified
Detected and fixed drift with driftctl	✅
Rotated secret after simulated log leak	✅
Refactored IAM role with least privilege	✅
Added security scanners to prevent insecure deploys	✅
Redeployed app with rotated secret and hardened infra	✅
🧠 Reflection Prompts
Include your answers in Reflection.md:

What signs might indicate infrastructure drift before you detect it explicitly?

How does IAM misconfiguration increase blast radius?

How would you build pipeline stages to halt deployment if tfsec/checkov fail?

What would you log and alert on in production to catch these issues early?

🚀 Bonus Challenge
Enable Terraform Sentinel or OPA to enforce:

All IAM policies must be scoped by resource and not use "*"

No public subnets in prod environment

All secrets must originate from aws_secretsmanager_secret



