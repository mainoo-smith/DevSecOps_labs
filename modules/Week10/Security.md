# 🔐 Week 10 – Security: Infrastructure as Code (IaC) with Terraform, CDK, and SAM

---

## 🔍 Core DevSecOps Security Concepts

| Concept | Description | Relevance |
|--------|-------------|-----------|
| Principle of Least Privilege (PoLP) | Only give services the exact permissions they need | Reduces blast radius in case of a breach |
| Immutable Infrastructure | Avoid modifying infra manually; always redeploy via code | Ensures repeatability, auditability, and prevents config drift |
| Infrastructure Drift Detection | Detect and reconcile changes made outside of IaC | Prevents out-of-band changes or shadow infrastructure |
| Secrets Management | Store secrets in managed vaults (not in code or env files) | Protects credentials, tokens, and sensitive data |
| Environment Isolation | Each environment should have its own infra, secrets, and roles | Reduces accidental cross-environment data leakage |

---

## ✅ Terraform-Specific Security Practices

### 🔐 Secret Handling

- **✅ Use `aws_secretsmanager_secret`** instead of `variable` blocks
- **❌ Don’t use `plain_text` env vars** or write secrets in `*.tfvars`

### 🔍 Static Security Scans

- **`tfsec`**: Static analysis with cloud-provider-specific checks
- **`checkov`**: Full IaC security policies and benchmarks (CIS, NIST, SOC2)
- **`tflint`**: Detects syntax and logic errors

```bash
tfsec . && checkov -d . && tflint
✅ Least Privilege IAM
Instead of:

resource "aws_iam_policy" {
  actions = ["*"]
  resources = ["*"]
}
Use:

actions = [
  "secretsmanager:GetSecretValue",
  "logs:PutLogEvents"
]
resources = [aws_secretsmanager_secret.my_secret.arn]
✅ AWS CDK Security Practices
✅ SecretsManager Integration
Inject secrets at runtime using ecs.Secret.fromSecretsManager()

Never define .env or config files with secrets in your CDK code

Avoid toString() or .value calls on secrets — use directly as SecretValue

🧪 CDK Security Scanning
Use cdk-nag for best practices:

Aspects.of(this).add(new AwsSolutionsChecks());
Enforces:

No public access on S3

Encryption on resources

Valid IAM trust relationships

✅ SAM-Specific Security Notes
Define secrets in Parameters and inject them via Environment.SecretsManager

Prefer AWS-managed Policies blocks over custom wildcard policies

Use Metadata to mark parameters as sensitive (useful in scans)

Example:

Environment:
  Variables:
    DB_SECRET: !Ref MySecret
🛡️ CI/CD Security Enforcement
Tool	Where	Why
tfsec, checkov, tflint	Pre-commit & CI/CD pipelines	Block insecure changes before deploy
OIDC + short-lived tokens	CDK/Terraform deploy roles	Prevent key leaks and stale access
driftctl or infracost	CI/CD or cron	Detect unplanned drift or cost spikes
Secrets rotation logic	CodeBuild step or Lambda	Enforce periodic rotation + audit logs
🔐 Common Misconfigurations & Their Fixes
❌ Insecure Practice	✅ Secure Alternative
IAM: "*" on all resources	Specific actions and resources
Secrets in terraform.tfvars	Use SecretsManager + data sources
docker run -e SECRET=value	Use ECS or Kubernetes secret injectors
Console-based infra edits	Use IaC tools only + detect drift
Overuse of default VPC	Create and secure isolated VPCs per env
Shared state across environments	Separate S3 backends for dev, staging, prod
🧠 DevSecOps Mental Models
“If it’s not in Git, it doesn’t exist.”

“Code is the boundary between intention and reality.”

“Static scanners enforce discipline. Drift detection enforces truth.”

“Every IAM wildcard is an unguarded door.”


---

Let me know when you're ready for:

✅ `Reflection.md` — your personal recap, what you learned about secure IaC, and how the app evolved  
➡️ Then we’ll move to **Week 11 – Kubernetes Security I: RBAC, NetworkPolicies, and Access Control** (the start of the K8s track)

Shall we continue?
You said:
Continue 
ChatGPT said:
Perfect — here’s the final file for Week 10: