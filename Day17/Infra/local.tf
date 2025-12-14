locals {
    ecs_services = [
        {
            name = "nginx-service"
            cpu = var.nginx_cpu
            memory = var.nginx_memory
            template_file = var.nginx_template_file
            vars = {
                environment = var.environment
            }
        }
    ]
}