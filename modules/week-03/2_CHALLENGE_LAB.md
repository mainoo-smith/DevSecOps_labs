````markdown
# 🎯 Challenge: DevSecOps Image Hardening

This challenge simulates a real-world DevSecOps incident where you'll find, fix, and verify vulnerabilities in a Docker container image.

---

## Challenge Objective

You’ll simulate a real-world DevSecOps incident:

* Intentionally build a vulnerable image.
* Scan and detect critical/high CVEs using **Trivy** or **Grype**.
* Harden the Dockerfile by:
    * Reducing dependencies
    * Upgrading base images
    * Applying multi-stage builds
* Optionally: verify image integrity with signing (**cosign**) or digests.

---

## 🔧 Step 1: Build a Vulnerable Container

Let’s modify the backend to use a bad practice: an outdated base image and running as the **root** user.

Edit `backend/Dockerfile.bad`:

```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
````

Build the image:

```bash
docker build -f backend/Dockerfile.bad -t insecure_backend ./backend
```

-----

## 🧪 Step 2: Scan for CVEs

Now, scan the image you just built to find its security flaws.

🔹 **Using Trivy:**

```bash
trivy image insecure_backend
```

🔹 **Or with Grype:**

```bash
grype insecure_backend
```

🔍 **You should see:**

  * Critical/high CVEs in base OS packages (e.g., glibc, openssl).
  * No user separation (root execution).
  * Possibly outdated Python or Flask versions.

-----

## 🛠️ Step 3: Fix and Harden

Now, let's fix the `Dockerfile` to make it more secure.

  * Use `python:3.11-slim` (an updated and smaller base image).
  * Add a non-root user `appuser`.
  * Reduce layers and remove the pip cache to slim the image.
  * (Optional) Pin exact package versions in `requirements.txt`.

✅ **Hardened `backend/Dockerfile` (Final Secure Version):**

```dockerfile
FROM python:3.11-slim

# Create a non-root user
RUN useradd -m appuser
WORKDIR /app

# Install dependencies without caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Switch to the non-root user
USER appuser
EXPOSE 5000

CMD ["python", "app.py"]
```

Rebuild with the secure Dockerfile and rescan it:

```bash
# Build the secure image
docker build -f backend/Dockerfile -t secure_backend ./backend

# Rescan with Trivy
trivy image secure_backend
```

You should now see fewer (or no) critical CVEs, and Trivy should report `user=appuser` ✅.

-----

## 🔐 Bonus: Use Cosign to Sign & Verify Image

Image signing allows you to prove integrity and enforce signature checks in your CI/CD pipeline or image registry.

#### 1\. Install Cosign

```bash
# For Mac
brew install cosign

# Or with Go
go install [github.com/sigstore/cosign@latest](https://github.com/sigstore/cosign@latest)
```

#### 2\. Generate a keypair

This command produces two files: `cosign.key` (your private key) and `cosign.pub` (your public key).

```bash
cosign generate-key-pair
```

#### 3\. Sign the image

Use your private key to sign the secure image.

```bash
cosign sign --key cosign.key secure_backend
```

#### 4\. Verify the image signature

Use the public key to verify that the image hasn't been tampered with since it was signed.

```bash
cosign verify --key cosign.pub secure_backend
```

✅ This enables image attestation and can be integrated with registries (e.g., ECR, GHCR, Docker Hub) and admission controllers (e.g., Kyverno, OPA).

-----

## 📋 Write Postmortem Notes

Create a summary file named `image-hardening-summary.md` to document the incident.

```markdown
## Problem

- Used an outdated Python base image (`python:3.9`).
- Ran the container as the **root** user.
- Vulnerabilities included OpenSSL CVEs and potential for user privilege escalation.

## Fixes Applied

- Upgraded to `python:3.11-slim` to reduce the attack surface.
- Dropped the root user and added a non-root `appuser`.
- Removed the pip cache with `--no-cache-dir` to slim the final image size.
- Verified that no critical CVEs remained using Trivy.

## Optional Assurance

- Signed the final image with Cosign to ensure its integrity.
- Verified the image signature using `cosign verify`.
```

✅ **Challenge complete\!**

You’ve now gone from an **insecure** → **secure** → **verifiable** container image — a core skill for any DevSecOps engineer building for production.

```
```