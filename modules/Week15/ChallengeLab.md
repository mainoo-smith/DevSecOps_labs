# ⚔️ Week 15 Challenge Lab – Simulated Security Incident & Observability Validation

---

## 🧠 Scenario Overview

An attacker is attempting to brute-force login credentials on your `auth-service`. Your DevSecOps goal is to:

1. Detect the attack via **metrics** (rate spikes)
2. Investigate the source via **logs**
3. Trace the request path via **OpenTelemetry**
4. Trigger an **alert**
5. Respond automatically or manually
6. Correlate all findings in **Grafana**

---

## 🎯 Objectives

| Goal | Success Indicator |
|------|-------------------|
| Detect abnormal activity | Spike in login failures metric |
| Confirm via logs | Multiple failed login attempts |
| View trace path | Slow response spans or retries |
| Trigger alert | Slack/Email or EventBridge fires |
| (Optional) Respond | Block IP or tag source |
| Dashboard correlation | Metrics, logs, traces line up visually |

---

## 🛠️ Step 1: Simulate Brute Force

You can use a script or a tool like `hydra`, `ab`, or curl in a loop.

### A. Simulate failed login loop

```bash
for i in {1..50}; do
  curl -X POST http://localhost:3000/login \
    -H "Content-Type: application/json" \
    -d '{"username":"user'$i'", "password":"wrong"}'
done
✅ This will:

Spike your auth_login_failures_total counter

Emit 401 Unauthorized logs

Generate traces if OpenTelemetry is hooked in

📊 Step 2: Monitor Metrics in Grafana
Query:

rate(auth_login_failures_total[1m])
✅ You should see a sharp increase, confirming abnormal behavior.

📜 Step 3: Investigate Logs (Loki)
Go to Explore → Loki

Query:

{app="auth-service"} |= "LOGIN FAILED"
Add filters:

By IP address

By user

By timestamp

✅ Correlate logs with spike time.

🔍 Step 4: Analyze Traces
Go to Explore → Tempo

Query by service.name = "auth-service"

Check recent traces

Look for:

High response times

Repeated failed auth attempts

Request path from frontend → auth

🚨 Step 5: Validate Alerting
Go to Alerting → Alert Rules

Your rule should fire:

rate(auth_login_failures_total[1m]) > 10
Notification:

Slack, Email, or AWS SNS

✅ Alert should include:

Timestamp

Affected service

Failure count

🛡️ Step 6: Optional Response (AWS or Manual)
If using AWS:

Create EventBridge Rule:

Trigger Lambda function that:

Tags source IP

Updates WAF rule

Sends to SecurityHub

If local:

Log offending IP

Block with iptables or security group update

✅ Completion Checklist
✅	Task
🟢 Attack simulated	
🟢 Metrics spike visible	
🟢 Logs show failed login attempts	
🟢 Traces capture offending requests	
🟢 Alert fired in Grafana	
🟡 (Optional) Response triggered	
🧠 Observability system validated	
🔁 DevSecOps Reflection
Aspect	Outcome
🔍 Detection speed	How fast did metrics/logs detect it?
🧩 Correlation	Were you able to link metrics ↔ logs ↔ traces?
⏱️ Response time	How quickly did alerts reach you or trigger?
🧠 Clarity	Were dashboards easy to interpret?
🔐 Gaps	Any missing signals or delays?
🧭 Suggested Next Steps
Set rate-based alerts for any POST /login failures over threshold

Use Grafana annotations to mark attack windows

Set up request ID propagation for even tighter correlation

Create a runbook for similar future incidents


---

Let me know when you’re ready for the **Security.md** and **Reflection.md** files to close out Week 15. These will highlight the **theory, defense principles, and takeaways** from what you just practiced.
You said:
Ready 
ChatGPT said:
Excellent — here’s the Security.md file for Week 15, focused on the DevSecOps theory behind observability: what threats it helps mitigate, how telemetry supports security operations, and how your stack enforces defense-in-depth principles.