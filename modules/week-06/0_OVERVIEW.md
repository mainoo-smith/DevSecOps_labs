```markdown
# 📁 Week06/Overview.md
## Title: Secure CI/CD Pipelines & Artifact Management
### Theme: Automating secure builds, artifact scanning, and safe multi-environment deployments

---

## 🎯 Goal
By the end of this week, you’ll have:

* Built secure CI/CD pipelines using GitLab and GitHub Actions
* Integrated infrastructure + app deployment (Terraform, CDK, SAM)
* Enforced pre-merge and pre-deploy security gates (e.g., `checkov`, `trivy`, `gitleaks`)
* Implemented branch-to-environment promotion (Dev → QA → Stable → UAT)
* Published signed, scanned artifacts to ECR and S3
* Used OpenID Connect (OIDC) for secure deploys without long-lived credentials
* Set up multiple CI agents to handle different app components securely (Python, Node.js)

---

## 🔍 Why This Matters in DevSecOps
DevOps accelerates delivery — but without security, it accelerates risk.

**DevSecOps ensures that automation enforces your security policies, not bypasses them.**
This module shifts security left by:

* Blocking misconfigurations before merge (`checkov`, `trivy`, `gitleaks`)
* Preventing secrets or vulnerable code from entering production
* Requiring approval for high-trust actions like `terraform apply`
* Making security posture observable in the pipeline itself

---

## 🧱 Core Concepts & Theory

### 1. 🔄 CI/CD Lifecycle in DevSecOps

| Stage        | Example Tasks                                  | Security Layer                               |
| :----------- | :--------------------------------------------- | :------------------------------------------- |
| **Commit** | Lint, unit test                                | Pre-commit checks, secrets scanning          |
| **CI** | Build, test, scan                              | SAST, IaC scan, SBOM generation              |
| **Artifact** | Push to ECR/S3                                 | Sign image, scan again (Trivy)               |
| **CD** | Deploy infra/app                               | Gate with plan, require manual approval      |
| **Post-deploy** | Monitor                                        | Drift detection, runtime scanning (later week) |

### 2. 📦 Artifact Security
Artifacts are deployable units — containers, Lambda packages, zip files.
A secure pipeline:

* Scans them before push (CVEs, licenses)
* Signs them with a key
* Stores them in immutable registries (ECR, S3)
* Tags them semantically (e.g., `v1.2.0-dev`, `qa-rc1`, `uat-prod-candidate`)
* Tracks provenance via Git commit or SBOM (later)

### 3. 🔐 Secrets & Credential Management in Pipelines
You’ll:

* Use GitLab & GitHub OIDC to deploy to AWS without hardcoded secrets
* Avoid plaintext environment variables (use GitHub/GitLab Secret Stores)
* Manage access by environment — UAT deploys need reviewer approval, dev does not

### 4. 🌱 Environment Promotion (Branch-to-Env Mapping)

| Git Branch    | Environment | Access Policy                                          |
| :------------ | :---------- | :----------------------------------------------------- |
| `develop`     | dev         | Auto-deploy, fast feedback                             |
| `qa`          | QA          | Deploy on merge + SAST/IaC approvals                   |
| `stable`      | staging     | Requires pipeline pass + reviewer                      |
| `uat`         | UAT         | Controlled deploy from stable only                     |

This will set the foundation for RBAC, audit trails, and deployment hygiene.

---

## 🛠️ Tooling Breakdown

| Tool                  | Role                                                      |
| :-------------------- | :-------------------------------------------------------- |
| **GitLab CI/CD** | Declarative pipelines (YAML) with security jobs           |
| **GitHub Actions** | Event-based CI/CD, great for OpenID and fine-grained workflows |
| **Terraform + CDK + SAM** | Infrastructure as Code delivery                           |
| **Trivy** | Container, IaC, and artifact scanner                      |
| **Gitleaks** | Detect hardcoded secrets in commits                       |
| **Checkov / tfsec** | IaC misconfiguration detection                            |
| **AWS ECR / S3** | Secure artifact registry with image scanning              |
| **AWS OIDC** | Deploy to AWS from GitHub/GitLab without long-term AWS keys |

---

## 🔄 Application Evolution This Week
We're now evolving our monorepo into a full DevSecOps-ready application.
You'll:

* Containerize both the Python backend and Node.js frontend
* Push signed/scanned images to ECR
* Deploy via CI/CD using approved infrastructure plans
* Route each environment (dev, qa, staging, uat) with namespace isolation (ECS Fargate)
* Lay the foundation for SBOMs and runtime policies (future modules)

---

## ✅ By End of Week 6, You Will Be Able To:
* Build secure CI pipelines for microservices + infrastructure
* Auto-deploy safely to multiple environments
* Block insecure merges/deploys using pipeline policy gates
* Securely manage pipeline credentials (OIDC vs access keys)
* Run IaC, container, and secrets scans as part of every PR and commit
```