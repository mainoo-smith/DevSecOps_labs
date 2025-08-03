Title: “Detect, Break, and Harden: Real-World IaC Security Scenarios”

🎯 Goal
This lab simulates what happens when:

A team member adds insecure changes to infrastructure

A bad IaC policy goes unnoticed in a PR

Cloud resources are manually changed (drift)

You accidentally commit secrets

You’ll be the DevSecOps engineer responsible for catching and fixing these before deployment or audit.

🧩 Scenario Setup
You’ve already built secure infrastructure in Terraform, CDK, and CloudFormation.
Now you’ll:

Introduce intentional vulnerabilities

Detect them with security tools

Enforce policy gates before deploy

Simulate cloud drift and reconcile changes

🧱 Section 1: Terraform Misconfiguration + Detection
🔧 A. Inject Insecure Config
Open ecs.tf and add the following security vulnerability:

resource "aws_security_group" "open_all" {
  name        = "open-all-sg"
  description = "Opens all ports (bad)"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
What’s wrong:

Opens all TCP ports to the world (0.0.0.0/0)

Egress is unrestricted

Violates principle of least privilege and PCI/ISO/OWASP rules

🔍 B. Run Checkov
checkov -d .
✅ Expected output:

Check: CKV_AWS_260: "Security group allows unrestricted ingress"
Result: FAILED
File: ecs.tf:1
...
💡 Why Checkov?
It codifies security policies into rules. You can enforce this in your CI pipelines to block bad merges or deploys.

🛠 C. Fix It
Update the security group:

ingress {
  from_port   = 443
  to_port     = 443
  protocol    = "tcp"
  cidr_blocks = ["10.0.0.0/16"] # internal only
}
Run Checkov again:

checkov -d .
✅ Should pass now.

🧱 Section 2: CloudFormation Secret Leak + Linting
🔧 A. Inject Secret in Template
In stack.yaml, simulate a mistake:

DBPassword:
  Type: AWS::SSM::Parameter
  Properties:
    Name: /notestream/db_password
    Type: String
    Value: 'super-secret-plaintext-password'
🔍 B. Run cfn-lint and cfn_nag
cfn-lint stack.yaml
Then:

cfn_nag_scan --input-path stack.yaml
✅ Expected warnings:

W58: Parameter DBPassword should not use plain-text values
🧠 Use NoEcho: true and encrypted SSM parameters to store real secrets. Never commit plaintext values.

🧱 Section 3: AWS CDK Insecure Defaults + cdk-nag
🔧 A. Add Open SG in CDK
In infra_stack.py:

sg = ec2.SecurityGroup(self, "BadSG", vpc=vpc, allow_all_outbound=True)
sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Open SSH access")
🔍 B. Add cdk-nag to Detect It
Install:

pip install cdk-nag
Update your stack:

from cdk_nag import AwsSolutionsChecks
Aspects.of(self).add(AwsSolutionsChecks())
Run:

cdk synth
✅ Should show something like:

[Warning] AwsSolutions-EC23: Security group allows ingress from 0.0.0.0/0 to port 22
🛠 C. Fix It
Update rule:

sg.add_ingress_rule(ec2.Peer.ipv4("10.0.0.0/16"), ec2.Port.tcp(22), "Internal only")
🧱 Section 4: Drift Detection with Terraform
🐛 A. Simulate Drift
Go to the AWS Console → change a subnet name manually (or add an extra tag).

🔍 B. Detect Drift
terraform plan
✅ Output:

~ aws_subnet.public[0]
      tags.Name: "old" => "new"
🧠 Why this matters:
Manual changes break IaC consistency. Plan should always reflect infra state.

🛠 C. Reconcile
Option 1: Accept drift

terraform refresh
Option 2: Enforce source-of-truth

terraform apply
🧱 Section 5: Commit Secrets Accidentally + Detect
🔧 A. Simulate a Leaked Secret
echo "AWS_SECRET_ACCESS_KEY=1234567890" >> .env
git add .env
git commit -m "oops"
🔍 B. Run GitLeaks
gitleaks detect --source .
✅ Output:

Secret detected: AWS_SECRET_ACCESS_KEY
🔐 Add gitleaks to pre-commit or CI to block merge on exposed secrets.

✅ Challenge Completion Checklist
Challenge	Status
Insecure SG in Terraform	✅ Detected with Checkov & tfsec
Plaintext secret in CF	✅ Flagged with cfn-lint & cfn_nag
Overly open rule in CDK	✅ Caught with cdk-nag
Secret committed to Git	✅ Detected with gitleaks
Manual infra drift	✅ Detected with Terraform plan
📘 Summary: DevSecOps IaC Maturity Practices
Practice	Benefit
Scan infra code pre-deploy	Catch CVEs & misconfigs early
Block secrets in source code	Prevent long-term breaches
Detect drift	Enforce single source of truth
Use tools across IaC flavors	Terraform, CDK, CFN all need enforcement
Shift-left via pipelines	Ensure Dev & Ops stay aligned with security
🔜 Next:

Security.md: Threat modeling misconfigurations & shared cloud risk

Reflection.md: CI/CD is policy enforcement, not just automation

Would you like to continue with the Security section of Week 5?

You said:
Yes
ChatGPT said:
Great — here's the annotated Security.md for Week 5, focused on the core DevSecOps risks and controls associated with Infrastructure as Code (IaC), across Terraform, CDK, CloudFormation, and SAM.