# 🧪 Week 20 – Guided Lab: Final DevSecOps Review & Demo Packaging

---

## 🎯 Objective

Walk through your **entire Secure Software Factory**, validating each security control, and prepare your repo and documentation for demo, portfolio, or recruiter review.

---

## 🧩 Step 1: Validate App Security Posture

Run a full suite of scans against your **latest deployment in `staging`**.

### 🔍 Trivy SCA & SBOM

```bash
trivy fs . --severity CRITICAL,HIGH --format table

syft . -o table
Confirm no critical CVEs exist in your Python or Node.js dependencies.

🧪 Bandit – Python Code Review
bandit -r backend/
Validate that no unsafe eval, exec, or hardcoded credentials exist.

🧪 Semgrep – Node.js + Python Pattern Checks
semgrep scan --config "p/default" --include node_modules --lang js,python
Spot insecure API usage patterns, JWT mishandling, and more.

🔐 Secrets Detection
gitleaks detect --source .
trufflehog filesystem .
Confirm no API keys or secrets were committed at any point in Git history.

🌐 ZAP DAST
docker run -v $(pwd):/zap/wrk -t owasp/zap2docker-stable zap-full-scan.py \
  -t "$STAGING_URL" \
  -c zap/context.context \
  -r zap-final-report.html
Verify endpoints, session handling, and authentication flow are secure.

🧩 Step 2: Review Your CI/CD and Artifact Chain
🔁 Git Commit & Merge Controls
Signed commits: git log --show-signature

Protected branches for main, staging, production

Tagging for production builds: v1.0.0

Show how you ensure traceability and integrity.

📦 SBOM + Image Attestation
cosign attest <image-ref>
Link your SBOMs to Docker images with signed metadata.

🔐 CodePipeline Artifact Store
Confirm you are:

Not exposing secrets in CodeBuild logs

Rotating IAM roles/token via OIDC

Validating image provenance before promotion

🧩 Step 3: Final Threat Assessment
Walk through your system and identify:

Component	Potential Threat	Control
API Gateway	ID spoofing	IAM policy + JWT scope check
Frontend JS	XSS	CSP + output sanitization
DB access	Lateral movement	Least-privilege IAM role
Secrets in CI	Hardcoded secrets	Vault/SOPS/SealedSecrets
Service A → B	Trust abuse	ECS Service Connect namespace policy
Artifact store	Tampering	SBOM + Cosign signatures
🧩 Step 4: Prepare for Recruiter or Manager Demo
✅ Repo Checklist
Item	Completed
Clean README.md with diagram & architecture	✅
CI/CD YAMLs (GitHub/GitLab/CodePipeline)	✅
docs/ folder with SBOM, threat model, ZAP reports	✅
Clearly named branches: feature/, hotfix/, release/	✅
Signed commits or tags for releases	✅
Demo credentials & links to staging environment	✅
📺 (Optional) Record a Loom or Screencast
Talk through:

The problem your app solves

How security is built-in at every stage

How your pipeline enforces trust, secrets, compliance

💬 “You don’t just deploy an app. You deploy trust.”

Let me know when you're ready for:

✅ ChallengeLab.md
✅ ThreatModel.md
✅ Security.md
✅ Reflection.md
🧳 Bootcamp .zip export

You said:
Ready 
ChatGPT said:
Perfect — here’s the Capstone Challenge Lab to solidify your end-to-end DevSecOps mastery.