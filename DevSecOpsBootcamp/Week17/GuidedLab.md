# 🛠️ Week 17 – Guided Lab: Implementing Zero Trust in ECS + Kubernetes

---

## 🎯 Goal

Enforce Zero Trust by controlling service-to-service traffic using:

- **Service Connect + IAM Roles (ECS)**
- **NetworkPolicies + Service Accounts (Kubernetes)**
- Environment isolation (dev, staging, prod)
- Identity-aware access with least privilege

---

## 🧪 Part 1 – ECS Fargate Zero Trust Implementation

---

### 🔧 Step 1: Setup Service Connect Namespace

```bash
aws servicediscovery create-http-namespace \
  --name dev.notesapp.local \
  --description "Dev namespace for Service Connect"
🧠 Why? Namespaces define isolated DNS/service networks — Zero Trust begins with clear boundaries.

⚙️ Step 2: ECS Task Definitions with IAM Role
IAM Role:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ssm:GetParameters",
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:REGION:ACCOUNT_ID:secret:notesapp/*"
    }
  ]
}
✅ This ensures each service only accesses its own secrets.

Attach this IAM role to each service’s task definition:

"taskRoleArn": "arn:aws:iam::ACCOUNT_ID:role/notesapp-auth-role",
🔌 Step 3: Enable Service Connect
In the ECS service definition:

"serviceConnectConfiguration": {
  "enabled": true,
  "namespace": "dev.notesapp.local",
  "services": [
    {
      "portName": "http",
      "discoveryName": "auth",
      "clientAliases": [{ "port": 80 }]
    }
  ]
}
This allows frontend to talk to auth.notesapp.local via Service Connect proxy.

🧠 Service Connect enforces traffic policies by routing through a sidecar proxy, not raw IPs.

🔐 Step 4: Restrict Communication
In the frontend task role, allow only auth:

{
  "Effect": "Allow",
  "Action": "servicediscovery:DiscoverInstances",
  "Resource": "arn:aws:servicediscovery:namespace/dev.notesapp.local"
}
Then explicitly block calls like backend → backend by omitting aliases and IAM permissions.

🧪 Part 2 – Kubernetes Zero Trust Implementation
📦 Step 1: Namespace Isolation
kubectl create ns dev
kubectl create ns staging
Each namespace = an environment with separate RBAC, secrets, and network policies.

🔐 Step 2: Service Accounts per Service
kubectl create serviceaccount auth-sa -n dev
kubectl create serviceaccount frontend-sa -n dev
Add to your Deployment:

spec:
  template:
    spec:
      serviceAccountName: auth-sa
This service identity is used for RBAC, secret access, and traffic controls.

📡 Step 3: NetworkPolicies
Start with deny-all:

kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: dev
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
Then explicitly allow frontend → auth:

kind: NetworkPolicy
metadata:
  name: allow-frontend-to-auth
  namespace: dev
spec:
  podSelector:
    matchLabels:
      app: auth
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
🔐 No other service can now access auth unless explicitly permitted.

💼 Step 4: Restrict Secrets Access
Use RBAC to limit secrets access:

kind: Role
metadata:
  name: auth-secrets
  namespace: dev
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["auth-secret"]
    verbs: ["get"]
Bind it to auth-sa only:

kubectl create rolebinding auth-secret-bind \
  --role=auth-secrets \
  --serviceaccount=dev:auth-sa \
  -n dev
📊 Step 5: Confirm Isolation
Try these tests:

Scenario	Expected
frontend → auth	✅ Allowed
backend → backend	❌ Denied
dev → staging search:v2	✅ Allowed (only if permitted in policy)
dev frontend → prod auth	❌ Blocked (cross-namespace)
✅ Completion Checklist
✅	Task
🧱 Namespaces created per environment	
🔐 IAM roles / ServiceAccounts per service	
⚙️ Service Connect enabled and isolated	
📡 NetworkPolicies applied (K8s)	
🔒 Secrets scoped by identity	
🔎 Traffic tested and denied/allowed appropriately	
🧠 Key Learnings
Zero Trust enforces identity + policy, not just network location

Service-to-service auth is enforceable with IAM, mTLS, and proxy layers

Kubernetes and ECS can both achieve fine-grained segmentation

Every environment, service, and secret should be scoped and verified


---

Let me know when you're ready to proceed with the `ChallengeLab.md`, which simulates **Zero Trust failures** and forces you to trace, debug, and fix the policy or IAM gap.

This will really cement the “trust nothing” mindset.
You said:
Proceed 
ChatGPT said:
Perfect — let’s move forward with the Week 17 Challenge Lab, where you’ll intentionally break Zero Trust boundaries and fix them using IAM policies, NetworkPolicies, and identity scopes. This hands-on debugging reinforces real-world troubleshooting and threat modeling.