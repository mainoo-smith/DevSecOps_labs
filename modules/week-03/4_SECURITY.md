````markdown
# 📁 Week 03: Secure Dockerfiles & Container Supply Chain Risks in DevSecOps

---

### 🧠 Why Container Security Matters

Containers are fast and portable—but they don’t isolate you from vulnerabilities. As a DevSecOps engineer, you’re responsible for:

* The integrity of everything in your containers.
* Preventing CVEs from leaking through Dockerfiles.
* Ensuring containers run with the least privilege.
* Monitoring for risks across the container supply chain.

---

### 🔥 Common Insecure Dockerfile Practices

| Bad Practice | Risk |
| :--- | :--- |
| `FROM ubuntu` (full base image) | Bloated with unused, potentially vulnerable packages. |
| `RUN apt install` without `--no-install-recommends` | Installs unnecessary software, increasing the attack surface. |
| Not pinning versions | Image rebuilds may bring in unverified or unstable dependencies. |
| Running as root (`USER root` or default) | Containers have full system privileges—the attack surface grows. |
| Including secrets in `ENV` or layers | Secrets can be extracted from image history. |
| Not cleaning up temp files or caches | Increases image size and exposes installation data. |
| `ADD` instead of `COPY` | `ADD` can automatically unpack archives or pull from remote URLs without validation. |

---

### ✅ Secure Dockerfile Best Practices

| Good Practice | Why It Matters |
| :--- | :--- |
| Use slim/minimal base images | Smaller attack surface (e.g., `python:3.11-slim`, `node:20-alpine`). |
| Use `COPY`, not `ADD` | Avoids implicit behavior that can lead to Remote Code Execution (RCE). |
| Use `USER` to drop root | Ensures container processes run with limited permissions. |
| Clean up caches (`--no-cache-dir`, `rm -rf /var/lib/apt/lists`) | Results in smaller, safer images. |
| Pin dependency versions (`package.json`, `requirements.txt`) | Prevents breaking changes and surprise CVEs. |
| Multi-stage builds | Keeps final images clean—no dev tools or secrets in production. |
| Use `.dockerignore` | Prevents sensitive files (e.g., `.env`, `node_modules`) from entering the image context. |

---

### 🧪 Example Comparison

#### 🔥 Insecure Dockerfile
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
````

  * Runs as root.
  * Includes `.env` file if not excluded.
  * Potentially large base image.
  * No cache cleanup.

#### ✅ Secure Dockerfile

```dockerfile
FROM python:3.11-slim

RUN useradd -m appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

USER appuser
CMD ["python", "app.py"]
```

  * Slim image.
  * Non-root user.
  * Clean install.
  * Layered security.

-----

### 🔐 Image Scanning Tools (Shift-Left CVE Detection)

| Tool | Description |
| :--- | :--- |
| **Trivy** | Scans images, Git repos, and Dockerfiles for vulnerabilities. |
| **Grype** | Open-source CVE scanner for container images and filesystems. |
| **Snyk** | Developer-friendly SCA (Software Composition Analysis) and Docker scanning. |
| **Dockle** | Linter for Dockerfiles to check for best practice violations. |

> 📌 **Pro tip:** Add these scanners to your CI/CD pipeline so vulnerabilities are caught *before* deployment.

-----

### 🔄 Runtime Flags for Container Hardening

| Flag | Description |
| :--- | :--- |
| `--read-only` | Makes the container's filesystem immutable (no writes allowed). |
| `--cap-drop=ALL` | Removes all Linux capabilities like `SYS_ADMIN` and `NET_RAW`. |
| `--no-new-privileges` | Prevents a process from escalating its privileges. |
| `--user` | Ensures the container does not run as the root user. |
| `--tmpfs /tmp` | Provides ephemeral memory for writes when needed. |
| `--security-opt apparmor:profile` | Applies additional MAC controls (like AppArmor or SELinux). |

-----

### 📦 Container Supply Chain Risks

| Risk | Example |
| :--- | :--- |
| 🧱 **Untrusted base images** | Pulling `FROM node:latest` from a public registry (could be tampered with). |
| 📦 **Dependency drift** | Packages automatically updating with new, undiscovered vulnerabilities. |
| 🔐 **Secrets baked in** | `.env` files or SSH keys committed directly into image layers. |
| 🛑 **Lack of SBOM** | No Software Bill of Materials means you have an unknown runtime footprint. |
| 🧬 **Compromised builder** | CI/CD pipelines pushing images with malicious code embedded. |

-----

### ✅ DevSecOps Supply Chain Countermeasures

| Tool | Purpose |
| :--- | :--- |
| **Trivy, Grype** | Detect known CVEs in images and dependencies. |
| **cosign, Notary** | Sign and verify trusted image authorship and integrity. |
| **SBOM generators (CycloneDX, Syft)** | Know exactly what’s inside your container images. |
| **opa, conftest, Dockle** | Enforce secure Dockerfile policies in your pipeline. |
| **CI/CD checks** | Break the build if an image has known critical CVEs or lacks a signature. |

-----

Of course, here is that content formatted as a Markdown file.

````markdown
### 🔄 Insecure vs. Secure Dockerfile

---

#### 🔥 Insecure Dockerfile

```dockerfile
FROM python:3.9

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
````

**What's wrong:**

  * Large, outdated base image (CVE exposure).
  * No user separation → runs as **root**.
  * All files copied (risk of leaking `.env`, keys, test files).
  * No cache cleanup.
  * No scan or verification steps.

-----

#### ✅ Secure Dockerfile (Fixed)

```dockerfile
FROM python:3.11-slim

# Add non-root user
RUN useradd -m appuser

WORKDIR /app

# Only copy what you need
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

USER appuser
EXPOSE 5000

CMD ["python", "app.py"]
```

**Improvements:**

  * Smaller, patched base image (less attack surface).
  * Non-root container runtime.
  * `--no-cache-dir` reduces leftover temp files.
  * Cleaner `COPY` structure.
  * Hardened defaults — ready for CI/CD scanning and deployment.

-----

### 🔐 Supply Chain Risks in Containers

Modern DevSecOps teams face indirect vulnerabilities through:

  * Base image inheritance.
  * Public package managers (PyPI, NPM).
  * Transitive dependency chains.
  * Tampered builds or layers from unverified sources.

**Real-world examples:**

  * A malicious NPM package (**event-stream**) was injected into many apps in 2018.
  * A Docker Hub image named **alpine-nginx** was backdoored in 2021.
  * In 2022, **Log4Shell** existed in thousands of container images.

-----

### 📦 Tools for Container Supply Chain Security

| Tool | Purpose |
| :--- | :--- |
| 🔍 **Trivy, Grype** | Detect CVEs and exposed secrets in images. |
| 🔏 **cosign** | Sign and verify images to ensure integrity. |
| 🧰 **Snyk, Docker Scout** | Monitor base image and dependency security. |
| 🧬 **SBOM (Software Bill of Materials)** | Track what's inside every image and where it came from. |
| 🕵️‍♂️ **Notary / Sigstore** | Cryptographic verification of image authorship and trust. |

-----

### 🛡️ Runtime Container Hardening (Recap from Guided Lab)

Add these to your `docker run` or `docker-compose.yml` files:

| Flag | Purpose |
| :--- | :--- |
| `--user appuser` | Drop root user access. |
| `--read-only` | Prevent writes to the disk inside the container. |
| `--cap-drop=ALL` | Remove Linux kernel capabilities. |
| `--security-opt no-new-privileges:true` | Prevent privilege escalation via child processes. |
| `--memory`, `--cpus` | Set resource constraints (DoS protection). |

-----

### ✅ DevSecOps CI/CD Checklist for Containers

| Stage | Check |
| :--- | :--- |
| 🛠️ **Build** | Dockerfile linting, SBOM generation. |
| 🧪 **Scan** | Trivy/Grype integrated into the pipeline. |
| 🔏 **Sign** | Sign the image with cosign. |
| 🧾 **Audit** | Keep a signed SBOM artifact in the release metadata. |
| 🔐 **Deploy** | Enforce `--read-only`, `--cap-drop`, and image digest pinning in orchestration (ECS/K8s). |

-----

### 🧩 What You Secured This Week

| Concern | Status |
| :--- | :--- |
| CVEs in base image or packages | ✅ Scanned and remediated |
| Root user containers | ✅ Replaced with `appuser` |
| Secrets in image layers | ✅ Avoided with `.dockerignore` and config injection |
| Image size bloat | ✅ Reduced with slim base + no pip/npm cache |
| Runtime misconfiguration | ✅ Locked down with Compose flags |
| Supply chain integrity | ✅ Optionally enforced with `cosign` signature |

```
```

### 🛡️ Summary: Docker + DevSecOps

| Pillar | Secure Practice |
| :--- | :--- |
| **Build** | Secure Dockerfile, slim base image, no secrets, pinned dependencies. |
| **Run** | Hardened container flags (`--user`, `--read-only`, `--cap-drop`). |
| **Deploy** | Verified image signature, SBOM, runtime monitoring. |
| **Automate** | CI/CD scanning with Trivy, cosign, and SBOM checkers. |

✅ You’re now prepared to build production-grade, secure, least-privilege containers—and enforce these policies via CI/CD or admission control.



```
```