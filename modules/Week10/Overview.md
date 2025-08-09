# IaC Fundamentals & Security with Terraform, CDK, CloudFormation, and SAM

## 🎯 Objective
In Week 10, you will:

* Understand the foundational and advanced principles of **Infrastructure as Code (IaC)**.
* Explore the IaC tools powering modern DevSecOps pipelines: `Terraform`, `AWS CDK`, `CloudFormation`, and `AWS SAM`.
* Implement defensive infrastructure configurations.
* Scan IaC code for misconfigurations and CVEs.
* Detect drift, prevent privilege escalation, and enforce least privilege.
* Begin evolving the infrastructure behind your app (e.g. `auth-service`, `notes-service`) using IaC.

---

## 🧠 Concepts & Theory

### 💡 What is Infrastructure as Code?
**IaC** is the practice of managing infrastructure (servers, networks, IAM, databases) using versioned, machine-readable definitions — just like code.

**Core principles:**

| Principle | Description |
| :--- | :--- |
| 🔁 **Idempotence** | Running IaC repeatedly produces the same result. |
| 📝 **Versioning** | Changes to infrastructure are tracked in Git. |
| 🔍 **Reviewability** | Infrastructure can be peer-reviewed via pull requests. |
| ✅ **Automatable** | CI/CD pipelines apply infrastructure with control gates. |
| 🧪 **Testable** | IaC can be statically analyzed and tested pre-deploy. |

### 🏗️ The Tools We'll Explore

| Tool | Language | Use Case | Why It Matters |
| :--- | :--- | :--- | :--- |
| **Terraform** | HCL | Cloud-agnostic IaC | Most widely adopted IaC tool. |
| **AWS CDK** | TypeScript/Python | AWS-native IaC using real code | Enables abstraction & reusable logic. |
| **CloudFormation**| YAML/JSON | AWS-native IaC | Integrated with AWS services. |
| **SAM** | YAML | IaC for serverless apps | Focused on `Lambda`/`APIGW`/`DynamoDB`. |

---

## 🔐 Why IaC Security Is Critical
When IaC goes wrong, it leads to:

| Misconfiguration | Risk |
| :--- | :--- |
| Open `0.0.0.0/0` in security groups | Unauthorized external access. |
| IAM roles with `*` permissions | Privilege escalation. |
| Hardcoded secrets in `Terraform` | Credential leaks. |
| Drifted resources | Inconsistent security posture. |
| Untracked changes via console | Shadow infrastructure. |

---

## 🔧 Tools for Securing IaC

| Tool | Purpose |
| :--- | :--- |
| `tfsec` / `tflint` | Terraform static analysis. |
| `checkov` | Multi-tool IaC scanning (`Terraform`, `CFN`, `CDK`). |
| `cfn-lint` | CloudFormation best practices. |
| `cdk-nag` | CDK security compliance checks. |
| `driftctl` | Drift detection between declared vs. real infra. |
| `aws-nuke` | Cleanup unused or orphaned resources. |

---

## 📦 App Evolution This Week
Our secure note/task app will evolve as follows:

| Component | IaC Change |
| :--- | :--- |
| **Auth Service** | `VPC`, `ECS` Service, `IAM` Role via `Terraform` & `CDK`. |
| **Secrets** | Stored in `AWS Secrets Manager` via `CDK` or `Terraform`. |
| **CI/CD Infra** | `CodePipeline` + `CodeBuild` via `CDK`. |
| **Audit Logging** | Add `CloudTrail` + `CloudWatch` infra declarations. |
| **IAM Role Policies** | Minimized permissions per service with `CDK` validation. |
| **Staging/UAT Isolation** | Environment-based infra modeled and deployed via IaC. |

---

## 🧰 Key Features in AWS CDK

| Feature | Why It Matters |
| :--- | :--- |
| **Constructs** | Reusable components for services (e.g. `EcsService`, `Vpc`). |
| **Stacks** | Group related resources (e.g., `AppStack`, `NetworkStack`). |
| **Environments**| Isolate `dev`/`qa`/`prod` infra programmatically. |
| **Aspects** | Add rules like security checks (`cdk-nag`) across stacks. |
| **Outputs** | Export values (e.g. ARNs, URLs) between stacks. |
| **Context** | Pass shared config or global values into builds. |

---

## 🛡️ DevSecOps Principles Reinforced

| Principle | Application |
| :--- | :--- |
| 🔍 **Shift-left** | Scan IaC in PR before deployment. |
| 🧱 **Defense in Depth** | Secure networking, IAM, VPCs, roles. |
| 🧾 **Auditability** | All changes committed and versioned in Git. |
| 🚫 **Least Privilege** | IAM roles and secrets access scoped tightly. |
| 🔄 **Drift Detection** | Identify out-of-band changes in real infra. |
| ✅ **Automated Provisioning** | `CDK`/`Terraform` controlled by pipeline, not humans. |

---

## 📄 Deliverables This Week
* `Terraform` modules or `CDK` stacks for:
    * `VPC`, `ECS`, `RDS` (or `DynamoDB`), `IAM` roles, Secrets.
    * `CodePipeline` + `CodeBuild`.
* All IaC committed to **Git**.
* Security scanning integrated in **CI** (e.g., `tfsec`, `checkov`, `cdk-nag`).
* Cloud resources managed **only through code**.
* **No use of AWS Console** for deployed services.
* Separation of infrastructure into `staging`, `UAT`, and `prod`.

---

Let me know when you're ready to begin the detailed, multi-part `GuidedLab.md`. We'll:

1.  Scaffold infrastructure using `Terraform`.
2.  Mirror it with `AWS CDK`.
3.  Harden both with scanners and IAM restrictions.
4.  Deploy via pipeline.
5.  Evolve the app with secure-by-default infrastructure provisioning.

This will be our deepest and most transformative week yet.