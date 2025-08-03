# 🛡️ Week 14 – Runtime Security with Falco, eBPF & Auditd

---

## 🧠 Core Concept: Runtime Security

Even with secure infrastructure-as-code, hardened containers, and policy gates in CI/CD, **attacks can still happen at runtime**.

> Runtime Security = Observing and alerting on suspicious behavior after an app is deployed and running.

It gives visibility into:
- Unexpected system calls (e.g., netcat inside a container)
- File reads/writes that should never happen (e.g., `/etc/shadow`)
- New processes being spawned inside containers
- Network anomalies or privilege escalation attempts

---

## 🧱 Tools Covered

| Tool     | Purpose |
|----------|---------|
| **Falco**     | Detect suspicious behavior in real-time using syscall rules |
| **eBPF**      | Collect low-overhead runtime data from the Linux kernel |
| **Auditd**    | Track system calls for deeper audit and forensic visibility |
| **Sysdig Inspect** | (Optional) Visualize captured Falco traces interactively |
| **CloudWatch Logs** | Store and alert on runtime events at scale |
| **SIEM Integration** | (e.g., Splunk/Elastic for SOC ops) |

---

## 🎯 Learning Goals

By the end of this week, you’ll be able to:

✅ Detect and alert on container-level threats in real time  
✅ Write custom Falco rules for your application behavior  
✅ Integrate Falco into ECS and Kubernetes workloads  
✅ Understand how eBPF enables observability without agents  
✅ Use Auditd for historical forensic logs of system access  
✅ Forward alerts to centralized systems (CloudWatch, SIEMs)

---

## 🔐 DevSecOps Tie-In

| DevSecOps Principle | Runtime Security Mapping |
|---------------------|--------------------------|
| 🧪 Detect anomalies | Falco monitors syscalls live in containers |
| 📦 App awareness   | Rules are tailored to your microservices' expected behavior |
| 🔁 Feedback loop   | Alerts inform future hardening & policy improvements |
| 🧠 Least privilege | Detect if workloads violate expected behavior or access |
| 📊 Continuous Monitoring | Alerts can trigger response automation |

---

## 🧩 How This Evolves the App

This week, you’ll:

- Attach **Falco sidecars** to services like `notes-service` and `auth-service`
- Define **custom Falco rules** per service:
  - e.g., "Auth-service should never spawn `bash`"
- Use **CloudWatch or a SIEM** to store and review alerts
- Simulate intrusion behavior (e.g., reverse shell, base64 decoding, etc.)
- Optionally pipe into an **automated blocking system** using EventBridge or AWS Lambda

---

## 🗂️ Modules This Week

| File | Purpose |
|------|---------|
| `GuidedLab.md` | Install, configure, and customize Falco for ECS and K8s |
| `ChallengeLab.md` | Simulate a real-world container escape + alert triage |
| `Security.md` | Deep dive into syscall-level monitoring, eBPF, and how Falco compares |
| `Reflection.md` | Reflect on tradeoffs between signal, noise, and response time |

---

## 🧠 Theory Snapshot: What is eBPF?

**eBPF (Extended Berkeley Packet Filter)** lets you run sandboxed programs inside the Linux kernel to safely and efficiently observe (or block) kernel-level events.

It powers modern observability tools like:
- Cilium (network policies)
- Falco (runtime detection)
- BCC/bpftrace (kernel tracing)

Why it matters:  
> eBPF enables deep visibility **without modifying your app** or container.

---

## 🔄 Integration Plan

You’ll add **runtime detection** to your existing services like this:

+------------------------+

Auth Service (Pod)
Node.js App
AWS SDK + IAM
Falco Sidecar 🔍
+------------------------+
    👇 alerts

[CloudWatch Logs]
         ↓
[EventBridge Rule]
         ↓
  [SNS / Slack / SIEM]

---

## 📘 Real-World Relevance

Runtime detection is critical for:

- **Zero-day threats** bypassing static analysis
- **Insider threats or compromised workloads**
- **Red team simulations**
- Meeting compliance like **PCI DSS**, **SOC 2**, **HIPAA**

---

## ✅ Completion Criteria

By the end of this week, you should have:

- [ ] Deployed Falco as a sidecar or daemonset
- [ ] Written at least 3 custom detection rules per service
- [ ] Forwarded alerts to logging system or alert handler
- [ ] Validated behavior by simulating container misuse
- [ ] Understood the basics of syscall monitoring with eBPF

---

## ⏭️ Next Up

➡️ Proceed to [`Week14/GuidedLab.md`](./GuidedLab.md)  
We’ll install Falco and begin observing real container behavior in your app.

Let me know when you're ready for the Guided Lab, where we'll deploy Falco, simulate suspicious behavior, and write detection rules tied to your services.

You said:
Ready 
ChatGPT said:
Awesome — let’s begin the Guided Lab for Week 14: Runtime Security with Falco, eBPF & Auditd. We’ll cover both Kubernetes and ECS setups, simulate common threats, and write custom Falco rules.