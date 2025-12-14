variable "ecs_cluster_name" {
  type    = string
}

variable "ecs_service_name" {
  type    = string
}

variable "max_tasks" {
  type    = number
}

variable "min_tasks" {
  type    = number
}

variable "sqs_queue_arn" {
  type    = string
}