Title: “Runtime, Registry & Network Hardening”

🔐 1. Container Signing: Trust But Verify
Cosign Signing (CI)

Every container built in CI is signed using GitHub/GitLab OIDC identity

Stored in OCI registry (ECR)

Verified at deploy via pipeline policy

Why It Matters:

Guarantees container provenance — no tampering between CI and runtime

Detects image swaps or untrusted sources

cosign sign --yes <image>
cosign verify <image>
📜 2. SBOMs: Audit-Ready from Day One
Trivy / Syft SBOM Generation

Captures exact software components (libs, deps, licenses)

Stored alongside artifacts (S3 or GitHub release)

Why It Matters:

Mandatory for regulated industries (FedRAMP, SOC2, DoD)

Enables instant CVE lookup if a zero-day hits a dependency

trivy image --format cyclonedx -o sbom.json <image>
🕵️ 3. Amazon Inspector Runtime Scanning
Enabled for ECS (Fargate)

Automatically scans running container layers

Reports CVEs even after build time

Best Practices:

Enable scanOnPush in ECR

Automate notifications to Slack, Jira, or SIEM via EventBridge

aws inspector2 enable --resource-types EC2 ECR
🔄 4. Drift Detection Between CI and Runtime
Compare:

ECS task image vs CI signed image hash

Why It Matters:

Detects unauthorized deploys or manual hotfixes

IMAGE=$(aws ecs describe-tasks --query 'tasks[].containers[].image')
cosign verify $IMAGE
🌐 5. Network Isolation (Service Connect Namespaces)
Per-Environment Namespaces

dev, qa, staging, uat all have isolated namespaces

Prevents cross-talk (e.g., dev-backend ↔ dev-backend)

Enforced via:

ECS Task Security Groups

Service Connect scoped DNS

🛡️ 6. HTTPS Enforcement Within ECS Service Connect
By default, ECS Service Connect uses HTTP over the VPC.
To enforce HTTPS (TLS) between services, use one of these options:

✅ Option 1: TLS Termination at the Service (Recommended)
Backend runs with TLS enabled (self-signed or ACM)

https.createServer({ key, cert }, app).listen(443);
Frontend or client services call:

await axios.get("https://service-b-v2.staging:443/secure", {
  httpsAgent: new https.Agent({ rejectUnauthorized: false }) // dev/test only
});
✅ Ideal for secure intra-VPC encryption and RBAC via certs.

🔐 Option 2: mTLS with Envoy Proxy Sidecar
Each ECS task runs Envoy or AWS App Mesh proxy

Certs issued via ACM Private CA

Enforced per-source/destination identity

Why It Matters:

Strongest security model: mTLS, policy enforcement, identity-bound traffic

🔒 Option 3: Internal ALBs with TLS & SNI Routing
Expose each ECS service via internal ALB with TLS listener

Attach ACM certificate

Use SNI or path-based routing to split versions

Useful if Service Connect DNS isn't flexible enough for your HTTPS model.

✅ Best Practice Summary:
Approach	TLS?	Auth?	Use When...
TLS inside app	✅	❌ (unless mTLS in app)	Simple HTTPS
TLS + ACM certs	✅	✅	Internal trust model
Envoy sidecar	✅✅	✅✅	Full mTLS, policy-driven
No HTTPS (default)	❌	❌	Not recommended
✅ Bonus: Version-Aware Service Routing Security
Register each service version separately in Service Connect (e.g., service-b-v2)

Limit each service to only talk to specific version endpoints

Use DNS patterns like service-b-v2.staging and reject fallback calls

axios.get("https://service-b-v2.staging:443")
✅ Prevents shadow deployments, version confusion, and data inconsistencies.

🔚 Summary
Area	Security Practice
Build pipeline	Cosign signature + SBOMs
Registry	Inspector scan-on-push
Runtime	Inspector + drift detection
Network	SG rules + Service Connect namespaces
Transport	HTTPS via in-app TLS or Envoy
Versioning	DNS-based routing + client enforcement
Would you like to proceed to the Reflection.md for Week 7?

You said:
Yes
ChatGPT said:
Here is your Reflection.md for Week 7: Secure Container Runtime & Image Provenance, capturing how your DevSecOps maturity has now reached runtime awareness and service version trust.