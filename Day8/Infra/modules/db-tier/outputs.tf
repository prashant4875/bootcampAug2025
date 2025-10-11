output "rds_endpoint" {
  value       = aws_db_instance.postgres.endpoint
  description = "The endpoint of the RDS instance"
}