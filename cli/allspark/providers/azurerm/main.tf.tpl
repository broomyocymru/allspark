# Mandatory
provider "azurerm" {
  subscription_id = "${var.azurerm_subscription_id}"
  client_id       = "${var.azurerm_client_id}"
  client_secret   = "${var.azurerm_client_secret}"
  tenant_id       = "${var.azurerm_tenant_id}"
}

module "allspark" {
  source  = "github.com/broomyocymru/tf_azurerm_allspark"
}
