# 🛡️ Guided Lab – Runtime Threat Detection with Falco, eBPF, and Auditd

---

## 🎯 Lab Goals

- ✅ Deploy Falco in Kubernetes and ECS environments
- ✅ Write custom Falco rules to monitor your app’s runtime behavior
- ✅ Simulate container misuse (e.g., reverse shell, netcat, file access)
- ✅ Route Falco alerts to CloudWatch or your local terminal
- ✅ Understand how Falco uses eBPF and kernel-level hooks

---

## 🧪 Part 1: Falco on Kubernetes

### 🧰 Step 1: Install Falco (Helm)

```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm repo update

helm install falco falcosecurity/falco \
  --namespace falco --create-namespace
🔍 Falco installs as a DaemonSet to monitor all pods on the node. It uses eBPF probes to capture syscalls with minimal overhead.

🔎 Step 2: View Live Alerts
kubectl logs -n falco -l app=falco -f
Try the following inside a pod:

kubectl exec -it deployment/notes-service -- bash
echo "hacked" > /tmp/hack.txt
Falco should alert on:

Shell spawned

File write in /tmp

🛠️ Step 3: Add a Custom Rule
Create custom-rules/falco-notes.yaml:

- rule: Unexpected Shell in Notes Service
  desc: Detect bash or sh shells in the notes service
  condition: container.name = "notes-service" and proc.name in ("bash", "sh")
  output: "Shell detected in notes-service (user=%user.name command=%proc.cmdline)"
  priority: WARNING
  tags: [container, shell, notes]
Apply:

kubectl create configmap falco-custom-rules \
  --from-file=custom-rules/ -n falco --dry-run=client -o yaml | kubectl apply -f -
kubectl rollout restart daemonset falco -n falco
🐳 Part 2: Falco on ECS (Fargate or EC2)
☁️ Step 1: Deploy a Sidecar or Use ECS EC2
ECS Fargate lacks full kernel access — so runtime detection is limited. For best visibility, use EC2 with ECS agent + Falco DaemonSet.

On ECS EC2:

Install Falco agent inside an EC2 instance (or sidecar with privileged access)

Or stream container logs to CloudWatch and use Falco as a centralized processor

🔥 Step 2: Simulate an Attack in ECS
Attach an interactive session to a task

Run:

nc -lvp 4444  # simulate reverse shell
cat /etc/shadow
These should trigger:

Suspicious port listen

Sensitive file read

📡 Part 3: Alert Routing
✅ Option 1: Local Logging (Dev)
Alerts appear in:

/var/log/falco.log
☁️ Option 2: CloudWatch Logging (ECS/K8s)
Edit Falco config:

program_output:
  enabled: true
  keep_alive: false
  program: "logger -p user.warning"
Ensure your system or container forwards logs to CloudWatch Logs.

🔁 Option 3: SNS/SIEM
Use falcosidekick to route alerts to:

Slack

SNS

Splunk

CloudEvent/Webhook endpoints

Deploy sidekick via:

helm install falcosidekick falcosecurity/falcosidekick \
  --namespace falco --set config.slack.webhookurl="https://hooks.slack.com/..."
📜 Part 4: Auditd (Bonus – Forensics)
Auditd helps with post-event forensics:

sudo apt install auditd -y
sudo auditctl -w /etc/passwd -p wa
This will log write attempts to /etc/passwd.

Check logs:

ausearch -f /etc/passwd
✅ Completion Checklist
✅ Task	Description
🧱 Deployed Falco in K8s or ECS	
🔔 Verified live alerts on shell or file access	
✍️ Wrote at least 1 custom detection rule	
☁️ Routed alerts to logs or Slack	
🔍 Understood syscall, eBPF, and probe behavior	
📊 Optional: Used auditd for forensic logging	
🧠 Observability Insight
Runtime threats are rare but high-impact. Falco helps catch the “unknown unknowns” that static tools miss — especially in Zero Trust or regulated environments.

⏭️ Next
➡️ Proceed to Week14/ChallengeLab.md
Simulate a real-world attack, triage the alert, and configure an automated response using EventBridge or a custom webhook.


---

Let me know when you’re ready for the **Challenge Lab**, or if you’d like to add additional detection rules for specific services or simulate more advanced intrusion techniques.
You said:
Ready 
ChatGPT said:
Perfect — let’s dive into the Challenge Lab for Week 14, where you’ll simulate a real-world attack scenario and respond using runtime security tools.