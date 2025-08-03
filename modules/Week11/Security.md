# 🔐 Security – Kubernetes RBAC, NetworkPolicy & Admission Controls

---

## 🧠 Core Security Concepts

| Concept | Description |
|--------|-------------|
| 🔐 **RBAC** | Controls *who* can access Kubernetes resources and *what* they can do |
| 🛡️ **ServiceAccounts** | Assign identity to workloads (e.g. `auth-service`) instead of giving full cluster access |
| 🌐 **NetworkPolicy** | Controls *pod-to-pod* communication to enforce least privilege |
| 🚫 **Admission Controllers** | Prevent risky workloads from being created (e.g., privileged, root) |
| 🧱 **Namespace Isolation** | Logical security boundary; used to apply RBAC, NetworkPolicy, quota, PodSecurity rules |
| ⚠️ **SecurityContext** | Pod/container-level rules (e.g. disallow `runAsRoot`, disable privilege escalation) |

---

## 🔐 Security Threats Mitigated This Week

| Threat | Defense |
|--------|---------|
| 🚨 Developer accidentally deploys insecure pod (root, privileged) | Admission controller rejects it |
| 📡 Pod accesses unauthorized services (e.g., Redis, other microservices) | NetworkPolicy blocks traffic |
| 👤 Unauthorized user accesses dev namespace | RBAC prevents it |
| 🔧 Workloads inherit cluster-admin privileges | Explicit ServiceAccounts with scoped permissions |
| 🐛 Exploited container escalates to node | `securityContext` + admission controller block it |

---

## 🧩 Best Practices: RBAC in Production

- Use **Roles** + **RoleBindings** for namespace-specific permissions  
- Avoid `cluster-admin` outside break-glass scenarios  
- Audit users and groups mapped from IAM (e.g. via `aws-iam-authenticator`)  
- Use **read-only roles** for observability tooling  
- Store RBAC policies in Git (infrastructure as code)

---

## 🌐 Best Practices: NetworkPolicy

- Start with **default deny** (`podSelector: {}` + no `ingress`/`egress`)
- Allow traffic by **label** (e.g. `app=db`)
- Apply per-namespace **egress restrictions**
- Use `kube-dns` and `external access` selectively
- Keep a policy catalog for each service/environment combo (e.g. `auth → db` but not `auth → redis`)

---

## 🚫 Best Practices: Admission Control

| Method | Description | Use Case |
|--------|-------------|----------|
| ✅ **PodSecurity Standards (PSS)** | Built-in to K8s 1.25+ | Block privileged, root, `hostNetwork`, etc. |
| ✅ **OPA Gatekeeper** | Rego-based policies | Custom logic: enforce labels, owners, envs |
| ✅ **Kyverno** | Kubernetes-native YAML policies | Easy to use, supports mutation + generation |
| ✅ **ValidatingWebhookConfiguration** | Advanced, run your own webhook | Last resort for org-wide control |

---

## 🔁 Real DevSecOps Lifecycle Alignment

| Phase | Security Control |
|-------|------------------|
| **Plan** | Define RBAC roles and namespace boundaries in Git |
| **Develop** | Use kustomize overlays per environment (dev/staging/prod) |
| **Build** | Validate manifests with `kubeconform`, `kubescape`, or `OPA` |
| **Deploy** | Admission controllers block unsafe workloads |
| **Run** | NetworkPolicies prevent lateral movement |
| **Monitor** | Audit logs show denied access and rejected API calls |

---

## 🧰 Tools You Should Know

| Tool | Use |
|------|-----|
| `kubectl auth can-i` | Check if a user or SA has access |
| `kubescape`, `kubeaudit` | Scan cluster for security misconfigurations |
| `OPA + Gatekeeper` | Write and enforce admission policies |
| `Kyverno` | Enforce policies like "no image tag `latest`" |
| `Auditd`, `Falco`, `KubeArmor` | Detect runtime violations (covered in Week 14) |

---

## 🔒 How This Enables Zero Trust in Kubernetes

| Zero Trust Principle | Kubernetes Implementation |
|----------------------|---------------------------|
| 🧍 Never trust a user by default | Enforce RBAC on users/groups |
| 🤖 Never trust a workload by default | Use ServiceAccounts + admission controls |
| 🌐 Never trust network by default | Apply NetworkPolicies and default-deny |
| 🧪 Always verify everything | Use policy-as-code (OPA/Kyverno), mutate & validate |
| 📡 Audit everything | Enable API audit logging and monitor access patterns |

---

## ✅ Summary

This week taught you how to:

✅ Secure namespaces with **scoped RBAC**  
✅ Deploy microservices using **non-root, limited ServiceAccounts**  
✅ Restrict **network communication** to intended services  
✅ Detect and block **misconfigured workloads**  
✅ Integrate **Zero Trust** principles directly into Kubernetes

---

Up next:  
➡️ [`Week11/Reflection.md`](./Reflection.md)  
Where we reflect on design trade-offs, troubleshooting challenges, and readiness for production.

Let me know when you're ready to proceed to:

🧠 Week11/Reflection.md
We'll discuss what worked, what could go wrong in a real-world setup, and how to apply this week’s lessons to an enterprise environment.

You said:
Ready 
ChatGPT said:
Excellent — let’s wrap up Week 11 with a reflection that ties together the hands-on work, security thinking, and operational impact. This will prepare you for future modules like Policy-as-Code and Runtime Security.