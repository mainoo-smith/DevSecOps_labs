````markdown
# 📁 Week06/ChallengeLab.md
## Title: “Catch Me If You Can: CI/CD Incidents and Security Enforcement”

---

## 🧠 Scenario
Your company has CI/CD pipelines for its Python backend, Node.js frontend, and infrastructure (Terraform/CDK).

This week, the following events occur:

| Incident                       | Description                                                     |
| :----------------------------- | :-------------------------------------------------------------- |
| 🔥 Secret pushed to Git        | A dev commits AWS credentials by mistake                        |
| ❌ Insecure Terraform Merge    | A team member bypasses security group validation                |
| 🐛 Vulnerable container built  | Outdated image with CVEs is pushed                              |
| 🚫 Deployment to UAT from wrong branch | A feature from `dev` accidentally gets to UAT                   |
| 🌀 Drift between ECR and deployed task | Deployed version differs from tagged artifact                   |
| 🤖 Developer tries to deploy manually from laptop | Bypassing CI/CD — no traceability                               |

Your job is to simulate, detect, and block these before they cause damage.

---

## 🧪 Challenge 1: Secret Leak in Git Commit

### Step 1: Simulate the Mistake

```bash
echo 'AWS_SECRET_ACCESS_KEY=abcd1234' >> backend/.env
git add backend/.env
git commit -m "oops: testing db fix"
````

### Step 2: Run Gitleaks Manually

```bash
gitleaks detect --source .
```

✅ You should see output like:

```text
Secret detected: AWS_SECRET_ACCESS_KEY
```

🎯 Fail the pipeline on this detection.

### Step 3: Add Gitleaks to CI

**GitHub:**

```yaml
- name: Secrets Scan
  uses: zricethezav/gitleaks-action@v2
```

**GitLab:**

```yaml
secrets:
  stage: scan
  script:
    - gitleaks detect --source .
```

-----

## 🔥 Challenge 2: Insecure Terraform Code Merged

### Step 1: Add Misconfig

In `infrastructure/terraform/ecs.tf`, add:

```hcl
resource "aws_security_group_rule" "bad_rule" {
  type        = "ingress"
  from_port   = 0
  to_port     = 65535
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
  security_group_id = aws_security_group.main.id
}
```

### Step 2: Checkov Should Detect This

```bash
checkov -d infrastructure/terraform
```

✅ Output:

```csharp
[CKV_AWS_260] Security group allows unrestricted ingress from 0.0.0.0/0
```

### Step 3: Enforce in CI

Block the merge unless `checkov` passes.

```yaml
- name: Checkov Scan
  run: checkov -d infrastructure/terraform
```

-----

## 🐳 Challenge 3: Vulnerable Image Gets Deployed

### Step 1: Build Image with Vulnerable Package

In `Dockerfile`:

```dockerfile
FROM python:3.8
RUN pip install flask==1.0.0
```

Flask 1.0.0 has known CVEs

### Step 2: Run Trivy Locally

```bash
trivy image backend:vuln
```

✅ You should see:

```text
[HIGH] Flask 1.0.0 has XX vulnerabilities...
```

### Step 3: Enforce in CI

Add to pipeline:

```yaml
- name: Trivy Image Scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: backend:${{ github.sha }}
    severity: HIGH,CRITICAL
    exit-code: 1
```

🛡️ If HIGH or CRITICAL CVEs are found, the job fails.

-----

## 🌀 Challenge 4: Wrong Branch Deployed to UAT

### Step 1: Simulate Branch Confusion

A dev merges a feature to `dev`, but QA approves it accidentally into `uat`.

### Step 2: Validate `ref` Before Deploying

Update CI job to block unauthorized deploy:

```yaml
if: github.ref == 'refs/heads/uat' && contains(github.event.head_commit.message, '[uat-approved]')
```

🔐 Tag or annotate commits to `uat` with required approvals.

-----

## 🧾 Challenge 5: ECR Image \!= Deployed Version

### Step 1: Push Image

```bash
docker build -t backend:v1.2.0 .
docker push <ecr>/backend:v1.2.0
```

### Step 2: Deploy Incorrectly Tagged Task

Manually deploy the wrong image version (`v1.0.0`).

### Step 3: Add ECR Drift Check Job

Use ECR CLI or script:

```bash
aws ecs describe-tasks ... | jq '.[] | .containers[].image'
```

Compare with Git tag or commit hash.

✅ Add pipeline check:

```bash
if deployed_image != tagged_artifact:
   echo "Drift detected!"
   exit 1
```

-----

## 👨‍💻 Challenge 6: Manual Deploy from Dev Machine

### Step 1: Simulate

Run `terraform apply` or `aws ecs update-service` directly from a dev laptop.

### Step 2: Catch Unauthorized Role Use

Use AWS CloudTrail to log role usage:

```bash
aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=DevUser
```

✅ This should alert if deploys bypass CI OIDC or IAM roles.

-----

## ✅ Checklist

| Incident         | Tool Detection             |
| :--------------- | :------------------------- |
| Secrets in Git   | Gitleaks                   | Pre-commit, CI scan |
| Insecure IaC     | Checkov, tfsec             | Fail merge          |
| Vulnerable containers | Trivy                      | Fail build          |
| Wrong env promotion | Git branch policy          | Tag validation      |
| Artifact drift   | ECS + ECR compare          | Alert and rollback  |
| Manual deploys   | IAM Role usage + CloudTrail | Alert and block     |

-----

🏁 You now understand how to simulate and guard against the most common real-world CI/CD incidents.

```
```