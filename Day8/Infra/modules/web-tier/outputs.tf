output "aws_instance_id" {
  value       = aws_instance.public.id
  description = "The ID of the web server instance"
}

output "security_group_id" {
  value       = aws_security_group.ssh.id
  description = "The ID of the security group allowing SSH access"
}