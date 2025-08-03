# 📡 Week 15 – Monitoring, Logging & Alerting

---

## 🎯 Core Learning Objectives

- Understand the pillars of observability: **Metrics, Logs, Traces**
- Deploy Prometheus, Loki, and Grafana for full-stack visibility
- Explore **AWS-native observability** with CloudWatch, CloudTrail, and GuardDuty
- Connect security events (e.g. Falco, IAM abuse, failed logins) to actionable alerts
- Build dashboards that help **DevSecOps triage threats faster**

---

## 🧠 Theory: Why Observability is Critical to DevSecOps

Security ≠ just prevention. In modern systems, **detection and response** matter just as much.

That means:

| Observability | Security Role |
|---------------|---------------|
| 📊 Metrics     | Detect anomalies (spikes, restarts, memory leaks) |
| 📜 Logs        | Detect misuse (API abuse, shell access) |
| 🔍 Traces      | Detect flow deviation or long tail latency |
| 🛑 Alerts      | Notify the right team — with enough context |

By instrumenting your apps and infrastructure with the right signals, you move from **reactive debugging** to **proactive threat detection**.

---

## 🔧 Tools Covered This Week

| Tool           | Purpose |
|----------------|---------|
| **Prometheus** | Metrics collection and alerting |
| **Loki**       | Log aggregation (like ELK but lightweight) |
| **Grafana**    | Visualization and dashboards |
| **Falco**      | Runtime security alerts (already deployed) |
| **CloudWatch** | AWS-native metrics, logs, and events |
| **GuardDuty**  | AWS threat detection (IAM misuse, DNS anomalies) |
| **SNS / EventBridge** | Alerting and automated response |

---

## 🧱 DevSecOps Tie-In

| Practice | This Week’s Coverage |
|----------|----------------------|
| **Shift Right Security** | Triage runtime events from Falco, App Logs, CloudTrail |
| **Continuous Monitoring** | Monitor CPU spikes, login failures, malicious requests |
| **Zero Trust Runtime** | Detect lateral movement and access violations |
| **Security Feedback Loop** | Use dashboards to inform hardening in CI/CD & IaC |
| **Compliance Evidence** | Show traceable, auditable evidence of alerting & logging (e.g. PCI, HIPAA)

---

## 🧩 App Evolution This Week

This week we’ll update our app to:

- Expose **custom application metrics** from the Node.js and Python services
- Stream **container logs** to Loki and/or CloudWatch
- Route **Falco alerts** and **runtime logs** into a central dashboard
- Build Grafana dashboards showing:
  - Auth failures
  - Unusual CPU/memory spikes
  - Notes service errors
  - Alerts per namespace/service
- (Bonus) Integrate GuardDuty findings into dashboards

---

## 🔐 Security Questions to Consider

- How would you detect if your app was being brute-forced?
- What metrics indicate a compromised container or function?
- Can your logs tell you *what user* did *what* and *when*?
- Are your alert thresholds tuned to avoid noise?

---

## 🛠️ Lab Structure

1. **Guided Lab**  
   - Deploy observability stack (Prometheus, Loki, Grafana)
   - Instrument the app (custom metrics + logs)
   - Add security alerting from Falco + CloudTrail + GuardDuty

2. **Challenge Lab**  
   - Simulate a brute-force or resource exhaustion attack
   - Visualize impact in Grafana + validate alert firing
   - Add an automated response (e.g., SNS → Slack or Lambda)

3. **Security.md**  
   - Explain log hygiene, alert fatigue, threat hunting, and observability for compliance

4. **Reflection.md**  
   - Connect observability work to enterprise roles
   - Update your resume and DevSecOps playbook

---

## ✅ Completion Criteria

| ✅ Item | Description |
|--------|-------------|
| 📈 Prometheus + Grafana Deployed |
| 📜 Logs from app + Falco → Loki or CloudWatch |
| 🧠 Dashboards showing key security signals |
| 🔔 Alert firing on simulated threat |
| 🤖 Optional: Alert → Slack / EventBridge auto-response |

---

## ⏭️ Next

➡️ Ready for the [`GuidedLab.md`](./GuidedLab.md)? We’ll start by deploying Prometheus + Loki via Helm, then wire up your services to emit metrics and logs.
Let me know when you're ready to proceed with the Guided Lab, and we’ll deploy your full observability stack step-by-step using Helm and AWS tools — tied to your app and its runtime security signals.

You said:
This is great, but we need to capture both application metrics and system metrics, logs and traces of requests 
ChatGPT said:
Absolutely — you’re right to insist on full-spectrum observability.

In a DevSecOps context, it's essential to capture and correlate four layers of visibility:

✅ Observability Layers to Cover
Layer	Source	Why It Matters
1. System Metrics	Node exporter, ECS/EC2 CloudWatch	Infra health (CPU, memory, disk I/O, network)
2. App Metrics	Custom /metrics endpoints (Node.js, Python), Prometheus client libraries	Request counts, error rates, latency, domain-specific KPIs
3. Logs	App logs + Falco logs → Loki or CloudWatch	Trace user actions, errors, and threats
4. Traces (Distributed)	OpenTelemetry → Tempo or X-Ray	Follow the lifecycle of a request across services
🔁 Updated Goals for the Week
In addition to our existing lab goals, we’ll now include:

Prometheus Node Exporter (for system-level metrics)

Custom Prometheus metrics in both:

🟦 auth-service (Node.js)

🐍 notes-service (Python)

OpenTelemetry SDKs added to trace:

User login/auth flows

Note creation & update

Traces visualized in Grafana Tempo or AWS X-Ray

Logs from containers and Falco routed to Loki and/or CloudWatch

Correlated dashboards to link a spike, log, and trace in a single view

📦 Tool Stack Summary
Category	Tool(s)	Notes
System Metrics	Prometheus + Node Exporter	Also AWS CloudWatch agent if on ECS/EC2
App Metrics	Prometheus client libraries (prom-client, prometheus_client)	Exposed at /metrics
Logs	Loki + Promtail, or CloudWatch logs	Sidecar or DaemonSet
Tracing	OpenTelemetry + Tempo or AWS X-Ray	Sample requests, latency, bottlenecks
Visualization	Grafana	Unified dashboarding
Security Alerts	Falco → Loki / CloudWatch / Sidekick	Runtime detection layer
🔄 Integration Across the Stack
Here's what a full request might look like:

A user logs in via the frontend

Auth-service logs the request (log file)

Emits a metric: auth_logins_total

OpenTelemetry traces request → auth → notes

CPU spike in Node exporter (system metric)

Notes-service fails due to OOM → Prometheus fires alert

Falco detects a suspicious command in notes container

Grafana shows:

Metric spike

Log trace

Falco alert

OpenTelemetry trace

This end-to-end view is what separates real DevSecOps observability from basic logging.

✅ Confirmed Additions to Guided Lab
 Deploy Prometheus + Node Exporter

 Add /metrics endpoint to Python and Node services

 Add Promtail or CloudWatch log agents

 Add OpenTelemetry SDKs + Tempo or AWS X-Ray

 Build Grafana dashboards for:

App latency, errors, throughput

System resource usage

Falco alerts + request trace

 Setup alert rules for abnormal behavior

Are you ready to begin the Guided Lab with this expanded scope?

We’ll take it step-by-step — starting with metrics (system + app), then logging, and then tracing.

Let me know and we’ll begin with a detailed Prometheus + Grafana + Node Exporter + custom metrics setup.

You said:
Sounds good 
ChatGPT said:
Perfect — let's begin the Guided Lab for Week 15, now expanded to include system metrics, application metrics, logs, and distributed traces.

We’ll proceed in 5 stages for clarity and completeness: