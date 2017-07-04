# Mandatory
provider "azurerm" {
  subscription_id = "${var.azurerm_subscription_id}"
  client_id       = "${var.azurerm_client_id}"
  client_secret   = "${var.azurerm_client_secret}"
  tenant_id       = "${var.azurerm_tenant_id}"
}

module "allspark" {
  source            = "github.com/broomyocymru/tf_azurerm_allspark_vpc"
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
