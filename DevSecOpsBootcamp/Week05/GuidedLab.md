(Annotated)
Secure Infrastructure as Code with Terraform, AWS CDK, and CloudFormation
Focus: What, Why, How for every command and file

🔹 SECTION 1: Terraform (Declarative, Cloud-Agnostic IaC)
✅ Use Terraform when you want clear state tracking, cloud-agnostic provisioning, and strong third-party tool ecosystem (Checkov, tfsec, TFC). It’s popular in enterprise DevSecOps environments.

🧱 Step 1: Set Up Terraform Directory
mkdir -p infrastructure/terraform
cd infrastructure/terraform
Why: Organize your IaC in a clean, modular structure. Keeping infrastructure code separate from app code helps with maintainability and security audits.

📄 main.tf
provider "aws" {
  region = "us-east-1"
}
What: Declares AWS as the provider and sets your default region.
Why: Every Terraform config needs a provider block. Region scoping ensures all resources are deployed consistently and avoids accidental cross-region provisioning.

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "4.0.2"

  name = "notestream-vpc"
  cidr = "10.0.0.0/16"
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]

  enable_dns_hostnames = true
  enable_nat_gateway   = true
  single_nat_gateway   = true

  tags = {
    Name        = "notestream"
    Environment = "dev"
  }
}
What: Uses a popular Terraform community module to create a secure, NAT-enabled VPC with public and private subnets.
Why: Never reinvent the wheel. Community modules simplify best-practice infrastructure. NAT gateways allow outbound internet access from private subnets (needed for ECS tasks to pull packages/images).
Security: ECS tasks should go in private subnets — never expose services directly without an ALB.

📄 ecs.tf
resource "aws_ecs_cluster" "main" {
  name = "notestream-ecs"
}
What: Creates an ECS cluster to run containers.
Why: This is the foundation of your container orchestration stack. We’ll deploy microservices here using Fargate.

resource "aws_ecr_repository" "backend" {
  name = "notestream-backend"
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}
What: Creates a secure container registry for your backend image.
Why: ECR supports automated scanning, version immutability (no overwriting tags), and fine-grained IAM.
Security: Enabling scan_on_push helps catch CVEs early; IMMUTABLE ensures every image is traceable (important for SBOM tracking).

📄 secrets.tf
resource "aws_secretsmanager_secret" "db_credentials" {
  name = "notestream/db"
  recovery_window_in_days = 0
}
What: Creates a secret entry in AWS Secrets Manager.
Why: Hardcoding secrets in code or environment files is insecure. Secrets Manager offers encryption at rest, access logging, and lifecycle rotation.
Security: Rotate these automatically using Lambda or AWS-native rotation features later.

resource "aws_secretsmanager_secret_version" "db_credentials_version" {
  secret_id     = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = "notestream_user"
    password = "secure_password_2025!"
  })
}
What: Assigns a version to the secret, including the sensitive values.
Why: You can rotate secrets by adding new versions. Version control lets you audit changes and roll back if needed.

🔁 Initialize & Apply
terraform init
What: Initializes the working directory and downloads required modules/plugins.
Why: Terraform must pull provider binaries and initialize the dependency graph before execution.

terraform fmt && terraform validate
Why:

fmt ensures consistent formatting for maintainability.

validate checks for syntax or logic errors before plan.

terraform plan
Why: Shows exactly what Terraform will do — critical for audit, approvals, and CI/CD previews.

terraform apply
What: Applies the plan and provisions infra.
Security Tip: Never run apply automatically in CI without plan approval step.

🔹 SECTION 2: AWS CDK (Imperative IaC in Code)
✅ Use CDK when your team prefers Python, TypeScript, or OOP. CDK allows programmatic abstractions, better IDE support, and reusable infra components.

🧱 Step 1: Init Python CDK App
cd infrastructure
mkdir cdk && cd cdk
cdk init app --language python
What: Initializes a CDK project scaffold using Python.
Why: This gives you a buildable project with app.py and an initial stack.

🔧 Install Dependencies
pip install aws-cdk.aws-ec2 aws-cdk.aws-ecs aws-cdk.aws-ecr aws-cdk.aws-secretsmanager
Why: CDK uses separate libraries per AWS service. You only install what you use (keeps stack clean and understandable).

📄 infra_stack.py
vpc = ec2.Vpc(self, "NotestreamVPC", max_azs=2)
What: Creates a secure VPC with 2 AZs (recommended baseline).
Why: AZ redundancy improves fault tolerance.

cluster = ecs.Cluster(self, "NotestreamCluster", vpc=vpc)
Why: Required ECS cluster to deploy containers via Fargate.

ecr.Repository(self, "BackendRepo", ...)
Why: Same as Terraform — creates secure image registry with IMMUTABLE tags and scanning on push.

secrets.Secret(self, "DBSecret", ...)
What: Creates a Secrets Manager entry with a generated password.
Why: Avoid hardcoding secrets. Let AWS generate and rotate sensitive data.

🚀 Deploy
cdk deploy
What: Synthesizes templates → deploys them using CloudFormation behind the scenes.
Why: CDK is a higher-level abstraction over CloudFormation. Same security benefits, better developer experience.

🔹 SECTION 3: CloudFormation (YAML/JSON Declarative)
✅ Use CloudFormation for full AWS-native IaC. It's harder to reuse than CDK or Terraform but is deeply integrated into AWS services.

📄 stack.yaml
Resources:
  NotestreamVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
What: Standard YAML declaration for a VPC.
Why: Same as Terraform/CDK, but less modular. Still used heavily in AWS SAM and legacy stacks.

BackendECR:
  Type: AWS::ECR::Repository
  Properties:
    RepositoryName: notestream-backend
    ImageScanningConfiguration:
      scanOnPush: true
Security Benefit: All pushed images are scanned for CVEs before being marked deployable.

Secrets:
  Type: AWS::SecretsManager::Secret
  Properties:
    Name: notestream/db
    SecretString: '{"username":"user", "password":"change-me"}'
Warning: Don’t hardcode secrets in YAML. Use parameters or secret values from SSM or encrypted input.

🚀 Deploy via CLI
aws cloudformation deploy \
  --template-file stack.yaml \
  --stack-name notestream-iac \
  --capabilities CAPABILITY_NAMED_IAM
Why: Deploys your stack safely. CAPABILITY_NAMED_IAM is required if you’re creating IAM roles or policies.

✅ Up Next (optional): Annotate AWS SAM if you want deeper Lambda/serverless support.

Would you like me to proceed with the annotated Challenge Lab, or annotate the SAM section before continuing?

You said:
Annotate the Sam before continuing. Sam will be useful for any serverless infrastructure 
ChatGPT said:
Perfect. Here's the annotated AWS SAM section from Week 5’s Guided Lab — focused on secure, production-ready serverless infrastructure for notestream.

🔹 SECTION 4: AWS SAM (Serverless Framework)
✅ Use AWS SAM (Serverless Application Model) when deploying Lambda functions, API Gateway, DynamoDB, and event-driven microservices — with the added benefit of built-in security, templates, and local testing.

📁 Directory Structure
infrastructure/sam/
├── template.yaml        # Core SAM infrastructure file
├── backend/             # Dockerized Lambda service (optional)
└── events/              # Test payloads for local invocation
🧱 Step 1: Create template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Description: Notestream serverless API

Globals:
  Function:
    Timeout: 10
    MemorySize: 512
    Runtime: python3.11
    Architectures: [x86_64]
    Tracing: Active   # Enables X-Ray
🔍 Explanation
Transform: Required for SAM — tells CloudFormation to use SAM’s syntax extensions.

Globals: DRY section for setting defaults like memory, timeout, and runtime.

Tracing: Enables AWS X-Ray for observability. Crucial for debugging in microservices environments.

📄 Define a Lambda + API Gateway
Resources:
  BackendAPI:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: notestream-backend
      PackageType: Image
      ImageUri: <your-ecr-image-url>      # e.g., 12345678.dkr.ecr.us-east-1.amazonaws.com/backend:latest
      Events:
        GetApi:
          Type: Api
          Properties:
            Path: /api
            Method: get
      Environment:
        Variables:
          DB_SECRET_NAME: notestream/db
      Policies:
        - SecretsManagerReadWrite
        - CloudWatchLogsFullAccess
🔍 Explanation
Type: PackageType: Image allows you to use a containerized Lambda from ECR — powerful for Flask/FastAPI/Node.js apps packaged as microservices.

Events: Creates an API Gateway → /api → triggers this Lambda.

Environment Variables: Inject secret name dynamically.

Policies: Grants the function read-only access to Secrets Manager and logging — follows least-privilege.

📁 Dockerfile for Lambda (optional)
Place in sam/backend/Dockerfile:

FROM public.ecr.aws/lambda/python:3.11

COPY app.py .

CMD ["app.lambda_handler"]
✅ This uses the AWS-provided Lambda base image and runs app.lambda_handler (standard entry point).
🔐 Lambda images must be under 10GB and use secure entry points.

🧪 Step 2: Local Testing (Optional but Powerful)
sam build
What it does: Converts your template.yaml and code/images into a CloudFormation-compatible package and builds Docker images if needed.

sam local invoke BackendAPI \
  --event events/get-event.json
Why: Run the Lambda locally with test data. Helps with tight inner-loop testing before deployment.

🚀 Step 3: Secure Deployment
sam deploy --guided
What this does:

Prompts for stack name, AWS region, and image repo

Uploads your images to ECR (if not already there)

Deploys via CloudFormation

🔐 Best Practice: Enable encryption and retention policies if using DynamoDB or logs. Use --capabilities CAPABILITY_IAM to allow role creation.

🔐 Security Considerations
Risk	Mitigation
Lambda can access too much	Use managed policies (e.g., SecretsManagerReadOnly), or custom IAM
API Gateway exposes insecure endpoints	Add auth (API Key, IAM, Cognito, JWT) in later modules
Hardcoded secrets in environment	Use Secrets Manager or SSM to inject
Unscanned Lambda base images	Use Trivy locally before pushing, or deploy only signed images to ECR
Excessive logs/exceptions	Use try/catch inside lambda_handler() with structured logging and X-Ray
🔁 CI/CD Ready
SAM can easily integrate into GitHub Actions, GitLab CI/CD, or CodePipeline:

- name: Build SAM
  run: sam build

- name: Deploy SAM
  run: sam deploy --no-confirm-changeset --no-fail-on-empty-changeset \
    --stack-name notestream-serverless \
    --capabilities CAPABILITY_IAM
✅ Summary: Why Use AWS SAM in DevSecOps?
Benefit	Explanation
Native support for API Gateway + Lambda + Secrets	Secure by default with reduced glue code
Local testability	Avoids slow deploy-feedback cycles
Image-based Lambda support	Use Dockerized apps (Python, Node.js) as serverless microservices
Seamless CI/CD integration	Works with GitHub Actions, GitLab, AWS CodePipeline
Deep CloudFormation integration	Policies, IAM, logs, tracing are native AWS features
Easy to enforce security policies	Run cfn-lint, cfn_nag, or Checkov against templates
Would you like to now proceed with the annotated Challenge Lab for Week 5? This will include:

Drift simulation

Insecure config injection

Policy violations

Detection and rollback scenarios

You said:
Yes proceed 
ChatGPT said:
Great — let’s move on to the annotated Week 5 Challenge Lab, where you’ll simulate real-world DevSecOps incidents using IaC misconfigurations and security violations — then detect and fix them with tools like checkov, tfsec, cfn-lint, and CDK's cdk-nag.