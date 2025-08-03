# ⚔️ Week 17 – Challenge Lab: Zero Trust Policy Debugging

---

## 🎯 Objective

Your goal is to identify and resolve **intentional violations of Zero Trust** principles in both ECS and Kubernetes environments.

---

## 🧪 Scenario Overview

Your platform team receives alerts and unexpected logs:

1. 🚨 **Dev backend is making unauthorized calls to itself**
2. 🚨 **Search service in `dev` is calling `auth` in `staging`**
3. 🚨 **Frontend in `dev` can't reach `auth`, even though it should**

You must fix these problems without breaking Zero Trust.

---

## 🧩 Part 1 – ECS Fargate Zero Trust Challenge

### 🛠 Reproduce the Problem

Deploy `backend` service with misconfigured Service Connect:

```json
"services": [
  {
    "portName": "http",
    "discoveryName": "backend",
    "clientAliases": [{ "port": 80 }]
  }
]
❌ This allows the backend to talk to itself, breaking Zero Trust.

✅ Fix
Remove the clientAliases field from backend’s Service Connect config

Deny backend's IAM role from discovering backend.notesapp.local

{
  "Effect": "Deny",
  "Action": "servicediscovery:DiscoverInstances",
  "Resource": "arn:aws:servicediscovery:service/backend.notesapp.local"
}
🔎 Misrouted Cross-Env Call
search.dev tries to talk to auth.staging, which breaks environment isolation.

Fix this by enforcing cross-env DNS control and IAM:

Ensure only staging IAM roles can resolve auth.staging.notesapp.local

Set Service Connect namespace per environment, with DNS not resolving across them

{
  "Effect": "Deny",
  "Action": "servicediscovery:DiscoverInstances",
  "Condition": {
    "StringNotEquals": {
      "servicediscovery:NamespaceName": "dev.notesapp.local"
    }
  }
}
🧩 Part 2 – Kubernetes Zero Trust Challenge
🧪 Problem 1: Self-call
Backend pod is trying to call itself over the network.

Test this:

kubectl exec -n dev backend-pod -- curl http://backend:3000/internal
❌ Call succeeds — violating Zero Trust.

✅ Fix
Apply this deny self-ingress policy:

kind: NetworkPolicy
metadata:
  name: deny-self-calls
  namespace: dev
spec:
  podSelector:
    matchLabels:
      app: backend
  ingress:
    - from:
        - podSelector:
            matchExpressions:
              - key: app
                operator: NotIn
                values:
                  - backend
🧪 Problem 2: Cross-namespace call from dev to staging
kubectl exec -n dev search-pod -- curl http://auth.staging.svc.cluster.local:3000/
❌ Call succeeds unless blocked.

✅ Fix
Apply NetworkPolicy in staging to deny ingress from dev

Use strict namespace selectors:

- from:
    - namespaceSelector:
        matchLabels:
          name: staging
Then label your namespaces:

kubectl label ns staging name=staging
kubectl label ns dev name=dev
🧪 Problem 3: Frontend can't reach auth (should be allowed)
Fix: Likely missing a NetworkPolicy or incorrect label

Verify frontend → auth is explicitly allowed

Ensure pod labels match exactly (case-sensitive!)

podSelector:
  matchLabels:
    app: auth
🧠 Real-World Debugging
Symptom	Fix
Allowed calls when they shouldn't be	Check IAM roles or NetworkPolicy missing
Denied calls when they should be	Labels may be misconfigured
Cross-env calls working	Wrong DNS or namespace scoping
Traffic still flowing after deny-all	Sidecar bypass, wrong selector, or old pods
✅ Completion Checklist
✅	Task
Blocked backend self-calls in ECS and K8s	
Enforced DNS and IAM boundaries per namespace	
Denied dev → staging service calls	
Allowed frontend → auth calls correctly	
Verified logs for success/failure states	
Documented policy changes in Git (bonus)	
📦 Bonus
Deploy a new versioned service (e.g. search:v2) in staging
Then allow dev backend to only talk to search:v2 via service alias

ECS: use discoveryName: search-v2

K8s: use label-based selector + DNS override


---

Let me know when you're ready to continue with:

- `Security.md` – The deep dive into Zero Trust theory in DevSecOps
- or directly to `Reflection.md` for end-of-week wrap-up

We’re now enforcing **segmentation, identity, and traffic control** — major enterprise skill set.
You said:
Ready 
ChatGPT said:
Great — here’s your detailed DevSecOps theory and security insight for Week 17, focused on Zero Trust in ECS and Kubernetes.