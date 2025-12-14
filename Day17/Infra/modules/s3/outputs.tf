output "sqs_queue_id" {
  description = "URL of the SQS Queue for S3 Event Notifications"
  value       = aws_sqs_queue.queue.id
}

output "sqs_queue_arn" {
  description = "ARN of the SQS Queue for S3 Event Notifications"
  value       = aws_sqs_queue.queue.arn
}

output "s3_bucket_name" {
  description = "Name of the S3 Bucket"
  value       = aws_s3_bucket.event-bucket.bucket
}
output "s3_bucket_arn" {
  description = "ARN of the S3 Bucket"
  value       = aws_s3_bucket.event-bucket.arn
}
