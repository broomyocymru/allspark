# Prerequisites
* [Terraform](https://www.terraform.io/downloads.html) >= 0.8.8
* [Python](https://www.python.org/) >=2.10 (python 3 is currently still preview for ansible)
* [Ansible](http://docs.ansible.com/ansible/intro_installation.html#latest-releases-via-pip) >= 2.2


# Installation
git clone "github.com/broomyocymru/allspark"
./install.sh

# Getting Started
link to docs


# allspark usage
init - "cloud settings, prompts based on first answer then generates main.tf, terraform.tfvars and variables
add <package> <name> - adds package to allspark.state and runs terraform get / ansible-galaxy install
remove <package> <name> - removes package from allspark.state
update - perform updates to allspark.state using terraform apply / ansible-playbook
