# 🧪 Guided Lab – Secure ECS Fargate Deployment with Service Connect & IAM Isolation

---

## 🎯 Goal

Securely deploy `auth-service` and `notes-service` into ECS using:

- 🔐 **Per-service IAM roles**
- 🧱 **Service Connect namespaces** for dev, staging
- 🌐 **Cross-environment communication with versioning**
- ❌ Block same-service loopback (e.g. dev-auth → dev-auth)
- ✅ Allow dev-auth → staging-notes:v2 for integration testing

---

## 🛠️ Prerequisites

- AWS CLI configured and logged in
- ECS Fargate cluster created (`my-cluster`)
- Cloud Map service discovery enabled
- A VPC with at least 2 public/private subnets and internet gateway
- Docker images for:
  - `auth-service`
  - `notes-service-v1`, `notes-service-v2`

---

## 🗂️ Step 1: Create Service Connect Namespaces

```bash
aws servicediscovery create-namespace \
  --name dev \
  --type HTTP \
  --creator-request-id dev-$(date +%s)

aws servicediscovery create-namespace \
  --name staging \
  --type HTTP \
  --creator-request-id staging-$(date +%s)
Each namespace will be used to scope service discovery.

🔐 Step 2: Create IAM Task Roles per Service
📁 iam/auth-task-role.json

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DynamoAccess",
      "Effect": "Allow",
      "Action": ["dynamodb:GetItem", "dynamodb:PutItem"],
      "Resource": "arn:aws:dynamodb:*:*:table/AuthTable"
    }
  ]
}
📁 iam/notes-task-role.json

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3Access",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::notes-data/*"
    }
  ]
}
Create IAM roles:

aws iam create-role \
  --role-name ecs-auth-task-role \
  --assume-role-policy-document file://iam/ecs-trust.json

aws iam put-role-policy \
  --role-name ecs-auth-task-role \
  --policy-name auth-access \
  --policy-document file://iam/auth-task-role.json
Repeat for notes-service as needed.

📁 iam/ecs-trust.json

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "ecs-tasks.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
🚀 Step 3: Define Task Definitions with Service Connect
📁 ecs/auth-task-def.json

{
  "family": "auth-service",
  "networkMode": "awsvpc",
  "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::<account-id>:role/ecs-auth-task-role",
  "containerDefinitions": [
    {
      "name": "auth",
      "image": "123456789012.dkr.ecr.us-west-2.amazonaws.com/auth-service:latest",
      "portMappings": [
        {
          "containerPort": 3000,
          "name": "auth",
          "appProtocol": "http"
        }
      ],
      "essential": true
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512"
}
Register it:

aws ecs register-task-definition \
  --cli-input-json file://ecs/auth-task-def.json
Repeat for notes-service (with v1, v2 variations in image/tag).

📦 Step 4: Deploy Services into Cluster with Connect Enabled
aws ecs create-service \
  --cluster my-cluster \
  --service-name auth-service-dev \
  --task-definition auth-service \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xyz],securityGroups=[sg-xyz],assignPublicIp=ENABLED}" \
  --service-connect-configuration "enabled=true,namespace=dev,services=[{portName=auth}]" \
  --scheduling-strategy REPLICA
Same idea for:

notes-service-v1 (in staging)

notes-service-v2 (in staging)

auth-service (in dev)

🔁 Step 5: Enable Cross-Version Communication
Allow auth-service.dev to call notes-service-v2.staging:

curl http://notes-service-v2.staging:3001/api/notes
You may configure DNS routing and allow-listing via:

Cloud Map DNS-based routing

Security groups (for port-level access control)

Service Connect’s internal proxy layer

❌ Block auth-service.dev → auth-service.dev using app-level or proxy-based rejection (handled in code or via ALB if needed).

🔒 Step 6: Harden the Task Runtime
In the containerDefinitions section, add:

"linuxParameters": {
  "capabilities": {
    "drop": ["ALL"]
  }
},
"readonlyRootFilesystem": true,
"user": "1000"
🛡️ This drops all Linux capabilities, uses a non-root user, and makes the container filesystem read-only.

✅ Completion Checklist
Task	✅
Created scoped namespaces for dev and staging	✅
Created per-service IAM roles for Fargate tasks	✅
Registered secure task definitions with roles	✅
Deployed auth-service and notes-service into ECS with Service Connect	✅
Allowed versioned access (e.g., dev → staging-v2)	✅
Dropped container capabilities and set user	✅
🧠 You Just Learned:
How to securely deploy services in ECS using Fargate

How to isolate environments using Service Connect namespaces

How to define least privilege IAM roles per microservice

How to use ECS Service Connect for version-aware routing

How to apply runtime security settings (drop CAP_*, rootless tasks)

➡️ Up Next:
Week12/ChallengeLab.md
Where you’ll simulate a misconfiguration, audit IAM permissions, and block unintended cross-service access.


---

Let me know when you're ready for the **Challenge Lab**, or if you'd like to expand any part of the Guided Lab above (e.g., CDK, Cloud Map internals, runtime audit logging).
You said:
Ready 
ChatGPT said:
Great — let’s move into the Week 12 Challenge Lab. Here, you’ll test your understanding of ECS security boundaries, IAM scoping, and controlled service-to-service access using ECS Fargate + Service Connect.