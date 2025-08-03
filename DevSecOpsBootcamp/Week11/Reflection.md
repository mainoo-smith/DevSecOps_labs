# 🧠 Reflection – Kubernetes Security I: RBAC, Network Policies & Admission Controls

---

## 🧩 What We Did

This week, we:

- Created an isolated Kubernetes namespace for `auth-service`
- Scoped developer access using **RBAC**
- Applied **NetworkPolicies** to restrict pod-to-pod communication
- Deployed with **ServiceAccounts** instead of using cluster-level identity
- Enforced workload security with **PodSecurity Admission** or **OPA/Kyverno**
- Simulated insecure deployments and actively blocked them

---

## 🔄 What We Learned

### ✅ Security by Design Works
- Most misconfigurations were blocked **before reaching production**.
- Enforcing security **at the manifest level** shifts controls left.

### ✅ Service Identity Is Critical
- Moving from cluster-wide identity to **per-ServiceAccount access** makes lateral movement significantly harder.
- Helps in future modules when we audit logs and connect requests to services.

### ✅ NetworkPolicies Need Planning
- It’s easy to accidentally block traffic (e.g. DNS, health probes).
- Label-based whitelisting helps organize policies cleanly.

---

## ⚠️ What Could Go Wrong in Production

| Risk | Impact |
|------|--------|
| 🔄 RBAC Misconfig | Locking out teams, or over-permissiveness |
| 🌐 NetworkPolicy Gaps | Internal services exposed to everyone |
| ❌ No Admission Controls | Anyone can deploy privileged containers |
| 🛑 Too Much Lockdown | Developers lose velocity without flexibility |
| 🔐 ServiceAccount Token Mounting | Auto-mount tokens can leak identity in sidecars |

---

## 🛠️ How to Improve This

- Apply a **default deny NetworkPolicy** in every namespace
- Use **namespace-bound IAM roles** (IRSA in EKS) instead of shared service accounts
- Integrate **OPA/Kyverno into CI/CD** to validate manifests before deploy
- Automate scanning with tools like **Kubescape** or **kube-bench**
- Track changes to RBAC using **audit logging** or **RBAC visualizers**

---

## 🔍 Real-World Interview Scenario

> **Interviewer:** "How would you ensure that only the frontend app can talk to the auth-service in Kubernetes?"

You could respond:

> "I'd use a combination of NetworkPolicies to restrict ingress to the auth-service to pods with the frontend label, and enforce that each workload uses its own ServiceAccount for traceability. I’d also ensure the deployment manifests are validated through an admission policy so the service cannot be deployed with insecure configurations."

---

## 🚀 How the App is Now More Secure

| Area | Change |
|------|--------|
| Auth-service namespace | Isolated with RBAC |
| Pod-level identity | Uses scoped ServiceAccount |
| Network communication | Restricted to db only |
| Root/privileged containers | Blocked by policy |
| Manifest validation | Enforced pre-deployment or at admission time |

---

## 🎓 Takeaways

- **Kubernetes is powerful**, but insecure by default unless you configure it correctly.
- DevSecOps means securing *everything as code* — RBAC, network access, and identity.
- Week 11 set the stage for deeper controls like:
  - Policy-as-Code (Week 13)
  - Runtime Security (Week 14)
  - Zero Trust Architecture (Week 17)

---

## ✅ You Are Now Able To:

- Lock down a namespace with RBAC and NetworkPolicies  
- Define service-level identity using ServiceAccounts  
- Enforce policy using admission control mechanisms  
- Recognize insecure deployments and block them  
- Confidently secure microservices in Kubernetes

---

➡️ Up Next:  
`Week 12 – ECS & Fargate Security I: Service Connect & IAM Boundaries`

We’ll apply many of these concepts — identity, service isolation, cross-env access — in ECS using Service Connect.

Let me know when you're ready to proceed to Week 12:

🔐 ECS & Fargate Security I – IAM, Namespaces, and Service Connect
We’ll explore isolation, cross-environment access, and runtime enforcement in ECS.

You said:
Proceed 
ChatGPT said:
Awesome. Let’s dive into Week 12 of the DevSecOps bootcamp — now shifting focus from Kubernetes to ECS Fargate, exploring IAM boundaries, Service Connect, and secure cross-environment service communication.