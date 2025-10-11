variable "vpc_cidr" {
  type    = string
}

variable "subnet_cidr_list" {
  type    = list(string)
}

variable "common_tags" {
  type    = map(string)
}

variable "prefix" {
  type    = string
}

variable "aws_region" {
  type    = string
}