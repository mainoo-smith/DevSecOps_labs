# 📅 Week 6 — Containers & Docker (Beginner → Advanced)

## 🎯 What You'll Learn

- Understand what containers are, why they matter, and how they differ from VMs.
- Build, run, and share Docker images.
- Use Dockerfiles with best practices for security and efficiency.
- Work with Docker Compose for local multi-service dev.
- Push/pull images to/from Docker Hub or a private registry.
- **Advanced**:
  - Multi-stage builds for small secure images.
  - Scan images for vulnerabilities.
  - Sign and verify container images.
  - Manage secrets in containers.
  - Optimize for production-ready images.

---

## 🔍 5W1H

- **Who**: Developers, DevOps, SREs — anyone shipping software in modern stacks.
- **What**: Containers package apps & dependencies into lightweight, portable units.
- **When**: Any time you want consistent environments from dev → prod.
- **Where**: Locally, on CI/CD runners, on orchestrators like Kubernetes.
- **Why**: Eliminate “works on my machine” problems; enable scaling and repeatability.
- **How**: Build → test → scan → sign → push → run.

---

## 🏗️ Real Project Context

You’re containerizing your microservice (from Week 4) and deploying it on the secure cloud infra you provisioned in Week 5.  
These images will run in Kubernetes next week!

---

## 🗝️ Analogy

Containers are like **shipping containers**:
- App + dependencies = goods inside.
- Container runtime = cargo ship/truck.
- Orchestrator = the port managing traffic.
- Signing = customs seal verifying contents haven’t been tampered with.

---

## ✅ Outcomes

- Build a secure, multi-stage Docker image.
- Run & test your container locally.
- Use Compose for a dev environment.
- Scan, sign, and push images to a registry.

# 📅 Week 6 — Containers & Cloud Registries Extended 

## 🎯 What You'll Learn

- Build real container images for microservices.
- Use Dockerfiles with multi-stage builds.
- Push images securely to **AWS ECR** (or GCP/ACR).
- Pull and run your images in dev/staging.
- Work with Docker Compose for local orchestration.
- Sign & scan images for supply chain security.
- Use real tagging & versioning strategies.
