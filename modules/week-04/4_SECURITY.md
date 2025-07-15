# 🔒 Week 4 Security — Securing the Supply Chain

## Key Points

- Use GPG signing for critical artifacts.
- Verify checksums after each build.
- Lock dependencies: use `package-lock.json` or `pom.xml` with explicit versions.
- Automate dependency scans with Trivy or Snyk.

---

## Real-World Scenario

In 2021, the Codecov supply chain attack started with an insecure artifact pipeline.  
Signing, scanning, and verifying integrity protect you and your customers.

---

## Analogy

A signed artifact is like a sealed, tamper-evident delivery.  
If the seal is broken — don’t trust it.
