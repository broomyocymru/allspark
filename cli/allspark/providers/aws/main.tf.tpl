# Mandatory
provider "aws" {
  access_key  = "${var.aws_access_key}"
  secret_key  = "${var.aws_secret_key}"
  region      = "${var.location}"
}

module "allspark" {
  source            = "github.com/broomyocymru/tf_aws_allspark_vpc"
  name              = "allspark"
  bastion_enabled   = "1"
  bastion_config    = {
    username = "<random_username>"
    password = "<random_password>"
  }
}

output "allspark_vpc_out" {
  value = "${module.allspark.allspark_data}"
}

output "allspark_bastion" {
  value = "${module.allspark.bastion_data}"
}
