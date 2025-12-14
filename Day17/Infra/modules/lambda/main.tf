############################################
# Archive Lambda Source Code (Zip)
############################################
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.root}/lambda/event.py"
  output_path = "${path.module}/lambda.zip"
}

############################################
# IAM Role for Lambda
############################################
resource "aws_iam_role" "lambda_role" {
  name = "event-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

############################################
# IAM Policy for Lambda to manage ECS
############################################
resource "aws_iam_policy" "lambda_policy" {
  name = "event-lambda-policy"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      # ECS Permissions
      {
        Effect   = "Allow",
        Action   = [
          "ecs:DescribeServices",
          "ecs:UpdateService"
        ],
        Resource = "*"
      },

      # SQS Permissions (MANDATORY)
      {
        Effect = "Allow",
        Action = [
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ],
        Resource = "*"
      },

      # CloudWatch Logs
      {
        Effect   = "Allow",
        Action   = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      }
    ]
  })
}

############################################
# Attach IAM Policy to Role
############################################
resource "aws_iam_role_policy_attachment" "lambda_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

############################################
# Lambda Function
############################################
resource "aws_lambda_function" "event_lambda" {
  function_name = "event-function"
  handler       = "event.handler"
  runtime       = "python3.11"

  role          = aws_iam_role.lambda_role.arn
  timeout       = 30

  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  environment {
    variables = {
      ECS_CLUSTER_NAME = var.ecs_cluster_name
      ECS_SERVICE_NAME = var.ecs_service_name
      MIN_TASKS        = tostring(var.min_tasks)
      MAX_TASKS        = tostring(var.max_tasks)
    }
  }
}

resource "aws_lambda_event_source_mapping" "example" {
  event_source_arn = var.sqs_queue_arn
  function_name    = aws_lambda_function.event_lambda.arn
  batch_size       = 10

  scaling_config {
    maximum_concurrency = 100
  }
}

############################################
# Output Lambda ARN
############################################
output "lambda_arn" {
  value = aws_lambda_function.event_lambda.arn
}
