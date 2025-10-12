variable "prefix" {
  default = "main"
}

variable "project" {
  default = "devops-101"
}

variable "contact" {
  default = "bhadoria998@gmail.com"
}

variable "region" {
  default = "eu-west-1"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "subnet_cidr_list" {
  type    = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24",  "10.0.3.0/24"]
}

variable "db_name" {
  description = "The name of the RDS database"
  type        = string
  default     = "mydatabase"
}

variable "db_username" {
  description = "The username for the RDS database"
  type        = string
  default     = "admin"
}

variable "instance_type" {
  default = "t2.micro"
}