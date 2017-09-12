# AllSpark ![build-status](https://travis-ci.org/broomyocymru/allspark.svg?branch=master)
Bringing infrastructure to life whilst avoiding lock-in!


### Prerequisites
AllSpark depends on the following software being installed
* [Terraform](https://www.terraform.io/downloads.html) >= 0.10.2
* [Python](https://www.python.org/) >=2.10 (python 3 is currently still preview for ansible)
* [Ansible](http://docs.ansible.com/ansible/intro_installation.html#latest-releases-via-pip) >= 2.2


### Install
Older pip versions have issues with some of the dependencies, upgrading is optional.
```bash
pip install --upgrade pip
pip install allspark
```

### Upgrade
```bash
pip install allspark -U
```

### Usage

Create a new Allspark project and move to its root directory. Open the terraform variables file and add the credentials for your cloud provider.
```bash
allspark init <project_name>
cd <project_name>
nano infrastructure/terraform.tfvars
```

List the installed sparks and then see what sparks are available for your cloud provider.
```bash
allspark sparks list  
allspark sparks available
```

Add a spark to your project, you'll be prompted for a name (and eventually any addition configurations it requires). Running list should now show you've added a spark.
```bash
allspark sparks add <spark_name>
allspark sparks list
```

Apply your configuration, optionally use -f to force packages to update from source (by default terraform and ansible modules will be cached otherwise).
```bash
allspark update [-f]
```

Modify your configuration in the allspark.json file at the root of the project. This stores the state of the packages you've added and any random username / passwords generated.

### Developer Setup
Developer setup will install the Python module in editable mode.
```bash
git clone "https://github.com/broomyocymru/allspark"
./install.sh
```
