📁 Week02/Reflection.md – Review, Takeaways, and Preparing for Secure Containerization

⸻

🔁 What You Did This Week

✅ Simulated two isolated microservices (frontend and backend) on the same Linux host
✅ Enforced host-based firewall rules to restrict access to only required ports
✅ Detected and patched a real-world misconfiguration: backend exposed on 0.0.0.0
✅ Explored Layer 3–7 threats, including port scans, lateral movement, and protocol abuse
✅ Practiced DevSecOps thinking around “secure by default” network posture
✅ Documented network policy assumptions and recommendations for future environments (ECS/K8s)

⸻

🧠 Key Concepts to Remember

Concept	Why It Matters
Network segmentation	Prevents an attacker from moving freely across services
Ingress & egress filtering	Controls both who can reach the app and where it can talk
Host-based firewalls	Lightweight first-line defense — often forgotten in cloud-native setups
Layer 3–4 awareness	Port and protocol security (e.g., TCP/UDP, NAT)
Layer 7 exposure	APIs and HTTP services are vulnerable even if the network is locked
Zero Trust Networking	Every connection must be explicitly allowed and auditable


⸻

❓ Self-Check Questions
	1.	Why is it risky for a backend service to bind to 0.0.0.0 instead of 127.0.0.1?
	2.	What’s the difference between a host firewall (ufw) and a cloud-native security group (e.g., AWS SG)?
	3.	How does a DevSecOps pipeline detect exposed or misconfigured ports?
	4.	What does “least privilege” mean when applied to network access?
	5.	How can you stop lateral movement between services within the same VPC or host?

⸻

🧩 DevSecOps in the Real World

“The biggest breaches often start with a tiny misconfiguration.”

— Security Engineer, Capital One Breach 2019

In real DevSecOps practice:
	•	Port scanning is used during red team assessments and by real attackers
	•	Services exposing debug ports (e.g., :8000, :5000, :9000) are routinely exploited
	•	Many companies fail to replicate production firewalls in dev/staging environments
	•	Container environments (like ECS and K8s) don’t protect you by default — you must define service-level and namespace-level policies

This week helped you shift security left to the network layer — before containers, service meshes, or proxies enter the picture.

⸻

📈 Application Evolution So Far

Component	Security Status
OS Layer	Hardened users, SSH, permissions ✅
Network Layer	Segmented ports, host firewall, detection ✅
Services	Separated runtime users, isolated ports ✅

You’re now ready to move into containerization — which is our Week 3 focus.