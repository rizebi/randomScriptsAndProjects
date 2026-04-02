module "ec2_instance_1" {
  source        = "./modules/ec2-instance"
  ami           = "ami-0ca5b159cbf5fe177"
  instance_type = "t2.micro"
  instance_name = "my-ec2-instance-1"
}