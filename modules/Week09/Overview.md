Title: 🐳 Container Image Security & SBOMs – Know What You Ship

🎯 Goal
By the end of this week, you will:

Generate SBOMs (Software Bills of Materials) for your container images

Scan images for vulnerabilities using tools like Trivy, Grype, and Docker Scout

Automate CVE scanning in GitLab CI, GitHub Actions, and CodeBuild

Enforce vulnerability gates in your pipeline

Understand how to sign and verify container images for trust and provenance

🧠 Why This Week Matters
Most modern applications are built on top of dozens of base images and open-source layers, which can include:

Vulnerable libraries (e.g., Log4Shell)

Misconfigured packages (e.g., SSH enabled in Alpine)

Outdated dependencies with public CVEs

Binaries you didn’t even know were included

You can’t secure what you don’t know you’re shipping.

That’s why we use SBOMs and image scanners — to illuminate the supply chain and block bad builds before they hit production.

📚 Core Concepts & Theory
1. 🧾 What Is an SBOM?
A Software Bill of Materials is a manifest of every package, binary, and dependency that exists inside your application or image.

It answers:

What’s in this container?

Where did it come from?

Is it vulnerable or outdated?

Example tools:

Syft (by Anchore)

Trivy

Docker Scout

Formats:

SPDX

CycloneDX

Syft JSON

2. 🚨 CVE Scanning: Detecting Vulnerabilities in Images
CVE (Common Vulnerabilities and Exposures) are published weaknesses in software libraries.

Container scanners work by:

Analyzing the file system and installed packages

Comparing against CVE databases (NVD, GitHub Advisory, etc.)

Producing severity-based reports (Critical, High, Medium, Low)

Popular scanners:

Tool	Features
Trivy	Fast, covers OS + language deps, SBOM + CVE
Grype	SBOM-first, good CycloneDX/SPDX support
Docker Scout	Built-in to Docker, easy for quick checks
Clair	Integrates with registries, good for Harbor
Snyk	SaaS-focused, Git integration
3. 🔄 Image Signature & Provenance
Image signing ensures that:

The image hasn’t been tampered with

The image was built and pushed by a trusted party

Tooling:

Cosign (part of Sigstore)

Docker Content Trust

Notary v2

You’ll explore:

How to sign your image during build

How to verify signature at deploy

How to enforce only signed images can be deployed

4. 🛡️ Policy Gates in CI/CD
You’ll enforce security gates like:

Gate	Enforcement
No Critical CVEs	Block pipeline
All images signed	Require Cosign verify
SBOM uploaded	Required for artifacts
Approved base image	Dockerfile check or whitelist
Version drift detected	Notify or fail
Example: GitLab CI + Trivy gate

script:
  - trivy image --exit-code 1 --severity CRITICAL my-image:latest
🧩 How This Evolves the App
Your secure note/task app now builds images that are:

Upgrade	Benefit
SBOM included in pipeline	Full supply chain traceability
Trivy & Grype scans	Vulnerabilities caught early
Image signing (Cosign)	Tamper-proof deployment pipeline
Deployment gating	No unscanned or unsigned images reach prod
✅ By End of Week 9, You’ll Be Able To:
Generate and include SBOMs for every image you build

Automate CVE scanning across GitHub, GitLab, and AWS CodeBuild

Fail builds if critical vulnerabilities are found

Sign and verify your own container images

Build pipelines that only deploy known-safe images

🔜 Ready for the GuidedLab.md, where you’ll:

Build and scan your container image

Generate and publish an SBOM

Gate deployments based on CVE scan severity

Use Cosign to sign and verify the image before deployment

Shall we proceed?

You said:
Proceed
ChatGPT said:
Excellent — let’s move into the Week 9 Guided Lab on Container Image Security & SBOMs.