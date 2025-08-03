Title: From Build to Trust: SBOMs, CVE Scans & Signed Containers

🧪 Scenario Summary
You’ll containerize notes-service, generate an SBOM, scan the image for CVEs, sign it with Cosign, and enforce gates in GitHub Actions and GitLab CI. These practices prepare your app for secure production pipelines.

🛠️ Part 1: Generate an SBOM with Syft
🔹 Step 1.1: Install Syft
curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin
Verify:

syft version
🔹 Step 1.2: Build Your Service Image
Assume you're in services/notes-service/ with a working Dockerfile.

docker build -t notes-service:dev .
🔹 Step 1.3: Generate SBOM in JSON format
syft notes-service:dev -o json > sbom-notes-service.json
✅ Now you have a complete software bill of materials for this image.

🔹 Step 1.4: Convert to CycloneDX format (optional)
syft notes-service:dev -o cyclonedx-json > sbom-notes-service.cdx.json
Why? CycloneDX is more interoperable with external scanners and policy engines like Anchore Enterprise, OWASP Dependency-Track, etc.

🧠 Why SBOM?
Shows exact dependencies (base image packages, OS libs, node/python deps)

Required for supply chain compliance (NIST, FedRAMP, SLSA)

Enables drift detection, image diffing, and CVE correlation

🛠️ Part 2: Scan for CVEs
🔹 Option 1: Trivy (recommended)
brew install aquasecurity/trivy/trivy  # macOS
Scan for all vulnerabilities:

trivy image notes-service:dev
Scan only critical:

trivy image --severity CRITICAL notes-service:dev
Scan with SBOM:

trivy sbom sbom-notes-service.json
🔹 Option 2: Grype (Anchore)
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

grype notes-service:dev
✅ Use Grype when you already have an SBOM — it integrates deeply with Syft.

🛠️ Part 3: Sign Your Image with Cosign
🔹 Step 3.1: Install Cosign
brew install cosign  # or use GitHub releases
🔹 Step 3.2: Generate a key pair (or use keyless signing)
cosign generate-key-pair
This creates:

cosign.key (private key)

cosign.pub (public key)

🔹 Step 3.3: Tag & Push to Registry
docker tag notes-service:dev ghcr.io/<your-org>/notes-service:dev

docker push ghcr.io/<your-org>/notes-service:dev
🔹 Step 3.4: Sign the Image
cosign sign --key cosign.key ghcr.io/<your-org>/notes-service:dev
🔹 Step 3.5: Verify the Signature
cosign verify --key cosign.pub ghcr.io/<your-org>/notes-service:dev
✅ Ensures the image is exactly what was signed — no tampering post-push.

🛠️ Part 4: Add Security Gates in CI/CD
🔹 GitHub Actions .github/workflows/build.yml
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Scan with Trivy
        run: |
          docker build -t notes-service:dev .
          trivy image --severity CRITICAL --exit-code 1 notes-service:dev
🚫 Fails the build if any CRITICAL CVEs are found.

🔹 GitLab CI .gitlab-ci.yml
scan:
  stage: test
  image: aquasec/trivy:latest
  script:
    - docker build -t notes-service:dev .
    - trivy image --severity CRITICAL --exit-code 1 notes-service:dev
🔒 Add cosign verify as a step after build to enforce image trust.

✅ Success Criteria
Task	Goal
SBOM created	Generated with Syft or Trivy
CVE scan	Completed with Trivy/Grype
Build gating	CI fails on critical vulnerabilities
Image signing	Signed and verified with Cosign
SBOM published	Artifact attached or stored
Let me know when you’re ready to tackle the ChallengeLab.md, where you’ll implement end-to-end security gates across services and automate trust enforcement for real pipelines.

You said:
Proceed
ChatGPT said:
Awesome — here’s the ChallengeLab.md for Week 9: Container Image Security & SBOMs.

This lab simulates a real-world production enforcement scenario: you’ll secure, scan, sign, and gate container images for all microservices (auth, notes, notifications, analytics) — then reject any deployment that violates your security posture.