# Week 01: DevOps Foundations + Git Fundamentals

## 🧠 What You’ll Learn
- What DevOps *really* means beyond buzzwords
- How software delivery has evolved (Waterfall → Agile → DevOps → GitOps)
- Git basics: repo, clone, commit, push, branch, merge, rebase
- Git collaboration: pull requests, branch protection
- Introduction to the real project we’ll build throughout the program

## 🔍 5W1H of DevOps

| Prompt | Answer |
|--------|--------|
| **What** | A culture + practices + tools to deliver software faster, safer, and more reliably |
| **Why**  | Traditional dev & ops handoffs caused long lead times, failures, and blame |
| **Who**  | Devs, Ops, SREs, QA, Security — working together instead of in silos |
| **When**| When you need to ship frequently, respond to change fast, and scale sustainably |
| **Where**| From startup CI/CD pipelines to Fortune 500 infra platforms |
| **How** | Automate all stages of software lifecycle using shared codebases, pipelines, monitoring, and collaboration |

## 📦 Real-World Analogy

> DevOps is like building **a Formula 1 pit crew**:
> - Dev = driver (writes the app)
> - Ops = pit crew (keeps the car running safely)
> - QA = sensors (quality checks)
> - Security = race rules (enforcement)
> All must work in sync. **Any lag = lost race.**

## 💡 Why Git?

Git is the **foundation of everything** we’ll build. Every change to your infrastructure, code, and even Kubernetes manifests will live in Git — enabling collaboration, versioning, and rollback.

---

## 🏗️ This Week’s Project Kickoff

We’ll create a base repo for our eCommerce platform with these folders:

ecommerce-platform/
├── frontend/ # React-based UI
├── backend-api/ # NodeJS/Flask REST API
├── auth-service/ # JWT auth microservice
├── db/ # PostgreSQL config
└── .github/ # Actions will go here later


You’ll practice:
- Creating branches per service
- Making commits, pull requests
- Enabling branch protection
- Merging changes safely
