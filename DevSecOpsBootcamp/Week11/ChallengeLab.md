# 🧪 Challenge Lab – Simulating a Breach & Blocking Privilege Escalation in Kubernetes

---

## 🎯 Objective

Simulate a real-world insecure deployment and **harden your cluster** to defend against it by:

- Deploying a pod with dangerous configurations
- Detecting misconfigurations using tools or review
- Enforcing prevention using native and custom policies

---

## 🧩 Scenario

A junior engineer accidentally deploys a version of the `auth-service` with:

- `runAsRoot: true`
- `hostNetwork: true`
- Open network access
- No RBAC protections

As a DevSecOps engineer, you must:

1. Identify this insecure workload
2. Patch the deployment with security context
3. Apply **admission rules or network policy** to block such behavior in the future

---

## 1️⃣ Deploy an Insecure Auth Pod (Simulated Breach)

📁 `insecure-auth.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: insecure-auth
  namespace: auth-dev
spec:
  replicas: 1
  selector:
    matchLabels:
      app: insecure-auth
  template:
    metadata:
      labels:
        app: insecure-auth
    spec:
      hostNetwork: true
      containers:
      - name: auth
        image: your-dockerhub-user/auth-service:latest
        ports:
        - containerPort: 3000
        securityContext:
          runAsUser: 0  # 👎 Runs as root
          privileged: true
kubectl apply -f insecure-auth.yaml
☠️ This deployment is insecure and simulates a real mistake or breach opportunity.

2️⃣ Review the Security Risks
Use tools like:

kubectl describe deployment insecure-auth -n auth-dev

kubescape scan framework nsa (requires installing kubescape)

Manual review: check for hostNetwork, runAsUser: 0, privileged: true

Expected Findings:

Issue	Risk
hostNetwork: true	Container can sniff host traffic
runAsUser: 0	Root user inside pod can escalate
privileged: true	Can access host devices and kernel
No securityContext	Lacks runtime restrictions
No ServiceAccount	May run with cluster-admin
3️⃣ Block the Breach Using Admission Controls
Option A: Native PodSecurity Admission (v1.25+)
kubectl label namespace auth-dev pod-security=restricted
This applies PodSecurity Standards to prevent privileged containers.

Option B: Gatekeeper with ConstraintTemplate (Preview)
Requires Open Policy Agent + Gatekeeper installed

📁 privileged-blocker.yaml

apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sPSPPrivilegedContainer
metadata:
  name: disallow-privileged-containers
spec:
  match:
    namespaces:
      - auth-dev
🔐 This rejects any pod that tries to run with privileged: true.

4️⃣ Apply a Fallback NetworkPolicy
📁 default-deny-egress.yaml

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-egress
  namespace: auth-dev
spec:
  podSelector: {}
  policyTypes:
    - Egress
This blocks all outgoing traffic from pods in auth-dev. You can add explicit rules to allow auth → db, etc.

5️⃣ Cleanup & Re-Deploy Secure Version
kubectl delete deployment insecure-auth -n auth-dev
Re-deploy auth-service using:

runAsNonRoot: true

hostNetwork: false

allowPrivilegeEscalation: false

Proper ServiceAccount

Applied NetworkPolicy

✅ Completion Checklist
Task	✅
Simulated insecure deployment with root access	✅
Identified risks using CLI or tools	✅
Blocked privileged pod using policy	✅
Applied default-deny network policy	✅
Re-deployed secured auth-service	✅
🧠 Bonus Challenge (Optional)
Use OPA Gatekeeper to enforce:

Every pod must define runAsNonRoot: true

Labels like env=dev must be present

Use kubescape to get a score of your namespace

Enable audit logging for rejected API requests


---

Let me know when you're ready to move on to:

### 🔐 `Week11/Security.md`  
Where we’ll cover deeper policy enforcement patterns, practical DevSecOps enforcement boundaries, and a real-world comparison of Zero Trust controls in Kubernetes.
You said:
Ready 
ChatGPT said:
Perfect. Let’s go deeper with Week 11 Security Concepts — this is where we connect the lab implementation to real-world DevSecOps practices, enforcement strategies, and best-in-class security posture for Kubernetes.