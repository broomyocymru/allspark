#!/bin/bash
# install.sh: Script to setup allspark

# define usage function
check_installed(){
  if ! type "$1" > /dev/null; then
    echo "$1 must be installed"
    exit 1
  fi
}

echo "Checking prereqs are installed..."
check_installed "python"
check_installed "terraform"

echo "Installing AllSpark cli..."
# todo - create in a virtualenv !!!!
pip install -r ./cli/requirements.txt --upgrade
pip install -e ./cli

echo "Run 'allspark init' to generate a new project"
exit 0
