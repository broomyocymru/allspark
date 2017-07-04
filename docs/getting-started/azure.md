# Microsoft Azure

## Provider Details
* subscription_id
* client id
* client secret
* tenant id

## Creating a Service Principal
https://github.com/Azure/acs-engine/blob/master/docs/serviceprincipal.md

A Service Principal is linked to an account in Azure Active Directory and delegates permissions to the app running with the service principal client id and secret. Terraform itself needs a security account to run. Kubernetes instances on their own also need a service principal.

Using the Azure CLI
```bash
az login
az account set --subscription="${SUBSCRIPTION_ID}"
az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/${SUBSCRIPTION_ID}"
```
