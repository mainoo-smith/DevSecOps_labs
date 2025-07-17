# Security – Week 2: Remote Access & OS Hardening

---

## 🚨 Risks If Not Secured:

- **Root login**: One misstep = full system compromise
- **Password-based SSH**: Susceptible to brute-force
- **Open ports**: Unused ports are breach opportunities
- **Unpatched system**: Known exploits may be used

---

## 🔐 Security Best Practices:

| Area | Recommendation |
|------|----------------|
| SSH | Disable root login, use keys only |
| Firewall | Only open ports you use (start with 22, 80, 443) |
| Fail2Ban | Block brute-force IPs |
| Users | Principle of least privilege |
| Monitoring | Use `auditd`, `ufw status`, logs |

---

## 🔑 Bonus Tools to Explore

- `auditd`
- `clamav`
- `chkrootkit`


===================================================
# Security – Week 2

## Why It Matters:

- Your EC2 server will be the first entry point for deploying real code
- Without SSH hardening, anyone can try brute force attacks
- Without monitoring, your app could silently crash

## Best Practices:

- Disable root login
- Use `AllowUsers` in SSH
- Apply firewalls for minimal ports
- Use `fail2ban` for brute force detection
- Log all cron and system activity