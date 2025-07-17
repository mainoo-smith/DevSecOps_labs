This is a test module for learning DevSecOps by simulating real-world scenarios using real tools. 
To use this repo, you can fork it, clone it, or create an issue from a PR. 
The project comes with scripts that can be run locally or on any VM.
You can play around with the commands, break things, and fix them to reinforce learning.

Curriculum structure:
```bash
  | Week      | Theme                                   | Includes (From All Sources)                                               |
| --------- | --------------------------------------- | ------------------------------------------------------------------------- |
| **01**    | DevOps Mindset + Git                    | DevOps 5W1H, CI/CD overview, Git basics → GitFlow, GitHub actions trigger |
| **02**    | Linux + SSH + Security                  | Users/groups, firewalls, SSH keys, OS hardening, patching                 |
| **03**    | Bash + Python Scripting                 | Real-world automation: log rotation, alerts, deployer                     |
| **04**    | CI/CD Concepts + GitHub Actions         | YAML pipelines, build/test/lint jobs, matrix builds                       |
| **05**    | Jenkins & GitLab CI                     | Jenkinsfile, runners, agents, GitLab pipelines, secrets mgmt              |
| **06**    | Docker & Best Practices                 | Image layers, multi-stage builds, `.dockerignore`, healthchecks           |
| **07**    | Image Signing + Scanning                | Trivy, SBoMs, Notary, AWS ECR scanning, vulnerabilities                   |
| **08**    | AWS ECR + Secure Push                   | OIDC auth in GitHub/GitLab/Jenkins, IRSA in EKS, lifecycle tags           |
| **09**    | Config Management (Ansible)             | Inventories, playbooks, roles, templates, Jinja2                          |
| **10**    | Advanced Ansible + Vault + Provisioning | Encrypted vars, provisioning EC2s, app install, Vault integration         |
| **11**    | IaC with Terraform                      | State mgmt, backend config, VPC, EC2, S3, IAM                             |
| **12**    | Advanced Terraform + EKS Setup          | EKS modules, node groups, IRSA, Helm provider                             |
| **13**    | Kubernetes Intro (EKS)                  | Deployments, services, configmaps, volumes, autoscaling                   |
| **14**    | Helm + Secrets + Ingress                | Helm templating, ingress-nginx, TLS via cert-manager, sealed-secrets      |
| **15**    | GitOps (ArgoCD or FluxCD)               | Git as source of truth, drift detection, self-healing apps                |
| **16**    | Observability I (Prometheus/Grafana)    | Metrics, dashboards, node\_exporter, alerts                               |
| **17**    | Observability II (Loki, ELK)            | Logs, structured formats, log correlation, log retention                  |
| **18**    | CI/CD on AWS (CodePipeline)             | CodeBuild, CodeDeploy, artifact mgmt, approval stages                     |
| **19**    | Cloud Cost + Optimization               | Spot, reserved instances, cost explorer, AWS Budgets                      |
| **20**    | Security: OPA + tfsec + Checkov + Falco | IaC policies, runtime protection, anomaly alerts                          |
| **21**    | SRE: SLIs, SLOs, SLAs                   | Golden signals, alert fatigue, error budgets                              |
| **22–24** | Capstone: DevSecOps Platform Build      | CI/CD → Secure Container → ECR → EKS → GitOps → Observability             |

```
The project is divided into modules by week. Every week has an overview, guided labs, challenge lab, reflection, security considerations, and expected outcome.
After completing each lab/task, you can create an issue and add it to the corresponding project to track your progress.

Enjoy!!!

Inspired by TechWorld With Nana's DevOps Bootcamp Syllabus
