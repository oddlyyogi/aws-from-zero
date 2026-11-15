# AWS from Zero: Photo Notes

The code for the **AWS** video course. One small app, Photo Notes (notes that can carry photos), grows on an AWS
Free plan account: a budget and alerts, IAM policies, the CLI and boto3, a first EC2 server, its own VPC, S3 for
photos, RDS and DynamoDB, a serverless API on Lambda, and more in later chapters.

The root of this repository is the project as it stands after the latest finished chapter. Each chapter's finished
project is in [`chapters/`](chapters). Policies and settings files use placeholders such as `ACCOUNT_ID`, `BUCKET` and
`TOPIC_ARN`; the videos fill them in with `sed` into a `build/` folder that git ignores, so no account details are ever
committed.

Everything runs in one Region, `us-east-2`. Sign in with `aws login` (AWS CLI v2); no access keys are needed. Each
chapter deletes what it creates, so follow along and clean up the same way.

| # | Chapter | Folder |
|---|---------|--------|
| 1 | Your Free AWS Account, Safely | [chapters/01-your-free-aws-account-safely](chapters/01-your-free-aws-account-safely) |
| 2 | IAM: Users, Roles and Policies | [chapters/02-iam-users-roles-and-policies](chapters/02-iam-users-roles-and-policies) |
| 3 | The AWS CLI, CloudShell and boto3 | [chapters/03-the-aws-cli-cloudshell-and-boto3](chapters/03-the-aws-cli-cloudshell-and-boto3) |
| 4 | EC2: Your First Server | [chapters/04-ec2-your-first-server](chapters/04-ec2-your-first-server) |
| 5 | Networking with VPC | [chapters/05-networking-with-vpc](chapters/05-networking-with-vpc) |
| 6 | S3: Storage for Photos | [chapters/06-s3-storage-for-photos](chapters/06-s3-storage-for-photos) |
| 7 | Databases: RDS and DynamoDB | [chapters/07-databases-rds-and-dynamodb](chapters/07-databases-rds-and-dynamodb) |
| 8 | Serverless: Lambda and API Gateway | [chapters/08-serverless-lambda-and-api-gateway](chapters/08-serverless-lambda-and-api-gateway) |
| 9 | Messaging: SQS, SNS and EventBridge | [chapters/09-messaging-sqs-sns-and-eventbridge](chapters/09-messaging-sqs-sns-and-eventbridge) |
| 10 | Containers: ECR and ECS Fargate | [chapters/10-containers-ecr-and-ecs-fargate](chapters/10-containers-ecr-and-ecs-fargate) |
| 11 | Monitoring and Audit: CloudWatch and CloudTrail | [chapters/11-monitoring-and-audit-cloudwatch-and-cloudtrail](chapters/11-monitoring-and-audit-cloudwatch-and-cloudtrail) |
| 12 | CDN, DNS and HTTPS: CloudFront, ACM and Route 53 | coming soon |
| 13 | Infrastructure as Code: CloudFormation and CDK | [chapters/13-infrastructure-as-code-cloudformation-and-cdk](chapters/13-infrastructure-as-code-cloudformation-and-cdk) |
| 14 | Security Essentials: KMS, Secrets and WAF | [chapters/14-security-essentials-kms-secrets-and-waf](chapters/14-security-essentials-kms-secrets-and-waf) |
| 15 | Deploy with GitHub Actions, Then Clean Up | coming soon |

## Versions

AWS CLI v2 2.40.3, Python 3.12 locally, boto3 1.44.3, Amazon Linux 2023, PostgreSQL 18.6 on RDS, Lambda python3.14.

## License

MIT
