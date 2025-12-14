locals {
  lambda_info = [
    {
      name    = "lambda1"
      path    = "lambda/lambda1"
      handler = "main.lambda_handler"
      runtime = "python3.12"
      layers  = ["layer1", "layer2"]
    },
    {
      name    = "lambda2"
      path    = "lambda/lambda2"
      handler = "main.lambda_handler"
      runtime = "python3.12"
      layers  = ["layer2"]
    },
  ]

  layers_info = [
    {
      name                = "layer1"
      path                = "layers/layer1"
      description         = "pandas"
      compatible_runtimes = ["python3.12", "python3.13", "python3.11"]
    },
    {
      name                = "layer2"
      path                = "layers/layer2"
      description         = "openpyxl"
      compatible_runtimes = ["python3.12", "python3.13", "python3.11"]
    },
  ]

  lambda_functions = { for lambda in local.lambda_info : lambda.name => lambda }
  lambda_layers    = { for layer in local.layers_info : layer.name => layer }
}