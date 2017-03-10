# Mandatory
module "allspark" {
  source  = "github.com/broomyocymru/tf_azurerm_allspark"
  azurerm_subscription_id = "${var.azurerm_subscription_id}"
  azurerm_client_id = "${var.azurerm_client_id}"
  azurerm_client_secret = "${var.azurerm_client_secret}"
  azurerm_tenant_id = "${var.azurerm_tenant_id}"
}
