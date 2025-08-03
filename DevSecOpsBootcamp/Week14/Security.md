# 🔐 Week 14 Security Deep Dive – Runtime Detection with Falco, eBPF & Auditd

---

## 🎯 Goal

Understand how Falco uses eBPF, syscall hooks, and rule engines to detect malicious behavior in containers, and how that fits into a layered DevSecOps security model.

---

## 🧠 What is eBPF and Why Does It Matter?

### 🔍 eBPF = Extended Berkeley Packet Filter

eBPF allows you to run sandboxed programs in the Linux kernel **without modifying kernel source or modules**.

It enables:

- Real-time visibility into **syscalls**, **network activity**, **file access**
- **Low overhead** collection vs traditional agents
- **Safe execution** (verified before loading)

Falco uses eBPF to observe:
- `open()`, `execve()`, `bind()`, `chmod()` syscalls
- Process trees, environment variables, and command lines
- Container boundaries and image metadata

---

## 🦅 How Falco Works

### 1. **Capture**

Falco uses one of two drivers:
- Kernel Module (faster, but invasive)
- eBPF Probe (safer, portable, and modern)

It captures **syscalls** on the host and correlates them with container metadata.

### 2. **Filter**

It filters syscalls through customizable **rules** written in YAML.

Example Rule:
```yaml
- rule: Write Below /etc
  desc: Unexpected file write below /etc
  condition: evt.type=write and fd.name startswith /etc
  output: "Write below /etc by %user.name (command=%proc.cmdline)"
  priority: WARNING
3. Alert
It sends an alert:

Locally (/var/log/falco.log)

To a centralized logging system (CloudWatch, Elastic, etc.)

To falcosidekick → Slack, SIEMs, Webhooks

📦 What Falco Monitors
Event Type	Description
File Access	/etc/shadow, /tmp/exploit.sh, etc.
Process Execution	bash, nc, wget, curl, chmod +s
Network Activity	Outbound to unknown IPs, reverse shells
User Privilege	Sudo use, new users, UID switches
Container Lifecycle	Container start, exec, kill
🔬 What Auditd Offers
Auditd = Linux’s built-in syscall auditing framework.

Use it for:

Forensic logs of access to sensitive files

Compliance-driven audit trails (HIPAA, PCI)

Long-term archival of syscalls

But unlike Falco, Auditd is not real-time and has a steeper config curve.

📊 Security Benefits
🔐 Security Principle	Falco Mapping
Least Privilege	Alert on privilege escalation
Defense in Depth	Adds runtime layer beyond static scanning
Visibility & Monitoring	Observes all containers and syscalls
Incident Response	Real-time alert triage
Zero Trust Runtime	Alerts on unexpected process behavior
🧩 ECS Considerations
ECS Fargate does not support privileged containers, so Falco can’t run inside the task

Instead:

Use Falco on ECS EC2 clusters

Forward container logs to CloudWatch

Parse logs with EventBridge + Lambda for detection

Fargate limitations mean Falco is best used in dev, staging, or EC2-based clusters for deep inspection.

🔐 Rule Writing Best Practices
Write per-service policies (e.g., auth-service shouldn’t curl)

Use container.name, proc.cmdline, user.name

Use priority: ERROR or CRITICAL for real threats

Group rules into policy packs (e.g., filesystem.yaml, network.yaml)

🚨 Limitations
Challenge	Workaround
False positives	Tune rules by service
High verbosity	Route alerts to SIEM, aggregate
Fargate no support	Use logging-based detection or switch to EC2
No enforcement	Combine with OPA/Kyverno to block workloads
🛡️ Integration with Other DevSecOps Layers
Layer	Example
SBOM & Image Scan	Detects known CVEs before runtime
Policy-as-Code	Blocks insecure config before deploy
Runtime Security (Falco)	Detects container abuse or shell access
Monitoring & Alerts	Routes Falco alerts to DevSecOps dashboards
Response Automation	Triggers pod deletion, network quarantine
🧠 Summary
Falco gives you kernel-level visibility into what’s happening inside your containers and hosts.

It acts as a real-time SIEM sensor inside Kubernetes and ECS EC2

Helps catch zero-day behavior, insider threats, and misconfigured services

Complements IaC security, image scanning, and CI/CD policy enforcement

If you're building a Zero Trust DevSecOps architecture, Falco is a core building block.

⏭️ Next
➡️ Proceed to Week14/Reflection.md
We’ll consolidate key takeaways from this module, update your resume bullet, and align this skill with real enterprise security operations.


---

Let me know when you're ready for the **Reflection** section of Week 14, or if you want to simulate more advanced container attack vectors first (e.g., Docker socket misuse, crypto miners, etc.).
You said:
Yes
ChatGPT said:
Here’s your Week 14 Reflection to consolidate everything you've learned, connect it to real-world security roles, and update your resume and DevSecOps playbook.