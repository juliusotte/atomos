data "aws_iam_policy_document" "s3_bucket_policy_document" {
  statement {
    sid    = "AddPerm"
    effect = "Allow"
    principals {
      identifiers = ["*"]
      type        = "AWS"
    }
    actions = ["s3:GetObject"]
    resources = [
      aws_s3_bucket.s3_bucket.arn,
      "${aws_s3_bucket.s3_bucket.arn}/*",
    ]
  }
}

data "aws_acm_certificate" "ssl_cert" {
  domain   = var.root_domain_name
  statuses = ["ISSUED"]
  tags     = var.resource_tags
}

data "aws_route53_zone" "zone" {
  name         = var.root_domain_name
  private_zone = false
}