variable "app_name" {
  type    = string
}

variable "nginx_cpu" {
  type    = number
}

variable "nginx_memory" {
  type    = number
}

variable "environment" {
  type    = string
}

variable "template_file" {
  type    = string
}

variable "ecs_task_execution_role_arn" {
    type    = string
}

variable "subnets" {
  type   = list(string)
}

variable "security_group_id" {
  type    = string
  
}