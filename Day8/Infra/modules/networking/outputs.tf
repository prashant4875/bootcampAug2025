output "vpc_id" {
  value       = aws_vpc.main.id
  description = "The ID of the VPC"
}

output "public_subnet_id" {
  value       = aws_subnet.public.id
  description = "The ID of the public subnet"
}

output "private_subnet_id" {
  value       = aws_subnet.private.id
  description = "The ID of the private subnet"
}

output "private_subnet_cidr" {
  value       = aws_subnet.private.cidr_block
  description = "The CIDR block of the private subnet"
}

output "aws_subnet_private_b_id" {
  value       = aws_subnet.private_b.id
  description = "The ID of the private subnet in AZ b"
}