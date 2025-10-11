output "aws_instance_id" {
  value       = aws_instance.private.id
  description = "The ID of the web server instance"
}