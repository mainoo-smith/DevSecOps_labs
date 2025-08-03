# 🧪 Guided Lab – Kubernetes Security I: RBAC, NetworkPolicies, and Namespace Isolation

---

## 🧭 Objective

Deploy the `auth-service` microservice into a **secure namespace (`auth-dev`)** with:

- 📛 Namespace-level isolation
- 🔐 RBAC permissions for DevSecOps engineers
- 🪪 Dedicated ServiceAccount with scoped permissions
- 🌐 NetworkPolicy limiting pod communication
- ❌ Admission rejection if resources are insecure

---

## 🛠️ Prerequisites

- `kubectl` and access to a cluster (Minikube, EKS, etc.)
- `kustomize` installed
- Sample Node.js `auth-service` container image (we'll use a placeholder)
- Cluster context set via `kubectl config use-context your-cluster`

---

## 1️⃣ Create a Secure Namespace

```bash
kubectl create namespace auth-dev
Optional: Annotate Namespace for OPA/Gatekeeper
kubectl annotate namespace auth-dev owner=devsecops-team
2️⃣ Define RBAC: Role + RoleBinding
📁 rbac/auth-role.yaml

apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: auth-dev
  name: auth-deployer
rules:
- apiGroups: ["", "apps"]
  resources: ["pods", "services", "deployments"]
  verbs: ["get", "list", "watch", "create", "update", "delete"]
📁 rbac/auth-rolebinding.yaml

apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: bind-auth-deployer
  namespace: auth-dev
subjects:
- kind: User
  name: devsecops-engineer
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: auth-deployer
  apiGroup: rbac.authorization.k8s.io
🛡️ Note: You can replace User with Group or ServiceAccount depending on your cluster auth method (OIDC, etc.).

3️⃣ Create a Scoped ServiceAccount
📁 auth-serviceaccount.yaml

apiVersion: v1
kind: ServiceAccount
metadata:
  name: auth-service-sa
  namespace: auth-dev
4️⃣ Deploy the Auth Service (Scoped)
📁 auth-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
  namespace: auth-dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: auth
  template:
    metadata:
      labels:
        app: auth
    spec:
      serviceAccountName: auth-service-sa
      containers:
      - name: auth
        image: your-dockerhub-user/auth-service:latest
        ports:
        - containerPort: 3000
        securityContext:
          runAsNonRoot: true
          allowPrivilegeEscalation: false
📁 auth-service.yaml

apiVersion: v1
kind: Service
metadata:
  name: auth-service
  namespace: auth-dev
spec:
  selector:
    app: auth
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
5️⃣ Apply a NetworkPolicy
📁 auth-networkpolicy.yaml

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: auth-deny-all-except-db
  namespace: auth-dev
spec:
  podSelector:
    matchLabels:
      app: auth
  policyTypes:
    - Ingress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: db
🔒 This ensures only the db service can talk to auth-service.

6️⃣ Test Misconfigured Access (Optional)
Try to create a pod as a regular user or without ServiceAccount:

kubectl run debugpod --image=alpine -n auth-dev --command -- sleep 3600
Expected result: ❌ Fails if RBAC is applied properly and admission controllers block unsafe pods (depending on your policy config).

✅ Completion Checklist
Task	Complete
Created isolated namespace for auth-service	✅
Scoped RBAC role and bound to DevSecOps user	✅
Created secure ServiceAccount for app	✅
Deployed app using ServiceAccount with securityContext	✅
Enforced traffic restrictions with NetworkPolicy	✅
Blocked unsafe workloads (via policy or admission)	✅
🧠 Quick Recap
Resource	Purpose
Namespace	Segments and scopes resources for security
Role / RoleBinding	Controls who can act in namespace
ServiceAccount	Assigns pod-level identity
NetworkPolicy	Controls ingress/egress at network level
SecurityContext	Ensures non-root containers, least privileges

---

Let me know if you’re ready to proceed to:

### 🧩 `Week11/ChallengeLab.md`  
It will simulate a breach scenario and make you write policies to block escalation paths.

Or let me know if you'd like to pause and explore a concept further.
You said:
Proceed 
ChatGPT said:
Perfect. Let’s move into the Challenge Lab for Week 11, where you’ll secure the Kubernetes environment further by simulating misconfigurations and enforcing defenses.