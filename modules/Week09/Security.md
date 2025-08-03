Title: Ship with Confidence: How SBOMs, CVE Scans & Signing Protect the Supply Chain

🎯 Security Objectives This Week
This week’s focus was on supply chain integrity:

Goal	Description
🧾 SBOM	Know everything that’s inside your images
🚨 CVE Scanning	Detect known vulnerable components
🔏 Image Signing	Ensure only trusted images are deployed
🔐 Gated Deployments	Block builds that fail security checks
🛡️ Real-World Threats You’re Now Mitigating
1. 💥 Vulnerable Base Images or Open-Source Dependencies
Threat:

Using an outdated base image with known CVEs (e.g. Ubuntu, Python, Node.js)

Or adding a vulnerable library like log4j-core without knowing it

Real Incidents:

Log4Shell (2021) → thousands of apps compromised via hidden Java lib

Mitigation:
✅ You now scan every image with Trivy or Grype
✅ You can fail builds on CRITICAL CVEs
✅ SBOMs give you visibility into the entire dependency tree

2. 🧟‍♂️ “Zombie Dependencies” and Transitive Risks
Threat:

Image contains packages you didn’t explicitly install (e.g., cron, netcat, curl, telnet)

These can be abused in RCE attacks

Mitigation:
✅ SBOM exposes all packages, not just what you install
✅ You can compare SBOMs between versions and detect drift

3. 🧬 Image Tampering in Registry
Threat:

Attacker pushes a malicious image to your registry using your tag (:prod)

Or image is modified post-build (supply chain attack)

Real Incidents:

SolarWinds (build system compromise)

DockerHub hijacked tags (crypto miners)

Mitigation:
✅ You now sign all images using Cosign
✅ You verify images before deploy in CI/CD
✅ Signature ensures image was built by you and hasn’t changed

4. 🔓 Untrusted Images in CI/CD
Threat:

CI/CD pipelines deploy images that are:

Missing scans

Unsigned

Built outside your system

Mitigation:
✅ Pipelines enforce:

SBOM generation

CVE scan gating (--exit-code 1)

Cosign verification

Artifact retention for SBOMs

5. 🧾 Regulatory Compliance & SBOM Requirements
Threat:

No ability to prove what’s inside your software

Inability to respond to supply chain disclosures

Emerging Standards:

U.S. Executive Order (EO 14028)

NIST SP 800-218 (SLSA), SPDX/CycloneDX SBOM formats

FedRAMP, ISO 27001 supply chain mandates

Mitigation:
✅ You now produce and retain SPDX or CycloneDX SBOMs
✅ You could plug them into tools like:

DependencyTrack

Anchore Enterprise

OpenSCAP

✅ Security Wins So Far
Capability	Tool
CVE Detection	Trivy, Grype
SBOM Generation	Syft, Trivy
Image Signing	Cosign
Deployment Gates	CI/CD (GitHub/GitLab)
Image Verification	Cosign Verify
Base Image Enforcement	Manual grep or CI linting
🧠 Secure by Default Mindset
You’re beginning to build a “no deploy without validation” pipeline culture — key to DevSecOps.

Every artifact must:

Declare what’s inside (SBOM)

Prove it’s safe (CVE-free)

Prove who built it (signature)

You’re not just checking a box — you’re reducing your blast radius, shortening MTTR, and creating auditability.

Let me know when you're ready for the final piece this week: the Reflection.md, where you’ll capture key learnings and prepare for IaC Security next week.

You said:
Ready
ChatGPT said:
Perfect — here’s the final file for Week 9.