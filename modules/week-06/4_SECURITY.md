# 🔒 Week 6 Security — Container Supply Chain

## Best Practices

- Keep base images minimal & updated.
- Never store secrets in images.
- Always scan images for known CVEs.
- Sign & verify images (Sigstore/Cosign).
- Pin image versions in Compose/Helm.

---

## Real-World Scenario

In 2021, attackers exploited insecure containers with embedded secrets to pivot into cloud environments.  
Always assume your image will be reused — protect your supply chain.

---

## Analogy

A container without scanning or signing is like shipping a box overseas with no customs seal.  
Anyone can tamper with it!
