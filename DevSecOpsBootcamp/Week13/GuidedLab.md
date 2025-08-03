# 🧪 Guided Lab – Policy-as-Code with OPA, Conftest, and CI/CD Enforcement

---

## 🎯 Objective

You’ll write and apply security policies to catch:
- Use of `:latest` container image tags
- ECS tasks running as `root`
- Overly permissive IAM roles (wildcards)
- Missing tags in Terraform
- Kubernetes manifests that mount host paths or allow privilege escalation

You’ll also:
- Integrate these policies into GitHub Actions or GitLab CI
- Run `conftest` locally and in CI
- Use OPA's Rego language to define your rules

---

## 🧰 Tools You'll Use

| Tool      | Use Case                         |
|-----------|----------------------------------|
| **OPA**   | Core policy engine using Rego    |
| **Conftest** | CLI to test YAML, JSON, HCL   |
| **GitHub Actions / GitLab CI** | Run checks during CI |
| **VS Code Rego Plugin** | (Optional) Syntax highlighting and linting for Rego |

---

## 🛠️ Setup

### 1. Install `conftest`

```bash
# macOS
brew install conftest

# Ubuntu
wget https://github.com/open-policy-agent/conftest/releases/download/v0.45.0/conftest_0.45.0_Linux_x86_64.tar.gz
tar xzf conftest_*.tar.gz
sudo mv conftest /usr/local/bin/
2. Create Policy Directory Structure
mkdir -p policy/docker policy/terraform policy/ecs policy/k8s
OPA will auto-detect policies in these folders.

🚫 Policy 1: Disallow :latest Tags in Dockerfiles
📄 policy/docker/no_latest_tag.rego

package docker.policies

deny[msg] {
  input.Cmd == "FROM"
  endswith(input.Value, ":latest")
  msg := "Do not use :latest tag in production"
}
🧪 Test it:

conftest test Dockerfile
🚫 Policy 2: ECS Task Must Not Run as Root
📄 policy/ecs/no_root.rego

package ecs.policies

deny[msg] {
  input.containerDefinitions[_].user == "root"
  msg := "ECS containers must not run as root"
}
🧪 Test it:

conftest test task-definition.json
🚫 Policy 3: IAM Roles Must Not Have Wildcards
📄 policy/iam/no_wildcards.rego

package iam.policies

deny[msg] {
  action := input.Statement[_].Action
  action == "*"
  msg := "Wildcard IAM actions are not allowed"
}
🧪 Test it:

conftest test iam-role.json
🚫 Policy 4: Terraform Must Include Tags
📄 policy/terraform/must_have_tags.rego

package terraform.policies

deny[msg] {
  not input.resource.aws_instance[_].tags
  msg := "AWS instances must have tags"
}
🧪 Test it:

conftest test main.tf.json
Use terraform show -json > main.tf.json to convert to JSON format.

🚫 Policy 5: Kubernetes Pod Must Not Use hostPath or Allow Privilege Escalation
📄 policy/k8s/secure_pods.rego

package k8s.policies

deny[msg] {
  input.kind == "Pod"
  input.spec.volumes[_].hostPath
  msg := "hostPath is not allowed in Pods"
}

deny[msg] {
  input.spec.containers[_].securityContext.allowPrivilegeEscalation
  msg := "Privileged escalation must be disabled"
}
🧪 Test it:

conftest test pod.yaml
🧪 CI/CD Integration – GitHub Actions Example
📄 .github/workflows/policy-check.yml

name: Policy Checks

on: [push, pull_request]

jobs:
  policy-check:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Install conftest
        run: |
          wget https://github.com/open-policy-agent/conftest/releases/download/v0.45.0/conftest_0.45.0_Linux_x86_64.tar.gz
          tar xzf conftest_*.tar.gz
          sudo mv conftest /usr/local/bin/

      - name: Run policy checks
        run: |
          conftest test Dockerfile
          conftest test ecs/task-definition.json
          conftest test terraform/main.tf.json
          conftest test k8s/pod.yaml
✅ Completion Checklist
Task	Complete?
Installed OPA + Conftest CLI	✅
Created 5 policy files in Rego	✅
Validated real files (Dockerfile, TF, IAM, K8s)	✅
Ran policies via conftest test	✅
Embedded policies into CI/CD pipeline	✅
Can now block insecure config pre-deploy	✅
🔄 Next Step
➡️ Proceed to Week13/ChallengeLab.md
You’ll define custom policies for your microservices app, enforce them in CI/CD, and validate secure deployment behaviors.


---

Let me know when you're ready to move on to the **Challenge Lab**, or if you’d like to dive deeper into any of the tools before that (e.g., writing advanced Rego, using Gatekeeper, or ECS IAM validation).
You said:
Let’s do kubernetes and Iac next for the guided lab before the challenge lab
ChatGPT said:
Excellent — let’s expand the Week 13 Guided Lab by diving deeper into Kubernetes and Infrastructure-as-Code (Terraform) policy enforcement using OPA + Conftest. This gives us control over what can be deployed — even before it hits your cluster or cloud environment.

📁 Week13/GuidedLab-K8s-Terraform.md
# 🧪 Guided Lab – Kubernetes & Terraform Policy-as-Code with OPA + Conftest

---

## 🎯 Objectives

You'll enforce policies that:

- Block **privilege escalation** and **hostPath** in Kubernetes
- Require **securityContext** to drop Linux capabilities and run as non-root
- Ensure all **Terraform resources have tags**
- Ensure **S3 buckets are encrypted**
- Test these rules using **conftest**
- Integrate with GitHub Actions or GitLab CI

---

## 🧰 Tooling Recap

| Tool       | Purpose                          |
|------------|----------------------------------|
| `conftest` | CLI to test config files         |
| `rego`     | OPA policy language              |
| `terraform show -json` | Converts plans to JSON for testing |
| `kubectl`  | View cluster manifests (optional) |

---

## 📦 Kubernetes Policy Enforcement

### 1. Block Dangerous Pod Configurations

📄 `policy/k8s/no_privileged.rego`

```rego
package k8s.security

deny[msg] {
  input.kind == "Pod"
  container := input.spec.containers[_]
  container.securityContext.allowPrivilegeEscalation == true
  msg := "Privileged escalation is not allowed"
}

deny[msg] {
  input.kind == "Pod"
  input.spec.volumes[_].hostPath
  msg := "hostPath volumes are not allowed in Pods"
}
✅ Test it:

conftest test k8s/pod.yaml
2. Enforce Hardened Security Context
📄 policy/k8s/hardening.rego

package k8s.hardening

deny[msg] {
  input.kind == "Pod"
  container := input.spec.containers[_]
  not container.securityContext.runAsNonRoot
  msg := "Container must run as non-root"
}

deny[msg] {
  input.kind == "Pod"
  container := input.spec.containers[_]
  not container.securityContext.capabilities.drop[_] == "ALL"
  msg := "All Linux capabilities must be dropped"
}
✅ Test it:

conftest test k8s/hardened-pod.yaml
📦 Terraform Policy Enforcement
1. All AWS Resources Must Have Tags
📄 policy/terraform/require_tags.rego

package terraform.tags

deny[msg] {
  resource := input.resource[_][_]
  not resource.tags
  msg := sprintf("Resource %s must have tags", [resource])
}
✅ Convert TF plan to JSON:

terraform show -json > plan.json
conftest test plan.json
2. S3 Buckets Must Be Encrypted
📄 policy/terraform/s3_encryption.rego

package terraform.security

deny[msg] {
  bucket := input.resource.aws_s3_bucket[_]
  not bucket.server_side_encryption_configuration
  msg := "S3 buckets must have encryption enabled"
}
✅ Run test:

conftest test plan.json
🤖 CI/CD Example – GitHub Actions (Extended for K8s & TF)
📄 .github/workflows/policy-check.yml

name: Policy Checks

on: [push, pull_request]

jobs:
  conftest:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Install conftest
        run: |
          wget https://github.com/open-policy-agent/conftest/releases/download/v0.45.0/conftest_0.45.0_Linux_x86_64.tar.gz
          tar xzf conftest_*.tar.gz
          sudo mv conftest /usr/local/bin/

      - name: Run Conftest for K8s
        run: |
          conftest test k8s/*.yaml

      - name: Convert Terraform plan to JSON
        run: |
          terraform init
          terraform plan -out=tfplan
          terraform show -json tfplan > plan.json

      - name: Run Conftest for Terraform
        run: |
          conftest test plan.json
✅ Completion Checklist
Task	Complete?
Wrote Rego policies for Kubernetes security	✅
Validated pod YAML for hardening and privilege rules	✅
Converted Terraform plan to JSON	✅
Wrote policies to check S3 encryption and resource tags	✅
Embedded tests into CI/CD pipeline	✅
🧠 You Learned
✅ How to apply security policies to Kubernetes manifests
✅ How to ensure Terraform IaC enforces compliance standards
✅ How to build and test Rego policies with conftest
✅ How to run those tests in CI/CD before merge or deploy

🔄 Next Step
➡️ Proceed to Week13/ChallengeLab.md
You’ll define custom policies for your evolving app, test violations, and enforce gates in CI/CD with GitLab/GitHub.


---

Let me know when you're ready to jump into the **Challenge Lab**, or if you’d like to dive deeper into a specific IaC or Kubernetes security case!
You said:
Ready 
ChatGPT said:
Perfect. Let’s dive into the Week 13 Challenge Lab, where you’ll apply what you've learned to secure your DevSecOps project using real-world policy enforcement across Kubernetes and IaC.