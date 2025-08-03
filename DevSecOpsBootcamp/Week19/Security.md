# 🔐 Week 19 – Security Review: Secure Software Factory

---

## 🎯 Security Objectives Recap

This week’s lab focused on building a **Secure Software Factory** that embeds security into every stage of the CI/CD pipeline:

| Phase | Security Layer | Tool |
|-------|----------------|------|
| Code commit | Signed commits, PR approvals | GitHub/GitLab |
| Build | SAST, SBOM, secret scan | Bandit, Syft, Trivy |
| Image | Signature, provenance | cosign |
| Deploy | IaC validation | Terraform/CDK + tfsec |
| Post-deploy | DAST | OWASP ZAP |
| Runtime | Monitoring | Falco, GuardDuty |

---

## 🧱 What Makes It Secure?

### ✅ 1. **Automation**
No manual security steps — everything runs as part of your CI/CD.

### ✅ 2. **Repeatability**
Every pipeline run generates:
- Signed images
- Verified SBOMs
- ZAP scan reports
- Deployment logs

### ✅ 3. **Gates, Not Just Scans**
Security findings impact **promotion decisions** — they’re not just logged and ignored.

### ✅ 4. **Artifact Provenance**
Everything is cryptographically signed, verified, and traceable to a source commit.

---

## 🔐 Key Security Controls Implemented

| Control | Purpose |
|--------|---------|
| 🔏 Signed Docker images | Prevent supply chain injection |
| 📦 SBOMs per build | Know what you’re shipping |
| 🧪 ZAP DAST scans | Find live app issues (auth bypass, XSS) |
| 🚨 Alerting on critical findings | Shift-left enforcement |
| 📄 Audit trail of artifacts | Trace back to any commit/image |

---

## 📌 Areas for Further Hardening

| Area | Suggestion |
|------|------------|
| 🧬 Provenance Verification | Add in-toto or SLSA attestations |
| 🔐 Secrets Lifecycle | Rotate secrets, enforce TTLs |
| 📢 Visibility | Push alerts into SIEM (e.g., Datadog, Splunk) |
| 👮 Policy-as-Code | Use OPA or Kyverno to enforce security policies |

---

## 🔁 Real-World Takeaway

A **Secure Software Factory** is not about tools — it’s about ensuring:

- **Trust** in what you deploy
- **Traceability** in who changed what
- **Enforcement** when something breaks your security baseline

---

> ✅ You now have a pipeline that reflects **enterprise-grade DevSecOps principles**.

Coming up next:
### 🧪 Week 19.5 – DAST Deep Dive with OWASP ZAP

Ready to go deeper?
Let me know when you're ready to begin Week 19.5 – ZAP Deep Dive, or if you’d prefer to do the Week 19 Reflection first.

You said:
Continue 
ChatGPT said:
Excellent — let’s go deep.