# 🏗️ Week 19 – Capstone Project I: Build a Secure Software Factory

---

## 🎯 Goal

Design and build a **fully integrated secure CI/CD pipeline** that takes your evolving app (NoteStream Pro) through:

- 🛠️ Secure code workflows  
- 🔐 Secrets management  
- 🐳 Container image hardening  
- 🧪 Vulnerability scanning  
- 📦 Artifact signing and SBOMs  
- 🚀 Deployment into a secured environment (ECS or K8s)

This isn't a simulation — this is your **real, production-grade pipeline**.

---

## 🧠 Core Concepts

| Concept | Explanation |
|--------|-------------|
| **Secure Software Factory** | A complete toolchain that enforces security from commit to deploy |
| **Trusted Supply Chain** | Ensure integrity and provenance of code, builds, and images |
| **Defense-in-Depth CI/CD** | Apply security at every stage: commit, build, scan, deploy, and monitor |
| **Provenance Attestation** | Use SBOMs and signing to prove artifact origin and trustworthiness |
| **Deployment Assurance** | Only signed, scanned, tested, and policy-compliant code gets deployed |

---

## 🧰 Tech Stack

| Stage | Tooling |
|-------|---------|
| Source | GitHub / GitLab |
| Build | GitHub Actions / GitLab CI / AWS CodeBuild |
| IaC | Terraform, CDK, SAM |
| Image Security | Trivy, Grype, Syft |
| Secrets | Vault, SOPS, GitHub Encrypted Secrets |
| Attestation | Sigstore (cosign), in-toto, Syft |
| Deploy | ECS Fargate + Service Connect or K8s |
| Runtime | Falco, OTEL, GuardDuty |
| Monitoring | CloudWatch / Loki / Prometheus |

---

## 🧩 Secure CI/CD Flow (Example)

```mermaid
graph TD
  A[Commit Signed Code] --> B[Pipeline Triggered]
  B --> C[Secrets Injected Securely]
  C --> D[SBOM Generated + Scan w/ Trivy]
  D --> E[Run Static + Dynamic Tests]
  E --> F[Sign Container w/ Cosign]
  F --> G[Deploy to Staging (K8s or ECS)]
  G --> H[Runtime Monitoring (Falco + OTEL)]
  G --> I[Generate Audit Trail + Compliance Report]
🔐 Security Layers (Mapped to Pipeline)
Stage	Security Control
Code	Signed commits, branch protection, SBOM
Build	CI runner isolation, secrets injection via OIDC
Test	SAST (SonarQube), DAST (ZAP), unit + API tests
Image	Minimal base image, no root, Trivy scan, Cosign sign
Deploy	CDK/Terraform IaC scan, OPA policy, IAM-scoped roles
Runtime	Falco for syscall alerts, OTEL for trace anomalies
Audit	CloudTrail/Logs + webhook alerts to Slack/SIEM
🛠️ Project Expectations
By the end of this week you will:

✅ Deploy an app using IaC + secured CI/CD

✅ Harden the build process with scanning, signing, and secrets management

✅ Configure runtime detection and log aggregation

✅ Capture artifacts (SBOMs, signed images, logs, attestations)

✅ Be able to demo your secure software factory to a potential employer or security team

📘 DevSecOps Value
This capstone project proves that you:

Understand how modern secure pipelines work end-to-end

Know how to balance delivery velocity with strong security guarantees

Can integrate security by design, not bolted on later

Have real-world deliverables (signed images, SBOMs, pipelines) to showcase

🧠 This week isn’t about new tools — it’s about assembling everything you’ve learned into a real-world system that you can reuse, adapt, and improve professionally.


---

Let me know when you're ready to begin the first task:  
✅ **Guided Lab – Secure Software Factory Setup** (Week19/GuidedLab.md),  
where you’ll set up and walk through each component of your secure factory.
You said:
Okay but did we do the burp suite or it’s after week 19?
ChatGPT said:
Great question — and you're absolutely right to check. Here's the clarification:

✅ Burp Suite Integration Plan
You mentioned earlier that you wanted Burp Suite (or Burp Scanner) included for dynamic application security testing (DAST). We haven’t yet done a full guided lab with Burp Suite.

Here's where it fits in:

📌 Burp Suite Placement in the Syllabus
Week	Module	Status	Burp Integration
Week 16	AppSec & OWASP for Node.js + Python	✅ Completed	Basic OWASP concepts covered, but Burp Suite not deeply used yet
Week 19 (now)	Capstone I – Secure Software Factory	⏳ In progress	Burp can be used optionally as part of testing pipeline
Post-Capstone (Optional Add-on)	DAST Automation with Burp Suite & ZAP	🔜 You requested this earlier as a follow-up module	
✅ Suggested Path
We proceed with Week 19 Capstone as planned — your secure software factory.

Immediately after that, we introduce a focused module on Dynamic App Security Testing (DAST) using:

Burp Suite (Pro or Community)

OWASP ZAP (for CI automation)

And optionally, DAST automation via Docker or CLI tools

Would you like me to:

Proceed with Week 19 Guided Lab now,

Or pause and create a Burp Suite lab first?

Let me know your preference and I’ll deliver accordingly.

You said:
Should not that be part of the secure software factory?
ChatGPT said:
You're absolutely right — and your reasoning is exactly aligned with real-world best practices.

✅ Burp Suite absolutely should be part of a Secure Software Factory
…but with nuance. Here's the breakdown:

🔍 Where DAST Fits in a Secure Software Factory
Test Type	Tooling	When it's run	Purpose
✅ SAST	Bandit, SonarQube, ESLint	During build	Detect insecure code patterns statically
✅ Dependency Scanning	Trivy, Grype, Syft	Build & pre-deploy	Catch vulnerable packages
✅ IaC Scanning	tfsec, Checkov	Build-time	Catch misconfig in Terraform, CDK, etc.
⚠️ DAST (Burp/ZAP)	BurpSuite, OWASP ZAP	Post-build, in a live staging env	Probe live app behavior: auth bypass, XSS, SSRF, etc.
DAST requires a live environment to interact with — it’s not like a code scanner. So it fits after image build and deployment to staging, which is part of your Secure Software Factory.

✅ Recommended Flow in Week 19
We’ll embed Burp Suite into the factory as part of the testing + validation phase, like this:

name: Secure Pipeline (GitHub Actions)

jobs:
  build:
    ...
  test:
    ...
  deploy:
    ...
  dast_scan:
    runs-on: ubuntu-latest
    needs: deploy
    steps:
      - name: Run OWASP ZAP or trigger Burp Suite Pro scan
        run: ./run-dast.sh --target https://staging.notestreampro.dev
🔁 If you're using Burp Suite Pro, you can run headless scans via CLI or Burp's REST API using:

burpsuite_pro.jar (headless)

or Dockerized containers with CI support

If you're using Burp Community, we guide manual testing steps after deploy.

🧩 Integration Options
Include Burp Suite in Week 19 now, as part of the CI/CD flow.

Break it out as a focused Week 19.5 DAST module, going deeper into:

Burp Suite setup, config, extensions

Automating scans (Pro)

Manual workflows (Community)

Comparing with ZAP and GitHub CodeQL

Would you like:

✅ Integrated into Week 19 CI/CD?

➕ Standalone deep dive after Capstone (Week 19.5)?

You can do both, but if you want pipeline-level realism, I recommend integrating Burp Pro or ZAP into the Week 19 pipeline now, then deep-dive later.

Let me know and I’ll tailor the next step.

You said:
Do the recommended industry best practices 
ChatGPT said:
Excellent — we'll follow industry best practices and do both:

✅ Plan: Burp Suite as Part of Secure Software Factory (Week 19)
We will:

Integrate DAST (Burp/ZAP) in Week 19’s pipeline — this mirrors real DevSecOps pipelines used in regulated and security-conscious environments.

Provide automation-first approach (Burp Pro/ZAP in CI).

Include fallback instructions for manual testing with Burp Community.

Follow up with a deep dive (Week 19.5) that goes into Burp Suite customization, reporting, and advanced flows.

🔐 Why This Approach Works
Industry Practice	What We’re Doing
🔁 Test live staging builds	We deploy then scan staging apps with DAST tools
📦 Automate security gates	CI/CD jobs fail on DAST critical findings
⚙️ Include DAST + SAST + SCA + IaC + SBOM	This pipeline includes them all
🔍 Real attacker mindset	DAST scans simulate malicious inputs, misconfig exploits, auth flaws
🧩 Optional manual pen testing	You can drop into Burp Suite GUI for targeted tests
🚀 Next Step
I’ll now generate the .md file for: