output "aws_s3_bucket_name" {
  value = aws_s3_bucket.s3_bucket.bucket
  description = "Name of the S3 bucket name"
}

output "aws_region" {
  value = aws_s3_bucket.s3_bucket.region
  description = "Name of the AWS region"
}