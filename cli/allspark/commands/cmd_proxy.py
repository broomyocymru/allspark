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
        print("For SSH")
        print("use: ssh -F software/ssh_config.conf " + api.get_vm_ip(name))
        print("")
        print("For RDP (ssh tunnel through bastion) then connect a RDP client to 127.0.0.1:3389")
        print("use: ssh -F software/ssh_config.conf -L 3389:" + api.get_vm_ip(name) +":3389")
