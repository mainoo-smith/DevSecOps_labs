# 🛠 Week 7 Guided Lab — Kubernetes Basics

## 🔍 5W1H: Why This Lab?

- **Who**: You, acting as Platform Engineer running microservices.
- **What**: Deploy containers securely at scale.
- **When**: Every production release.
- **Where**: Local cluster (kind/minikube) or cloud K8s.
- **Why**: Manual containers don’t scale; K8s orchestrates everything.
- **How**: Use `kubectl` & manifests.

---

## 📌 Prerequisites

- Docker Desktop with K8s, `kind` or `minikube` installed.
- Container image pushed to Docker Hub/ECR.

---

## 1️⃣ Create a Cluster

✅ Using `kind`:
```bash
kind create cluster --name dev-cluster
kubectl cluster-info --context kind-dev-cluster

✅ Or minikube:
minikube start
kubectl get nodes

2️⃣ Deploy a Pod & Service
✅ Create deployment.yaml:
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: yourdockerhub/myapp:2.0
        ports:
        - containerPort: 3000

✅ Apply:
kubectl apply -f deployment.yaml
kubectl get pods

✅ Expose with service.yaml:
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  type: NodePort
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 30080

✅ Apply:
kubectl apply -f service.yaml
minikube service myapp-service

3️⃣ Advanced: ConfigMaps & Secrets
✅ Create configmap.yaml:
apiVersion: v1
kind: ConfigMap
metadata:
  name: myapp-config
data:
  APP_ENV: production

✅ Create secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
type: Opaque
data:
  DB_PASSWORD: bXlwYXNzd29yZA==  # echo -n 'mypassword' | base64

✅ Reference in Deployment:
envFrom:
- configMapRef:
    name: myapp-config
- secretRef:
    name: myapp-secret

4️⃣ Health Checks
✅ Add to deployment.yaml:
readinessProbe:
  httpGet:
    path: /
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 10

livenessProbe:
  httpGet:
    path: /
    port: 3000
  initialDelaySeconds: 15
  periodSeconds: 20

5️⃣ Autoscaling
✅ Enable metrics server:
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

✅ Scale:
kubectl autoscale deployment myapp-deployment --cpu-percent=50 --min=2 --max=5
kubectl get hpa

✅ Deliverables
deployment.yaml with ConfigMaps, Secrets, probes.
service.yaml for NodePort.
kubectl screenshots or outputs.