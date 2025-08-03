Title: Centralized Secrets Without Compromise: Vault, SOPS & Sealed Secrets

🧪 Scenario
You’ve been asked to modernize secret handling for your evolving note/task management app. The app runs across ECS and Kubernetes. Secrets currently live in unencrypted .env files and plaintext Helm charts.

You’ll now:

Set up Vault for centralized secrets

Encrypt GitOps-compatible secrets using SOPS

Deploy Kubernetes secrets using Sealed Secrets

Inject secrets securely into GitLab/GitHub CI

Enforce access control across environments (dev, staging, prod)

🧰 Prerequisites
Docker or K8s dev environment (minikube or ECS dev cluster)

GitLab and/or GitHub repo access

Tools installed: vault, sops, kubeseal, jq, helm, kubectl

🔧 Part 1: Setup & Use Vault
🔹 Step 1.1: Start a Dev Vault Server
In production, use HA mode + integrated storage. Here we’ll use dev mode.

vault server -dev
You'll see:

Root Token: s.xxxxxxxx
Export the token:

export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='s.xxxxxxxx'
🔹 Step 1.2: Enable KV Secrets Engine (Version 2)
vault secrets enable -path=secrets kv-v2
🔹 Step 1.3: Add a Secret
vault kv put secrets/dev/db password='devpass123' username='devuser'
🔹 Step 1.4: Read Secret
vault kv get secrets/dev/db
🔹 Step 1.5: Configure App Access (GitHub Auth Example)
vault auth enable github

vault write auth/github/config organization="YourOrg"

vault write auth/github/map/teams/dev team="dev" value="default,dev"

vault policy write dev - <<EOF
path "secrets/data/dev/*" {
  capabilities = ["read"]
}
EOF
Use GitHub token to authenticate:

vault login -method=github token=YOUR_GITHUB_TOKEN
✅ This limits access to specific secret paths per team/environment.

🔐 Part 2: Use SOPS for Git-Safe Secrets
🔹 Step 2.1: Generate a GPG Key (or use AWS KMS / GCP KMS)
gpg --full-generate-key
gpg --list-keys
Copy your key ID (e.g. A1B2C3D4).

🔹 Step 2.2: Create a Secret File
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  password: myplaintextpassword
🔹 Step 2.3: Encrypt with SOPS
sops --encrypt --pgp A1B2C3D4 secret.yaml > secret.enc.yaml
Check the output — values are encrypted inline.

🔹 Step 2.4: Decrypt
sops --decrypt secret.enc.yaml
✅ Now you can commit the encrypted file to Git — safe for GitOps workflows.

🛡️ Part 3: Sealed Secrets in Kubernetes
🔹 Step 3.1: Install Sealed Secrets Controller
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.23.0/controller.yaml
🔹 Step 3.2: Get Public Key
kubeseal --fetch-cert \
  --controller-namespace kube-system \
  --controller-name sealed-secrets-controller \
  > pub-cert.pem
🔹 Step 3.3: Create & Seal a Secret
kubectl create secret generic my-secret --from-literal=password='SuperSecret' --dry-run=client -o json > secret.json

kubeseal --cert pub-cert.pem -o yaml < secret.json > sealed-secret.yaml
✅ Now sealed-secret.yaml can be safely committed to Git. Only the cluster with the private key can decrypt it.

🔹 Step 3.4: Apply Sealed Secret
kubectl apply -f sealed-secret.yaml
Verify the decrypted Secret was created.

🤖 Part 4: Inject Secrets in CI/CD
🔹 GitHub Actions
jobs:
  deploy:
    runs-on: ubuntu-latest
    env:
      DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
Or use OIDC to retrieve from Vault dynamically:

vault write auth/jwt/login role=github \
     jwt=${GITHUB_TOKEN}
🔹 GitLab CI
In .gitlab-ci.yml:

variables:
  VAULT_ADDR: https://vault.mycorp.com
  VAULT_TOKEN: ${VAULT_CI_TOKEN}

script:
  - vault kv get -field=password secrets/dev/db
✅ Success Criteria
Task	Validation
Vault set up	Secrets stored and scoped to envs
SOPS working	Secret YAML encrypted inline
Sealed Secrets	Secrets sealed, committed, and deployed safely
CI/CD injection	Secrets retrieved dynamically or from env
Access controls	Limited by environment, service, or auth
Ready to move on to ChallengeLab.md, where you’ll build your own full secrets handling flow across Vault, GitOps, and deployment pipelines?

You said:
Yes
ChatGPT said:
Awesome — here's your hands-on ChallengeLab.md for Week 8: Secrets Management. This lab assumes your infrastructure is growing, and now you must treat secrets as first-class, version-controlled, yet zero-trust resources — rotating, encrypting, and auditing them end-to-end.