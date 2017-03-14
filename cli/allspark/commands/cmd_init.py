import click
from allspark.core import config, util, logger
from allspark.providers import api

@click.command('init')
@click.option('--name', prompt=True)
@click.option('--provider', prompt=True, default=config.get("allspark.provider"),
              type=click.Choice(api.providers()))
def cli(name, provider):
    """Initiate an AllSpark Setup"""
    config.set("allspark.provider", provider)
    api.init(name, provider)
