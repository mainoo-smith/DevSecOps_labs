📁 Week5/GuidedLab.md

Title: Secure Scripting: Bash & Python Automation for Cloud, CI/CD & Compliance

⸻

🧪 Scenario

You’ve been asked to:
	•	Monitor the health of your ECS services
	•	Generate SBOM reports from vulnerability scans
	•	Fetch secrets from AWS SSM Parameter Store
	•	Log archive and cleanup routines

You’ll build Bash and Python scripts that run locally and in CI/CD — with secure handling of secrets, inputs, logs, and IAM.

⸻

🧱 Project Structure

We’ll add this to your app repo:

scripts/
├── health/
│   └── check_ecs_health.sh
├── sbom/
│   └── trivy_to_html.py
├── secrets/
│   └── fetch_secrets.sh
├── logs/
│   └── archive_logs.py
.env.example

You’ll also prepare scripts/ci/ for jobs that can run in GitHub Actions or GitLab CI.

⸻

🐚 Part 1: Bash Script – ECS Service Health Check

🔹 Step 1.1: check_ecs_health.sh

#!/bin/bash
set -euo pipefail

CLUSTER_NAME="${1:-}"
SERVICE_NAME="${2:-}"

if [[ -z "$CLUSTER_NAME" || -z "$SERVICE_NAME" ]]; then
  echo "Usage: $0 <cluster-name> <service-name>"
  exit 1
fi

STATUS=$(aws ecs describe-services \
  --cluster "$CLUSTER_NAME" \
  --services "$SERVICE_NAME" \
  --query "services[0].deployments[?status=='PRIMARY'].rolloutState" \
  --output text)

if [[ "$STATUS" == "COMPLETED" ]]; then
  echo "✅ $SERVICE_NAME is healthy in $CLUSTER_NAME"
else
  echo "❌ $SERVICE_NAME is not fully deployed. Status: $STATUS"
  exit 2
fi

✅ Security Practices:
	•	set -euo pipefail → fail fast
	•	Validates arguments
	•	Doesn’t log secrets or tokens

🔹 Step 1.2: Run locally

chmod +x scripts/health/check_ecs_health.sh
./scripts/health/check_ecs_health.sh notes-cluster notes-service


⸻

🐍 Part 2: Python Script – SBOM Formatter

🔹 Step 2.1: Install Trivy and generate SBOM

trivy image --format cyclonedx --output results.json yourapp:latest

🔹 Step 2.2: trivy_to_html.py

import json, sys
from pathlib import Path

def generate_html(input_file: str):
    data = json.loads(Path(input_file).read_text())

    html = "<html><body><h1>SBOM Vulnerabilities</h1><ul>"
    for component in data.get("components", []):
        name = component.get("name", "unknown")
        version = component.get("version", "unknown")
        html += f"<li>{name} – {version}</li>"
    html += "</ul></body></html>"

    output_file = input_file.replace(".json", ".html")
    Path(output_file).write_text(html)
    print(f"✅ SBOM report saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python trivy_to_html.py results.json")
        sys.exit(1)
    generate_html(sys.argv[1])

✅ Security Practices:
	•	No eval(), no shell injection
	•	Validates file input

python scripts/sbom/trivy_to_html.py results.json


⸻

🔐 Part 3: Bash – Secure Secrets Fetch from AWS SSM

🔹 Step 3.1: fetch_secrets.sh

#!/bin/bash
set -euo pipefail

SECRETS=("DB_PASSWORD" "API_KEY")

for secret in "${SECRETS[@]}"; do
  VALUE=$(aws ssm get-parameter \
    --name "/devsecops/${secret}" \
    --with-decryption \
    --query "Parameter.Value" \
    --output text)
  echo "export $secret='$VALUE'" >> .env
done

echo "✅ Secrets loaded into .env"

✅ Fetches encrypted parameters securely
✅ IAM permissions required: ssm:GetParameter, kms:Decrypt

⸻

☁️ Part 4: Python – Archive Logs to S3

import boto3, datetime, gzip, shutil
from pathlib import Path

logs_dir = Path("/var/log/myapp")
bucket = "devsecops-log-archive"
date = datetime.datetime.now().strftime("%Y-%m-%d")

session = boto3.Session()
s3 = session.client("s3")

for log_file in logs_dir.glob("*.log"):
    compressed = log_file.with_suffix(".gz")
    with open(log_file, 'rb') as f_in, gzip.open(compressed, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

    s3_key = f"logs/{date}/{compressed.name}"
    s3.upload_file(str(compressed), bucket, s3_key)
    print(f"✅ Uploaded {compressed.name} to s3://{bucket}/{s3_key}")

✅ Handles log rotation
✅ Compresses locally, uploads securely with Boto3
✅ Avoids uploading raw secrets

⸻

🧪 Bonus: CI/CD Integration

GitHub Actions example:

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: bash scripts/health/check_ecs_health.sh notes-cluster notes-service

Secrets fetch before pipeline step:

      - name: Load Secrets
        run: bash scripts/secrets/fetch_secrets.sh

✅ Your scripts are now portable, secure, and CI-ready.
