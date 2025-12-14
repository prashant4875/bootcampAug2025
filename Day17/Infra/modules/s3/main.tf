data "aws_iam_policy_document" "queue" {
  ### S3 -> SQS (SendMessage)
  statement {
    sid    = "AllowS3ToSendMessage"
    effect = "Allow"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions   = ["sqs:SendMessage"]
    resources = ["arn:aws:sqs:*:*:s3-event-notification-queue"]

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_s3_bucket.event-bucket.arn]
    }
  }

  ### Lambda -> SQS (Poll/Delete/Get)
  statement {
    sid    = "AllowLambdaToPollQueue"
    effect = "Allow"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage",
      "sqs:GetQueueAttributes",
      "sqs:ChangeMessageVisibility"
    ]

    resources = ["arn:aws:sqs:*:*:s3-event-notification-queue"]
  }
}


resource "aws_sqs_queue" "queue" {
  name   = "s3-event-notification-queue"
  policy = data.aws_iam_policy_document.queue.json
}

resource "aws_s3_bucket" "event-bucket" {
  bucket = "event-bucket-psb-2025"

  tags = {
    Name        = "My bucket"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.event-bucket.id

  queue {
    queue_arn     = aws_sqs_queue.queue.arn
    events        = ["s3:ObjectCreated:*"]
    filter_suffix = ".log"
  }
}