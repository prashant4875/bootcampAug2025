module "networking" {
  source = "./modules/networking"

  vpc_cidr        = var.vpc_cidr
  subnet_cidr_list = var.subnet_cidr_list
  common_tags = local.common_tags
  prefix = local.prefix
  aws_region = data.aws_region.current.name

}

module "db" {
    source = "./modules/db-tier"

    vpc_id         = module.networking.vpc_id
    private_subnet_a = module.networking.private_subnet_id
    private_subnet_b = module.networking.aws_subnet_private_b_id
    private_subnet_cidr = module.networking.private_subnet_cidr
    db_name = var.db_name
    db_username = var.db_username
    common_tags = local.common_tags
    prefix = local.prefix
}

module "web-tier" {
  source = "./modules/web-tier"

  vpc_id = module.networking.vpc_id
  vpc_cidr = var.vpc_cidr
  public_subnet = module.networking.public_subnet_id
  instance_type = var.instance_type
  common_tags = local.common_tags
  prefix = local.prefix
  aws_region = data.aws_region.current.name
  aws_ami = data.aws_ami.amazon_linux.id
}

module "app-tier" {
  source = "./modules/app-tier"

  private_subnet = module.networking.private_subnet_id
  instance_type = var.instance_type
  ssh_security_group = module.web-tier.security_group_id
  common_tags = local.common_tags
  prefix = local.prefix
  aws_region = data.aws_region.current.name
  aws_ami = data.aws_ami.amazon_linux.id
}

