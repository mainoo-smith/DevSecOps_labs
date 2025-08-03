(continued)
🧪 ECS Task Definition with Secrets Injection (CDK)
// lib/auth-service-stack.ts

import * as ecs from 'aws-cdk-lib/aws-ecs';
import * as secrets from 'aws-cdk-lib/aws-secretsmanager';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs_patterns from 'aws-cdk-lib/aws-ecs-patterns';

export class AuthServiceStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const vpc = ec2.Vpc.fromLookup(this, 'VPC', { isDefault: true });

    const cluster = new ecs.Cluster(this, 'Cluster', { vpc });

    const secret = secrets.Secret.fromSecretNameV2(
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
✅ Explanation:

The secret is passed securely into the container as an environment variable (DB_SECRET)

Only the taskRole is granted permission to read the secret — enforcing least privilege

🏗️ CodePipeline + CodeBuild (CDK)
Add to lib/pipeline-stack.ts:

import * as codepipeline from 'aws-cdk-lib/aws-codepipeline';
import * as codepipeline_actions from 'aws-cdk-lib/aws-codepipeline-actions';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as s3 from 'aws-cdk-lib/aws-s3';

const artifactBucket = new s3.Bucket(this, 'ArtifactBucket', {
  versioned: true,
  removalPolicy: cdk.RemovalPolicy.DESTROY,
});

const sourceOutput = new codepipeline.Artifact();
const buildOutput = new codepipeline.Artifact();

const project = new codebuild.PipelineProject(this, 'BuildProject', {
  buildSpec: codebuild.BuildSpec.fromObject({
    version: '0.2',
    phases: {
      install: {
        commands: ['npm install'],
      },
      build: {
        commands: ['npm run build', 'npm run lint'],
      },
    },
    artifacts: {
      files: ['**/*'],
    },
  }),
});

new codepipeline.Pipeline(this, 'Pipeline', {
  artifactBucket,
  stages: [
    {
      stageName: 'Source',
      actions: [
        new codepipeline_actions.GitHubSourceAction({
          actionName: 'GitHub',
          owner: 'your-org',
          repo: 'your-repo',
          oauthToken: cdk.SecretValue.secretsManager('github-token'),
          output: sourceOutput,
          branch: 'main',
        }),
      ],
    },
    {
      stageName: 'Build',
      actions: [
        new codepipeline_actions.CodeBuildAction({
          actionName: 'CodeBuild',
          project,
          input: sourceOutput,
          outputs: [buildOutput],
        }),
      ],
    },
  ],
});
🌍 CDK Context for Multi-Environment Awareness
📄 cdk.json

{
  "context": {
    "envs": {
      "dev": {
        "account": "111111111111",
        "region": "us-west-2"
      },
      "staging": {
        "account": "222222222222",
        "region": "us-west-2"
      }
    }
  }
}
📄 bin/main.ts

const envName = process.env.ENV || 'dev';
const envConfig = app.node.tryGetContext('envs')[envName];

new AuthServiceStack(app, `AuthService-${envName}`, {
  env: {
    account: envConfig.account,
    region: envConfig.region,
  },
});
💡 Use ENV=staging cdk deploy to deploy into specific environment accounts with isolated stacks.

🔐 Fine-Grained IAM Role for ECS Tasks
Instead of giving ECS access to all logs/secrets, use inline IAM policy:

taskRole.addToPolicy(
  new iam.PolicyStatement({
    actions: ['secretsmanager:GetSecretValue'],
    resources: [secret.secretArn],
  })
);
📉 Drift Detection with driftctl
Install:

brew install driftctl
Run in Terraform root:

driftctl scan --from tfstate+s3://my-state-bucket/path/to/terraform.tfstate
🚨 Detects resources in AWS that are not in Terraform, helping prevent shadow infrastructure and drift.

💾 Terraform Remote State Backend
📄 backend.tf

terraform {
  backend "s3" {
    bucket         = "my-secure-terraform-state"
    key            = "dev/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
Let me know when you're ready and I’ll regenerate the Finalized Completion Checklist reflecting these corrected and added capabilities before we proceed to ChallengeLab.md.

You said:
Proceed 
ChatGPT said:
Perfect. Here's the finalized .md-formatted Completion Checklist that fully aligns with the enhanced and corrected Guided Lab for Week 10 – Infrastructure as Code (IaC) & Security.