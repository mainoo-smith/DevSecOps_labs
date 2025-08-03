# 🧠 Week 13 – Policy-as-Code (OPA, Kyverno, Gatekeeper)

---

## 🎯 Goal

Introduce and implement **Policy-as-Code** using tools like:

- **OPA (Open Policy Agent)** – General-purpose policy engine
- **Gatekeeper** – Kubernetes admission controller for OPA
- **Kyverno** – Native Kubernetes policy engine (optional)
- **Conftest** – For testing policies against IaC (e.g., Terraform)
- ECS IAM policy validation via custom scripts or Conftest
- GitLab/GitHub policy enforcement in CI/CD pipelines

> We'll learn how to express **security rules as code**, validate them in CI/CD, and reject deployments that break rules.

---

## 🧠 Core DevSecOps Concepts

| Concept | Description |
|---------|-------------|
| 📜 Policy-as-Code | Define infrastructure and security rules in code (YAML, Rego) |
| 🧪 Admission Controls | Prevent unauthorized Kubernetes/ECS resources from deploying |
| ✅ Pre-Deployment Checks | Reject IaC or manifests that violate security policies |
| 🔍 Drift Detection | Compare actual config vs. desired state in policies |
| 🧰 OPA / Gatekeeper | Evaluate policies in Kubernetes clusters or pipelines |
| 🔒 Trust Enforcement | Enforce non-root, disallow latest tags, restrict hostPaths |

---

## 🛠️ Tools We’ll Use

| Tool | Purpose |
|------|---------|
| ✅ **OPA** | Define and evaluate policies (Rego language) |
| 🧱 **Gatekeeper** | Kubernetes-native enforcement (CRDs + OPA) |
| 🔐 **Conftest** | Validate IaC (Terraform, YAML, Dockerfile) via OPA |
| 🔧 **Kyverno** (optional) | Easier YAML-native policies for K8s |
| 🧪 **GitHub/GitLab CI** | Run policy checks in pre-merge hooks |
| 📄 **Rego** | Policy language used by OPA and Gatekeeper |

---

## 📦 How the App Evolves

This week, we **codify constraints** for our ECS + Kubernetes environments:

| Area | Policy |
|------|--------|
| ECS Task Definitions | Must drop all `CAP_*`, enforce `non-root` |
| Container Images | Disallow `:latest` tags in production |
| IAM Roles | Must not include wildcard (`*`) actions |
| Terraform Modules | Required tagging, encryption enabled |
| Kubernetes Manifests | Block hostPath, require labels, enforce non-root |
| CI/CD Pipelines | Fail build if policy checks do not pass |

> All policies are tested pre-deploy and enforced at runtime (via admission controls or CI gates).

---

## 🔐 Why Policy-as-Code Matters

In a growing DevOps team or regulated environment, you can’t rely on humans to:

- Remember best practices
- Always write secure Dockerfiles or YAML
- Avoid wildcards in IAM roles

> Policies **codify security**, shift enforcement left, and make decisions repeatable.

---

## 🧠 DevSecOps Tie-In

| Practice | Benefit |
|---------|---------|
| ✅ Automation | Policies run automatically in CI/CD pipelines |
| 🧪 Verification | Test IaC and K8s configs before deploying |
| 🛡️ Security as Code | Teams don’t guess — they follow enforced rules |
| 🔄 Auditable Controls | All policy changes go through Git review |
| ⛔️ Deployment Guardrails | Unsafe changes are blocked early |

---

## 📚 Learning Outcomes

✅ Write security policies in **Rego**  
✅ Use **Conftest** to validate Terraform, Kubernetes YAML, Dockerfiles  
✅ Integrate policy checks into **CI/CD pipelines**  
✅ Enforce rules on ECS task definitions and IAM roles  
✅ Understand how **OPA/Gatekeeper** prevent drift and enforce standards  
✅ Prepare the foundation for **Zero Trust** in deployment and runtime

---

## ✅ Prerequisites

- Basic familiarity with Terraform, YAML, Dockerfile
- GitLab or GitHub pipeline set up (from earlier weeks)
- Local development environment with:
  - Docker
  - OPA CLI
  - Conftest
- Sample IaC code or K8s manifests from earlier bootcamp modules

---

## 🔄 Coming Up Next

➡️ `Week13/GuidedLab.md`  
We’ll build real policies and enforce them across ECS task definitions, IAM roles, and Kubernetes workloads.

---

Let me know when you’re ready to proceed with the Week 13 Guided Lab — where we’ll:

Write your first Rego policy

Test it against Dockerfiles, ECS definitions, IAM roles

Embed Conftest into your CI/CD pipeline

Would you like to start with ECS, Kubernetes, or IaC/Terraform policies?

You said:
Ready
ChatGPT said:
Great — let’s dive into the Week 13 Guided Lab, where we bring Policy-as-Code to life using OPA, Conftest, and CI/CD integration. This will help us catch insecure configurations before they ever make it to staging or production.