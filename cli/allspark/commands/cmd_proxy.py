import click
import os
from allspark.core import config, util, logger
from allspark.providers import api
from subprocess import Popen

@click.command('proxy')
@click.argument('name')
def cli(name):
    """Proxy to an AllSpark VM (ssh)"""
    if name == "list":
        api.list_vms()
    else:
        print("use: ssh -F software/ssh_config.conf " + api.get_vm_ip(name))
