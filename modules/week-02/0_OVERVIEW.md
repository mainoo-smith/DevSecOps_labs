# Week 02: Linux, SSH, and Secure Remote Access

## 🧠 What You’ll Learn

- Core Linux administration (users, permissions, packages)
- Securely connecting to remote cloud servers via SSH
- Hardening Linux servers against brute-force and bad practices
- The foundational security work needed before we automate provisioning with Ansible or Terraform

---

## 📦 Real-World Project Scenario

> 🛠️ Your team just provisioned its first AWS EC2 instance (via Terraform or console). This host will act as your **deployment jumpbox** or internal utility server for now. In the coming weeks, it may:
>
> - Serve as a bastion host to access private networks
> - Run background jobs like backup, log sync, patching
> - Be used for Ansible provisioning
> - Host temporary staging apps (frontend/backend)

Before this server can safely be used, it must be **secured, hardened, and monitored**. This is the task for this week.

---

## 🔍 5W1H of Linux + SSH

| Prompt | Answer |
|--------|--------|
| **What** | Linux is the operating system for most cloud servers; SSH is the encrypted protocol to access them |
| **Why** | You must be able to provision, monitor, or troubleshoot environments remotely and securely |
| **Who** | DevOps, Platform Engineers, Sysadmins, SREs |
| **When** | Before configuring CI/CD runners, K8s nodes, or any cloud infra |
| **Where** | In AWS EC2, local VM, EKS node pools, or bare-metal |
| **How** | Securely via SSH keys, hardened users, firewalls, log monitoring, and package updates |

---

## 🔧 Analogy

> Think of this EC2 server like your **first delivery van** for the company. You must:
> - Install a GPS (monitoring)
> - Lock the doors (firewall)
> - Disable master keys (no root login)
> - Assign a responsible driver (create devops user)
> - Keep it fueled and safe (patches and fail2ban)

---

## 📗 Learning Outcome

By the end of this week:
- You’ll be able to securely access and administer cloud servers
- You’ll prepare the foundation to automate this via config mgmt
- You’ll start thinking like a systems operator with security in mind


# Week 02: Linux Essentials, SSH, and Secure Remote Access (App-Aware)

## 🧠 What You’ll Learn

- How to securely configure a Linux server to support real deployments
- SSH key-based access for DevOps pipelines
- Creating user roles and hardening server access
- Writing system health scripts tailored for running microservices

---

## 📦 Real-World Project Scenario

You're working on the `backend-api` microservice for your cloud-native eCommerce platform.

This week’s goal is to:
- Provision and harden an EC2 instance where `backend-api` will be deployed for staging.
- Create a `devops` user that GitHub Actions or Ansible can later use for deployment.
- Write a `health-check.sh` script that reports CPU, memory, and the service status of `backend-api`.

---

## 🔍 5W1H of Linux + SSH

| Prompt | Answer |
|--------|--------|
| **What** | Secure the infrastructure for app deployment |
| **Why** | All DevOps pipelines and tools must connect and deploy securely |
| **Who** | DevOps engineers, platform engineers, CI/CD tools |
| **When** | Initial staging deployment, automation setup, pre-production |
| **Where** | AWS EC2 server running Ubuntu 22.04 or Amazon Linux 2 |
| **How** | Secure shell, firewalls, hardening, health checks

---

## 🔧 Analogy

> Think of this instance like your company’s **warehouse staging area**: before anything goes to production, it gets stored, inspected, and verified here. You must secure the warehouse, control who can enter, and ensure it has basic fire safety and power checks — just like monitoring memory, CPU, and service uptime.