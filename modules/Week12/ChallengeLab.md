# 🧪 Challenge Lab – Secure ECS Service Isolation and Cross-Version Testing

---

## 🎯 Objective

Put your skills to the test by deploying two services:

- A **dev version** of `auth-service` (v1)
- Two **staging versions** of `notes-service` (`v1` and `v2`)

Your challenge is to:

1. Prevent `auth-service` in **dev** from calling itself (loopback)
2. Allow it to call **only** `notes-service-v2` in staging
3. Apply **least privilege IAM roles**
4. Enforce **runtime hardening**
5. Block insecure traffic patterns and validate connectivity via logs or curl

---

## 🛠️ Lab Requirements

| Component | Requirement |
|----------|-------------|
| ECS Cluster | Exists with public/private subnets |
| IAM Roles | 1 per service with scoped policies |
| Namespaces | `dev`, `staging` |
| Task Definition | Hardened, Service Connect enabled |
| Image Tags | Use v1 for dev, v2 for staging |

---

## 🧩 Part 1: Deploy Staging Versions

Create two services in the `staging` namespace:

- `notes-service-v1.staging`
- `notes-service-v2.staging`

Both should respond on port `3001`.

Verify you can curl:

```bash
curl http://notes-service-v2.staging:3001/health
✅ Should return 200 OK.

🧩 Part 2: Deploy Dev Auth-Service
Deploy auth-service in the dev namespace.

This service:

Must have IAM scoped only to what it needs (e.g., Dynamo access)

Must not be able to access auth-service.dev (itself)

Must be able to reach only notes-service-v2.staging

🧪 Part 3: Attempt Unauthorized Loopback
Inside the container, run:

curl http://auth-service.dev:3000/api/profile
✅ This should fail — your app or network rules must block it.

You may enforce this using:

Application logic (deny calls to its own DNS)

Security groups (block outbound to its own IP/DNS)

Env variable-based allowlisting

🧪 Part 4: Allow Cross-Version Call
From auth-service.dev, call:

curl http://notes-service-v2.staging:3001/api/notes
✅ This should succeed.

Make sure:

Service Connect routes it correctly

The DNS is resolvable

Staging v2 is accessible from the dev namespace

🔐 Part 5: IAM Audit
From the AWS CLI:

aws iam get-role-policy \
  --role-name ecs-auth-task-role \
  --policy-name auth-access
✅ Confirm the role only has permission to:

Access DynamoDB:AuthTable

No permissions to invoke Lambda, access S3, etc.

🛡️ Part 6: Runtime Hardening
Inspect the task definition:

✅ It should include:

"user": "1000"

"readonlyRootFilesystem": true

"capabilities": { "drop": ["ALL"] }

Also test within the container:

id   # should return uid=1000
touch /tmp/test  # should fail if root FS is readonly
✅ Completion Checklist
Task	Status
notes-service-v1 and v2 deployed in staging	✅
auth-service deployed in dev with IAM and runtime hardening	✅
Loopback to auth-service.dev fails	✅
Access to notes-service-v2.staging succeeds	✅
IAM role is scoped only to required permissions	✅
Runtime settings enforced (non-root, readonly FS)	✅
🧠 Reflection Prompts
How would you enforce these rules at scale across 50+ services?

What if notes-service was compromised? Could it access prod?

Where would you store access rules (e.g., YAML, Terraform, CDK)?

🔄 Next Step
➡️ Proceed to Week12/Security.md
We’ll break down how these boundaries enforce Zero Trust, prevent lateral movement, and integrate into broader DevSecOps workflows.


---

Let me know when you're ready for the **Week 12 Security** section, or if you'd like to explore CDK for any part of this lab before we continue.
You said:
Ready
ChatGPT said:
Excellent — now let’s break down the security implications of what we just implemented in ECS Fargate, connecting it directly to DevSecOps best practices and Zero Trust principles.