resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(
    var.common_tags, 
    tomap({ Name = "${var.prefix}-vpc" })
  )
}

resource "aws_subnet" "public" {

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.subnet_cidr_list[0]
  map_public_ip_on_launch = true
  availability_zone = "${var.aws_region}a"

  tags = merge(
    var.common_tags, 
    tomap({ Name = "${var.prefix}-public-subnet" })
  )
}

resource "aws_subnet" "private" {

  vpc_id            = aws_vpc.main.id
  cidr_block        = var.subnet_cidr_list[1]
  availability_zone = "${var.aws_region}a"

  tags = merge(
    var.common_tags, 
    tomap({ Name = "${var.prefix}-private-subnet-a" })
  )
}

resource "aws_subnet" "private_b" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.subnet_cidr_list[2]
  availability_zone = "${var.aws_region}b"

  tags = merge(
    var.common_tags, 
    tomap({ Name = "${var.prefix}-private-subnet-b" })
  )
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.common_tags, 
    tomap({ Name = "${var.prefix}-igw" })
  )
}

resource "aws_eip" "public"{

  tags = merge(
    var.common_tags, 
    tomap({ Name = "${var.prefix}-eip" })
  )
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.public.id
  subnet_id     = aws_subnet.public.id

  tags = merge(
    var.common_tags, 
    tomap({ Name = "${var.prefix}-nat-gateway" })
  )

}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.common_tags, 
    tomap({ Name = "${var.prefix}-public-rt" })
  )
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    var.common_tags, 
    tomap({ Name = "${var.prefix}-private-rt" })
  )
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  subnet_id      = aws_subnet.private.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route" "public_internet_access" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}

resource "aws_route" "private_internet_access" {
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat.id
}


