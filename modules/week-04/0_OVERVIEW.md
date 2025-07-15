# 📅 Week 4 — Build & Package Management

## 🎯 What You'll Learn

- Core build concepts: compile, test, package.
- Use Maven (Java), npm (Node.js), or Gradle to automate builds.
- Push artifacts to a repository (Nexus, Artifactory, or AWS CodeArtifact).
- **Advanced**:
  - Multi-stage builds (Docker context)
  - Build caching for faster pipelines
  - Signed artifacts & promotion workflows
  - Build scanning for supply chain security

---

## 🔍 5W1H

- **Who**: Developers, DevOps engineers, Release Managers.
- **What**: Builds convert source to tested, versioned, shareable artifacts.
- **When**: Every time you release or deploy.
- **Where**: Local, CI/CD runners, containers.
- **Why**: Reproducibility, rollback, collaboration.
- **How**: Automate with build tools, sign artifacts, push to secure repos.

---

## 🗝️ Analogy

A build tool is like a chef — you give raw ingredients (code) → chef follows a recipe → you get a repeatable dish (artifact).  
A signed artifact is like a sealed food package: tamper-evident and trustworthy.

---

## 🏗️ Real Project Context

**Scenario:**  
You’re building a 3-tier microservice app:  
- Backend API (Java or Node.js)
- Frontend (React, npm)
- All built, versioned, and pushed to Nexus.

Your CI/CD pipeline will pull these signed artifacts to build Docker images in the next weeks.

---

## ✅ Outcomes

By the end of this week:
- Build, test, and package a real component of your microservice.
- Push versioned artifacts to a repo.
- Use checksums & signing for supply chain security.
- Document build & promotion workflow for your pipeline.
