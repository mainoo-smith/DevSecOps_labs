– Fixing Vulnerable Containers & Implementing Image Assurance
🎯 Challenge Objective
You’ll simulate a real-world DevSecOps incident:

Intentionally build a vulnerable image

Scan and detect critical/high CVEs using Trivy or Grype

Harden the Dockerfile by:

Reducing dependencies

Upgrading base images

Applying multi-stage builds

Optionally: verify image integrity with signing (cosign) or digests

🔧 Step 1: Build a Vulnerable Container
Let’s modify the backend to use a bad practice: outdated base image + running as root.

Edit backend/Dockerfile.bad:

FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
Build the image:

docker build -f backend/Dockerfile.bad -t insecure_backend ./backend
🧪 Step 2: Scan for CVEs
🔹 Using Trivy:
trivy image insecure_backend
Or with Grype:

grype insecure_backend
🔍 You should see:

Critical/high CVEs in base OS packages (glibc, openssl, etc.)

No user separation (root execution)

Possibly outdated Python or Flask versions

🛠️ Step 3: Fix and Harden
Now fix the Dockerfile:

Use python:3.11-slim (updated)

Add USER appuser

Reduce layers and remove cache

(Optional) Pin exact versions

✅ Hardened backend/Dockerfile (Final Secure Version):
FROM python:3.11-slim

RUN useradd -m appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

USER appuser
EXPOSE 5000

CMD ["python", "app.py"]
Rebuild:

docker build -f backend/Dockerfile -t secure_backend ./backend
trivy image secure_backend
You should now see fewer/no critical CVEs, and Trivy should report user=appuser ✅

🔐 Bonus: Use Cosign to Sign & Verify Image
Image signing allows you to prove integrity and enforce signature checks in CI/CD or registries.

1. Install Cosign
brew install cosign               # Mac
go install github.com/sigstore/cosign@latest
2. Generate a keypair
cosign generate-key-pair
# Produces cosign.key and cosign.pub
3. Sign the image
cosign sign --key cosign.key secure_backend
4. Verify the image signature
cosign verify --key cosign.pub secure_backend
✅ This enables image attestation and can be integrated with registries (e.g., ECR, GHCR, Docker Hub) and admission controllers (e.g., Kyverno, OPA).

📋 Write Postmortem Notes
📄 image-hardening-summary.md

## Problem

- Used outdated Python base image (python:3.9)
- Ran container as root
- Vulnerabilities included OpenSSL CVEs and user privilege escalation

## Fixes Applied

- Upgraded to python:3.11-slim
- Dropped root user, added non-root `appuser`
- Removed pip cache, slimmed image size
- Verified no critical CVEs with Trivy

## Optional Assurance

- Signed image with Cosign
- Verified image integrity via `cosign verify`
✅ Challenge complete!

You’ve now gone from insecure → secure → verifiable container images — a core skill for any DevSecOps engineer building for production.

🔜 Next:

Security.md: Dockerfile best practices, dependency risk, container supply chain

Reflection.md: Lessons for ECS and Kubernetes security layers

Proceed?

You said:
Challenge lab
ChatGPT said:
You've already completed the Challenge Lab for Week 3 — where you:

✅ Intentionally built a vulnerable container
✅ Scanned it with Trivy or Grype
✅ Hardened the Dockerfile (upgraded base image, dropped root, added slim layers)
✅ (Optionally) signed and verified it with cosign
✅ Documented the hardening in image-hardening-summary.md

If you'd like to continue, the next file is:

🔐 Week03/Security.md – Dockerfile Best Practices & Container Supply Chain Risks

Would you like to proceed to the Security section, or revisit any part of the Challenge Lab?

You said:
Security 
ChatGPT said: