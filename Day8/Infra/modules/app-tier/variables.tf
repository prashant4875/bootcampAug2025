variable "private_subnet" {
  type    = string
}

variable "instance_type" {
  type = string
}

variable "ssh_security_group" {
  type = string
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

variable "aws_ami" {
  description = "The AMI to use for the EC2 instance"
  type        = string
}