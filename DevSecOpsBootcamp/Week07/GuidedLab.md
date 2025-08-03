Title: Runtime Integrity, Provenance & Environment Isolation

🧠 Lab Goals
By the end of this lab, you'll have:

Signed your container images via CI/CD using Cosign

Generated SBOMs using Trivy and Syft

Enabled Amazon Inspector runtime scanning for ECS

Verified container signatures before ECS deployment

Enforced network isolation policies via ECS Service Connect

Detected drift between signed image and deployed runtime task

🧱 Lab Structure
Stage	Tools
Image Signing	Cosign + GitHub OIDC
SBOM Generation	Trivy + Syft
Runtime Scanning	Amazon Inspector
Signature Verification	Cosign + deploy gating
ECS Isolation	ECS Service Connect, namespaces
Drift Monitoring	ECR tags + ECS task metadata comparison
🛠️ PART 1: Container Signing with Cosign
🧾 Step 1: Install Cosign Locally (for testing)
brew install cosign  # macOS
# OR
curl -sSL https://github.com/sigstore/cosign/releases/latest/download/cosign-linux-amd64 \
  -o /usr/local/bin/cosign && chmod +x /usr/local/bin/cosign
🔐 Step 2: Sign Image via GitHub Actions
Add to your pipeline (backend.yml or frontend.yml):

- name: Sign Docker image with Cosign
  run: |
    cosign sign --yes \
      --key env://COSIGN_PRIVATE_KEY \
      ${{ secrets.ECR_REGISTRY }}/backend:${{ github.sha }}
  env:
    COSIGN_PRIVATE_KEY: ${{ secrets.COSIGN_PRIVATE_KEY }}
    COSIGN_PASSWORD: ${{ secrets.COSIGN_PASSWORD }}
🔐 Store the COSIGN_PRIVATE_KEY and COSIGN_PASSWORD in GitHub Secrets.

Use GitHub Actions OIDC instead of a static key (recommended for prod):

cosign sign --yes --identity-token $ACTIONS_ID_TOKEN <image>
✅ Step 3: Verify Image Signature (Before Deploy)
cosign verify $ECR_REGISTRY/backend:<tag>
❌ CI fails if image is unsigned or modified.

📦 PART 2: Generate SBOMs
Step 1: Generate SBOM with Trivy
Add to pipeline:

- name: Generate SBOM
  run: |
    trivy image --format cyclonedx \
      --output sbom-backend.json \
      ${{ secrets.ECR_REGISTRY }}/backend:${{ github.sha }}
🎯 Store this in S3, SSM Parameter Store, or attach to build artifacts.

Step 2: Generate SBOM with Syft
syft $ECR_REGISTRY/backend:${{ github.sha }} -o json > sbom-backend.json
🔍 PART 3: Enable Amazon Inspector for Runtime CVE Scanning
Step 1: Enable Inspector in Region
aws inspector2 enable --resource-types EC2 ECR
ECS on Fargate automatically integrates via ECR scanning.

Step 2: Enable Scan on Push (ECR)
aws ecr put-image-scanning-configuration \
  --repository-name backend \
  --image-scanning-configuration scanOnPush=true
Step 3: View Inspector Findings
aws inspector2 list-findings \
  --filter criteria='{"repositoryName":[{"value":"backend","comparison":"EQUALS"}]}'
🚦 PART 4: Gate ECS Deployments Based on Signature Verification
Update deployment pipeline:

- name: Verify Image Signature
  run: |
    cosign verify $ECR_REGISTRY/backend:${{ github.sha }}
❌ Block deploy if unsigned or tampered.

Add optional signature check in ECS task definition label or tag:

"imageTag": "backend:git-sha-verified"
🌐 PART 5: ECS Service Connect Isolation Rules
Step 1: Enable Namespaces Per Environment
Create namespaces:

aws servicediscovery create-namespace --name dev --type HTTP
aws servicediscovery create-namespace --name qa --type HTTP
Assign services to namespace:

service_connect_configuration {
  enabled = true
  namespace = "dev"
  services {
    port_name = "backend"
    client_alias {
      port = 8080
    }
  }
}
Step 2: Block Same-Service Calls in Dev
In ECS Task Security Groups:

# Allow frontend to backend
ingress {
  from_port = 8080
  to_port = 8080
  protocol = "tcp"
  security_groups = [frontend_sg]
}

# Deny backend → backend
Step 3: Allow Dev Service A → Staging Service B
Use Service Connect + hardcoded aliasing:

client_alias {
  dns_name = "staging-b.backend.staging"
  port = 9090
}
🌀 PART 6: Detect Container Drift
Step 1: Get Running Task Image
aws ecs describe-tasks --tasks <id> \
  --cluster <cluster> \
  --query "tasks[].containers[].image"
Step 2: Compare with Signed Tag
Use:

cosign verify <ECR_IMAGE_URI>
Fail if:

Image doesn’t match latest signed SHA

Container was launched manually or from unsigned pipeline

✅ You’ve Now Secured the Runtime
Layer	Secured How
Build → Deploy	Cosign signing + Trivy SBOM
Registry	Amazon Inspector scans, scanOnPush enabled
Runtime	ECS + Inspector alerts + ECS task metadata
Networking	ECS Service Connect with namespace isolation
Drift Detection	Signature check vs running task hash
🔜 Next: ChallengeLab.md — simulate a runtime image swap, a network violation, and a signature bypass attempt.
Proceed?

You said:
Yes. Let’s also include how services talk to each other with versioning of the services. For example we can point to different versions of the same service in the staging environment 
ChatGPT said:
Excellent — we’ll incorporate version-aware service communication, such as:

dev-service-A targeting staging-service-B:v2

Cross-env routing using ECS Service Connect DNS aliasing

Runtime validation of version constraints

SBOM and signature enforcement per version

Let’s now begin the ChallengeLab.md for Week 7: Secure Container Runtime & Image Provenance, including these advanced runtime and networking scenarios.

Ready?

You said:
Ready
ChatGPT said:
Here is your advanced ChallengeLab.md for Week 7, combining runtime security, container provenance, and version-aware service communication across environments.