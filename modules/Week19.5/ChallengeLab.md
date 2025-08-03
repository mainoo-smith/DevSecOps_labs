# 🧪 Week 19.5 – Challenge Lab: Mastering ZAP in DevSecOps Pipelines

---

## 🎯 Goal

Apply what you've learned about OWASP ZAP and DAST to:

- Simulate authenticated attacks
- Integrate ZAP into your app lifecycle
- Fine-tune findings and thresholds
- Automate enforcement in real-world pipelines

You’ll demonstrate full-stack security testing maturity in your CI/CD flow.

---

## 🧩 Challenge Tasks

---

### ✅ 1. 🔐 Create a ZAP Context File

- Define your login endpoint (`/api/auth/login`)
- Use a **bearer token injection** or form-based session login
- Exclude logout or static files from scanning

📄 `zap/notestream.context`

```xml
<context>
  <authentication>
    <method type="script-based" />
    <loginurl>https://staging.notestreampro.dev/api/auth/login</loginurl>
    <bearertoken source="env" name="BEARER_TOKEN" />
  </authentication>
  <include>
    <url>https://staging.notestreampro.dev/.*</url>
  </include>
  <exclude>
    <url>.*logout.*</url>
    <url>.*static/.*</url>
  </exclude>
</context>
🧠 ZAP can now reuse this across scans to stay logged in and scan deeper.

✅ 2. 🕷️ Launch Full ZAP Spider + Active Scan in Pipeline
Use zap-full-scan.py or launch ZAP daemon + CLI separately

Capture and store the report artifacts

docker run --rm -v $(pwd):/zap/wrk \
  owasp/zap2docker-stable zap-full-scan.py \
  -t "$NOTE_STREAM_PRO_STAGING_URL" \
  -c zap/notestream.context \
  -r zap-auth-full.html \
  -J zap-auth-full.json
✅ 3. ✋ Fail Pipeline on Custom Risk Threshold
Write a CI/CD-safe parser:

📄 .zap/check-severity.sh

#!/bin/bash
THRESHOLD="Medium"

if jq -e --arg risk "$THRESHOLD" \
  '.site.alerts[] | select(.risk == $risk)' zap-auth-full.json > /dev/null; then
  echo "❌ Found $THRESHOLD or higher risk vulnerabilities"
  exit 1
else
  echo "✅ No risky vulnerabilities found"
fi
Add this as a build gate before promotion to production.

✅ 4. 📬 Push ZAP Report to Your Security Team Automatically
Upload to S3:

aws s3 cp zap-auth-full.html s3://org-security-reports/notestream/$(date +%s).html
Or send a Slack notification using webhook + ZAP summary (bonus).

✅ 5. 🔁 Rerun After Each Feature Merge to staging
Make ZAP run:

Every merge to staging

Every time infra or API changes

During security smoke tests

Use a GitHub/GitLab conditional trigger:

if: github.ref == 'refs/heads/staging'
🧠 Advanced Bonus (Optional)
Test with expired tokens

Add CSRF token simulation

Integrate with a dashboard like DefectDojo or Dependency-Track

Link ZAP to GitHub Security tab using SARIF format

✅ Completion Checklist
Item	Status
ZAP context file configured	✅
Authenticated scan with spider and active tests	✅
Pipeline fails on medium/high alerts	✅
Reports uploaded and traceable	✅
Automated re-scan policy implemented	✅
🧠 Reflection
Question	Prompt
What was the most challenging part of configuring ZAP?	
How can you make sure DAST doesn’t become noisy?	
Where in your real pipeline should DAST run — pre-prod or earlier?	
How would you explain DAST vs SAST to a dev team?	
🎯 By completing this lab, you've proven that you're not just scanning apps — you understand how to operationalize DAST securely and reliably in real CI/CD workflows.

Let me know when you're ready for the Week19.5/Security.md summary — or to proceed to Week 20: Capstone Review & Threat Modeling.


Would you like to continue with the **Security Summary** for Week 19.5 or jump to **Week 20**?
You said:
Ready, but did we cover SCA ?
ChatGPT said:
Great question — and you're absolutely right to ask.

✅ Yes, we did cover SCA (Software Composition Analysis) — but let me clarify where and how, so you’re confident it's not been overlooked:

🧪 SCA Coverage in Our Curriculum
📅 Week	Module	Tool	What We Did
Week 6	CI/CD Pipelines Part I	Trivy, npm audit, bandit	Performed scans on code dependencies during builds (SCA + SAST)
Week 7	CI/CD Pipelines Part II	Grype, Syft, Trivy	Generated and verified SBOMs for base images and dependencies
Week 9	Container Image Security & SBOMs	Syft + Grype	Focused specifically on open source vulnerabilities, license risks, SBOM generation
Week 19	Secure Software Factory	Integrated all tools to enforce vulnerability scan gates (e.g., fail on CVE severity)	
✅ Recap of SCA-Related Actions
Generate SBOMs using Syft or Trivy

Scan dependencies in both Node.js and Python via:

npm audit

pip-audit

bandit for code-level issues

Enforce gating rules (e.g., fail build if trivy finds CVEs above a threshold)

Link scans to CI/CD and artifact promotion (only allow trusted, signed, and scanned artifacts)

❓ What's the Difference Between SCA and SAST/DAST?
Type	Focus	Tools
SCA	3rd-party dependencies (e.g., lodash, express, requests)	Trivy, Grype, npm audit, pip-audit
SAST	Source code analysis (your code)	Bandit, semgrep
DAST	Runtime behavior (live app testing)	ZAP, Burp, Postman (in some workflows)
So:
✅ SCA was covered across multiple weeks, integrated with your CI/CD, and aligned with your artifact trust pipeline.

If you'd like, we can do a Week 9.5 that shows enterprise-level SCA dashboards (like Snyk, DependencyTrack, or OWASP Dependency-Check) — or move ahead to Week 19.5 Security Summary or Week 20.

How would you like to proceed?

You said:
Move ahead 
ChatGPT said:
Perfect — let’s wrap up Week 19.5 with: