import click
from allspark.core import util, logger
from allspark.providers import api


@click.command('update')
@click.option('-d', '--dry', is_flag=True)
@click.option('-b', '--batch', is_flag=True)
@click.option('-f', '--force', is_flag=True)
def cli(dry, batch, force):
    """Update AllSpark setup"""
    api.update(dry, batch, force)
