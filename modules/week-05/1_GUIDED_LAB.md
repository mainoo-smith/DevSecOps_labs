# 🛠 Week 5 Guided Lab — Build & Secure Cloud Infra (Beginner → Advanced)

## 🔍 5W1H: Why This Lab?

- **Who**: You, acting as the DevOps/Cloud Engineer.
- **What**: Practice real cloud provisioning — manual first, then plan for automation.
- **When**: Every environment (dev/staging/prod) starts here.
- **Where**: AWS (but skills apply to any cloud).
- **Why**: 70% of cloud breaches = misconfigured infra.
- **How**: Secure-by-design workflow.

---

## 📌 Prerequisites

- AWS Free Tier account.
- SSH key pair.

---

## 1️⃣ Create a Custom VPC

✅ Basic: Use default VPC (beginner)  
✅ Advanced: Create custom VPC.
- CIDR: 10.0.0.0/16
- Public subnet: 10.0.1.0/24
- Private subnet: 10.0.2.0/24
- Internet Gateway & Route Table for public subnet.

---

## 2️⃣ Launch an EC2 Instance

- AMI: Ubuntu 22.04
- Type: t2.micro (Free Tier)
- Key pair: your SSH key
- Security Group: allow SSH (port 22) from your IP only.

✅ Advanced: Launch a Bastion host in the public subnet.

---

## 3️⃣ SSH in Securely

```bash
ssh -i mykey.pem ubuntu@your-ec2-ip
```

✅ Create a non-root user:
```bash
sudo adduser devopsstudent
sudo usermod -aG sudo devopsstudent
```

✅ Set up SSH keys for new user.

✅ Disable root SSH:
```bash
sudo nano /etc/ssh/sshd_config
PermitRootLogin no
```

✅ Change default SSH port (optional advanced).

---

## 4️⃣ IAM Roles & Policies

- Create IAM user for yourself with MFA.
- Create IAM role with least privilege.
- Attach the role to your EC2 for SSM Session Manager access.

---

## 5️⃣ Advanced: Bastion & Private Instances

- Deploy app servers in private subnet.
- SSH → Bastion → Private instance only.
- Try using `ProxyJump` with SSH.

---

## 6️⃣ Intro to IaC (Terraform Starter)

✅ Generate Terraform:
- Create `main.tf` to spin up the same VPC + EC2.
- Validate & apply.

---

## ✅ Deliverables

- `cloud-notes.md` describing VPC, subnet, security group setup.
- Screenshot of SSH access.
- `main.tf` for Terraform if you try it.

---

## 🏗️ Real Project Context

This VPC & EC2 setup will host your CI/CD runners, containers, and app nodes in later weeks.