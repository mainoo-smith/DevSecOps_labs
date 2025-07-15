# 📅 Week 7 — Kubernetes Basics (Beginner → Advanced)

## 🎯 What You'll Learn

- Understand what Kubernetes is and why it’s the standard for orchestration.
- Spin up a local dev cluster with `kind` or `minikube` (or use EKS, GKE).
- Deploy and manage Pods, Deployments, Services.
- Learn real troubleshooting with `kubectl`.
- **Advanced**:
  - Use ConfigMaps and Secrets securely.
  - Implement health checks and readiness probes.
  - Scale deployments with HPA (Horizontal Pod Autoscaler).
  - Work with Namespaces and RBAC.
  - Intro to GitOps and multi-cluster basics.

---

## 🔍 5W1H

- **Who**: DevOps, SREs, Platform Engineers — anyone deploying containers at scale.
- **What**: Kubernetes orchestrates containers for high availability, scaling, and recovery.
- **When**: When you need your app to run reliably across nodes.
- **Where**: Local cluster → cloud-managed K8s → multi-cluster.
- **Why**: Manual container ops don’t scale — orchestration is your new best friend.
- **How**: Use `kubectl`, YAML manifests, Helm, and GitOps best practices.

---

## 🏗️ Real Project Context

This week you’ll deploy your **signed container image** from Week 6 into a real cluster:
- Use local dev cluster now, then EKS/GKE in production.
- Next: you’ll hook this up to your CI/CD pipeline for automated rollouts.

---

## 🗝️ Analogy

Think of Kubernetes like an air traffic control system:
- Pods = airplanes  
- Nodes = runways  
- Services = gates for passengers  
- Controller Manager = air traffic controller ensuring no crashes.

---

## ✅ Outcomes

- Local cluster up & running.
- Secure Pod & Deployment manifests.
- Expose services with proper networking.
- Use ConfigMaps, Secrets, probes, and autoscaling.
