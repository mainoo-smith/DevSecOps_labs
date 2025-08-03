# 🏗️ Week 19 – Guided Lab: Secure Software Factory with OWASP ZAP DAST

---

## 🎯 Goal

Set up a **production-grade CI/CD pipeline** for NoteStream Pro that:

- Builds and scans Docker images
- Injects secrets securely
- Deploys to a staging environment
- Runs OWASP ZAP **DAST** scans against the live staging app
- Blocks or flags builds with critical vulnerabilities
- Stores **SBOMs**, logs, and scan reports

---

## 🧱 Lab Architecture

```mermaid
graph TD
  A[Git Push] --> B[GitHub Actions or GitLab CI]
  B --> C[Build Docker Image]
  C --> D[Run SCA Scan (Trivy)]
  C --> E[Generate SBOM (Syft)]
  E --> F[Sign w/ cosign]
  F --> G[Deploy to ECS/K8s Staging]
  G --> H[Run ZAP DAST Scan via CLI]
  H --> I[Upload HTML Report to CI/CD logs or S3]
  I --> J[Runtime Monitoring (Falco, GuardDuty)]
🛠️ Prerequisites
✅ CI/CD pipeline already set up (GitHub Actions or GitLab CI)

✅ App is containerized

✅ ECS Fargate or Kubernetes staging environment deployed

✅ docker build and kubectl/aws ecs available in pipeline

✅ Your NOTE_STREAM_PRO_STAGING_URL environment variable is set (e.g. https://staging.notestreampro.dev)

📦 Add ZAP to Your Pipeline
✅ Step 1: Install ZAP in CI Runner
In GitHub Actions:

- name: Install OWASP ZAP CLI
  run: |
    sudo apt update && sudo apt install -y snapd
    sudo snap install zaproxy --classic
In GitLab CI (Docker image):

image: owasp/zap2docker-stable
✅ Step 2: Run ZAP Baseline Scan
Create a ZAP scan script:

📄 .zap/zap-baseline.sh
#!/bin/bash
TARGET_URL=$1
REPORT_FILE=$2

docker run --rm -v $(pwd):/zap/wrk/:rw \
  owasp/zap2docker-stable zap-baseline.py \
  -t "$TARGET_URL" \
  -r "$REPORT_FILE" \
  -x zap-report.xml \
  -J zap-report.json \
  -m 5 \
  -T 10
✅ What it does:

-t: Target URL to scan (your staging app)

-r: HTML report output

-x/-J: Output XML/JSON results for machine parsing

-m: Max alerts per rule

-T: Timeout in minutes

✅ Step 3: Call the Script in CI
GitHub Actions
- name: ZAP Baseline DAST Scan
  run: |
    chmod +x .zap/zap-baseline.sh
    .zap/zap-baseline.sh "$NOTE_STREAM_PRO_STAGING_URL" "zap-report.html"
GitLab CI
zap_scan:
  stage: test
  image: docker:latest
  services:
    - docker:dind
  script:
    - chmod +x .zap/zap-baseline.sh
    - .zap/zap-baseline.sh "$NOTE_STREAM_PRO_STAGING_URL" "zap-report.html"
  artifacts:
    paths:
      - zap-report.html
✅ Step 4: Add Post-Scan Security Gate (Optional)
In GitHub Actions:

- name: Fail on High ZAP Alerts
  run: |
    grep -q 'High' zap-report.html && exit 1 || echo "No high severity alerts"
🛑 This breaks the build if any high-severity issues are found.

📁 Output Artifacts
File	Purpose
zap-report.html	Human-readable report
zap-report.xml	Machine-readable for CI tools
zap-report.json	JSON for dashboards or alerting
✅ Completion Checklist
 App builds and deploys to staging on push

 OWASP ZAP runs baseline scan against the deployed app

 ZAP report artifacts are stored with each CI run

 Optional: Build fails on critical/high ZAP findings

 Optional: ZAP results are published to Slack/S3

🧠 DevSecOps Lessons
Lesson	Description
Shift DAST left	You don’t need a QA team to test for live attack surfaces
Don’t trust just the code	You must test the behavior of the live app
Fail fast	DAST failures should stop promotion to production
Trace findings back to code	Every alert should map to a fixable component
Automate reports	Scans are useless unless teams see and act on them
✅ Congrats. You now have a working, real-world secure software factory that includes:
SBOMs, image scanning, secrets management, and DAST — all enforced in CI/CD.

Next up:
🔬 Week19.5 – ZAP + DAST Deep Dive (tuning, spidering, auth flows, integration with dashboards)

Let me know when you’re ready to proceed.


---

Would you like the Challenge Lab next, or proceed to the 19.5 Deep Dive with ZAP?
You said:
Next 
ChatGPT said:
Perfect — up next is: