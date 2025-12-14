variable "region" {
  type    = string
}
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

variable "nginx_template_file" {
  type    = string
}

variable "ecs_task_execution_role_arn" {
    type    = string
}