# 🔐 Week 13 – Security Deep Dive: Policy-as-Code

---

## 🧠 Why Policy-as-Code Matters

Traditional security practices rely heavily on manual review and tribal knowledge:

- "Don't use `:latest`"
- "Always tag resources"
- "Don’t run containers as root"

But these guidelines are **easy to forget** and **hard to scale**.  
Policy-as-Code transforms security from **suggestion to enforcement**, by encoding rules into version-controlled, testable code.

---

## 🔍 What We're Securing

| Domain       | Risk                                           | PaC Control                              |
|--------------|------------------------------------------------|-------------------------------------------|
| Kubernetes   | Privileged containers, host access             | Rego blocks `hostPath`, privilege escalation |
| ECS          | Running as root, mutable root filesystem       | Rego blocks `user: root`, enforces readonly |
| Terraform    | Missing tags, unencrypted buckets              | Rego enforces metadata and encryption     |
| IAM Policies | Wildcard access (`*`)                          | Rego blocks overly broad permissions      |
| CI/CD        | Undetected drift and misconfigurations         | Policy gates catch violations pre-deploy  |

---

## 🧰 OPA + Rego Security Capabilities

| Feature                    | Description |
|---------------------------|-------------|
| ✅ **Deny-by-default**    | Prevent insecure config automatically |
| 📂 **Modular Rego**       | Reuse policy logic across projects    |
| 🧪 **OPA test**           | Unit-test security logic like application code |
| 🔐 **Admission Control**  | Prevent bad manifests from entering cluster (via Gatekeeper) |
| 📦 **CI/CD Blocking**     | Fail build if security policy is violated |
| 📄 **Versioned Policies** | Track policy evolution alongside app changes |

---

## 📊 Real-World Security Benefits

| Security Practice            | Policy-as-Code Application |
|-----------------------------|----------------------------|
| ✍️ **Secure Coding Standards** | Define policies for config hygiene |
| 🏷️ **Tagging for Governance** | Require tags for cost visibility and traceability |
| 🔒 **IAM Minimization**        | Block overly permissive policies (`*`) |
| 🛡️ **Image Hardening**         | Enforce non-root, deny `:latest`, drop Linux caps |
| 🧼 **Data Hygiene**            | Require S3 encryption, disallow public ACLs |
| 🔁 **Audit Trails**            | All policy decisions are testable, logged, and stored in Git |

---

## 🧠 DevSecOps Alignment

| DevSecOps Principle | Policy-as-Code Impact |
|---------------------|-----------------------|
| Shift Left          | Fail builds at PR/MR time, not runtime |
| Automate Everything | CI runs policies automatically on every change |
| Version Control     | Policy logic stored and tracked in Git |
| Least Privilege     | Policies enforce least privilege in infra/app |
| Compliance-as-Code  | Ready for audits and regulatory reporting |

---

## 📌 Best Practices

- ✅ **Bundle policies with each microservice** (e.g., `services/notes/policies`)
- 📁 **Separate policies by domain** (e.g., `terraform/`, `k8s/`, `ecs/`)
- 🧪 **Write unit tests for policies** using `opa test`
- 🧵 **Document your intent** using policy metadata/comments
- 🔁 **Integrate in all environments**, not just prod
- 🛡️ **Fail builds** on any security violation (use `--fail-on-warn`)
- 🔍 **Review policy changes like code** (pull requests, reviews, approvals)

---

## 🔄 How Policy-as-Code Prevents Drift

PaC ensures that:

- Your Kubernetes manifests conform to cluster standards
- Your Terraform always produces secure, tagged resources
- Your Dockerfiles and ECS configs don’t regress into insecure states

This acts as a **drift prevention mechanism** by making security testable and visible during code review — before merge.

---

## 🧱 Preparing for Zero Trust (Week 17)

These policies form the backbone of:

- Workload isolation
- Identity enforcement
- Resource access control
- Preventing lateral movement

> You can't implement Zero Trust later — you need policy guardrails early on.

---

## ✅ Summary

| Category | Win |
|---------|-----|
| 📋 Governance | Policies codify org-wide security expectations |
| 🧪 Automation | Violations fail in CI/CD pipelines |
| 🔒 Security | Least privilege, hardened workloads, no surprises |
| 🔁 Auditing | Versioned, testable, peer-reviewed policy logic |
| 🧠 Culture | Developers get instant feedback with every commit |

---

## ⏭️ Next

➡️ Proceed to [`Week13/Reflection.md`](./Reflection.md)  
We'll recap lessons, reflect on policy design challenges, and prep for Week 14: **Runtime Security with Falco, eBPF, and Auditd**.

Let me know when you're ready to move on to the Reflection, or if you'd like to dive deeper into OPA unit testing, custom Gatekeeper constraints, or Conftest bundles.

You said:
Ready
ChatGPT said:
Perfect — let’s reflect on Week 13: Policy-as-Code and how it connects to the bigger DevSecOps picture.