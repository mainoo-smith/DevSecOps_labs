# 🔒 Week 7 Security — Container Orchestration

## Best Practices

- Never store plaintext secrets in manifests — use secret managers.
- Use RBAC for least privilege.
- Use Namespaces to isolate workloads.
- Monitor with `kubectl top` and audit logs.
- Rotate service account tokens.

---

## Real-World Scenario

In 2022, misconfigured K8s dashboards exposed admin credentials.  
Keep clusters locked down!

---

## Analogy

Kubernetes is like an air traffic control tower — without strict rules and checks, collisions happen!
