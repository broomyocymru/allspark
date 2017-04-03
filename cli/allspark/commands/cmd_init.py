import click
import os
from allspark.core import config, util, logger
from allspark.providers import api

@click.command('init')
@click.argument('name')
@click.option('--path', prompt=False, default=os.getcwd())
@click.option('--provider', prompt=True, default=config.get("allspark.provider"),
              type=click.Choice(api.providers()))
def cli(name, path, provider):
    """Initiate an AllSpark Setup"""
    config.set("allspark.provider", provider)
    api.init(path + "/" + name , provider)
