# 🧪 Week 19.5 – Guided Lab: OWASP ZAP Deep Dive for DevSecOps Pipelines

---

## 🎯 Goal

Master OWASP ZAP for **real-world DAST** (Dynamic Application Security Testing). You will:

- Customize ZAP scan configurations
- Run spidering and active scans
- Scan authenticated areas using tokens or cookies
- Tune alerts and fail builds based on severity
- Generate and analyze actionable reports

This bridges the gap between "just running ZAP" and **using it like a professional DevSecOps engineer**.

---

## 🛠️ Prerequisites

- A running **staging app** (NoteStream Pro)
- ZAP CLI/Docker image available in your CI/CD
- A login page or token-based auth in the app
- Environment variable: `NOTE_STREAM_PRO_STAGING_URL`

---

## 🧩 Part 1: Authenticated Scanning (Token or Session-Based)

### 🧪 Example: Bearer Token Auth

1. Log in manually and capture a valid bearer token:
```bash
curl -X POST https://staging.notestreampro.dev/api/auth/login \
  -d '{"email": "testuser@example.com", "password": "testpass"}' \
  -H "Content-Type: application/json"
Extract and export it:

export BEARER_TOKEN="eyJhbGciOiJIUzI1NiIsIn..."
Add the token to your ZAP baseline call (via header injection):

docker run --rm -v $(pwd):/zap/wrk/:rw \
  owasp/zap2docker-stable zap-baseline.py \
  -t "$NOTE_STREAM_PRO_STAGING_URL" \
  -r zap-auth-report.html \
  -z "-config replacer.full_list(0).description=AuthHeader \
      -config replacer.full_list(0).enabled=true \
      -config replacer.full_list(0).matchtype=REQ_HEADER \
      -config replacer.full_list(0).matchregex=false \
      -config replacer.full_list(0).matchstring=Authorization \
      -config replacer.full_list(0).replacement=Bearer $BEARER_TOKEN"
✅ ZAP will now inject the token in every request, enabling auth-protected route testing.

🧩 Part 2: Spidering the App (Crawl Before Attack)
Why?
DAST tools need to discover pages before they can scan them.

docker run --rm -v $(pwd):/zap/wrk/:rw \
  owasp/zap2docker-stable zap-full-scan.py \
  -t "$NOTE_STREAM_PRO_STAGING_URL" \
  -r full-zap-spider.html \
  -z "-addoninstall ascanrulesAlpha"
🐙 The zap-full-scan.py script spiders your site and runs a deeper active scan.

🧩 Part 3: Custom Rule Filtering (Fail on High Only)
If using CI/CD, filter results based on severity:

docker run --rm -v $(pwd):/zap/wrk/:rw \
  owasp/zap2docker-stable zap-full-scan.py \
  -t "$NOTE_STREAM_PRO_STAGING_URL" \
  -J full-zap.json
Parse and fail the job (example for GitHub Actions):

cat full-zap.json | jq '.site.alerts[] | select(.risk == "High")' | grep -q . && exit 1 || echo "No high-risk issues"
🧩 Part 4: ZAP Context Files (Advanced Auth & Routing)
You can define a .context file with:

Login URL

Auth type (form, script, API token)

Excluded endpoints

CSRF token extraction

Session awareness

Import it like:

zap-cli context import context/notestream.context
🤓 This allows multi-user login, CSRF protection simulation, and complex routing scenarios.

🧩 Part 5: Report Outputs
Format	How to generate
HTML	-r report.html
XML	-x report.xml
JSON	-J report.json
Upload reports to:

🗂️ GitHub/GitLab Artifacts

☁️ S3 bucket or GCS

📬 Slack or Email summaries

🧠 DevSecOps Concepts Reinforced
Concept	How We Used It
Dynamic security testing	Scanning live staging deployments
Authenticated DAST	Validating logged-in paths
Security gates	Failing builds on high alerts
Automation	Embedding scans into the delivery pipeline
Traceability	Generating permanent, signed scan artifacts
✅ Completion Checklist
 Spidering and full scan runs on every PR to staging

 Bearer or session-based login flows are tested

 ZAP fails build if high alerts are found

 Reports are pushed to a shared store or pipeline artifacts

🎯 You now have hands-on mastery of ZAP as a DAST tool, fully integrated with CI/CD and auth-aware.

Let me know when you’re ready for Week19.5/ChallengeLab.md, where we’ll push you to build advanced scanning flows and validation gates.


---

Let me know if you'd like to proceed with the **Week 19.5 Challenge Lab** or pause to test what we've done so far.
You said:
Ready 
ChatGPT said:
Excellent — here's your Week 19.5 challenge lab: