# Secure Infrastructure as Code with Terraform, CFN & AWS SAM

## 🧪 Scenario

Your DevSecOps team is tasked with building infrastructure for the `notes-service` as part of the evolving note/task manager app. You’ll:

  * Provision a secure **VPC**, **ECS Cluster**, **ECR repo**, and **IAM roles** using **Terraform**.
  * Define a serverless endpoint using **AWS SAM**.
  * Create a **CloudFormation** template for static infrastructure (e.g., S3 bucket).
  * Scan all infrastructure code for misconfigurations using `tfsec`, `checkov`, and `cfn-nag`.

-----

## 🛠️ Part 1: Secure VPC + ECS Cluster using Terraform

### 🔹 Step 1.1: Create project structure

```bash
mkdir -p iac/terraform/notes-infra
cd iac/terraform/notes-infra
```

### 🔹 Step 1.2: Create `main.tf`

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "secure_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "notes-secure-vpc"
  }
}

resource "aws_subnet" "private_subnet" {
  vpc_id     = aws_vpc.secure_vpc.id
  cidr_block = "10.0.1.0/24"
  tags = {
    Name = "notes-private-subnet"
  }
}

resource "aws_ecr_repository" "notes_repo" {
  name                 = "notes-service"
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecs_cluster" "notes_cluster" {
  name = "notes-ecs-cluster"
}
```

### 🔹 Step 1.3: Initialize and apply

```bash
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

✅ You now have a secure ECS-ready **VPC**, **subnet**, and **ECR repository** with image scanning enabled.

### 🔍 Step 1.4: Scan Terraform code with `tfsec` and `checkov`

```bash
# Install tools
brew install tfsec
pip install checkov

# Run scans
tfsec .
checkov -d .
```

Look for alerts like:

  * Insecure CIDR blocks (e.g., `0.0.0.0/0`)
  * Missing tags
  * IAM policies with `*`
  * Lack of encryption

✅ **Fix any high-severity issues before continuing.**

-----

## 🛠️ Part 2: Define a Lambda + API using AWS SAM

### 🔹 Step 2.1: Scaffold project

```bash
# Navigate out of the terraform directory
cd ../../../
sam init --runtime python3.11 --name notes-sam --app-template hello-world
cd notes-sam
```

This creates:

```
notes-sam/
├── template.yaml
├── hello_world/
└── tests/
```

### 🔹 Step 2.2: Review and secure `template.yaml`

Key checks:

  * Enable **X-Ray tracing**.
  * Add **environment variable encryption**.
  * Attach only **required IAM roles**.

<!-- end list -->

```yaml
Resources:
  NotesApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: notes-api
      Handler: app.lambda_handler
      Runtime: python3.11
      Timeout: 10
      Policies: AWSLambdaBasicExecutionRole
      Tracing: Active
```

### 🔹 Step 2.3: Validate the template

```bash
sam validate
```

✅ Confirms syntax and AWS resource compliance.

### 🔹 Step 2.4: Deploy (optional)

```bash
sam build
sam deploy --guided
```

### 🔍 Step 2.5: Scan with `cfn-nag`

```bash
brew install cfn-nag
cfn_nag_scan --input-path template.yaml
```

✅ Look for:

  * Public S3 buckets
  * Over-permissive IAM roles
  * Functions without logging or tracing

-----

## 🛠️ Part 3: Static Infra with CloudFormation

Create a basic CloudFormation template `s3-static-bucket.yaml`:

```yaml
Resources:
  NotesS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: notesapp-static-data
      VersioningConfiguration:
        Status: Enabled
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
```

Scan the template:

```bash
cfn_nag_scan --input-path s3-static-bucket.yaml
```

✅ Ensure all buckets have **public access blocked** and **versioning enabled**.

-----

## 🚨 Part 4: Add IaC Security to CI/CD

### GitHub Actions Snippet

Add the following jobs to your workflow file (e.g., `.github/workflows/ci.yml`).

```yaml
jobs:
  tfsec:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Scan Terraform
        run: |
          # These install steps may vary based on your runner setup
          pip install checkov
          # Using a pre-built action is often better than brew
          # For example: uses: aquasecurity/tfsec-action@v1.0.0
          tfsec ./iac/terraform
          checkov -d ./iac/terraform

  cfn:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Scan CFN templates
        run: |
          # These install steps may vary based on your runner setup
          # For example: gem install cfn-nag
          cfn_nag_scan --input-path ./iac/cfn
```

✅ **Fail the build if high-severity findings are detected.**

-----

## ✅ Success Criteria

| Task                  | Validation                                 |
| :-------------------- | :----------------------------------------- |
| **Terraform infra** | Created and passes `tfsec` + `checkov`     |
| **SAM function** | Validates and scans clean via `cfn-nag`    |
| **CFN static bucket** | Has public access blocked                  |
| **CI/CD enforcement** | Security scans run and fail build on error |
| **Issues fixed** | No CRITICAL findings left unpatched        |

-----

## 🧪 Bonus: Advanced CDK Patterns

### ECS Task Definition with Secrets Injection (CDK)

Here’s how you can securely inject secrets into an ECS task using the AWS CDK.
File: `lib/auth-service-stack.ts`

```typescript
import * as cdk from 'aws-cdk-lib';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';
import { Construct } from 'constructs';

export class AuthServiceStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = ec2.Vpc.fromLookup(this, 'VPC', { isDefault: true });

    const cluster = new ecs.Cluster(this, 'Cluster', { vpc });

    const secret = secretsmanager.Secret.fromSecretNameV2(
      this,
      'ImportedSecret',
      'auth-service-db-secret'
    );

    const taskRole = new iam.Role(this, 'TaskRole', {
      assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
    });

    secret.grantRead(taskRole);

    const fargateService = new ecs_patterns.ApplicationLoadBalancedFargateService(this, 'FargateService', {
      cluster,
      cpu: 256,
      memoryLimitMiB: 512,
      taskImageOptions: {
        image: ecs.ContainerImage.fromRegistry('node:20-alpine'),
        containerPort: 3000,
        secrets: {
          DB_SECRET: ecs.Secret.fromSecretsManager(secret),
        },
        taskRole,
      },
      desiredCount: 2,
    });
  }
}
```

✅ **Explanation:**

  * The secret is passed securely into the container as an environment variable (`DB_SECRET`).
  * Only the `taskRole` is granted permission to read the secret, enforcing **least privilege**.

### 📉 Drift Detection with `driftctl`

Install `driftctl`:

```bash
brew install driftctl
```

Run scan against your remote Terraform state:

```bash
driftctl scan --from tfstate+s3://my-state-bucket/path/to/terraform.tfstate
```

🚨 Detects resources in AWS that are not managed by Terraform, helping prevent **shadow infrastructure** and configuration drift.

### 💾 Terraform Remote State Backend

Create a `backend.tf` file to configure a secure, remote backend for your state file, enabling collaboration and state locking.

```hcl
terraform {
  backend "s3" {
    bucket         = "my-secure-terraform-state"
    key            = "dev/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

---

### 📁 `Week10/CompletionChecklist.md`

```md
# ✅ Week 10 Completion Checklist – Infrastructure as Code (IaC) & Security

This checklist ensures all key infrastructure and security practices covered in the Guided Lab are completed and committed.

---

## 🔧 Terraform-Based Provisioning

- [x] VPC with CIDR and DNS hostnames created (`vpc.tf`)
- [x] Public subnet with proper AZ targeting and IP mapping
- [x] ECS Cluster created and named (`ecs.tf`)
- [x] ECS Task Definition created with Fargate compatibility and secure networking mode (`awsvpc`)
- [x] ECS Service deployed with correct networking configuration
- [x] IAM Execution Role created using `sts:AssumeRole` for ECS tasks
- [x] Attached `AmazonECSTaskExecutionRolePolicy` to task role (minimal permissions)
- [x] Applied Terraform using `terraform plan/apply` with environment-based tfvars (`dev`, `staging`)
- [x] Configured remote state backend using S3 and DynamoDB lock table (`backend.tf`)
- [x] Scanned Terraform with:
  - `tfsec` for security misconfigurations
  - `checkov` for compliance rules
  - `tflint` for syntax/style best practices

---

## 🧱 AWS CDK (TypeScript) Provisioning

- [x] CDK project initialized with `cdk init app --language=typescript`
- [x] Created SecretsManager secret with autogenerated credentials (`SecretsStack`)
- [x] ECS Task securely pulls secret via `secretsManagerEnvironmentVariables`
- [x] IAM task role explicitly granted permission to read secret only
- [x] Created Fargate service with CDK Patterns (`ApplicationLoadBalancedFargateService`)
- [x] Created CodePipeline with GitHub source and CodeBuild stage (`PipelineStack`)
- [x] Used `cdk.json` + `ENV` env var for dynamic multi-env deployment (`main.ts`)
- [x] Deployed CDK stacks using `cdk deploy` per environment

---

## 🔐 Security Hardening & DevSecOps Controls

- [x] Avoided `*` IAM actions in Terraform and CDK roles
- [x] Injected secrets into containers securely (no plaintext in env or code)
- [x] Avoided use of AWS Console for infrastructure provisioning
- [x] Added `cdk-nag` for static analysis of CDK constructs (CIS, NIST checks)
- [x] Used Git version control and PRs to track and review IaC
- [x] Separated infrastructure by environment (e.g., dev, staging) in both Terraform and CDK
- [x] Used `driftctl` to detect out-of-band changes in AWS infra

---

## 📦 Application Evolution

- [x] Deployed secure `auth-service` with secrets, IAM, networking via Terraform
- [x] Injected DB credentials from SecretsManager into ECS container at runtime
- [x] Laid foundation for app-wide CI/CD automation
- [x] Infra-as-Code now governs app deployment lifecycle for secure environments

---
```


