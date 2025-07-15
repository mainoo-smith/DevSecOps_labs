# 📅 Week 5 — Cloud & Infrastructure Basics (Beginner → Advanced)

## 🎯 What You'll Learn

- Understand cloud fundamentals: IaaS, PaaS, SaaS, regions, AZs, pricing.
- Launch and secure your first VM in the cloud (AWS EC2).
- Master basics of networking: VPCs, subnets, route tables, security groups.
- Apply IAM best practices: users, roles, policies, least privilege.
- **Advanced**:
  - Design multi-tier architectures (public/private subnets).
  - Use Bastion hosts & jump boxes.
  - Automate provisioning with launch templates and CLI tools.
  - Start using Infrastructure as Code (Terraform intro).
  - Plan for multi-cloud or disaster recovery basics.
  - Apply tagging & cost management practices.

---

## 🔍 5W1H

- **Who**: DevOps, Cloud Engineers, SREs, Security Engineers.
- **What**: Provision, secure, and manage cloud compute/network resources.
- **When**: Every time you deploy an app, scale, or patch infra.
- **Where**: AWS, Azure, GCP — core concepts transfer across clouds.
- **Why**: 90% of breaches come from misconfigured cloud infra.
- **How**: Manual first → then automate.

---

## 🏗️ Real Project Context

You’re setting up **the cloud environment that will run your containerized microservices stack**.  
- This week: Build your base VPC, EC2 instances, and secure SSH access.
- Later: You’ll add containers, EKS, and CI/CD pipelines that deploy into this infra.
- By the end: You’ll have reusable Terraform scripts to spin up prod/staging in minutes.

---

## 🗝️ Analogy

Think of your cloud infra like a **gated neighborhood**:
- VPC = the neighborhood boundary  
- Subnets = streets  
- Security groups = fences around each house  
- Bastion host = security guardhouse for visitors  
- IAM = the master key system for who can unlock what.

---

## ✅ Outcomes

- Launch & secure your own cloud server.
- Design a simple VPC with best practices.
- Connect securely using SSH keys & Bastion host.
- Apply least privilege IAM.
- Prepare for infra automation in Week 6.
