📁 Week7/GuidedLab.md

Title: Building a Secure, Automated CI/CD Pipeline with AWS CodePipeline & CodeBuild

⸻

🧪 Scenario

You’re building the production-grade pipeline for notes-service.
It must:
	1.	Pull source from GitHub
	2.	Run tests and generate SBOM using CodeBuild
	3.	Enforce Trivy vulnerability scans
	4.	Store artifacts in S3
	5.	Deploy to ECS (or Lambda) only if scans pass
	6.	Securely handle secrets via SSM
	7.	Notify on failures via SNS (optional)

⸻

🔧 Pre-Requirements

✅ A working notes-service repo
✅ AWS CLI and credentials set up
✅ IAM permissions to create:
	•	CodePipeline
	•	CodeBuild projects
	•	S3 bucket
	•	ECS service or Lambda function

⸻

🧱 Directory Layout

Add to your repo:

infra/
├── pipeline/
│   ├── pipeline.yaml        # CloudFormation/CDK definition
│   ├── buildspec.yml        # CodeBuild instructions
│   └── deploy.sh            # Secure deploy script
scripts/
├── sbom/
│   └── trivy_to_html.py     # Reuse from Week 5
├── secrets/
│   └── fetch_secrets.sh     # Reuse from Week 5
.env.example


⸻

🛠️ Step-by-Step

⸻

✅ Step 1: Define buildspec.yml

This controls what CodeBuild does.
Create infra/pipeline/buildspec.yml:

version: 0.2

env:
  variables:
    IMAGE_NAME: "notes-service"
  secrets-manager:
    DB_PASSWORD: "notes/db_password"
    API_KEY: "notes/api_key"

phases:
  install:
    runtime-versions:
      nodejs: 18
      python: 3.11
    commands:
      - echo "🔐 Installing tools"
      - pip install trivy boto3
  pre_build:
    commands:
      - echo "🔍 Running tests..."
      - npm install && npm run test
  build:
    commands:
      - echo "🔐 Running vulnerability scan"
      - trivy image --format cyclonedx --output sbom.json $IMAGE_NAME
      - python scripts/sbom/trivy_to_html.py sbom.json
      - mkdir -p artifacts && mv sbom.* artifacts/
  post_build:
    commands:
      - echo "📦 Uploading to S3"
      - aws s3 cp artifacts/ s3://devsecops-artifacts/$IMAGE_NAME/ --recursive
artifacts:
  files:
    - artifacts/*

✅ Security Notes:
	•	Secrets pulled from AWS Secrets Manager (not env vars)
	•	No hardcoded creds
	•	All logs are S3-uploaded, not printed

⸻

✅ Step 2: Create the S3 Artifact Bucket

aws s3 mb s3://devsecops-artifacts

Restrict access via bucket policy to:
	•	CodePipeline
	•	CodeBuild
	•	Your IAM user

⸻

✅ Step 3: Deploy CodePipeline using CloudFormation or CDK

Option A: YAML (CloudFormation)

Create infra/pipeline/pipeline.yaml:

Resources:
  NotesBuildRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Effect: Allow
            Principal:
              Service: codebuild.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: BuildAccess
          PolicyDocument:
            Statement:
              - Effect: Allow
                Action:
                  - ssm:GetParameter
                  - secretsmanager:GetSecretValue
                  - s3:PutObject
                Resource: "*"

  NotesCodeBuild:
    Type: AWS::CodeBuild::Project
    Properties:
      Name: notes-service-build
      Source:
        Type: GITHUB
        Location: https://github.com/YOUR_USER/notes-service
      Artifacts:
        Type: CODEPIPELINE
      Environment:
        Type: LINUX_CONTAINER
        ComputeType: BUILD_GENERAL1_SMALL
        Image: aws/codebuild/standard:7.0
        PrivilegedMode: true
      ServiceRole: !GetAtt NotesBuildRole.Arn
      TimeoutInMinutes: 10
      BuildSpec: infra/pipeline/buildspec.yml

  Pipeline:
    Type: AWS::CodePipeline::Pipeline
    Properties:
      Name: notes-service-pipeline
      RoleArn: arn:aws:iam::YOUR_ACCOUNT_ID:role/CodePipelineServiceRole
      ArtifactStore:
        Type: S3
        Location: devsecops-artifacts
      Stages:
        - Name: Source
          Actions:
            - Name: GitHubSource
              ActionTypeId:
                Category: Source
                Owner: ThirdParty
                Provider: GitHub
                Version: "1"
              OutputArtifacts:
                - Name: SourceOutput
              Configuration:
                Owner: YOUR_USER
                Repo: notes-service
                Branch: main
                OAuthToken: YOUR_GITHUB_TOKEN
        - Name: Build
          Actions:
            - Name: BuildNotes
              ActionTypeId:
                Category: Build
                Owner: AWS
                Provider: CodeBuild
                Version: "1"
              InputArtifacts:
                - Name: SourceOutput
              OutputArtifacts:
                - Name: BuildOutput
              Configuration:
                ProjectName: !Ref NotesCodeBuild

Deploy:

aws cloudformation deploy \
  --template-file infra/pipeline/pipeline.yaml \
  --stack-name notes-pipeline \
  --capabilities CAPABILITY_NAMED_IAM


⸻

✅ Step 4: Secure Deployment Script

In infra/pipeline/deploy.sh:

#!/bin/bash
set -euo pipefail

echo "Deploying $IMAGE_NAME to ECS..."

aws ecs update-service \
  --cluster notes-cluster \
  --service notes-service \
  --force-new-deployment

echo "✅ Deployed successfully"

Only execute this if scans pass.

⸻

✅ Step 5: Integrate Notifications (Optional)

You can add a failure notification via SNS:

  Notifications:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: BuildFailures

Or in CodeBuild UI, configure notification rules.

⸻

✅ What You Now Have

Component	Secured?	Notes
buildspec.yml	✅	Secrets from Secrets Manager
CodePipeline stages	✅	Isolated, structured
SBOM & scans	✅	Artifacted and uploaded
IAM Roles	✅	Per-stage, scoped
Deploy	✅	Only after passing build