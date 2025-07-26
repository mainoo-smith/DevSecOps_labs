📁 Week02/Overview.md – Networking & Firewalls for DevSecOps

⸻

🧠 Module Theory: Networking Fundamentals in DevSecOps

Networking is at the heart of how systems communicate — and how attackers move.

In a modern DevSecOps environment, your responsibilities go far beyond writing security group rules. You must understand how networks are structured, how to segment access by role and workload, and how to detect or prevent lateral movement between services.

This week we’ll explore:
	•	How DevSecOps applies network segmentation, firewalls, and least-privilege access
	•	How tools like iptables, ufw, and cloud-native firewalls (e.g., AWS SGs/NACLs, K8s Network Policies) enforce these boundaries
	•	How vulnerable or over-permissive rules can be exploited in real attacks

⸻

🎯 Objectives

By the end of this module, you will:
	•	Understand and apply core networking concepts: IP, TCP/UDP, ports, DNS
	•	Set up a host-based firewall using ufw or iptables
	•	Simulate and block lateral movement between two app services
	•	Visualize traffic and access attempts using logs and CLI tools
	•	Define baseline rules for environment isolation in ECS and Kubernetes
	•	Understand Zero Trust principles in DevSecOps networking

⸻

📦 Application Tie-In: Evolving the Project

This week, we simulate breaking the monolith into two isolated parts:
	•	A backend service (Python API) and a frontend (Node.js)
	•	They live on the same Linux VM but must be isolated by:
	•	User access
	•	Firewall ports
	•	Execution context (systemd or containers)

You will:
	•	Expose only the frontend (port 3000)
	•	Block public access to the backend (port 5000)
	•	Allow frontend → backend communication only
	•	Verify this using tools like curl, ss, ufw, iptables, and logs

Later in ECS/Kubernetes, these concepts evolve into Service Connect, SGs, and NetworkPolicies — this is your foundation.

⸻

🔧 Tools & Technologies
	•	TCP/IP stack
	•	nmap, ss, netstat, ufw, iptables
	•	curl, telnet, nc
	•	Linux system logs
	•	Optional: tcpdump, wireshark (for packet capture exploration)

⸻

🛡️ DevSecOps Concepts Introduced

Concept	Relevance
Network Segmentation	Limit lateral movement between services
Port & Protocol Control	Prevent accidental exposure (e.g., dev DB open to internet)
Principle of Least Network Access	“Need to talk” basis between microservices
Ingress/Egress Boundaries	Who can reach what, and from where
Auditing and Logging	Detect unauthorized scans or attempts


⸻

📁 Deliverables
	•	Two services (frontend and backend) deployed and network-isolated on the same VM
	•	Host-based firewall rules that enforce correct access paths
	•	Evidence of rejected vs. accepted connections (e.g., curl output, logs)
	•	A network-policy.md file explaining current state + assumptions
	•	Prep for Week 3 where we’ll containerize both services securely