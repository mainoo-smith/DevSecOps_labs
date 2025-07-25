📁 Week03/GuidedLab.md – Securely Containerizing Frontend and Backend with DevSecOps Best Practices

⸻

🧠 Objective

This lab walks you through securely containerizing both your notestream microservices:
	•	Node.js Frontend (port 3000)
	•	Python Flask Backend (port 5000)

You’ll:
	•	Build hardened Dockerfiles
	•	Scan images for CVEs
	•	Apply runtime security flags
	•	Use Docker Compose for local orchestration

This will simulate how you’ll later deploy to ECS or Kubernetes with security-first containers.

⸻

🛠️ Step 1: Directory Structure

mkdir -p ~/devsecops-bootcamp/notestream/{frontend,backend}
cd ~/devsecops-bootcamp/notestream


⸻

🧩 Step 2: Create the Backend (Flask)

📄 backend/app.py

from flask import Flask
app = Flask(__name__)

@app.route('/data')
def data():
    return "Secure data from backend"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

📄 backend/requirements.txt

Flask==2.3.3

📄 backend/Dockerfile

FROM python:3.11-slim

# Use non-root user
RUN useradd -m appuser

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

USER appuser
EXPOSE 5000

CMD ["python", "app.py"]


⸻

🖼️ Step 3: Create the Frontend (Node.js + Express)

📄 frontend/index.js

const express = require('express');
const axios = require('axios');
const app = express();
const PORT = 3000;

app.get('/', async (req, res) => {
  try {
    const response = await axios.get('http://backend:5000/data');
    res.send(`Frontend got: ${response.data}`);
  } catch (err) {
    res.status(500).send('Could not reach backend');
  }
});

app.listen(PORT, () => console.log(`Frontend running on port ${PORT}`));

📄 frontend/package.json

{
  "name": "frontend",
  "version": "1.0.0",
  "main": "index.js",
  "dependencies": {
    "axios": "^1.6.8",
    "express": "^4.18.2"
  }
}

📄 frontend/Dockerfile

FROM node:20-slim

RUN useradd -m appuser
WORKDIR /app

COPY package.json .
RUN npm install --omit=dev

COPY index.js .

USER appuser
EXPOSE 3000

CMD ["node", "index.js"]


⸻

🧪 Step 4: Compose the App

📄 docker-compose.yml

version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    security_opt:
      - no-new-privileges:true
    read_only: true
    cap_drop:
      - ALL

  backend:
    build:
      context: ./backend
    ports:
      - "5000:5000"
    security_opt:
      - no-new-privileges:true
    read_only: true
    cap_drop:
      - ALL

Start it up:

docker compose up --build

Test:

curl http://localhost:3000

✅ You should see: Frontend got: Secure data from backend

⸻

🔍 Step 5: Scan Your Images for Vulnerabilities

🔹 Using Trivy

brew install aquasecurity/trivy/trivy  # macOS
sudo apt install trivy                 # Debian/Ubuntu

# Scan backend
trivy image notestream_backend

# Scan frontend
trivy image notestream_frontend

📌 Fix any critical/high CVEs by upgrading base image or dependencies.

⸻

🔐 Step 6: Add Runtime Hardening (Recap)

Verify containers were started with:
	•	read_only root filesystem
	•	--cap-drop=ALL to remove Linux capabilities
	•	--security-opt=no-new-privileges:true

Optional: Run them manually to test

docker run --rm -it \
  --read-only \
  --cap-drop=ALL \
  --security-opt no-new-privileges:true \
  notestream_backend


⸻

🧾 Step 7: Document the Runtime Policy

📄 container-policy.md

## Notestream Secure Container Policy

- Base images: python:3.11-slim, node:20-slim
- No root user (uses appuser)
- Only essential ports exposed (3000, 5000)
- Runtime hardened:
  - read-only filesystem
  - dropped Linux capabilities
  - no privilege escalation
- Scanned with Trivy for CVEs


⸻

✅ You now have a securely containerized version of both services — ready for CI/CD and later orchestration with ECS or Kubernetes.
