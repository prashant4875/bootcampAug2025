resource "aws_instance" "private" {
  ami                    = var.aws_ami
  instance_type          = var.instance_type
  subnet_id              = var.private_subnet
  availability_zone      = "${var.aws_region}a"
  vpc_security_group_ids = [var.ssh_security_group, ]
  key_name               = "ssh-key"
  tags = merge(
    var.common_tags,
    tomap({ "Name" = "${var.prefix}-private-ec2" })
  )
}