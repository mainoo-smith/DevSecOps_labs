This is a test module for learning DevSecOps by simulating real-world scenarios using real tools. 
To use this repo, you can fork it, clone it, or create an issue from a PR. 
The project comes with scripts that can be run locally or on any VM.
You can play around with the commands, break things, and fix them to reinforce learning.

✅ Revised Course Plan (Integrated DevOps + DevSecOps Focus)

| Week | Title                                                      | Focus Areas                                                   | DevSecOps Tie-In                                           |
| ---- | ---------------------------------------------------------- | ------------------------------------------------------------- | ---------------------------------------------------------- |
| 1    | 🔍 Linux & OS Fundamentals for DevSecOps                   | Shell, permissions, users, file structure, process management | OS hardening, secure permissions, attack surface           |
| 2    | 🌐 Networking & Firewalls for DevSecOps                    | TCP/IP, ports, DNS, SSH, iptables, proxies                    | Network segmentation, firewall policies, lateral movement  |
| 3    | 🧱 Containers, Docker & Image Basics                       | Docker CLI, layers, image building, volumes                   | Dockerfile security, attack vectors, minimal base images   |
| 4    | 🧠 Git, GitHub, GitLab & Secure Git Workflows              | Git internals, branching, signed commits, GitOps              | Preventing supply chain attacks, SBOM integration          |
| 5    | ⚙️ Scripting & Automation with Bash & Python               | Bash loops, cron, Python scripts, automation jobs             | Writing secure scripts, input validation, secrets handling |
| 6    | 🏗️ CI/CD Pipelines Part I – GitHub Actions & GitLab CI    | Pipelines, jobs, runners, secrets, artifact management        | Shift-left testing, secrets injection, SBOM publishing     |
| 7    | 🏗️ CI/CD Pipelines Part II – AWS CodePipeline & CodeBuild | CodePipeline YAML, IAM roles, artifact stores                 | Secure build environments, CodeBuild OIDC                  |
| 8    | 🔐 Secrets Management with Vault, SOPS, Sealed Secrets     | Encryption, secret rotation, key policies                     | Preventing leaks, centralizing secret lifecycle            |
| 9    | 🐳 Container Image Security & SBOMs                        | Trivy, Grype, Syft, vulnerability scans                       | Supply chain integrity, CVE workflows                      |
| 10   | 🔍 IaC Fundamentals & Security (Terraform, CFN, SAM)       | Resources, providers, tfstate, plan/apply                     | tfsec, drift detection, GitOps for infra                   |
| 11   | 🔧 Kubernetes Security I – Access, Policies, RBAC          | Kubeconfig, RBAC, Roles, NetworkPolicies                      | Preventing privilege escalation, least privilege           |
| 12   | 🔧 ECS & Fargate Security I – Service Connect & IAM        | ECS Services, IAM roles, namespace policies                   | Service isolation, cross-env communication                 |
| 13   | 🧠 Policy as Code (OPA, Gatekeeper, Kyverno)               | Rego, policies, admission controllers                         | Enforce org-wide security standards                        |
| 14   | 🛡️ Runtime Security with Falco, eBPF & Auditd             | Process monitoring, file access, kernel hooks                 | Intrusion detection, anomaly alerting                      |
| 15   | 📡 Monitoring, Logging, Alerting                           | Prometheus, Loki, CloudWatch, GuardDuty                       | Security monitoring, log aggregation                       |
| 16   | 🔐 AppSec & OWASP for Node.js + Python                     | Threat modeling, validation, API testing                      | OWASP Top 10 coverage, JWT handling, rate limiting         |
| 17   | 🔐 Zero Trust in ECS + Kubernetes                          | Env isolation, workload identity, network security            | Implementing Zero Trust boundaries                         |
| 18   | ⚔️ Red Team vs Blue Team Scenarios                         | Simulated attacks, detection, forensics                       | Real-world incident response simulation                    |
| 19   | 🏗️ Capstone Project I – Secure Software Factory           | CI/CD, scanning, secrets, SBOM, deploy                        | DevSecOps automation end-to-end                            |
| 20   | 📘 Capstone Project II – Review, Demo, Threat Modeling     | Peer review, post-mortem, lessons learned                     | Reinforce learning, simulate interviews                    |


⸻

💡 Why This Matters

We’ve now fully:
	•	Respected the DevOps foundation (Linux, Git, networking, scripting)
	•	Integrated DevSecOps theory into every topic
	•	Preserved advanced security content (runtime, red team, supply chain)
	•	Balanced concept + hands-on practice

⸻

✅ Updated DevSecOps Course Principles
1. 🔄 Project Lifecycle Driven
Every module evolves the application and supporting infrastructure.

Simulates real development cycles: feature expansion, hardening, pipeline upgrades, threat mitigation.

2. 📦 Full Application Evolution
Node.js frontend + Python backend grow weekly.

Secure ECS & Kubernetes deployments.

Evolving IaC using Terraform, CloudFormation, and SAM.

3. 🔐 DevSecOps Responsibilities per Role
Real-world roles simulated:

CI/CD Engineer

Cloud Security Engineer

Runtime Defender

Policy Enforcer

AppSec Specialist

Resume-ready experience with practical controls.

4. 🎓 Capstone-Ready Outcome
By the end of 20 weeks, you'll have:

📂 A GitHub portfolio with infrastructure, apps, security, and monitoring

🔄 Working pipelines: GitHub Actions, GitLab CI, AWS CodePipeline

🧾 SBOMs, signed commits, container/image scans

🛡️ Policy-as-code & runtime defenses

🏗️ A complete reference architecture for end-to-end DevSecOps



Inspired by TechWorld With Nana's DevOps Bootcamp Syllabus
