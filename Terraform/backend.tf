terraform {
  backend "s3" {
    # Edit the bucket name and region
    bucket         = "backend-terraform-tvnews"
    key            = "global/s3/terraform.tfstate"
    region         = "us-east-1"
  }
}