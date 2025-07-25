📁 Week02/GuidedLab.md – Enforcing Host-Based Network Isolation Between Services

⸻

🛠️ Objective

Simulate two microservices — frontend (Node.js) and backend (Python) — running on the same Linux VM.
Then apply host-level firewall rules to restrict which services can talk to each other.

This lays the foundation for secure network policies in ECS and Kubernetes later in the bootcamp.

⸻

⚙️ Environment Assumptions
	•	You’re using the hardened Linux VM from Week 1
	•	You have devsecops user access with sudo privileges
	•	Node.js and Python are installed (node -v, python3 --version)
	•	Ports:
	•	Frontend (Node.js): port 3000
	•	Backend (Python Flask): port 5000

⸻

🔧 Step 1: Create Frontend and Backend Services

We’ll keep these services intentionally simple for now.

🔹 Frontend Service (Node.js)

Create /opt/notestream/frontend/index.js:

const express = require('express');
const app = express();
const axios = require('axios');
const PORT = 3000;

app.get('/', async (req, res) => {
  try {
    const backendRes = await axios.get('http://localhost:5000/data');
    res.send(`Frontend connected to backend: ${backendRes.data}`);
  } catch (err) {
    res.status(500).send('Could not reach backend.');
  }
});

app.listen(PORT, () => console.log(`Frontend running on port ${PORT}`));

Install dependencies and run:

cd /opt/notestream/frontend
npm init -y
npm install express axios
node index.js

Test in browser or with:

curl http://localhost:3000


⸻

🔹 Backend Service (Python Flask)

Create /opt/notestream/backend/api.py:

from flask import Flask
app = Flask(__name__)

@app.route('/data')
def data():
    return "Secure data from backend service"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)

Run:

cd /opt/notestream/backend
pip3 install flask
python3 api.py

Test:

curl http://localhost:5000/data


⸻

🔒 Step 2: Install and Configure UFW (Uncomplicated Firewall)

sudo apt update
sudo apt install ufw -y
sudo ufw default deny incoming
sudo ufw default allow outgoing

Open only frontend port:

sudo ufw allow 3000/tcp
sudo ufw enable

Try accessing both services:

curl http://localhost:3000      # ✅ should work
curl http://localhost:5000      # ❌ should fail from outside the service


⸻

🔁 Step 3: Verify Firewall Rules

sudo ufw status numbered
sudo ss -tuln
sudo netstat -plnt

You should see:
	•	Frontend port 3000 open
	•	Backend port 5000 listening only on 127.0.0.1
	•	Firewall blocking access to 5000 from external IPs

⸻

🧪 Step 4: Simulate Attack Attempt

Try scanning open ports:

sudo apt install nmap -y
nmap -sS localhost

You should see only:

PORT     STATE SERVICE
3000/tcp open  ppp

Backend port is now isolated from the outside world — but reachable from the frontend.

⸻

📋 Step 5: Document Network Policy

Create network-policy.md:

## Host-Level Network Policy

- Frontend Service: exposed via port 3000 to the internet
- Backend Service: not exposed externally (bound to 127.0.0.1)
- Only frontend can communicate with backend over loopback
- All other ports are firewalled by UFW

## Future Enforcement Goals:
- ECS Service Connect namespaces
- K8s NetworkPolicies by pod label
- Service-to-service TLS


⸻

✅ You’ve now implemented host-based microservice network segmentation — this is exactly how you’ll scale to container-level or VPC-level segmentation later.
