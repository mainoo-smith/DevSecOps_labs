# 🔧 Week 11 – Kubernetes Security I: RBAC, Network Policies & Admission Controls

---

## 🎯 Goal

By the end of this module, you'll understand how to **secure access to Kubernetes clusters** using:

- Role-Based Access Control (RBAC)
- Network segmentation using NetworkPolicies
- Admission control using built-in and custom plugins

All within a **real-world microservices application**, as we deploy parts of our evolving app (e.g. `auth-service`) into a **secure Kubernetes namespace**.

---

## 📚 Core DevSecOps Concepts

| Concept | Description |
|--------|-------------|
| 🔐 RBAC | Fine-grained control over **who can do what** in the cluster |
| 🌐 Network Policies | Control **who can talk to whom** over the network |
| 🧩 Admission Controllers | Gate incoming resource requests (e.g. prevent privileged pods) |
| 🔄 Principle of Least Privilege | Only give the permissions needed — no more, no less |
| 🧱 Namespaces & Isolation | Organize resources and isolate environments securely |
| 📜 Service Accounts & Boundaries | Workload identity tied to permissions, not users |

---

## 🧠 Why This Matters

Modern Kubernetes clusters can become **attack surfaces** if:

- RBAC is overly permissive
- Workloads run as root or with `hostNetwork: true`
- Anyone can deploy insecure manifests
- Pods can talk to other services or databases without restriction

This week gives you the **core tools to defend your cluster**, enforce compliance, and practice **Zero Trust principles inside Kubernetes**.

---

## 🧱 How the App Evolves This Week

| Area | Evolution |
|------|-----------|
| Auth Service | Now deployed into Kubernetes with a dedicated namespace (`auth-dev`) |
| RBAC | Only DevSecOps engineers can deploy to this namespace |
| ServiceAccount | Each microservice gets a unique identity |
| NetworkPolicy | `auth-service` can only talk to the `db` service, not other pods |
| Admission | Pod creation is blocked if it lacks labels or tries to run as root |

---

## 🛠️ Tools You'll Use

- `kubectl`, `kustomize`
- `RBAC` YAMLs (Role, RoleBinding, ClusterRole, ServiceAccount)
- `NetworkPolicy`
- `Admission Controllers` (built-in + preview for OPA/Gatekeeper)

Optional (for deeper visibility):
- `k9s`, `kubescape`, `kubewarden`

---

## 📦 Learning Outcomes

✅ Define secure namespaces with scoped permissions  
✅ Apply RBAC roles to users, teams, and service accounts  
✅ Enforce ingress/egress policies using `NetworkPolicy`  
✅ Restrict workload privileges using admission policies  
✅ Build deployable, secure Kubernetes manifests  
✅ Enable auditability and compliance on resource creation  

---

## 🔐 Real-World Use Case

Your org runs multiple environments (dev, staging, prod) in a shared cluster.  
You want:

- Developers to **deploy only into their own namespaces**
- Sensitive services to **only talk to their dependencies**
- A system that **rejects dangerous manifests** (e.g., running as root)

This week sets the foundation for **policy-as-code**, **runtime security**, and **zero trust enforcement** in Kubernetes.

---

## 🔄 Coming Up Next

🔒 Week 12 will continue building on this foundation with:

- ECS Security Best Practices  
- Runtime Isolation  
- Cross-environment policies  
- Secure sidecars and service mesh (if enabled)

---

## ✅ Prerequisites

- Docker Desktop with Kubernetes enabled **OR** access to a K8s cluster (EKS, GKE, or Minikube)
- `kubectl` installed and configured
- Kustomize (for managing manifests)
- Helm (optional but useful later)

---

## 🧪 Next Step

Proceed to [`GuidedLab.md`](./GuidedLab.md) where you'll:

- Create namespaces and RBAC roles
- Deploy the `auth-service` securely
- Apply `NetworkPolicies`
- Simulate a security breach and block it via policy

---
Let me know if you'd like to proceed to:

✅ Week11/GuidedLab.md
It’ll include step-by-step Kubernetes RBAC, secure namespace deployment, and more — with real app evolution.

You said:
Continue 
ChatGPT said:
Great — let’s continue with the Week 11 Guided Lab, formatted in .md and focused on practical Kubernetes security using RBAC, ServiceAccounts, and NetworkPolicies — all tied to your evolving auth-service.