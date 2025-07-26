```markdown
# 📁 Week04/Security.md – CI/CD Pipeline Hardening & Attack Surface Reduction

---

## 🧠 Why CI/CD Security Is Critical

In DevSecOps, your CI/CD pipelines are production's front door.
If an attacker:

* Pushes malicious code
* Bypasses a scan
* Leaks secrets via CI logs

→ they can ship insecure builds directly into production.
CI/CD pipelines must be treated like production infrastructure: monitored, gated, auditable, and least-privilege.

---

## 🕷️ Common CI/CD Vulnerabilities

| Vulnerability                   | Real-World Example                                            |
| :------------------------------ | :------------------------------------------------------------ |
| 🗝️ Leaked secrets in logs        | AWS keys printed by `echo` or bad scripts                     |
| 🧪 Disabled scanners            | Developers disable Trivy/Grype to pass builds                 |
| ⚠️ Insecure runner permissions  | GitLab runner with full Docker access = root on host          |
| 🐍 Pulling unverified dependencies | CI fetches code from GitHub/GitLab without checksum/signature |
| 🏷️ Image tags like `:latest`     | Deployment inconsistency or rollback to vulnerable versions   |
| 🔄 Unverified third-party actions | GitHub workflows using compromised community actions        |
| 🧬 SBOM missing or ignored        | No visibility into image contents for compliance/security     |

---

## 🔐 Best Practices for Secure Pipelines

| Category           | Best Practice                                                                                                      |
| :----------------- | :----------------------------------------------------------------------------------------------------------------- |
| **Secrets** | Use built-in secrets managers (e.g., GitHub Secrets, GitLab CI variables, AWS Secrets Manager). Never `echo` secrets. |
| **Image Security** | Scan Dockerfiles and images in CI (Trivy, Grype). Break build on CVE threshold.                                    |
| **Runner Hardening** | Run on ephemeral, isolated runners. Avoid `privileged: true`. Use separate runners per project/team.               |
| **Image Signing** | Use `cosign` to sign all images. Verify signatures before deploy.                                                  |
| **Artifact Management** | Store and track SBOMs, scan reports, image digests, and deployment metadata.                                       |
| **Branch Protections** | Enforce review + scan gates before merge. Require PR status checks.                                                |
| **Trusted Sources Only** | Use vetted, version-pinned GitHub Actions and Docker base images.                                                  |
| **Logging + Audit Trails** | Keep logs for every scan, signature, build, and deploy — with timestamps and checksums.                            |

---

## 🔄 CI/CD Security Flow (Shift-Left Policy Enforcement)

```

```
    Dev Commit ➜ CI Trigger ➜
     ┌────────────┐
     │  Lint Code │
     └────┬───────┘
          ↓
    ┌─────────────┐
    │  Build      │
    └────┬────────┘
          ↓
  ┌────────────────┐
  │  Trivy/Grype   │ ⇦ scan fails = STOP
  └────┬───────────┘
        ↓
  ┌────────────────┐
  │ Sign with Cosign│ ⇦ required before push
  └────┬───────────┘
        ↓
 ┌─────────────────┐
 │ Push to Registry│
 └────┬────────────┘
       ↓
 ┌────────────────────┐
 │ Deploy if Verified │ ⇦ signature + digest match
 └────────────────────┘
```

```

---

## 🔐 Securing GitHub Actions

| Action                      | Why                                                                       |
| :-------------------------- | :------------------------------------------------------------------------ |
| `permissions:` field        | Explicitly define token permissions (`contents: read`, `packages: write`, etc.) |
| `trusted: true` actions     | Use verified, pinned third-party actions only                             |
| Avoid `env:` for secrets    | Use `secrets.X` rather than hardcoded `env:`                              |
| Enable required checks      | Enforce that all CI jobs pass before merge                                |
| Restrict `workflow_dispatch` | Use with role-based triggers only (avoid PR auto-runs from forks)         |

---

## 🔐 Securing GitLab CI/CD

| Practice           | Description                                                                 |
| :----------------- | :-------------------------------------------------------------------------- |
| **Scoped Variables** | Use protected, masked, and environment-scoped variables                     |
| **Runner Isolation** | Use dedicated runners with network, volume, and access controls             |
| **Tags + Approvals** | Require merge requests to pass scan jobs + human approval                 |
| **Environment Protection** | Prevent CI/CD jobs from deploying to prod without a secure pipeline gate    |
| **Secrets Scanning** | Enable GitLab’s built-in secrets detection for new commits                  |

---

## 🛡️ DevSecOps CI/CD Policy-as-Code

Pipelines should encode your security policy, not bypass it:

| Policy                           | Implementation                                                                 |
| :------------------------------- | :----------------------------------------------------------------------------- |
| No unsigned images in prod       | Require `cosign verify` step before deploy                                     |
| No CVEs > HIGH                   | `trivy image --exit-code 1 --severity CRITICAL,HIGH`                           |
| Only SBOM-verified images        | Store `sbom.json` as artifact + validate                                       |
| Require peer review              | GitHub PR protection or GitLab MR approvals                                    |
| Enforce minimal base images      | Dockle or Trivy Dockerfile check                                               |
| Block secrets in history         | `git-secrets`, TruffleHog, or GitHub Advanced Security                         |

---

## ✅ Summary

You now understand how to secure your CI/CD pipelines by:

* Enforcing scan gates, signature checks, and hardening steps
* Treating secrets as first-class assets
* Running pipelines as code-defined, auditable security controls
* Blocking unverified, unsafe, or non-compliant artifacts

This is what separates DevOps from DevSecOps — pipelines are no longer just for speed; they’re security policy automation layers.
```