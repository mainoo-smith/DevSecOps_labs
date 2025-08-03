# 🔐 Week 17 – Security: Zero Trust in ECS + Kubernetes

---

## 🎯 Why This Matters

Zero Trust security challenges the old model of “trusted internal networks” by assuming **everything is compromised** — including workloads inside your VPC or cluster.

In DevSecOps, this means:

- Enforcing **identity at every layer**
- Allowing only explicitly permitted traffic
- Treating every request as potentially malicious — even internally
- Monitoring and logging everything for traceability

---

## 🔍 Core Zero Trust Principles

| Principle | DevSecOps Implementation |
|----------|--------------------------|
| **Never trust, always verify** | mTLS, IAM role checks, DNS identity validation |
| **Least privilege** | Per-service IAM roles, namespace secrets, RBAC |
| **Explicit access only** | NetworkPolicies, deny-all by default |
| **Assume breach** | Logging, anomaly detection, minimal attack surface |
| **Microsegmentation** | Namespaces, service-specific identity, isolated DNS routing |

---

## 🧠 Identity-Driven Access in ECS

- **IAM Roles for Tasks**: Each ECS service has its own IAM role.
- **Service Connect**: Every request is routed through a proxy that can enforce **namespace isolation** and **client aliasing**.
- **DNS Routing**: Controls which services are discoverable via `*.notesapp.local`.

✅ This builds a verifiable identity chain for every request.

---

## 🧠 Identity-Driven Access in Kubernetes

- **Service Accounts**: Each workload has its own K8s identity.
- **RBAC**: Fine-grained permissions to configmaps, secrets, APIs.
- **NetworkPolicies**: Restrict traffic based on pod labels and namespaces.
- **Mutual TLS** (optional via Istio/Linkerd): Enforces identity at transport layer.

✅ Zero Trust is enforced at **network**, **API**, and **identity** layers.

---

## 🔐 Risks You’re Mitigating

| Risk | Example | Zero Trust Control |
|------|---------|--------------------|
| Lateral movement | One service compromised, others infected | NetworkPolicies, IAM isolation |
| Secrets sprawl | One container reads all secrets | Scoped secret access (Vault/K8s) |
| Misrouted traffic | Dev service calls staging/production | Namespace isolation, IAM discovery limits |
| Impersonation | No service identity, all share one token | Per-service IAM/SA with short-lived credentials |
| Over-privilege | Services can access unused APIs | Least privilege via roles and deny-by-default |

---

## 🧠 Threat Modeling View

| Attack | Impact | Zero Trust Response |
|--------|--------|---------------------|
| Compromised backend queries itself to extract internal data | Full access to internal methods | Deny self-calls via policies |
| Dev frontend queries staging secrets | Cross-env leak | Isolate namespaces + block IAM discovery |
| Rogue staging service calls prod | Potential data exfiltration | Explicit namespace trust boundaries |

---

## 🛠 Key Enforcement Techniques

| Platform | Enforcement | Notes |
|----------|-------------|-------|
| ECS | IAM roles, Service Connect, DNS isolation | Identity-aware service-to-service access |
| Kubernetes | NetworkPolicies, Service Accounts, RBAC | Pod-level control over ingress/egress |
| Optional Add-ons | Istio, Linkerd, SPIRE | Stronger identity and transport-level control |

---

## 📊 Visibility & Monitoring

Zero Trust is only effective if visibility exists:

- **ECS VPC Flow Logs + CloudWatch Logs**
- **Kubernetes Audit Logs + Prometheus Metrics**
- **OpenTelemetry tracing for service-to-service calls**
- **GuardDuty for anomalous traffic**
- **Falco for unexpected process activity**

> 🎯 Observability is part of the Zero Trust loop: **authenticate ➝ authorize ➝ audit.**

---

## 📘 DevSecOps Mindset Shift

| Old Model | Zero Trust Model |
|-----------|------------------|
| Flat network = trusted | Every boundary must be earned and validated |
| Secrets shared across services | Each workload gets scoped identity and credentials |
| Manual allow lists | Policy-as-code governs traffic and access dynamically |
| Trust by subnet | Trust by identity, enforced by proxy and IAM |

---

## 🏁 What You’ve Gained

You can now:

✅ Enforce service isolation in ECS and Kubernetes  
✅ Apply least privilege access to IAM roles and service accounts  
✅ Implement namespace boundaries to prevent cross-env access  
✅ Monitor and debug misrouted or unauthorized service calls  
✅ Align workload infrastructure with **Zero Trust best practices**

---

## 🧱 App Evolution Summary

| Layer | Upgrade |
|-------|---------|
| 🧠 Identity | IAM Roles for ECS, Service Accounts for K8s |
| 🌐 Traffic | Service Connect & K8s NetworkPolicies |
| 🔒 Secrets | Environment-scoped + identity-scoped access |
| 🧪 Test Cases | Cross-env traffic, self-call prevention, isolation verified |
| 📦 Version Routing | dev → staging:search:v2 (selectively allowed) |

Let me know when you're ready to finish Week 17 with Reflection.md, or we can jump into Week 18: Red Team vs Blue Team Scenarios, where you’ll test your defenses with offensive security tooling.

You said:
Ready 
ChatGPT said:
Awesome — let’s wrap up Week 17: Zero Trust in ECS + Kubernetes with our end-of-week retrospective.