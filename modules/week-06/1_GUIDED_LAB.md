````markdown
# 📁 Week06/GuidedLab.md
## Title: Build Secure CI/CD for App + Infrastructure + Artifact Management

---

## 🧠 What You’ll Do
* Set up secure GitHub Actions and GitLab pipelines
* Automate secure deployment of:
    * Python backend (as container)
    * Node.js frontend (as container)
    * ECS infra (via Terraform/CDK)
* Add security gates:
    * `checkov`, `trivy`, `gitleaks`, `cfn-lint`
* Push signed & scanned images to AWS ECR
* Implement OIDC for secretless AWS deploy
* Use Git branches to promote between `dev` → `qa` → `stable` → `uat`

---

## 🧱 PART 1: Prep Your Repositories (Monorepo Setup)

```bash
repo/
├── .github/workflows/        ← GitHub Actions (or .gitlab-ci.yml)
├── infrastructure/
│   ├── terraform/            ← ECS, VPC, ALB, etc.
│   ├── cdk/
│   └── sam/
├── backend/                  ← Python Flask or FastAPI
├── frontend/                 ← Node.js (e.g. Vite + React)
└── scripts/ci/               ← Shared scan/publish scripts
````

-----

## 🔐 PART 2: Secure GitHub → AWS OIDC Authentication

### ✅ Why use OIDC?

  * No AWS access keys.
  * No secret rotation.
  * No storage of credentials.
  * Only valid builds from your repo can assume roles.

### Step 1: Create OIDC IAM Role

```bash
aws iam create-role --role-name GitHubDeployRole \
  --assume-role-policy-document file://trust-policy.json
```

**`trust-policy.json`:**

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Federated": "arn:aws:iam::<account_id>:oidc-provider/token.actions.githubusercontent.com"
    },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
        "token.actions.githubusercontent.com:sub": "repo:<owner>/<repo>:ref:refs/heads/dev"
      }
    }
  }]}
```

🎯 This allows only the `dev` branch in your repo to assume the role.

### Step 2: Attach Minimal Policies

```bash
aws iam attach-role-policy \
  --role-name GitHubDeployRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess

aws iam attach-role-policy \
  --role-name GitHubDeployRole \
  --policy-arn arn:aws:iam::aws:policy/AWSCloudFormationFullAccess
```

Later, use custom least-privilege roles per environment.

-----

## 🤖 PART 3: GitHub Actions CI/CD for Python + Node + Infra

### 📦 Step 1: Secure CI for Backend

Create `.github/workflows/backend.yml`

```yaml
name: Backend CI/CD
on:
  push:
    branches: [dev, qa, stable, uat]
permissions:
  id-token: write
  contents: read
jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to ECR
      uses: aws-actions/amazon-ecr-login@v2

    - name: Build backend
      run: |
        docker build -t backend:${{ github.sha }} ./backend
        docker tag backend:${{ github.sha }} ${{ secrets.ECR_REGISTRY }}/backend:${{ github.sha }}

    - name: Trivy Image Scan
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: ${{ secrets.ECR_REGISTRY }}/backend:${{ github.sha }}

    - name: Push to ECR
      run: docker push ${{ secrets.ECR_REGISTRY }}/backend:${{ github.sha }}

    - name: Assume OIDC Role
      uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: arn:aws:iam::<account>:role/GitHubDeployRole
        aws-region: us-east-1
```

### 🧪 Step 2: Secure CI for Infra

Add `.github/workflows/infra.yml`

```yaml
name: Terraform CI
on:
  pull_request:
    paths:
      - 'infrastructure/**'
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Install tools
      run: |
        curl -sSL [https://install.terraform.io](https://install.terraform.io) | bash
        pip install checkov
    - name: Terraform Init & Plan
      run: |
        cd infrastructure/terraform
        terraform init
        terraform plan
    - name: Checkov IaC Scan
      run: checkov -d infrastructure/terraform
```

### 🔐 Step 3: Add Secrets Scan

Add to all CI jobs:

```yaml
    - name: Secrets Scan
      uses: zricethezav/gitleaks-action@v2
```

### 📤 Step 4: Promote Environments via Branches

| Branch   | Auto Deploy? | Approval Needed?                           |
| :------- | :----------- | :----------------------------------------- |
| `dev`    | ✅ yes        | ❌ no                                      |
| `qa`     | ✅ yes        | ✅ after SAST, IaC pass                    |
| `stable` | ✅ yes        | ✅ with reviewer                           |
| `uat`    | ✅ yes        | ✅ tagged artifact only                    |

-----

## 🛠️ PART 4: GitLab CI/CD Sample for Frontend

Add `.gitlab-ci.yml`:

```yaml
stages:
  - lint
  - test
  - build
  - scan
  - deploy

lint:
  stage: lint
  script:
    - npm install
    - npm run lint

test:
  stage: test
  script:
    - npm test

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_SHORT_SHA ./frontend
    - docker push $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_SHORT_SHA

scan:
  stage: scan
  script:
    - trivy image $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_SHORT_SHA

deploy:
  stage: deploy
  only:
    - dev
  script:
    - aws ecs update-service --cluster dev-cluster --service frontend --force-new-deployment
```

🔐 Add secret variables (e.g., `AWS_ACCESS_KEY_ID`, `OIDC_ROLE`) in GitLab settings.

-----

## ✅ You’ve Now Covered:

  * ✅ Secure builds for both backend & frontend
  * ✅ Scan containers, IaC, and secrets in every pipeline
  * ✅ Push only scanned artifacts to AWS ECR
  * ✅ Promote between environments using Git branch control
  * ✅ Deploy apps + infra securely without long-term secrets

<!-- end list -->

```
```