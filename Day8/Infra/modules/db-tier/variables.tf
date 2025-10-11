variable "vpc_id" {
  type    = string
}

variable "private_subnet" {
  type    = string
}

variable "db_name" {
  description = "The name of the RDS database"
  type        = string
}

variable "db_username" {
  description = "The username for the RDS database"
  type        = string
}

variable "common_tags" {
  type    = map(string)
}

variable "prefix" {
  type    = string
}
