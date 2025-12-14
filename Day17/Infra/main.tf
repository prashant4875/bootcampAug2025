terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.region
}

terraform {
  backend "s3" {
  }
}

data "template_file" "services" {
    for_each = { for svc in local.ecs_services : svc.name => svc }
    
    template = file(each.value.template_file)
    
    vars = each.value.vars
}

module "networking" {
    source = "./modules/networking"
    
    environment = var.environment
    availability_zones = data.aws_availability_zones.available_zones.names
}

module "iam" {
    source = "./modules/iam"
    
    environment = var.environment
}

module "ecs_cluster" {
    source = "./modules/ecs"
    
    app_name                        = var.app_name
    environment                     = var.environment
    nginx_cpu                       = var.nginx_cpu
    nginx_memory                    = var.nginx_memory
    ecs_task_execution_role_arn     = module.iam.ecs_task_execution_role_arn
    template_file                   = data.template_file.services["nginx-service"].rendered
    subnets                         = module.networking.private_subnet_ids
    security_group_id               = module.networking.nginx_security_group_id

}

module "s3" {
    source = "./modules/s3"
    
    environment = var.environment
}

module "lambda" {
    source = "./modules/lambda"
    
    ecs_cluster_name              = module.ecs_cluster.ecs_cluster_name
    ecs_service_name              = module.ecs_cluster.ecs_service_name
    min_tasks                    = 1
    max_tasks                    = 10
    sqs_queue_arn                = module.s3.sqs_queue_arn
}
