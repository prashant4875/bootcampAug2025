terraform {
  backend "s3" {
    bucket  = "my-backend-devops101-terraform-psb"
    key     = "tfstate/terraform.tfstate"
    region  = "eu-west-1"
    encrypt = true
    #dynamodb_table = "terraform-lock-table"
  }
}