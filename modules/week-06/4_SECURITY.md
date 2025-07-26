```markdown
# 📁 Week06/Security.md
## Title: “Securing the Pipeline: Shifting Left in CI/CD”

---

## 🧠 Why CI/CD Security is Core to DevSecOps
CI/CD is the heartbeat of DevOps — it touches:

* Your code
* Your infra
* Your credentials
* Your production environments

If an attacker compromises your pipeline, they can bypass all runtime controls — making CI/CD a critical security boundary.

---

## 🔍 Key Threats in CI/CD Pipelines

| Risk                               | Description                                                      |
| :--------------------------------- | :--------------------------------------------------------------- |
| **Secrets in repos or env vars** | Hardcoded keys in code or exposed to builds                      |
| **Unscanned IaC/app code** | Misconfigurations go live without detection                      |
| **Artifact tampering** | Images pushed without scanning, tagging, or validation           |
| **Manual deploys from dev machines** | Bypasses audit logs and policy gates                             |
| **Unapproved code merged to secure branches** | No human in the loop for prod                                    |
| **Over-permissive CI roles** | CI can modify anything in AWS/GCP without restrictions           |
| **Shadow pipelines** | Old/insecure pipelines with outdated runners                     |

---

## 🔐 Essential CI/CD Security Controls

| Layer               | Control                                                        |
| :------------------ | :------------------------------------------------------------- |
| **Source Control** | Protected branches, required PR approvals, code owners         |
| **Pre-Commit** | Hooks with `gitleaks`, `checkov`, `trivy` config scan          |
| **CI Security Gates** | Fail pipelines on SAST/IaC/secrets/CVE violations              |
| **Artifact Control** | Immutable ECR/S3, signed tags, image scanning on push          |
| **IAM Access** | OIDC role assumption (no long-lived AWS secrets)               |
| **Manual Approvals** | Required for `terraform apply`, prod deploy                    |
| **Multi-Env Isolation** | Git branch + env mapping (dev/qa/stage/uat/prod)             |
| **Audit Logging** | CloudTrail on assumed roles and deploy actions                 |
| **RBAC in CI/CD** | GitLab groups, GitHub environments with role policies          |

---

## ✅ Secure CI/CD Architecture Pattern

```

```
         +------------------------+
         |        Source Code     |
         |    (GitHub/GitLab)     |
         +------------------------+
                   |
             (Webhook Trigger)
                   |
           +-----------------+
           |     Pipeline    |
           |  (GitHub/GitLab)|
           +-----------------+
         /       |         \
        /        |          \
 +---------+ +----------+ +-----------+
 | IaC Scan| | Secrets  | | Container |
 | Checkov | | Gitleaks | | Trivy     |
 +---------+ +----------+ +-----------+
        \         |          /
         \        |         /
          \       |        /
          +----------------+
          |    Approval    |
          |  (Manual Gate) |
          +----------------+
                   |
              +-----------+
              | Deploy to |
              |   AWS     |
              +-----------+
                   |
           (OIDC AssumeRole)
```

```

---

## 🔧 Secure Pipeline Practices by Tool

| Tool         | Best Practices                                                                     |
| :----------- | :--------------------------------------------------------------------------------- |
| **GitHub Actions** | Use OIDC with least-privilege roles; protect environments; use required reviewers  |
| **GitLab CI/CD** | Store secrets in CI/CD Variables; use environments + approval jobs; enable pipeline policies |
| **Terraform** | Run `plan` + `checkov` before `apply`; avoid auto-apply for prod                   |
| **SAM/CDK** | Scan templates with `cfn-lint`, `cdk-nag`; require diffs in MR                     |
| **Docker** | Use `trivy`, sign/tag images; fail builds on critical CVEs                         |
| **AWS Deploys** | Use IAM roles per environment; deny non-CI access via policy                       |
| **ECR/S3** | Mark artifacts immutable; require `scanOnPush` for ECR                             |

---

## 🧪 Detecting & Blocking CI/CD Attacks

| Threat                   | Detection                   | Control                                       |
| :----------------------- | :-------------------------- | :-------------------------------------------- |
| Secret leaked in commit  | `gitleaks`, GitHub secret scan | Fail PR, alert dev                              |
| Insecure SG in Terraform | `checkov` in CI             | Block merge                                   |
| CVE in backend image     | `trivy` in CI               | Block build step                              |
| Dev deploys manually     | IAM policy audit, CloudTrail | Limit role access to CI only                  |
| Wrong branch to UAT      | `github.ref` check          | Require annotated commit or PR approval       |

---

## 🧠 Final Principles

* CI/CD is not just automation — it’s a security boundary
* Shift security left — run scans at every phase (commit, build, deploy)
* Replace “hope-based” deploys with policy-enforced pipelines
* Monitor drift between intended state (CI) and deployed state (AWS)

---

## 🔐 Your New Security Responsibilities
As a DevSecOps Engineer, you are now responsible for:

| Responsibility                             | Impact                                                      |
| :----------------------------------------- | :---------------------------------------------------------- |
| Designing pipelines that block insecure deploys | Protects prod from human error                              |
| Implementing guardrails, not gates         | Empowers devs with safe defaults                            |
| Managing role-based CI/CD access           | Limits blast radius of credential misuse                    |
| Observing and alerting on pipeline anomalies | Reduces dwell time of pipeline attacks                      |
| Teaching others to scan before they build  | Culture of secure engineering                               |

---

✅ CI/CD is now secured, monitored, and enforced — not just scripted.

You're operating at real-world DevSecOps level.
```