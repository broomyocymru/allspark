import click
from allspark.core import util, logger
from allspark.providers import api


@click.command('update')
@click.option('--dry', is_flag=True)
@click.option('--batch', is_flag=True)
def cli(dry, batch):
    """Update AllSpark setup"""
    api.update(dry, batch)
