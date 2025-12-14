region = "us-east-1"
app_name = "nginx"
nginx_cpu = 256
nginx_memory = 512
environment = "dev"
nginx_template_file = "./task-definitions/nginx-service.json.tpl"
ecs_task_execution_role_arn = "arn:aws:iam::123456789012:role/ecsTaskExecutionRole"