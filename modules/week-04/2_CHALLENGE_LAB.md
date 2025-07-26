````markdown
# 📁 Week04/ChallengeLab.md – Break the CI/CD Pipeline & Enforce Security Gates

---

## 🎯 Challenge Objective

You will:

* **Intentionally break the CI/CD pipeline by:**
    * Introducing critical vulnerabilities
    * Removing signing or pushing unsigned images
* **Force the pipeline to stop deployments if:**
    * CVEs exceed your policy threshold (e.g., critical/high)
    * The image is not signed
* **Fix the breakage and demonstrate DevSecOps resiliency:**
    * Patch the vulnerable dependency
    * Add back image signing
    * Enforce conditional logic (e.g., if scan fails, do not deploy)

---

## 🧪 Step 1: Introduce a Vulnerability

In the `backend`, update `requirements.txt` with an insecure Flask version:

```txt
Flask==0.12
````

This version is vulnerable to:

  * CVE-2018-1000656 (XSS and path traversal)

Rebuild your image:

```bash
docker build -t insecure_backend ./backend
```

-----

## 🔍 Step 2: Push Insecure Code to GitHub or GitLab

Commit and push the update to `main`.
Your pipeline should fail at the scan step:

  * Trivy or Grype will detect critical/high CVEs
  * If `exit-code: 1` is used in the scan job (as we configured), the job will stop

📌 **If the pipeline does not fail, check:**

  * Does your scan job use `exit-code: 1`?
  * Are you targeting the right image?
  * Are `CRITICAL` and `HIGH` in your severity flags?

-----

## 🔐 Step 3: Try to Push Without Signing

Comment out or remove the `cosign sign` step in your pipeline.
This simulates a compromised pipeline trying to bypass image verification.
Then push again.

**Expected result:**

  * Your deploy job should fail or skip because the image is unsigned.

-----

## 🔐 Step 4: Enforce Signature Check in CI/CD

Add a verification gate (optional but advanced):

**GitHub Actions**

```yaml
- name: Verify image signature
  run: |
    cosign verify --key cosign.pub $IMAGE_NAME:latest
```

**GitLab CI**

```yaml
verify:
  stage: sign
  image: ghcr.io/sigstore/cosign
  script:
    - cosign verify --key cosign.pub $IMAGE_NAME:latest
```

This ensures only signed images reach your registry or deploy job.

-----

## ✅ Step 5: Fix the Vulnerability

In `backend/requirements.txt`, revert to a safe version:

```txt
Flask==2.3.3
```

Then:

```bash
docker build -t backend ./backend
```

Scan again to verify the CVEs are resolved:

```bash
trivy image backend
```

-----

## ✅ Step 6: Restore Secure Signing

Make sure:

  * `cosign.key` exists in your secrets or CI/CD variables
  * `cosign sign` runs after the build

Push the image again. The full pipeline should now pass ✅

-----

## 📄 Write a Postmortem Report

### 📄 `pipeline-hardening-summary.md`

```markdown
## Summary

### Incident
- CI/CD pipeline allowed image with critical Flask CVE (Flask 0.12)
- Signing step was removed accidentally
- Insecure image nearly pushed to production

### Response
- Scan step blocked build via `Trivy`
- Signature verification gate added
- CVE remediated by upgrading to Flask 2.3.3
- Cosign signing and verify steps re-enabled

### Improvements
- Added verify stage to CI/CD
- Audit log shows all image push attempts
- Created policy for critical/high CVEs to block deploys

### Lessons Learned
- DevSecOps requires continuous monitoring of all build-time security controls
```

-----

✅ **Challenge Complete.**
You’ve now broken, fixed, and hardened your container pipeline — a realistic and essential DevSecOps capability.

```
```