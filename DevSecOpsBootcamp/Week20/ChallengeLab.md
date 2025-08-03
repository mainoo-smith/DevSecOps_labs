# 🧪 Week 20 – Challenge Lab: Build + Defend Your Secure Software Factory

---

## 🎯 Goal

Prove you can manage the full DevSecOps lifecycle by:

- Automating code-to-cloud deployments
- Enforcing multiple layers of security gates
- Capturing artifacts, SBOMs, and evidence
- Executing a realistic attack simulation and defending against it

---

## 💻 Scenario

Your team is preparing to release **v1.0.0** of `NoteStream Pro`.

You must:
- Promote the current `staging` build to `production`
- Prove that it passed all trust gates (SCA, DAST, SBOM, Secrets, IAM)
- Simulate a realistic attack chain (e.g., leaked secret or vulnerable dependency)
- Demonstrate how your system detects, blocks, or recovers

---

## ✅ Part 1: Secure Promotion Flow

### 🔁 Tag & Build

```bash
git checkout staging
git tag -s v1.0.0 -m "Secure release candidate"
git push origin v1.0.0
🎯 Use signed tags and push to trigger pipeline.

📦 GitHub/GitLab CI/CD Pipeline
Ensure the following jobs run on the tag:

Job	Tool	Expected Output
sbom-gen	Syft	sbom.json in /dist
sca-check	Trivy, npm audit	Pass or fail on CVE threshold
sast-check	Bandit, Semgrep	Clean scan
secret-check	Gitleaks	No hardcoded secrets
image-scan	Trivy (image)	CVE severity filtered
deploy-prod	Terraform/CDK	Secure infra + ECS/K8s deploy
sign-image	Cosign	Signed Docker image
✅ Part 2: Attack Simulation
Pick one realistic risk from below and simulate it:

Attack	Simulate
Leaked Git secret	Temporarily push a fake token and test detection
Downgrade vulnerable lib	Use a known-vulnerable version of a package
Broken endpoint	Disable auth guard on an API route
Over-permissive IAM	Add wildcard to policy and test detection in review
Then:

Document how your tools caught it (e.g., ZAP, Gitleaks, tfsec)

Describe how a build would fail or alert you

Fix the issue and rerun pipeline to confirm secure promotion

✅ Part 3: Collect Audit Trail
Artifact	Tool/Source	Storage
sbom.json	Syft/Trivy	/artifacts/sbom/
zap-report.html	ZAP	/artifacts/zap/
attestation.json	Cosign	/artifacts/attestation/
tfplan.json	Terraform	/artifacts/iac/
pipeline.log	CI system	/logs/builds/v1.0.0/
🎯 Push these to a docs/release/ folder or s3://notestream-artifacts/releases/v1.0.0/

✅ Part 4: Defense Retrospective
Write a brief in docs/security/retrospective.md answering:

What could’ve gone wrong if the attack succeeded?

What caught the issue?

What changes did you make to improve the pipeline?

What new detection rule/policy should be added?

🎓 Evaluation Rubric
Section	Weight
Secure CI/CD with 5+ gates	✅
Attestation and SBOM traceability	✅
Risk-based failure response	✅
Attack simulation and recovery	✅
Audit and documentation trail	✅
✅ If this lab is complete, you're operating at a professional DevSecOps engineer level.

Let me know when you’re ready for:

ThreatModel.md

Security.md

Reflection.md

and final .zip export


Ready for the **Threat Model**?
You said:
Ready 
ChatGPT said:
Excellent — let’s build your final threat model for the NoteStream Pro system.