# 🔒 Week 5 Security — Real Cloud Pitfalls

## Key Practices

- Use MFA for root and IAM users.
- Apply least privilege for IAM roles.
- Restrict SSH to trusted IPs only.
- Use Bastion hosts instead of wide-open SSH.
- Tag all resources for accountability.
- Rotate keys regularly.

---

## Real-World Breach Example

In 2019, the Capital One breach happened because an over-permissive IAM role exposed data from a misconfigured firewall.  
Good IAM hygiene + secure networking = your first defense.

---

## Analogy

Cloud IAM is like your neighborhood’s master key system:  
You don’t want everyone to have keys to every house!
