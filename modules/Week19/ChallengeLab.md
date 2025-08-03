# 🧪 Week 19 – Challenge Lab: Harden and Extend Your Secure Software Factory

---

## 🎯 Goal

Take the baseline secure CI/CD pipeline you built in the Guided Lab and:

1. Extend it with deeper security gates
2. Add traceability and integrity checks
3. Harden the entire build/deploy process
4. Build confidence in promotion to production

This challenge mimics what you'd do in an enterprise DevSecOps role.

---

## 🧩 Challenge Tasks

### ✅ 1. **Add Sigstore Cosign to Sign Your Container Images**

- Use `cosign` to sign the image after SBOM + scan
- Store the signature in your container registry (e.g., ECR or DockerHub)

```bash
cosign sign --key env://COSIGN_PRIVATE_KEY ghcr.io/yourorg/notestream-pro:latest
🧠 Why? So you can verify provenance of every deployable image

✅ 2. Create a Promotion Workflow Based on Trust Signals
Build a CI/CD stage that only promotes builds to production if:

✅ Trivy scan = no critical vulnerabilities

✅ Cosign signature exists and is valid

✅ ZAP DAST scan = no high findings

✅ SBOM file exists in artifacts or S3

❗ Simulate this with a "gatekeeper" script that checks all conditions before allowing the prod-deploy stage.

✅ 3. Automatically Push ZAP Scan Report to S3 or GitHub Releases
Add a post-processing step:

aws s3 cp zap-report.html s3://your-team-security-logs/notestream/zap-$(date +%s).html
Or for GitHub Actions:

- name: Upload ZAP Report
  uses: softprops/action-gh-release@v1
  with:
    files: zap-report.html
📊 Now your security team or DevOps manager can always audit DAST results.

✅ 4. Write a Shell Script that Verifies the Full Security State
This script should check:

Signature presence

SBOM file

Scan pass/fail

DAST report status

Simulate a tool like in-toto or Conftest that verifies the entire artifact chain.

✅ 5. Bonus: Add Notifications
Integrate Slack or email alerts if ZAP finds anything >= Medium

Use GitHub Actions + Slack Webhook or SES

✅ Expected Outcome
By the end of this challenge:

You’ve extended your Secure Software Factory with trust and verification gates

CI/CD flow now enforces evidence of security before promotion

You’ve created artifacts you can use in a portfolio, demo, or interview

🧠 DevSecOps Reflection Questions
How did it feel to treat security as part of the delivery lifecycle, not a blocker?

Where would you improve visibility for security findings in a real team?

How might you automate these checks further using OPA/Rego or in-toto?

What would happen in your org if someone bypassed this system?

🧠 This challenge is about bringing maturity into your pipeline — not more tools, but better trust, audit, and gates.

Let me know when you’re ready for:
🔐 Week19/Security.md – Review all security layers and controls across the factory.


---

Would you like to continue to the **Security Summary** or do the **ZAP Deep Dive (Week 19.5)** first?
You said:
Ready 
ChatGPT said:
Great — let’s wrap up Week 19 with: