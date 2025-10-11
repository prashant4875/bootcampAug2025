resource "aws_security_group" "ssh" {

  description = "allow ssh to ec2"
  name        = "${var.prefix}-ssh_access"
  vpc_id      = var.vpc_id

  ingress {
    protocol    = "tcp"
    from_port   = 22
    to_port     = 22
    cidr_blocks = [var.vpc_cidr]
    #We can limit the ip here
  }
  tags = var.common_tags

}

resource "aws_instance" "public" {
  ami                    = var.aws_ami
  instance_type          = var.instance_type
  subnet_id              = var.public_subnet
  vpc_security_group_ids = [aws_security_group.ssh.id, ]
  key_name               = "ssh-key"
  availability_zone      = "${var.aws_region}a"

  tags = merge(
    var.common_tags,
    tomap({ "Name" = "${var.prefix}-public-ec2" })
  )
}