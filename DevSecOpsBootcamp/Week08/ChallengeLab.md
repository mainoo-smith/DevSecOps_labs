Title: No Secrets Left Behind: Encrypt, Inject & Rotate Across Environments

🧪 Scenario
You’ve onboarded 4 services in your note/task manager platform:

auth-service

notes-service

notification-service

analytics-service

You now need to:

Build a multi-environment secret strategy

Use Vault for dynamic database secrets

Encrypt GitOps secrets using SOPS

Deliver Sealed Secrets to Kubernetes securely

Inject secrets into CI/CD pipelines

Enforce RBAC and TTL policies

🛠️ Challenge 1: Vault for Dynamic Secrets
Create a dynamic secrets engine in Vault for PostgreSQL:

vault secrets enable database

vault write database/config/my-postgres-db \
  plugin_name=postgresql-database-plugin \
  allowed_roles="readonly" \
  connection_url="postgresql://{{username}}:{{password}}@db.internal:5432/postgres?sslmode=disable" \
  username="admin" \
  password="adminpass"
Define a dynamic role:

vault write database/roles/readonly \
  db_name=my-postgres-db \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"
Test the dynamic secret:

vault read database/creds/readonly
✅ Output should be a short-lived credential.

🛠️ Challenge 2: SOPS-Encrypted GitOps Secrets
Create a YAML manifest with environment-specific values:

apiVersion: v1
kind: Secret
metadata:
  name: analytics-api-keys
type: Opaque
data:
  stripe_key: sk_test_12345
Encrypt it with SOPS using AWS KMS or GPG:

sops --encrypt --kms arn:aws:kms:us-east-1:123456789012:key/abcd... secret.yaml > encrypted.yaml
Commit encrypted.yaml to your GitOps repo.

Decrypt in CI to render the full manifest:

sops -d encrypted.yaml > manifest.yaml
✅ Manifest ready for Kustomize/Helm or direct kubectl apply.

🛠️ Challenge 3: Kubernetes Sealed Secrets
Create a Kubernetes secret for auth-service JWT signing key:

kubectl create secret generic auth-jwt \
  --from-literal=jwt_key='super-secure-secret' \
  --dry-run=client -o json > secret.json
Seal it:

kubeseal --cert pub-cert.pem -o yaml < secret.json > sealed-auth-jwt.yaml
Apply to cluster:

kubectl apply -f sealed-auth-jwt.yaml
✅ Should automatically decrypt to usable secret within cluster.

🛠️ Challenge 4: Secrets in CI/CD
🔹 GitHub Actions
Retrieve a secret from Vault using JWT OIDC:

vault write auth/jwt/login role=github jwt=${ACTIONS_ID_TOKEN}
Fetch secret for deploy:

vault kv get -field=stripe_key secrets/prod/analytics
🔹 GitLab CI
Use Vault environment variables or secret variables.

Store VAULT_TOKEN as masked variable.

Pull dynamic DB credentials for notes-service.

🛠️ Challenge 5: Access Policies per Environment
Create Vault policies for dev, qa, prod:

# dev-policy.hcl
path "secrets/data/dev/*" {
  capabilities = ["read"]
}
vault policy write dev dev-policy.hcl
Assign access based on GitHub team, CI OIDC claim, or service name.

✅ Success Criteria
Task	Validation
Dynamic DB credentials	vault read returns valid temporary creds
Encrypted GitOps secret	SOPS-encrypted YAML decrypts and applies cleanly
Sealed Kubernetes secret	Encrypted secret deploys and is usable
Vault CI/CD integration	Secrets retrieved in pipeline without storing plaintext
Scoped access	Dev team cannot access prod secrets
🧠 Bonus (Optional)
Rotate the Vault DB root credentials using a rotation command

Trigger Slack or email on secret read from Vault

Store audit logs from Vault to CloudWatch or ELK

Configure Vault agent injector into K8s sidecars

Let me know when you're ready to move on to the Security.md — we’ll cover the threats this model protects against (like secret sprawl, Git leaks, insider threats, and over-permissioned access).

You said:
Yes
ChatGPT said:
Perfect. Here's the Security.md for Week 8: Secrets Management, where we break down exactly what threats you're mitigating by building secret handling into your infrastructure and pipelines.