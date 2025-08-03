Title: Security Gates Up: SBOMs, CVEs, and Signed Images Across the Pipeline

🧪 Scenario
You've been tasked with:

Enforcing a production deployment policy:
No unsigned images and no critical vulnerabilities allowed in any container.

To meet this standard, you'll build and validate all 4 services (auth, notes, notifications, analytics) using:

✅ SBOMs (Syft or Trivy)

✅ CVE scanning (Trivy, Grype)

✅ Image signing (Cosign)

✅ Build failure on critical vulnerabilities

✅ Registry trust enforcement

🔧 Setup
All services live in services/:

services/
├── auth-service
├── notes-service
├── notification-service
└── analytics-service
Ensure all services have a valid Dockerfile and can be built locally.

🛠️ Challenge 1: Generate SBOMs for Each Service
Loop through each service and create SBOMs:

for service in auth-service notes-service notification-service analytics-service; do
  docker build -t noteapp/$service:dev ./services/$service
  syft noteapp/$service:dev -o json > sbom-$service.json
done
✅ Store these SBOMs as build artifacts or attach to releases.

🛠️ Challenge 2: Vulnerability Scanning and Gating
Scan each image:

for service in auth-service notes-service notification-service analytics-service; do
  echo "Scanning $service..."
  trivy image --exit-code 1 --severity CRITICAL noteapp/$service:dev || echo "$service failed security gate!"
done
✅ Any CRITICAL CVE should fail the build.

🛠️ Challenge 3: Image Signing with Cosign
Generate or reuse your cosign.key and cosign.pub.

Push and sign each image:

for service in auth-service notes-service notification-service analytics-service; do
  docker tag noteapp/$service:dev ghcr.io/<your-org>/$service:dev
  docker push ghcr.io/<your-org>/$service:dev
  cosign sign --key cosign.key ghcr.io/<your-org>/$service:dev
done
✅ Each image is now signed in the registry.

🛠️ Challenge 4: Signature Enforcement (Verification Step)
Before deploy (in CI/CD or manual step), verify each signature:

for service in auth-service notes-service notification-service analytics-service; do
  cosign verify --key cosign.pub ghcr.io/<your-org>/$service:dev
done
✅ CI fails if the signature is missing or invalid.

🛠️ Challenge 5: CI/CD Integration (Example for GitHub Actions)
Use a matrix strategy to run a reusable job across services:

jobs:
  scan-sign:
    strategy:
      matrix:
        service: [auth-service, notes-service, notification-service, analytics-service]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build & Scan
        run: |
          docker build -t ${{ matrix.service }}:dev ./services/${{ matrix.service }}
          syft ${{ matrix.service }}:dev -o json > sbom-${{ matrix.service }}.json
          trivy image --exit-code 1 --severity CRITICAL ${{ matrix.service }}:dev
      - name: Push & Sign
        run: |
          docker tag ${{ matrix.service }}:dev ghcr.io/<your-org>/${{ matrix.service }}:dev
          docker push ghcr.io/<your-org>/${{ matrix.service }}:dev
          cosign sign --key ${{ secrets.COSIGN_KEY }} ghcr.io/<your-org>/${{ matrix.service }}:dev
✅ Reusable across all microservices.

🛡️ Bonus Challenge: Approved Base Image Enforcement
Create a bash check to block Dockerfiles using disallowed base images:

grep "^FROM " services/*/Dockerfile | grep -v "python:3.11-slim"
✅ Fails pipeline if a Dockerfile uses an unapproved base.

✅ Success Criteria
Checkpoint	Passes If…
SBOM exists for each service	sbom-*.json is present
Trivy scan blocks critical CVEs	--exit-code 1 halts on high risk
Cosign signature present	verify command passes for each image
All services covered	Auth, Notes, Notifications, Analytics
CI/CD gates enforced	No unsigned or vulnerable images pass
Let me know when you’re ready for the Security.md where we’ll break down how this challenge protects against real-world threats, from Log4Shell to rogue contributors and compromised build systems.

You said:
Next 
ChatGPT said:
Great — here’s the Security.md for Week 9: Container Image Security & SBOMs, where we tie everything together by mapping what you’ve implemented to the real-world threats it protects against.