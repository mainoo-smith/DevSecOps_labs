# ⚔️ Challenge Lab – Policy-as-Code in a Real DevSecOps Workflow

---

## 🧩 Scenario

Your team is deploying a new version of the `notes-service` and `auth-service` to Kubernetes. At the same time, you’re onboarding infrastructure via Terraform for S3, IAM, and ECS resources.

Security has mandated the following:

1. **No Kubernetes pods can escalate privileges or use hostPath**
2. **All Terraform resources must include standard tags**
3. **S3 buckets must have server-side encryption enabled**
4. **ECS task definitions must explicitly run as non-root**
5. **No container images should use `:latest` tag**
6. **CI/CD must block all violations pre-deploy**

Your job is to:

✅ Write the necessary **Rego policies**  
✅ Validate your IaC (Terraform) and app manifests (Kubernetes, ECS)  
✅ Configure GitLab/GitHub to **block merges** on failure

---

## 🧪 Tasks

### 🔧 Task 1: Write Kubernetes Hardening Policies

- Require all containers to have `securityContext.runAsNonRoot: true`
- Block any use of `hostPath`
- Prevent `allowPrivilegeEscalation: true`

📄 Save as: `policy/k8s/secure_pods.rego`

---

### 🔧 Task 2: Enforce Terraform Compliance

- Require `tags` on all resources
- Ensure all `aws_s3_bucket` resources include encryption
- Block any IAM policy with `*` in `"Action"`

📄 Save as:
- `policy/terraform/require_tags.rego`
- `policy/terraform/s3_encryption.rego`
- `policy/terraform/no_wildcard_iam.rego`

Use `terraform show -json > plan.json` to generate test input.

---

### 🔧 Task 3: Harden ECS Configs

- Deny if any `containerDefinition.user == "root"`
- Deny if `readonlyRootFilesystem` is not set to `true`

📄 Save as: `policy/ecs/no_root.rego`

Test with your ECS JSON definition file.

---

### 🔧 Task 4: Prevent `:latest` Tags

Write a policy to block the use of `:latest` in Dockerfiles:

```rego
package docker.images

deny[msg] {
  input.Cmd == "FROM"
  endswith(input.Value, ":latest")
  msg := "Do not use the :latest tag in production"
}
📄 Save as: policy/docker/no_latest_tag.rego

🔧 Task 5: CI/CD Policy Gate Integration
Choose either GitHub or GitLab CI below:

✅ GitHub Actions
Extend .github/workflows/policy-check.yml to:

Run conftest test on:

Dockerfile

ECS task definition

Terraform plan (plan.json)

Kubernetes manifests

✅ GitLab CI
stages:
  - test

conftest-policy-check:
  stage: test
  image: alpine
  before_script:
    - apk add --no-cache curl tar
    - curl -L https://github.com/open-policy-agent/conftest/releases/download/v0.45.0/conftest_0.45.0_Linux_x86_64.tar.gz | tar xz
    - mv conftest /usr/local/bin/
  script:
    - conftest test Dockerfile
    - conftest test terraform/plan.json
    - conftest test k8s/
    - conftest test ecs/task-definition.json
📁 Folder Structure
Week13/
├── policy/
│   ├── docker/no_latest_tag.rego
│   ├── ecs/no_root.rego
│   ├── k8s/secure_pods.rego
│   └── terraform/
│       ├── require_tags.rego
│       ├── s3_encryption.rego
│       └── no_wildcard_iam.rego
├── k8s/
│   ├── notes-service.yaml
│   └── auth-service.yaml
├── terraform/
│   ├── main.tf
│   └── plan.json
├── Dockerfile
├── ecs/
│   └── task-definition.json
├── .github/workflows/policy-check.yml
✅ Completion Checklist
✅ Task	Description
🛡️ All 6 policies written and saved in correct folders	
🧪 All conftest tests pass (or fail with meaningful violations)	
🔁 CI/CD integration runs and fails on insecure code	
🚫 :latest, root, wildcards, and untagged resources blocked	
📦 App manifests and IaC validated before deploy	
📄 All policy-as-code committed to Git	
🔒 Security shifted left by default	
💬 Bonus Challenge (Optional)
Create an OPA policy test suite with sample violating configs to test against.

Use Conftest’s --fail-on-warn or --fail-on-deny flags to enforce strict behavior.

Visualize policy coverage with opa test.

⏭️ Up Next
➡️ Proceed to Week13/Security.md
We’ll review how Policy-as-Code enforces governance and enables security teams to audit and gate changes proactively.


---

Let me know when you're ready to move on to the **Security** section — where we’ll explore **auditing**, **drift prevention**, and **how Policy-as-Code empowers security without slowing teams down**.
You said:
Ready 
ChatGPT said:
Great — let’s wrap up Week 13 with the Security deep dive on how Policy-as-Code (PaC) strengthens governance, enforces compliance, and enables scalable security in your DevSecOps workflow.