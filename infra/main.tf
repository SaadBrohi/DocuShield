provider "aws" {
  region = "us-east-1"
}

# 1. S3 Bucket for Documents
resource "aws_s3_bucket" "docs" {
  bucket = "docushield-docs-${random_id.suffix.hex}"
}

resource "random_id" "suffix" {
  byte_length = 4
}

# 2. DynamoDB Table for Results
resource "aws_dynamodb_table" "audit" {
  name           = "DocuShieldAudit"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "document_id"

  attribute {
    name = "document_id"
    type = "S"
  }
}

# 3. EKS Cluster (Simplified)
# Note: Real EKS requires VPC, Subnets, IAM Roles. 
# This is a minimal example wrapper using a module would be better.

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "docushield-cluster"
  cluster_version = "1.27"

  cluster_endpoint_public_access  = true

  vpc_id                   = "vpc-12345678" # placeholder
  subnet_ids               = ["subnet-abc", "subnet-xyz"] # placeholder

  eks_managed_node_groups = {
    default = {
      min_size     = 1
      max_size     = 3
      desired_size = 2
      instance_types = ["t3.medium"]
    }
  }
}

# 4. IAM Roles for Service Accounts (IRSA)
# Grant access to S3 and Textract for the backend pod

module "irsa" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role-for-service-accounts-eks"
  
  role_name = "docushield-backend-role"
  
  role_policy_arns = {
    AmazonS3FullAccess = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
    AmazonTextractFullAccess = "arn:aws:iam::aws:policy/AmazonTextractFullAccess"
    AmazonDynamoDBFullAccess = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
  }

  oidc_providers = {
    main = {
      provider_arn               = module.eks.oidc_provider_arn
      namespace_service_accounts = ["default:backend-account"]
    }
  }
}
