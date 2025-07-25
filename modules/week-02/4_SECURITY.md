📁 Week02/Security.md – Network Security in DevSecOps: Layered Threats, Tools, and Mitigation Strategies

⸻

🧠 Why Network Security is Critical in DevSecOps

Even with perfect code and secure configurations, an exposed port or misrouted packet can open the door to attackers.

As a DevSecOps Engineer, you are responsible for:
	•	Ensuring only the right systems and services can talk to each other
	•	Auditing and controlling ingress/egress
	•	Building defense-in-depth across network layers
	•	Detecting and preventing lateral movement, port scanning, and service exposure

⸻

🌐 Understanding Network Layers (L3–L7)

OSI Layer	Name	DevSecOps Relevance
L3	Network	IP routing, firewall rules, subnets
L4	Transport	TCP/UDP ports, NAT, connection limits
L7	Application	HTTP, gRPC, DNS — vulnerable to injection, protocol abuse

Attackers often move from L3 → L7 as they escalate:
	•	L3/L4: Use port scans (nmap) to find listening services
	•	L4/L7: Exploit open services (e.g., insecure API, default creds)
	•	L7: Abuse protocols (e.g., SSRF, DNS tunneling, HTTP flooding)

⸻

🚨 Common Network Threats

Threat	Example	Detection / Prevention
Open Ports	Backend service on 0.0.0.0	nmap, ss, ufw
Port Scanning	nmap -sS or masscan from attacker	Firewall logging, rate limiting
Lateral Movement	Exploiting shared network or trust zones	Segment with firewalls and least privilege
Egress Abuse	Malware calling out via HTTP	Egress filtering, DNS monitoring
Protocol Abuse	SSRF, gRPC injection	Web firewalls, request validation
Misrouted Traffic	VPC misconfig, service exposed	Network policy enforcement (ECS/K8s)


⸻

🔐 DevSecOps Network Defenses

Defense	What It Does
🔒 Host Firewalls (ufw, iptables)	First line of defense on every VM/container
🌐 VPC Security Groups / NACLs	Cloud-native firewall controls at L3/L4
🧱 Kubernetes NetworkPolicies	Pod-level firewall rules (namespaced)
🔌 ECS Service Connect	Namespaced, service-specific routing inside ECS
🚦 TLS Everywhere	Encrypts traffic and prevents sniffing or tampering
📈 Flow Logging	Detects anomalies (e.g., CloudWatch Logs, VPC Flow Logs)
📜 CI/CD Validation	Static checks on ufw, iptables, SGs, etc.


⸻

🔧 Tools You Should Know

Tool	Purpose
ufw, iptables	Host-level ingress/egress control
nmap, netcat (nc)	Port scanning and socket probing
ss, netstat	View open ports and listening services
tcpdump, wireshark	Deep packet inspection
AWS VPC Flow Logs	Detect unexpected IP or port communication
Kubernetes NetworkPolicy	Control which pods/services can talk to each other


⸻

🧪 Real-World Patterns to Defend Against

Red Team Tactic	What They Look For	Your Defense
Port scanning	Exposed high ports (5000–9000)	ufw, rate limit, alert
Weak segmentation	Service A → Service B freely	Create deny-all defaults + allowlists
Exposed staging/dev	Incomplete firewall rules in non-prod	Replicate prod firewall config in CI/CD
Proxy chaining	Port forwarding to internal APIs	Restrict local listeners and use mTLS
Egress data exfiltration	Internal → External over HTTP/443	Use egress firewall with URL filtering


⸻

🧩 Applying Zero Trust to Network Security

Zero Trust = “Never trust, always verify”

In network terms:
	•	Every service should authenticate and authorize before communicating
	•	Traffic should be encrypted and observable
	•	Firewalls should default to deny — only explicit paths are allowed
	•	Even within the same subnet/VPC/pod group, traffic should be audited

This mindset prepares you to design segmented microservice environments using:
	•	ECS Service Connect namespaces
	•	Kubernetes NetworkPolicies
	•	Sidecars with policy enforcement (e.g., Istio + OPA)

⸻

🛠️ DevSecOps Pipeline Tip

Include checks like:

# Block deployment if any port > 1024 is exposed without reason
if ss -tuln | grep ':5[0-9][0-9][0-9]'; then
  echo "Port 5xxx exposed — block pipeline."
  exit 1
fi

Also scan Dockerfiles for EXPOSE 0.0.0.0.