module "s3" {
  source = "./modules/s3"

  bucket_name = "${data.aws_caller_identity.current.account_id}-lambda-layers-bucket"
}

module "lambda_layer_s3" {
  for_each = local.lambda_layers
  source   = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name          = each.key
  description         = each.value.description
  compatible_runtimes = each.value.compatible_runtimes
  runtime             = "python"

  source_path = {
    path             = "${path.module}/../${each.value.path}",
    pip_requirements = true,
    prefix_in_zip    = "python"
  }

  store_on_s3 = true
  s3_bucket   = module.s3.s3_bucket_id
}

module "lambda_functions" {
  for_each = local.lambda_functions
  source   = "terraform-aws-modules/lambda/aws"

  function_name = each.key
  handler       = each.value.handler
  runtime       = each.value.runtime
  source_path   = "${path.module}/../${each.value.path}"
  publish       = true
  timeout       = 60

  layers = [
    for layer_name in each.value.layers : module.lambda_layer_s3[layer_name].lambda_layer_arn
  ]
}